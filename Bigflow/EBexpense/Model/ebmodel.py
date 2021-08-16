from django.db import connection
import pandas as pd
from Bigflow.Master.Model import mVariable
import json



class Eb_model(mVariable.variable):


    def set_ebmasterdata(self):
        cursor = connection.cursor()
        parameters = (self.action, self.jsonData,self.classification, '')
        cursor.callproc('sp_EBconsumer_Set', parameters)
        cursor.execute('select @_sp_EBconsumer_Set_3')
        output_msg = cursor.fetchone()
        return output_msg


    def payment_ebmaster(self):
        cursor = connection.cursor()
        parameters = (self.action, self.jsonData,self.classification, '')
        cursor.callproc('sp_EBbill_Set', parameters)
        cursor.execute('select @_sp_EBbill_Set_3')
        output_msg = cursor.fetchone()
        return output_msg


    def get_eb_summary(self):
        cursor = connection.cursor()
        parameters = (self.action, self.jsonData,self.classification, '')
        cursor.callproc('Sp_EBconsumer_Get', parameters)
        columns = [x[0] for x in cursor.description]
        rows = cursor.fetchall()
        cursor.execute('select @_Sp_EBconsumer_Get_3')
        out_put = cursor.fetchone()
        rows = list(rows)
        df_empup = pd.DataFrame(rows, columns=columns)
        return df_empup



    def get_table_datareport(self):
        cursor = connection.cursor()
        parameters = (self.action, self.jsonData,self.jsondata,self.jsonData_sec, self.classification, '')
        cursor.callproc('Sp_Overall_Report_Get', parameters)
        columns = [x[0] for x in cursor.description]
        rows = cursor.fetchall()
        cursor.execute('select @_Sp_Overall_Report_Get_5')
        out_put = cursor.fetchone()
        rows = list(rows)
        df_empup = pd.DataFrame(rows, columns=columns)
        return df_empup

    def set_table_report(self):
        cursor = connection.cursor()
        parameters = (self.action, self.jsonData, self.jsondata, self.jsonData_sec, self.classification, '')
        cursor.callproc('Sp_Overall_Report_Set', parameters)
        cursor.execute('select @_Sp_Overall_Report_Set_5')
        output_msg = cursor.fetchone()
        return output_msg