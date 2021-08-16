from django.db import connection
import pandas as pd
from Bigflow.Master.Model import mVariable
import json

class ERMA_model(mVariable.variable):
    def ermaarchivalset(self):
        cursor = connection.cursor()
        Parameters = (self.action, self.jsonData, self.dataw, '')
        cursor.callproc('sp_Atma_activitydtlpproduct_Set', Parameters)
        cursor.execute('select @_sp_Atma_activitydtlpproduct_Set_3')
        df_header = cursor.fetchone()
        return df_header[0]

    def Set_ArchivalRequest(self):
        cursor = connection.cursor()
        Parameters = (self.action,self.type,self.sub_type, self.jsonData, '{}',self.dataw,self.classification,self.create_by, '')
        cursor.callproc('sp_Erma_Process_Set', Parameters)
        cursor.execute('select @_sp_Erma_Process_Set_8')
        df_header = cursor.fetchone()
        return df_header[0]


    def ermaproductget(self):
        cursor = connection.cursor()
        parameters = (self.action, self.jsonData,self.json_classification,'')
        cursor.callproc('sp_erma_product_get', parameters)
        columns = [x[0] for x in cursor.description]
        rows = cursor.fetchall()
        rows = list(rows)
        df_product = pd.DataFrame(rows, columns=columns)
        cursor.execute('select @_sp_erma_product_get_3')
        outmsg_sp = cursor.fetchone()
        return df_product

    def erma_getbarcode(self):
        cursor = connection.cursor()
        self.type="BARCODE"
        self.sub_type="GET"
        parameters = (self.type,self.sub_type, self.jsonData, self.json_classification, '')
        cursor.callproc('sp_Erma_Process_Get', parameters)
        cursor.execute('select @_sp_Erma_Process_Get_4')
        outmsg_sp = cursor.fetchone()
        return { "MESSAGE": outmsg_sp[0]}

    def Get_barcode(self):
        cursor = connection.cursor()
        all_data = (self.action, self.type, self.filter, self.classification, '')
        cursor.callproc('sp_Erma_Process_Get', all_data)
        columns = [x[0] for x in cursor.description]
        rows = cursor.fetchall()
        rows = list(rows)
        df_sales = pd.DataFrame(rows, columns=columns)
        cursor.execute('select @_sp_Erma_Process_Get_4')
        sp_out_message = cursor.fetchone()

        return {"DATA": df_sales, "MESSAGE": sp_out_message[0]}

    def Set_barcoderequest(self):
        cursor = connection.cursor()
        Parameters = (self.action, self.type, self.subtype, self.Filter, self.Status, self.Changes, self.Classification,
                      self.create_id1, '')
        cursor.callproc('sp_Erma_Process_Set', Parameters)
        cursor.execute('select @_sp_Erma_Process_Set_8')
        df_header = cursor.fetchone()
        return df_header

