import logging
import traceback

from django.db import connection
import pandas as pd
import json
from Bigflow.Transaction.Model import mFET
from Bigflow.Core.models import MasterRequestObject


class Purchase_model(mFET.FET_model):
    def __init__(self):
        self.prheader_gid = 0
        self.prdetail_gid = 0
        self.poheader_gid = 0
        self.podetails_gid = 0
        self.grnheader_gid = 0
        self.grndetail_gid = 0
        self.serail_no = 0
        self.date = ""
        self.product_qty = 0
        self.status = ""
        self.action = ""
        self.amount = 0.00
        self.netamount = 0.00
        self.per_unitamt = 0.00
        self.prod_cat_gid = 0
        self.prod_cat_name = ""
        self.product_gid = 0
        self.product_name = ""
        self.prod_type_name = ""
        self.prod_type_gid = 0
        self.umo_gid = 0
        self.umo_name = ""
        self.tax_gid = 0
        self.taxamt = 0.00
        self.supplier_gid = 0
        self.supplier_name = ""
        self.teamandcont_gid = 0
        self.teamandcont_name = ""
        self.actionsys = ""
        self.prpo_gid = 0
        self.godown_gid = 0
        self.dcno = ""
        self.remark = ""
        self.Employee_gid = 0
        self.tablename = ''
        self.gid = 0
        self.amement_gid = ""
        self.vesion_gid = 0
        self.delivery_gid = 0
        self.adment_hrdgid = 0
        self.adment_details_gid = 0
        self.vendor=''
        self.ref_gid=0
        self.reftable=''
        self.totype=''
        self.to=''
        self.remarks=''
        self.from_year=''
        self.to_year=''
        self.from_month = ''
        self.to_month = ''


    def set_prheader(self):
        cursor = connection.cursor()
        parameters = (self.action, self.date, self.Employee_gid, self.status,self.branchcode,self.mepnumber,self.totalamt,self.commodity_gid,self.entity_gid, self.Employee_gid, '')
        cursor.callproc('sp_PRHeader_Set', parameters)
        cursor.execute('select @_sp_PRHeader_Set_10')
        output_msg = cursor.fetchone()
        cursor.close()
        return output_msg

    def set_prdetails(self):
        cursor = connection.cursor()
        parameters = (self.prheader_gid, self.product_gid, self.product_qty,self.supplier_gid, self.entity_gid, self.Employee_gid, '')
        cursor.callproc('sp_PRDetail_Set', parameters)
        cursor.execute('select @_sp_PRDetail_Set_6')
        output_msg = cursor.fetchone()
        cursor.close()
        return output_msg

    def set_prdetailupdate(self):
        cursor = connection.cursor()
        parameters = (self.prdetail_gid, self.product_gid, self.product_qty, '')
        cursor.callproc('sp_PRDetailUpdate_Set', parameters)
        cursor.execute('select @_sp_PRDetailUpdate_Set_3')
        output_msg = cursor.fetchone()
        cursor.close()
        return output_msg

