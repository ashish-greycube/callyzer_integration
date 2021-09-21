import frappe
from frappe.modules.import_file import import_file_by_path
from frappe.utils import get_bench_path
import os
from os.path import join

def after_migrate(**args):
	callyzer_integration_create_custom_fields(**args)




def callyzer_integration_create_custom_fields(**args):
    from frappe.custom.doctype.custom_field.custom_field import create_custom_fields

 
    custom_fields = {
'Sales Person':[
 dict(
   doctype= 'Custom Field',
  dt= 'Sales Person',
  fieldname= 'mobile_no_cf',
  fieldtype= 'Data',
  insert_after= 'cb0',
  label= 'Sales Person Mobile',
  name= 'Sales Person-mobile_no_cf',
  options= 'Phone',
  reqd= 1
  )],
'Lead':[
 dict(
  doctype= 'Custom Field',
  dt= 'Lead',
  fieldname= 'call_info_cf',
  fieldtype= 'HTML',
  insert_after= 'email_id',
  label= 'Call Info',
  name= 'Lead-call_info_cf'
  ),
   dict(
  depends_on= "eval:doc.mobile_no",
  doctype= "Custom Field",
  dt= "Lead",
  fieldname= "check_call_log_cf",
  fieldtype= "Button",
  insert_after= "call_info_cf",
  label= "Check Call Log",
  name= "Lead-check_call_log_cf"
  )
  ]
  }

    create_custom_fields(custom_fields)
    frappe.db.commit()  # to avoid implicit-commit errors				

	