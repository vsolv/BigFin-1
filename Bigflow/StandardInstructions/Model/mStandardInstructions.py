from django.db import connection
import pandas as pd
from Bigflow.Master.Model import mVariable
import json


class StandardInstuctions(mVariable.variable):
    def print_parameters(sp_name, parameters):
        print("set @message=0;")
        print("call galley.",sp_name, parameters,";")
        print("select @message;")

    def set_SI(self):
        cursor = connection.cursor()
        parameters = (self.action, self.type, self.filter, self.classification, self.create_by, '')

        p = (self.action, self.type, self.filter, self.classification,self.create_by,"@message")
        StandardInstuctions.print_parameters("sp_APSIprocess_Set", p);

        cursor.callproc('sp_APSIprocess_Set', parameters)
        cursor.execute('select @_sp_APSIprocess_Set_5')
        sp_out_message = cursor.fetchall()
        return {"MESSAGE": sp_out_message[0]}

    def get_SI(self):
        cursor = connection.cursor()
        parameters = (self.action, self.type, self.filter, self.classification, '')

        p = (self.action, self.type, self.filter, self.classification, "@message")
        StandardInstuctions.print_parameters("sp_APSIprocess_Get", p);

        cursor.callproc('sp_APSIprocess_Get', parameters)
        columns = [x[0] for x in cursor.description]
        rows = cursor.fetchall()
        cursor.execute('select @_sp_APSIprocess_Get_4')
        outmsg_sp = cursor.fetchone()
        rows = list(rows)
        si_data = pd.DataFrame(rows, columns=columns)
        return si_data




