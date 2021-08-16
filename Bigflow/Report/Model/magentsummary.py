from django.db import connection
import pandas as pd
from Bigflow.Master.Model import mVariable
class control(mVariable.variable):
    def Agentsummary_Get(self):
        cursor = connection.cursor()
        Parameters = (self.action, self.type, self.main, self.enty, '')
        cursor.callproc('sp_Agentsummary_Get', Parameters)
        columns = [x[0] for x in cursor.description]
        rows = cursor.fetchall()
        rows = list(rows)
        df_customer = pd.DataFrame(rows, columns=columns)
        return {"DATA": df_customer, "MESSAGE": "FOUND"}

    def sp_PPR_Data_Get_frm_gen_Bussiness(self):
        cursor = connection.cursor()
        Parameters = (self.action, self.jsonData, self.dataw, '')
        cursor.callproc('sp_PPR_Data_Get', Parameters)
        columns = [x[0] for x in cursor.description]
        rows = cursor.fetchall()
        cursor.execute('select @_sp_PPR_Data_Get_3')
        outmsg_sp = cursor.fetchone()
        rows = list(rows)
        df_sales = pd.DataFrame(rows, columns=columns).to_dict(orient='records')
        return {"DATA": df_sales, "MESSAGE": outmsg_sp[0]}

    def sp_AllTableValues_Get_frm_gen(self):
        cursor = connection.cursor()
        Parameters = ('', self.jsonData, self.entity_gid, '')
        cursor.callproc('sp_AllTableValues_Get', Parameters)
        columns = [x[0] for x in cursor.description]
        rows = cursor.fetchall()
        cursor.execute('select @_sp_AllTableValues_Get_3')
        outmsg_sp = cursor.fetchone()
        rows = list(rows)
        df_sales = pd.DataFrame(rows, columns=columns).to_dict(orient='records')
        return {"DATA": df_sales, "MESSAGE": outmsg_sp[0]}

    def sp_PPR_Data_Get_frm_gen(self):
        cursor = connection.cursor()
        Parameters = (self.action, self.jsonData, self.dataw, '')
        cursor.callproc('sp_PPR_Data_Get', Parameters)
        columns = [x[0] for x in cursor.description]
        rows = cursor.fetchall()
        cursor.execute('select @_sp_PPR_Data_Get_3')
        outmsg_sp = cursor.fetchone()
        rows = list(rows)
        df_sales = pd.DataFrame(rows, columns=columns).to_dict(orient='records')
        return {"DATA": df_sales, "MESSAGE": outmsg_sp[0]}

