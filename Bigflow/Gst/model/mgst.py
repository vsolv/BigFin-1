from django.db import connection
import pandas as pd
from Bigflow.Master.Model import mVariable
import json

class Gst_model(mVariable.variable):


    def set_gst(self):
        cursor = connection.cursor()
        parameters = (self.action, self.sub_type,
                        json.dumps(self.filter_json),
                        '{"Entity_Gid":['+str(self.entity_gid) +']}',self.employee_gid,'')
        cursor.callproc('sp_Gstrecon_Set',parameters)
        cursor.execute('select @_sp_Gstrecon_Set_5')
        df_cltn = cursor.fetchone()
        return df_cltn



    def get_gstsummary(self):
        cursor = connection.cursor()
        parameters = (self.type, self.sub_type,
                        self.filter_json,
                        '{"Entity_Gid":['+str(self.entity_gid) +']}',self.employee_gid,'')
        cursor.callproc('sp_Gstrecon_Get',parameters)
        columns = [x[0] for x in cursor.description]
        rows = cursor.fetchall()
        rows = list(rows)
        service_out = pd.DataFrame(rows,columns=columns)
        return service_out
