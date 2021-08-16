from django.db import connection
import pandas as pd
from Bigflow.Master.Model import mVariable

class MasterSyncData(mVariable.variable):

    def masterSync_data(self):
        cursor = connection.cursor()
        parameters = ( self.type,self.action, self.main, '')
        print(parameters)
        cursor.callproc('sp_MasterSync_Get', parameters)
        columns = [x[0] for x in cursor.description]
        rows = cursor.fetchall()
        cursor.execute('select @_sp_MasterSync_Get_3')
        outmsg_sp = cursor.fetchone()
        rows = list(rows)
        message = pd.DataFrame(rows, columns=columns)
        return {"DATA": message, "MESSAGE": outmsg_sp[0]}

    def masterSync_employee_data(self):
        cursor = connection.cursor()
        parameters = ( self.type,self.action, self.main, '')
        print(parameters)
        cursor.callproc('sp_EmployeeSync_Get', parameters)
        columns = [x[0] for x in cursor.description]
        rows = cursor.fetchall()
        cursor.execute('select @_sp_EmployeeSync_Get_3')
        outmsg_sp = cursor.fetchone()
        rows = list(rows)
        message = pd.DataFrame(rows, columns=columns)
        return {"DATA": message, "MESSAGE": outmsg_sp[0]}

    def masterSync_branch_data(self):
        cursor = connection.cursor()
        parameters = ( self.type,self.action, self.main, '')
        print(parameters)
        cursor.callproc('Sp_Branchsync_Get', parameters)
        columns = [x[0] for x in cursor.description]
        rows = cursor.fetchall()
        cursor.execute('select @_Sp_Branchsync_Get_3')
        outmsg_sp = cursor.fetchone()
        rows = list(rows)
        message = pd.DataFrame(rows, columns=columns)
        return {"DATA": message, "MESSAGE": outmsg_sp[0]}


    def masterSync_gl_data(self):
        cursor = connection.cursor()
        parameters = ( self.type,self.action, self.main, '')
        print(parameters)
        cursor.callproc('sp_Glsync_Get', parameters)
        columns = [x[0] for x in cursor.description]
        rows = cursor.fetchall()
        cursor.execute('select @_sp_Glsync_Get_3')
        outmsg_sp = cursor.fetchone()
        rows = list(rows)
        message = pd.DataFrame(rows, columns=columns)
        return {"DATA": message, "MESSAGE": outmsg_sp[0]}