frappe.ui.form.on("Lead", {
	onload: function(frm) {
		if(frm.fields_dict['call_info_cf'] && "call_info_content" in frm.doc.__onload) {
			$(frm.fields_dict['call_info_cf'].wrapper)
				.html(frappe.render_template("call_info_template.html",
					frm.doc.__onload))
				.find(".btn-contact").on("click", function() {
					frappe.new_doc("Contact");
				}
			);
		}
	}
})