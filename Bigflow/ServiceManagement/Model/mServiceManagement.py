from django.db import connection
import pandas as pd
from Bigflow.Master.Model import mVariable
import json


class ServiceManagement(mVariable.variable):
    def print_parameters(sp_name, parameters):
        message_tuple = ("@message",)
        listx = list(parameters)
        # listx.remove("")
        listx.pop()
        tuplex = tuple(listx)
        parameters3 = tuplex + message_tuple
        print("set @message=0;")
        print("call galley." + sp_name, parameters3, end="")
        print(";")
        print("select @message;")

    def get_supplier_data(self):
        cursor = connection.cursor()
        parameters = (self.type, self.sub_type, self.filter, self.classification, '')

        ServiceManagement.print_parameters("sp_SupplierDetails_Get", parameters);

        cursor.callproc('sp_SupplierDetails_Get', parameters)
        columns = [x[0] for x in cursor.description]
        rows = cursor.fetchall()
        cursor.execute('select @_sp_SupplierDetails_Get_4')
        outmsg_sp = cursor.fetchone()
        rows = list(rows)
        data = pd.DataFrame(rows, columns=columns)
        return data

    def get_branch_name(self):
        cursor = connection.cursor()
        parameters = (self.type, self.sub_type, self.filter,self.classification, '')

        ServiceManagement.print_parameters("sp_Classification_Get", parameters);

        cursor.callproc('sp_Classification_Get', parameters)
        columns = [x[0] for x in cursor.description]
        rows = cursor.fetchall()
        cursor.execute('select @_sp_Classification_Get_4')
        outmsg_sp = cursor.fetchone()
        rows = list(rows)
        branch_data = pd.DataFrame(rows, columns=columns)
        return branch_data


    def get_all_data(self):
        cursor = connection.cursor()
        parameters = (self.type, self.sub_type, self.filter,self.classification, '')

        ServiceManagement.print_parameters("sp_SVSProcess_Get", parameters);

        cursor.callproc('sp_SVSProcess_Get', parameters)
        columns = [x[0] for x in cursor.description]
        rows = cursor.fetchall()
        cursor.execute('select @_sp_SVSProcess_Get_4')
        outmsg_sp = cursor.fetchone()
        rows = list(rows)
        branch_data = pd.DataFrame(rows, columns=columns)
        return branch_data


    def create_ticket(self):
        cursor = connection.cursor()
        parameters = (self.action, self.type, self.filter,self.classification,self.create_by, '')

        ServiceManagement.print_parameters("sp_SVSProcess_Set", parameters);

        cursor.callproc('sp_SVSProcess_Set', parameters)
        cursor.execute('select @_sp_SVSProcess_Set_5')
        sp_out_message = cursor.fetchall()
        return {"MESSAGE": sp_out_message[0]}

    def create_amc(self):
        cursor = connection.cursor()
        parameters = (self.action, self.type, self.filter, self.classification, self.create_by, '')

        ServiceManagement.print_parameters("sp_SVSamc_Set", parameters);

        cursor.callproc('sp_SVSamc_Set', parameters)
        cursor.execute('select @_sp_SVSamc_Set_5')
        sp_out_message = cursor.fetchall()
        return {"MESSAGE": sp_out_message[0]}

    def amc_Update(self):
        cursor = connection.cursor()
        parameters = (self.action, self.type, self.filter, self.classification, self.create_by, '')

        ServiceManagement.print_parameters("sp_SVSamc_Set", parameters);

        cursor.callproc('sp_SVSamc_Set', parameters)
        cursor.execute('select @_sp_SVSamc_Set_5')
        sp_out_message = cursor.fetchall()
        return {"MESSAGE": sp_out_message[0]}


    def get_amc_data(self):
        cursor = connection.cursor()
        parameters = (self.action, self.type, self.filter,self.classification, '')

        ServiceManagement.print_parameters("sp_SVSamc_get", parameters);

        cursor.callproc('sp_SVSamc_get', parameters)
        columns = [x[0] for x in cursor.description]
        rows = cursor.fetchall()
        cursor.execute('select @_sp_SVSamc_get_4')
        outmsg_sp = cursor.fetchone()
        rows = list(rows)
        amc_data = pd.DataFrame(rows, columns=columns)

        return amc_data

    def get_alltablevalue_metadata(self):
        cursor = connection.cursor()
        jsondt = self.jsonData
        # jsondata = json.dumps(jsondt)
        Parameters = (self.action, jsondt,self.entity_gid,'')
        
        ServiceManagement.print_parameters("sp_AllTableValues_Get", Parameters);
        
        cursor.callproc('sp_AllTableValues_Get', Parameters)
        columns = [d[0] for d in cursor.description]
        rows = cursor.fetchall()
        rows = list(rows)
        ldict1 = pd.DataFrame(rows, columns=columns)
        return ldict1

    def get_product_data(self):
        cursor = connection.cursor()
        parameters = (self.type, self.sub_type, self.filter, self.classification, '')
        
        ServiceManagement.print_parameters("sp_SuppProdType_Get", parameters);

        cursor.callproc('sp_SuppProdType_Get', parameters)
        columns = [x[0] for x in cursor.description]
        rows = cursor.fetchall()
        cursor.execute('select @_sp_SuppProdType_Get_4')
        outmsg_sp = cursor.fetchone()
        rows = list(rows)
        data = pd.DataFrame(rows, columns=columns)
        return data

    def get_follow_up_data(self):
        cursor = connection.cursor()
        parameters = (self.type, self.sub_type, self.filter,self.classification, '')

        ServiceManagement.print_parameters("sp_SVSFollowup_Get", parameters);

        cursor.callproc('sp_SVSFollowup_Get', parameters)
        columns = [x[0] for x in cursor.description]
        rows = cursor.fetchall()
        cursor.execute('select @_sp_SVSFollowup_Get_4')
        outmsg_sp = cursor.fetchone()
        rows = list(rows)
        followup_data = pd.DataFrame(rows, columns=columns)
        followupdetail = followup_data['followupdetail'][0]
        trackdetails=followup_data['trackdetails'][0]
        asset_name=followup_data['asset_name'][0]
        if(followupdetail!=None):
            followup_data['followupdetail']=followup_data['followupdetail'].apply(json.loads)
        if(trackdetails!=None):
            followup_data['trackdetails']=followup_data['trackdetails'].apply(json.loads)
        if(asset_name!=None):
            followup_data['asset_name']=followup_data['asset_name'].apply(json.loads)
        return followup_data

    def get_emp_data(self):
        cursor = connection.cursor()
        Parameters = (self.table_name, self.gid, self.name,self.entity_gid,'')
        
        ServiceManagement.print_parameters("sp_Dropdown_Common_Get", Parameters);

        cursor.callproc('sp_Dropdown_Common_Get', Parameters)
        columns = [d[0] for d in cursor.description]
        rows = cursor.fetchall()
        rows = list(rows)
        ldict1 = pd.DataFrame(rows, columns=columns)
        return ldict1

    def set_followup(self):
        cursor = connection.cursor()
        parameters = (self.action, self.type, self.filter, self.classification, self.create_by, '')

        ServiceManagement.print_parameters("sp_SVSFollowup_Set", parameters);

        cursor.callproc('sp_SVSFollowup_Set', parameters)
        cursor.execute('select @_sp_SVSFollowup_Set_5')
        sp_out_message = cursor.fetchall()
        return {"MESSAGE": sp_out_message[0]}

    def set_pr_detils(self):
        cursor = connection.cursor()
        parameters = (self.action, self.type, self.filter, self.classification, '{}', self.classification_json, self.create_by, '')

        ServiceManagement.print_parameters("sp_PRrequestSPS_Set", parameters);

        cursor.callproc('sp_PRrequestSPS_Set', parameters)
        cursor.execute('select @_sp_PRrequestSPS_Set_7')
        output_msg = cursor.fetchone()
        return output_msg


