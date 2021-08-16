from django.db import connection
from Bigflow.Master.Model import mVariable
import pandas as pd
import json
import Bigflow

class BOM(mVariable.variable):

    def get_compnt(self):
        cursor = connection.cursor()
        Parameters = (self.group,self.type,self.jsonData,self.entity_gid,'')
        cursor.callproc('sp_BOMComponent_Get', Parameters)
        columns = [x[0] for x in cursor.description]
        rows = cursor.fetchall()
        rows = list(rows)
        df_courier = pd.DataFrame(rows, columns=columns)
        return df_courier


    def set_comp(self):
        cursor = connection.cursor()
        parameters = (self.action, self.type, self.jsonData,
                      self.entity_gid,self.create_by,'')
        cursor.callproc('sp_BOMComponent_Set',parameters)
        cursor.execute('select @_sp_BOMComponent_Set_5')
        output_msg = cursor.fetchone()
        return output_msg
    # rttt  saa
    #d