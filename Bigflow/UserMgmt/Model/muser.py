from django.db import connection
import pandas as pd


class user_model:
    def __init__(self):
        self.created_by=''
        self.employee_gid = 0
        self.employee_name=''
        self.role_gid=0
        self.role_code = ''
        self.role_name = 0
        self.rolegroup_gid = 1
        self.menu_gid=0
        self.entity_gid=0
        self.cluster_gid=0
        self.is_removed=''
        self.type=''
        self.json_data=''
        self.new_password = ''
        self.ismobile=''

    def get_roleGroup(self):
        cursor = connection.cursor()
        parameters = (self.employee_gid,'')
        cursor.callproc('sp_UMUservsGroup_Get', parameters)

        columns = [x[0] for x in cursor.description]
        rows = cursor.fetchall()
        cursor.execute('select @_sp_UMUservsGroup_Get_1')
        out_put = cursor.fetchone()
        rows = list(rows)
        df_rolegroup = pd.DataFrame(rows, columns=columns)
        return df_rolegroup

    def get_roleList(self):
        cursor = connection.cursor()
        parameters = (self.role_code,self.role_name,self.rolegroup_gid,self.entity_gid, '')
        cursor.callproc('sp_UMRole_Get', parameters)
        columns = [x[0] for x in cursor.description]
        rows = cursor.fetchall()
        cursor.execute('select @_sp_UMRole_Get_4')
        out_put = cursor.fetchone()
        rows = list(rows)
        df_rolelist = pd.DataFrame(rows, columns=columns)
        return df_rolelist

    def get_userList(self):
        cursor = connection.cursor()
        parameters = (self.role_gid,self.employee_gid,self.entity_gid,self.type, self.json_data,'')
        cursor.callproc('sp_UMRolevsEmployee_Get', parameters)
        columns = [x[0] for x in cursor.description]
        rows = cursor.fetchall()
        cursor.execute('select @_sp_UMRolevsEmployee_Get_5')
        out_put = cursor.fetchone()
        rows = list(rows)
        df_rolelist = pd.DataFrame(rows, columns=columns)
        return df_rolelist

    def get_menuList(self):
        cursor = connection.cursor()
        parameters = (self.role_gid,self.ismobile, '')
        cursor.callproc('sp_UMMenu_Get', parameters)
        columns = [x[0] for x in cursor.description]
        rows = cursor.fetchall()
        cursor.execute('select @_sp_UMMenu_Get_2')
        out_put = cursor.fetchone()
        rows = list(rows)
        df_menulist = pd.DataFrame(rows, columns=columns)
        return df_menulist

    def setroles(self):
        cursor = connection.cursor()
        parameters = (self.role_code,self.role_name,self.rolegroup_gid,self.entity_gid,self.created_by, '')
        cursor.callproc('sp_UMRole_Set', parameters)
        cursor.execute('select @_sp_UMRole_Set_5')
        output_msg = cursor.fetchone()
        return output_msg

    def setrolevsMenu(self):
        cursor = connection.cursor()
        parameters = (self.role_gid, self.menu_gid, 'Y', self.entity_gid, self.created_by,self.json_data, '')
        cursor.callproc('sp_UMRolevsMenu_Set', parameters)
        cursor.execute('select @_sp_UMRolevsMenu_Set_6')
        output_msg = cursor.fetchone()
        return output_msg

    def setusersvsMenu(self):
        cursor = connection.cursor()
        parameters = (self.role_gid, self.employee_gid, self.entity_gid, self.created_by,self.is_removed, '')
        cursor.callproc('sp_UMRolevsEmployee_Set', parameters)
        cursor.execute('select @_sp_UMRolevsEmployee_Set_5')
        output_msg = cursor.fetchone()
        return output_msg

    def set_roledtl(self):
        cursor = connection.cursor()
        parameters = (self.role_gid,self.ismobile, '')
        cursor.callproc('sp_UMMenu_Get', parameters)

        columns = [x[0] for x in cursor.description]
        rows = cursor.fetchall()
        cursor.execute('select @_sp_UMMenu_Get_2')
        out_put = cursor.fetchone()
        rows = list(rows)
        df_menulist = pd.DataFrame(rows, columns=columns)
        return df_menulist

    def get_employee(self):
        cursor = connection.cursor()
        temp = 'ALL'
        if(self.cluster_gid !='0'):
            temp = 'CLUSTER'
        Parameters = (self.employee_gid, self.employee_name, self.cluster_gid, temp , 'Y', self.jsonData,'')
        cursor.callproc('sp_Employee_Get', Parameters)

        columns = [x[0] for x in cursor.description]
        rows = cursor.fetchall()
        cursor.execute('select @_sp_Employee_Get_6')
        out_put = cursor.fetchone()
        rows = list(rows)
        df_employee = pd.DataFrame(rows, columns=columns)
        return df_employee

    def get_clustgroupList(self): # Not In Use
        cursor = connection.cursor()
        parameters = ('PARENT', '')
        cursor.callproc('sp_Cluster_Get', parameters)
        columns = [x[0] for x in cursor.description]
        rows = cursor.fetchall()
        cursor.execute('select @_sp_Cluster_Get_1')
        out_put = cursor.fetchone()
        rows = list(rows)
        df_menulist = pd.DataFrame(rows, columns=columns)
        return df_menulist

    # password

    def set_password(self):
        cursor = connection.cursor()
        parameters = (self.employee_gid, self.new_password, 'Y', self.employee_gid, 'Y', '')
        cursor.callproc('sp_UMPassword_Set', parameters)
        cursor.execute('select @_sp_UMPassword_Set_5')
        output_msg = cursor.fetchone()
        return output_msg

    def get_password(self):
        cursor = connection.cursor()
        parameters = (self.employee_gid, self.employee_name,'')
        cursor.callproc('sp_UMPassword_Get', parameters)
        columns = [x[0] for x in cursor.description]
        rows = cursor.fetchall()
        rows = list(rows)
        df_password = pd.DataFrame(rows, columns=columns)
        return df_password


