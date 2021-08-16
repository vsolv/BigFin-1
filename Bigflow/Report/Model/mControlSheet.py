from django.db import connection
import pandas as pd
import json
from Bigflow.Master.Model import mVariable

class CtrlModel(mVariable.variable):

    def set_ctrl_dump(self):
        cursor = connection.cursor()
        parameters = (self.action,self.type,self.sub_type,self.jsonData,self.jsondata,
                      self.json_classification,self.create_by,'')
        cursor.callproc('sp_ControlSheetProcess_Set',parameters)

        if cursor.description != None:
            colums = [x[0] for x in cursor.description]
            rows = cursor.fetchall()
            rows = list(rows)
            df_ctrl_set = pd.DataFrame(rows,columns=colums)
            cursor.execute('select @_sp_ControlSheetProcess_Set_7')
            sp_out_msg = cursor.fetchone()
            return {"MESSAGE":"PROCESS_DATA","DATA":df_ctrl_set}
        else:
            cursor.execute('select @_sp_ControlSheetProcess_Set_7')
            sp_out_msg = cursor.fetchone()
            return {"MESSAGE": sp_out_msg[0], "DATA": "NO_DATA"}

    def get_ctrl_summary(self):
        cursor = connection.cursor()
        parameters = (self.group,self.type, self.sub_type, self.jsonData,
                      self.json_classification,self.create_by, '')
        cursor.callproc('sp_ControlSheetProcess_Get', parameters)
        columns = [x[0] for x in cursor.description]
        rows = cursor.fetchall()
        rows = list(rows)
        df_ctrl = pd.DataFrame(rows, columns=columns)
        cursor.execute('select @_sp_ControlSheetProcess_Get_6')
        sp_out_message = cursor.fetchone()
        if self.group == 'INITIAL_SUMMARY':
            df_ctrl['lj_data'] = df_ctrl['lj_data'].apply(json.loads)
            return {"DATA": df_ctrl, "MESSAGE": sp_out_message[0]}
        return {"DATA": df_ctrl, "MESSAGE": sp_out_message[0]}