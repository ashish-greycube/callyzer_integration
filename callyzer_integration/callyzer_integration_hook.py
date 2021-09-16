from __future__ import unicode_literals
import frappe
from frappe import _
from frappe.integrations.utils import create_request_log,make_post_request
from frappe.utils import get_datetime,now_datetime,format_datetime,format_date,format_time,getdate, duration_to_seconds
from datetime import timedelta
import datetime
from frappe.utils.password import get_decrypted_password
import json
import re


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
			start_time=get_datetime(callyzer_settings.get('last_api_call_time'))- datetime.timedelta(minutes=2)
			# end_time=callyzer_settings.get('last_api_call_time')
			end_time=current_datetime
		else:
			start_time= current_datetime - datetime.timedelta(minutes=5)
			end_time=current_datetime

		DATE_FORMAT='%Y-%m-%d'
		TIME_FORMAT='%H:%M'
		data={
			"callStartDate" : start_time.strftime(DATE_FORMAT),
			"callEndDate" : end_time.strftime(DATE_FORMAT),
			"callStartTime" : start_time.strftime(TIME_FORMAT),
			"callEndTime" : end_time.strftime(TIME_FORMAT),
			"pageSize" : 50000		
		}	

		# call URL
		integration_request=create_request_log(data=frappe._dict(data),integration_type="Remote",service_name="Callyzer")
		response = make_post_request(url, headers=headers, data=data)
		frappe.db.set_value('Integration Request', integration_request.name, 'output',frappe._dict(response))

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
							callyzer_call_log=make_callyzer_call_log_records(call_row,integration_request.name)
			frappe.db.set_value('Integration Request', integration_request.name, 'status', 'Completed')
			frappe.db.set_value('Callyzer Settings','Callyzer Settings', 'last_api_call_time', end_time)
			return
	except Exception as e:
		print(e)
		frappe.db.set_value('Integration Request', integration_request.name, 'status', 'Failed')
		if hasattr(e, 'response'):
			frappe.log_error(frappe.get_traceback()+'\n\n\n'+e.response.text, title=_('Callyzer Error'))
		else:
			frappe.log_error(frappe.get_traceback(), title=_('Callyzer Error'))
			# set last time, as error is not with api cal but in data..so move ahead
			frappe.db.set_value('Callyzer Settings','Callyzer Settings', 'last_api_call_time', end_time)
		return		

def make_callyzer_call_log_records(call_row,integration_request):
	# pattern = "\((.*?)\)"
	# customer_mobile_search=re.search(pattern, call_row.get('client',None))
	customer_mobile=call_row.get('client',None).rsplit("(")[-1].strip(")")
	employee_mobile=call_row.get('employee',None).rsplit("(")[-1].strip(")")
	date=getdate(format_date(call_row.get('date',None)))
	time=format_time(call_row.get('time',None))
	existing_callyzer_call_log = frappe.db.get_value("Callyzer Call Log", {"customer_mobile": customer_mobile,"date":date,"time":time})
	if not existing_callyzer_call_log:
		callyzer_call_log=frappe.new_doc('Callyzer Call Log')
		callyzer_call_log.employee=call_row.get('employee',None)
		callyzer_call_log.client=call_row.get('client',None)
		callyzer_call_log.date=getdate(format_date(call_row.get('date',None)))
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