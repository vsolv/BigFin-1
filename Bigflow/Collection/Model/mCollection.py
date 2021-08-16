from django.db import connection
import pandas as pd
import json
from Bigflow.Master.Model import mVariable

class Collection_model(mVariable.variable):

    def __init__(self):
        self.filter_json = {}
        self.Classification = {}

    def get_collection_inv_map(self):
        cursor = connection.cursor()
        json1 = json.dumps(self.jsonData)
        json2 = json.dumps(self.jsondata)
        parameters = (self.action,self.type,self.collectionheader_gid,self.name,self.date,json1,json2,'')
        cursor.callproc('sp_Collection_Get',parameters)
        columns = [x[0] for x in cursor.description]
        rows = cursor.fetchall()
        rows = list(rows)
        df_cltn = pd.DataFrame(rows,columns=columns)
        return df_cltn

    def get_lastbounce_collection(self):
        cursor = connection.cursor()
        # json1 = json.dumps(self.jsonData)
        # json2 = json.dumps(self.jsondata)
        parameters = (
        self.action, self.type, self.collectionheader_gid, self.name, self.date, self.filter_json, self.jsondata, '')
        cursor.callproc('sp_Collection_Get', parameters)
        columns = [x[0] for x in cursor.description]
        rows = cursor.fetchall()
        rows = list(rows)
        df_cltn = pd.DataFrame(rows, columns=columns)
        return df_cltn

    def get_vgfcollection(self):
        cursor = connection.cursor()
        # json1 = json.dumps(self.jsonData)
        # json2 = json.dumps(self.jsondata)
        parameters = (self.Action, self.Type, self.collectionheader_gid, self.name, self.date, self.filter_json, self.jsondata, '')
        cursor.callproc('sp_Collection_Get', parameters)
        columns = [x[0] for x in cursor.description]
        rows = cursor.fetchall()
        rows = list(rows)
        df_cltn = pd.DataFrame(rows, columns=columns)
        return df_cltn

    def get_collection(self):
        cursor = connection.cursor()
        json1 = json.dumps(self.jsonData)
        # json2 = json.dumps(self.jsondata)
        parameters = (self.action, self.type, self.collectionheader_gid, self.name, self.date, json1, self.jsondata, '')
        cursor.callproc('sp_Collection_Get', parameters)
        columns = [x[0] for x in cursor.description]
        rows = cursor.fetchall()
        rows = list(rows)
        df_cltn = pd.DataFrame(rows, columns=columns)
        return df_cltn

    def get_cutoff(self):
        cursor = connection.cursor()
        parameters = (self.action, self.type, self.collectionheader_gid, self.name, self.date, self.jsonData, self.json_classification, '')
        cursor.callproc('sp_Collection_Get', parameters)
        columns = [x[0] for x in cursor.description]
        rows = cursor.fetchall()
        rows = list(rows)
        df_cutoffs = pd.DataFrame(rows, columns=columns)
        return df_cutoffs


        # columns = [x[0] for x in cursor.description]
        # rows = cursor.fetchall()
        # cursor.execute('select @_sp_Collection_Get_8')
        # out_put = cursor.fetchone()
        # rows = list(rows)
        # df_cutoffs = pd.DataFrame(rows, columns=columns)
        # return df_cutoffs


    def set_invreceipt_map(self):
        cursor =connection.cursor()
        jsondata=json.dumps(self.jsonData)
        classification=json.dumps(self.json_classification)
        parameters=(self.action,self.type,jsondata,self.commit,self.create_by,classification,'')
        cursor.callproc('sp_InvoiceReceiptMap_Set', parameters)
        cursor.execute('select @_sp_InvoiceReceiptMap_Set_6')
        df_cltn = cursor.fetchone()
        return df_cltn

    def get_receipt_ar(self):
        cursor = connection.cursor()
        jsondata = json.dumps(self.jsonData)
        classification = json.dumps(self.json_classification)
        parameters = (self.type, self.sub_type, jsondata, classification, '')
        cursor.callproc('sp_Receipt_Get', parameters)
        columns = [x[0] for x in cursor.description]
        rows = cursor.fetchall()
        rows = list(rows)
        df_receipt = pd.DataFrame(rows, columns=columns)
        return df_receipt

    def set_bank_upload(self):
        cursor = connection.cursor()
        lj_bank_stmt = json.dumps(self.jsonData)
        lj_classification = json.dumps(self.json_classification)
        lj_file = json.dumps(self.jsondata)
        parameters = (self.action,self.type,lj_bank_stmt,lj_file,lj_classification,self.create_by,'')
        cursor.callproc('sp_BankUpload_Set',parameters)
        cursor.execute('select @_sp_BankUpload_Set_6')
        out_message = cursor.fetchone()
        return out_message

    def get_cutoff(self):
        cursor = connection.cursor()
        Parameters = (self.action, self.type, self.collectionheader_gid, self.name,self.date, self.jsonData, self.json_classification,'')
        cursor.callproc('sp_Collection_Get', Parameters)
        columns = [x[0] for x in cursor.description]
        rows = cursor.fetchall()
        rows = list(rows)
        df_cutoffs = pd.DataFrame(rows, columns=columns)
        return df_cutoffs

    def get_bank_upload(self):
        cursor = connection.cursor()
        lj_data = json.dumps(self.jsonData)
        lj_classification = json.dumps(self.json_classification)
        parameters = (self.type, self.sub_type, lj_data, lj_classification, '')
        cursor.callproc('sp_BankUpload_Get', parameters)
        columns = [x[0] for x in cursor.description]
        rows = cursor.fetchall()
        rows = list(rows)
        df_bnk = pd.DataFrame(rows, columns=columns)
        return df_bnk

    def get_OutstandingCustomer(self):
        cursor = connection.cursor()
        parameters = (self.type, self.sub_type, self.filter_json, self.Classification, '')
        cursor.callproc('sp_OutstandingCustomer_Get', parameters)
        columns = [x[0] for x in cursor.description]
        rows = cursor.fetchall()
        rows = list(rows)
        output = pd.DataFrame(rows, columns=columns)
        return output

    def set_receipt_ar(self):
        cursor=connection.cursor()
        jsondata=json.dumps(self.jsonData)
        jsonclassification=json.dumps(self.json_classification)
        parameters=(self.action,self.type,jsondata,self.commit,jsonclassification,self.create_by,'','')
        cursor.callproc('sp_Receipt_Set', parameters)
        cursor.execute('select @_sp_Receipt_Set_6')
        out_message = cursor.fetchone()
        return out_message

    def set_receiptprocess_ar(self):
        cursor = connection.cursor()
        jsondata=json.dumps(self.jsonData)
        jsonclassifivation=json.dumps(self.json_classification)
        parameters=(self.action,self.type,self.sub_type,jsondata,'Y',jsonclassifivation,self.create_by,'')
        cursor.callproc('sp_ReceiptProcess_Set',parameters)
        cursor.execute('select @_sp_ReceiptProcess_Set_7')
        out_message = cursor.fetchone()
        return out_message