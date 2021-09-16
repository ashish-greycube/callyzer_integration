# Copyright (c) 2013, Frappe Technologies Pvt. Ltd. and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe import _, scrub

def execute(filters=None):
	columns = [
		{
			'fieldname': 'date',
			'label': _('Date'),
			'fieldtype': 'Date',
			'width': 100
		},
		{
				'label': _('Sales Person'),
				'options': 'Sales Person',
				'fieldname': 'sales_person',
				'fieldtype': 'Link',
				'width': 300
		},
		{
			'fieldname': 'first_call',
			'label': _('First Call'),
			'fieldtype': 'Time',
			'width': 80
		},		
		{
			'fieldname': 'outgoing_calls',
			'label': _('Outgoing#'),
			'fieldtype': 'Int',
			'width': 90
		},		
		{
			'fieldname': 'unique_calls',
			'label': _('Unique#'),
			'fieldtype': 'Int',
			'width': 80
		},	
		{
			'fieldname': 'incoming_calls',
			'label': _('Incoming#'),
			'fieldtype': 'Int',
			'width': 90
		},		
		{
			'fieldname': 'missed_calls',
			'label': _('Missed#'),
			'fieldtype': 'Int',
			'width': 80
		},	
		{
			'fieldname': 'rejected_calls',
			'label': _('Rejected#'),
			'fieldtype': 'Int',
			'width': 90
		}						
	]

	data = frappe.db.sql("""
select call_log.date, sales.sales_person_name as sales_person, 
MIN(call_log.`time`) as first_call,
COUNT(CASE WHEN call_log.calltype = 'Outgoing' THEN call_log.name ELSE NULL END) as outgoing_calls,
COUNT(DISTINCT (call_log.customer_mobile)) as unique_calls,
COUNT(CASE WHEN call_log.calltype = 'Incoming' THEN call_log.name ELSE NULL END) as incoming_calls,
COUNT(CASE WHEN call_log.calltype = 'Missed' THEN call_log.name ELSE NULL END) as missed_calls,
COUNT(CASE WHEN call_log.calltype = 'Rejected' THEN call_log.name ELSE NULL END) as rejected_calls
FROM  `tabCallyzer Call Log` call_log
inner join `tabSales Person` sales
on call_log.employee_mobile = sales.mobile_no_cf 
where date(call_log.date) between %(from_date)s AND %(to_date)s
{conditions}
group by call_log.date,sales.mobile_no_cf 
order by call_log.date desc,sales.mobile_no_cf asc""".format(conditions=get_conditions(filters)), filters, as_dict=1)
	return columns, data

def get_conditions(filters) :
	conditions = []

	if filters.get("sales_person"):
		conditions.append(" and sales.sales_person_name=%(sales_person)s")


	return " ".join(conditions) if conditions else ""