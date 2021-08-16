import json


class variable:
    def __init__(self):
        # common
        self.entity_gid = 0
        self.create_by = 0
        self.limit = 0
        self.gid = 0
        self.code = ''
        self.password = ''
        self.name = ''
        self.date = ''
        self.from_date = ''
        self.to_date = ''
        self.action = ''
        self.remark = ''
        self.reason = ''
        self.status = ''
        self.outmsg = ''
        self.jsondata = '{}'
        self.jsonData = json.dumps([])
        self.jsonData_sec = json.dumps([])
        self.gender = ''
        self.email = ''
        self.wedding_day = ''
        self.mysql_limit = ''

        self.address_gid = 0
        self.mobile_no = ''
        self.landline_no = 0
        self.state_gid = 0
        self.state_name = ''
        self.district_gid = 0
        self.district_name = ''
        self.city_gid = 0
        self.city_name = ''
        self.pincode_gid = 0
        self.pincode_no = 0
        self.add_refcode = ''
        self.address1 = ''
        self.address2 = ''
        self.address3 = ''
        self.location_gid = 0
        self.location_code = ''
        self.location_name = ''

        self.customer_gid = 0
        self.customer_name = ''
        self.customer_code = ''
        self.landmark = ''
        self.cust_type = ''
        self.cust_subtype = ''
        self.custgrp_gid = 0
        self.custcate_gid = 0
        self.custgrp_code = ''
        self.custgrp_name = ''
        self.cust_billingname=''

        self.cluster_gid = 0
        self.json_cluster_gid = json.dumps([])
        self.cluster_name = ''
        self.cluster_parent_gid = 0
        self.cluster = ''

        self.employee_gid = 0
        self.json_employee_gid = json.dumps([])
        self.employee_name = ''
        self.employee_code = 0
        self.emp_dob = ''
        self.emp_doj = ''
        self.emp_sup_name = ''
        self.emp_sup_gid = 0
        self.emp_mobileno = 0

        self.department_gid = 0
        self.department_code = 0
        self.department_name = ''

        self.courier_gid = 0
        self.courier_code = ''
        self.courier_name = ''

        self.product_gid = 0
        self.productcat_gid = 0
        self.product_type = 0
        self.product_stockcode = ''

        self.routeHead_gid = 0
        self.route_gid = 0
        self.route_code = ''
        self.route_name = ''

        self.leadref_gid = 0
        self.leadref_name = ''

        self.sechedule_gid = 0
        self.so_header_gid = 0
        self.schedule_gid = 0
        self.schedule_name = ''
        self.schedule_date = ''
        self.schedule_ref_gid = 0
        self.schedule_type_gid = 0
        self.sch_remark = 'Direct'
        self.followup_reason_gid = 0
        self.ls_followup_date = ''

        self.stock_code = ''
        self.invoice_no = ''
        self.invoice_date = ''
        self.mode = ''
        self.amount = 0
        self.cheque_no = ''

        self.resechedule_date = 0
        self.soheader_gid = 0
        self.collectionheader_gid = 0
        self.table_name = ''
        self.hierarchy_gid = 0
        self.all_cluster_gid = 'ALL'
        self.execu = ''
        self.parent = 'All'

        self.column_name = ''
        self.constitution_gid = 0
        self.salemode_gid = 0
        self.size_gid = 0

        self.add_gid = 0
        self.conper1 = ''
        self.desig1 = ''
        self.conper2 = ''
        self.desig2 = ''
        self.mobile_no1 = 0
        self.landline_no1 = 0

        self.contact_gid = 0
        self.cont_refcode = ''
        self.cont_refgid = 0
        self.contacttype_gid = 0
        self.designation_gid = 0
        self.cont_dob = ''
        self.exemapjson=''
        self.exemapping_gid=0

        self.inwardheader_json = ''
        self.inwarddetail_json = ''
        self.type=''
        self.sub_type=''
        self.char = ''

        #latitude longitude
        self.latlong_gid=0
        self.latitude=0
        self.longitude=0

        # BOM
        self.group = ''

        #gst
        self.taxdtl_gid = 0
        self.tax_code = ''
        self.subtax_name = ''
        self.ref_name = ''
        self.tax_type = ''
        self.reftbl_code = ''
        self.gstno = ''

        self.json_unique = ''

        self.group = ''

        #client
        self.client_gid = 0
        self.client_name = ''
        self.client_code = ''

        self.supplier_gid=0
        self.receipt_gid=0
        self.receiptdetails_gid=0

        self.cust_courier_gid = 0
        self.version_no=0
        self.version_flag=''
        self.commit=0
        self.json_classification= json.dumps([])
        self.json_rate=json.dumps([])
        self.json_file = json.dumps([])

        ## Sale
        self.product_type = 0
        self.unit_price = 0
        self.So_Header_date = ''
        self.Channel = ''
        self.sodetails = ''
        self.soheader_gid = 0
        self.detail_gid = 0
        self.quantity = ''
        self.date = ''
        self.type = ''
        self.header = ''
        self.detail = ''
        self.Classification = ''
        self.sales = ''
        self.filter_json = ''
        self.year = ''
        self.product_type_gid = ''
        self.is_commit = ''