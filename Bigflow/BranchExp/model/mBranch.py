from django.db import connection
import pandas as pd
import json
from Bigflow.Transaction.Model import mFET

class BranchExp_model(mFET.FET_model):
    def print_parameters(sp_name, parameters):
        pass

    def get_expensedetails(self):
        cursor = connection.cursor()
        parameters = (self.type, self.sub_type, self.jsonData, self.json_classification, '')

        BranchExp_model.print_parameters("sp_APExpense_Get", parameters);
        cursor.callproc('sp_APExpense_Get', parameters)
        columns = [x[0] for x in cursor.description]
        rows = cursor.fetchall()
        rows = list(rows)
        df_dp = pd.DataFrame(rows, columns=columns)
        cursor.execute('select @_sp_APExpense_Get_4')
        sp_out_message = cursor.fetchone()
        return {"DATA": df_dp, "MESSAGE": sp_out_message[0]}

    def get_expense_data(self):
        cursor = connection.cursor()
        Parameters = (self.type, self.sub_type, self.filter,self.classification,'')

        BranchExp_model.print_parameters("sp_APExpense_Get",Parameters);

        cursor.callproc('sp_APExpense_Get', Parameters)
        columns = [d[0] for d in cursor.description]
        rows = cursor.fetchall()
        rows = list(rows)
        ldict1 = pd.DataFrame(rows, columns=columns)
        return ldict1

    def set_expensedetails(self):
        cursor = connection.cursor()
        parameters = (self.action, self.type, self.jsonData,'Y', self.json_classification,1, '')

        BranchExp_model.print_parameters("sp_APExpense_Set", parameters);

        cursor.callproc('sp_APExpense_Set', parameters)
        cursor.execute('select @_sp_APExpense_Set_6')
        sp_out_message = cursor.fetchone()
        return { "MESSAGE": sp_out_message[0]}

    def property_set(self):
        cursor=connection.cursor()
        parameters=(self.type,self.sub_type,self.filters,self.classification,'')
        # cursor.callproc('sp_ap_property_Set',parameters)
        cursor.callproc('sp_APProperty_Set', parameters)

        BranchExp_model.print_parameters("sp_APProperty_Set", parameters);

        cursor.execute('select @_sp_APProperty_Set_4')
        msg = cursor.fetchone()
        return {"MESSAGE":msg[0]}

    def get_alltablevalue(self):
        cursor = connection.cursor()
        Parameters = (self.type,self.table_values,self.entity_gid,'')

        BranchExp_model.print_parameters("sp_AllTableValues_Get", Parameters);

        cursor.callproc('sp_AllTableValues_Get', Parameters)
        columns = [x[0] for x in cursor.description]
        rows = cursor.fetchall()
        rows = list(rows)
        pro_type = pd.DataFrame(rows, columns=columns)
        return pro_type

    def get_pro_details(self):
        cursor=connection.cursor()
        Parameters=(self.Type,self.Sub_Type,self.filter,self.classification,'')

        BranchExp_model.print_parameters("sp_APProperty_Get", Parameters);

        cursor.callproc('sp_APProperty_Get', Parameters)
        columns = [x[0] for x in cursor.description]
        rows = cursor.fetchall()
        rows = list(rows)
        pro_det = pd.DataFrame(rows, columns=columns)
        return pro_det

    def premises_set(self):
        cursor=connection.cursor()
        parameters=(self.action,self.type,self.filter,self.classification,'')
        BranchExp_model.print_parameters("sp_BranchExp_Process_Set", parameters);
        cursor.callproc('sp_BranchExp_Process_Set', parameters)
        cursor.execute('select @_sp_BranchExp_Process_Set_4')
        msg = cursor.fetchone()
        return {"MESSAGE":msg[0]}

    def premises_get(self):
        cursor=connection.cursor()
        Parameters=(self.action,self.type,self.filter,self.classification,'')
        BranchExp_model.print_parameters("sp_BranchExp_Process_Get", Parameters);
        cursor.callproc('sp_BranchExp_Process_Get', Parameters)
        columns = [x[0] for x in cursor.description]
        rows = cursor.fetchall()
        rows = list(rows)
        pro_det = pd.DataFrame(rows, columns=columns)
        return pro_det
