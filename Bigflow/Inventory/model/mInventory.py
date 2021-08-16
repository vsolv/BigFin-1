from django.db import connection
import pandas as pd
from Bigflow.Master.Model import mVariable
import json

class Invertory_model(mVariable.variable):

    def get_stockdetails(self):
        cursor = connection.cursor()
        parameters = (self.action,self.type,self.jsondata,
                      self.from_date,self.to_date,self.product_gid,self.supplier_gid,self.entity_gid, '')
        cursor.callproc('sp_Stock_Get', parameters)
        columns = [x[0] for x in cursor.description]
        rows = cursor.fetchall()
        cursor.execute('select @_sp_Stock_Get_9')
        out_put = cursor.fetchone()
        rows = list(rows)
        df_preschedule = pd.DataFrame(rows, columns=columns)
        return df_preschedule

    def set_stockdetails(self):
        cursor = connection.cursor()
        self.jsonData=json.dumps(self.jsonData)
        parameters = (self.action, self.type,  self.jsonData, self.jsondata, self.create_by, self.entity_gid, '')
        cursor.callproc('sp_Stock_Set', parameters)
        cursor.execute('select @_sp_Stock_Set_6')
        output_msg = cursor.fetchone()
        return output_msg

    def set_recepit(self):
        cursor = connection.cursor()
        self.jsonData=json.dumps(self.jsonData)
        self.jsonData_sec = json.dumps(self.jsonData_sec)
        self.jsondata = json.dumps(self.jsondata)
        parameters = (self.action,self.jsonData, self.jsonData_sec,self.jsondata, self.entity_gid, self.create_by, '')
        cursor.callproc('sp_Return_Set', parameters)
        cursor.execute('select @_sp_Return_Set_6')
        output_msg = cursor.fetchone()
        return output_msg

    def get_receipt(self):
        cursor = connection.cursor()
        parameters = (self.action,self.customer_gid,self.supplier_gid,
                      self.receipt_gid,self.receiptdetails_gid,self.status,self.entity_gid, '')
        cursor.callproc('sp_Return_Get', parameters)
        columns = [x[0] for x in cursor.description]
        rows = cursor.fetchall()
        cursor.execute('select @_sp_Return_Get_7')
        out_put = cursor.fetchone()
        rows = list(rows)
        df_preschedule = pd.DataFrame(rows, columns=columns)
        return df_preschedule


    def get_sales_fav_product(self):
        cursor = connection.cursor()
        parameters = (self.customer_gid, self.product_type, self.entity_gid, '')
        cursor.callproc('sp_SalesFavProdt_Get', parameters)
        columns = [x[0] for x in cursor.description]
        rows = cursor.fetchall()
        rows = list(rows)
        df_sales_fav_pdct = pd.DataFrame(rows, columns=columns)
        dd = df_sales_fav_pdct.loc[df_sales_fav_pdct['fav'] == 'Y']
        return dd

    def set_stockconvert(self):
        cursor = connection.cursor()
        self.jsonheader = json.dumps(self.jsonheader)
        self.jsondetails = json.dumps(self.jsondetails)
        parameters = (self.action,'', self.jsonheader,self.jsondetails,'{}','{}', self.create_by, self.entity_gid, '')
        cursor.callproc('sp_Conversion_Set', parameters)
        cursor.execute('select @_sp_Conversion_Set_8')
        output_msg = cursor.fetchone()
        return output_msg

    def get_conversion(self):
        cursor = connection.cursor()
        parameters = (self.action,self.customer_gid,self.supplier_gid,
                      self.receipt_gid,self.receiptdetails_gid,self.status,self.entity_gid, '')
        cursor.callproc('sp_Conversion_Get', parameters)
        columns = [x[0] for x in cursor.description]
        rows = cursor.fetchall()
        cursor.execute('select @_sp_Conversion_Get_7')
        out_put = cursor.fetchone()
        rows = list(rows)
        df_preschedule = pd.DataFrame(rows, columns=columns)
        return df_preschedule
