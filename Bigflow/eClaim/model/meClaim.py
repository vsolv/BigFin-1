# import self as self
from django.db import connection, models
import pandas as pd
import json

from Bigflow import eClaim
from Bigflow.Master.Model import mVariable
from django.db import connections

class eClaim_Model(mVariable.variable):
    def get_eClaim_Master(self):
        cursor = connections['eclaim_db'].cursor()
        parameters = (self.type, self.sub_type, self.filter_json, self.json_classification, '')
        cursor.callproc('sp_Claim_Mst_Get', parameters)
        if cursor.description != None:
            columns = [x[0] for x in cursor.description]
            rows = cursor.fetchall()
            cursor.execute('select @_sp_Claim_Mst_Get_4')
            outmsg_sp = cursor.fetchone()
            rows = list(rows)
            df_location = pd.DataFrame(rows, columns=columns)
            return {"DATA": df_location, "MESSAGE": outmsg_sp[0]}
        else:
            cursor.execute('select @_sp_Claim_Mst_Get_4')
            sp_out_msg = cursor.fetchone()
            return {"MESSAGE": sp_out_msg[0], "DATA": "NO_DATA"}

    def set_eClaim_Master(self):
        cursor = connections['eclaim_db'].cursor()
        parameters = (self.action,self.type,self.sub_type,self.jsondata,self.json_classification,self.employee_gid,'')
        cursor.callproc('sp_Claim_Mst_Set', parameters)
        cursor.execute('select @_sp_Claim_Mst_Set_6')
        out_message = cursor.fetchone()
        return {"MESSAGE": out_message[0]}

    def eClaim_request_get(self):
        cursor = connections['eclaim_db'].cursor()
        parameters = (self.filter_json, '')
        cursor.callproc('sp_tourrequest_Get', parameters)
        if cursor.description != None:
            columns = [x[0] for x in cursor.description]
            rows = cursor.fetchall()
            cursor.execute('select @_sp_tourrequest_Get_1')
            outmsg_sp = cursor.fetchone()
            rows = list(rows)
            df_location = pd.DataFrame(rows, columns=columns)
            return {"DATA": df_location, "MESSAGE": outmsg_sp[0]}
        else:
            cursor.execute('select @_sp_eClaimtran_Get_1')
            sp_out_msg = cursor.fetchone()
            return {"MESSAGE": sp_out_msg[0], "DATA": "NO_DATA"}

    def eClaim_advancemaker_get(self):
        cursor = connections['eclaim_db'].cursor()
        parameters = (self.filter_json, '')
        cursor.callproc('sp_advancemaker_get', parameters)
        if cursor.description != None:
            columns = [x[0] for x in cursor.description]
            rows = cursor.fetchall()
            cursor.execute('select @_sp_advancemaker_get_1')
            outmsg_sp = cursor.fetchone()
            rows = list(rows)
            df_location = pd.DataFrame(rows, columns=columns)
            return {"DATA": df_location, "MESSAGE": outmsg_sp[0]}
        else:
            cursor.execute('select @_sp_advancemaker_get_1')
            sp_out_msg = cursor.fetchone()
            return {"MESSAGE": sp_out_msg[0], "DATA": "NO_DATA"}

    def eClaim_expensemaker_get(self):
            cursor = connections['eclaim_db'].cursor()
            parameters = (self.filter_json, '')
            cursor.callproc('sp_expensemaker_get', parameters)
            if cursor.description != None:
                columns = [x[0] for x in cursor.description]
                rows = cursor.fetchall()
                cursor.execute('select @_sp_expensemaker_get_1')
                outmsg_sp = cursor.fetchone()
                rows = list(rows)
                df_location = pd.DataFrame(rows, columns=columns)
                return {"DATA": df_location, "MESSAGE": outmsg_sp[0]}
            else:
                cursor.execute('select @_sp_expensemaker_get_1')
                sp_out_msg = cursor.fetchone()
                return {"MESSAGE": sp_out_msg[0], "DATA": "NO_DATA"}

    def eClaim_tourcancel_get(self):
        cursor = connections['eclaim_db'].cursor()
        parameters = (self.filter_json, '')
        cursor.callproc('sp_tourcancel_get', parameters)
        if cursor.description != None:
            columns = [x[0] for x in cursor.description]
            rows = cursor.fetchall()
            cursor.execute('select @_sp_tourcancel_get_1')
            outmsg_sp = cursor.fetchone()
            rows = list(rows)
            df_location = pd.DataFrame(rows, columns=columns)
            return {"DATA": df_location, "MESSAGE": outmsg_sp[0]}
        else:
            cursor.execute('select @_sp_tourcancel_get_1')
            sp_out_msg = cursor.fetchone()
            return {"MESSAGE": sp_out_msg[0], "DATA": "NO_DATA"}


    def eClaim_expense_get(self):
        cursor = connections['eclaim_db'].cursor()
        cursor.execute('''select gid,code,name from claim_mst_ttourexpense where status = 1''')
        columns = [x[0] for x in cursor.description]
        rows = cursor.fetchall()
        cursor.close()
        rows = list(rows)
        df_location = pd.DataFrame(rows, columns=columns)
        return {"DATA": df_location}

    def eClaim_onbehalf_get(self):
        cursor = connections['eclaim_db'].cursor()
        parameters = (self.filter_json, '')
        cursor.callproc('sp_Onbehalfof_Employee_Get', parameters)
        if cursor.description != None:
            columns = [x[0] for x in cursor.description]
            rows = cursor.fetchall()
            cursor.execute('select @_sp_Onbehalfof_Employee_Get_1')
            outmsg_sp = cursor.fetchone()
            rows = list(rows)
            df_location = pd.DataFrame(rows, columns=columns)
            return {"DATA": df_location, "MESSAGE": outmsg_sp[0]}
        else:
            cursor.execute('select @_sp_Onbehalfof_Employee_Get_1')
            sp_out_msg = cursor.fetchone()
            return {"MESSAGE": sp_out_msg[0], "DATA": "NO_DATA"}

    def eClaim_onbehalf_set(self):
        cursor = connections['eclaim_db'].cursor()
        parameters = (self.jsondata, '')
        cursor.callproc('sp_Onbehalfof_Employee_Set', parameters)
        cursor.execute('select @_sp_Onbehalfof_Employee_Set_1')
        out_message = cursor.fetchone()
        return {"MESSAGE": out_message[0]}

    def eClaim_hierarchy_set(self):
        cursor = connection.cursor()
        parameters = (self.jsondata, '')
        cursor.callproc('sp_eClaim_emphierarchy_set', parameters)
        cursor.execute('select @_sp_eClaim_emphierarchy_set_1')
        out_message = cursor.fetchone()
        return {"MESSAGE": out_message[0]}

    def eClaim_approver_set(self):
        cursor = connections['eclaim_db'].cursor()
        parameters = (self.jsondata, '')
        cursor.callproc('sp_tourapprover_set', parameters)
        cursor.execute('select @_sp_tourapprover_set_1')
        out_message = cursor.fetchone()
        return {"MESSAGE": out_message[0]}

    def eClaim_tourapprover_get(self):
        cursor = connections['eclaim_db'].cursor()
        quot = ''
        query = 'select gid, employeegid, branchgid, tourapprove, advanceapprove, expenseapprove, status from claim_mst_tapproverlist where status = 1'
        query = quot+query+quot
        cursor.execute(query)
        columns = [x[0] for x in cursor.description]
        rows = cursor.fetchall()
        cursor.close()
        rows = list(rows)
        df_location = pd.DataFrame(rows, columns=columns)
        return {"DATA": df_location}

    def eClaim_claimedexpense_get(self):
        cursor = connections['eclaim_db'].cursor()
        parameters = (self.filter_json, '')
        cursor.callproc('sp_claimexpense_get', parameters)
        if cursor.description != None:
            columns = [x[0] for x in cursor.description]
            rows = cursor.fetchall()
            cursor.execute('select @_sp_claimexpense_get_1')
            outmsg_sp = cursor.fetchone()
            rows = list(rows)
            df_location = pd.DataFrame(rows, columns=columns)
            return {"DATA": df_location, "MESSAGE": outmsg_sp[0]}
        else:
            cursor.execute('select @_sp_claimexpense_get_1')
            sp_out_msg = cursor.fetchone()
            return {"MESSAGE": sp_out_msg[0], "DATA": "NO_DATA"}

    def eClaim_dailydiem_get(self):
        cursor = connections['eclaim_db'].cursor()
        parameters = (self.filter_json, '')
        cursor.callproc('sp_dailydiem_get', parameters)
        if cursor.description != None:
            columns = [x[0] for x in cursor.description]
            rows = cursor.fetchall()
            cursor.execute('select @_sp_dailydiem_get_1')
            outmsg_sp = cursor.fetchone()
            rows = list(rows)
            df_location = pd.DataFrame(rows, columns=columns)
            return {"DATA": df_location, "MESSAGE": outmsg_sp[0]}
        else:
            cursor.execute('select @_sp_dailydiem_get_1')
            sp_out_msg = cursor.fetchone()
            return {"MESSAGE": sp_out_msg[0], "DATA": "NO_DATA"}

    def eClaim_lodging_get(self):
        cursor = connections['eclaim_db'].cursor()
        parameters = (self.filter_json, '')
        cursor.callproc('sp_Lodging_get', parameters)
        if cursor.description != None:
            columns = [x[0] for x in cursor.description]
            rows = cursor.fetchall()
            cursor.execute('select @_sp_Lodging_get_1')
            outmsg_sp = cursor.fetchone()
            rows = list(rows)
            df_location = pd.DataFrame(rows, columns=columns)
            return {"DATA": df_location, "MESSAGE": outmsg_sp[0]}
        else:
            cursor.execute('select @_sp_Lodging_get_1')
            sp_out_msg = cursor.fetchone()
            return {"MESSAGE": sp_out_msg[0], "DATA": "NO_DATA"}
    def eClaim_loccon_get(self):
        cursor = connections['eclaim_db'].cursor()
        parameters = (self.filter_json, '')
        cursor.callproc('sp_Localconveyence_get', parameters)
        if cursor.description != None:
            columns = [x[0] for x in cursor.description]
            rows = cursor.fetchall()
            cursor.execute('select @_sp_Localconveyence_get_1')
            outmsg_sp = cursor.fetchone()
            rows = list(rows)
            df_location = pd.DataFrame(rows, columns=columns)
            return {"DATA": df_location, "MESSAGE": outmsg_sp[0]}
        else:
            cursor.execute('select @_sp_Localconveyence_get_1')
            sp_out_msg = cursor.fetchone()
            return {"MESSAGE": sp_out_msg[0], "DATA": "NO_DATA"}

    def eClaim_miscellaneous_get(self):
        cursor = connections['eclaim_db'].cursor()
        parameters = (self.filter_json, '')
        cursor.callproc('sp_Misc_get', parameters)
        if cursor.description != None:
            columns = [x[0] for x in cursor.description]
            rows = cursor.fetchall()
            cursor.execute('select @_sp_Misc_get_1')
            outmsg_sp = cursor.fetchone()
            rows = list(rows)
            df_location = pd.DataFrame(rows, columns=columns)
            return {"DATA": df_location, "MESSAGE": outmsg_sp[0]}
        else:
            cursor.execute('select @_sp_Misc_get_1')
            sp_out_msg = cursor.fetchone()
            return {"MESSAGE": sp_out_msg[0], "DATA": "NO_DATA"}

    def eClaim_travelexp_get(self):
        cursor = connections['eclaim_db'].cursor()
        parameters = (self.filter_json, '')
        cursor.callproc('sp_travel_get', parameters)
        if cursor.description != None:
            columns = [x[0] for x in cursor.description]
            rows = cursor.fetchall()
            cursor.execute('select @_sp_travel_get_1')
            outmsg_sp = cursor.fetchone()
            rows = list(rows)
            df_location = pd.DataFrame(rows, columns=columns)
            return {"DATA": df_location, "MESSAGE": outmsg_sp[0]}
        else:
            cursor.execute('select @_sp_travel_get_1')
            sp_out_msg = cursor.fetchone()
            return {"MESSAGE": sp_out_msg[0], "DATA": "NO_DATA"}

    def eClaim_incidental_get(self):
        cursor = connections['eclaim_db'].cursor()
        parameters = (self.filter_json,'')
        cursor.callproc('sp_incidental_get', parameters)
        if cursor.description != None:
            columns = [x[0] for x in cursor.description]
            rows = cursor.fetchall()
            cursor.execute('select @_sp_incidental_get_1')
            outmsg_sp = cursor.fetchone()
            rows = list(rows)
            df_location = pd.DataFrame(rows, columns=columns)
            return {"DATA": df_location, "MESSAGE": outmsg_sp[0]}
        else:
            cursor.execute('select @_sp_incidental_get_1')
            sp_out_msg = cursor.fetchone()
            return {"MESSAGE": sp_out_msg[0], "DATA": "NO_DATA"}

    def eClaim_packingmoving_get(self):
        cursor = connections['eclaim_db'].cursor()
        parameters = (self.filter_json,'')
        cursor.callproc('sp_packingmoving_get', parameters)
        if cursor.description != None:
            columns = [x[0] for x in cursor.description]
            rows = cursor.fetchall()
            cursor.execute('select @_sp_packingmoving_get_1')
            outmsg_sp = cursor.fetchone()
            rows = list(rows)
            df_location = pd.DataFrame(rows, columns=columns)
            return {"DATA": df_location, "MESSAGE": outmsg_sp[0]}
        else:
            cursor.execute('select @_sp_packingmoving_get_1')
            sp_out_msg = cursor.fetchone()
            return {"MESSAGE": sp_out_msg[0], "DATA": "NO_DATA"}

    def eClaim_employee_get(self):
        cursor = connection.cursor()
        parameters = (self.filter_json, self.json_classification, '')
        cursor.callproc('sp_eClaimEmp_Get', parameters)
        if cursor.description != None:
            columns = [x[0] for x in cursor.description]
            rows = cursor.fetchall()
            cursor.execute('select @_sp_eClaimEmp_Get_2')
            outmsg_sp = cursor.fetchone()
            rows = list(rows)
            df_location = pd.DataFrame(rows, columns=columns)
            return {"DATA": df_location, "MESSAGE": outmsg_sp[0]}
        else:
            cursor.execute('select @_sp_eClaimEmp_Get_2')
            sp_out_msg = cursor.fetchone()
            return {"MESSAGE": sp_out_msg[0], "DATA": "NO_DATA"}

    def eClaim_employeename_get(self):
        cursor = connection.cursor()
        parameters = (self.filter_json, '')
        cursor.callproc('sp_eClaimEmpName_Get', parameters)
        if cursor.description != None:
            columns = [x[0] for x in cursor.description]
            rows = cursor.fetchall()
            cursor.execute('select @_sp_eClaimEmpName_Get_1')
            outmsg_sp = cursor.fetchone()
            rows = list(rows)
            df_location = pd.DataFrame(rows, columns=columns)
            return {"DATA": df_location, "MESSAGE": outmsg_sp[0]}
        else:
            cursor.execute('select @_sp_eClaimEmpName_Get_1')
            sp_out_msg = cursor.fetchone()
            return {"MESSAGE": sp_out_msg[0], "DATA": "NO_DATA"}

    def eClaim_emp_hierarchy_get(self):
        cursor = connection.cursor()
        parameters = (self.filter_json, '')
        cursor.callproc('sp_eClaimEmp_Hierarchy_Get', parameters)
        if cursor.description != None:
            columns = [x[0] for x in cursor.description]
            rows = cursor.fetchall()
            cursor.execute('select @_sp_eClaimEmp_Hierarchy_Get_1')
            outmsg_sp = cursor.fetchone()
            rows = list(rows)
            df_location = pd.DataFrame(rows, columns=columns)
            return {"DATA": df_location, "MESSAGE": outmsg_sp[0]}
        else:
            cursor.execute('select @_sp_eClaimEmp_Hierarchy_Get_1')
            sp_out_msg = cursor.fetchone()
            return {"MESSAGE": sp_out_msg[0], "DATA": "NO_DATA"}

    def eClaim_entity_get(self):
        cursor = connection.cursor()
        quot = ''
        query = 'select entity_gid from gal_mst_temployee where employee_gid = '
        gid = str(self.employee_gid)
        query = quot+query+gid+quot
        cursor.execute(query)
        columns = [x[0] for x in cursor.description]
        rows = cursor.fetchall()
        cursor.close()
        rows = list(rows)
        df_location = pd.DataFrame(rows, columns=columns)
        return {"DATA": df_location}

    def eClaim_emp_grade_get(self):
        cursor = connection.cursor()
        quot = ''
        query = 'select entity_gid from gal_mst_temployee where employee_gid = '
        gid = str(self.employee_gid)
        query = quot+query+gid+quot
        cursor.execute(query)
        columns = [x[0] for x in cursor.description]
        rows = cursor.fetchall()
        cursor.close()
        rows = list(rows)
        df_location = pd.DataFrame(rows, columns=columns)
        return {"DATA": df_location}

    def eClaim_employeebnk_get(self):
        cursor = connection.cursor()
        parameters = (self.filter_json,'')
        cursor.callproc('sp_eClaimEmp_bank_Get', parameters)
        if cursor.description != None:
            columns = [x[0] for x in cursor.description]
            rows = cursor.fetchall()
            cursor.execute('select @_sp_eClaimEmp_Get_1')
            outmsg_sp = cursor.fetchone()
            rows = list(rows)
            df_location = pd.DataFrame(rows, columns=columns)
            return {"DATA": df_location, "MESSAGE": outmsg_sp[0]}
        else:
            cursor.execute('select @_sp_eClaimEmp_bank_Get_1')
            sp_out_msg = cursor.fetchone()
            return {"MESSAGE": sp_out_msg[0], "DATA": "NO_DATA"}

    def eClaim_branch_get(self):
        cursor = connection.cursor()
        parameters = (self.filter_json, '')
        cursor.callproc('sp_Branch_Data_Get', parameters)
        if cursor.description != None:
            columns = [x[0] for x in cursor.description]
            rows = cursor.fetchall()
            cursor.execute('select @_sp_Branch_Data_Get_1')
            outmsg_sp = cursor.fetchone()
            rows = list(rows)
            df_location = pd.DataFrame(rows, columns=columns)
            return {"DATA": df_location, "MESSAGE": outmsg_sp[0]}
        else:
            cursor.execute('select @_sp_Branch_Data_Get_1')
            sp_out_msg = cursor.fetchone()
            return {"MESSAGE": sp_out_msg[0], "DATA": "NO_DATA"}

    def eClaim_approverlist_get(self):
        cursor = connections['eclaim_db'].cursor()
        parameters = (self.filter_json, '')
        cursor.callproc('sp_Approver_Get', parameters)
        if cursor.description != None:
            columns = [x[0] for x in cursor.description]
            rows = cursor.fetchall()
            cursor.execute('select @_sp_Approver_Get_1')
            outmsg_sp = cursor.fetchone()
            rows = list(rows)
            df_location = pd.DataFrame(rows, columns=columns)
            return {"DATA": df_location, "MESSAGE": outmsg_sp[0]}
        else:
            cursor.execute('select @_sp_Approver_Get_1')
            sp_out_msg = cursor.fetchone()
            return {"MESSAGE": sp_out_msg[0], "DATA": "NO_DATA"}

    def eClaim_branchtoemp_get(self):
        cursor = connection.cursor()
        parameters = (self.filter_json, '')
        cursor.callproc('sp_Emp_Branch_Get', parameters)
        if cursor.description != None:
            columns = [x[0] for x in cursor.description]
            rows = cursor.fetchall()
            cursor.execute('select @_sp_Emp_Branch_Get_1')
            outmsg_sp = cursor.fetchone()
            rows = list(rows)
            df_location = pd.DataFrame(rows, columns=columns)
            return {"DATA": df_location, "MESSAGE": outmsg_sp[0]}
        else:
            cursor.execute('select @_sp_Emp_Branch_Get_1')
            sp_out_msg = cursor.fetchone()
            return {"MESSAGE": sp_out_msg[0], "DATA": "NO_DATA"}

    def eClaim_forward_get(self):
        cursor = connections['eclaim_db'].cursor()
        parameters = (self.filter_json, '')
        cursor.callproc('sp_Forward_Get', parameters)
        if cursor.description != None:
            columns = [x[0] for x in cursor.description]
            rows = cursor.fetchall()
            cursor.execute('select @_sp_Forward_Get_1')
            outmsg_sp = cursor.fetchone()
            rows = list(rows)
            df_location = pd.DataFrame(rows, columns=columns)
            return {"DATA": df_location, "MESSAGE": outmsg_sp[0]}
        else:
            cursor.execute('select @_sp_Forward_Get_1')
            sp_out_msg = cursor.fetchone()
            return {"MESSAGE": sp_out_msg[0], "DATA": "NO_DATA"}

    def eClaim_citytoallowance_get(self):
        cursor = connections['eclaim_db'].cursor()
        parameters = (self.filter_json, '')
        cursor.callproc('sp_claimallowance_get', parameters)
        if cursor.description != None:
            columns = [x[0] for x in cursor.description]
            rows = cursor.fetchall()
            cursor.execute('select @_sp_claimallowance_get_1')
            outmsg_sp = cursor.fetchone()
            rows = list(rows)
            df_location = pd.DataFrame(rows, columns=columns)
            return {"DATA": df_location, "MESSAGE": outmsg_sp[0]}
        else:
            cursor.execute('select @_sp_claimallowance_get_1')
            sp_out_msg = cursor.fetchone()
            return {"MESSAGE": sp_out_msg[0], "DATA": "NO_DATA"}

    def eClaim_statetoholiday_get(self):
        cursor = connections['eclaim_db'].cursor()
        parameters = (self.filter_json, '')
        cursor.callproc('sp_Holidaycheck_get', parameters)
        if cursor.description != None:
            columns = [x[0] for x in cursor.description]
            rows = cursor.fetchall()
            cursor.execute('select @_sp_Holidaycheck_get_1')
            outmsg_sp = cursor.fetchone()
            rows = list(rows)
            df_location = pd.DataFrame(rows, columns=columns)
            return {"DATA": df_location, "MESSAGE": outmsg_sp[0]}
        else:
            cursor.execute('select @_sp_Holidaycheck_get_1')
            sp_out_msg = cursor.fetchone()
            return {"MESSAGE": sp_out_msg[0], "DATA": "NO_DATA"}


    def eClaim_expensecity_get(self):
        cursor = connections['eclaim_db'].cursor()
        parameters = (self.filter_json, '')
        cursor.callproc('sp_expensecity_get', parameters)
        if cursor.description != None:
            columns = [x[0] for x in cursor.description]
            rows = cursor.fetchall()
            cursor.execute('select @_sp_expensecity_get_1')
            outmsg_sp = cursor.fetchone()
            rows = list(rows)
            df_location = pd.DataFrame(rows, columns=columns)
            return {"DATA": df_location, "MESSAGE": outmsg_sp[0]}
        else:
            cursor.execute('select @_sp_expensecity_get_1')
            sp_out_msg = cursor.fetchone()
            return {"MESSAGE": sp_out_msg[0], "DATA": "NO_DATA"}

    def eClaim_paymentstatus_get(self):
        cursor = connection.cursor()
        parameters = (self.filter_json, '')
        cursor.callproc('sp_eclaim_ap_paymentstatus', parameters)
        if cursor.description != None:
            columns = [x[0] for x in cursor.description]
            rows = cursor.fetchall()
            cursor.execute('select @_sp_eclaim_ap_paymentstatus_1')
            outmsg_sp = cursor.fetchone()
            rows = list(rows)
            df_location = pd.DataFrame(rows, columns=columns)
            return {"DATA": df_location, "MESSAGE": outmsg_sp[0]}
        else:
            cursor.execute('select @_sp_eclaim_ap_paymentstatus_1')
            sp_out_msg = cursor.fetchone()
            return {"MESSAGE": sp_out_msg[0], "DATA": "NO_DATA"}

    def eClaim_citytogst_get(self):
        cursor = connection.cursor()
        parameters = (self.filter_json, '')
        cursor.callproc('sp_eclaim_citytogst', parameters)
        if cursor.description != None:
            columns = [x[0] for x in cursor.description]
            rows = cursor.fetchall()
            cursor.execute('select @_sp_eclaim_citytogst_1')
            outmsg_sp = cursor.fetchone()
            rows = list(rows)
            df_location = pd.DataFrame(rows, columns=columns)
            return {"DATA": df_location, "MESSAGE": outmsg_sp[0]}
        else:
            cursor.execute('select @_sp_eclaim_citytogst_1')
            sp_out_msg = cursor.fetchone()
            return {"MESSAGE": sp_out_msg[0], "DATA": "NO_DATA"}

    def eClaim_ccbs_get(self):
        cursor = connections['eclaim_db'].cursor()
        parameters = (self.filter_json, '')
        cursor.callproc('sp_ccbs_get', parameters)
        if cursor.description != None:
            columns = [x[0] for x in cursor.description]
            rows = cursor.fetchall()
            cursor.execute('select @_sp_ccbs_get_1')
            outmsg_sp = cursor.fetchone()
            rows = list(rows)
            df_location = pd.DataFrame(rows, columns=columns)
            return {"DATA": df_location, "MESSAGE": outmsg_sp[0]}
        else:
            cursor.execute('select @_sp_ccbs_get_1')
            sp_out_msg = cursor.fetchone()
            return {"MESSAGE": sp_out_msg[0], "DATA": "NO_DATA"}

    def eClaim_tourtoemp_get(self):
        cursor = connections['eclaim_db'].cursor()
        quot = ''
        format = "%d-%b-%Y"
        query = 'select requestno,empgrade,empgid,requestdate,empbranchgid from claim_trn_ttourrequest where gid = '
        gid = str(self.employee_gid)
        query = quot+query+gid+quot
        cursor.execute(query)
        columns = [x[0] for x in cursor.description]
        rows = cursor.fetchall()
        cursor.close()
        rows = list(rows)
        df_location = pd.DataFrame(rows, columns=columns)
        return {"DATA": df_location}

    def eClaim_gradetoelig_get(self):
        cursor = connections['eclaim_db'].cursor()
        parameters = (self.filter_json, '')
        cursor.callproc('sp_gradeeligible_get', parameters)
        if cursor.description != None:
            columns = [x[0] for x in cursor.description]
            rows = cursor.fetchall()
            cursor.execute('select @_sp_gradeeligible_get_1')
            outmsg_sp = cursor.fetchone()
            rows = list(rows)
            df_location = pd.DataFrame(rows, columns=columns)
            return {"DATA": df_location, "MESSAGE": outmsg_sp[0]}
        else:
            cursor.execute('select @_sp_gradeeligible_get_1')
            sp_out_msg = cursor.fetchone()
            return {"MESSAGE": sp_out_msg[0], "DATA": "NO_DATA"}


    def eClaim_dailydiem_set(self):
        cursor = connections['eclaim_db'].cursor()
        parameters = (self.jsondata,self.jsonData,'')
        cursor.callproc('sp_dailydiem_Set', parameters)
        cursor.execute('select @_sp_dailydiem_Set_2')
        out_message = cursor.fetchone()
        return {"MESSAGE": out_message[0]}

    def eClaim_lodging_set(self):
        cursor = connections['eclaim_db'].cursor()
        parameters = (self.jsondata, self.jsonData, '')
        cursor.callproc('sp_Lodging_Set', parameters)
        cursor.execute('select @_sp_Lodging_Set_2')
        out_message = cursor.fetchone()
        return {"MESSAGE": out_message[0]}

    def eClaim_loccon_set(self):
        cursor = connections['eclaim_db'].cursor()
        parameters = (self.jsondata, self.jsonData, '')
        cursor.callproc('sp_Localconveyence_Set', parameters)
        cursor.execute('select @_sp_Localconveyence_Set_2')
        out_message = cursor.fetchone()
        return {"MESSAGE": out_message[0]}

    def eClaim_miscellaneous_set(self):
        cursor = connections['eclaim_db'].cursor()
        parameters = (self.jsondata, self.jsonData,'')
        cursor.callproc('sp_Misc_Set', parameters)
        cursor.execute('select @_sp_Misc_Set_2')
        out_message = cursor.fetchone()
        return {"MESSAGE": out_message[0]}

    def eClaim_pkgmoving_set(self):
        cursor = connections['eclaim_db'].cursor()
        parameters = (self.jsondata,self.jsonData,'')
        cursor.callproc('sp_packingmoving_Set', parameters)
        cursor.execute('select @_sp_packingmoving_Set_2')
        out_message = cursor.fetchone()
        return {"MESSAGE": out_message[0]}

    def eClaim_travelexp_set(self):
        cursor = connections['eclaim_db'].cursor()
        parameters = (self.jsondata, self.jsonData,'')
        cursor.callproc('sp_travel_Set', parameters)
        cursor.execute('select @_sp_travel_Set_2')
        out_message = cursor.fetchone()
        return {"MESSAGE": out_message[0]}

    def eClaim_incidental_set(self):
        cursor = connections['eclaim_db'].cursor()
        parameters = (self.jsondata, self.jsonData, '')
        cursor.callproc('sp_Incidental_Set', parameters)
        cursor.execute('select @_sp_Incidental_Set_2')
        out_message = cursor.fetchone()
        return {"MESSAGE": out_message[0]}

    def eClaim_movetoapproval_set(self):
        cursor = connections['eclaim_db'].cursor()
        parameters = (self.jsonData, '')
        cursor.callproc('sp_movetoapprove_Set', parameters)
        cursor.execute('select @_sp_movetoapprove_Set_1')
        out_message = cursor.fetchone()
        return {"MESSAGE": out_message[0]}

    def eClaim_movetoapproval2_set(self):
        cursor = connections['eclaim_db'].cursor()
        parameters = (self.jsonData, '')
        cursor.callproc('sp_approval_Set', parameters)
        cursor.execute('select @_sp_approval_Set_1')
        out_message = cursor.fetchone()
        return {"MESSAGE": out_message[0]}

    def eClaim_return_set(self):
        cursor = connections['eclaim_db'].cursor()
        parameters = (self.jsonData, '')
        cursor.callproc('sp_return_Set', parameters)
        cursor.execute('select @_sp_return_Set_1')
        out_message = cursor.fetchone()
        return {"MESSAGE": out_message[0]}

    def eClaim_forward_set(self):
        cursor = connections['eclaim_db'].cursor()
        parameters = (self.jsonData, '')
        cursor.callproc('sp_Forward_Set', parameters)
        cursor.execute('select @_sp_Forward_Set_1')
        out_message = cursor.fetchone()
        return {"MESSAGE": out_message[0]}

    def eClaim_reject_set(self):
        cursor = connections['eclaim_db'].cursor()
        parameters = (self.jsonData, '')
        cursor.callproc('sp_reject_Set', parameters)
        cursor.execute('select @_sp_reject_Set_1')
        out_message = cursor.fetchone()
        return {"MESSAGE": out_message[0]}

    def eClaim_approveamount_set(self):
        cursor = connections['eclaim_db'].cursor()
        parameters = (self.jsondata, self.jsonData, '')
        cursor.callproc('sp_approvedamount_Set', parameters)
        cursor.execute('select @_sp_approvedamount_Set_2')
        out_message = cursor.fetchone()
        return {"MESSAGE": out_message[0]}


    def eClaim_approval_get(self):
        cursor = connections['eclaim_db'].cursor()
        parameters = (self.filter_json, '')
        cursor.callproc('sp_approval_Get', parameters)
        if cursor.description != None:
            columns = [x[0] for x in cursor.description]
            rows = cursor.fetchall()
            cursor.execute('select @_sp_approval_Get_1')
            outmsg_sp = cursor.fetchone()
            rows = list(rows)
            df_location = pd.DataFrame(rows, columns=columns)
            return {"DATA": df_location, "MESSAGE": outmsg_sp[0]}
        else:
            cursor.execute('select @_sp_approval_Get_1')
            sp_out_msg = cursor.fetchone()
            return {"MESSAGE": sp_out_msg[0], "DATA": "NO_DATA"}

    def eClaim_tourreason_get(self):
        cursor = connections['eclaim_db'].cursor()
        quot = ''
        query = 'select gid,code,name from claim_mst_ttourreason where status = 1 and entitygid = 1 '
        query = quot+query+quot
        cursor.execute(query)
        columns = [x[0] for x in cursor.description]
        rows = cursor.fetchall()
        cursor.close()
        rows = list(rows)
        df_location = pd.DataFrame(rows, columns=columns)
        return {"DATA": df_location}

    def eClaim_empgrade_get(self):
        cursor = connections['eclaim_db'].cursor()
        quot = ''
        query = 'select gid,designation,orderno,grade from claim_tmp_temployeemapping where status = 1'
        query = quot+query+quot
        cursor.execute(query)
        columns = [x[0] for x in cursor.description]
        rows = cursor.fetchall()
        cursor.close()
        rows = list(rows)
        df_location = pd.DataFrame(rows, columns=columns)
        return {"DATA": df_location}

    def eClaim_empwise_grade_get(self):
        cursor = connections['eclaim_db'].cursor()
        parameters = (self.filter_json, '')
        cursor.callproc('sp_emp_grade_designation_get', parameters)
        if cursor.description != None:
            columns = [x[0] for x in cursor.description]
            rows = cursor.fetchall()
            cursor.execute('select @_sp_emp_grade_designation_get_1')
            outmsg_sp = cursor.fetchone()
            rows = list(rows)
            df_location = pd.DataFrame(rows, columns=columns)
            return {"DATA": df_location, "MESSAGE": outmsg_sp[0]}
        else:
            cursor.execute('select @_sp_approval_Get_1')
            sp_out_msg = cursor.fetchone()
            return {"MESSAGE": sp_out_msg[0], "DATA": "NO_DATA"}

    def eClaim_tourrequest_set(self):
        cursor = connections['eclaim_db'].cursor()
        parameters = (self.jsondata, self.jsonData, '')
        cursor.callproc('sp_tourrequest_Set', parameters)
        cursor.execute('select @_sp_tourrequest_Set_2')
        out_message = cursor.fetchone()
        return {"MESSAGE": out_message[0]}


    def eClaim_tourdetails_get(self):
        cursor = connections['eclaim_db'].cursor()
        parameters = (self.filter_json, '')
        cursor.callproc('sp_tourdetails_get', parameters)
        if cursor.description != None:
            columns = [x[0] for x in cursor.description]
            rows = cursor.fetchall()
            cursor.execute('select @_sp_tourdetails_get_1')
            outmsg_sp = cursor.fetchone()
            rows = list(rows)
            df_location = pd.DataFrame(rows, columns=columns)
            return {"DATA": df_location, "MESSAGE": outmsg_sp[0]}
        else:
            cursor.execute('select @_sp_tourdetails_get_1')
            sp_out_msg = cursor.fetchone()
            return {"MESSAGE": sp_out_msg[0], "DATA": "NO_DATA"}


    def eClaim_hsncode_get(self):
        cursor = connection.cursor()
        quot = ''
        query = 'select hsn_gid,hsn_code,hsn_description,hsn_cgstrate,hsn_sgstrate,hsn_igstrate from gal_mst_thsn where hsn_isactive = "Y"'
        query3 = ' and hsn_isremoved = "N"'
        query5 = ' and entity_gid = 1'
        query = quot+query+query3+query5+quot
        cursor.execute(query)
        columns = [x[0] for x in cursor.description]
        rows = cursor.fetchall()
        cursor.close()
        rows = list(rows)
        df_location = pd.DataFrame(rows, columns=columns)
        return {"DATA": df_location}

    def eClaim_citytostate_get(self):
        cursor = connection.cursor()
        parameters = (self.filter_json, '')
        cursor.callproc('sp_citystate_get', parameters)
        if cursor.description != None:
            columns = [x[0] for x in cursor.description]
            rows = cursor.fetchall()
            cursor.execute('select @_sp_citystate_get_1')
            outmsg_sp = cursor.fetchone()
            rows = list(rows)
            df_location = pd.DataFrame(rows, columns=columns)
            return {"DATA": df_location, "MESSAGE": outmsg_sp[0]}
        else:
            cursor.execute('select @_sp_citystate_get_1')
            sp_out_msg = cursor.fetchone()
            return {"MESSAGE": sp_out_msg[0], "DATA": "NO_DATA"}

    def eClaim_holydaydeim_get(self):
        cursor = connections['eclaim_db'].cursor()
        parameters = (self.filter_json, '')
        cursor.callproc('sp_holidaydeim_get', parameters)
        if cursor.description != None:
            columns = [x[0] for x in cursor.description]
            rows = cursor.fetchall()
            cursor.execute('select @_sp_holidaydeim_get_1')
            outmsg_sp = cursor.fetchone()
            rows = list(rows)
            df_location = pd.DataFrame(rows, columns=columns)
            return {"DATA": df_location, "MESSAGE": outmsg_sp[0]}
        else:
            cursor.execute('select @_sp_holidaydeim_get_1')
            sp_out_msg = cursor.fetchone()
            return {"MESSAGE": sp_out_msg[0], "DATA": "NO_DATA"}


    def eClaim_hsntotaxrate_get(self):
        cursor = connection.cursor()
        quot = ''
        query = 'select  hsn_gid,hsn_cgstrate,hsn_sgstrate,hsn_igstrate from gal_mst_thsn where hsn_isactive = "Y"'
        query3 = ' and hsn_isremoved = "N"'
        query5 = ' and entity_gid = 1 and hsn_gid = '+ str(self.employee_gid)
        query = quot + query + query3 + query5 + quot
        cursor.execute(query)
        columns = [x[0] for x in cursor.description]
        rows = cursor.fetchall()
        cursor.close()
        rows = list(rows)
        df_location = pd.DataFrame(rows, columns=columns)
        return {"DATA": df_location}

    def eClaim_file_set(self):
        cursor = connection.cursor()
        parameters = (self.jsonData, '')
        cursor.callproc('sp_eClaimFiles_Set', parameters)
        cursor.execute('select @_sp_eClaimFiles_Set_1')
        out_message = cursor.fetchone()
        return {"MESSAGE": out_message[0]}

    def eClaim_file_get(self):
        cursor = connection.cursor()
        parameters = (self.filter_json, '')
        cursor.callproc('sp_eClaimFiles_Get', parameters)
        if cursor.description != None:
            columns = [x[0] for x in cursor.description]
            rows = cursor.fetchall()
            cursor.execute('select @_sp_eClaimFiles_Get_1')
            outmsg_sp = cursor.fetchone()
            rows = list(rows)
            df_location = pd.DataFrame(rows, columns=columns)
            return {"DATA": df_location, "MESSAGE": outmsg_sp[0]}
        else:
            cursor.execute('select @_sp_eClaimFiles_Get_1')
            sp_out_msg = cursor.fetchone()
            return {"MESSAGE": sp_out_msg[0], "DATA": "NO_DATA"}

    def eClaim_approvalflow_get(self):
        cursor = connections['eclaim_db'].cursor()
        parameters = (self.filter_json, '')
        cursor.callproc('sp_approvalflow_get', parameters)
        if cursor.description != None:
            columns = [x[0] for x in cursor.description]
            rows = cursor.fetchall()
            cursor.execute('select @_sp_approvalflow_get_1')
            outmsg_sp = cursor.fetchone()
            rows = list(rows)
            df_location = pd.DataFrame(rows, columns=columns)
            return {"DATA": df_location, "MESSAGE": outmsg_sp[0]}
        else:
            cursor.execute('select @_sp_approvalflow_get_1')
            sp_out_msg = cursor.fetchone()
            return {"MESSAGE": sp_out_msg[0], "DATA": "NO_DATA"}

    def eClaim_approvalflow_pdf_get(self):
        cursor = connections['eclaim_db'].cursor()
        parameters = (self.filter_json, '')
        cursor.callproc('sp_approvalflow_pdf_get', parameters)
        if cursor.description != None:
            columns = [x[0] for x in cursor.description]
            rows = cursor.fetchall()
            cursor.execute('select @_sp_approvalflow_pdf_get_1')
            outmsg_sp = cursor.fetchone()
            rows = list(rows)
            df_location = pd.DataFrame(rows, columns=columns)
            return {"DATA": df_location, "MESSAGE": outmsg_sp[0]}
        else:
            cursor.execute('select @_sp_approvalflow_pdf_get_1')
            sp_out_msg = cursor.fetchone()
            return {"MESSAGE": sp_out_msg[0], "DATA": "NO_DATA"}

    def eClaim_emptodependent_get(self):
        cursor = connections['eclaim_db'].cursor()
        quot = ''
        query = 'SELECT gid,dependentname FROM claim_trn_ttraveldependent where empgid ='
        gid = str(self.employee_gid)
        query = quot+query+gid+quot
        cursor.execute(query)
        columns = [x[0] for x in cursor.description]
        rows = cursor.fetchall()
        cursor.close()
        rows = list(rows)
        df_location = pd.DataFrame(rows, columns=columns)
        return {"DATA": df_location}


    def eClaim_touradvance_set(self):
        cursor = connections['eclaim_db'].cursor()
        parameters = (self.jsondata, '')
        cursor.callproc('sp_touradvance_Set', parameters)
        cursor.execute('select @_sp_touradvance_Set_1')
        out_message = cursor.fetchone()
        return {"MESSAGE": out_message[0]}

    def eClaim_tourcancel_set(self):
        cursor = connections['eclaim_db'].cursor()
        parameters = (self.jsondata, '')
        cursor.callproc('sp_tourcancel_set', parameters)
        cursor.execute('select @_sp_tourcancel_set_1')
        out_message = cursor.fetchone()
        return {"MESSAGE": out_message[0]}

    def eClaim_advinv_set(self):
        cursor = connections['eclaim_db'].cursor()
        parameters = (self.jsondata, '')
        cursor.callproc('sp_touradvinv_Set', parameters)
        cursor.execute('select @_sp_touradvinv_Set_1')
        out_message = cursor.fetchone()
        return {"MESSAGE": out_message[0]}

    def eClaim_expinv_set(self):
        cursor = connections['eclaim_db'].cursor()
        parameters = (self.jsondata, '')
        cursor.callproc('sp_tourexpinv_Set', parameters)
        cursor.execute('select @_sp_tourexpinv_Set_1')
        out_message = cursor.fetchone()
        return {"MESSAGE": out_message[0]}


    def eClaim_touradvance_get(self):
        cursor = connections['eclaim_db'].cursor()
        parameters = (self.filter_json, '')
        cursor.callproc('sp_touradvance_get', parameters)
        if cursor.description != None:
            columns = [x[0] for x in cursor.description]
            rows = cursor.fetchall()
            cursor.execute('select @_sp_touradvance_get_1')
            outmsg_sp = cursor.fetchone()
            rows = list(rows)
            df_location = pd.DataFrame(rows, columns=columns)
            return {"DATA": df_location, "MESSAGE": outmsg_sp[0]}
        else:
            cursor.execute('select @_sp_touradvance_get_1')
            sp_out_msg = cursor.fetchone()
            return {"MESSAGE": sp_out_msg[0], "DATA": "NO_DATA"}


    def eClaim_hsncode(self):
        cursor = connection.cursor()
        quot = ''
        query = 'SELECT hsn_gid,hsn_code,hsn_description,hsn_igstrate FROM gal_mst_thsn where hsn_gid ='
        gid = str(self.employee_gid)
        query = quot + query + gid + quot
        cursor.execute(query)
        columns = [x[0] for x in cursor.description]
        rows = cursor.fetchall()
        cursor.close()
        rows = list(rows)
        df_location = pd.DataFrame(rows, columns=columns)
        return {"DATA": df_location}

    def get_APbankdetails(self):
        cursor = connection.cursor()
        parameters = (self.action, self.type, self.filter, self.classification, '');
        cursor.callproc('sp_APbankdetails_Get', parameters)
        columns = [x[0] for x in cursor.description]
        rows = cursor.fetchall()
        rows = list(rows)
        grn_dtl = pd.DataFrame(rows, columns=columns)
        if (self.type == "SUPPLIER_DETAILS"):
            i = 0
            while (cursor.nextset()):
                if (i != 1):
                    columns = [x[0] for x in cursor.description]
                    row = cursor.fetchall()
                    row = list(row)
                    tds = pd.DataFrame(row, columns=columns)
                    grn_dtl['tds_data'] = tds.to_json(orient='records')
                    i = 1
        return {"DATA": grn_dtl}

    def eClaim_glmapping_get(self):
        cursor = connections['eclaim_db'].cursor()
        parameters = (self.filter_json, '')
        cursor.callproc('sp_glmapping_get', parameters)
        if cursor.description != None:
            columns = [x[0] for x in cursor.description]
            rows = cursor.fetchall()
            cursor.execute('select @_sp_glmapping_get_1')
            outmsg_sp = cursor.fetchone()
            rows = list(rows)
            df_location = pd.DataFrame(rows, columns=columns)
            return {"DATA": df_location, "MESSAGE": outmsg_sp[0]}
        else:
            cursor.execute('select @_sp_glmapping_get_1')
            sp_out_msg = cursor.fetchone()
            return {"MESSAGE": sp_out_msg[0], "DATA": "NO_DATA"}

    def eClaim_tourreasondata_get(self):
        cursor = connections['eclaim_db'].cursor()
        parameters = (self.filter_json, '')
        cursor.callproc('sp_tourreason_get', parameters)
        if cursor.description != None:
            columns = [x[0] for x in cursor.description]
            rows = cursor.fetchall()
            cursor.execute('select @_sp_tourreason_get_1')
            outmsg_sp = cursor.fetchone()
            rows = list(rows)
            df_location = pd.DataFrame(rows, columns=columns)
            return {"DATA": df_location, "MESSAGE": outmsg_sp[0]}
        else:
            cursor.execute('select @_sp_tourreason_get_1')
            sp_out_msg = cursor.fetchone()
            return {"MESSAGE": sp_out_msg[0], "DATA": "NO_DATA"}

    def eClaim_exp_delete_set(self):
        cursor = connections['eclaim_db'].cursor()
        parameters = (self.filter_json, '')
        cursor.callproc('sp_tourexp_detele_Set', parameters)
        cursor.execute('select @_sp_tourexp_detele_Set_1')
        out_message = cursor.fetchone()
        return {"MESSAGE": out_message[0]}

    def eClaim_hrd_employeedtl_set(self):
        cursor = connections['eclaim_db'].cursor()
        parameters = (self.jsonData, '')
        cursor.callproc('sp_hrd_employeedtl_Set', parameters)
        cursor.execute('select @_sp_hrd_employeedtl_Set_1')
        out_message = cursor.fetchone()
        return {"MESSAGE": out_message[0]}

    def eClaim_employee_tmp_get(self):
        cursor = connections['eclaim_db'].cursor()
        parameters = (self.filter_json, '')
        cursor.callproc('sp_employee_tmp_get', parameters)
        if cursor.description != None:
            columns = [x[0] for x in cursor.description]
            rows = cursor.fetchall()
            cursor.execute('select @_sp_employee_tmp_get_1')
            outmsg_sp = cursor.fetchone()
            rows = list(rows)
            df_location = pd.DataFrame(rows, columns=columns)
            return {"DATA": df_location, "MESSAGE": outmsg_sp[0]}
        else:
            cursor.execute('select @_sp_employee_tmp_get_1')
            sp_out_msg = cursor.fetchone()
            return {"MESSAGE": sp_out_msg[0], "DATA": "NO_DATA"}

    # mobile Api
    def eClaim_tour_dailydiem_get(self):
        cursor = connections['eclaim_db'].cursor()
        parameters = (self.filter_json, '')
        cursor.callproc('sp_tour_dailydiem_get', parameters)
        if cursor.description != None:
            columns = [x[0] for x in cursor.description]
            rows = cursor.fetchall()
            cursor.execute('select @_sp_tour_dailydiem_get_1')
            outmsg_sp = cursor.fetchone()
            rows = list(rows)
            df_location = pd.DataFrame(rows, columns=columns)
            return {"DATA": df_location, "MESSAGE": outmsg_sp[0]}
        else:
            cursor.execute('select @_sp_tour_dailydiem_get_1')
            sp_out_msg = cursor.fetchone()
            return {"MESSAGE": sp_out_msg[0], "DATA": "NO_DATA"}

    def eClaim_tour_incidental_get(self):
        cursor = connections['eclaim_db'].cursor()
        parameters = (self.filter_json, '')
        cursor.callproc('sp_tour_incidental_get', parameters)
        if cursor.description != None:
            columns = [x[0] for x in cursor.description]
            rows = cursor.fetchall()
            cursor.execute('select @_sp_tour_incidental_get_1')
            outmsg_sp = cursor.fetchone()
            rows = list(rows)
            df_location = pd.DataFrame(rows, columns=columns)
            return {"DATA": df_location, "MESSAGE": outmsg_sp[0]}
        else:
            cursor.execute('select @_sp_tour_incidental_get_1')
            sp_out_msg = cursor.fetchone()
            return {"MESSAGE": sp_out_msg[0], "DATA": "NO_DATA"}

    def eClaim_tour_localconveyence_get(self):
        cursor = connections['eclaim_db'].cursor()
        parameters = (self.filter_json, '')
        cursor.callproc('sp_tour_localconveyence_get', parameters)
        if cursor.description != None:
            columns = [x[0] for x in cursor.description]
            rows = cursor.fetchall()
            cursor.execute('select @_sp_tour_localconveyence_get_1')
            outmsg_sp = cursor.fetchone()
            rows = list(rows)
            df_location = pd.DataFrame(rows, columns=columns)
            return {"DATA": df_location, "MESSAGE": outmsg_sp[0]}
        else:
            cursor.execute('select @_sp_tour_localconveyence_get_1')
            sp_out_msg = cursor.fetchone()
            return {"MESSAGE": sp_out_msg[0], "DATA": "NO_DATA"}

    def eClaim_tour_lodging_get(self):
        cursor = connections['eclaim_db'].cursor()
        parameters = (self.filter_json, '')
        cursor.callproc('sp_tour_lodging_get', parameters)
        if cursor.description != None:
            columns = [x[0] for x in cursor.description]
            rows = cursor.fetchall()
            cursor.execute('select @_sp_tour_lodging_get_1')
            outmsg_sp = cursor.fetchone()
            rows = list(rows)
            df_location = pd.DataFrame(rows, columns=columns)
            return {"DATA": df_location, "MESSAGE": outmsg_sp[0]}
        else:
            cursor.execute('select @_sp_tour_lodging_get_1')
            sp_out_msg = cursor.fetchone()
            return {"MESSAGE": sp_out_msg[0], "DATA": "NO_DATA"}

    def eClaim_tour_packingmoving_get(self):
        cursor = connections['eclaim_db'].cursor()
        parameters = (self.filter_json, '')
        cursor.callproc('sp_tour_packingmoving_get', parameters)
        if cursor.description != None:
            columns = [x[0] for x in cursor.description]
            rows = cursor.fetchall()
            cursor.execute('select @_sp_tour_packingmoving_get_1')
            outmsg_sp = cursor.fetchone()
            rows = list(rows)
            df_location = pd.DataFrame(rows, columns=columns)
            return {"DATA": df_location, "MESSAGE": outmsg_sp[0]}
        else:
            cursor.execute('select @_sp_tour_packingmoving_get_1')
            sp_out_msg = cursor.fetchone()
            return {"MESSAGE": sp_out_msg[0], "DATA": "NO_DATA"}

    def eClaim_tour_travel_get(self):
        cursor = connections['eclaim_db'].cursor()
        parameters = (self.filter_json, '')
        cursor.callproc('sp_tour_travel_get', parameters)
        if cursor.description != None:
            columns = [x[0] for x in cursor.description]
            rows = cursor.fetchall()
            cursor.execute('select @_sp_tour_travel_get_1')
            outmsg_sp = cursor.fetchone()
            rows = list(rows)
            df_location = pd.DataFrame(rows, columns=columns)
            return {"DATA": df_location, "MESSAGE": outmsg_sp[0]}
        else:
            cursor.execute('select @_sp_tour_travel_get_1')
            sp_out_msg = cursor.fetchone()
            return {"MESSAGE": sp_out_msg[0], "DATA": "NO_DATA"}

    def eClaim_tour_misc_get(self):
        cursor = connections['eclaim_db'].cursor()
        parameters = (self.filter_json, '')
        cursor.callproc('sp_tour_misc_get', parameters)
        if cursor.description != None:
            columns = [x[0] for x in cursor.description]
            rows = cursor.fetchall()
            cursor.execute('select @_sp_tour_misc_get_1')
            outmsg_sp = cursor.fetchone()
            rows = list(rows)
            df_location = pd.DataFrame(rows, columns=columns)
            return {"DATA": df_location, "MESSAGE": outmsg_sp[0]}
        else:
            cursor.execute('select @_sp_tour_misc_get_1')
            sp_out_msg = cursor.fetchone()
            return {"MESSAGE": sp_out_msg[0], "DATA": "NO_DATA"} 
            
    def eClaim_Recovery_get(self):
        cursor = connection.cursor()
        parameters = (self.filter_json, '')
        cursor.callproc('sp_eClaimRecovery_Get', parameters)
        if cursor.description != None:
            columns = [x[0] for x in cursor.description]
            rows = cursor.fetchall()
            cursor.execute('select @_sp_eClaimRecovery_Get_1')
            outmsg_sp = cursor.fetchone()
            rows = list(rows)
            df_location = pd.DataFrame(rows, columns=columns)
            return {"DATA": df_location, "MESSAGE": outmsg_sp[0]}
        else:
            cursor.execute('select @_sp_eClaimRecovery_Get_1')
            sp_out_msg = cursor.fetchone()
            return {"MESSAGE": sp_out_msg[0], "DATA": "NO_DATA"}

    def eClaim_Crnno_get(self):
        cursor = connection.cursor()
        parameters = (self.filter_json, '')
        cursor.callproc('sp_eClaim_CRNNo_Get', parameters)
        if cursor.description != None:
            columns = [x[0] for x in cursor.description]
            rows = cursor.fetchall()
            cursor.execute('select @_sp_eClaim_CRNNo_Get_1')
            outmsg_sp = cursor.fetchone()
            rows = list(rows)
            df_location = pd.DataFrame(rows, columns=columns)
            return {"DATA": df_location, "MESSAGE": outmsg_sp[0]}
        else:
            cursor.execute('select @_sp_eClaim_CRNNo_Get_1')
            sp_out_msg = cursor.fetchone()
            return {"MESSAGE": sp_out_msg[0], "DATA": "NO_DATA"}

    def eClaim_Crnno_advance_get(self):
        cursor = connection.cursor()
        parameters = (self.filter_json, '')
        cursor.callproc('sp_eClaim_CRN_Advance_Get', parameters)
        if cursor.description != None:
            columns = [x[0] for x in cursor.description]
            rows = cursor.fetchall()
            cursor.execute('select @_sp_eClaim_CRN_Advance_Get_1')
            outmsg_sp = cursor.fetchone()
            rows = list(rows)
            df_location = pd.DataFrame(rows, columns=columns)
            return {"DATA": df_location, "MESSAGE": outmsg_sp[0]}
        else:
            cursor.execute('select @_sp_eClaim_CRN_Advance_Get_1')
            sp_out_msg = cursor.fetchone()
            return {"MESSAGE": sp_out_msg[0], "DATA": "NO_DATA"}

    def eClaim_advance_adjust_set(self):
        cursor = connections['eclaim_db'].cursor()
        parameters = (self.jsondata, '')
        cursor.callproc('sp_advance_adjust_set', parameters)
        cursor.execute('select @_sp_advance_adjust_set_1')
        out_message = cursor.fetchone()
        return {"MESSAGE": out_message[0]}

    def eClaim_jvdata_get(self):
        cursor = connection.cursor()
        parameters = (self.filter_json, '')
        cursor.callproc('sp_eClaim_JV_Get', parameters)
        if cursor.description != None:
            columns = [x[0] for x in cursor.description]
            rows = cursor.fetchall()
            rows = list(rows)
            df_location = pd.DataFrame(rows, columns=columns)
            data = {}
            data['debit'] = json.loads(df_location.to_json(orient='records'))
            i = 0
            while (cursor.nextset()):
                if (i != 1):
                    columns = [x[0] for x in cursor.description]
                    rows = cursor.fetchall()
                    rows = list(rows)
                    grn_dtl = pd.DataFrame(rows, columns=columns)
                    if i == 0:
                        data['credit'] = json.loads(grn_dtl.to_json(orient='records'))
                        i = 1
            return data
        else:
            cursor.execute('select @_sp_eClaim_JV_Get_1')
            sp_out_msg = cursor.fetchone()
            return {"MESSAGE": sp_out_msg[0], "DATA": "NO_DATA"}


    def eClaim_ongoingtour_get(self):
        cursor = connections['eclaim_db'].cursor()
        parameters = (self.filter_json, '')
        cursor.callproc('sp_ongoingtour_Get', parameters)
        if cursor.description != None:
            columns = [x[0] for x in cursor.description]
            rows = cursor.fetchall()
            cursor.execute('select @_sp_ongoingtour_Get_1')
            outmsg_sp = cursor.fetchone()
            rows = list(rows)
            df_location = pd.DataFrame(rows, columns=columns)
            return {"DATA": df_location, "MESSAGE": outmsg_sp[0]}
        else:
            cursor.execute('select @_sp_ongoingtour_Get_1')
            sp_out_msg = cursor.fetchone()
            return {"MESSAGE": sp_out_msg[0], "DATA": "NO_DATA"}

    def get_server_date(self):
        cursor = connection.cursor()
        parameters = (self.date, '')
        cursor.callproc('sp_Server_Get', parameters)
        if cursor.description != None:
            rows = cursor.fetchone()
            cursor.execute('select @_sp_Server_Get_1')
            outmsg_sp = cursor.fetchone()
            return rows[0]
        else:
            return ''

    def eClaim_Expense_Amount_get(self):
        cursor = connections['eclaim_db'].cursor()
        parameters = (self.filter_json, '')
        cursor.callproc('sp_claimrequest_datasum_get', parameters)
        if cursor.description != None:
            columns = [x[0] for x in cursor.description]
            rows = cursor.fetchall()
            cursor.execute('select @_sp_claimrequest_datasum_get_1')
            outmsg_sp = cursor.fetchone()
            rows = list(rows)
            df_location = pd.DataFrame(rows, columns=columns)
            return {"DATA": df_location, "MESSAGE": outmsg_sp[0]}
        else:
            cursor.execute('select @_sp_claimrequest_datasum_get_1')
            sp_out_msg = cursor.fetchone()
            return {"MESSAGE": sp_out_msg[0], "DATA": "NO_DATA"}

    def eClaim_tourrequest_report_get(self):
        cursor = connections['eclaim_db'].cursor()
        parameters = (self.filter_json, '')
        cursor.callproc('sp_tourrequest_report_get', parameters)
        if cursor.description != None:
            columns = [x[0] for x in cursor.description]
            rows = cursor.fetchall()
            cursor.execute('select @_sp_tourrequest_report_get_1')
            outmsg_sp = cursor.fetchone()
            rows = list(rows)
            df_location = pd.DataFrame(rows, columns=columns)
            return {"DATA": df_location, "MESSAGE": outmsg_sp[0]}
        else:
            cursor.execute('select @_sp_tourrequest_report_get_1')
            sp_out_msg = cursor.fetchone()
            return {"MESSAGE": sp_out_msg[0], "DATA": "NO_DATA"}

    def eClaim_advancecancelmaker_get(self):
        cursor = connections['eclaim_db'].cursor()
        parameters = (self.filter_json, '')
        cursor.callproc('sp_advance_cancelmaker_get', parameters)
        if cursor.description != None:
            columns = [x[0] for x in cursor.description]
            rows = cursor.fetchall()
            cursor.execute('select @_sp_advance_cancelmaker_get_1')
            outmsg_sp = cursor.fetchone()
            rows = list(rows)
            df_location = pd.DataFrame(rows, columns=columns)
            return {"DATA": df_location, "MESSAGE": outmsg_sp[0]}
        else:
            cursor.execute('select @_sp_advance_cancelmaker_get_1')
            sp_out_msg = cursor.fetchone()
            return {"MESSAGE": sp_out_msg[0], "DATA": "NO_DATA"}

    def eClaim_tourcancelmaker_get(self):
        cursor = connections['eclaim_db'].cursor()
        parameters = (self.filter_json, '')
        cursor.callproc('sp_tour_cancelmaker_get', parameters)
        if cursor.description != None:
            columns = [x[0] for x in cursor.description]
            rows = cursor.fetchall()
            cursor.execute('select @_sp_tour_cancelmaker_get_1')
            outmsg_sp = cursor.fetchone()
            rows = list(rows)
            df_location = pd.DataFrame(rows, columns=columns)
            return {"DATA": df_location, "MESSAGE": outmsg_sp[0]}
        else:
            cursor.execute('select @_sp_tour_cancelmaker_get_1')
            sp_out_msg = cursor.fetchone()
            return {"MESSAGE": sp_out_msg[0], "DATA": "NO_DATA"}

    def eClaim_tourequest_cancel_get(self):
        cursor = connections['eclaim_db'].cursor()
        parameters = (self.filter_json, '')
        cursor.callproc('sp_tourequest_cancel_get', parameters)
        if cursor.description != None:
            columns = [x[0] for x in cursor.description]
            rows = cursor.fetchall()
            cursor.execute('select @_sp_tourequest_cancel_get_1')
            outmsg_sp = cursor.fetchone()
            rows = list(rows)
            df_location = pd.DataFrame(rows, columns=columns)
            return {"DATA": df_location, "MESSAGE": outmsg_sp[0]}
        else:
            cursor.execute('select @_sp_tourequest_cancel_get_1')
            sp_out_msg = cursor.fetchone()
            return {"MESSAGE": sp_out_msg[0], "DATA": "NO_DATA"}

    def eClaim_jv_crn_get(self):
        cursor = connection.cursor()
        parameters = (self.filter_json, '')
        cursor.callproc('sp_eClaim_jv_crn_get', parameters)
        if cursor.description != None:
            columns = [x[0] for x in cursor.description]
            rows = cursor.fetchall()
            cursor.execute('select @_sp_eClaim_jv_crn_get_1')
            outmsg_sp = cursor.fetchone()
            rows = list(rows)
            df_location = pd.DataFrame(rows, columns=columns)
            return {"DATA": df_location, "MESSAGE": outmsg_sp[0]}
        else:
            cursor.execute('select @_sp_eClaim_jv_crn_get_1')
            sp_out_msg = cursor.fetchone()
            return {"MESSAGE": sp_out_msg[0], "DATA": "NO_DATA"}

    def eClaim_branch_wisecount_get(self):
        cursor = connections['eclaim_db'].cursor()
        parameters = (self.filter_json, '')
        cursor.callproc('sp_branch_wisecount_get', parameters)
        if cursor.description != None:
            columns = [x[0] for x in cursor.description]
            rows = cursor.fetchall()
            cursor.execute('select @_sp_branch_wisecount_get_1')
            outmsg_sp = cursor.fetchone()
            rows = list(rows)
            df_location = pd.DataFrame(rows, columns=columns)
            return {"DATA": df_location, "MESSAGE": outmsg_sp[0]}
        else:
            cursor.execute('select @_sp_branch_wisecount_get_1')
            sp_out_msg = cursor.fetchone()
            return {"MESSAGE": sp_out_msg[0], "DATA": "NO_DATA"}

    def eClaim_ccbs_set(self):
        cursor = connections['eclaim_db'].cursor()
        parameters = (self.jsondata, '')
        cursor.callproc('sp_ccbs_set', parameters)
        cursor.execute('select @_sp_ccbs_set_1')
        out_message = cursor.fetchone()
        return {"MESSAGE": out_message[0]}