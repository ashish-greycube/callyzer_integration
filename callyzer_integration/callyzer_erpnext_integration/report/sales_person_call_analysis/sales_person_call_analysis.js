// Copyright (c) 2016, GreyCube Technologies and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Sales Person Call Analysis"] = {
	"filters": [
		{
			"fieldname": "from_date",
			"label": __("Call From Date"),
			"fieldtype": "Date",
			"reqd": 1,
			"default": frappe.datetime.add_days(frappe.datetime.nowdate(), -30)
		},
		{
			"fieldname": "to_date",
			"label": __("Call To Date"),
			"fieldtype": "Date",
			"reqd": 1,
			"default":frappe.datetime.nowdate()
		},
		{
			fieldname: "sales_person",
			label: __("Sales Person"),
			fieldtype: "Link",
			options: "Sales Person",
			reqd: 0
		}		
	]
};
