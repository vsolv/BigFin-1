from django.db import connection
import pandas as pd
from Bigflow.Master.Model import mVariable
import json

class Proofing_model(mVariable.variable):

    def Get_Mainentry(self):
        cursor = connection.cursor()
        parameters = (self.Type,self.sub_type,self.filter_json,self.json_classification,'')
        cursor.callproc('sp_IntegrityProcess_Get', parameters)
        columns = [x[0] for x in cursor.description]
        rows = cursor.fetchall()
        rows = list(rows)
        df_producttypeddl = pd.DataFrame(rows, columns=columns)
        return df_producttypeddl

    def set_integrity_upload(self):
        cursor = connection.cursor()
        lj_bank_stmt = json.dumps(self.jsonData)
        lj_file = json.dumps(self.jsondata)
        parameters = (self.action,self.type,lj_bank_stmt,lj_file,self.json_classification,self.create_by,'')
        cursor.callproc('sp_IntegrityProcess_Set',parameters)
        cursor.execute('select @_sp_IntegrityProcess_Set_6')
        out_message = cursor.fetchone()
        return out_message[0]