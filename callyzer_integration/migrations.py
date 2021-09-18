import frappe
from frappe.modules.import_file import import_file_by_path
from frappe.utils import get_bench_path
import os
from os.path import join


def after_migrations():
	# if(not frappe.db.exists('Custom Field','Lead-call_info_cf')):
	fname="custom_field.json"
	import_folder_path="{bench_path}/{app_folder_path}".format(bench_path=get_bench_path(),app_folder_path='/apps/callyzer_integration/callyzer_integration/import_records')
	make_records(import_folder_path,fname)

	

def make_records(path, fname):
	if os.path.isdir(path):
		import_file_by_path("{path}/{fname}".format(path=path, fname=fname))