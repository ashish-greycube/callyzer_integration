// Copyright (c) 2016, GreyCube Technologies and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Lead Wise Call Analysis"] = {
	"filters": [
		{
			"fieldname": "from_date",
			"label": __("Call From Date"),
			"fieldtype": "Date",
			"reqd": 1,
			"default": frappe.datetime.add_days(frappe.datetime.nowdate(), -1)
		},
		{
			"fieldname": "to_date",
			"label": __("Call To Date"),
			"fieldtype": "Date",
			"reqd": 1,
			"default":frappe.datetime.nowdate()
		},
		{
			"fieldname": "lead_owner",
			"label": __("Lead Owner"),
			"fieldtype": "Link",
			"options": "User"
		},
		{
			"fieldname": "source",
			"label": __("Source"),
			"fieldtype": "Link",
			"options": "Lead Source"
		}				
	]
};
