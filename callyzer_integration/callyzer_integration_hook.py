from __future__ import unicode_literals
import frappe
from frappe import _
from frappe.integrations.utils import create_request_log,make_post_request
from frappe.utils import get_datetime,now_datetime,format_datetime,format_date,format_time,getdate, duration_to_seconds,format_duration
from datetime import timedelta
import datetime
from frappe.utils.password import get_decrypted_password
import json
import re
from frappe.utils.background_jobs import enqueue


def get_callyzer_configuration():
	if frappe.db.get_single_value("Callyzer Settings", "enabled"):
		callyzer_settings = frappe.get_doc("Callyzer Settings")
		return {
			"bearer_token": callyzer_settings.get_password(fieldname="bearer_token", raise_exception=False),
			"last_api_call_time": callyzer_settings.last_api_call_time,
			"call_history_url":callyzer_settings.call_history_url
		}
	return "disabled"


@frappe.whitelist()
def auto_pull_callyzer_logs():
	callyzer_settings=get_callyzer_configuration()
	if callyzer_settings!='disabled':
			fetch_callyzer_data_and_make_integration_request(callyzer_settings)
	return


def fetch_callyzer_data_and_make_integration_request(callyzer_settings):
	try:
		# prepare post data
		url= callyzer_settings.get('call_history_url')
		headers={"Authorization": "Bearer {0}".format(callyzer_settings.get('bearer_token'), raise_exception=False)}
		
		current_datetime=now_datetime()
		if callyzer_settings.get('last_api_call_time'):
			# overlap of 2 times
			start_time=get_datetime(callyzer_settings.get('last_api_call_time'))- datetime.timedelta(minutes=2)
			end_time=current_datetime
		else:
			start_time= current_datetime - datetime.timedelta(minutes=5)
			end_time=current_datetime

		DATE_FORMAT='%Y-%m-%d'
		TIME_FORMAT='%H:%M'
		data={
			"syncStartDate" : start_time.strftime(DATE_FORMAT),
			"syncEndDate" : end_time.strftime(DATE_FORMAT),
			"syncStartTime" : start_time.strftime(TIME_FORMAT),
			"syncEndTime" : end_time.strftime(TIME_FORMAT),
			"pageSize" : 50000		
		}	
		request_log_data={
			"syncStartDate" : start_time.strftime(DATE_FORMAT),
			"syncEndDate" : end_time.strftime(DATE_FORMAT),
			"syncStartTime" : start_time.strftime(TIME_FORMAT),
			"syncEndTime" : end_time.strftime(TIME_FORMAT),
			"pageSize" : 50000		,
			"reference_doctype":"Callyzer Call Log"
		}	

		# call URL
		integration_request=create_request_log(data=frappe._dict(request_log_data),integration_type="Remote",service_name="Callyzer")
		response = make_post_request(url, headers=headers, data=data)
		frappe.db.set_value('Integration Request', integration_request.name, 'output',json.dumps(response))

		output=frappe.db.get_value('Integration Request', integration_request.name, 'output')
		if not output:
			frappe.db.set_value('Integration Request', integration_request.name, 'status', 'Failed')
		else:
			# Iterate through response
			# example
			# { 'data': [
			# 			{'employee': 'Sudip Adhikari (6353532248)', 'client': 'Unknown (09163127901)', 'date': '15 Sep 2021', 'time': '09:22:43', 'duration': '0h 0m 44s', 'callType': 'Outgoing', 'note': None}, 
			# 			{'employee': 'Mayur Chauhan (7434881313)', 'client': 'Unknown (07869544660)', 'date': '15 Sep 2021', 'time': '09:03:58', 'duration': None, 'callType': 'Missed', 'note': None}
			# 		 ], 
			#   'message': None, 
			#   'recordsTotal': 2, 
			#   'recordsFiltered': 2, 
			#   'srNoCounterStart': 0
			# }			
			recordsTotal=frappe._dict(response).get('recordsTotal')
			if recordsTotal!=0:
				for x ,y in frappe._dict(response).items():
					if x == 'data':
						for call_row in y:
							if	recordsTotal<100:
								callyzer_call_log=make_callyzer_call_log_records(call_row,integration_request.name)
							else:
								frappe.enqueue(make_callyzer_call_log_records,call_row=call_row,integration_request=integration_request.name, queue='long')
			frappe.db.set_value('Integration Request', integration_request.name, 'status', 'Completed')
			frappe.db.set_value('Callyzer Settings','Callyzer Settings', 'last_api_call_time', end_time)
			return
	except Exception as e:
		print(e)
		frappe.db.set_value('Integration Request', integration_request.name, 'status', 'Failed')
		if hasattr(e, 'response'):
			frappe.log_error(frappe.get_traceback()+'\n\n\n'+json.dumps(data)+'\n\n\n'+e.response.text, title=_('Callyzer Error'))
		else:
			frappe.log_error(frappe.get_traceback()+'\n\n\n'+json.dumps(data), title=_('Callyzer Error'))
			# set last time, as error is not with api cal but in data..so move ahead
			frappe.db.set_value('Callyzer Settings','Callyzer Settings', 'last_api_call_time', end_time)
		return		

