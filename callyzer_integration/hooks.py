from . import __version__ as app_version

app_name = "callyzer_integration"
app_title = "Callyzer ERPNext Integration"
app_publisher = "GreyCube Technologies"
app_description = "Intergration between ERPNext and Callyzer , a call log data analysis tool for CRM domain"
app_icon = "octicon octicon-comment-discussion"
app_color = "red"
app_email = "admin@greycube.in"
app_license = "MIT"

# Includes in <head>
# ------------------

# include js, css files in header of desk.html
# app_include_css = "/assets/callyzer_integration/css/callyzer_integration.css"
# app_include_js = "/assets/callyzer_integration/js/callyzer_integration.js"

# include js, css files in header of web template
# web_include_css = "/assets/callyzer_integration/css/callyzer_integration.css"
# web_include_js = "/assets/callyzer_integration/js/callyzer_integration.js"

# include custom scss in every website theme (without file extension ".scss")
# website_theme_scss = "callyzer_integration/public/scss/website"

# include js, css files in header of web form
# webform_include_js = {"doctype": "public/js/doctype.js"}
# webform_include_css = {"doctype": "public/css/doctype.css"}

# include js in page
# page_js = {"page" : "public/js/file.js"}

# include js in doctype views
# doctype_js = {"doctype" : "public/js/doctype.js"}
# doctype_list_js = {"doctype" : "public/js/doctype_list.js"}
# doctype_tree_js = {"doctype" : "public/js/doctype_tree.js"}
# doctype_calendar_js = {"doctype" : "public/js/doctype_calendar.js"}

# Home Pages
# ----------

# application home page (will override Website Settings)
# home_page = "login"

# website user home page (by Role)
# role_home_page = {
#	"Role": "home_page"
# }

# Generators
# ----------

# automatically create page for each record of this doctype
# website_generators = ["Web Page"]

# Installation
# ------------

# before_install = "callyzer_integration.install.before_install"
# after_install = "callyzer_integration.install.after_install"
after_migrate="callyzer_integration.migrations.after_migrations"
# Desk Notifications
# ------------------
# See frappe.core.notifications.get_notification_config

# notification_config = "callyzer_integration.notifications.get_notification_config"

# Permissions
# -----------
# Permissions evaluated in scripted ways

# permission_query_conditions = {
# 	"Event": "frappe.desk.doctype.event.event.get_permission_query_conditions",
# }
#
# has_permission = {
# 	"Event": "frappe.desk.doctype.event.event.has_permission",
# }

# DocType Class
# ---------------
# Override standard doctype classes

# override_doctype_class = {
# 	"ToDo": "custom_app.overrides.CustomToDo"
# }

# Document Events
# ---------------
# Hook on document methods and events

# doc_events = {
# 	"*": {
# 		"on_update": "method",
# 		"on_cancel": "method",
# 		"on_trash": "method"
#	}
# }

# Scheduled Tasks
# ---------------
scheduler_events = {
	"cron": {
		"0/5 * * * *": [
			"callyzer_integration.callyzer_integration_hook.auto_pull_callyzer_logs"
		]
	}
}
# scheduler_events = {
# 	"all": [
# 		"callyzer_integration.tasks.all"
# 	],
# 	"daily": [
# 		"callyzer_integration.tasks.daily"
# 	],
# 	"hourly": [
# 		"callyzer_integration.tasks.hourly"
# 	],
# 	"weekly": [
# 		"callyzer_integration.tasks.weekly"
# 	]
# 	"monthly": [
# 		"callyzer_integration.tasks.monthly"
# 	]
# }

# Testing
# -------

# before_tests = "callyzer_integration.install.before_tests"

# Overriding Methods
# ------------------------------
#
# override_whitelisted_methods = {
# 	"frappe.desk.doctype.event.event.get_events": "callyzer_integration.event.get_events"
# }
#
# each overriding function accepts a `data` argument;
# generated from the base implementation of the doctype dashboard,
# along with any modifications made in other Frappe apps
# override_doctype_dashboards = {
# 	"Task": "callyzer_integration.task.get_dashboard_data"
# }

# exempt linked doctypes from being automatically cancelled
#
# auto_cancel_exempted_doctypes = ["Auto Repeat"]


# User Data Protection
# --------------------

user_data_fields = [
	{
		"doctype": "{doctype_1}",
		"filter_by": "{filter_by}",
		"redact_fields": ["{field_1}", "{field_2}"],
		"partial": 1,
	},
	{
		"doctype": "{doctype_2}",
		"filter_by": "{filter_by}",
		"partial": 1,
	},
	{
		"doctype": "{doctype_3}",
		"strict": False,
	},
	{
		"doctype": "{doctype_4}"
	}
]

# Authentication and authorization
# --------------------------------

# auth_hooks = [
# 	"callyzer_integration.auth.validate"
# ]

fixtures = [
      {
        "dt": "Custom Field", 
        "filters": [["name", "in", ['Sales Person-mobile_no_cf']]]
      }	   			     
]