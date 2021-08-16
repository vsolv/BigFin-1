from django.db import connection
import pandas as pd
from Bigflow.Master.Model import mVariable

class PurchaseModel(mVariable.variable):

    def get_prpo_query(self):
        cursor = connection.cursor()
        parameters = (self.type, self.sub_type, self.filter_json, self.json_classification, '')
        cursor.callproc('sp_PRPO_Query_Get', parameters)
        columns = [x[0] for x in cursor.description]
        rows = cursor.fetchall()
        cursor.execute('select @_sp_PRPO_Query_Get_4')
        outmsg_sp = cursor.fetchone()
        rows = list(rows)
        df_fa = pd.DataFrame(rows, columns=columns)
        return {"DATA": df_fa, "MESSAGE": outmsg_sp[0]}



