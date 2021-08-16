import json

from django.db import connection
import pandas as pd
from Bigflow.Master.Model import mVariable


class Claim_model(mVariable.variable):

    def get_claim_summary(self):
        cursor = connection.cursor()
        parameters = (self.type, self.sub_type, self.jsonData, self.json_classification, '')
        cursor.callproc('sp_ClaimProcess_Get', parameters)
        columns = [x[0] for x in cursor.description]
        rows = cursor.fetchall()
        cursor.execute('select @_sp_ClaimProcess_Get_4')
        outmsg_sp = cursor.fetchone()
        rows = list(rows)
        df_ta = pd.DataFrame(rows, columns=columns)
        if self.type == 'Summary_Details' and self.sub_type == 'Details':
            df_ta['Daywise_Amt'] = df_ta['Daywise_Amt'].apply(json.loads)
            df_ta['split_amt'] = df_ta['split_amt'].apply(json.loads)
            df_ta['totaltype_amount'] = df_ta['totaltype_amount'].apply(json.loads)
            return {"DATA": df_ta, "MESSAGE": outmsg_sp[0]}
        return {"DATA": df_ta, "MESSAGE": outmsg_sp[0]}

    def set_claim(self):
        cursor = connection.cursor()
        parameters = (self.action,self.type,self.sub_type,self.jsonData,self.jsondata,self.json_file,self.jsondata,
                      self.json_classification,self.employee_gid,'')
        cursor.callproc('sp_ClaimProcess_Set', parameters)
        cursor.execute('select @_sp_ClaimProcess_Set_9')
        sp_out_message = cursor.fetchone()
        return {"MESSAGE": sp_out_message[0]}