def make_callyzer_call_log_records(call_row,integration_request):
	# pattern = "\((.*?)\)"
	# customer_mobile_search=re.search(pattern, call_row.get('client',None))
	customer_mobile=call_row.get('client',None).rsplit("(")[-1].strip(")").lstrip('0').rsplit("+91")[-1]
	customer_mobile=customer_mobile[-10:]
	employee_mobile=call_row.get('employee',None).rsplit("(")[-1].strip(")").lstrip('0')
	date=getdate(format_date(call_row.get('date',None),'yyyy-mm-dd'))
	time=format_time(call_row.get('time',None))
	existing_callyzer_call_log = frappe.db.get_value("Callyzer Call Log", {"customer_mobile": customer_mobile,"date":date,"time":time})
	if not existing_callyzer_call_log:
		callyzer_call_log=frappe.new_doc('Callyzer Call Log')
		callyzer_call_log.employee=call_row.get('employee',None)
		client=call_row.get('client',None)
		if len(client)>140:
			client=client[0:140]
		callyzer_call_log.client=client
		callyzer_call_log.date=date
		callyzer_call_log.time=format_time(call_row.get('time',None))
		callyzer_call_log.duration=duration_to_seconds(call_row.get('duration') if call_row.get('duration')!=None else '0s')
		callyzer_call_log.calltype=call_row.get('callType')
		callyzer_call_log.note=call_row.get('note',None)
		callyzer_call_log.employee_mobile=employee_mobile
		callyzer_call_log.customer_mobile=customer_mobile
		callyzer_call_log.raw_log=json.dumps(call_row)
		callyzer_call_log.integration_request=integration_request
		callyzer_call_log.save(ignore_permissions=True)
		return callyzer_call_log.name
	else:
		# Duplicate call record
		print('Duplicate')
		pass
	return	

@frappe.whitelist()
def load_lead_call_info(self,method):
		if self.mobile_no:	
			call_info = get_call_info(self.mobile_no)
			self.set_onload('call_info', call_info)	
# TIMEDIFF(DATE_FORMAT(min(addtime(call_log.date, call_log.time)) ,"%Y-%m-%d %H:%i"),DATE_FORMAT(lead.creation ,"%Y-%m-%d %H:%i")) as `first_call_response_time`,

def get_call_info(mobile_no):
	data = frappe.db.sql('''
select 
lead.name as lead_name,
lead.mobile_no as `customer_no`,
lead.creation as creation,
TIMESTAMPDIFF(SECOND,lead.creation,min(addtime(call_log.date, call_log.time))) as `first_call_response_time`,
min(addtime(call_log.date, call_log.time)) as `first_call`, 
max(addtime(call_log.date, call_log.time)) as `last_call`,
COUNT(call_log.name) as `total_count`,
COUNT(CASE WHEN call_log.calltype = 'Outgoing' THEN call_log.name ELSE NULL END) as `outgoing_count`,
COUNT(CASE WHEN call_log.calltype = 'Incoming' THEN call_log.name ELSE NULL END) as `incoming_count`,
COUNT(CASE WHEN call_log.calltype = 'Missed' THEN call_log.name ELSE NULL END) as `missed_count`,
COUNT(CASE WHEN call_log.calltype = 'Rejected' THEN call_log.name ELSE NULL END) as `rejected_count`
FROM  `tabCallyzer Call Log` call_log
inner join `tabLead` lead
on call_log.customer_mobile = lead.mobile_no 
WHERE lead.mobile_no=%s
group by lead.mobile_no
	''', (mobile_no),as_dict=True)
	result=data[0]	if data else None
	if result:
		if 'first_call_response_time' in result:
			result['first_call_response_time']=format_duration(result['first_call_response_time'])
	return  result