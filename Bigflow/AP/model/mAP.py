from django.db import connection
import pandas as pd
import json
from Bigflow.Transaction.Model import mFET


class ap_model(mFET.FET_model):
    def print_parameters(sp_name, parameters):
        pass
    
    def get_grn(self):
        cursor = connection.cursor()
        parameters = (self.action, self.POnumber, self.supplier_gid, self.entity_gid, '')
        cursor.callproc('sp_APInvoiceGRN_Get', parameters)
        columns = [x[0] for x in cursor.description]
        rows = cursor.fetchall()
        rows = list(rows)
        grn_dtl = pd.DataFrame(rows, columns=columns)
        return grn_dtl

    def get_inwarddtl(self):
        cursor = connection.cursor()
        jsondata = self.FILTER_JSON
        FILTER_JSON = json.dumps(jsondata)
        parameters = (self.action, self.type, FILTER_JSON, self.entity_gid, '')
        cursor.callproc('sp_InwardOffice_Get', parameters)
        cursor.execute('select @_sp_InwardOffice_Get_4')
        output_msg = cursor.fetchone()
        return output_msg

    def set_Invoice(self):
        cursor = connection.cursor()
        headjsondata = self.header_json
        deatailjson = self.detail_json
        invoicejson = self.invoice_json
        debitjson = self.debit_json
        creditjson = self.credit_json
        statusjson = self.status_json
        header_json = json.dumps(headjsondata)
        detail_json = json.dumps(deatailjson)
        invoice_json = json.dumps(invoicejson)
        debit_json = json.dumps(debitjson)
        credit_json = json.dumps(creditjson)
        status_json = json.dumps(statusjson)
        parameters = (
        self.action, self.type, invoice_json, detail_json, header_json, debit_json, credit_json, status_json,
        self.entity_gid, self.employee_gid, '')
        ap_model.print_parameters("sp_APInvoiceSPS_Set", parameters)
        cursor.callproc('sp_APInvoiceSPS_Set', parameters)
        cursor.execute('select @_sp_APInvoiceSPS_Set_10')
        output_msg = cursor.fetchone()
        return output_msg

    def Invoice_get(self):
        cursor = connection.cursor()
        parameters = (
        self.action, self.ponumber, self.supplier_gid, self.inwardheader_gid, self.inwarddetail_gid, self.status,
        self.state_gid, self.entity_gid, 1, '')
        ap_model.print_parameters("sp_APInvoice_Get",parameters)
        #  parameters = (self.action, self.ponumber,self.supplier_gid,self.inwardheader_gid,self.inwarddetail_gid ,self.status,self.state_gid,self.entity_gid, '')
        cursor.callproc('sp_APInvoice_Get', parameters)
        columns = [x[0] for x in cursor.description]
        rows = cursor.fetchall()
        rows = list(rows)
        grn_dtl = pd.DataFrame(rows, columns=columns)
        return grn_dtl

    def Invoice_set(self):
        cursor = connection.cursor()
        parameters = (
        self.action, self.type, self.sub_type, self.filter, self.status, self.classification, self.create_by, '');

        ap_model.print_parameters("sp_APsalesprocess_Set", parameters)
        #  parameters = (self.action, self.ponumber,self.supplier_gid,self.inwardheader_gid,self.inwarddetail_gid ,self.status,self.state_gid,self.entity_gid, '')
        cursor.callproc('sp_APsalesprocess_Set', parameters)
        cursor.execute('select @_sp_APsalesprocess_Set_7')
        output_msg = cursor.fetchone()
        return output_msg

    def get_invoice_all(self):
        cursor = connection.cursor()
        parameters = (self.action, self.type, self.filter, self.classification, '');
        ap_model.print_parameters("sp_APProcess_Get", parameters)

        cursor.callproc('sp_APProcess_Get', parameters)
        columns = [x[0] for x in cursor.description]
        rows = cursor.fetchall()
        rows = list(rows)
        grn_dtl = pd.DataFrame(rows, columns=columns)
        return grn_dtl

    def get_gl_report(self):
        cursor = connection.cursor()
        parameters = (self.action, self.type, self.filter, self.classification, '');
        ap_model.print_parameters("sp_glreport", parameters)

        cursor.callproc('sp_glreport', parameters)
        columns = [x[0] for x in cursor.description]
        rows = cursor.fetchall()
        rows = list(rows)
        grn_dtl = pd.DataFrame(rows, columns=columns)
        return grn_dtl

    def get_transaction_details(self):
        cursor = connection.cursor()
        parameters = (self.action, self.type, self.filter, self.classification, '');
        ap_model.print_parameters("sp_APTranGet", parameters)

        cursor.callproc('sp_APTranGet', parameters)
        columns = [x[0] for x in cursor.description]
        rows = cursor.fetchall()
        rows = list(rows)
        grn_dtl = pd.DataFrame(rows, columns=columns)
        return grn_dtl

    def get_invoice_all_demo(self):
        cursor = connection.cursor()
        parameters = (self.action, self.type, self.filter, self.classification, '');
        ap_model.print_parameters("sp_APProcessNew_Get", parameters)
        cursor.callproc('sp_APProcessNew_Get', parameters)
        columns = [x[0] for x in cursor.description]
        rows = cursor.fetchall()
        rows = list(rows)
        grn_dtl = pd.DataFrame(rows, columns=columns)
        return grn_dtl
    
    def get_ecf_file_details(self):
        cursor = connection.cursor()
        parameters = (self.action, self.type, self.filter, self.classification, '');

        ap_model.print_parameters("sp_FileDetail_Get", parameters)

        cursor.callproc('sp_FileDetail_Get', parameters)
        columns = [x[0] for x in cursor.description]
        rows = cursor.fetchall()
        rows = list(rows)
        grn_dtl = pd.DataFrame(rows, columns=columns)
        return grn_dtl

    def get_ap_debit_details(self):
        cursor = connection.cursor()
        parameters = (self.action, self.type, self.filter, self.classification, '');

        ap_model.print_parameters("sp_APDebit_Get", parameters)

        cursor.callproc('sp_APDebit_Get', parameters)
        columns = [x[0] for x in cursor.description]
        rows = cursor.fetchall()
        rows = list(rows)
        grn_dtl = pd.DataFrame(rows, columns=columns)
        return grn_dtl
    
    def get_billentry_all(self):
        cursor = connection.cursor()
        parameters = (self.action, self.type, self.filter, self.classification, '');

        ap_model.print_parameters("sp_APProcess_Get", parameters)

        data = {}
        cursor.callproc('sp_APProcess_Get', parameters)
        columns = [x[0] for x in cursor.description]
        rows = cursor.fetchall()
        rows = list(rows)
        grn_dtl = pd.DataFrame(rows, columns=columns)
        data['invoice'] = json.loads(grn_dtl.to_json(orient='records'))
        i = 0
        while (cursor.nextset()):
            if(i!=2):
                columns = [x[0] for x in cursor.description]
                rows = cursor.fetchall()
                rows = list(rows)
                grn_dtl = pd.DataFrame(rows, columns=columns)
                if i == 0:
                    data['DEBIT'] = json.loads(grn_dtl.to_json(orient='records'))
                    i=1
                else :
                    data['CREDIT'] = json.loads(grn_dtl.to_json(orient='records'))
                    i=2
        return data

    def ap_process_get_double_data(self):
        cursor = connection.cursor()
        parameters = (self.action, self.type, self.filter, self.classification, '');
        ap_model.print_parameters("sp_APProcess_Get", parameters)
        data = {}
        cursor.callproc('sp_APProcess_Get', parameters)
        columns = [x[0] for x in cursor.description]
        rows = cursor.fetchall()
        rows = list(rows)
        grn_dtl = pd.DataFrame(rows, columns=columns)
        data['Credit'] = json.loads(grn_dtl.to_json(orient='records'))
        i = 0
        while (cursor.nextset()):
            if(i!=1):
                columns = [x[0] for x in cursor.description]
                rows = cursor.fetchall()
                rows = list(rows)
                grn_dtl = pd.DataFrame(rows, columns=columns)
                if i == 0:
                    data['Debit'] = json.loads(grn_dtl.to_json(orient='records'))
                    i=1
        return data

    def ecf_payment_details(self):
        cursor = connection.cursor()
        parameters = (self.action, self.type, self.filter, self.classification, '');
        ap_model.print_parameters("sp_APProcess_Get", parameters)
        data = {}
        cursor.callproc('sp_APProcess_Get', parameters)
        columns = [x[0] for x in cursor.description]
        rows = cursor.fetchall()
        rows = list(rows)
        grn_dtl = pd.DataFrame(rows, columns=columns)
        data['Inward_Details'] = json.loads(grn_dtl.to_json(orient='records'))
        i = 0
        while (cursor.nextset()):
            if(i!=1):
                columns = [x[0] for x in cursor.description]
                rows = cursor.fetchall()
                rows = list(rows)
                grn_dtl = pd.DataFrame(rows, columns=columns)
                if i == 0:
                    data['Payment_Details'] = json.loads(grn_dtl.to_json(orient='records'))
                    i=1
        return data
    
    def get_dedube_details(self):
        cursor = connection.cursor()
        parameters = (self.action, self.type, self.filter, self.classification, '');

        ap_model.print_parameters("sp_DedupeProcess_Get", parameters)

        data = {}
        cursor.callproc('sp_DedupeProcess_Get', parameters)
        columns = [x[0] for x in cursor.description]
        rows = cursor.fetchall()
        rows = list(rows)
        dedube_data = pd.DataFrame(rows, columns=columns)
        data['EXACT_MATCH'] = json.loads(dedube_data.to_json(orient='records'))
        i = 0
        while (cursor.nextset()):
            if(i!=4):
                columns = [x[0] for x in cursor.description]
                rows = cursor.fetchall()
                rows = list(rows)
                dedube_data = pd.DataFrame(rows, columns=columns)
                if i == 0:
                    data['WITHOUT_SUPPLIER'] = json.loads(dedube_data.to_json(orient='records'))
                    i=1
                elif i==1:
                    data['WITHOUT_INVOICE_AMOUNT'] = json.loads(dedube_data.to_json(orient='records'))
                    i = 2
                elif i==2:
                    data['WITHOUT_INVOICE_NUMBER'] = json.loads(dedube_data.to_json(orient='records'))
                    i = 3
                elif i==3:
                    data['WITHOUT_INVOICE_DATE'] = json.loads(dedube_data.to_json(orient='records'))
                    i = 4
        return data

    def set_ammort_details(self):
        cursor = connection.cursor()
        parameters = (self.action, self.type, self.filter, self.classification, self.create_by, '');

        ap_model.print_parameters("sp_APAmmort_Set", parameters)

        cursor.callproc('sp_APAmmort_Set', parameters)
        cursor.execute('select @_sp_APAmmort_Set_5')
        output_msg = cursor.fetchone()
        return output_msg

    def set_dispatch_details(self):
        cursor = connection.cursor()
        parameters = (self.action, self.type, self.filter, self.classification, self.create_by, '');

        ap_model.print_parameters("sp_DispatchAP_Set", parameters)

        cursor.callproc('sp_DispatchAP_Set', parameters)
        cursor.execute('select @_sp_DispatchAP_Set_5')
        output_msg = cursor.fetchone()
        return output_msg

    def common_lock_set(self):
        cursor = connection.cursor()
        parameters = (self.action, self.type, self.filter, self.classification, self.create_by, '');
        ap_model.print_parameters("sp_CommonLock_Set", parameters)
        cursor.callproc('sp_CommonLock_Set', parameters)
        cursor.execute('select @_sp_CommonLock_Set_5')
        output_msg = cursor.fetchone()
        return output_msg

    def get_ap_pod(self):
        cursor = connection.cursor()
        parameters = (self.action, self.type, self.filter, self.classification, '');

        ap_model.print_parameters("sp_DispatchAP_Get", parameters)

        cursor.callproc('sp_DispatchAP_Get', parameters)
        columns = [x[0] for x in cursor.description]
        rows = cursor.fetchall()
        rows = list(rows)
        grn_dtl = pd.DataFrame(rows, columns=columns)
        return grn_dtl

    def get_ammort_details(self):
        cursor = connection.cursor()
        parameters = (self.action, self.type, self.filter, self.classification, '');

        ap_model.print_parameters("sp_APAmmort_Get", parameters)

        cursor.callproc('sp_APAmmort_Get', parameters)
        columns = [x[0] for x in cursor.description]
        rows = cursor.fetchall()
        rows = list(rows)
        grn_dtl = pd.DataFrame(rows, columns=columns)
        return grn_dtl


    def credit_get(self):
        cursor = connection.cursor()
        parameters = (self.type, self.supplier_gid, self.entity_gid, '')
        p = (self.type, self.supplier_gid, self.entity_gid,"@message")
        ap_model.print_parameters("sp_APSupplierCredit_Get", p);

        cursor.callproc('sp_APSupplierCredit_Get', parameters)
        columns = [x[0] for x in cursor.description]
        rows = cursor.fetchall()
        rows = list(rows)
        grn_dtl = pd.DataFrame(rows, columns=columns)
        return grn_dtl

    def set_accounting_entry(self):
        cursor = connection.cursor()
        parameters = (self.action, self.type, self.filter, self.classification, self.create_by, '');

        ap_model.print_parameters("sp_AccountEntry_Set", parameters)

        cursor.callproc('sp_AccountEntry_Set', parameters)
        cursor.execute('select @_sp_AccountEntry_Set_5')
        output_msg = cursor.fetchone()
        return output_msg

    def set_Invoiceheader(self):
        cursor = connection.cursor()
        headjsondata = self.header_json
        debitjson = self.debit_json
        deatailjson = self.detail_json
        statusjson = self.status_json
        header_json = json.dumps(headjsondata)
        debit_json = json.dumps(debitjson)
        detail_json = json.dumps(deatailjson)
        status_json = json.dumps(statusjson)
        parameters = (self.action, self.type, header_json, detail_json, debit_json, status_json, self.employee_gid, self.entity_gid,'')

        ap_model.print_parameters("sp_APInvoice_Set", parameters);

        cursor.callproc('sp_APInvoice_Set', parameters)
        cursor.execute('select @_sp_APInvoice_Set_8')
        output_msg = cursor.fetchone()
        return output_msg

    def set_Invoiceheader_status_update(self):
        cursor = connection.cursor()
        headjsondata = self.header_json
        debitjson = self.debit_json
        deatailjson = self.detail_json
        statusjson = self.status_json
        header_json = json.dumps(headjsondata)
        debit_json = json.dumps(debitjson)
        detail_json = json.dumps(deatailjson)
        status_json = json.dumps(statusjson)
        parameters = (self.action, self.type, header_json, detail_json, debit_json, status_json, self.employee_gid, self.entity_gid,'')

        ap_model.print_parameters("sp_APInvoiceStatus_Set", parameters);

        cursor.callproc('sp_APInvoiceStatus_Set', parameters)
        cursor.execute('select @_sp_APInvoiceStatus_Set_8')
        output_msg = cursor.fetchone()
        return output_msg

    def hsn_get(self):
        cursor = connection.cursor()
        parameters = (self.type, self.group, '{}', self.entity_gid, '')
        ap_model.print_parameters("sp_HSN_Get", parameters);
        cursor.callproc('sp_HSN_Get', parameters)
        columns = [x[0] for x in cursor.description]
        rows = cursor.fetchall()
        rows = list(rows)
        grn_dtl = pd.DataFrame(rows, columns=columns)
        return grn_dtl

    def hsn_taxget(self):
        cursor = connection.cursor()
        hsndtl = self.hsndtl
        hsndtl_json = json.dumps(hsndtl)
        parameters = (self.group, 'AMOUNT_DISCOUNT', hsndtl_json, 1, '')
        ap_model.print_parameters("sp_TAXcalculate_Get", parameters);
        cursor.callproc('sp_TAXcalculate_Get', parameters)
        columns = [x[0] for x in cursor.description]
        # rows = cursor.fetchall()
        # rows = list(rows)
        # while (cursor.nextset()):
        #     try:
        #      columns = [x[0] for x in cursor.description]
        #      rows = cursor.fetchall()
        #      # columns.append([x[0] for x in cursor.description]).replace('[','').replace(']','')
        #      # rows.append(cursor.fetchall())
        #     except:
        #         print("")
        #
        # grn_dtl = pd.DataFrame(rows, columns=columns)
        # return grn_dtl
        rows = cursor.fetchall()
        rows = list(rows)
        tax_dtl = pd.DataFrame(rows, columns=columns)
        cursor.nextset()
        columns = [x[0] for x in cursor.description]
        rows = cursor.fetchall()
        rows = list(rows)
        tax_dtl2 = pd.DataFrame(rows, columns=columns)
        cursor.nextset()
        columns = [x[0] for x in cursor.description]
        rows = cursor.fetchall()
        rows = list(rows)
        tax_dtl3 = pd.DataFrame(rows, columns=columns)
        cursor.close()
        data = [tax_dtl, tax_dtl2, tax_dtl3]
        return data

    def hsn_Credittaxget(self):
        cursor = connection.cursor()
        hsndtl = self.hsndtl
        hsndtl_json = json.dumps(hsndtl)
        parameters = (self.group, '', hsndtl_json, 1, '')
        ap_model.print_parameters("sp_TAXcalculate_Get", parameters);
        cursor.callproc('sp_TAXcalculate_Get', parameters)
        columns = [x[0] for x in cursor.description]
        rows = cursor.fetchall()
        rows = list(rows)
        grn_dtl = pd.DataFrame(rows, columns=columns)
        return grn_dtl

    def tablevalue_get(self):
        cursor = connection.cursor()
        tablevalue = self.tablevalue
        tablevalue_json = json.dumps(tablevalue)
        parameters = (self.type, tablevalue_json, self.entity_gid, '')
        ap_model.print_parameters("sp_AllTableValues_Get", parameters);
        cursor.callproc('sp_AllTableValues_Get', parameters)
        columns = [x[0] for x in cursor.description]
        rows = cursor.fetchall()
        rows = list(rows)
        grn_dtl = pd.DataFrame(rows, columns=columns)
        return grn_dtl

    def get_ap_cat(self):
        cursor = connection.cursor()
        tablevalue = self.tablevalue
        tablevalue_json = json.dumps(tablevalue)
        parameters = (self.type, tablevalue_json, self.entity_gid, '')
        ap_model.print_parameters("sp_APcat_Get", parameters);
        cursor.callproc('sp_APcat_Get', parameters)
        columns = [x[0] for x in cursor.description]
        rows = cursor.fetchall()
        rows = list(rows)
        grn_dtl = pd.DataFrame(rows, columns=columns)
        return grn_dtl

    def get_ap_paymode_details(self):
        cursor = connection.cursor()
        parameters = (self.action, self.type, self.filter, self.classification, '');
        ap_model.print_parameters("sp_Paymodedetails_Get", parameters)
        cursor.callproc('sp_Paymodedetails_Get', parameters)
        columns = [x[0] for x in cursor.description]
        rows = cursor.fetchall()
        rows = list(rows)
        grn_dtl = pd.DataFrame(rows, columns=columns)
        return grn_dtl

    def subcategory_tablevalue_get(self):
        cursor = connection.cursor()
        tablevalue = self.tablevalue
        tablevalue_json = json.dumps(tablevalue)
        parameters = (self.type, tablevalue_json, self.entity_gid, '')
        ap_model.print_parameters("sp_APgl_Get", parameters);
        cursor.callproc('sp_APgl_Get', parameters)
        columns = [x[0] for x in cursor.description]
        rows = cursor.fetchall()
        rows = list(rows)
        grn_dtl = pd.DataFrame(rows, columns=columns)
        return grn_dtl

    def get_CCBS_Master_Value(self):
        cursor = connection.cursor()
        Parameters = (self.type, self.sub_type, self.jsonData, self.json_classification, '')
        cursor.callproc('sp_CCBS_Master_Get', Parameters)
        columns = [x[0] for x in cursor.description]
        rows = cursor.fetchall()
        rows = list(rows)
        df_cam = pd.DataFrame(rows, columns=columns)
        return df_cam

    def History_get(self):
        cursor = connection.cursor()
        refvalue = self.refvalue
        refvalue_json = json.dumps(refvalue)
        parameters = (self.group, self.type, refvalue_json, self.entity_gid, '')
        cursor.callproc('sp_APHistory_Get', parameters)
        columns = [x[0] for x in cursor.description]
        rows = cursor.fetchall()
        rows = list(rows)
        grn_dtl = pd.DataFrame(rows, columns=columns)
        return grn_dtl

    def set_payment(self):
        cursor = connection.cursor()
        headjsondata = self.header_json
        detailjson = self.detail_json
        otherjson = self.other_json
        statusjson = self.status_json
        header_json = json.dumps(headjsondata)
        detail_json = json.dumps(detailjson)
        other_json = json.dumps(otherjson)
        status_json = json.dumps(statusjson)
        parameters = (
        self.action, self.type, header_json, detail_json, other_json, status_json, self.employee_gid, self.entity_gid,
        '')
        ap_model.print_parameters("sp_APPayment_Set",parameters);

        cursor.callproc('sp_APPayment_Set', parameters)
        cursor.execute('select @_sp_APPayment_Set_8')
        output_msg = cursor.fetchone()
        return output_msg

    def set_midcash_entry(self):
        cursor = connection.cursor()
        parameters = (self.action, self.type,self.filter, self.classification, self.create_by, '')

        ap_model.print_parameters("sp_MidcashEntry_Set", parameters);

        cursor.callproc('sp_MidcashEntry_Set', parameters)
        cursor.execute('select @_sp_MidcashEntry_Set_5')
        out_message = cursor.fetchone()
        return out_message

    def rejectdata_get(self):
        cursor = connection.cursor()
        reject_json = json.dumps(self.reject_json)
        parameters = (self.group, self.type, reject_json, self.entity_gid, '')
        ap_model.print_parameters("sp_APInvoiceReject_Get",parameters)
        cursor.callproc('sp_APInvoiceReject_Get', parameters)
        columns = [x[0] for x in cursor.description]
        rows = cursor.fetchall()
        rows = list(rows)
        reject_dtl = pd.DataFrame(rows, columns=columns)
        return reject_dtl

    def getreasondata(self):
        cursor = connection.cursor()
        reason_json = json.dumps(self.reason_json)
        parameters = (self.type, reason_json, self.entity_gid, '')
        ap_model.print_parameters("sp_AllTableValues_Get",parameters)
        cursor.callproc('sp_AllTableValues_Get', parameters)
        columns = [x[0] for x in cursor.description]
        rows = cursor.fetchall()
        rows = list(rows)
        reject_dtl = pd.DataFrame(rows, columns=columns)
        return reject_dtl

    def set_Invoicereject(self):
        cursor = connection.cursor()
        reject_json = self.reject_json
        reject_json = json.dumps(reject_json)
        parameters = (self.action, self.type, reject_json, self.entity_gid, self.employee_gid, '')
        ap_model.print_parameters("sp_APInvoiceReject_Set",parameters)
        cursor.callproc('sp_APInvoiceReject_Set', parameters)
        cursor.execute('select @_sp_APInvoiceReject_Set_5')
        output_msg = cursor.fetchone()
        return output_msg

    def getpaymentdtl(self):
        cursor = connection.cursor()
        pay_json = self.pay_json
        pay_json = json.dumps(pay_json)
        parameters = (self.group, self.type, pay_json, self.entity_gid, '')
        ap_model.print_parameters("sp_APPayment_Get",parameters)
        cursor.callproc('sp_APPayment_Get', parameters)
        columns = [x[0] for x in cursor.description]
        rows = cursor.fetchall()
        rows = list(rows)
        out = pd.DataFrame(rows, columns=columns)
        return out

    def get_dropdown_detail(self):
        cursor = connection.cursor()
        parameters = (self.tablename, self.gid, self.name, self.entity_gid, '')
        ap_model.print_parameters("sp_Dropdown_Common_active_Get",parameters)
        cursor.callproc('sp_Dropdown_Common_active_Get', parameters)
        columns = [x[0] for x in cursor.description]
        rows = cursor.fetchall()
        rows = list(rows)
        dropdown = pd.DataFrame(rows, columns=columns)
        return dropdown

    def get_ppxdetails(self):
        cursor = connection.cursor()
        parameters = (self.group, self.type, json.dumps(self.filter), self.entity_gid, '')
        ap_model.print_parameters("sp_APPPX_Get",parameters)
        cursor.callproc('sp_APPPX_Get', parameters)
        columns = [x[0] for x in cursor.description]
        rows = cursor.fetchall()
        rows = list(rows)
        result = pd.DataFrame(rows, columns=columns)
        result.insert(4, "Liquidate", 0)
        return result

    def set_ppxdetails(self):
        cursor = connection.cursor()
        detail_json = self.detail_json
        detail_json = json.dumps(detail_json)
        parameters = (self.action, self.type, json.dumps(self.header_json), detail_json, '{}',
                      '{"Entity_Gid":[' + str(self.entity_gid) + ']}', self.employee_gid, '', '')
        ap_model.print_parameters("sp_Ap_ppx_Set",parameters)
        cursor.callproc('sp_Ap_ppx_Set', parameters)
        cursor.execute('select @_sp_Ap_ppx_Set_8')
        output_msg = cursor.fetchone()
        return output_msg

    def set_Dispatchpayment(self):
        cursor = connection.cursor()
        jsondata = self.PAYMENT_JSON
        PAYMENT_JSON = json.dumps(jsondata)
        parameters = (self.action, self.type, self.in_out, self.courier_gid, self.Dispatch_date, self.send_by,
                      self.awbno, self.dispatch_mode, self.dispatch_type, self.packets, self.weight,
                      self.dispatch_to, self.address, self.city, self.state, self.pincode, self.remark,
                      self.returned, self.returned_on, self.returned_remark, self.pod,
                      self.pod_image, self.isactive, self.isremoved, self.dispatch_gid,
                      PAYMENT_JSON, self.status, self.entity_gid, self.employee_gid, '')
        ap_model.print_parameters("sp_DispatchSPs_Set",parameters)
        cursor.callproc('sp_DispatchSPs_Set', parameters)
        cursor.execute('select @_sp_DispatchSPs_Set_29')
        output_msg = cursor.fetchone()
        return output_msg

    def get_auditchklist(self):
        cursor = connection.cursor()
        parameters = (self.type, self.chk_type, self.header_gid, self.entity_gid, '')
        ap_model.print_parameters("sp_APauditchklist_Get",parameters)

        cursor.callproc('sp_APauditchklist_Get', parameters)
        columns = [x[0] for x in cursor.description]
        rows = cursor.fetchall()
        rows = list(rows)
        result = pd.DataFrame(rows, columns=columns)
        return result

    def auditchklist(self):
        cursor = connection.cursor()
        chklist_json = self.chklist_json
        chklist_json = json.dumps(chklist_json)
        parameters = (
        self.action, self.type, chklist_json, '{"Entity_Gid":[' + str(self.entity_gid) + ']}', self.employee_gid, '')
        ap_model.print_parameters("sp_APauditchklist_Set",parameters)

        
        cursor.callproc('sp_APauditchklist_Set', parameters)
        cursor.execute('select @_sp_APauditchklist_Set_5')
        output_msg = cursor.fetchone()
        return output_msg

    def Address_Get(self):
        cursor = connection.cursor()
        parameters = (self.location_gid, self.entity_gid, '')
        ap_model.print_parameters("sp_Address_Get",parameters)

        cursor.callproc('sp_Address_Get', parameters)
        columns = [x[0] for x in cursor.description]
        rows = cursor.fetchall()
        rows = list(rows)
        service_out = pd.DataFrame(rows, columns=columns)
        return service_out

    def set_PODDispatch_ap(self):
        cursor = connection.cursor()
        parameters = (self.action, self.type, self.courier_gid, self.Dispatch_date, self.send_by,
                      self.awbno, self.dispatch_mode, self.dispatch_type, self.packets, self.weight,
                      self.dispatch_to, self.address, self.city, self.state, self.pincode, self.remark,
                      self.returned, self.returned_on, self.returned_remark, self.pod,
                      self.pod_image, self.isactive, self.isremoved, self.dispatch_gid, "DISPATCHED",
                      self.entity_gid, self.employee_gid, '')
        ap_model.print_parameters("sp_Dispatch_Set",parameters)

        cursor.callproc('sp_Dispatch_Set', parameters)
        cursor.execute('select @_sp_Dispatch_Set_27')
        output_msg = cursor.fetchone()
        return output_msg

    def set_APstale(self):
        cursor = connection.cursor()
        parameters = (
        self.action, self.type, json.dumps(self.header_json), '{"Entity_Gid":[' + str(self.entity_gid) + ']}',
        self.employee_gid, '')
        ap_model.print_parameters("sp_APStale_Set",parameters)

        cursor.callproc('sp_APStale_Set', parameters)
        cursor.execute('select @_sp_APStale_Set_5')
        output_msg = cursor.fetchone()
        return output_msg

    def get_stale(self):
        cursor = connection.cursor()
        parameters = (self.type, self.sub_type,
                      self.filter_json,
                      '{"Entity_Gid":[' + str(self.entity_gid) + ']}', self.employee_gid, '')
        ap_model.print_parameters("sp_APStale_Get",parameters)

        cursor.callproc('sp_APStale_Get', parameters)
        columns = [x[0] for x in cursor.description]
        rows = cursor.fetchall()
        rows = list(rows)
        service_out = pd.DataFrame(rows, columns=columns)
        return service_out

    def get_classification_summary(self):
        cursor = connection.cursor()
        parameters = (self.type, self.sub_type, self.jsonData, json.dumps(self.json_classification), '')

        ap_model.print_parameters("sp_Classification_Get",parameters)

        cursor.callproc('sp_Classification_Get', parameters)
        columns = [x[0] for x in cursor.description]
        rows = cursor.fetchall()
        cursor.execute('select @_sp_Classification_Get_4')
        outmsg_sp = cursor.fetchone()
        rows = list(rows)
        df_ta = pd.DataFrame(rows, columns=columns)
        return {"DATA": df_ta, "MESSAGE": outmsg_sp[0]}

    def get_supplier_data(self):
        cursor = connection.cursor()
        parameters = (self.type, self.sub_type, self.jsonData, json.dumps(self.json_classification), '')

        ap_model.print_parameters("sp_SupplierDetails_Get", parameters);

        cursor.callproc('sp_SupplierDetails_Get', parameters)
        columns = [x[0] for x in cursor.description]
        rows = cursor.fetchall()
        cursor.execute('select @_sp_SupplierDetails_Get_4')
        outmsg_sp = cursor.fetchone()
        rows = list(rows)
        df_ta = pd.DataFrame(rows, columns=columns)
        return {"DATA": df_ta, "MESSAGE": outmsg_sp[0]}

    def set_ECFInvoiceheader(self):
        cursor = connection.cursor()
        headjsondata = self.header_json
        debitjson = self.debit_json
        deatailjson = self.detail_json
        statusjson = self.status_json
        header_json = json.dumps(headjsondata)
        debit_json = json.dumps(debitjson)
        detail_json = json.dumps(deatailjson)
        status_json = json.dumps(statusjson)
        parameters = (
        self.action, self.type, header_json, detail_json, debit_json, status_json, self.employee_gid, self.entity_gid,
        '')
        cursor.callproc('sp_ECFInvoice_Set', parameters)
        ap_model.print_parameters("sp_ECFInvoice_Set", parameters);
        cursor.execute('select @_sp_ECFInvoice_Set_8')
        output_msg = cursor.fetchone()
        return output_msg

    def set_ECFInvoice_Status(self):
        cursor = connection.cursor()
        headjsondata = self.header_json
        debitjson = self.debit_json
        deatailjson = self.detail_json
        statusjson = self.status_json
        header_json = json.dumps(headjsondata)
        debit_json = json.dumps(debitjson)
        detail_json = json.dumps(deatailjson)
        status_json = json.dumps(statusjson)
        parameters = (
        self.action, self.type, header_json, detail_json, debit_json, status_json, self.employee_gid, self.entity_gid,
        '')
        cursor.callproc('sp_ECFInvoice_Set', parameters)
        ap_model.print_parameters("sp_ECFInvoice_Set", parameters);
        cursor.execute('select @_sp_ECFInvoice_Set_8')
        output_msg = cursor.fetchone()
        return output_msg

    def ECFInvoice_get(self):
        cursor = connection.cursor()
        parameters = (
        self.action, self.ecfnumber, self.supplier_gid, self.inwardheader_gid, self.inwarddetail_gid, self.status,
        self.state_gid, self.entity_gid, '')
        
        ap_model.print_parameters("sp_ECFInvoice_Get",parameters)

        cursor.callproc('sp_ECFInvoice_Get', parameters)
        columns = [x[0] for x in cursor.description]
        rows = cursor.fetchall()
        rows = list(rows)
        grn_dtl = pd.DataFrame(rows, columns=columns)
        return grn_dtl

    def ECFset_Invoice(self):
        cursor = connection.cursor()
        headjsondata = self.header_json
        deatailjson = self.detail_json
        invoicejson = self.invoice_json
        debitjson = self.debit_json
        creditjson = self.credit_json
        statusjson = self.status_json
        header_json = json.dumps(headjsondata)
        detail_json = json.dumps(deatailjson)
        invoice_json = json.dumps(invoicejson)
        debit_json = json.dumps(debitjson)
        credit_json = json.dumps(creditjson)
        status_json = json.dumps(statusjson)
        parameters = (
            self.action, self.type, invoice_json, detail_json, header_json, debit_json, credit_json, status_json,
            self.entity_gid, self.employee_gid, '')
        
        ap_model.print_parameters("sp_ECFInvoiceSPS_Set",parameters)

        cursor.callproc('sp_ECFInvoiceSPS_Set', parameters)
        cursor.execute('select @_sp_ECFInvoiceSPS_Set_10')
        output_msg = cursor.fetchone()
        return output_msg

    def get_ecf_details(self):
        cursor = connection.cursor()
        parameters = (self.action, self.type, self.filter, self.classification, '');
        ap_model.print_parameters("sp_ECFProcess_Get", parameters);
        cursor.callproc('sp_ECFProcess_Get', parameters)
        columns = [x[0] for x in cursor.description]
        rows = cursor.fetchall()
        rows = list(rows)
        grn_dtl = pd.DataFrame(rows, columns=columns)
        return grn_dtl

    def get_ecf_approval_details(self):
        cursor = connection.cursor()
        parameters = (self.action, self.type, self.filter, self.classification, '');
        ap_model.print_parameters("sp_ECFApproval_Get", parameters);
        cursor.callproc('sp_ECFApproval_Get', parameters)
        columns = [x[0] for x in cursor.description]
        rows = cursor.fetchall()
        rows = list(rows)
        grn_dtl = pd.DataFrame(rows, columns=columns)
        return grn_dtl

    def get_ecf_debit_details(self):
        cursor = connection.cursor()
        parameters = (self.action, self.type, self.filter, self.classification, '');
        ap_model.print_parameters("sp_ECFDebit_Get", parameters);
        cursor.callproc('sp_ECFDebit_Get', parameters)
        columns = [x[0] for x in cursor.description]
        rows = cursor.fetchall()
        rows = list(rows)
        grn_dtl = pd.DataFrame(rows, columns=columns)
        return grn_dtl

    def get_ecf_duplicate_details(self):
        cursor = connection.cursor()
        parameters = (self.action, self.type, self.filter, self.classification, '');
        ap_model.print_parameters("sp_ECFProcess_Duplicate_Get", parameters);
        cursor.callproc('sp_ECFProcess_Duplicate_Get', parameters)
        columns = [x[0] for x in cursor.description]
        rows = cursor.fetchall()
        rows = list(rows)
        grn_dtl = pd.DataFrame(rows, columns=columns)
        return grn_dtl

    def get_ecf_credit_details(self):
        cursor = connection.cursor()
        parameters = (self.action, self.type, self.filter, self.classification, '');
        ap_model.print_parameters("sp_ECFCredit_Get", parameters);
        cursor.callproc('sp_ECFCredit_Get', parameters)
        columns = [x[0] for x in cursor.description]
        rows = cursor.fetchall()
        rows = list(rows)
        grn_dtl = pd.DataFrame(rows, columns=columns)
        return grn_dtl
    
    def get_email_templates_data(self):
        cursor = connection.cursor()
        parameters = (self.action, self.type, self.filter, self.classification, '');

        ap_model.print_parameters("sp_Mailtemplates_Get", parameters);

        cursor.callproc('sp_Mailtemplates_Get', parameters)
        columns = [x[0] for x in cursor.description]
        rows = cursor.fetchall()
        rows = list(rows)
        grn_dtl = pd.DataFrame(rows, columns=columns)
        return grn_dtl

    def get_send_mail(self):
        cursor = connection.cursor()
        parameters = (self.action, self.type, self.filter, self.classification, '');

        ap_model.print_parameters("sp_MailDetail_Get", parameters);

        cursor.callproc('sp_MailDetail_Get', parameters)
        columns = [x[0] for x in cursor.description]
        rows = cursor.fetchall()
        rows = list(rows)
        grn_dtl = pd.DataFrame(rows, columns=columns)
        return grn_dtl

    def get_multiple_email_templates_data(self):
        cursor = connection.cursor()
        parameters = (self.action, self.type, self.filter, self.classification, '');

        ap_model.print_parameters("sp_Mailtemplates_Get", parameters);
        data={}
        cursor.callproc('sp_Mailtemplates_Get', parameters)
        columns = [x[0] for x in cursor.description]
        rows = cursor.fetchall()
        rows = list(rows)
        result_data = pd.DataFrame(rows, columns=columns)
        data['Mail_Data'] = json.loads(result_data.to_json(orient='records'))
        i = 0
        while (cursor.nextset()):
            if (i != 1):
                columns = [x[0] for x in cursor.description]
                rows = cursor.fetchall()
                rows = list(rows)
                result_data = pd.DataFrame(rows, columns=columns)
                if i == 0:
                    data['Header_Data'] = json.loads(result_data.to_json(orient='records'))
                    i = 1
        return data


    def get_ecf_billentry_details(self):
        cursor = connection.cursor()
        parameters = (self.action, self.type, self.filter, self.classification, '');

        ap_model.print_parameters("sp_ECFProcess_Get", parameters);

        data = {}
        cursor.callproc('sp_ECFProcess_Get', parameters)
        columns = [x[0] for x in cursor.description]
        rows = cursor.fetchall()
        rows = list(rows)
        grn_dtl = pd.DataFrame(rows, columns=columns)
        data['INVOICE'] = json.loads(grn_dtl.to_json(orient='records'))
        i = 0
        while (cursor.nextset()):
            if (i != 2):
                columns = [x[0] for x in cursor.description]
                rows = cursor.fetchall()
                rows = list(rows)
                grn_dtl = pd.DataFrame(rows, columns=columns)
                if i == 0:
                    data['DEBIT'] = json.loads(grn_dtl.to_json(orient='records'))
                    i = 1
                else:
                    data['CREDIT'] = json.loads(grn_dtl.to_json(orient='records'))
                    i = 2
        return data

    def get_ecf_pdf_data(self):
        cursor = connection.cursor()
        parameters = (self.action, self.type, self.filter, self.classification, '');
        p = (self.action, self.type, self.filter, self.classification, "@message")

        ap_model.print_parameters("sp_ECFbarcodegen_Get", parameters);
        data = {}
        cursor.callproc('sp_ECFbarcodegen_Get', parameters)
        columns = [x[0] for x in cursor.description]
        rows = cursor.fetchall()
        rows = list(rows)
        grn_dtl = pd.DataFrame(rows, columns=columns)
        data['INVOICE_HEADER'] = json.loads(grn_dtl.to_json(orient='records'))
        i = 0
        while (cursor.nextset()):
            if (i != 3):
                columns = [x[0] for x in cursor.description]
                rows = cursor.fetchall()
                rows = list(rows)
                grn_dtl = pd.DataFrame(rows, columns=columns)
                if i == 0:
                    data['INVOICE_DETAIL'] = json.loads(grn_dtl.to_json(orient='records'))
                    i = 1
                elif i == 1:
                    data['DEBIT'] = json.loads(grn_dtl.to_json(orient='records'))
                    i = 2
                elif i == 2:
                    data['CREDIT'] = json.loads(grn_dtl.to_json(orient='records'))
                    i = 3
        return data

    def get_ecf_form_details(self):
        cursor = connection.cursor()
        parameters = (self.action, self.type, self.filter, self.classification, '');
        p = (self.action, self.type, self.filter, self.classification, "@message")

        ap_model.print_parameters("sp_ECFProcess_Get", parameters);
        data = {}
        cursor.callproc('sp_ECFProcess_Get', parameters)
        columns = [x[0] for x in cursor.description]
        rows = cursor.fetchall()
        rows = list(rows)
        grn_dtl = pd.DataFrame(rows, columns=columns)
        data['INVOICE_HEADER'] = json.loads(grn_dtl.to_json(orient='records'))
        i = 0
        while (cursor.nextset()):
            if (i != 3):
                columns = [x[0] for x in cursor.description]
                rows = cursor.fetchall()
                rows = list(rows)
                grn_dtl = pd.DataFrame(rows, columns=columns)
                if i == 0:
                    data['INVOICE_DETAIL'] = json.loads(grn_dtl.to_json(orient='records'))
                    i = 1
                elif i == 1:
                    data['DEBIT'] = json.loads(grn_dtl.to_json(orient='records'))
                    i = 2
                elif i == 2:
                    data['CREDIT'] = json.loads(grn_dtl.to_json(orient='records'))
                    i = 3
        return data

    def set_emp_bank(self):
        cursor = connection.cursor()
        parameters = (
        self.action, self.type, self.sub_type, self.jsondata, self.json_classification, self.employee_gid, '')

        ap_model.print_parameters("sp_AP_Emp_Bank_Set", parameters);

        cursor.callproc('sp_AP_Emp_Bank_Set', parameters)
        cursor.execute('select @_sp_AP_Emp_Bank_Set_6')
        out_message = cursor.fetchone()
        return {"MESSAGE": out_message[0]}

    def get_master_data(self):
        cursor = connection.cursor()
        parameters = (self.type, self.sub_type,self.filter_json,self.limit, self.json_classification, '')
        ap_model.print_parameters("sp_Mst_Data_Get", parameters);
        cursor.callproc('sp_Mst_Data_Get', parameters)
        columns = [x[0] for x in cursor.description]
        rows = cursor.fetchall()
        cursor.execute('select @_sp_Mst_Data_Get_5')
        outmsg_sp = cursor.fetchone()
        rows = list(rows)
        df_asset_cat = pd.DataFrame(rows, columns=columns)
        return {"DATA": df_asset_cat, "MESSAGE": outmsg_sp[0]}

    def get_emp_bank(self):
        cursor = connection.cursor()
        parameters = (self.type, self.sub_type, self.filter_json, self.json_classification, '')
        cursor.callproc('sp_AP_Emp_Bank_Get', parameters)

        ap_model.print_parameters("sp_AP_Emp_Bank_Get", parameters);

        if cursor.description != None:
            columns = [x[0] for x in cursor.description]
            rows = cursor.fetchall()
            cursor.execute('select @_sp_AP_Emp_Bank_Get_4')
            outmsg_sp = cursor.fetchone()
            rows = list(rows)
            df_asset_cat = pd.DataFrame(rows, columns=columns)
            return {"DATA": df_asset_cat, "MESSAGE": outmsg_sp[0]}

        else:
            cursor.execute('select @_sp_AP_Emp_Bank_Get_4')
            sp_out_msg = cursor.fetchone()
            return {"MESSAGE": sp_out_msg[0], "DATA": "NO_DATA"}

    def Invoice_get_(self):
        cursor = connection.cursor()
        parameters = (
            self.action, self.ponumber, self.supplier_gid, self.inwardheader_gid, self.inwarddetail_gid, self.status,
            self.state_gid, self.entity_gid, 1, '')
        
        ap_model.print_parameters("sp_APInvoice_Get",parameters)

        cursor.callproc('sp_APInvoice_Get', parameters)
        columns = [x[0] for x in cursor.description]
        rows = cursor.fetchall()
        rows = list(rows)
        grn_dtl = pd.DataFrame(rows, columns=columns)
        while (cursor.nextset()):
            # fetch rows from next set, discarding first
            rows = cursor.fetchall()
        return grn_dtl
    
    def get_delmat_datas(self):
        cursor = connection.cursor()
        parameters = (self.action, self.type, self.filter, self.classification, '')
        ap_model.print_parameters("sp_Delmatlimit_Get", parameters);
        cursor.callproc('sp_Delmatlimit_Get', parameters)
        columns = [x[0] for x in cursor.description]
        rows = cursor.fetchall()
        cursor.execute('select @_sp_Delmatlimit_Get_4')
        outmsg_sp = cursor.fetchone()
        rows = list(rows)
        emp_data = pd.DataFrame(rows, columns=columns)
        return emp_data

    def get_ecfAP_billentry_details(self):
        cursor = connection.cursor()
        parameters = (self.action, self.type, self.filter, self.classification, '');

        ap_model.print_parameters("sp_ECFAPdata_Get", parameters);

        data = {}
        cursor.callproc('sp_ECFAPdata_Get', parameters)
        columns = [x[0] for x in cursor.description]
        rows = cursor.fetchall()
        rows = list(rows)
        grn_dtl = pd.DataFrame(rows, columns=columns)
        data['invoice'] = json.loads(grn_dtl.to_json(orient='records'))
        i = 0
        while (cursor.nextset()):
            if (i != 1):
                columns = [x[0] for x in cursor.description]
                rows = cursor.fetchall()
                rows = list(rows)
                grn_dtl = pd.DataFrame(rows, columns=columns)
                if i == 0:
                    data['credit'] = json.loads(grn_dtl.to_json(orient='records'))
                    i = 1
                else:
                    data['CREDIT'] = json.loads(grn_dtl.to_json(orient='records'))
                    i = 2
        return data

    def get_APbankdetails(self):
        cursor = connection.cursor()
        parameters = (self.action, self.type, self.filter, self.classification, '');
        ap_model.print_parameters("sp_APbankdetails_Get", parameters)
        cursor.callproc('sp_APbankdetails_Get', parameters)
        columns = [x[0] for x in cursor.description]
        rows = cursor.fetchall()
        rows = list(rows)
        grn_dtl = pd.DataFrame(rows, columns=columns)
        if (self.type == "SUPPLIER_DETAILS"):
            i = 0
            while (cursor.nextset()):
                if (i != 1):
                    columns = [x[0] for x in cursor.description]
                    row = cursor.fetchall()
                    row = list(row)
                    tds = pd.DataFrame(row, columns=columns)
                    grn_dtl['tds_data'] = tds.to_json(orient='records')
                    i = 1
        return grn_dtl

    def get_bank_details(self):
        cursor = connection.cursor()
        parameters = (self.entity_gid, '',)
        ap_model.print_parameters("sp_CompanyBankDetails_Get",parameters)

        cursor.callproc('sp_CompanyBankDetails_Get', parameters)
        columns = [x[0] for x in cursor.description]
        rows = cursor.fetchall()
        rows = list(rows)
        bank_details = pd.DataFrame(rows, columns=columns)
        return bank_details

    def get_pmd_details(self):
        cursor = connection.cursor()
        parameters = (self.action, self.type, self.filter, self.classification, '');
        ap_model.print_parameters("sp_PMD_Get",parameters)

        cursor.callproc('sp_PMD_Get', parameters)
        columns = [x[0] for x in cursor.description]
        rows = cursor.fetchall()
        rows = list(rows)
        bank_details = pd.DataFrame(rows, columns=columns)
        return bank_details

    def set_pmd_details(self):
        cursor = connection.cursor()
        parameters = (self.action, self.type, self.filter, self.classification, '')

        ap_model.print_parameters("sp_PMD_Set", parameters);

        cursor.callproc('sp_PMD_Set', parameters)
        cursor.execute('select @_sp_PMD_Set_4')
        output_msg = cursor.fetchone()
        return output_msg

    def set_file_details(self):
        cursor = connection.cursor()
        parameters = (self.action, self.type, self.filter, self.classification,self.create_by, '')
        ap_model.print_parameters("sp_FileDetail_Set", parameters);
        cursor.callproc('sp_FileDetail_Set', parameters)
        cursor.execute('select @_sp_FileDetail_Set_5')
        output_msg = cursor.fetchone()
        return output_msg

    def get_hedergid_crnno(self):
        cursor = connection.cursor()
        parameters = (self.action, self.type, self.filter,'');
        ap_model.print_parameters("sp_ECF_Crnno_Get",parameters)
        cursor.callproc('sp_ECF_Crnno_Get', parameters)
        columns = [x[0] for x in cursor.description]
        rows = cursor.fetchall()
        rows = list(rows)
        hedergid = pd.DataFrame(rows, columns=columns)
        return hedergid

    def ap_update_flag(self):
        cursor = connection.cursor()
        parameters = (self.action, self.type, self.filter, self.classification, self.create_by, '');
        ap_model.print_parameters("sp_AP_Update_Status", parameters)
        cursor.callproc('sp_AP_Update_Status', parameters)
        cursor.execute('select @_sp_AP_Update_Status_5')
        output_msg = cursor.fetchone()
        return output_msg

    def set_day_entry_details(self):
        cursor = connection.cursor()
        parameters = (self.action, self.type, self.filter, self.classification,self.employee_gid, '')
        ap_model.print_parameters("sp_Dayentry_Set", parameters);
        cursor.callproc('sp_Dayentry_Set', parameters)
        cursor.execute('select @_sp_Dayentry_Set_5')
        output_msg = cursor.fetchone()
        return output_msg