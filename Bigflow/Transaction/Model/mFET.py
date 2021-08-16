from django.db import connection
import pandas as pd
from Bigflow.Master.Model import mVariable
import json



class FET_model(mVariable.variable):
    # def __init__(self, day=10, month=10, year=2000):
    #     self.day = day
    #     self.month = month
    #     self.year = year

    def get_preschedule_fet(self):
        cursor = connection.cursor()
        employee = self.employee_gid
        if employee == 0:
            parameters = (self.action, self.employee_gid, self.date, self.jsondata, self.create_by, self.jsonData, '')
            cursor.callproc('sp_FETSchedule_Get', parameters)
            columns = [x[0] for x in cursor.description]
            rows = cursor.fetchall()
            cursor.execute('select @_sp_FETSchedule_Get_6')
            out_put = cursor.fetchone()
            rows = list(rows)
            df_preschedule = pd.DataFrame(rows, columns=columns)
            return {"DATA": df_preschedule, "MESSAGE": out_put[0]}
        else:
            parameters = (self.action, self.employee_gid, self.date, self.jsondata, self.create_by, self.jsonData, '')
            cursor.callproc('sp_FETSchedule_Get', parameters)
            columns = [x[0] for x in cursor.description]
            rows = cursor.fetchall()
            cursor.execute('select @_sp_FETSchedule_Get_6')
            out_put = cursor.fetchone()
            rows = list(rows)
            df_preschedule = pd.DataFrame(rows, columns=columns)
            dd = df_preschedule.loc[df_preschedule['schedule_employee_gid'] == pd.to_numeric(self.employee_gid)]
            return {"DATA": dd, "MESSAGE": out_put[0]}

    def get_preschedul(self):
        cursor = connection.cursor()
        parameters = (self.action, self.type, self.jsondata)
        cursor.callproc('sp_ScheduleFilter_Get', parameters)
        columns = [x[0] for x in cursor.description]
        rows = cursor.fetchall()
        cursor.execute('select @_sp_ScheduleFilter_Get_2')
        out_put = cursor.fetchone()
        rows = list(rows)
        df_preschedule = pd.DataFrame(rows, columns=columns)
        return df_preschedule

    def get_preschedule(self):
        cursor = connection.cursor()
        parameters = (self.action, self.employee_gid, self.date, self.jsondata, self.create_by, self.jsonData, '')
        cursor.callproc('sp_FETSchedule_Get', parameters)
        columns = [x[0] for x in cursor.description]
        rows = cursor.fetchall()
        cursor.execute('select @_sp_FETSchedule_Get_6')
        out_put = cursor.fetchone()
        rows = list(rows)
        df_preschedule = pd.DataFrame(rows, columns=columns)
        return df_preschedule

    def get_empvsSchedule(self):
        cursor = connection.cursor()
        parameters = (self.action, '', self.jsonData, self.jsondata, '')
        cursor.callproc('sp_FETReview_Get', parameters)
        if cursor.description != None:
            columns = [x[0] for x in cursor.description]
            rows = cursor.fetchall()
            cursor.execute('select @_sp_FETReview_Get_4')
            out_put = cursor.fetchone()
            rows = list(rows)
            df_preschedule = pd.DataFrame(rows, columns=columns)
            return df_preschedule
        else:
            cursor.execute('select @_sp_FETReview_Get_4')
            out_put = cursor.fetchone()
            df_preschedule = None
            return df_preschedule

    def get_followup_reason_fet(self):
        cursor = connection.cursor()
        parameters = (self.schedule_type_gid, self.entity_gid, '')
        cursor.callproc('sp_FETFollowupReason_Get', parameters)
        columns = [x[0] for x in cursor.description]
        rows = cursor.fetchall()
        rows = list(rows)
        df_followup_reason = pd.DataFrame(rows, columns=columns)
        return df_followup_reason

    def get_schedule_type(self):
        cursor = connection.cursor()
        parameters = (0, '', '', self.entity_gid, '')
        cursor.callproc('sp_FETScheduleType_Get', parameters)
        columns = [x[0] for x in cursor.description]
        rows = cursor.fetchall()
        rows = list(rows)
        df_schedule_type = pd.DataFrame(rows, columns=columns)
        return df_schedule_type

    # def get_url(self):
    #     cursor = connection.cursor()
    #     details = {'Employee_Gid': self.employee_gid, 'Menu_Link': self.action}
    #     user_details = {'Entity_Gid': self.entity_gid}
    #     parameters = ('CHECK_URL', 'MENU', json.dumps(details), json.dumps(user_details), self.create_by, '')
    #     cursor.callproc('sp_UMMenuData_Get', parameters)
    #     cursor.execute('select @_sp_UMMenuData_Get_5')
    #     sp_out_message = cursor.fetchone()
    #     return sp_out_message

    def get_mapped_customer(self):
        cursor = connection.cursor()
        parameters = (self.action, self.employee_gid, self.entity_gid)
        cursor.callproc('sp_Custemp_Get', parameters)
        columns = [x[0] for x in cursor.description]
        rows = cursor.fetchall()
        rows = list(rows)
        df_customer = pd.DataFrame(rows, columns=columns)
        return df_customer

    def get_product(self):
        cursor = connection.cursor()
        Parameters = (0, self.name, self.limit)
        cursor.callproc('sp_Product_Get', Parameters)
        columns = [d[0] for d in cursor.description]
        ldict = [dict(zip(columns, row)) for row in cursor.fetchall()]
        return ldict

    def get_qty(self):
        cursor = connection.cursor()
        parameters = (self.from_date, self.to_date, self.customer_gid, self.employee_gid, 30, self.entity_gid, '')
        cursor.callproc('sp_FETScheduleView_Get', parameters)
        columns = [x[0] for x in cursor.description]
        rows = cursor.fetchall()
        cursor.execute('select @_sp_FETScheduleView_Get_5')
        rows = list(rows)
        df_obj_add_schedul = pd.DataFrame(rows, columns=columns)
        dd = df_obj_add_schedul.loc[df_obj_add_schedul['Schedule_ref_gid'] > 0]
        return dd

    def get_schedul(self):
        cursor = connection.cursor()
        parameters = (self.from_date, self.to_date, self.customer_gid, self.employee_gid, 30, self.entity_gid, '')
        cursor.callproc('sp_FETScheduleView_Get', parameters)
        columns = [x[0] for x in cursor.description]
        rows = cursor.fetchall()
        cursor.execute('select @_sp_FETScheduleView_Get_5')
        rows = list(rows)
        df_obj_add_schedule = pd.DataFrame(rows, columns=columns)
        dd = df_obj_add_schedule.loc[df_obj_add_schedule['schedule_status'] == 'CLOSED']
        return dd

    def get_customer(self):
        cursor = connection.cursor()
        parameters = (self.customer_gid, '', '', self.jsonData, self.entity_gid, '')
        cursor.callproc('sp_Customer_Get', parameters)
        columns = [x[0] for x in cursor.description]
        rows = cursor.fetchall()
        rows = list(rows)
        df_customerddl = pd.DataFrame(rows, columns=columns)
        return df_customerddl

    def get_productcategory(self):
        cursor = connection.cursor()
        parameters = (0, '',)
        cursor.callproc('sp_ProductCategory_Get', parameters)
        columns = [x[0] for x in cursor.description]
        rows = cursor.fetchall()
        rows = list(rows)
        df_productcategoryddl = pd.DataFrame(rows, columns=columns)
        return df_productcategoryddl

    def get_producttype(self):
        cursor = connection.cursor()
        parameters = (self.productcat_gid,)
        cursor.callproc('sp_Prodcat_Get', parameters)
        columns = [x[0] for x in cursor.description]
        rows = cursor.fetchall()
        rows = list(rows)
        df_producttypeddl = pd.DataFrame(rows, columns=columns)
        return df_producttypeddl

    def get_sales_fav_product(self):
        cursor = connection.cursor()
        parameters = (self.customer_gid, self.product_type, self.entity_gid, '')
        cursor.callproc('sp_SalesFavProdt_Get', parameters)
        columns = [x[0] for x in cursor.description]
        rows = cursor.fetchall()
        rows = list(rows)
        df_sales_fav_pdct = pd.DataFrame(rows, columns=columns)
        dd = df_sales_fav_pdct.loc[df_sales_fav_pdct['fav'] == 'Y']
        return dd

    def get_outstanding_fet(self):  ### Check, Not in Use
        cursor = connection.cursor()
        parameters = (
        self.action, self.from_date, self.to_date, self.customer_gid, self.employee_gid, self.limit, self.entity_gid,
        '')
        cursor.callproc('sp_OutstandingHistory_Get', parameters)
        columns = [x[0] for x in cursor.description]
        rows = cursor.fetchall()
        rows = list(rows)
        df_sales_outstanding_fet = pd.DataFrame(rows, columns=columns)
        return df_sales_outstanding_fet

    def get_FEToutstanding_fet(self):
        cursor = connection.cursor()
        parameters = (self.action, self.from_date, self.to_date, self.customer_gid, self.employee_gid, self.limit, '')
        cursor.callproc('sp_FETOutstandingHistory_Get', parameters)
        columns = [x[0] for x in cursor.description]
        rows = cursor.fetchall()
        rows = list(rows)
        df_sales_outstanding_fet = pd.DataFrame(rows, columns=columns)
        return df_sales_outstanding_fet

    def get_sales_history_fet(self):
        cursor = connection.cursor()
        parameters = (
        self.from_date, self.to_date, self.customer_gid, self.employee_gid, self.limit, self.entity_gid, '')
        cursor.callproc('sp_SalesHistory_Get', parameters)
        columns = [x[0] for x in cursor.description]
        rows = cursor.fetchall()
        rows = list(rows)
        df_sales_history_fet = pd.DataFrame(rows, columns=columns)
        return df_sales_history_fet

    api_token = 'watchers'

    def get_collection_history_fet(self):
        # api_url_base = 'http://192.168.1.29/sally_api/api/Product/GetEmp'
        # api_url = api_url_base
        # parameters = {'ls_from_date': self.from_date, 'ls_to_date': self.to_date,
        #               'li_emp_gid': self.employee_gid, 'li_cust_gid': self.customer_gid}
        # import json
        # import requests
        #
        # response = requests.get(api_url, params=parameters)
        #
        # if response.status_code == 200:
        #     return json.loads(response.content.decode('utf-8'))
        #
        # else:
        #     return None

        cursor = connection.cursor()
        parameters = (self.action, self.from_date, self.to_date, self.employee_gid, self.customer_gid, '')
        cursor.callproc('sp_FETCollection_Get', parameters)
        columns = [x[0] for x in cursor.description]
        rows = cursor.fetchall()
        rows = list(rows)
        df_collection_fet = pd.DataFrame(rows, columns=columns)
        return df_collection_fet

    def get_schedule_view_fet(self):
        cursor = connection.cursor()
        parameters = (
        self.from_date, self.to_date, self.customer_gid, self.employee_gid, self.limit, self.entity_gid, '')
        cursor.callproc('sp_FETScheduleView_Get', parameters)
        columns = [x[0] for x in cursor.description]
        rows = cursor.fetchall()
        rows = list(rows)
        df_schedule_view_fet = pd.DataFrame(rows, columns=columns)
        return df_schedule_view_fet

    def set_schedule(self):
        cursor = connection.cursor()
        parameters = (self.action, self.type, self.sechedule_gid, self.date, self.customer_gid, self.employee_gid,
                      self.schedule_type_gid,
                      self.sch_remark, self.followup_reason_gid, self.schedule_ref_gid, self.ls_followup_date,
                      self.resechedule_date,
                      self.jsonData, self.jsonData_sec, self.entity_gid, self.create_by, '')
        cursor.callproc('sp_FETSchedule_Set', parameters)
        cursor.execute('select @_sp_FETSchedule_Set_16')
        output_msg = cursor.fetchone()
        return output_msg

    def set_service(self):
        cursor = connection.cursor()
        parameters = (
        'Insert', 0, self.date, self.customer_gid, self.product_gid, self.product_stockcode, self.invoice_no,
        self.invoice_date, self.remark, self.entity_gid, self.employee_gid, '')
        cursor.callproc('sp_Service_Set', parameters)
        cursor.execute('select @_sp_Service_Set_11')
        output_msg = cursor.fetchone()
        return output_msg

    def set_collection(self):
        cursor = connection.cursor()
        parameters = (
            self.action, self.type, self.collectionheader_gid, self.customer_gid, self.employee_gid, self.mode,
            self.amount, self.date,
            self.cheque_no,
            self.remark, json.dumps(self.jsonData),self.json_file, self.entity_gid, self.employee_gid, '')
        cursor.callproc('sp_Collection_Set', parameters)
        cursor.execute('select @_sp_Collection_Set_14')
        output_msg = cursor.fetchone()
        return output_msg

    def set_leadrequest(self):
        cursor = connection.cursor()
        parameters = (self.action, self.leadref_gid, self.customer_name, self.address1, self.mobile_no, '', self.reason,
                      self.status, self.entity_gid, self.employee_gid, '')
        cursor.callproc('sp_FETLeadsRequest_Set', parameters)
        cursor.execute('select @_sp_FETLeadsRequest_Set_10')
        output_msg = cursor.fetchone()
        return output_msg

    def get_leadrequest(self):
        cursor = connection.cursor()
        parameters = (self.leadref_gid, self.leadref_name, self.status, self.mobile_no, self.entity_gid, '')
        cursor.callproc('sp_FETLeadsRequest_Get', parameters)
        columns = [x[0] for x in cursor.description]
        rows = cursor.fetchall()
        rows = list(rows)
        df_producttypeddl = pd.DataFrame(rows, columns=columns)
        return df_producttypeddl

    def get_collection_amt(self):
        cursor = connection.cursor()
        json1 = json.dumps(self.jsonData)
        json2 = json.dumps(self.jsondata)
        parameters = (self.action,self.type,self.collectionheader_gid,self.name,self.date,json1,json2,'')
        cursor.callproc('sp_Collection_Get', parameters)
        columns = [x[0] for x in cursor.description]
        rows = cursor.fetchall()
        rows = list(rows)
        collection_amt = pd.DataFrame(rows, columns=columns)
        return collection_amt

    def get_bankdetails(self):
        cursor = connection.cursor()
        parameters = (self.entity_gid, '',)
        cursor.callproc('sp_CompanyBankDetails_Get', parameters)
        columns = [x[0] for x in cursor.description]
        rows = cursor.fetchall()
        rows = list(rows)
        bank_details = pd.DataFrame(rows, columns=columns)
        return bank_details

    def get_scheduleEdit(self):### Old One :: Used and will remove in Future
        cursor = connection.cursor()
        parameters = (self.schedule_gid, self.entity_gid, '')
        cursor.callproc('sp_ScheduleDetailsSPs_Get', parameters)
        columns = [x[0] for x in cursor.description]
        rows = cursor.fetchall()
        rows = list(rows)
        df_schedule = pd.DataFrame(rows, columns=columns)
        return df_schedule

    def get_schedule_review(self):### Added Newly
        cursor = connection.cursor()
        parameters = (self.schedule_gid, self.entity_gid, '')
        cursor.callproc('sp_ScheduleDetailsSPs_Get', parameters)
        columns = [x[0] for x in cursor.description]
        rows = cursor.fetchall()
        rows = list(rows)
        cursor.execute('select @_sp_ScheduleDetailsSPs_Get_2')
        out_put = cursor.fetchone()
        df_schedule = pd.DataFrame(rows, columns=columns)
        return {"DATA":df_schedule,"MESSAGE":out_put[0]}

    def get_drctEdit(self):
        cursor = connection.cursor()
        parameters = (self.action, self.so_header_gid, self.schedule_gid, self.entity_gid, '')
        cursor.callproc('sp_SalesOrderFET_Get', parameters)
        columns = [x[0] for x in cursor.description]
        rows = cursor.fetchall()
        rows = list(rows)
        df_schedule = pd.DataFrame(rows, columns=columns)
        return df_schedule

    def getHierarchy_employeeList(self):
        cursor = connection.cursor()
        Parameters = (self.employee_gid, self.employee_name, self.cluster_gid, 'HIERARCHY', 'Y', self.jsonData, '')
        cursor.callproc('sp_Employee_Get', Parameters)
        columns = [x[0] for x in cursor.description]
        rows = cursor.fetchall()
        rows = list(rows)
        df_add = pd.DataFrame(rows, columns=columns)
        return df_add

    def getRoute(self):
        cursor = connection.cursor()
        Parameters = (
        self.action, self.route_gid, self.route_name, self.route_code, self.json_employee_gid, self.json_cluster_gid,
        self.entity_gid, '')
        cursor.callproc('sp_Route_Get', Parameters)
        columns = [x[0] for x in cursor.description]
        rows = cursor.fetchall()
        rows = list(rows)
        df_add = pd.DataFrame(rows, columns=columns)
        return df_add

    def getcustomer(self):
        cursor = connection.cursor()
        Parameters = (self.action, self.jsonData, self.jsondata, '')
        cursor.callproc('sp_CustomerFilter_Get', Parameters)
        columns = [x[0] for x in cursor.description]
        rows = cursor.fetchall()
        rows = list(rows)
        df_add = pd.DataFrame(rows, columns=columns)
        return df_add

    def get_stock(self):
        cursor = connection.cursor()
        parameters = (
        self.action, self.type, self.from_date, self.to_date, self.customer_gid, self.date, self.entity_gid, '')
        cursor.callproc('sp_FETStock_Get', parameters)
        columns = [x[0] for x in cursor.description]
        rows = cursor.fetchall()
        rows = list(rows)
        df_add = pd.DataFrame(rows, columns=columns)
        return df_add

    def set_stock(self):
        cursor = connection.cursor()
        parameters = (
        self.action, self.employee_gid, self.customer_gid, self.date, self.stckdet, self.entity_gid, self.employee_gid,
        '')
        cursor.callproc('sp_FETStock_Set', parameters)
        cursor.execute('select @_sp_FETStock_Set_7')
        output_msg = cursor.fetchone()
        return output_msg

    def set_saleaprve(self):
        cursor = connection.cursor()
        parameters = (self.action, self.soheader_gid, self.remark, self.entity_gid, self.create_by, '')
        cursor.callproc('sp_SalesOrder_Approval_Set', parameters)
        cursor.execute('select @_sp_SalesOrder_Approval_Set_5')
        output_msg = cursor.fetchone()
        return output_msg

    def get_attendance_mis(self):
        cursor = connection.cursor()
        parameters = (self.type,self.sub_type,self.jsonData,self.json_classification,'')
        cursor.callproc('sp_OutstandingCustomer_Get',parameters)
        columns = [x[0] for x in cursor.description]
        rows = cursor.fetchall()
        cursor.execute('select @_sp_OutstandingCustomer_Get_4')
        out_put = cursor.fetchone()
        rows = list(rows)
        df_preschedule = pd.DataFrame(rows, columns=columns)
        return df_preschedule

    def set_schedulereview(self):
        cursor = connection.cursor()
        parameters = (self.action, self.jsonData, self.entity_gid, self.create_by, '')
        cursor.callproc('sp_FETSchedulereview_Set', parameters)
        cursor.execute('select @_sp_FETSchedulereview_Set_4')
        output_msg = cursor.fetchone()
        return output_msg

    def set_check_in_check_out(self):
        cursor = connection.cursor()
        parameters = (self.action, self.type, self.jsonData, self.jsondata,self.create_by, '')
        cursor.callproc('sp_CheckinCheckout_Set', parameters)
        cursor.execute('select @_sp_CheckinCheckout_Set_5')
        output_msg = cursor.fetchone()
        return {"MESSAGE": output_msg[0]}

    def get_check_in_check_out(self):
        cursor = connection.cursor()
        parameters = (self.action, self.type, self.jsonData, self.json_classification, '')
        cursor.callproc('sp_CheckinCheckout_Get', parameters)
        columns = [x[0] for x in cursor.description]
        rows = cursor.fetchall()
        cursor.execute('select @_sp_CheckinCheckout_Get_4')
        out_put = cursor.fetchone()
        rows = list(rows)
        df_schedule_cust = pd.DataFrame(rows, columns=columns)
        return {"DATA": df_schedule_cust, "MESSAGE": out_put[0]}

    def get_schedule_customer(self):
        cursor = connection.cursor()
        parameters = (self.action, self.type, self.jsondata,self.json_classification, '')
        cursor.callproc('sp_FETScheduleAPI_Get', parameters)
        columns = [x[0] for x in cursor.description]
        rows = cursor.fetchall()
        cursor.execute('select @_sp_FETScheduleAPI_Get_4')
        out_put = cursor.fetchone()
        rows = list(rows)
        df_schedule_cust = pd.DataFrame(rows, columns=columns)
        return {"DATA": df_schedule_cust, "MESSAGE": out_put[0]}

    def get_reportexcel(self):
        cursor = connection.cursor()
        fulljson = self.jsondata
        jsondata = json.dumps(fulljson)
        parameters = (self.action, self.type, jsondata, 1, '')
        cursor.callproc('sp_FETPerformance_Get', parameters)
        columns = [x[0] for x in cursor.description]
        rows = cursor.fetchall()
        cursor.execute('select @_sp_FETPerformance_Get_4')
        out_put = cursor.fetchone()
        rows = list(rows)
        df_preschedule = pd.DataFrame(rows, columns=columns)
        return df_preschedule

    def set_schedule_update(self):
        cursor = connection.cursor()
        parameters = (
        self.type, self.sub_type, self.jsondata, self.schedule_name, self.schedule_gid, self.schedule_date,
        self.customer_gid,
        self.employee_gid, self.schedule_type_gid, self.remark, self.followup_reason_gid, self.schedule_ref_gid,
        self.ls_followup_date, self.resechedule_date, self.jsondata, self.jsondata, self.entity_gid, self.create_by, ''
        )
        cursor.callproc('sp_FETScheduleSPS_Set', parameters)
        cursor.execute('select @_sp_FETScheduleSPS_Set_18')
        output_message = cursor.fetchone()
        return output_message

    def get_hierarchy(self):
        cursor = connection.cursor()
        function = "select fn_HierarchyAction(%s,%s,%s,%s,%s)"
        parameters = (self.group,self.type,self.employee_gid,self.create_by,self.entity_gid)
        cursor.execute(function,parameters)
        rows = cursor.fetchone()
        return rows
