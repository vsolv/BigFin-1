from django.db import connection
import pandas as pd
import json
from Bigflow.Transaction.Model import mFET


from django import forms
from django.db import models

class inward_model(mFET.FET_model):


    def set_inward(self):
        cursor = connection.cursor()
        jsondata = self.inwardheader_json
        jsondatadetl=self.inwarddetail_json
        header_json = json.dumps(jsondata)
        detail_json = json.dumps(jsondatadetl)
        parameters = (self.action,self.type,header_json,detail_json,self.employee_gid,self.entity_gid,'')
        cursor.callproc('sp_InwardOffice_Set',parameters)
        cursor.execute('select @_sp_InwardOffice_Set_6')
        output_msg = cursor.fetchone()
        return output_msg

    def get_inward(self):
        cursor = connection.cursor()
        jsondata = self.inwardheader_json
        header_json = json.dumps(jsondata)
        parameters = (self.action, self.type, header_json,self.entity_gid,'')
        cursor.callproc('sp_InwardOffice_Process_Get', parameters)
        columns = [x[0] for x in cursor.description]
        rows = cursor.fetchall()
        rows = list(rows)
        df_inward = pd.DataFrame(rows, columns=columns)
        return df_inward

    def get_inward_details(self):
        cursor = connection.cursor()
        jsondata = self.inwardheader_json
        header_json = json.dumps(jsondata)
        parameters = (self.action, self.type, header_json,self.entity_gid,'')
        cursor.callproc('sp_InwardOffice_Get', parameters)
        columns = [x[0] for x in cursor.description]
        rows = cursor.fetchall()
        rows = list(rows)
        df_inward = pd.DataFrame(rows, columns=columns)
        return df_inward



    def get_courier(self):
        cursor = connection.cursor()
        parameters = (self.courier_gid,self.courier_name,self.entity_gid)
        cursor.callproc('sp_Courier_Get',parameters)
        columns = [x[0] for x in cursor.description]
        rows = cursor.fetchall()
        rows = list(rows)
        df_customerddl = pd.DataFrame(rows, columns=columns)
        return df_customerddl