from django.db import connection
import pandas as pd
from Bigflow.Master.Model import mVariable
import json

class Memo_model(mVariable.variable):

    def Set_MemoRequest(self):
        cursor = connection.cursor()
        Parameters = (self.action, self.type,self.SubType,self.jsonData, self.status,self.Entity_Gid,self.Create_By1, '')
        cursor.callproc('sp_Memo_Process_Set', Parameters)
        cursor.execute('select @_sp_Memo_Process_Set_7')
        df_header = cursor.fetchone()
        return df_header
    def update_MemoRequest(self):
        cursor = connection.cursor()
        Parameters = (self.action, self.type,self.SubType,self.jsonData, self.status,self.Entity_Gid,self.Create_By1, '')
        cursor.callproc('sp_Memo_Process_Set', Parameters)
        cursor.execute('select @_sp_Memo_Process_Set_7')
        df_header = cursor.fetchone()
        return df_header

    def Get_MemoReqeust(self):
        cursor = connection.cursor()
        all_data = (self.action, self.type, self.dataw, self.Entity_Gid, '')
        cursor.callproc('sp_Memo_Process_Get', all_data)
        columns = [x[0] for x in cursor.description]
        rows = cursor.fetchall()
        rows = list(rows)
        df_sales = pd.DataFrame(rows, columns=columns)
        cursor.execute('select @_sp_Memo_Process_Get_4')
        sp_out_message = cursor.fetchone()
        return {"DATA": df_sales, "MESSAGE": sp_out_message[0]}

    def Get_Memotransation(self):
        cursor = connection.cursor()
        all_data = (self.action, self.type, self.dataw, self.Entity_Gid, '')
        cursor.callproc('sp_Memo_Process_Get', all_data)
        columns = [x[0] for x in cursor.description]
        rows = cursor.fetchall()
        rows = list(rows)
        df_sales = pd.DataFrame(rows, columns=columns)
        cursor.execute('select @_sp_Memo_Process_Get_4')
        sp_out_message = cursor.fetchone()
        return {"DATA": df_sales, "MESSAGE": sp_out_message[0]}

    def Set_MemoApproval(self):
        cursor = connection.cursor()
        Parameters = (self.action, self.type, self.SubType, self.jsonData, self.status, self.Entity_Gid, self.Create_By1, '')
        cursor.callproc('sp_Memo_Process_Set', Parameters)
        cursor.execute('select @_sp_Memo_Process_Set_7')
        df_header = cursor.fetchone()
        return df_header
    def Update_Isactive(self):
        cursor = connection.cursor()
        Parameters = (self.Action, self.Type, self.SubType, self.Filter, self.AddJson, self.Classification, self.Update_By, '')
        cursor.callproc('sp_Memo_Process_Set', Parameters)
        cursor.execute('select @_sp_Memo_Process_Set_7')
        df_header = cursor.fetchone()
        return df_header
    def Update_transaction(self):
        cursor = connection.cursor()
        Parameters = (self.Action, self.Type, self.SubType, self.Filter, self.AddJson, self.Classification, self.Update_By, '')
        cursor.callproc('sp_Memo_Process_Set', Parameters)
        cursor.execute('select @_sp_Memo_Process_Set_7')
        df_header = cursor.fetchone()
        return df_header

    def Category_Set(self):
        cursor = connection.cursor()
        Parameters = (
        self.Action, self.Type, self.SubType, self.Filter, self.AddJson, self.Classification, self.Update_By, '')
        cursor.callproc('sp_Memo_Mst_Process_Set', Parameters)
        cursor.execute('select @_sp_Memo_Mst_Process_Set_7')
        df_header = cursor.fetchone()
        return df_header
    def SubCategory_Set(self):
        cursor = connection.cursor()
        Parameters = (
        self.Action, self.Type, self.SubType, self.Filter, self.AddJson, self.Classification, self.Update_By, '')
        cursor.callproc('sp_Memo_Mst_Process_Set', Parameters)
        cursor.execute('select @_sp_Memo_Mst_Process_Set_7')
        df_header = cursor.fetchone()
        return df_header
    def updateCategory_Set(self):
        cursor = connection.cursor()
        Parameters = (
        self.Action, self.Type, self.SubType, self.Filter, self.AddJson, self.Classification, self.Update_By, '')
        cursor.callproc('sp_Memo_Mst_Process_Set', Parameters)
        cursor.execute('select @_sp_Memo_Mst_Process_Set_7')
        df_header = cursor.fetchone()
        return df_header
    def updatesubCategory_Set(self):
        cursor = connection.cursor()
        Parameters = (
        self.Action, self.Type, self.SubType, self.Filter, self.AddJson, self.Classification, self.Update_By, '')
        cursor.callproc('sp_Memo_Mst_Process_Set', Parameters)
        cursor.execute('select @_sp_Memo_Mst_Process_Set_7')
        df_header = cursor.fetchone()
        return df_header

    def Get_Category(self):
        cursor = connection.cursor()
        all_data = (self.action, self.type, self.dataw, self.Entity_Gid, '')
        cursor.callproc('sp_Memo_Mst_Process_Get', all_data)
        columns = [x[0] for x in cursor.description]
        rows = cursor.fetchall()
        rows = list(rows)
        df_sales = pd.DataFrame(rows, columns=columns)
        cursor.execute('select @_sp_Memo_Mst_Process_Get_4')
        sp_out_message = cursor.fetchone()
        return {"DATA": df_sales, "MESSAGE": sp_out_message[0]}
    def Get_SubCategory(self):
        cursor = connection.cursor()
        all_data = (self.action, self.type, self.dataw, self.Entity_Gid, '')
        cursor.callproc('sp_Memo_Mst_Process_Get', all_data)
        columns = [x[0] for x in cursor.description]
        rows = cursor.fetchall()
        rows = list(rows)
        df_sales = pd.DataFrame(rows, columns=columns)
        cursor.execute('select @_sp_Memo_Mst_Process_Get_4')
        sp_out_message = cursor.fetchone()
        return {"DATA": df_sales, "MESSAGE": sp_out_message[0]}
    def Updatecategory_Isactive(self):
        cursor = connection.cursor()
        Parameters = (self.Action, self.Type, self.SubType, self.Filter, self.AddJson, self.Classification, self.Update_By, '')
        cursor.callproc('sp_Memo_Mst_Process_Set', Parameters)
        cursor.execute('select @_sp_Memo_Mst_Process_Set_7')
        df_header = cursor.fetchone()
        return df_header
    def Updatesubcategory_Isactive(self):
        cursor = connection.cursor()
        Parameters = (self.Action, self.Type, self.SubType, self.Filter, self.AddJson, self.Classification, self.Update_By, '')
        cursor.callproc('sp_Memo_Mst_Process_Set', Parameters)
        cursor.execute('select @_sp_Memo_Mst_Process_Set_7')
        df_header = cursor.fetchone()
        return df_header