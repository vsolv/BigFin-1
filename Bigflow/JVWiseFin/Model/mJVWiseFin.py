from django.db import connection
import pandas as pd
from Bigflow.Master.Model import mVariable
import json


class JVWiseFin(mVariable.variable):
    def print_parameters(sp_name, parameters):
        message_tuple = ("@message",)
        listx = list(parameters)
        listx.remove("")
        tuplex = tuple(listx)
        parameters3 = tuplex + message_tuple
        print("set @message=0;")
        print("call galley." + sp_name, parameters3, end="")
        print(";")
        print("select @message;")

    def jv_wisefin_process_set_model(self):
        cursor = connection.cursor()
        parameters = (self.action, self.type, self.filter, self.classification, self.create_by, '')

        JVWiseFin.print_parameters("sp_JVProcess_Set", parameters);

        cursor.callproc('sp_JVProcess_Set', parameters)
        cursor.execute('select @_sp_JVProcess_Set_5')
        sp_out_message = cursor.fetchall()
        return {"MESSAGE": sp_out_message[0]}

    def jv_wisefin_process_get_model(self):
        cursor = connection.cursor()
        parameters = (self.action, self.type, self.filter, self.classification, '')

        JVWiseFin.print_parameters("sp_JVProcess_Get", parameters);
        if(self.type!="JV_FIND_ALL"):
            cursor.callproc('sp_JVProcess_Get', parameters)
            columns = [x[0] for x in cursor.description]
            rows = cursor.fetchall()
            cursor.execute('select @_sp_JVProcess_Get_4')
            outmsg_sp = cursor.fetchone()
            rows = list(rows)
            jv_data = pd.DataFrame(rows, columns=columns)
            return jv_data
        elif(self.type=="JV_FIND_ALL"):
            try:
                cursor.callproc('sp_JVProcess_Get', parameters)
                columns = [x[0] for x in cursor.description]
                rows = cursor.fetchall()
                cursor.execute('select @_sp_JVProcess_Get_4')
                outmsg_sp = cursor.fetchone()
                rows = list(rows)
                jv_data = pd.DataFrame(rows, columns=columns)
                my = jv_data.get("@finaldata")[0]
                item = json.loads(my)
                r = str(item).replace("'", '')
                data = json.loads(r)
                jv_data = pd.DataFrame(data)
                return jv_data
            except:
                cursor.callproc('sp_JVProcess_Get', parameters)
                cursor.execute('select @_sp_JVProcess_Get_4')
                outmsg_sp = cursor.fetchone()
                rows = list(outmsg_sp)
                jv_data = pd.DataFrame(rows)
                return jv_data

    def get_bank_details(self):
        cursor = connection.cursor()
        parameters = (self.action, self.type, self.filter, self.classification, '');

        JVWiseFin.print_parameters("sp_APProcess_Get", parameters)

        cursor.callproc('sp_APProcess_Get', parameters)
        columns = [x[0] for x in cursor.description]
        rows = cursor.fetchall()
        rows = list(rows)
        grn_dtl = pd.DataFrame(rows, columns=columns)
        return grn_dtl




