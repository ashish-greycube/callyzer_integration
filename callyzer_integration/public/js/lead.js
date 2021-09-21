const call_html='             <h5>Call Details:</h5>		{% if (call_info) { %}<i><ul><li>Lead : {{call_info.lead_name}}</li><li>Customer No : {{call_info.customer_no}}</li><li>First Call Response Time  : <b>{{call_info.first_call_response_time}}</b></li><li>First Call : {{call_info.first_call}}</li><li>Last Call : {{call_info.last_call}}</li><li>Total# : {{call_info.total_count}}</li><li>Outgoing# : {{call_info.outgoing_count}}</li><li>Incoming# : {{call_info.incoming_count}}</li><li>Missed# : {{call_info.missed_count}}</li><li>Rejected# : {{call_info.rejected_count}}</li></ul></i>{% } else { %}<i class="text-muted">{{ __("No calls.") }}</i>{% } %}'
frappe.ui.form.on("Lead", {
	check_call_log_cf: function(frm) {
		frappe.set_route('List', 'Callyzer Call Log', {customer_mobile: frm.doc.mobile_no});
	},
	onload: function(frm) {
		if(frm.fields_dict['call_info_cf'] && "call_info" in frm.doc.__onload) {
			console.log('frm.doc.__onload',frm.doc.__onload)
			$(frm.fields_dict['call_info_cf'].wrapper)
				.html(frappe.render_template(call_html,
					frm.doc.__onload))
		}
	}
})