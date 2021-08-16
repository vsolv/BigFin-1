from django.db import connection
import pandas as pd
from Bigflow.Master.Model import mVariable
import json

class ATMA_model(mVariable.variable):
    def atmaSet_Catalog(self):
        cursor = connection.cursor()
        Parameters = (self.action, self.jsonData, self.dataw, '')
        cursor.callproc('sp_Atma_activitydtlpproduct_Set', Parameters)
        cursor.execute('select @_sp_Atma_activitydtlpproduct_Set_3')
        df_header = cursor.fetchone()
        return df_header[0]

    def atmaSet_AssginCatalog(self):
        cursor = connection.cursor()
        Parameters = (self.action, self.jsonData, self.dataw, '')
        cursor.callproc('sp_Atma_Assign_Catalog_Set', Parameters)
        cursor.execute('select @_sp_Atma_Assign_Catalog_Set_3')
        df_header = cursor.fetchone()
        return df_header[0]

    def update_catalogdetails(self):
        cursor = connection.cursor()
        Parameters = (self.action, self.jsonData, self.dataw, '')
        cursor.callproc('sp_Atma_activitydtlpproduct_Set', Parameters)
        cursor.execute('select @_sp_Atma_activitydtlpproduct_Set_3')
        df_header = cursor.fetchone()
        return df_header

    def atmaget_ProductCatSubCat(self):
        cursor = connection.cursor()
        parameters = (self.type, self.jsonData, self.json_classification, '')
        cursor.callproc('sp_APCatSubCat_Get', parameters)
        columns = [x[0] for x in cursor.description]
        rows = cursor.fetchall()
        cursor.execute('select @_sp_APCatSubCat_Get_3')
        outmsg_sp = cursor.fetchone()
        rows = list(rows)
        df_sales = pd.DataFrame(rows, columns=columns)
        return {"DATA": df_sales, "MESSAGE": outmsg_sp[0]}

    def atmaget_catalog(self):
        cursor = connection.cursor()
        parameters = (self.type, self.jsonData, self.json_classification, '')
        cursor.callproc('sp_Atma_activitydtlpproduct_Get', parameters)
        columns = [x[0] for x in cursor.description]
        rows = cursor.fetchall()
        cursor.execute('select @_sp_Atma_activitydtlpproduct_Get_3')
        outmsg_sp = cursor.fetchone()
        rows = list(rows)
        df_sales = pd.DataFrame(rows, columns=columns)
        return {"DATA": df_sales, "MESSAGE": outmsg_sp[0]}

    def getcatalog_partnerproduct(self):
        cursor = connection.cursor()
        parameters = (self.type, self.jsonData, self.json_classification, '')
        cursor.callproc('sp_Atma_Product_Name_Get', parameters)
        columns = [x[0] for x in cursor.description]
        rows = cursor.fetchall()
        cursor.execute('select @_sp_Atma_Product_Name_Get_3')
        outmsg_sp = cursor.fetchone()
        rows = list(rows)
        df_sales = pd.DataFrame(rows, columns=columns)
        return {"DATA": df_sales, "MESSAGE": outmsg_sp[0]}

    def atma_summary(self):
        cursor = connection.cursor()
        parameters = (self.Action, self.jsonData, self.json_classification, '')
        cursor.callproc('sp_Atma_Partner_Get', parameters)
        columns = [x[0] for x in cursor.description]
        rows = cursor.fetchall()
        rows = list(rows)
        df_sales = pd.DataFrame(rows, columns=columns)
        cursor.execute('select @_sp_Atma_Partner_Get_3')
        sp_out_message = cursor.fetchone()
        return {"DATA": df_sales, "MESSAGE": sp_out_message[0]}

    def query_summary(self):
        cursor = connection.cursor()
        parameters = (self.Action, self.jsonData, self.json_classification, '')

        cursor.callproc('sp_Atma_Query_Get', parameters)
        columns = [x[0] for x in cursor.description]
        rows = cursor.fetchall()
        rows = list(rows)
        df_sales = pd.DataFrame(rows, columns=columns)
        cursor.execute('select @_sp_Atma_Query_Get_3')
        sp_out_message = cursor.fetchone()
        return {"DATA": df_sales, "MESSAGE": sp_out_message[0]}

    def History_Get(self):
        cursor = connection.cursor()
        parameters = (self.Action, self.jsonData, self.json_classification, '')
        cursor.callproc('sp_Atma_History_Get', parameters)
        columns = [x[0] for x in cursor.description]
        rows = cursor.fetchall()
        rows = list(rows)
        df_sales = pd.DataFrame(rows, columns=columns)
        cursor.execute('select @_sp_Atma_History_Get_3')
        sp_out_message = cursor.fetchone()
        return {"DATA": df_sales, "MESSAGE": sp_out_message[0]}

    def atmadirector_summary(self):
        cursor = connection.cursor()
        parameters = (self.Action, self.jsonData, self.json_classification, '')
        cursor.callproc('sp_Atma_Directors_Get', parameters)
        columns = [x[0] for x in cursor.description]
        rows = cursor.fetchall()
        rows = list(rows)
        df_sales = pd.DataFrame(rows, columns=columns)
        cursor.execute('select @_sp_Atma_Directors_Get_3')
        sp_out_message = cursor.fetchone()
        return {"DATA": df_sales, "MESSAGE": sp_out_message[0]}

    def Set_Header(self):
        cursor = connection.cursor()
        Parameters = (self.action, self.jsonData, self.dataw, '')
        cursor.callproc('sp_Atma_Partner_Set', Parameters)
        cursor.execute('select @_sp_Atma_Partner_Set_3')
        df_header = cursor.fetchone()
        return df_header
    def Set_movetorm(self):
        cursor = connection.cursor()
        Parameters = (self.action, self.jsonData, self.dataw, '')
        cursor.callproc('sp_Atma_Draft_To_Pending_Set', Parameters)
        cursor.execute('select @_sp_Atma_Draft_To_Pending_Set_3')
        df_header = cursor.fetchone()
        return df_header

    def Set_newAPI_atma_frm_memo(self):
        cursor = connection.cursor()
        Parameters = (self.action, self.jsonData, self.dataw, '')
        cursor.callproc('sp_New_Atma_Data_Set', Parameters)
        cursor.execute('select @_sp_New_Atma_Data_Set_3')
        df_header = cursor.fetchone()
        return df_header

    def change_request_page(self):
        cursor = connection.cursor()
        Parameters = (self.action, self.jsonData, self.dataw, '')
        cursor.callproc('sp_Atma_Master_View_And_Cancle', Parameters)
        cursor.execute('select @_sp_Atma_Master_View_And_Cancle_3')
        df_header = cursor.fetchone()
        return df_header


    def Set_Activitydetails(self):
        cursor = connection.cursor()
        Parameters = (self.action, self.jsonData, self.dataw, '')
        cursor.callproc('sp_Atma_Activitydetails_Set', Parameters)
        cursor.execute('select @_sp_Atma_Activitydetails_Set_3')
        df_header = cursor.fetchone()
        return df_header[0]

    def update_activitydetails(self):
        cursor = connection.cursor()
        Parameters = (self.action, self.jsonData, self.dataw, '')
        cursor.callproc('sp_Atma_Activitydetails_Set', Parameters)
        cursor.execute('select @_sp_Atma_Activitydetails_Set_3')
        df_header = cursor.fetchone()
        return df_header

    def atma_Activitydetails_Get(self):
        cursor = connection.cursor()
        parameters = (self.type, self.jsonData, self.json_classification, '')
        cursor.callproc('sp_Atma_Activitydetails_Get', parameters)
        columns = [x[0] for x in cursor.description]
        rows = cursor.fetchall()
        cursor.execute('select @_sp_Atma_Activitydetails_Get_3')
        outmsg_sp = cursor.fetchone()
        rows = list(rows)
        df_sales = pd.DataFrame(rows, columns=columns)
        return {"DATA": df_sales, "MESSAGE": outmsg_sp[0]}

    def set_paymode(self):
        cursor = connection.cursor()
        Parameters = (self.action, self.jsonData, self.dataw, '')
        cursor.callproc('sp_Atma_payment_Set', Parameters)
        cursor.execute('select @_sp_Atma_payment_Set_3')
        df_header = cursor.fetchone()
        return df_header

    def update_paymode(self):
        cursor = connection.cursor()
        Parameters = (self.action, self.jsonData, self.dataw, '')
        cursor.callproc('sp_Atma_payment_Set', Parameters)
        cursor.execute('select @_sp_Atma_payment_Set_3')
        df_header = cursor.fetchone()
        return df_header

    def bankbranch_module(self):
        cursor = connection.cursor()
        all_data = (self.type, self.finaldata, self.emptyjson, '')
        cursor.callproc('sp_Atma_payment_Get', all_data)
        columns = [x[0] for x in cursor.description]
        rows = cursor.fetchall()
        rows = list(rows)
        df_courier = pd.DataFrame(rows, columns=columns)
        return df_courier

    def atma_paymentsummary(self):
        cursor = connection.cursor()
        parameters = (self.action, self.jsonData, self.cls, '')
        cursor.callproc('sp_Atma_payment_Get', parameters)
        columns = [x[0] for x in cursor.description]
        rows = cursor.fetchall()
        rows = list(rows)
        df_sales = pd.DataFrame(rows, columns=columns)
        cursor.execute('select @_sp_Atma_payment_Get_3')
        sp_out_message = cursor.fetchone()
        return {"DATA": df_sales, "MESSAGE": sp_out_message[0]}

    def get_AttachmentSummary_model(self):
        cursor = connection.cursor()
        parameters = (self.type, self.jsonData, self.json_classification, '')
        cursor.callproc('sp_Atma_Document_Get', parameters)
        columns = [x[0] for x in cursor.description]
        rows = cursor.fetchall()
        cursor.execute('select @_sp_Atma_Document_Get_3')
        outmsg_sp = cursor.fetchone()
        rows = list(rows)
        df_sales = pd.DataFrame(rows, columns=columns)
        return {"DATA": df_sales, "MESSAGE": outmsg_sp[0]}

    def Set_Docgroup(self):
        cursor = connection.cursor()
        Parameters = (self.action, self.jsonData, '')
        cursor.callproc('sp_Atma_Document_Set', Parameters)
        cursor.execute('select @_sp_Atma_Document_Set_2')
        df_header = cursor.fetchone()
        return df_header[0]

    def atmaupdateattachment(self):
        cursor = connection.cursor()
        Parameters = (self.Action, self.filterjson1, '')
        cursor.callproc('sp_Atma_Document_Set', Parameters)
        cursor.execute('select @_sp_Atma_Document_Set_2')
        df_header = cursor.fetchone()
        return df_header

    def gettaxdetails(self):
        cursor = connection.cursor()
        parameters = (self.Action, self.emptyjsonone, self.emptyjsontwo, '')
        cursor.callproc('sp_Atma_TaxType_Get', parameters)
        columns = [x[0] for x in cursor.description]
        rows = cursor.fetchall()
        rows = list(rows)
        df_sales = pd.DataFrame(rows, columns=columns)
        cursor.execute('select @_sp_Atma_TaxType_Get_3')
        sp_out_message = cursor.fetchone()
        return {"DATA": df_sales, "MESSAGE": sp_out_message[0]}

    def set_taxdetailsdata(self):
        cursor = connection.cursor()
        Parameters = (self.Action, self.clsjson2, self.clsjson3, '')
        cursor.callproc('sp_Atma_Tax_Details_Set', Parameters)
        cursor.execute('select @_sp_Atma_Tax_Details_Set_3')
        df_header = cursor.fetchone()
        return df_header

    def update_taxdetailsdata(self):
        cursor = connection.cursor()
        Parameters = (self.Action, self.clsjson2, self.clsjson3, '')
        cursor.callproc('sp_Atma_Tax_Details_Set', Parameters)
        cursor.execute('select @_sp_Atma_Tax_Details_Set_3')
        df_header = cursor.fetchone()
        return df_header

    def get_taxsummary(self):
        cursor = connection.cursor()
        parameters = (self.Action, self.jsonData, self.cls, '')
        cursor.callproc('sp_Atma_Tax_Details_Get', parameters)
        columns = [x[0] for x in cursor.description]
        rows = cursor.fetchall()
        rows = list(rows)
        df_sales = pd.DataFrame(rows, columns=columns)
        cursor.execute('select @_sp_Atma_Tax_Details_Get_3')
        sp_out_message = cursor.fetchone()
        return {"DATA": df_sales, "MESSAGE": sp_out_message[0]}

    def atmaget_ProductCatSubCat(self):
        cursor = connection.cursor()
        parameters = (self.type, self.jsonData, self.json_classification, '')
        cursor.callproc('sp_APCatSubCat_Get', parameters)
        columns = [x[0] for x in cursor.description]
        rows = cursor.fetchall()
        cursor.execute('select @_sp_APCatSubCat_Get_3')
        outmsg_sp = cursor.fetchone()
        rows = list(rows)
        df_sales = pd.DataFrame(rows, columns=columns)
        return {"DATA": df_sales, "MESSAGE": outmsg_sp[0]}

    def atmaget_activity(self):
        cursor = connection.cursor()
        parameters = (self.type, self.jsonData, self.json_classification, '')
        cursor.callproc('sp_Atma_Activity_Get', parameters)
        columns = [x[0] for x in cursor.description]
        rows = cursor.fetchall()
        cursor.execute('select @_sp_Atma_Activity_Get_3')
        outmsg_sp = cursor.fetchone()
        rows = list(rows)
        df_sales = pd.DataFrame(rows, columns=columns)
        return {"DATA": df_sales, "MESSAGE": outmsg_sp[0]}

    def atma_activityadd(self):
        cursor = connection.cursor()
        Parameters = (self.action, self.jsonData, self.dataw, '')
        cursor.callproc('sp_Atma_Activity_Set', Parameters)
        cursor.execute('select @_sp_Atma_Activity_Set_3')
        df_header = cursor.fetchone()
        return df_header[0]

    def update_Actgroup(self):
        cursor = connection.cursor()
        Parameters = (self.action, self.jsonData, self.dataw, '')
        cursor.callproc('sp_Atma_Activity_Set', Parameters)
        cursor.execute('select @_sp_Atma_Activity_Set_3')
        df_header = cursor.fetchone()
        return df_header[0]

    def Set_clientgroup(self):
        cursor = connection.cursor()
        Parameters = (self.action, self.jsonData, self.dataw, '')
        cursor.callproc('sp_Atma_Partnerclient_Set', Parameters)
        cursor.execute('select @_sp_Atma_Partnerclient_Set_3')
        df_header = cursor.fetchone()
        return df_header[0]

    def get_clientgroup(self):
        cursor = connection.cursor()
        parameters = (self.action, self.jsonData, self.json_classification, '')
        cursor.callproc('sp_Atma_Partnerclient_Get', parameters)
        columns = [x[0] for x in cursor.description]
        rows = cursor.fetchall()
        rows = list(rows)
        df_sales = pd.DataFrame(rows, columns=columns)
        cursor.execute('select @_sp_Atma_Partnerclient_Get_3')
        sp_out_message = cursor.fetchone()
        return {"DATA": df_sales, "MESSAGE": sp_out_message[0]}

    def update_clientdetails(self):
        cursor = connection.cursor()
        Parameters = (self.action, self.jsonData, self.dataw, '')
        cursor.callproc('sp_Atma_Partnerclient_Set', Parameters)
        cursor.execute('select @_sp_Atma_Partnerclient_Set_3')
        df_header = cursor.fetchone()
        return df_header

    def Set_contractgroup(self):
        cursor = connection.cursor()
        Parameters = (self.action, self.jsonData, self.dataw, '')
        cursor.callproc('sp_Atma_Partnercontractor_Set', Parameters)
        cursor.execute('select @_sp_Atma_Partnercontractor_Set_3')
        df_header = cursor.fetchone()
        return df_header

    def get_contractgroup(self):
        cursor = connection.cursor()
        parameters = (self.action, self.jsonData, self.json_classification, '')
        cursor.callproc('sp_Atma_Partnercontractor_Get', parameters)
        columns = [x[0] for x in cursor.description]
        rows = cursor.fetchall()
        rows = list(rows)
        df_sales = pd.DataFrame(rows, columns=columns)
        cursor.execute('select @_sp_Atma_Partnercontractor_Get_3')
        sp_out_message = cursor.fetchone()
        return {"DATA": df_sales, "MESSAGE": sp_out_message[0]}

    def update_contractdetails(self):
        cursor = connection.cursor()
        Parameters = (self.action, self.jsonData, self.dataw, '')
        cursor.callproc('sp_Atma_Partnercontractor_Set', Parameters)
        cursor.execute('select @_sp_Atma_Partnercontractor_Set_3')
        df_header = cursor.fetchone()
        return df_header

    def Set_branchgroup(self):
        cursor = connection.cursor()
        Parameters = (self.action, self.jsonData, self.dataw, '')
        cursor.callproc('sp_Atma_PartnerBranch_Set', Parameters)
        cursor.execute('select @_sp_Atma_PartnerBranch_Set_3')
        df_header = cursor.fetchone()
        return df_header

    def get_branchgroup(self):
        cursor = connection.cursor()
        parameters = (self.action, self.jsonData, self.json_classification, '')
        cursor.callproc('sp_Atma_PartnerBranch_Get', parameters)
        columns = [x[0] for x in cursor.description]
        rows = cursor.fetchall()
        rows = list(rows)
        df_sales = pd.DataFrame(rows, columns=columns)
        cursor.execute('select @_sp_Atma_PartnerBranch_Get_3')
        sp_out_message = cursor.fetchone()
        return {"DATA": df_sales, "MESSAGE": sp_out_message[0]}

    def update_branchdetails(self):
        cursor = connection.cursor()
        Parameters = (self.action, self.jsonData, self.dataw, '')
        cursor.callproc('sp_Atma_PartnerBranch_Set', Parameters)
        cursor.execute('select @_sp_Atma_PartnerBranch_Set_3')
        df_header = cursor.fetchone()
        return df_header

    def Set_basicprofilegroup(self):
        cursor = connection.cursor()
        Parameters = (self.action, self.jsonData, self.dataw, '')
        cursor.callproc('sp_Atma_Partnerprofile_Set', Parameters)
        cursor.execute('select @_sp_Atma_Partnerprofile_Set_3')
        df_header = cursor.fetchone()
        return df_header

    def get_basicprofiledetailsgroup(self):
        cursor = connection.cursor()
        parameters = (self.action, self.jsonData, self.json_classification, '')
        cursor.callproc('sp_Atma_Partnerprofile_Get', parameters)
        columns = [x[0] for x in cursor.description]
        rows = cursor.fetchall()
        rows = list(rows)
        df_sales = pd.DataFrame(rows, columns=columns)
        cursor.execute('select @_sp_Atma_Partnerprofile_Get_3')
        sp_out_message = cursor.fetchone()
        return {"DATA": df_sales, "MESSAGE": sp_out_message[0]}

    def get_checker_detailsgroup(self):
        cursor = connection.cursor()
        parameters = (self.action, self.jsonData, self.json_classification, '')
        cursor.callproc('sp_Atma_PartnerProduct_Checker_Get', parameters)
        columns = [x[0] for x in cursor.description]
        rows = cursor.fetchall()
        rows = list(rows)
        df_sales = pd.DataFrame(rows, columns=columns)
        cursor.execute('select @_sp_Atma_PartnerProduct_Checker_Get_3')
        sp_out_message = cursor.fetchone()
        return {"DATA": df_sales, "MESSAGE": sp_out_message[0]}

    def update_productstatusdetails(self):
        cursor = connection.cursor()
        Parameters = (self.action, self.jsonData, self.dataw, '')
        cursor.callproc('sp_Atma_PartnerProduct_Checker_Set', Parameters)
        cursor.execute('select @_sp_Atma_PartnerProduct_Checker_Set_3')
        df_header = cursor.fetchone()
        return df_header

    def Set_Prmaker(self):
        cursor = connection.cursor()
        Parameters = (self.action, self.jsonData, self.dataw, '')
        cursor.callproc('sp_Atma_partnerproduct_Map_Set', Parameters)
        cursor.execute('select @_sp_Atma_partnerproduct_Map_Set_3')
        df_header = cursor.fetchone()
        return df_header[0]

    def get_prmaker(self):
        cursor = connection.cursor()
        parameters = (self.type, self.jsonData, self.json_classification, '')
        cursor.callproc('sp_Atma_partnerproduct_Map_Get', parameters)
        columns = [x[0] for x in cursor.description]
        rows = cursor.fetchall()
        cursor.execute('select @_sp_Atma_partnerproduct_Map_Get_3')
        outmsg_sp = cursor.fetchone()
        rows = list(rows)
        df_sales = pd.DataFrame(rows, columns=columns)
        return {"DATA": df_sales, "MESSAGE": outmsg_sp[0]}
    def catalog_getproduct(self):
        cursor = connection.cursor()
        parameters = (self.type, self.jsonData, self.json_classification, '')
        cursor.callproc('sp_Atma_partnerproduct_Map_Get', parameters)
        columns = [x[0] for x in cursor.description]
        rows = cursor.fetchall()
        cursor.execute('select @_sp_Atma_partnerproduct_Map_Get_3')
        outmsg_sp = cursor.fetchone()
        rows = list(rows)
        df_sales = pd.DataFrame(rows, columns=columns)
        return {"DATA": df_sales, "MESSAGE": outmsg_sp[0]}

    def get_profileProduct(self):
        cursor = connection.cursor()
        parameters = (self.type, self.jsonData, self.json_classification, '')
        cursor.callproc('sp_Atma_PartnerProduct_Get', parameters)
        columns = [x[0] for x in cursor.description]
        rows = cursor.fetchall()
        cursor.execute('select @_sp_Atma_PartnerProduct_Get_3')
        outmsg_sp = cursor.fetchone()
        rows = list(rows)
        df_sales = pd.DataFrame(rows, columns=columns)
        return {"DATA": df_sales, "MESSAGE": outmsg_sp[0]}

    def Set_Partnerproduct(self):
        cursor = connection.cursor()
        Parameters = (self.action, self.jsonData, self.dataw, '')
        cursor.callproc('sp_Atma_PartnerProduct_Set', Parameters)
        cursor.execute('select @_sp_Atma_PartnerProduct_Set_3')
        df_header = cursor.fetchone()
        return df_header[0]

    def Set_Partnerdeactivate(self):
        cursor = connection.cursor()
        Parameters = (self.action, self.jsonData, self.dataw, '')
        cursor.callproc('sp_Atma_Partner_Deactivate_Set', Parameters)
        cursor.execute('select @_sp_Atma_Partner_Deactivate_Set_3')
        df_header = cursor.fetchone()
        return df_header[0]

    def update_aproval_stagesdetails(self):
        cursor = connection.cursor()
        Parameters = (self.action, self.jsonData, self.dataw, '')
        cursor.callproc('sp_Atma_Draft_To_Pending_Set', Parameters)
        cursor.execute('select @_sp_Atma_Draft_To_Pending_Set_3')
        df_header = cursor.fetchone()
        return df_header

    def update_headaproval_stagesdetails(self):
        cursor = connection.cursor()
        Parameters = (self.action, self.jsonData, self.dataw, '')
        cursor.callproc('sp_Atma_Pending_To_Approval_Set', Parameters)
        cursor.execute('select @_sp_Atma_Pending_To_Approval_Set_3')
        df_header = cursor.fetchone()
        return df_header

    def get_partapproval(self):
        cursor = connection.cursor()
        parameters = (self.type, self.jsonData, self.json_classification, '')
        cursor.callproc('sp_Atma_Partner_Get', parameters)
        columns = [x[0] for x in cursor.description]
        rows = cursor.fetchall()
        cursor.execute('select @_sp_Atma_Partner_Get_3')
        outmsg_sp = cursor.fetchone()
        rows = list(rows)
        df_sales = pd.DataFrame(rows, columns=columns)
        return {"DATA": df_sales, "MESSAGE": outmsg_sp[0]}

    def get_partdisapproval(self):
        cursor = connection.cursor()
        parameters = (self.type, self.jsonData, self.json_classification, '')
        cursor.callproc('sp_Atma_Partner_Get', parameters)
        columns = [x[0] for x in cursor.description]
        rows = cursor.fetchall()
        cursor.execute('select @_sp_Atma_Partner_Get_3')
        outmsg_sp = cursor.fetchone()
        rows = list(rows)
        df_sales = pd.DataFrame(rows, columns=columns)
        return {"DATA": df_sales, "MESSAGE": outmsg_sp[0]}

    def get_approvalpartner(self):
        cursor = connection.cursor()
        parameters = (self.type, self.json_classification, self.jsonData, '')
        cursor.callproc('sp_Atma_Partner_Get', parameters)
        columns = [x[0] for x in cursor.description]
        rows = cursor.fetchall()
        cursor.execute('select @_sp_Atma_Partner_Get_3')
        outmsg_sp = cursor.fetchone()
        rows = list(rows)
        df_sales = pd.DataFrame(rows, columns=columns)
        return {"DATA": df_sales, "MESSAGE": outmsg_sp[0]}

    def updateapprovalrequest(self):
        cursor = connection.cursor()
        Parameters = (self.action, self.jsonData, self.dataw, '')
        cursor.callproc('sp_Atma_Partner_Deactivate_Set', Parameters)
        cursor.execute('select @_sp_Atma_Partner_Deactivate_Set_3')
        df_header = cursor.fetchone()
        return df_header

    def view_aproval_change(self):
        cursor = connection.cursor()
        Parameters = (self.action, self.jsonData, self.dataw, '')
        cursor.callproc('sp_Atma_Master_View_And_Cancle', Parameters)
        cursor.execute('select @_sp_Atma_Master_View_And_Cancle_3')
        df_header = cursor.fetchone()
        return df_header

    def activation_request(self):
        cursor = connection.cursor()
        Parameters = (self.action, self.jsonData, self.dataw, '')
        cursor.callproc('sp_Atma_Approval_To_Draft_Set', Parameters)
        cursor.execute('select @_sp_Atma_Approval_To_Draft_Set_3')
        df_header = cursor.fetchone()
        return df_header
    def setbankbranch(self):
        cursor = connection.cursor()
        Parameters = (self.action, self.type, self.subtype,self.filter_json,self.json_classification,self.create_by, '')
        cursor.callproc('sp_BankBranch_Process_Set', Parameters)
        cursor.execute('select @_sp_BankBranch_Process_Set_6')
        df_header = cursor.fetchone()
        return df_header
    def updatebankbranch(self):
        cursor = connection.cursor()
        Parameters = (self.action, self.type, self.subtype,self.filter_json,self.json_classification,self.create_by, '')
        cursor.callproc('sp_BankBranch_Process_Set', Parameters)
        cursor.execute('select @_sp_BankBranch_Process_Set_6')
        df_header = cursor.fetchone()
        return df_header
    def updatebranchmaster(self):
        cursor = connection.cursor()
        Parameters = (self.action, self.type, self.subtype,self.filter_json,self.json_classification,self.create_by, '')
        cursor.callproc('sp_Branch_Mst_Set', Parameters)
        cursor.execute('select @_sp_Branch_Mst_Set_6')
        df_header = cursor.fetchone()
        return df_header

    def activebankbranch(self):
        cursor = connection.cursor()
        Parameters = (self.action, self.type, self.subtype,self.filter_json,self.json_classification,self.create_by, '')
        cursor.callproc('sp_BankBranch_Process_Set', Parameters)
        cursor.execute('select @_sp_BankBranch_Process_Set_6')
        df_header = cursor.fetchone()
        return df_header

    def get_bankbranchdtl(self):
        cursor = connection.cursor()
        parameters = (self.action,self.type,self.jsonData,self.json_classification, '')
        cursor.callproc('sp_BankBranch_Process_Get', parameters)
        columns = [x[0] for x in cursor.description]
        rows = cursor.fetchall()
        cursor.execute('select @_sp_BankBranch_Process_Get_4')
        outmsg_sp = cursor.fetchone()
        rows = list(rows)
        df_sales = pd.DataFrame(rows, columns=columns)
        return {"DATA": df_sales, "MESSAGE": outmsg_sp[0]}
    def get_masterbranchdtl(self):
        cursor = connection.cursor()
        parameters = (self.action,self.type,self.jsonData,self.json_classification, '')
        cursor.callproc('sp_Branch_Mst_Get', parameters)
        columns = [x[0] for x in cursor.description]
        rows = cursor.fetchall()
        cursor.execute('select @_sp_Branch_Mst_Get_4')
        outmsg_sp = cursor.fetchone()
        rows = list(rows)
        df_sales = pd.DataFrame(rows, columns=columns)
        return {"DATA": df_sales, "MESSAGE": outmsg_sp[0]}