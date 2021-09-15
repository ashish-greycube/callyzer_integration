# Copyright (c) 2021, GreyCube Technologies and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe import _
from frappe.model.document import Document

class CallyzerSettings(Document):
	def validate(self):
		if self.enabled==1 and (not self.bearer_token  or not self.call_history_url):
			frappe.throw(_("Please enter value for Bearer Token & Callyzer History Pull Url"))