#insertprccbs
    def insertprccbs(self):
        cursor = connection.cursor()

        if(self.action=='Update'):
            parameters = (self.action, self.type, json.dumps(self.prheaderddl), self.productsddl, '{}', self.draft, self.emp, '')
        else:
            parameters = (self.action, self.type, json.dumps(self.prheaderddl), self.productsddl, '{}', self.classification_json, self.emp, '')
        cursor.callproc('sp_PRrequestSPS_Set', parameters)
        cursor.execute('select @_sp_PRrequestSPS_Set_7')
        output_msg = cursor.fetchone()
        cursor.close()
        return output_msg

    def get_prapproval(self):
        cursor = connection.cursor()
        parameters = (self.action, self.type,self.filter, self.enty, '')
        # parameters = (self.Employee_gid,self.enty, '')
        cursor.callproc('sp_POprocess_Get', parameters)
        # print("aaa",parameters)
        columns = [x[0] for x in cursor.description]
        rows = cursor.fetchall()
        rows = list(rows)
        df_prapproval = pd.DataFrame(rows, columns=columns)
        cursor.close()
        return df_prapproval

    def get_prheader(self):
        cursor = connection.cursor()
        parameters = (self.action, self.data, self.Entity_gid, self.Employee_gid, '')
        # print(parameters)
        cursor.callproc('sp_PRHeader_Get', parameters)
        columns = [x[0] for x in cursor.description]
        rows = cursor.fetchall()
        rows = list(rows)
        cursor.execute('select @_sp_PRHeader_Get_4')
        outmsg_sp = cursor.fetchone()
        cursor.close()
        df_prheader = pd.DataFrame(rows, columns=columns)

        return {"DATA": df_prheader, "MESSAGE": outmsg_sp[0]}



    def getfinalapprovalget(self):
        cursor = connection.cursor()
        parameters = ('select','')
        cursor.callproc('sp_Finalapproval_Get', parameters)
        columns = [x[0] for x in cursor.description]
        rows = cursor.fetchall()
        rows = list(rows)
        cursor.close()
        df_prheader = pd.DataFrame(rows, columns=columns)
        return df_prheader

    def getPoheader_details(self):
        cursor = connection.cursor()
        parameters = (self.type,self.filter_json,self.classification_json, self.create_by, '')
        #parameters = ('get','{"poheader_gid":1}','{"entity_gid":1}',1,'')
        cursor.callproc('sp_PO_Summary_Details_Get', parameters)
        columns = [x[0] for x in cursor.description]
        rows = cursor.fetchall()
        cursor.close()
        rows = list(rows)
        df_prheader = pd.DataFrame(rows, columns=columns)
        return df_prheader




    def get_prdetails(self):
        cursor = connection.cursor()
        parameters = (self.action,self.prheader_gid, self.product_name, self.Employee_gid,self.entity_gid, '')
        # print(parameters)
        cursor.callproc('sp_PRDetail_Get', parameters)
        columns = [x[0] for x in cursor.description]
        rows = cursor.fetchall()
        rows = list(rows)
        cursor.close()
        df_prdetails = pd.DataFrame(rows, columns=columns)
        return df_prdetails

    def get_poheader(self):
        cursor = connection.cursor()
        parameters = (self.type, self.filter_json, self.classification_json, self.create_by, '')
        cursor.callproc('sp_POHeader_Get', parameters)
        columns = [x[0] for x in cursor.description]
        rows = cursor.fetchall()
        rows = list(rows)
        cursor.close()
        df_poheader = pd.DataFrame(rows, columns=columns)
        return df_poheader

    def get_po_header_details(self):
        cursor = connection.cursor()
        parameters = (self.type, self.filter_json, self.classification_json, self.create_by,'')
        # print(parameters)
        cursor.callproc('sp_POHeader_Get', parameters)
        columns = [x[0] for x in cursor.description]
        rows = cursor.fetchall()
        rows = list(rows)
        cursor.close()
        df_poheader = pd.DataFrame(rows, columns=columns)
        return df_poheader


    def get_podetails(self):
        cursor = connection.cursor()
        parameters = (self.podetails_gid, self.product_name, self.Employee_gid, '')
        cursor.callproc('sp_PODetail_Get', parameters)
        # print(parameters)
        columns = [x[0] for x in cursor.description]
        rows = cursor.fetchall()
        rows = list(rows)
        cursor.close()
        df_podetails = pd.DataFrame(rows, columns=columns)
        return df_podetails

    def get_poamend(self):
        cursor = connection.cursor()
        parameters = (self.action, self.type,self.jsondata, self.classification,self.create_by, '')
        cursor.callproc('sp_POAmendment_Get', parameters)
        columns = [x[0] for x in cursor.description]
        rows = cursor.fetchall()
        cursor.close()
        rows = list(rows)
        df_grndetail = pd.DataFrame(rows, columns=columns)
        return df_grndetail



    def get_poapproval(self):
        cursor = connection.cursor()
        parameters = (self.serail_no, self.status, self.supplier_name, self.amount)
        cursor.callproc('sp_POApproval_Get', parameters)
        columns = [x[0] for x in cursor.description]
        rows = cursor.fetchall()
        rows = list(rows)
        cursor.close()
        df_poapproval = pd.DataFrame(rows, columns=columns)
        return df_poapproval

    def get_pocolse(self):
        cursor = connection.cursor()
        parameters = (self.action, self.type, self.po_data, self.classification_json, '')
        cursor.callproc('sp_POClose_Get', parameters)
        # print(parameters)
        columns = [x[0] for x in cursor.description]
        rows = cursor.fetchall()
        rows = list(rows)
        cursor.close()
        df_poclose = pd.DataFrame(rows, columns=columns)
        return df_poclose

    def get_pocloseapproval(self):
        cursor = connection.cursor()
        parameters = (self.serail_no, self.amount, self.Employee_gid, self.status)
        cursor.callproc('sp_POCloseApproval_Get', parameters)
        # print( 'sp_POCloseApproval_Get', parameters)
        columns = [x[0] for x in cursor.description]
        rows = cursor.fetchall()
        rows = list(rows)
        cursor.close()
        df_pocloseapproval = pd.DataFrame(rows, columns=columns)
        return df_pocloseapproval

    def get_poreopen(self):
        cursor = connection.cursor()
        parameters = (self.serail_no, self.supplier_name, self.amount, self.status, self.Employee_gid)
        cursor.callproc('sp_POReopenView_Get', parameters)
        # print(parameters)
        columns = [x[0] for x in cursor.description]
        rows = cursor.fetchall()
        rows = list(rows)
        cursor.close()
        df_poreopen = pd.DataFrame(rows, columns=columns)
        return df_poreopen

    def get_pocancel(self):
        cursor = connection.cursor()
        parameters = (self.action,self.type,self.pocancel_data,self.classification_json,'')#

        cursor.callproc('sp_POCancelView_Get', parameters)
        columns = [x[0] for x in cursor.description]
        rows = cursor.fetchall()
        rows = list(rows)
        cursor.close()
        df_pocancel = pd.DataFrame(rows, columns=columns)
        return df_pocancel

    def get_pocancelapproval(self):
        cursor = connection.cursor()
        parameters = (self.serail_no, self.amount, self.Employee_gid, self.status)
        #print(parameters)
        cursor.callproc('sp_POCancelApproval_Get', parameters)
        #print(parameters)
        columns = [x[0] for x in cursor.description]
        rows = cursor.fetchall()
        rows = list(rows)
        cursor.close()
        df_pocancelapproval = pd.DataFrame(rows, columns=columns)
        return df_pocancelapproval

    def get_poqty(self):
        cursor = connection.cursor()
        parameters = (self.action,self.supplier_gid, self.product_gid, self.product_name, self.serail_no, '')
        cursor.callproc('sp_POQtyList_Get', parameters)
        columns = [x[0] for x in cursor.description]
        rows = cursor.fetchall()
        rows = list(rows)
        cursor.close()
        df_poqty = pd.DataFrame(rows, columns=columns)
        return df_poqty

    def get_supplier(self):
        cursor = connection.cursor()
        jsondatadetl = self.vendor
        vendor_del = json.dumps(jsondatadetl)
        parameters = (self.action, self.type,vendor_del, '')
       # print(parameters)
        cursor.callproc('sp_Suppliercapacity_Get', parameters)
        columns = [x[0] for x in cursor.description]
        rows = cursor.fetchall()
        rows = list(rows)
        cursor.close()
        df_poqty = pd.DataFrame(rows, columns=columns)
        return df_poqty


    def set_poamend(self):
        cursor = connection.cursor()
        parameters = (self.action, self.type, self.jsondata, self.classification, self.create_by, '')
        cursor.callproc('sp_POAmendment_Update_Set', parameters)
        cursor.execute('select @_sp_POAmendment_Update_set_5')
        output_msg = cursor.fetchone()
        cursor.close()
        return output_msg


    def set_poapprovalupdate(self):
        cursor = connection.cursor()
        parameters = (self.action, self.poheader_gid, self.remark, self.entity_gid, self.Employee_gid, '')
        cursor.callproc('sp_POApproval_Update_set', parameters)
       # print('Approval_Update',parameters)
        cursor.execute('select @_sp_POApproval_Update_set_5')
        output_msg = cursor.fetchone()
        cursor.close()
        return output_msg

    def set_poapprovalviewupdate(self):
        cursor = connection.cursor()
        parameters = (
        self.action, self.actionsys, self.poheader_gid, self.remark, self.entity_gid, self.Employee_gid, '')
        # print('rrrrrrrr',parameters)
        cursor.callproc('sp_POApprovalView_Update_set', parameters)
        cursor.execute('select @_sp_POApprovalView_Update_set_6')
        output_msg = cursor.fetchone()
        cursor.close()
        return output_msg

    def set_poreject(self):
        cursor = connection.cursor()
        parameters = (self.Type, self.actionsys, self.lj_filters, self.lj_classification, '')
        cursor.callproc('sp_PonewRejection_Set', parameters)
        cursor.execute('select @_sp_PonewRejection_Set_4')
        output_msg = cursor.fetchone()
        cursor.close()
        return output_msg

    def set_poapproval(self):
        cursor = connection.cursor()
        parameters = (self.action, self.poheader_gid,self.Employee_gid,self.lsremaks,self.empname, '')
        cursor.callproc('sp_POApproval_Set', parameters)
        cursor.execute('select @_sp_POApproval_Set_5')
        output_msg = cursor.fetchone()
        cursor.close()
        return output_msg

    def set_poheaderupdate(self):
        cursor = connection.cursor()
        parameters = (self.action, self.poheader_gid,self.teamandcont_gid,self.from_date,self.to_date, self.amount,self.create_by,self.entity_gid ,'')
        cursor.callproc('sp_POHeaderUpdate_Set', parameters)
        cursor.execute('select @_sp_POHeaderUpdate_Set_8')
        output_msg = cursor.fetchone()
        cursor.close()
        return output_msg

    def set_podetailupdate(self):
        cursor = connection.cursor()
        parameters = (self.podetails_gid, self.product_gid, self.product_qty,self.per_unitamt ,self.amount,'0.00',self.netamount,self.Employee_gid,'')
        cursor.callproc('sp_PODetailUpdate_Set', parameters)
        cursor.execute('select @_sp_PODetailUpdate_Set_8')
        output_msg = cursor.fetchone()
        cursor.close()
        return output_msg

    def set_prpoqty(self):
        cursor = connection.cursor()
        parameters = (
        self.action, self.poheader_gid, self.podetails_gid, self.prdetail_gid,self.prpoqty_prccbs_gid, self.product_qty, self.entity_gid,
        self.Employee_gid, self.prpo_gid, '')
        cursor.callproc('sp_PRPOQty_Set', parameters)
        cursor.execute('select @_sp_PRPOQty_Set_9')
        output_msg = cursor.fetchone()
        cursor.close()
        return output_msg

    def set_podelivery(self):
        cursor = connection.cursor()
        parameters = (
        self.action, self.poheader_gid, self.podetails_gid, self.product_gid,self.podelivery_prpoqty_gid,self.podelivery_ccbs, self.product_qty, self.reftable,
        self.entity_gid, self.Employee_gid, self.delivery_gid, '')
        cursor.callproc('sp_PODelivery_Set', parameters)
        cursor.execute('select @_sp_PODelivery_Set_11')
        output_msg = cursor.fetchone()
        cursor.close()
        return output_msg

    def gett_poapproval(self):
        cursor = connection.cursor()
        parameters = (self.serial_no, self.status, self.login_gid, '')
        cursor.callproc('sp_POApproval_Get', parameters)
        columns = [x[0] for x in cursor.description]
        rows = cursor.fetchall()
        cursor.close()
        rows = list(rows)
        df_poapproval = pd.DataFrame(rows, columns=columns)
        return df_poapproval

    def set_ponewapproval(self):
        cursor = connection.cursor()
        parameters = (
        self.action, self.header_gid, self.remarks, self.employee_name, self.entity_gid, self.create_by, '')
        cursor.callproc('sp_PONewApproval_Set', parameters)
        cursor.execute('select @_sp_PONewApproval_Set_6')
        output_msg = cursor.fetchone()
        cursor.close()
        return output_msg

    def set_delmatsave(self):
        cursor = connection.cursor()
        parameters = (self.action, self.type, self.array, self.enty, self.crtby, '')
        cursor.callproc('sp_PRDelmat_set', parameters)
        # print(parameters)
        cursor.execute('select @_sp_PRDelmat_set_5')
        output_msg = cursor.fetchone()
        cursor.close()
        return {"MESSAGE": output_msg[0]}

    def mep_pr (self):
        cursor = connection.cursor()
        parameters = ( self.type, self.sub_type,self.jsonData, self.json_classification ,'')
        cursor.callproc('sp_Mep_Process_Get', parameters)
        # print(parameters)
        columns = [x[0] for x in cursor.description]
        rows = cursor.fetchall()
        rows = list(rows)
        cursor.execute('select @_sp_Mep_Process_Get_4')
        outmsg_sp = cursor.fetchone()

        cursor.close()
        df_poapproval = pd.DataFrame(rows, columns=columns)
        return {"DATA": df_poapproval, "MESSAGE": outmsg_sp[0]}
    def PO_HeaderDDL (self):
        cursor = connection.cursor()
        parameters = ( self.action, self.type,self.jsonData, json.dumps(self.json_classification) ,'')
        cursor.callproc('sp_POprocess_Get', parameters)
        columns = [x[0] for x in cursor.description]
        rows = cursor.fetchall()
        rows = list(rows)
        cursor.execute('select @_sp_POprocess_Get_4')
        outmsg_sp = cursor.fetchone()
        cursor.close()
        df = pd.DataFrame(rows, columns=columns)
        return {"DATA": df, "MESSAGE": outmsg_sp[0]}


    def set_delmatupdate(self):
        cursor = connection.cursor()
        parameters = (self.action, self.type, self.array, self.enty, int(self.crtby), '')

        cursor.callproc('sp_PRDelmat_set', parameters)
        # print(parameters)
        cursor.execute('select @_sp_PRDelmat_set_5')
        output_msg = cursor.fetchone()
        cursor.close()

        return {"MESSAGE": output_msg[0]}



    # delmatlimit
    def delmatlimit(self):
        cursor = connection.cursor()
        parameters = (self.action, self.type, self.commodity_gid, self.entity_gid, self.limitamut, '')
        cursor.callproc('sp_pr_limit_Get', parameters)

        columns = [x[0] for x in cursor.description]
        rows = cursor.fetchall()
        # Close and delete cursor
        cursor.close()
        # del cursor
        # connection.close()
        rows = list(rows)
        df_del = pd.DataFrame(rows, columns=columns)
        return df_del




    def tranapp1(self):
        cursor = connection.cursor()
        self.filter_json = json.dumps(self.filter_json)
        self.classification_json = json.dumps(self.classification_json)
        parameters = (self.type, self.subtype, self.filter_json, self.classification_json, '')
        cursor.callproc('sp_Pr_Trans_Set', parameters)

        cursor.execute('select @_sp_Pr_Trans_Set_4')
        output_msg = cursor.fetchone()
        cursor.close()
        return output_msg

   # tran

    def tranapp(self):
        cursor = connection.cursor()
        parameters = (self.action,self.type,self.data,self.enty,'')
        cursor.callproc('sp_Pr_Trans_Set', parameters)
        cursor.execute('select @_sp_Pr_Trans_Set_4')
        output_msg = cursor.fetchone()
        cursor.close()
        return output_msg


    def pr_po_delete(self):
        cursor = connection.cursor()
        parameters = (self.action, self.data,self.enty, self.Employee_gid,'')
        cursor.callproc('Sp_PRDelete_Set', parameters)
        cursor.execute('select @_Sp_PRDelete_Set_4')
        output_msg = cursor.fetchone()
        cursor.close()
        return output_msg


    def set_delmatget(self):
        cursor = connection.cursor()
        parameters = (self.action,'{}',self.enty,  '')
        cursor.callproc('sp_PRDelmat_Get', parameters)
        columns = [x[0] for x in cursor.description]
        rows = cursor.fetchall()
        cursor.close()
        rows = list(rows)
        df_del= pd.DataFrame(rows, columns=columns)
        return df_del

    def getdraftddl(self):
        cursor = connection.cursor()
        parameters = ('INV_PROCESS', 'SINGLE',self.filter_json, '{}', '')
        cursor.callproc('sp_PRrequest_Get', parameters)
        columns = [x[0] for x in cursor.description]
        rows = cursor.fetchall()
        cursor.close()
        rows = list(rows)
        df_del = pd.DataFrame(rows, columns=columns)
        # df_del.loc[:, ~df_del.columns.duplicated()]
        return df_del

    def New_delmatget(self):
        cursor = connection.cursor()
        parameters = (self.Type,self.filter_json,self.json_classification,self.create_by,'')
        cursor.callproc('sp_NewDelmat_Get', parameters)

        columns = [x[0] for x in cursor.description]
        rows = cursor.fetchall()
        cursor.close()
        rows = list(rows)
        df_del= pd.DataFrame(rows, columns=columns)
        return df_del

    def get_podelivery(self):
        cursor = connection.cursor()
        parameters = (self.serail_no, '')
        cursor.callproc('sp_PODlvrygodown_Get', parameters)
        columns = [x[0] for x in cursor.description]
        rows = cursor.fetchall()
        cursor.close()
        rows = list(rows)
        df_podelivery = pd.DataFrame(rows, columns=columns)
        return df_podelivery

    def get_pogrndetails(self):
        cursor = connection.cursor()
        parameters = (self.grnheader_gid,self.supplier_gid, '')
        cursor.callproc('sp_GRNQtyList_Get', parameters)
        columns = [x[0] for x in cursor.description]
        rows = cursor.fetchall()
        cursor.close()
        rows = list(rows)
        df_podelivery = pd.DataFrame(rows, columns=columns)
        return df_podelivery

    def get_grnheader(self):
        cursor = connection.cursor()
        parameters = (self.action, self.type, self.filter,self.classification,'')
        cursor.callproc('sp_GRNHeader_Get', parameters)
        columns = [x[0] for x in cursor.description]
        rows = cursor.fetchall()
        cursor.close()
        rows = list(rows)
        df_grnheader = pd.DataFrame(rows, columns=columns)
        return df_grnheader

    def get_grndetails(self):
        cursor = connection.cursor()
        parameters = (self.grnheader_gid, self.supplier_gid, '')
        cursor.callproc('sp_GRNDetail_Get', parameters)
        columns = [x[0] for x in cursor.description]
        rows = cursor.fetchall()
        cursor.close()
        rows = list(rows)
        df_grndetail = pd.DataFrame(rows, columns=columns)
        return df_grndetail

    def set_grnheader(self):
        cursor = connection.cursor()
        parameters = (self.action, self.date, self.dcno,
                      self.invoice_no, self.remark, self.entity_gid, self.Employee_gid, '')
        cursor.callproc('sp_GRNHeader_Set', parameters)
        cursor.execute('select @_sp_GRNHeader_Set_7')
        output_msg = cursor.fetchone()
        cursor.close()
        return output_msg

    # def get_attendance_mis(self):
    #     cursor = connection.cursor()
    #     parameters = (self.type,self.sub_type,self.jsonData,self.json_classification,'')
    #     cursor.callproc('sp_OutstandingCustomer_Get',parameters)
    #     columns = [x[0] for x in cursor.description]
    #     rows = cursor.fetchall()
    #     cursor.execute('select @_sp_OutstandingCustomer_Get_4')
    #     outmsg_sp = cursor.fetchone()
    #     rows = list(rows)
    #     df_sales = pd.DataFrame(rows,columns=columns)
    #     return {"DATA":df_sales,"MESSAGE":outmsg_sp[0]}

    def get_attendance_mis(self):
        cursor = connection.cursor()
        parameters = (self.type, self.sub_type, self.jsonData, self.json_classification, '')
        cursor.callproc('sp_OutstandingCustomer_Get', parameters)
        columns = [x[0] for x in cursor.description]
        rows = cursor.fetchall()
        cursor.execute('select @_sp_OutstandingCustomer_Get_4')
        out_put = cursor.fetchone()
        rows = list(rows)
        df_preschedule = pd.DataFrame(rows, columns=columns)
        return df_preschedule


    def pending_posummary(self):
        cursor = connection.cursor()
        json1 = json.dumps(self.darta)
        Parameters = (self.Type,self.SubType,json1, '')
        cursor.callproc('sp_Openpo_Get', Parameters)
        columns = [x[0] for x in cursor.description]
        rows = cursor.fetchall()
        cursor.close()
        rows = list(rows)
        df_customer = pd.DataFrame(rows, columns=columns)

        return df_customer

    def alltable_data(self):
        cursor = connection.cursor()
        Parameters = (self.action, self.jdata, self.enty, '')
        cursor.callproc('sp_AllTableValues_Get', Parameters)
        columns = [x[0] for x in cursor.description]
        rows = cursor.fetchall()
        cursor.close()
        rows = list(rows)
        df_customer = pd.DataFrame(rows, columns=columns)
        return {"DATA": df_customer, "MESSAGE":"FOUND"}

    def getdelmattype(self):
        cursor = connection.cursor()
        Parameters = ('',self.data,self.entity_gid,'')
        cursor.callproc('sp_AllTableValues_Get', Parameters)
        columns = [x[0] for x in cursor.description]
        rows = cursor.fetchall()
        cursor.close()
        rows = list(rows)
        df_customer = pd.DataFrame(rows, columns=columns)
        return df_customer

    def Reftable_Get(self):
        cursor = connection.cursor()
        Parameters = ('',self.datas, self.entity_gid, '')
        cursor.callproc('sp_AllValuesRef_Get', Parameters)
        columns = [x[0] for x in cursor.description]
        rows = cursor.fetchall()
        cursor.close()
        rows = list(rows)
        df_customer = pd.DataFrame(rows, columns=columns)
        return df_customer



    def set_grnheaderupdate(self):
        cursor = connection.cursor()
        parameters = (self.action, self.grnheader_gid, self.date,
                      self.dcno, self.invoice_no,self.remark, '')
        cursor.callproc('sp_GRNHeaderUpdate_Set', parameters)
        cursor.execute('select @_sp_GRNHeaderUpdate_Set_6')
        output_msg = cursor.fetchone()
        cursor.close()
        return output_msg

    def set_grndetails(self):
        cursor = connection.cursor()
        parameters = (self.action, self.grnheader_gid, self.grndetail_gid,
                      self.poheader_gid, self.podetails_gid, self.product_qty, self.godown_gid, self.entity_gid,
                      self.Employee_gid, '')
        cursor.callproc('sp_GRNDetail_Set', parameters)
        cursor.execute('select @_sp_GRNDetail_Set_9')
        output_msg = cursor.fetchone()
        cursor.close()
        return output_msg

    def set_grnapproval(self):
        cursor = connection.cursor()
        parameters = (self.action, self.grnheader_gid, self.entity_gid,self.Employee_gid,self.remark, '')
        cursor.callproc('sp_GRNApproval_Set', parameters)
        cursor.execute('select @_sp_GRNApproval_Set_5')
        output_msg = cursor.fetchall()
        cursor.close()
        return output_msg

    def get_postatus(self):
        cursor = connection.cursor()
        cursor.callproc('sp_POStatus_Get')
        columns = [x[0] for x in cursor.description]
        rows = cursor.fetchall()
        cursor.close()
        rows = list(rows)
        postatus = pd.DataFrame(rows, columns=columns)
        return postatus

    def get_grnapprovalset(self):
        cursor = connection.cursor()
        parameters = (self.grnheader_gid, self.supplier_gid)
        cursor.callproc('sp_GRNApproval_Get',parameters)
        columns = [x[0] for x in cursor.description]
        rows = cursor.fetchall()
        cursor.close()
        rows = list(rows)
        postatus = pd.DataFrame(rows, columns=columns)
        return postatus



    def get_delivery(self):
        cursor = connection.cursor()
        parameters = (self.podetails_gid, '')
        cursor.callproc('sp_PODelivery_Get', parameters)
        # print(parameters)
        columns = [x[0] for x in cursor.description]
        rows = cursor.fetchall()
        cursor.close()
        rows = list(rows)
        detail = pd.DataFrame(rows, columns=columns)
        return detail

    def get_dropdown_details(self):
        cursor = connection.cursor()
        parameters = (self.tablename, self.gid, self.name,self.entity_gid,'')
        cursor.callproc('sp_Dropdown_Common_active_Get', parameters)

        columns = [x[0] for x in cursor.description]
        rows = cursor.fetchall()
        cursor.close()
        rows = list(rows)
        dropdown = pd.DataFrame(rows, columns=columns)
        return dropdown

    def get_productnames(self):
        cursor = connection.cursor()
        parameters = (self.action,self.date, self.supplier_gid, self.product_gid, self.char_active, '')
        cursor.callproc('sp_SupplierProductMap_Get', parameters)
        columns = [x[0] for x in cursor.description]
        rows = cursor.fetchall()
        cursor.close()
        rows = list(rows)
        data = pd.DataFrame(rows, columns=columns)
        return data

    def set_prapproval(self):
        cursor = connection.cursor()
        parameters = (self.action, self.prheader_gid, self.remark,self.empname,self.entity_gid, self.Employee_gid, '')
        cursor.callproc('sp_PRApproval_Set', parameters)
        cursor.execute('select @_sp_PRApproval_Set_6')
        output_msg = cursor.fetchone()
        cursor.close()
        return output_msg

    def set_prdelete(self):
        cursor = connection.cursor()
        parameters = (self.prdetail_gid, self.Employee_gid, '')
        cursor.callproc('sp_PRDelete_Set', parameters)
        cursor.execute('select @_sp_PRDelete_Set_2')
        output_msg = cursor.fetchone()
        cursor.close()
        return output_msg

    def set_prheaderupdate(self):
        cursor = connection.cursor()
        parameters = (self.action, self.prheader_gid,self.entity_gid,self.create_by, '')
        cursor.callproc('sp_PRHeaderUpdate_Set', parameters)
        cursor.execute('select @_sp_PRHeaderUpdate_Set_4')
        output_msg = cursor.fetchone()
        cursor.close()
        return output_msg

    def set_poheader(self):
        cursor = connection.cursor()
        parameters = (
            self.action, self.date, self.supplier_gid, self.teamandcont_gid, self.amount, self.amement_gid,
            self.vesion_gid, self.commodity_gid, self.branchgid, self.mepno,
            self.status, self.from_date, self.to_date, self.entity_gid, self.Employee_gid, '')
        cursor.callproc('sp_POHeader_Set', parameters)
        cursor.execute('select @_sp_POHeader_Set_15')
        output_msg = cursor.fetchone()
        cursor.close()
        return output_msg

    def set_podetails(self):
        cursor = connection.cursor()
        parameters = (
        self.poheader_gid, self.product_gid, self.product_qty, self.umo_gid, self.per_unitamt, self.amount, self.taxamt,
        self.netamount, self.entity_gid, self.Employee_gid, '')
        cursor.callproc('sp_PODetail_Set', parameters)
        cursor.execute('select @_sp_PODetail_Set_10')
        output_msg = cursor.fetchone()
        cursor.close()
        return output_msg

    def set_podetele(self):
        cursor = connection.cursor()
        parameters = (
            self.podetails_gid,  self.Employee_gid, self.entity_gid, '')
        cursor.callproc('sp_PODelete_Set', parameters)
        cursor.execute('select @_sp_PODelete_Set_3')
        output_msg = cursor.fetchone()
        cursor.close()
        return output_msg


    def set_trans(self):
        cursor = connection.cursor()
        parameters = ( self.action, self.ref_gid, self.reftable, self.status, self.totype, self.to,
                       self.remark, self.entity_gid, self.Employee_gid, '')
        cursor.callproc('sp_Trans_Set', parameters)
        cursor.execute('select @_sp_Trans_Set_9')
        output_msg = cursor.fetchone()
        cursor.close()
        return  output_msg

    def get_prstatus(self):
        cursor = connection.cursor()
        cursor.callproc('sp_PRStatus_Get')
        columns = [x[0] for x in cursor.description]
        rows = cursor.fetchall()
        cursor.close()
        rows = list(rows)
        prstatus = pd.DataFrame(rows, columns=columns)
        return prstatus

    def get_poadment(self):
        cursor = connection.cursor()
        parameters = ('0', '', '0.00', '', 0)
        cursor.callproc('sp_POAmendHeader_Get',parameters)
        columns = [x[0] for x in cursor.description]
        rows = cursor.fetchall()
        cursor.close()
        rows = list(rows)
        poamentment = pd.DataFrame(rows, columns=columns)
        return poamentment

    def get_poadmentapproval(self):
        cursor = connection.cursor()
        parameters = ('', '')
        cursor.callproc('sp_POAmendApproval_Get',parameters)
        columns = [x[0] for x in cursor.description]
        rows = cursor.fetchall()
        cursor.close()
        rows = list(rows)
        poamentment = pd.DataFrame(rows, columns=columns)
        return poamentment

    def get_salesplanningl(self):
        cursor = connection.cursor()
        parameters = (self.type,self.prod_type_gid,self.product_gid,self.from_year,self.to_year,self.from_month,self.to_month,'')
        cursor.callproc('sp_salespalnndtl_Get',parameters)
        columns = [x[0] for x in cursor.description]
        rows = cursor.fetchall()
        cursor.close()
        rows = list(rows)
        salesplanning = pd.DataFrame(rows, columns=columns)
        return salesplanning

    def get_purchplanningl(self):
        cursor = connection.cursor()
        parameters = (self.prod_type_gid,self.from_year,self.to_year,self.from_month,self.to_month,'')
        cursor.callproc('sp_Purchasepalnndtl_Get',parameters)
        columns = [x[0] for x in cursor.description]
        rows = cursor.fetchall()
        cursor.close()
        rows = list(rows)
        purchplanning = pd.DataFrame(rows, columns=columns)
        return purchplanning

    def get_producttype(self):
        cursor = connection.cursor()
        parameters = (self.prod_type_gid,self.supplier_gid)
        cursor.callproc('sp_Prodtype_Get',parameters)
        columns = [x[0] for x in cursor.description]
        rows = cursor.fetchall()
        cursor.close()
        rows = list(rows)
        producttype = pd.DataFrame(rows, columns=columns)
        return producttype

    def get_querystring(self):
        cursor = connection.cursor()
        parameters = (self.poheader_gid, self.podetails_gid,self.entity_gid,'')
        cursor.callproc('sp_querystring',parameters)
        columns = [x[0] for x in cursor.description]
        rows = cursor.fetchall()
        cursor.close()
        rows = list(rows)
        querystring = pd.DataFrame(rows, columns=columns)
        return querystring

    def get_questatus(self):
        cursor=connection.cursor()
        parameters=(self.tablename,self.ref_gid,self.status,self.entity_gid,'')
        cursor.callproc('sp_chkque_status',parameters)
        cursor.execute('select @_sp_chkque_status_4')
        output_msg = cursor.fetchone()
        cursor.close()
        # columns = [x[0] for x in cursor.description]
        # rows=cursor.fetchall()
        # rows=list(rows)
        # querystring = pd.DataFrame(rows, columns=columns)
        return output_msg
    #PR
    def get_pr_productcategory(self):
        cursor = connection.cursor()
        parameters = (self.action,self.type,self.data,self.classification_json,'')
        cursor.callproc('sp_PRProcess_Get', parameters)
        # print(parameters)
        columns = [x[0] for x in cursor.description]
        rows = cursor.fetchall()
        cursor.close()
        rows = list(rows)
        df_productcategoryddl = pd.DataFrame(rows, columns=columns)
        return df_productcategoryddl
    #product
    def get_alltablevalue(self):
        cursor = connection.cursor()
        parameters = (self.action, self.json_data, self.entity_gid, '')
        cursor.callproc('sp_AllTableValues_Get', parameters)
        columns = [x[0] for x in cursor.description]
        rows = cursor.fetchall()
        cursor.close()
        rows = list(rows)
        grn_dtl = pd.DataFrame(rows, columns=columns)
        return grn_dtl

    def get_commodity_master(self):
        cursor = connection.cursor()
        parameters = (self.action, self.type, self.jsondata, self.classification_json, '')
        cursor.callproc('sp_Commodity_Get', parameters)

        columns = [x[0] for x in cursor.description]
        rows = cursor.fetchall()
        cursor.close()
        rows = list(rows)
        grn_dtl = pd.DataFrame(rows, columns=columns)
        return grn_dtl

    #commo_productmap
    def commo_productmap(self):
        cursor = connection.cursor()
        Parameters = (self.value, self.value1, self.value2, '')
        cursor.callproc('sp_Commodityprod_Set', Parameters)
        cursor.execute('select @_sp_Commodityprod_Set_3')
        output_msg = cursor.fetchone()
        cursor.close()
        return output_msg

    #dimdim
    def dimdimmod(self):
        cursor = connection.cursor()
        entity=json.loads(self.value2).pop('Entity_Gid_sync')
        create_by= json.loads(self.value2).pop('Create_By_sync')
        Parameters = (self.value,self.value1,self.value2,'')
        cursor.callproc('sp_Commodity_Set', Parameters)
        cursor.execute('select @_sp_Commodity_Set_3')
        output_msg = cursor.fetchone()
        cursor.close()
        try:
            if (output_msg[0] == 'SUCCESSFULLY INSERTED'):
                print(json.loads(Parameters[1]))
                data = {'code':json.loads(Parameters[1]).get('Commodity_Code'),'name': json.loads(Parameters[1]).get('Commodity_Name'),'Entity_Gid':entity,'create_by':create_by}
                print(data)
                mrobject = MasterRequestObject("COMMODITY", data, 'POST')
        except:
            logging.ERROR(traceback.print_exc())
        return output_msg

    def get_allactive_Inactivedata(self):
        cursor = connection.cursor()
        Parameters = (self.action, self.jsonData,self.entity_gid,'')
        cursor.callproc('sp_Check_In_Active_Values_Get', Parameters)
        columns = [d[0] for d in cursor.description]
        rows = cursor.fetchall()
        rows = list(rows)
        ldict1 = pd.DataFrame(rows, columns=columns)
        return ldict1

    # Commodity_code_generate_model
    def codegen_commodity(self):
        cursor = connection.cursor()
        Parameters = (self.type, self.sub_type, self.filter_json,self.classification_json, '')
        cursor.callproc('sp_Commodity_Generate_No', Parameters)

        cursor.execute('select @_sp_Commodity_Generate_No_4')
        sp_out_message = cursor.fetchone()
        cursor.close()
        return {"DATA":sp_out_message[0]}


    #supplier_Dropdown
    def supplier_drop(self):
        cursor = connection.cursor()
        Parameters = (self.action, self.json_data, self.entity_gid, '')
        cursor.callproc('sp_vendorSelection_PoAggregate', Parameters)
        columns = [x[0] for x in cursor.description]
        rows = cursor.fetchall()
        cursor.close()
        rows = list(rows)
        df_add = pd.DataFrame(rows, columns=columns)
        return df_add

    # prccbs_details
    def prccbs_details(self):
        cursor = connection.cursor()
        Parameters = (self.Type, self.Sub_type, self.json_data, self.json_classification,self.create_by, '')
        cursor.callproc('sp_prheader_ccbs_get', Parameters)
        columns = [x[0] for x in cursor.description]
        rows = cursor.fetchall()
        cursor.close()
        rows = list(rows)
        df_ccbs = pd.DataFrame(rows, columns=columns)
        return df_ccbs

    #commoditydropdown
    def commoditydropdow(self):
        cursor = connection.cursor()
        Parameters = (self.value, self.value1, self.value2, '')
        cursor.callproc('sp_Commodity_Get', Parameters)
        columns = [x[0] for x in cursor.description]
        rows = cursor.fetchall()
        cursor.close()
        rows = list(rows)
        df_add = pd.DataFrame(rows, columns=columns)
        return df_add
    #PR Commodity_product data
    def Commodity_product_data(self):
        cursor = connection.cursor()
        Parameters = (self.action,self.pgid,self.engid,'')
        cursor.callproc('sp_Commodityprod_Get', Parameters)
        columns = [x[0] for x in cursor.description]
        rows = cursor.fetchall()
        cursor.close()
        rows = list(rows)
        df_add = pd.DataFrame(rows, columns=columns)
        return df_add

    def get_generatepoddl(self):
        cursor = connection.cursor()
        Parameters = (self.action, self.sub_type, self.jdata,self.entity_gid, '')
        cursor.callproc('sp_POprocess_Get', Parameters)
        columns = [x[0] for x in cursor.description]
        rows = cursor.fetchall()
        cursor.close()
        rows = list(rows)
        df_add = pd.DataFrame(rows, columns=columns)
        return df_add

    def get_sendmail(self):
        cursor = connection.cursor()
        Parameters = (self.action, self.sub_type, self.jdata,'{}','','', '')
        # print(Parameters)
        cursor.callproc('sp_POProcessDTS_Get', Parameters)
        columns = [x[0] for x in cursor.description]
        rows =  cursor.fetchall()
        # cursor.close()
        rows = list(rows)
        df_add = pd.DataFrame(rows, columns=columns)
        # data=[];
        df_add[['po_amount', 'supplier_unit_price','podetails_totalamount','hsn_igstrate','tax_amount']] = df_add[['po_amount', 'supplier_unit_price','podetails_totalamount','hsn_igstrate','tax_amount']].astype(float)
        df = pd.DataFrame(df_add)
        df['delivery_details'] = df['delivery_details'].apply(json.loads)
        df['total_amount'] = df['podetails_totalamount'].sum()

        dk = df.to_dict(orient='records')
        return dk
     #PR type
    def get_pr_product_types(self):
        cursor = connection.cursor()
        Parameters = (str(self.prodcat_gid),'')
        cursor.callproc('sp_Prodcat_Get', Parameters)
        columns = [x[0] for x in cursor.description]
        rows = cursor.fetchall()
        cursor.close()
        rows = list(rows)
        df_add = pd.DataFrame(rows, columns=columns)
        return df_add
    #PR product
    def get_pr_productname(self):
        cursor = connection.cursor()
        parameters = (self.producttype_gid,0)
        cursor.callproc('sp_Prodtype_Get', parameters)
        columns = [x[0] for x in cursor.description]
        rows = cursor.fetchall()
        cursor.close()
        rows = list(rows)
        productname = pd.DataFrame(rows, columns=columns)
        return productname

    def get_salescount(self):
        cursor = connection.cursor()
        json_fliter = json.dumps(self.fliter)
        json_classification = json.dumps(self.classification)
        parameters = (self.type,self.sub_type,json_fliter,json_classification,self.create_by,'')
        cursor.callproc('sp_SalesInvoice_Get', parameters)
        columns = [x[0] for x in cursor.description]
        rows = cursor.fetchall()
        cursor.close()
        rows = list(rows)
        salescount = pd.DataFrame(rows, columns=columns)
        return salescount
    def set_grn_data(self):
        cursor = connection.cursor()

        parameters = (self.action, self.type, self.jsonData, 'Y', self.json_classification, self.employee_gid, 0)
        cursor.callproc('sp_GRNDetails_Set', parameters)
        cursor.execute('select @_sp_GRNDetails_Set_6')
        output_msg = cursor.fetchone()
        cursor.close()
        return output_msg

    def grndetails_get_(self):
        cursor = connection.cursor()
        parameters = (self.type, self.sub_type, json.dumps(self.filter_json), '{}', '')
        # print(parameters)
        cursor.callproc('sp_GRNDetails_Get', parameters)
        columns = [x[0] for x in cursor.description]
        rows = cursor.fetchall()
        cursor.close()
        rows = list(rows)
        df_grndetail = pd.DataFrame(rows, columns=columns)
        return df_grndetail

    def grndetails_get(self):
        cursor = connection.cursor()
        parameters = (self.type, self.sub_type, json.dumps(self.filter_json), '{}', '')
        cursor.callproc('sp_GRNDetails_Get', parameters)
        # print(parameters)
        columns = [x[0] for x in cursor.description]
        rows = cursor.fetchall()
        cursor.close()
        rows = list(rows)
        df_grndetail = pd.DataFrame(rows, columns=columns)
        return df_grndetail

    def set_expense_line(self):
        cursor = connection.cursor()
        parameters = (self.action, self.type, self.filter, self.classification, self.create_by, '')
        cursor.callproc('sp_APExpenseLine_Set', parameters)
        cursor.execute('select @_sp_APExpenseLine_Set_5')
        output_msg = cursor.fetchone()
        cursor.close()
        return output_msg

    def get_expense_line(self):
        cursor = connection.cursor()
        parameters = (self.action, self.type, self.classification, '')
        cursor.callproc('sp_APExpenseLine_Get', parameters)
        columns = [x[0] for x in cursor.description]
        rows = cursor.fetchall()
        cursor.execute('select @_sp_APExpenseLine_Get_3')
        outmsg_sp = cursor.fetchone()
        rows = list(rows)
        branch_data = pd.DataFrame(rows, columns=columns)
        cursor.close()
        return branch_data
    def po_insert(self):
        cursor = connection.cursor()
        parameters = (self.type, self.action, self.datas,
                      self.classification_json, self.sub, self.crtb, '')
        cursor.callproc('sp_POProcessSPS_set', parameters)
        # print(parameters)
        cursor.execute('select @_sp_POProcessSPS_set_6')
        output_msg = cursor.fetchone()
        cursor.close()
        return output_msg

    def set_poterms(self):
        cursor = connection.cursor()
        parameters = (self.action, self.type,self.jsondata, self.classification,self.create_by, '')
        cursor.callproc('sp_Poterms_Set', parameters)
        # print(parameters)
        cursor.execute('select @_sp_Poterms_Set_5')
        output_msg = cursor.fetchone()
        cursor.close()
        return output_msg

    def set_poterms_temp(self):
        cursor = connection.cursor()
        parameters = (self.action, self.type,self.jsondata, self.classification,self.create_by, '')
        cursor.callproc('sp_Poterms_Template_Set', parameters)
        cursor.execute('select @_sp_Poterms_Template_Set_5')
        output_msg = cursor.fetchone()
        return output_msg

    def get_poterms(self):
        cursor = connection.cursor()
        parameters = (self.action, self.type,self.jsondata,self.classification,self.create_by, '')
        cursor.callproc('sp_Poterms_Get', parameters)
        # print(parameters)
        columns = [x[0] for x in cursor.description]
        rows = cursor.fetchall()
        cursor.close()
        rows = list(rows)
        df_grndetail = pd.DataFrame(rows, columns=columns)
        return df_grndetail

    def get_reportdatas(self):
        cursor = connection.cursor()
        parameters = (self.action,self.jsondata,self.classification,'')
        cursor.callproc('sp_PRPO_Report_Get', parameters)
        columns = [x[0] for x in cursor.description]
        rows = cursor.fetchall()
        cursor.close()
        rows = list(rows)
        df_grndetail = pd.DataFrame(rows, columns=columns)
        return df_grndetail


    def get_trandata(self):
        cursor = connection.cursor()
        parameters = ( self.type, self.sub_type,self.jsonData, self.json_classification ,'')
        cursor.callproc('sp_GRN_PR_PO_History', parameters)
        columns = [x[0] for x in cursor.description]
        rows = cursor.fetchall()
        rows = list(rows)
        cursor.execute('select @_sp_GRN_PR_PO_History_4')
        outmsg_sp = cursor.fetchone()
        cursor.close()
        df_poapproval = pd.DataFrame(rows, columns=columns)
        return {"DATA": df_poapproval, "MESSAGE": outmsg_sp[0]}


    def set_fa_maker_from_ms(self):
        if self.action != 'GRN':
            cursor = connection.cursor()
            parameters = (self.action,self.type,self.sub_type,self.jsondata,self.jsonData,self.json_file,self.jsonData_sec,self.json_classification,self.employee_gid,'')
            cursor.callproc('sp_POFlow_API', parameters)
            cursor.execute('select @_sp_POFlow_API_9')
            out_message = cursor.fetchone()
            return {"MESSAGE": out_message[0]}
        else:
            cursor = connection.cursor()
            parameters = (self.action,self.type,self.sub_type,self.jsondata,self.jsonData,self.json_file,self.jsonData_sec,self.json_classification,self.employee_gid,'')
            # print(parameters)
            cursor.callproc('sp_POFlow_API', parameters)
            columns = [x[0] for x in cursor.description]
            rows = cursor.fetchall()
            cursor.close()
            rows = list(rows)
            df_grndetail = pd.DataFrame(rows, columns=columns)
            return df_grndetail
