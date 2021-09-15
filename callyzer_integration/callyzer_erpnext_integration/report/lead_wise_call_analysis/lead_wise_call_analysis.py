# Copyright (c) 2013, Frappe Technologies Pvt. Ltd. and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe import _, scrub

def execute(filters=None):
	columns = [
		{
				'label': _('Lead#'),
				'options': 'Lead',
				'fieldname': 'lead_id',
				'fieldtype': 'Link',
				'width': 100
		},
		{
				'label': _('Lead Owner'),
				'fieldname': 'lead_owner',
				'fieldtype': 'Data',
				'width': 150
		},
		{
			"fieldname":"status",
			"label": _("Status"),
			"fieldtype": "Data",
			"width": 90
		},
		{
			"label": _("Territory"),
			"fieldname": "territory",
			"fieldtype": "Link",
			"options": "Territory",
			"width": 100
		},
		{
			"label": _("Lead Name"),
			"fieldname": "lead_name",
			"fieldtype": "Data",
			"width": 160
		},				
		{
			"label": _("Organization"),
			"fieldname": "organization",
			"fieldtype": "Data",
			"width": 210
		},		
		{
			"label": _("Mobile"),
			"fieldname": "mobile_no",
			"fieldtype": "Data",
			"width": 110
		},							
		{
			'fieldname': 'first_call',
			'label': _('First Call'),
			'fieldtype': 'Time',
			'width': 80
		},		
		{
			'fieldname': 'last_call',
			'label': _('Last Call'),
			'fieldtype': 'Time',
			'width': 80
		},		
		{
			'fieldname': 'total_calls',
			'label': _('Total#'),
			'fieldtype': 'Int',
			'width': 65
		},		
		{
			'fieldname': 'outgoing_calls',
			'label': _('Outgoing#'),
			'fieldtype': 'Int',
			'width': 90
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

	data = frappe.db.sql('''
select lead.name as lead_id,user.full_name as lead_owner,lead.status,lead.territory,lead.lead_name,lead.company_name as organization,lead.mobile_no,
MIN(call_log.time) as first_call,MAX(call_log.`time`) as last_call, COUNT(call_log.name) as total_calls,
COUNT(CASE WHEN call_log.calltype = 'Outgoing' THEN call_log.name ELSE NULL END) as outgoing_calls,
COUNT(CASE WHEN call_log.calltype = 'Incoming' THEN call_log.name ELSE NULL END) as incoming_calls,
COUNT(CASE WHEN call_log.calltype = 'Missed' THEN call_log.name ELSE NULL END) as missed_calls,
COUNT(CASE WHEN call_log.calltype = 'Rejected' THEN call_log.name ELSE NULL END) as rejected_calls
FROM  `tabCallyzer Call Log` call_log
inner join `tabLead` lead
on call_log.customer_mobile = lead.mobile_no 
inner join `tabUser` user
on user.name=lead.lead_owner
where date(call_log.date) between %s and %s
group by lead.mobile_no
order by call_log.creation desc
	''', (filters.from_date, filters.to_date))
	return columns, data
