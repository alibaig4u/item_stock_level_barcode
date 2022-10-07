frappe.ui.form.on("Item", {
    refresh: function(frm){
        frm.add_custom_button('Generate Barcode',()=>{
            cur_frm.events.generate_barcode(cur_frm);

        })
    },
    generate_barcode: function(frm){
        frappe.call({
            method: 'barcode.events.item.generate_barcodes',
            async: false,
            args:{
                item: frm.doc.name
            },
            callback: (r)=>{
                frappe.msgprint("Barcodes has been printed")
                frm.reload_doc()
            }
        })

    }

})