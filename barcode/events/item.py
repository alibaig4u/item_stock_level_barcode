import frappe


@frappe.whitelist()
def generate_barcodes(item=None):
    get_current_item_stock(item)


def get_current_item_stock(item_code=None):

    current_stock = frappe.db.sql(
        """select
                tb.item_code,
                tb.warehouse,
                COALESCE(tb.actual_qty,0) as actual_qty
            from
                `tabBin` tb
            left join tabWarehouse tw on
                tb.warehouse = tw.name
            where
                tb.item_code = '{item_code}'
                and tb.actual_qty > 0
        """.format(item_code=item_code), as_dict=True)
    item_doc = frappe.get_doc("Item", item_code)
    item_doc.barcodes = []
    item_doc.save(ignore_permissions=True)
    item_doc = frappe.get_doc("Item", item_code)
    for idx, stock in enumerate(current_stock):
        label = "Item:{}-Warehouse:{}-Qty:{}".format(stock.item_code, stock.warehouse, stock.actual_qty)
        generate_barcode(idx, stock.item_code, label, label)

        item_doc.append('barcodes',{
            "barcode":label,
            "description": label
        })
    item_doc.save(ignore_permissions=True)

def generate_barcode(idx=None, item_code=None, code=None, label=None):
    from pathlib import Path
    import os
    import qrcode

    try:
        name_tobe = label + ".png"
        # Get the current working directory
        cwd = os.getcwd()
        print(cwd)
        site_dir_path = cwd + "/sites/"
        site_dir_path = site_dir_path.replace('sites/sites', 'sites')
        f = open(site_dir_path + "currentsite.txt", "r")
        currentsitename = f.readline()
        qrcode_dir = site_dir_path + currentsitename + "/public/files/qrcodes/"+item_code+"/"
        if not os.path.exists(qrcode_dir):
            os.makedirs(qrcode_dir)
            os.chmod(qrcode_dir, 0o775)
        check_file = Path(qrcode_dir + name_tobe)
        # if not check_file.is_file():
        img = qrcode.make(code)
        img.save(qrcode_dir + name_tobe)
    except Exception as ex:
        frappe.log_error(frappe.get_traceback())