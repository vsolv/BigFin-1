from django.db import connection
import pandas as pd
from Bigflow.Master.Model import mVariable
import json

class MEP_model(mVariable.variable):

    def Set_PAR_PARDET(self):
        cursor = connection.cursor()
        Parameters = (self.action, self.create_id1,self.par_json,self.a, self.dataw, '')
        cursor.callproc('sp_Par_Set', Parameters)
        cursor.execute('select @_sp_Par_Set_5')
        df_header = cursor.fetchone()
        return df_header
    def Get_PAR_PARDET(self):
        cursor = connection.cursor()
        all_data = (self.action, self.create_id1, self.dataw,self.Entity_Gid, '')
        cursor.callproc('sp_Par_Get', all_data)
        columns = [x[0] for x in cursor.description]
        rows = cursor.fetchall()
        rows = list(rows)
        df_sales = pd.DataFrame(rows, columns=columns)
        cursor.execute('select @_sp_Par_Get_4')
        sp_out_message = cursor.fetchone()
        return {"DATA": df_sales, "MESSAGE": sp_out_message[0]}

    def Set_MEP_PARDET(self):
        cursor = connection.cursor()
        Parameters = (self.action, self.create_id1,self.par_json,self.pardet_json, self.dataw, '')
        cursor.callproc('sp_Mep_Set', Parameters)
        cursor.execute('select @_sp_Mep_Set_5')
        df_header = cursor.fetchone()
        return df_header

    def Get_MEP_PARDET(self):
        cursor = connection.cursor()
        all_data = (self.action, self.create_id1, self.dataw, self.Entity_Gid, '')
        cursor.callproc('sp_Mep_Get', all_data)
        columns = [x[0] for x in cursor.description]
        rows = cursor.fetchall()
        rows = list(rows)
        df_sales = pd.DataFrame(rows, columns=columns)
        cursor.execute('select @_sp_Mep_Get_4')
        sp_out_message = cursor.fetchone()
        return {"DATA": df_sales, "MESSAGE": sp_out_message[0]}