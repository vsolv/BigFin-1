from django.db import connection
import pandas as pd
import json
from Bigflow.Transaction.Model import mFET
from Bigflow.Master.Model import mVariable


class Sales_Model(mFET.FET_model,mVariable.variable):


    def get_tasummary(self):
        cursor = connection.cursor()
        parameters = (
        self.action, self.date, self.customer_gid, self.employee_gid, self.limit, self.jsonData, self.jsondata, '')
        cursor.callproc('sp_SalesOrder_Get', parameters)
        columns = [x[0] for x in cursor.description]
        rows = cursor.fetchall()
        rows = list(rows)
        df_schedule_view_fet = pd.DataFrame(rows, columns=columns)
        return df_schedule_view_fet

    def set_sales_order(self):
        cursor = connection.cursor()
        jsondata= self.sodetails
        sodetails = json.dumps(jsondata)
        parameters = (self.action, self.soheader_gid, self.detail_gid, self.customer_gid, self.So_Header_date, self.employee_gid, self.Channel, '', 0, 0, sodetails,
                      self.entity_gid,self.create_by,'')
        cursor.callproc('sp_SalesOrder_Set',parameters)
        cursor.execute('select @_sp_SalesOrder_Set_13')
        output_msg = cursor.fetchone()
        return output_msg

    def get_sales_order(self):
        cursor = connection.cursor()
        parameters = (self.action,self.date, self.customer_gid, self.employee_gid, self.limit,self.jsonData,self.jsondata, '')
        cursor.callproc('sp_SalesOrder_Get',parameters)
        columns = [x[0] for x in cursor.description]
        rows = cursor.fetchall()
        rows = list(rows)
        df_schedule_view_fet = pd.DataFrame(rows, columns=columns)
        return df_schedule_view_fet

    def get_salesquery_summary(self):
        cursor = connection.cursor()
        parameters = (self.jsonData,self.json_classification,'')
        cursor.callproc('sp_Sales_Get',parameters)
        columns = [x[0] for x in cursor.description]
        rows = cursor.fetchall()
        cursor.execute('select @_sp_Sales_Get_2')
        outmsg_sp = cursor.fetchone()
        rows = list(rows)
        df_sales = pd.DataFrame(rows,columns=columns)
        return {"DATA":df_sales,"MESSAGE":outmsg_sp[0]}

    def get_salesquery_summaryProduct(self):
        cursor = connection.cursor()
        parameters = (self.jsonData,self.json_classification,'')
        cursor.callproc('sp_SalesProduct_Get',parameters)
        columns = [x[0] for x in cursor.description]
        rows = cursor.fetchall()
        cursor.execute('select @_sp_SalesProduct_Get_2')
        outmsg_sp = cursor.fetchone()
        rows = list(rows)
        df_sales = pd.DataFrame(rows,columns=columns)
        return {"DATA":df_sales,"MESSAGE":outmsg_sp[0]}

    def get_salesquery_summaryCollection(self):
        cursor = connection.cursor()
        parameters = (self.action,self.type,"0","","",self.jsonData,self.json_classification,'')
        cursor.callproc('sp_Collection_Get',parameters)
        columns = [x[0] for x in cursor.description]
        rows = cursor.fetchall()
        cursor.execute('select @_sp_Collection_Get_7')
        outmsg_sp = cursor.fetchone()
        rows = list(rows)
        df_sales = pd.DataFrame(rows,columns=columns)
        return {"DATA":df_sales,"MESSAGE":outmsg_sp[0]}

    def get_salesquery_summaryCollectionStatus(self):
        cursor = connection.cursor()
        parameters = (self.action, self.type,  self.jsonData, self.json_classification, '')
        cursor.callproc('sp_Collectionstatus_Get', parameters)
        columns = [x[0] for x in cursor.description]
        rows = cursor.fetchall()
        cursor.execute('select @_sp_Collectionstatus_Get_4')
        outmsg_sp = cursor.fetchone()
        rows = list(rows)
        df_sales = pd.DataFrame(rows, columns=columns)
        return {"DATA": df_sales, "MESSAGE": outmsg_sp[0]}

    def get_salesquery_summaryOutstanding(self):
        cursor = connection.cursor()
        parameters = (self.type,self.sub_type,self.jsonData,self.json_classification,'')
        cursor.callproc('sp_OutstandingCustomer_Get',parameters)
        columns = [x[0] for x in cursor.description]
        rows = cursor.fetchall()
        cursor.execute('select @_sp_OutstandingCustomer_Get_4')
        outmsg_sp = cursor.fetchone()
        rows = list(rows)
        df_sales = pd.DataFrame(rows,columns=columns)
        return {"DATA":df_sales,"MESSAGE":outmsg_sp[0]}

    def get_salessetapi(self):
        api_url_base = 'http://192.168.1.29/sally_api/api/Purchase/post_sale'
        api_url = api_url_base
        objData1 = self.jsonData
        sales = objData1['parms']
        del objData1['parms']
        objData1['parms'] = sales
        objData = {'sales': sales}
        import json
        import requests
        # objData = json.dumps(objData1)
        response = requests.post(api_url, json=objData)

        if response.status_code == 200:
            return 'SUCCESS'
        else:
            return None

    def set_salesplanning(self):
        cursor = connection.cursor()
        parameters = (
        self.action, self.type, self.header, self.detail, self.Classification, self.sales ,self.entity_gid, '')
        cursor.callproc('sp_SalesPlanningSPS_set', parameters)
        cursor.execute('select @_sp_SalesPlanningSPS_set_7')
        output_msg = cursor.fetchone()
        return output_msg

    def get_salesplanning(self):
        cursor = connection.cursor()
        parameters = (self.type,self.filter_json,self.customer_gid,self.year, self.product_type_gid, self.product_gid, self.employee_gid,self.Classification, '')
        cursor.callproc('sp_SalesPlanDetails_get',parameters)
        columns = [x[0] for x in cursor.description]
        rows = cursor.fetchall()
        rows = list(rows)
        df_schedule_view_fet = pd.DataFrame(rows, columns=columns)
        if self.type == 'SUMMARY':
            df_schedule_view_fet['Sales_Plan_Details'] = df_schedule_view_fet['Sales_Plan_Details'].apply(json.loads)
        return df_schedule_view_fet

    def get_salesplanningmis(self):
        cursor = connection.cursor()
        parameters = (self.customer_gid,self.from_date,self.to_date,self.employee_gid,self.product_gid,self.type,'')
        cursor.callproc('sp_SalesPlanDetailsMIS_get',parameters)
        columns = [x[0] for x in cursor.description ]
        rows = cursor.fetchall()
        rows = list(rows)
        output = pd.DataFrame(rows,columns=columns)
        return output

    def get_salesplanning_historyget(self):
        cursor = connection.cursor()
        parameters = (self.from_date, self.to_date, self.customer_gid, self.employee_gid,  self.limit,self.entity_gid, '')
        cursor.callproc('sp_SalesHistory_Get', parameters)
        columns = [x[0] for x in cursor.description]
        rows = cursor.fetchall()
        rows = list(rows)
        output = pd.DataFrame(rows, columns=columns)
        return output

    def get_salesplanning_reportget(self):
        cursor = connection.cursor()
        parameters = (self.customer_gid, self.from_date, self.to_date, self.employee_gid,  self.product_gid,self.searchtype, '')
        cursor.callproc('sp_SalesHistoryRPT_get', parameters)
        columns = [x[0] for x in cursor.description]
        rows = cursor.fetchall()
        rows = list(rows)
        output = pd.DataFrame(rows, columns=columns)
        return output
    #### Masters ###############
    def get_dealer_price(self):
        cursor = connection.cursor()
        parameters = (self.type, self.sub_type, self.jsonData,self.json_classification,self.create_by, '')
        cursor.callproc('sp_DealerPrice_Get', parameters)
        columns = [x[0] for x in cursor.description]
        rows = cursor.fetchall()
        rows = list(rows)
        df_dp = pd.DataFrame(rows, columns=columns)
        cursor.execute('select @_sp_DealerPrice_Get_5')
        sp_out_message = cursor.fetchone()

        return {"DATA":df_dp,"MESSAGE":sp_out_message[0]}


    def set_dealer_price(self):
         cursor = connection.cursor()
         parameters = (self.action, self.type, self.jsonData, self.json_classification, self.create_by, '')
         cursor.callproc('sp_DealerPrice_Set', parameters)
         cursor.execute('select @_sp_DealerPrice_Set_5')
         sp_out_message = cursor.fetchone()
         return  {"MESSAGE":sp_out_message[0]}

    def get_rate_card(self):
        cursor = connection.cursor()
        parameters = (self.type, self.sub_type, self.jsonData,self.json_classification,self.create_by, '')
        cursor.callproc('sp_SalesRate_Get', parameters)
        columns = [x[0] for x in cursor.description]
        rows = cursor.fetchall()
        rows = list(rows)
        df_dp = pd.DataFrame(rows, columns=columns)
        cursor.execute('select @_sp_SalesRate_Get_5')
        sp_out_message = cursor.fetchone()
        return {"DATA":df_dp,"MESSAGE":sp_out_message[0]}

    def set_rate_card(self):
        cursor = connection.cursor()
        parameters = (self.action, self.type, self.jsonData, self.json_classification, self.create_by, '')
        cursor.callproc('sp_SalesRate_Set', parameters)
        cursor.execute('select @_sp_SalesRate_Set_5')
        sp_out_message = cursor.fetchone()
        return {"MESSAGE": sp_out_message[0]}

    def set_invprocess(self):
        cursor = connection.cursor()
        parameters =(self.action,self.type,self.jsonData,self.jsondata,self.json_rate,self.is_commit,self.json_classification,self.create_by,'')
        cursor.callproc('sp_SOInvoiceProcess_Set',parameters)
        cursor.execute('select @_sp_SOInvoiceProcess_Set_8')
        sp_out_message=cursor.fetchone()
        return {"MESSAGE": sp_out_message[0]}

    def get_invprocess(self):
        cursor = connection.cursor()
        parameters = (self.type, self.sub_type, self.jsonData,self.json_classification, '')
        cursor.callproc('sp_SOInvoiceProcess_Get', parameters)
        columns = [x[0] for x in cursor.description]
        rows = cursor.fetchall()
        rows = list(rows)
        df_dp = pd.DataFrame(rows, columns=columns)
        cursor.execute('select @_sp_SOInvoiceProcess_Get_4')
        sp_out_message = cursor.fetchone()
        return {"DATA":df_dp,"MESSAGE":sp_out_message[0]}


    def get_INV_Dispatch(self):
        cursor = connection.cursor()
        parameters = (self.type, self.sub_type, self.jsonData,self.json_classification,self.create_by, '')
        cursor.callproc('sp_SalesInvoice_Get', parameters)
        columns = [x[0] for x in cursor.description]
        rows = cursor.fetchall()
        rows = list(rows)
        df_dp = pd.DataFrame(rows, columns=columns)
        cursor.execute('select @_sp_SalesInvoice_Get_5')
        sp_out_message = cursor.fetchone()
        return {"DATA":df_dp,"MESSAGE":sp_out_message[0]}

    def get_total_sales(self):
       cursor=connection.cursor()
       parameters = (self.type, self.sub_type, self.jsonData, self.json_classification, '')
       cursor.callproc('sp_Report_Customer_Performance',parameters)
       columns = [x[0] for x in cursor.description]
       rows = cursor.fetchall()
       rows = list(rows)
       df_dp = pd.DataFrame(rows, columns=columns)
       cursor.execute('select @_sp_Report_Customer_Performance_4')
       sp_out_message = cursor.fetchone()
       return {"DATA": df_dp, "MESSAGE": sp_out_message[0]}

    def get_sales(self):
        cursor = connection.cursor()
        parameters = (self.type, self.sub_type, self.jsonData, self.json_classification, '')
        cursor.callproc('sp_Report_Customer_Performance', parameters)
        columns = [x[0] for x in cursor.description]
        rows = cursor.fetchall()
        rows = list(rows)
        df_dp = pd.DataFrame(rows, columns=columns)
        return df_dp

    def get_Dispatch_Process(self):
        cursor = connection.cursor()
        parameters = (self.type, self.sub_type, self.jsonData,self.json_classification, '')
        cursor.callproc('sp_DispatchProcess_Get', parameters)
        columns = [x[0] for x in cursor.description]
        rows = cursor.fetchall()
        rows = list(rows)
        df_dp = pd.DataFrame(rows, columns=columns)
        if self.type == 'LABEL_PRINT_SALES' and self.sub_type == 'SALES':
            df_dp['Details'] = df_dp['Details'].apply(json.loads)
        cursor.execute('select @_sp_DispatchProcess_Get_4')
        sp_out_message = cursor.fetchone()
        return {"DATA":df_dp,"MESSAGE":sp_out_message[0]}

    def set_Dispatch_Process(self):
        cursor = connection.cursor()
        parameters =(self.action,self.type,self.sub_type,self.jsonData,self.jsondata,self.json_classification,self.create_by,'')
        cursor.callproc('sp_DispatchProcess_Set',parameters)
        if self.type == 'LABEL_PRINT' and self.sub_type == 'SALES' and cursor.description != None:
            columns = [x[0] for x in cursor.description]
            rows = cursor.fetchall()
            rows = list(rows)
            df_dp = pd.DataFrame(rows, columns=columns)
            df_dp['Master_Carton_Details'] = df_dp['Master_Carton_Details'].apply(json.loads)
            cursor.execute('select @_sp_DispatchProcess_Set_7')
            sp_out_message = cursor.fetchone()
            return {"DATA": df_dp, "MESSAGE": sp_out_message[0]}
        else:
            cursor.execute('select @_sp_DispatchProcess_Set_7')
            sp_out_message=cursor.fetchone()
            return {"MESSAGE": sp_out_message[0]}