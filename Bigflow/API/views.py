from tempfile import NamedTemporaryFile

import boto3
from boto3.dynamodb.conditions import Key
from rest_framework.views import APIView
from rest_framework.response import Response
import json
from Bigflow.Master import views as MasterViews
from Bigflow.Master.Model import mMasters
from Bigflow.Transaction import views
from Bigflow.Transaction.Model import mFET, mSales
from Bigflow.Collection.Model import mCollection
from Bigflow.AP.model import mAP
from Bigflow.UserMgmt import views as UM_View
# from Bigflow.Core import class1
from Bigflow.inward.model import mInvoice
import pandas as pd
from django.http import HttpResponse, request
from django.conf import settings
import Bigflow
import Bigflow.Core.models as common
import Bigflow.class1 as class1

mCore = Bigflow.mCore
import base64
from Bigflow.settings import BASE_DIR, MEDIA_URL
from rest_framework import authentication, permissions
import datetime
import time
import os, shutil
import requests
from Bigflow.Core.models import Excelfilename
from Bigflow.Core.models import decrpt as decry_data

class login(APIView):

    def get(self, request):
        obj_login = mMasters.Masters
        jsondata = json.loads(request.body.decode('utf-8')).get('ls_json')

        user_name = jsondata.get('parms').get('username')
        user_password = jsondata.get('parms').get('password')

        out_message = mCore.get_login(user_name, user_password)
        return Response(out_message)

    def post(self, request):
        # jsondata = json.loads(request.body.decode('utf-8')).get('ls_json')
        jsondata = json.loads(request.body.decode('utf-8'))
        user_name = jsondata.get('username')
        user_password = jsondata.get('password')

        # serializer = loginSerializer(data=request.data)
        #
        #
        # if serializer.is_valid(raise_exception=True):
        #     new_data = serializer.data
        mCorez = mCore.login()
        mCorez.code = user_name
        mCorez.password = user_password
        out_message = mCorez.get_login()

        if out_message[1][0] == 'SUCCESS':
            ld_dict = {"DATA": out_message[0][0], "MESSAGE": out_message[1][0]}
        elif out_message[1][0] == 'FAIL':
            ld_dict = {"MESSAGE": out_message[1][0]}

        return Response(ld_dict)


class LoginBigflow(APIView):
    def post(self, request):
        try:
            if self.request.query_params.get("TYPE") == 'LOGIN_AD':
                jsondata = json.loads(request.body.decode('utf-8'))
                user_name = jsondata.get('username')
                del jsondata['TYPE']
                client_api = common.clientapi()
                headers = {"Content-Type": "application/x-www-form-urlencoded", "APIKey": common.ADToken()}
                resp = requests.post("" + client_api + "/next/v1/mw/internal/login", params="", data=jsondata, headers=headers, verify=False)
                response = json.loads(resp.content)
                response_msg = response.get("out_msg")
                dict = json.loads(response_msg)
                msg = dict["ErrorCode"]
                if msg == '00' or msg == '0' :
                    out_message = mCore.get_login(user_name, '')
                    ld_dict = {}
                    if out_message[1][0] == 'SUCCESS':
                        ld_dict = {"DATA": out_message[0][0], "MESSAGE": out_message[1][0]}
                        ld_dict = json.dumps(ld_dict)
                        ld_dict = json.loads(ld_dict)
                    elif out_message[1][0] == 'FAIL':
                        ld_dict = {"MESSAGE": out_message[1][0]}
                    return Response(ld_dict)

                else:
                    return  Response({"MESSAGE":"FAIL","DATA":msg})
            else:
                return Response({"MESSAGE": "ERROR_OCCURED", "DATA": ""})
        except Exception as e:
            return Response({"MESSAGE": "ERROR_OCCURED", "DATA": str(e)})


class UM_RightsMenu(APIView):

    def get(self, request):
        obj_menu = class1.login
        obj_menu.employee_gid = self.request.query_params.get("emp_gid")
        obj_menu.char = self.request.query_params.get("Is_Mobile")
        # Validation
        out_message = class1.menulist(obj_menu.employee_gid, obj_menu.char)
        if out_message[1][0] == 'FOUND':
            ld_dict = {"DATA": out_message[0], "MESSAGE": out_message[1][0]}
        elif out_message[1][0] == 'NOT_FOUND':
            ld_dict = {"MESSAGE": out_message[1][0]}
        return Response(ld_dict)


class FET_Schedule(APIView):
    # Used to GET the Day's Schedule Data.
    def post(self, request):
        try:
            obj_schedule = mFET.FET_model()
            obj_schedule.employee_gid = self.request.query_params.get("emp_gid")
            obj_schedule.action = self.request.query_params.get("action")
            obj_schedule.date = self.request.query_params.get("date")
            obj_schedule.create_by = self.request.query_params.get("emp_gid")

            jsondata = json.loads(request.body.decode('utf-8'))

            obj_schedule.jsonData = json.dumps(jsondata.get("Classification"))

            ld_schedule = obj_schedule.get_preschedule_fet()
            json_data = ld_schedule.get("DATA").to_json(orient='records')

            if ld_schedule.get("MESSAGE") == 'FOUND':
                ld_dict = {"DATA": json.loads(json_data), "MESSAGE": "FOUND"}
            elif ld_schedule.get("MESSAGE") == 'NOT_FOUND':
                ld_dict = {"DATA": json.loads(json_data), "MESSAGE": ld_schedule.get("MESSAGE")}
            else:
                ld_dict = {"MESSAGE": 'ERROR_OCCURED.' + ld_schedule.get("MESSAGE")}
            return Response(ld_dict)
        except Exception as e:
            return Response({"MESSAGE": "ERROR_OCCURED", "DATA": str(e)})


class FET_ScheduleHistory(APIView):
    def get(self, request):
        try:
            obj_history = mFET.FET_model()
            obj_history.from_date = ''
            obj_history.to_date = ''
            obj_history.customer_gid = self.request.query_params.get("Customer_Gid")
            obj_history.employee_gid = self.request.query_params.get("Employee_Gid")
            obj_history.limit = self.request.query_params.get("Limit")
            obj_history.entity_gid = self.request.query_params.get("Entity_Gid")

            out_message = obj_history.get_schedule_view_fet()
            if out_message.empty == False:
                json_data = json.loads(out_message.to_json(orient='records'))
                return Response({"MESSAGE": "FOUND", "DATA": json_data})
            else:
                return Response({"MESSAGE": "NOT_FOUND"})

        except Exception as e:
            return Response({"MESSAGE": "ERROR_OCCURED", "DATA": str(e)})


class FET_ReviewProcess(APIView):
    def post(self, request):
        global lst_outstanding
        try:
            if self.request.query_params.get("Group"):
                obj_sales = mFET.FET_model()
                obj_sales.schedule_gid = self.request.query_params.get("Schedule_Gid")
                obj_sales.entity_gid = self.request.query_params.get("Entity_Gid")
                # For Getting The Sale Details
                ld_out_data = obj_sales.get_schedule_review()
                if ld_out_data.get("MESSAGE") == 'FOUND':
                    lst_out_sales = json.loads(ld_out_data.get("DATA").to_json(orient='records'))
                    if len(lst_out_sales) > 0:
                        obj_sales.customer_gid = lst_out_sales[0].get("soheader_customer_gid")
                    else:
                        return Response({"MESSAGE": "NOT_FOUND"})
                        # Get The Outstanding Details.
                    obj_outstanding = mSales.Sales_Model()
                    jsondata = json.loads(request.body.decode('utf-8'))
                    obj_outstanding.type = 'OUTSTANDING_POSITION'
                    obj_outstanding.sub_type = 'FET_REVIEW'
                    obj_outstanding.jsonData = json.dumps({"Customer_Gid": obj_sales.customer_gid})
                    obj_outstanding.json_classification = json.dumps(jsondata.get('Params').get("CLASSIFICATION"))
                    ld_out_outstanding = obj_outstanding.get_salesquery_summaryOutstanding()
                    if ld_out_outstanding.get("MESSAGE") == 'FOUND':
                        lst_outstanding = json.loads(ld_out_outstanding.get("DATA").to_json(orient='records'))
                    else:
                        return Response({"MESSAGE": "NOT_FOUND"})
                    ### get The Pending POD Details.
                    obj_outstanding.type = "SALES_FET"
                    obj_outstanding.sub_type = "PENDING_POD"
                    obj_outstanding.jsonData = json.dumps({"Customer_Gid": obj_sales.customer_gid})
                    obj_outstanding.json_classification = json.dumps(jsondata.get('Params').get('CLASSIFICATION'))
                    obj_outstanding.create_by = 0
                    ld_out_message = obj_outstanding.get_INV_Dispatch()
                    if ld_out_message.get("MESSAGE") == 'FOUND':
                        lst_pod = json.loads(ld_out_message.get("DATA").to_json(orient='records'))
                    else:
                        return Response({"MESSAGE": "NOT_FOUND"})
                    #### ALL Data.
                    ld_alldata = {"SALES_DATA": lst_out_sales, "OUTSTANDING_POSITION": lst_outstanding,
                                  "SALES_POD": lst_pod}

                    return Response({"MESSAGE": "FOUND", "DATA": ld_alldata})


                elif ld_out_data.get("MESSAGE") == 'NOT_FOUND':
                    return Response({"MESSAGE": "NOT_FOUND"})


        except Exception as e:
            return Response({"MESSAGE": "ERROR_OCCURED", "DATA": str(e)})


class TEST(APIView):
    def post(self, request):
        try:
            taxdtl = views
            jsondata = json.loads(request.body.decode('utf-8'))
            request.session['Entity_gid'] = 1
            lj_sales_fav_pdct = taxdtl.sales_fav_product(request)
            test = lj_sales_fav_pdct.content
            return Response(json.loads(test))
        except:
            return Response({"MESSAGE": "ERROR_OCCURED"})


class FET_Customer_Filter(APIView):  # Client TO DO
    def get(self, request):
        try:
            obj_customer = views
            request.session['Entity_gid'] = self.request.query_params.get("Entity_gid")
            request.session['Emp_gid'] = self.request.query_params.get("Emp_gid")
            request.session['date'] = self.request.query_params.get("date")
            lj_customer_filter = obj_customer.getCustomerFilterlist(request)
            lj_output = lj_customer_filter.content.decode('utf-8')
            return Response({"MESSAGE": "FOUND", "DATA": json.loads(lj_output)})
        except Exception as e:
            return Response({"MESSAGE": "NOT_FOUND", "DATA": str(e)})


class Customer_Mapped(APIView):
    # authentication_classes = (authentication.TokenAuthentication,)
    # permission_classes = (permissions.IsAdminUser,)

    def get(self, request):
        try:
            obj_customer = mFET.FET_model()
            obj_customer.action = self.request.query_params.get("action")
            obj_customer.employee_gid = decry_data(self.request.query_params.get("emp_gid"))
            obj_customer.entity_gid = decry_data(self.request.query_params.get("Entity_gid"))
            out_message = obj_customer.get_mapped_customer()
            if out_message.empty == False:
                jdata = out_message.to_json(orient='records')
                ld_cust = {"DATA": json.loads(jdata), "MESSAGE": "FOUND"}
            else:
                ld_cust = {"MESSAGE": "NOT_FOUND"}
            return Response(ld_cust)
        except:
            return Response({"MESSAGE": "ERROR_OCCURED"})


class FET_Schedule_Set(APIView):
    def post(self, request):
        try:
            obj_schedule = views
            request.session['Entity_gid'] = self.request.query_params.get("Entity_gid")
            request.session['Emp_gid'] = self.request.query_params.get("Emp_gid")
            lj_out_message = obj_schedule.add_schdle(request)

            out_message = json.loads(json.loads(json.dumps(lj_out_message.content.decode('utf-8'))))
            # Two Loads to Convert the Actual

            lscheck = out_message[0]

            if lscheck.isdigit() or lscheck == 'SUCCESS':
                return Response({"MESSAGE": "SUCCESS", "DATA": out_message})
            else:
                return Response({"MESSAGE": "FAIL", "DATA": out_message})

        except Exception as e:
            return Response({"MESSAGE": "Error Occured"})


class FET_Schedule_Update(APIView):
    def post(self, request):
        obj_schedule = mFET.FET_model()
        obj_schedule.action = self.request.query_params.get("Type")
        if obj_schedule.action == 'SCHEDULE':
            obj_schedule.type = obj_schedule.action
            obj_schedule.sub_type = self.request.query_params.get("Sub_Type")
            jsondata = json.loads(request.body.decode('utf-8')).get('PARMS').get('Schedule_Update')
            obj_schedule.customer_gid = jsondata.get('Cust_Gid')
            obj_schedule.employee_gid = jsondata.get('Emp_Gid')
            obj_schedule.schedule_name = jsondata.get('ScheduleType_Name')
            obj_schedule.followup_reason_gid = jsondata.get('FollowUpReason_Gid')
            obj_schedule.ls_followup_date = jsondata.get('FollowUp_Date')
            obj_schedule.schedule_ref_gid = jsondata.get('Ref_Gid')
            obj_schedule.create_by = jsondata.get('Create_By')
            obj_schedule.remark = jsondata.get('Remark')

            # Validations.
            if obj_schedule.schedule_ref_gid != 0 and obj_schedule.ls_followup_date != '':
                return Response(
                    {"MESSAGE": "Error", "DATA": "Incorrect Parameters,Can't Update Ref gid and Followup Date."})

            out_message = obj_schedule.set_schedule_update()

            if out_message[0] == 'SUCCESS':
                return Response({"MESSAGE": "SUCCESS"})
            else:
                return Response({"MESSAGE": "FAIL", "DATA": out_message})


class FET_SalesOrder(APIView):
    def post(self, request):
        try:
            obj_sales = views
            request.session['Entity_gid'] = self.request.query_params.get("Entity_gid")
            request.session['Emp_gid'] = self.request.query_params.get("Emp_gid")
            request.session['date'] = self.request.query_params.get("Date")
            lj_out_message = obj_sales.sales_order_set(request)
            lj_out_message = json.loads(lj_out_message.content.decode('utf-8'))

            if lj_out_message == 'SUCCESS' or lj_out_message.isdigit:
                return Response({"MESSAGE": "SUCCESS", "DATA": lj_out_message})
            else:
                return Response({"MESSAGE": "FAIL", "DATA": lj_out_message})
        except Exception as e:
            return Response({"MESSAGE": "ERROR_OCCURED", "DATA": str(e)})


# To Get the Sales Product from a Sales Summary
class FET_SalesOrder_Get(APIView):
    def get(self, request):
        try:
            obj_sales = mFET.FET_model()
            obj_sales.so_header_gid = self.request.query_params.get("SO_Header_gid")
            obj_sales.entity_gid = self.request.query_params.get(("Entity_gid"))
            obj_sales.action = self.request.query_params.get("Action")
            obj_sales.schedule_gid = 0
            ldf_sales = obj_sales.get_drctEdit()

            if ldf_sales.empty == False:

                lj_data = json.loads(ldf_sales.to_json(orient='records'))

                return Response({"MESSAGE": "FOUND", "DATA": lj_data})

            elif ldf_sales.empty == True:
                return Response({"MESSAGE": "NOT_FOUND"})

        except Exception as e:
            return Response({"MESSAGE": "ERROR_OCCURED", "DATA": str(e)})


class Product_Sales(APIView):
    def get(self, request):
        obj_product = mFET.FET_model()
        obj_product.name = self.request.query_params.get("Product_Name")
        obj_product.limit = self.request.query_params.get("Limit")
        ld_product = obj_product.get_product()
        if len(ld_product) != 0:
            ld_product = json.dumps(ld_product)
            return Response({"MESSAGE": "FOUND", "DATA": json.loads(ld_product)})
        else:
            return Response({"MESSAGE": "NOT_FOUND", "DATA": ''})


class Product_Sales_Favourite(APIView):
    def get(self, request):
        obj_product = mFET.FET_model()
        obj_product.customer_gid = self.request.query_params.get("Customer_gid")
        obj_product.product_type = 1
        obj_product.entity_gid = self.request.query_params.get("Entity_gid")
        out_message = obj_product.get_sales_fav_product()
        if not out_message.empty:
            ldict = out_message.to_json(orient='records')
            return Response({"MESSAGE": "FOUND", "DATA": json.loads(ldict)})
        else:
            return Response({"MESSAGE": "NOT_FOUND"})


class LatLong(APIView):
    def get(self, request):  #### Get Not Used
        obj_location = class1.login()
        obj_location.action = self.request.query_params.get("Action")
        if obj_location.action == "INSERT":
            obj_location.latlong_gid = 0
            obj_location.employee_gid = self.request.query_params.get("Emp_gid")
            obj_location.latitude = self.request.query_params.get("Latitude")
            obj_location.longitude = self.request.query_params.get("Londitude")
            obj_location.entity_gid = self.request.query_params.get("Entity_gid")
            obj_location.create_by = self.request.query_params.get("Emp_gid")
            out_message = obj_location.setposition()
            out_message = str(out_message[0])
            result = out_message.split(",")
            if result[1] == "SUCCESS":
                return Response({"MESSAGE": "SUCCESS"})
            else:
                return Response({"MESSAGE": "FAIL", "DATA": out_message})
        else:
            return Response({"MESSAGE": "FAIL", "DATA": "Incorrect Action Value."})

    def post(self, request):
        obj_location = class1.login()
        obj_location.action = self.request.query_params.get("Action")
        if obj_location.action == 'MULTIPLE_INSERT':
            obj_location.jsondata = json.loads(json.dumps(request.body.decode('utf-8')))
            out_message = obj_location.setposition()

            if out_message[0] == "SUCCESS":
                return Response({"MESSAGE": "SUCCESS"})
            else:
                return Response({"MESSAGE": "FAIL", "DATA": out_message})
        else:
            return Response({"MESSAGE": "FAIL", "DATA": "Incorrect Action Value."})


class Schedule_Master(APIView):
    def get(self, request):
        obj_Schedule = mFET.FET_model()
        obj_Schedule.action = self.request.query_params.get("Action")
        obj_Schedule.entity_gid = self.request.query_params.get("Entity_gid")
        if obj_Schedule.action == 'SCHEDULE_TYPE':
            ldf_Schedule_Type = obj_Schedule.get_schedule_type()
        elif obj_Schedule.action == 'FOLLOWUP_REASON':
            obj_Schedule.schedule_type_gid = self.request.query_params.get("Schedule_Type_gid")
            ldf_Schedule_Type = obj_Schedule.get_followup_reason_fet()
        else:
            return Response({"MESSAGE": "NOT_FOUND", "DATA": "Incorrect Action Value."})

        return Response({"MESSAGE": "FOUND", "DATA": json.loads(ldf_Schedule_Type.to_json(orient='records'))})


class Employee_Profile(APIView):
    def get(self, request):
        obj_Employee = mMasters.Masters()
        obj_Employee.entity_gid =decry_data(self.request.query_params.get("Entity_gid"))
        obj_Employee.cluster = self.request.query_params.get("Action")
        obj_Employee.employee_gid = decry_data(self.request.query_params.get("Emp_gid"))
        obj_Employee.jsonData = json.dumps({"entity_gid": [obj_Employee.entity_gid], "client_gid": []})
        if obj_Employee.cluster == "EMPLOYEE_EDIT":
            Out_Message = obj_Employee.get_employee()
            if Out_Message.empty == False:
                return Response({"MESSAGE": "FOUND", "DATA": json.loads(Out_Message.to_json(orient='records'))})
            else:
                return Response({"MESSAGE": "NOT_FOUND"})
        elif obj_Employee.cluster == 'HIERARCHY':
            # obj_Employee.cluster = 'Y'
            Out_Message = obj_Employee.get_employee()
            if Out_Message.empty == False:
                return Response({"MESSAGE": "FOUND", "DATA": json.loads(Out_Message.to_json(orient='records'))})
            else:
                return Response({"MESSAGE": "NOT_FOUND"})
        elif obj_Employee.cluster == 'EMP_MAP_CLUSTER_SUPERVISOR':
            obj_Employee.cluster_gid = self.request.query_params.get("Cluster_Gid")
            obj_Employee.entity_gid = self.request.query_params.get("Entity_gid")
            Out_Message = obj_Employee.get_employee()
            if Out_Message.empty == False:
                return Response({"MESSAGE": "FOUND", "DATA": json.loads(Out_Message.to_json(orient='records'))})
            else:
                return Response({"MESSAGE": "NOT_FOUND"})

        else:
            return Response({"MESSAGE": "NOT_FOUND", "DATA": "Incorrect Action Value."})


class ScheduleCustomerFET(APIView):
    def post(self, request):
        try:
            obj_Schedule = mFET.FET_model()
            obj_Schedule.action = self.request.query_params.get("Type")
            obj_Schedule.type = self.request.query_params.get("Sub_Type")
            obj_Schedule.json1 = json.loads(request.body.decode('utf-8')).get('Params').get('FILTER')
            obj_Schedule.jsondata = json.dumps(obj_Schedule.json1)
            obj_Schedule.json2 = json.loads(request.body.decode('utf-8')).get('Params').get('CLASSIFICATION')
            obj_Schedule.json_classification = json.dumps(obj_Schedule.json2)
            ld_schedule_Cust = obj_Schedule.get_schedule_customer()

            json_data = ld_schedule_Cust.get("DATA").to_json(orient='records')

            lj_data = json.loads(json_data)

            if ld_schedule_Cust.get("MESSAGE") == 'FOUND':
                ll_Schedule = json.loads(lj_data[0].get("ScheudleTask"))
                ll_NonSchedule = json.loads(lj_data[0].get("Non_ScheduleTask"))
                ll_Sales_Detail = json.loads(lj_data[0].get("Sales_Details"))
                ll_Service = json.loads(lj_data[0].get("Service"))

                # Checking Empty. Starts
                # if empty send empty list.
                if ll_Schedule[0].get('ScheduleType_Name') is None or ll_Schedule[0].get('ScheduleType_Name') == '':
                    ll_Schedule = []
                if ll_NonSchedule[0].get('ScheduleType_Name') is None or ll_NonSchedule[0].get(
                        'ScheduleType_Name') == '':
                    ll_NonSchedule = []
                if ll_Sales_Detail[0].get('SO_NO') is None or ll_Sales_Detail[0].get('SO_NO') == '':
                    ll_Sales_Detail = []
                if ll_Service[0].get('Service_Code') is None or ll_Service[0].get('Service_Code') == '':
                    ll_Service = []
                ### Checking Empty Ends

                ld_dict = {"DATA": {"ScheudleTask": ll_Schedule, "Non_ScheduleTask": ll_NonSchedule,
                                    "Sales_Details": ll_Sales_Detail, "Service": ll_Service
                                    }, "MESSAGE": "FOUND"}

            elif ld_schedule_Cust.get("MESSAGE") == 'NOT_FOUND':
                ld_dict = {"DATA": json.loads(json_data), "MESSAGE": ld_schedule_Cust.get("MESSAGE")}
            else:
                ld_dict = {"MESSAGE": 'Error Occured.' + ld_schedule_Cust.get("MESSAGE")}
            return Response(ld_dict)

        except Exception as e:
            return Response({"MESSAGE": e})


class Change_Password(APIView):
    def post(self, request):
        try:
            obj_UM = UM_View
            obj_UM.action = self.request.query_params.get("Type")
            # obj_UM.jsondata = json.loads(json.dumps(request.body.decode('utf-8')))
            if obj_UM.action == 'PROFILE_EMPCHANGE_PASSWORD':
                out_message = obj_UM.Password_verifiy(request)
            else:
                return Response({"MESSAGE": "In Correct Type Supplied"})

            out_message = json.loads(out_message.content.decode('utf-8'))
            return Response({"MESSAGE": out_message})

        except Exception as e:
            return Response({"MESSAGE": e})


class Get_position(APIView):
    def get(self, request):
        try:
            obj_poisionget = mCore.login()
            obj_poisionget.action = self.request.query_params.get("Action")
            obj_poisionget.employee_gid = self.request.query_params.get("Emp_gid")
            obj_poisionget.from_date = self.request.query_params.get("From_Date")
            if self.request.query_params.get("To_Date") == '' or self.request.query_params.get("To_Date") is None:
                obj_poisionget.to_date = ''
            else:
                # obj_poisionget.to_date = Bigflow.common.convertDate(self.request.query_params.get("To_Date"))
                obj_poisionget.to_date = self.request.query_params.get("To_Date")

            obj_poisionget.entity_gid = self.request.query_params.get("Entity_gid")
            df_position = obj_poisionget.getposition()
            if not df_position.empty:
                ldict = df_position.to_json(orient='records')
                return Response({"MESSAGE": "FOUND", "DATA": json.loads(ldict)})
            else:
                return Response({"MESSAGE": "NOT_FOUND"})

        except Exception as e:
            return Response({"MESSAGE": e})


class FileUpload(APIView):
    # parser_classes = (FileUploadParser,)
    ### POC ::KEEP it as Reference
    def post(self, request):

        jsondata = json.loads(request.body.decode('utf-8'))

        file_list = jsondata.get('File')

        if len(file_list) != 0:
            for i in range(len(file_list)):
                file_json = file_list[i]

                file_data = file_json.get('File_Base64data')

                file_data = base64.b64decode(file_data)
                file_name = file_json.get('File_Name')
                file_extension = file_json.get('File_Extension')

                file_name_new = file_name + str(datetime.datetime.now().strftime("%Y-%m-%d:%H:%M:%S"))

                # open(BASE_DIR + '/Bigflow/media/' + file_name + file_extension, 'wb')
                lsfile_name = str((BASE_DIR + '/Bigflow/media/' + file_name_new + file_extension))

                with open(lsfile_name, 'wb') as f:
                    f.write(file_data)

        return Response("Success")


from pathlib import Path


# from datetime import datetime
def File_Upload(file_list, dir_folder, emp_id):
    file_list = json.loads(file_list)

    if len(file_list) != 0:
        lst_saved_file_list = []
        for i in range(len(file_list)):
            file_json = file_list[i]

            file_data = file_json.get('File_Base64data')
            file_data = base64.b64decode(file_data)
            file_name = file_json.get('File_Name')
            file_extension = file_json.get('File_Extension')
            file_reftable_gid = file_json.get('Ref_Table_Gid')

            file_name_new = emp_id + '_' + str(datetime.datetime.now().strftime("%y%m%d_%H%M%S"))+str(i)

            current_month = datetime.datetime.now().strftime('%m')
            current_day = datetime.datetime.now().strftime('%d')
            current_year_full = datetime.datetime.now().strftime('%Y')
            # /media/  is the MEDIA_URL

            lsfile_name = str((BASE_DIR + '/Bigflow' + "/media/" + dir_folder + '/'
                               + str(current_year_full) + '/' + str(current_month) + '/' + str(current_day) + '/' +
                               file_name_new + '.' + file_extension))

            ### Added Newly
            lsfile_name_db = str((MEDIA_URL + dir_folder + '/'
                                  + str(current_year_full) + '/' + str(current_month) + '/' + str(current_day) + '/' +
                                  file_name_new + '.' + file_extension))

            path = Path(lsfile_name)
            path.parent.mkdir(parents=True, exist_ok=True)

            with open(lsfile_name, 'wb') as f:
                f.write(file_data)

                if file_reftable_gid == None:
                    file_reftable_gid = 0
                else:
                    file_reftable_gid = file_reftable_gid

                ld_saved_file = {"SavedFilePath": lsfile_name_db, "File_Name": file_name,
                                 "RefTable_Gid": file_reftable_gid}
                lst_saved_file_list.append(ld_saved_file)
        return lst_saved_file_list  ### Wip for Multiple Files

def FileUpload_S3(file_list):
    file_list = json.loads(file_list)

    if len(file_list) != 0:
        lst_saved_file_list = []
        for i in range(len(file_list)):
            file_json = file_list[i]

            file_data = file_json.get('File_Base64data')
            # file_data = base64.b64decode(file_data)

            # file_data = '/9j/4AAQSkZJRgABAQAAAQABAAD/2wCEAAkGBw8PDw8PDw4QEA8NDxAQDRUVDQ8QEBYWFREYFhUYFRUZHigsGholHRYYITEhJSkrLi4vGh8zODMtNygtMSsBCgoKDg0OGxAQGi0lICUvLS8tLS0tLS0tKy0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLf/AABEIAMIBAwMBEQACEQEDEQH/xAAcAAEAAgIDAQAAAAAAAAAAAAAABgcFCAIDBAH/xABIEAACAQMABgQJCAcHBQEAAAABAgADBBEFBgcSITETQVFhFyIyVHGBkZTSFCM1VXJ0obIkQlKCsbPBJTNikrTC0TRDU6LTFf/EABsBAQACAwEBAAAAAAAAAAAAAAAEBQEDBgcC/8QAOBEBAAEDAQQEDgICAgMAAAAAAAECAwQRBRIhMQYUQVETFiIyMzRSU2FxgZGxwSPRoeFC8CRy8f/aAAwDAQACEQMRAD8ArmWyqICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICGSGCAgICAgCYEt0Bs+vrtVqEJb0XwVapvb5BGQy0xzHpIlLl7cxsed3zp+CVbxK6uMpfQ2TWm6Oku7pn6ynQovqDI38ZS1dJr0z5NMaJUYFPbLs8E1j5zef57b/5T58Zr/swz1GhgtMbKrhPGtK6Vh+zUHRVOXURkE+yWOP0kt1cL0bvxabmFVHmygN1bVKLtTqo1OohwyspVh6p0Vu5Rcp3qOMd6FVTNPCqOLqn2+SAgICAgICAgICAgICAgICAgICAgICAgICAjTXhAsjZbqktX9PuaYZASLVGAIYg4LkdgPAA957Jy23dqTR/BZnj/AMpWGJY18upa84/XXisiAgIiOIjGvWqiaRokoFW7pD5hz19ZRu49R6jx7c2+ytpVYlyIq8ztRr9jwlKialNlZlZSrISrA8wQcEHvBnoFFUVRvR28lPMTHPscZ9MEBAQEBAGJ5a9hHGdIe2hoi6qY3LS4cMcAi3qlc+nGJHryrFHnV0x9Y/t9+Drnsd1xq5f08b9jcje5Yt6jflBnxTnY1Xm3I+8f2zNquOxj61F6Z3aiMjdjKyNw58DJFNdNXmzr8tHzNNUc4cJ9/N8kBAQEBAQEBAQEBAQEBA9+gdHG6uqFuDjpqgVjjOF5sfYDI2XfixYruT2NlqneriGxlCitNVRAFVFCqAMAADAnmNdc1zNU9q8imIjR2T5fRAQEBERx0FO7W9CLQuUuqa4W7z0vPHSKBx9Y4+kGdv0dzJvWZtVc6fwqs23u1awgU6JCICAgIEq1O1Jr6QPSMTRtQeNTGS+DgimOv0ngO+U+0tr2sON2ONfd/aTYxqrk8eS2tCap2NmB0Nupcc6jgVKp/ePL1YnG5W08nInWqdI7lnRZt0xyZuQNW4gdN3aUqylKtNKiHgQ6K49hm23euWp1oqmHzVRFXOFf61bMqThqth81U5mkzfNN9lj5B9OR6J0Oz+kFdE7l/jHf2od7DiY1p4Kqr0XpsyVFZHQlXVhhlI5gidhRcpqiKqZ11Vs0zE8XXPt8kBAQEBAQEMkMEBDJDBAlWy/6Wtvs1/5Dyo276lX9EnE9IvWeerkgICAgJieQgO2VAbGgccVulAPWM03z/CdJ0bmes1R8ELOjyFPTtlUQEBAz+pOgP/0LxaLZFFAalwRnyAQN3I5FiQPbK3amb1WxNcc55N+Pa8JUv2lTVFVVG6qAKoHIAchPOrlc11TVM8Z5rqIiI0hznwyTIQEBAgO1PVlK1B76mAte2TNXkN+mMZz3qM49Y7J0ewdozauxZr4xPL4IWXZiad+FPTtvgqiAgICAgICAgICAgIEm2bVlTStoWOAxqIPS9F1X8SB65VbaomrCr0+aTi8LkL5nna5ICAgICOwV3tnucW1rS4ZqVy/fhEI/3zpujNufC11T2R+UDOq8mIVJOzVhAQECydiijpb444inQAOOOCz5H4D2Tlek8/x2/qn4HnVLWnILMgICAgIGH1x+jdIfcrn+U0nbN9bt/OGq96OWvE9LURAQEBAQEBAQEBAQEDstq7U3Sohw9J1dD2MpyD7RPi7bi5RNE8pjRmJ3ZiYbB6qafp6QtkrpgP5FZM5KOOYPceY7jPNtoYVWJd3J5TynvXlm5FdOsMxITaQEBA41HCgsxAVQSxJwAAMkmZimap3aY1YmYjjKgtd9YTpC7aquRRp/N24OfJB4sR1Fjx9GOyej7LweqWIonzp4z/X0U2Re8JUj8sUcgICZE22TaUWhfNRc4W7p7i8cDfU7yfhvD1zn+kGNVdxorj/j+0zDr3a5ie1dM4WOPJbEBAQEBAjW0TSaW+jrkP5VzSe3pjrLVFI9gBzLXY2NXdyqZp7OKPk1xTbnVQs9EUpAQEBAQEBAQEBAQEBAzGq+sVfR9cVaR3lbArUycI69/YR1HqkHOwLeXb3K+E9k9zdZvTbq1Xnq/p+2v6XS275x/eIeFRD2Mv8AXkZwGZhXcWvdrj69i3t3abkawykhtpA6rq5p0UarVdadOmN52Y4UDvM+7Vqq7VFFEazPYxMxEayp3X3Xpr3NtbZS1z47cQ9XHURngnLhzOOPZO32TseMf+S753d3KvJyd/yaeSDy/Q5IYICAgfUYggg4KkMpHMEHIMxNMTGk8WYmYnWFt6jbQUrKtvfVAlcYWnVbglQdW8f1X9gPdOM2tsSqiZu2I4dsd3yWePlRPk1LCz+PKc3MTHYnRx5PswEBAxen9P21hSNS4qAcCaaDBqOR1Iv9eQkvDwb2VXu244d/Y13btNuNZlR+tmslXSNc1X8Smvi0ae8SqqO3tY9Z/wCJ3+Bs+jEt7kcZ7ZVF69NyrVhJPaCAhkhggICAgICAgICAgI0Eh2f06raTtRRdkO+TUKnHzags4PaCBjHeJWbXminErmuNdOXzSMbXwkaL+nnPJdECFbVdE1riyD0S5Fs/SVaYPBlxxbHWV549MvdgZNu1f3a+3hE9yJl0VTRwUrO8VGhAQEBAQEBAmOzq50i93SpW1ar0CMrXCli9FaYODlSeBPEADBz6OFHtm1iUWJruUxvTyntlLxpuVV8+C7pwS3IGA170nVtNHXFeg27VXo1RsA7u/VVCQD1gMecstk49N/Kpor5f00ZFc025mFC3d1UrOalWo9So3NnYsx9Znoduzbt07tEaQppqmebpmx8kBAQyQwQEBAYhkhggICAgICBYexizDXNzXIPzNFaanBxmo2Tx7cJ+M5rpNd3bFNHfOv2T8GnWqZW5OLWRDIY+QpLaNqobKt09Ff0W4Y4xypueJQ9gPMegjqnebF2lGTb3KvOj/KoybO5OsckNl7z5ckQgICAgIGV1b0BX0hXFGiMAYNVyPEpr2t39g65Dzc63i29+v6R3ttq1NydIXxq/oShY0FoUFwBxdj5bt1sx7f4TzzMy7mVcmuufp3Lm3biiNIZKRWwgRTal9EXP2rb/AFNOXGwfXafqjZfolFz0FTEBAQPsD5AQEBAQzqQwQEBAQEBAtrYtTAtrt+trhVPZhaYI/MZxnSer+WiPh+1ngR5MysWcynkBA8mldHUrqjUt6y71OquG6iOwg9RB4zdj5FzHuRdo5w+K6IrjSWv2sWhKthcPb1cEjjTYYw6ZwrgZ4ZxyPKekYeZbybUXKJ+fzUl23NurSWMktrICZCYGa1Z1ZudI1NyiN2mp+dqsp6NO7PW3HyR+A4yBnbRtYlGtc8eyG61ZquTwXnq/oShY0FoUFwBxdjjfdutmPb/CcBmZlzKuTXcn/S4tW4txpDJSI2EBAj20Gjv6LvRu727SDgYJ4o6sD6sZ9UstkVaZlHzaciP45UDPR1GQEBAQEBAQEBAQEBAQEBATIubY8gGj3IAy11U3j1nCIBOE6RTPWaY+H7lbYXmfVOZQJhAQECP666urpC1anj5+mC9s2cYfHAE/snkZZbLzqsS7Ex5s82i/ai5T8VB1qTIzI6lXRirqRggg4IM9ForpriK6eUqWY0nSXCfTBDOjOao6t1dI1xTXK0UINxUxwRewZ5seQHr5CV20c+jEtb0855R3/wCm+xam5OnYvnRmjqVrSShQQJTpjCgfiSesk8STPPb9+u/cm5cnWZXFFMUU6Q9U0vpwo1lcZRlYZIyrBhkHBGR1gz7rt10TpVGjETE8nOfDJA8OnbfpbS6pkFukt6y4BwTmmQAJIxKppvUVR3vi5GtEw1tE9RUD7AQEBAQEBAQEMkMEBAQEBAQLj2OVs2FVMf3d0/Ht3qaGcP0kp0yaZ+H7lbYU60T808nPJhAQEBHxFa7VNU98NpCgvjqB8rUDylAwKgx1gDj3Adk6nYO092Yx7k8Oz+kDLsa+XCqp2CtZvVTVutpGv0dPxaaYNeoRlUHZ3seof8Svz8+3iW96rjM8o7/9N1mzN2dOxe2htE0bOilCgm6ic+tmPWzHrYzz7KyrmTcmu5Os/hcUURRTpD03VzTpI1Sq6pTpgs7MQFAHWTNVu3Vcq3aY1lmqqKY1lUeuu0KpcFqFkzUrfxldxwqVRy4daL7Ce7lOz2ZsSizEXL0a1d3crb+VNU7tPJnti1Mi0um4bpugoHetFCeHoZfZK7pNNPhqIiOxuwNdyZlYc5pOIHF13gV5bwI9oxPq3OldM/H9sTy0ayVU3WZee6zL7DieqW51oifgoKucuM+3yQEBAQEBAQEMkMEBAQEBAQLZ2LVc212mOK3Cvn7VMD/b+M43pPR/JRV8P2s8GfJlY05hPICBHNoWkK1to24q0HNOoDSQMOYD1VRsdhwTxlpsaxRezKabkaxx/DRkVzRbmYYLZdrU1yjWlzVL3FMl6LO2XdDxIyfKZTn1HulhtzZsWpi9ap0jTjHdLTiXpq8mqeKfsARggEHmCMg+mc3TM84TFVaW2X1WvT8ndEs6p38knepcfGQL+t/h6scDjHHr7HSKmMePCRrXHD5/FX14WtfDksjQ2iqNnRShQTdRPWzHrZj1se2cxlZVzJuTcuTrP/eCdRTFEaQ8WsutFro9M1nzUYZp0lwarerqHeeE3YOzb2XPkxw7+x8Xb1NuOKmdada7nSL/ADh3KKnNKipO4Owt+23efUBO6wNm2cSmNI1ntntVV2/VclgZYz3y0Lp2Q0QujSw51Lmqz8esBUGPUonC9Iq5nL07oiP2t8ONLf1TaUCWQEzE6DWvTFIJc3KLndS4rKuTk4FRgMz1LGnWzRPwj8Ofr86fm8k3PkgICAgICAgICAgICAgICBZ2xSqc3yfqgUH5ccnpB/Scp0oo1i3V8/0sMDthaM5FZEBAiW1P6JuPt2/+oSXOwPXqfr+EXM9DKkKFZqbK6MUdCGRgcMCORBnfV0U106VQqYmYnWFv6j7QEut23vClO44BH4LTq9g/wv3cj1dk4vauxKrMzdscae7thZ4+VveTVzTm5uEpI1So6pTQZZmYKoHeTOfot111btMTMpk1RHGVZ607Tzl6Oj1GAd3p24g8OJpoR7C3snVYHR6NIuZE/RX3s2eVKtLm4eq7VKjs9Rzl2ZizE95M6i3bpt0xTTCBVVMzrPF1zY+SBeeywf2TbHAyXuSeHP8ASag4+yefbf8AXqo7tPwucT0UJZKdJICYka46y0il9eK3MXVfPHPOoT/Weo4VUVY9Ex3QobsaVyx0ktZAQEBAQEBAQEBAQEBAQECf7GqwF7XTjmpbEjs8Souc/wCac50lo1x6au6fz/8AE7BnSuVwTiFoTIQIntS+ibj7dv8Az0lzsD12n6/hFzPQyoyegdiokiWHpuNIV6iqlSvVqInkK1V2UcMDAJmmjHtUTrRTEPublU9rzTdo+CAgIF+7PUC6LsgABmkWOO1nYk+skmecbYmZzbkz8Pwu8b0UJFK1vICYY7WvOuf0lffeqv5p6bs31W38lHf9JLDSa1EBAQEBAQEBAQEBAQEBAQJbsruNzSlEEkdLTrU/T4m+Af8AJn1Sm2/RvYVU90xP6/aThzpdXXc3lKkUFSrTpmq27TDOqljjOFzzM4Oizcr13KZnTuW81Uxzl3zW+iBE9qf0Tcfbt/56S52D67T9fwjZnoZUZPQFNPMgICAgICZGwGoQI0XZZGPmAfaSRPNtrTE5lzTvXeN6Kln5XfBvICYO1rxrn9JX/wB6q/mnpuzfVbfyUV/0ksPJrUQEBAQEBAQEBAQEBAQEBAzOplx0WkbJ+PC4RTjGcP4hH/tIO07e/iV0/D8cW6xOlyFibYdGb1vQvE4Pa1NwkZzu1CMH1Mo9s5fo7kRFyq1MedH4/wBJ+ZTOm/HYlWqWlxe2VGvgBmBWoAc4ZTg/wz65VbSxZxsmq39fpKRZr36IqZiQW1FdqFMtom5wM4agx9AroSZcbBqiM6jX4/hGy/QyoqegqeSGCAgICAmRsPqef7NsPudv/KWeZbR9au/+0/leWPR0/Jy1r0x8hs61yFDNTCimDnBZmCrnHVxjAxetX6bPZzmWb1e5RvOjUrS9W9sqdzWRUd2qDxQwUhXKg4PLOJ97VxbeNkVW6J1YsXJuUas7K5u7WvOuX0lf/eqv5p6bs31W38lFf9JLDSa1EBAQEBAQEBDJDBAQEBAQEDI6uUme9tFQkMbmjukAEjxwSR6BxkXNmIsVzPdP4bLUa1wv/T+jhdWtxbn/AL1JlXubGVPqIBnnOHfmzfpuR3rq7RvUzEq/2MaRI+VWbHBXdr016x+pV9h3PbOi6SWYmKL8fKf0h4VemtErPnJ/JYMPrha9No+8pgZLW9Qrz8pV3l5d4EnbOu+CyaK/jDVejW3LXiemaaKLQgICGSGCACk8BxJ4D0nlPmqrSGYjVsxY0OjpUqf/AI6aJyx5KgcvVPLb9e/dqq75mV/RG7TEILtmvN20t6IP99XLHnypof6uvP8ApL7o1a3r1dzujREzatKYhm9m30VZ/ZqfznkHbnr1z/vY24voqUmlSkdrXjXP6SvvvVX809N2b6rb+Siv+klh5NaiAgICAgICAgICAgICAgd1naVazinRpvUqN5KopZvYOrvmu5dotRvVzER8X1TTNU6RC1tnmolS1qC8vMCsoIoUwwbc3hgs5H62CRgEgZPPq5DbG2ab9PgbOunbP6hY42NuzvVLDnMwn6Kg0T+hayvTHipVr1k7itZN9cZ6t7dHqxO1yP8AytkRX3RH+OCro8jI0W/OKWj4QDwIyDwI7uuZidJhieTWrSdp0FevR4/MVqlMZxnCuQM47hPUse74W3TX3xqoa40ql5pufBAQEBAzmpOjPlWkLaljKrUFWrwBG7T8Y5z24A9cr9qZHgMWurt00j5y349G/ciGwc82XanNsV7v31KiMYt7cE/aqMSc+pVnb9G7W7jTX7U/hVZ1Wte73Jxswrb2irfhjcNVBxznFVjnu58u6UG3ad3Oq+k/pMxJ1tUpXKWEjta865/SV/8Aeqv5p6ds31W38lHf9JLDSa1EBAQEBAQEBAQEBAQEBAkuqGuFTRi1Vp29OqazKSWZlI3RjAwOXGVe0dl05tVM1VzER8O9Is35txPDVnK+1i7I+btbdTniWaq49gKyuo6M2Y51zP8AhunOrmOUPdozazllW6tML+s9Kpkjv6Nur972yNkdGoiJm1Vx7pbKM72oYXW7TttX0raXdrVLInyYVCabrulKxJ8VgM+Ke+WGBh3rWDcsXY087T7NN25TVdiqldU4SecrYmY5jXHWSsKl7eVF8l7quy8uRqNjlPTsGiaMa3TPZER/hQ3Z1rqY6SmsgICAgXDso1dNvQa8qjFS7UdGP2aXME97Hj6As4jpBnReuRaonhTz+a1w7O7G9POU+nOprXzXi86bSV4+cgVjSXnwFICnjj3qfbPSNl2vB4dFPwUmRVvXJWBsavS1tcUCxPQVVZBwwFqA8v3lY+uc70ms7t2i5Ec+Cbg1eTurDnMRxTmv+vtq9LSd4HGN+saqc+Kv4ykfw9IM9I2TdpuYlEx2QpMmmabksBLJoICAgICAgICBafgjTz9vdR8c5Hxnn3cfdY9Qj2nzwRp5+3uq/HHjPPu4+51CPaPBGnn7e6r8ceM8+7j7nUI9p98Eaeft7qvxx4zz7uPudQj2jwRp9YN7qvxx4zz7uPudRj2jwRp9YN7qvxzHjRPu4+51GPaPBGnn7e6r8cz40Ve7j7nUI9r8HgjTz9/dR8cx40T7uPudQj2vweCNPrBvdV+OPGefdR9zqEe0+09kqAg/L24EH/pV6v35ieks1RNPgufdM/0+owYidd5Zc5aZ1mZTuXB5dJ29SrRqU6VXoXqKVD7m+VB4EgZHHHI9U3Y9ym3ciuqnXTs10YqiZjSJ0V4NkSeft7qPjnRx0onstR90DqMdtT74I0+sH91HxzPjRPu4+51GPa/B4I08/b3VfjmfGefdx9zqEe0eCNPP291X448Z593H3OoR7R4I08/b3Vfjjxon3cfdnqEe0kui9Q9G0EQNbJWqJgl6gLFmxxO6TgDu6pU39tZd2ZmK5iO6NEijGt0wk4Eqp48Zb3CsGKsEYK5BCsV3wD1ErkZ9GZ9UTTrFVXGI7CY1hXFbZOHZnbSDlnZmY/JV4ljkny+0zp6ek27TFMWo4fFBnBiZ13mQ0Bs/qWFYV6GkSGxuurWgKMuQSGHSd3McRI2VtyjKt7tdqNPnyfdvF8HOsVJyoOOOM9eBgeyc/PwS0V1y1KTSdSlUNc0WpIyHFEVCwJyMneHLj7TLjZu16sKmaYjXXs1Rr+P4WY4o94I08/b3Vfjll40T7r/LR1GPaPBGn1g/uo+OPGifdx9zqMe1+DwRp9YN7qPjmfGefdx9zqEe0eCNPP291X448Z593H3Z6hHtHgjT6wf3VfjmPGifdx92OoR7R4I08/b3VfjmfGifdx9zqMe0eCNPP291X448aJ93H3OoR7R4I0+sG91X448aJ93H3Z6hHtHgjTz9/dR8cx40T7uPux1GPa/CzJyqxICAgICAgICAgICAgICAgICAgICAjt1CAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgf/2Q=='
            # WIP - Get File path and frame bacj to json - will do
            lsfile_name = 'TESTFA.png'

            with open(lsfile_name, 'wb') as f:
                file_data = base64.b64decode(file_data)
                f.write(file_data)
            with open(lsfile_name, 'rb') as f:
                contents = f.read()
                os.remove(lsfile_name)
            s3 = boto3.resource('s3')
            s3_obj = s3.Object(bucket_name='vysfin-assets-uat', key=lsfile_name)
            s3_obj.put(Body=contents)
            s3_client = boto3.client('s3')
            response = s3_client.generate_presigned_url('get_object',
                                                        Params={'Bucket': 'vysfin-assets-uat', 'Key': lsfile_name},
                                                        ExpiresIn=3600)
            print(response)


def File_Uploadforscan(file_list, dir_folder, employee_gid, File_count):
    file_list = json.loads(file_list)
    if len(file_list) != 0:
        lst_saved_file_list = []
        for i in range(len(file_list)):
            file_json = file_list[i]
            file_data = file_json.get('File_Base64data')
            file_data = base64.b64decode(file_data)
            file_name = file_json.get('File_Name')
            file_extension = file_json.get('File_Extension')
            file_reftable_gid = file_json.get('Ref_Table_Gid')
            file_name_new = file_name
            current_month = datetime.datetime.now().strftime('%m')
            current_day = datetime.datetime.now().strftime('%d')
            current_year_full = datetime.datetime.now().strftime('%Y')
            # /media/  is the MEDIA_URL
            checkfilepath = str(
                (settings.MEDIA_ROOT) + '/INWARD/' + str(current_year_full) + '/' + str(current_month) + '/' + str(
                    current_day) + '/')
            if int(File_count) == 1:
                for pat, subdirs, files in os.walk(checkfilepath):
                    if employee_gid in checkfilepath:
                        shutil.rmtree(checkfilepath)

            lsfile_name = str(
                (settings.MEDIA_ROOT) + '/INWARD/' + str(current_year_full) + '/' + str(current_month) + '/' + str(
                    current_day) + '/' + employee_gid + '/' + 'Tempinward/' + file_name_new + '.' + file_extension)
            # lsfile_name = str(f+file_name + '.'  + file_name_new )
            ### Added Newly
            lsfile_name_db = str((settings.MEDIA_ROOT) + '/INWARD/' + str(current_year_full) + '/' + str(
                current_month) + '/' + str(
                current_day) + '/' + employee_gid + '/' + file_name_new + '.' + file_extension)
            path = Path(lsfile_name)
            path.parent.mkdir(parents=True, exist_ok=True)

            with open(lsfile_name, 'wb') as f:
                f.write(file_data)

                if file_reftable_gid == None:
                    file_reftable_gid = 0
                else:
                    file_reftable_gid = file_reftable_gid

                ld_saved_file = {"SavedFilePath": lsfile_name_db, "File_Name": file_name,
                                 "RefTable_Gid": file_reftable_gid}
                lst_saved_file_list.append(ld_saved_file)
                return HttpResponse("data:{MESSAGE:SUCCESS1222}")


### Wip for Multiple Files


class Stock_GetAPI(APIView):

    def post(self, request):
        request.session['Entity_gid'] = self.request.query_params.get("Entity_gid")
        request.session['Emp_gid'] = self.request.query_params.get("Emp_gid")
        Object_Stockget = views.stockget(request)

        out_put = json.loads(Object_Stockget.content.decode('utf-8'))
        ## List Type as Output
        if len(out_put) > 0:
            return Response({"MESSAGE": "FOUND", "DATA": out_put})
        else:
            return Response({"MESSAGE": "NOT_FOUND"})


class Stock_SetAPI(APIView):
    def post(self, request):
        request.session['Emp_gid'] = self.request.query_params.get("Emp_Gid")
        out_message = views.stockset(request)
        out_message = json.loads(out_message.content.decode('utf-8'))
        return Response({"MESSAGE": out_message})


# class Customer_view_get(APIView):
#     def post(self,request):
#         jsondata = json.loads(request.body.decode('utf-8')).get('parms')
#         Action = jsondata.get('ACTION')
#         request.session['Entity_gid'] = self.request.query_params.get("Entity_gid")
#         #request.session['Emp_gid'] = self.request.query_params.get("Emp_gid")
#         if Action == 'Common':
#             object_viewdetail = mFET.FET_model()
#             object_viewdetail.customer_gid = jsondata.get('customer_gid')
#             object_viewdetail.employee_gid = jsondata.get('emp_gid')
#             object_viewdetail.action = jsondata.get('Outstanding_Group')
#             object_viewdetail.from_date = ""
#             object_viewdetail.to_date = ""
#             object_viewdetail.limit = self.request.query_params.get("Limit")
#             outstanding_detail = object_viewdetail.get_FEToutstanding_fet() ### Sally Table
#             object_viewdetail.action = "Scheduleview"
#             collection_history = object_viewdetail.get_collection_history_fet() ### Sally table
#             object_viewdetail.employee_gid = 0
#             sales_history = object_viewdetail.get_sales_history_fet() ### Need To Change
#         if len(outstanding_detail) or len(collection_history) or len(sales_history) > 0:
#            return Response({ "MESSAGE": "FOUND",
#                          "outstanding_detail":json.loads(outstanding_detail.to_json(orient='records')),
#                          "sales_history":json.loads(sales_history.to_json(orient='records')),
#                          "collection_history": json.loads(collection_history.to_json(orient='records'))})
#         else:
#             return Response({"MESSAGE": "NOT_FOUND"})
#
class Customer_view_get(APIView):
    def post(self, request):
        jsondata = json.loads(request.body.decode('utf-8'))
        Action = jsondata.get('ACTION')
        # request.session['Entity_gid'] = decry_data(self.request.query_params.get("Entity_gid"))
        # request.session['Emp_gid'] = self.request.query_params.get("Emp_gid")
        if Action == 'Common':
            object_viewdetail = mFET.FET_model()
            obj_collection = mCollection.Collection_model()
            ### For Outstanding
            obj_collection.type = jsondata.get('Outstanding_Type')
            obj_collection.sub_type = jsondata.get('Outstanding_SubType')
            obj_collection.filter_json = jsondata
            obj_collection.filter_json['Employee_Gid'] = decry_data(obj_collection.filter_json['Employee_Gid'])
            obj_collection.filter_json = json.dumps(jsondata)
            obj_collection.Classification = jsondata.get('CLASSIFICATION')

            obj_collection.entity = self.request.query_params.get("entity")
            obj_collection.Classification['entity_gid'] = [decry_data(obj_collection.entity)]
            obj_collection.Classification = json.dumps(obj_collection.Classification)
            common.main_fun1(request.read(), request.path)
            outstanding_detail = obj_collection.get_OutstandingCustomer()

            #### For Sale
            object_viewdetail.customer_gid = jsondata.get('Customer_Gid')
            object_viewdetail.employee_gid = jsondata.get('Employee_Gid')
            object_viewdetail.from_date = ""
            object_viewdetail.to_date = ""
            object_viewdetail.entity_gid = decry_data(obj_collection.filter_json['Employee_Gid'])
            object_viewdetail.limit = self.request.query_params.get("Limit")
            sales_history = object_viewdetail.get_sales_history_fet()

            #### For Collection
            obj_collection.action = "COLLECTION"
            obj_collection.type = "SUMMARY"
            obj_collection.collectionheader_gid = 0
            obj_collection.name = ''
            obj_collection.date = ''
            obj_collection.jsonData = jsondata
            obj_collection.jsondata = jsondata.get('CLASSIFICATION')
            collection_history = obj_collection.get_collection_inv_map()

            ## For Get Hierarchy
            object_viewdetail.employee_gid = jsondata.get('Employee_Gid')
            object_viewdetail.group = 'CUSTOMER_OUTSTANDING_GROUP'
            object_viewdetail.create_by = decry_data(jsondata.get('Employee_Gid'))
            object_viewdetail.entity_gid = self.request.query_params.get("Entity_gid")

            lt_out_message = object_viewdetail.get_hierarchy()
            ls_hierarchy = lt_out_message[0]

            if ls_hierarchy == 'Y' or ls_hierarchy == 'N':
                ls_hierarchy = ls_hierarchy
            else:
                ls_hierarchy = 'N'

        if len(outstanding_detail) or len(collection_history) or len(sales_history) > 0:
            return Response({"MESSAGE": "FOUND",
                             "outstanding_detail": json.loads(outstanding_detail.to_json(orient='records')),
                             "sales_history": json.loads(sales_history.to_json(orient='records')),
                             "collection_history": json.loads(collection_history.to_json(orient='records')),
                             "outstanding_hierarchy": ls_hierarchy
                             })

        else:
            return Response({"MESSAGE": "NOT_FOUND"})


class Direct_Outcome_Summary(APIView):
    def post(self, request):
        try:
            obj_summary = views

            request.session['Emp_gid'] = self.request.query_params.get("Emp_Gid")
            request.session['Entity_gid'] = self.request.query_params.get("Entity_gid")
            out_message = obj_summary.pre_schedule_get(request)
            out_message = json.loads(out_message.content.decode('utf-8'))

            if len(out_message) > 0:
                return Response({"MESSAGE": "FOUND", "DATA": out_message})
            else:
                return Response({"MESSAGE": "NOT_FOUND"})
        except Exception as e:
            return Response({"MESSAGE": "ERROR_OCCURED", "DATA": str(e)})


class FET_Approve(APIView):
    def post(self, request):
        try:
            obj_approve_sales = mSales.Sales_Model()
            obj_approve_sales.action = self.request.query_params.get("Action")

            obj_approve_leads = mFET.FET_model()
            if obj_approve_sales.action == 'PENDING':
                obj_approve_sales.date = self.request.query_params.get("Date")
                obj_approve_sales.customer_gid = self.request.query_params.get("Customer_Gid")
                obj_approve_sales.employee_gid = self.request.query_params.get("Emp_Gid")
                obj_approve_sales.limit = self.request.query_params.get("Limit")
                obj_approve_sales.jsonData = json.loads(request.body.decode('utf-8')).get('Classification')
                # obj_approve_sales.jsonData['Entity_Gid'] = [1]
                obj_approve_sales.jsondata = '{}'

                obj_approve_sales.jsonData = json.dumps(obj_approve_sales.jsonData)

                obj_approve_leads.action = self.request.query_params.get("Action")
                obj_approve_leads.leadref_gid = 0
                obj_approve_leads.leadref_name = ''
                obj_approve_leads.status = obj_approve_sales.action  # PENDING
                obj_approve_leads.mobile_no = ''
                obj_approve_leads.entity_gid = self.request.query_params.get("Entity_Gid")

                dfout_message_sales = obj_approve_sales.get_sales_order()
                dfout_message_leads = obj_approve_leads.get_leadrequest()

                if not dfout_message_sales.empty or not dfout_message_leads.empty:

                    ldict_sales = dfout_message_sales.to_json(orient='records')

                    lst_sales = json.loads(ldict_sales)

                    for i in range(len(lst_sales)):
                        obj_sales = mMasters.Masters()

                        obj_sales.customer_gid = lst_sales[i].get("customer_gid")
                        obj_sales.soheader_gid = lst_sales[i].get("soheader_gid")
                        ## To Call the Model SALES.................................................
                        obj_sales.action = 'proposedbill'
                        obj_sales.type = ""
                        obj_sales.jsonData = {"customer_gid": obj_sales.customer_gid,
                                              "soheader_gid": obj_sales.soheader_gid}
                        obj_sales.jsonData = json.dumps(obj_sales.jsonData)
                        obj_sales.entity_gid = self.request.query_params.get("Entity_Gid")

                        df_salesdetails = obj_sales.getcreditapprv()

                        if not df_salesdetails.empty:
                            ldict_salesdetails = df_salesdetails.to_json(orient='records')
                            lst_sales[i].update({'Sale_Details': json.loads(ldict_salesdetails)})
                        else:
                            lst_sales[i].update({'Sale_Details': []})

                        ### To Call the Model Outstanding. ##############################
                        ### a) Customer Level
                        obj_outstanding = mCollection.Collection_model()
                        jsondata = json.loads(request.body.decode('utf-8'))
                        obj_outstanding.type = jsondata.get('Outstanding_Type')
                        obj_outstanding.sub_type = jsondata.get('Outstanding_SubType')
                        obj_outstanding.filter_json = json.dumps({"Customer_Gid": lst_sales[i].get("customer_gid")})
                        obj_outstanding.Classification = json.dumps(
                            json.loads(request.body.decode('utf-8')).get('Classification'))
                        df_outstanding_details = obj_outstanding.get_OutstandingCustomer()

                        ### b) Customer Group Level
                        obj_outstanding.filter_json = json.dumps(
                            {"Outstanding_Customer_Group_Gid": lst_sales[i].get("customer_custgroup_gid")})
                        df_outstanding_details_cust_group = obj_outstanding.get_OutstandingCustomer()
                        ## a) Customer Level Data
                        if not df_outstanding_details.empty:
                            ldict_outstandingdetails = df_outstanding_details.to_json(orient='records')
                            lst_sales[i].update({'Outstanding_Details': json.loads(ldict_outstandingdetails)})
                        else:
                            lst_sales[i].update({'Outstanding_Details': []})

                        ## a) Customer Group Level Data
                        if not df_outstanding_details_cust_group.empty:
                            ldict_outstandingdetails_group = df_outstanding_details_cust_group.to_json(orient='records')
                            lst_sales[i].update(
                                {'Outstanding_Details_Group': json.loads(ldict_outstandingdetails_group)})
                        else:
                            lst_sales[i].update({'Outstanding_Details_Group': []})

                            #
                            # ####VGF Details
                            # obj_vgf = mCollection.Collection_model()
                            #
                            # obj_vgf.Action = "VGF"
                            # obj_vgf.Type = "CALCULATION"
                            # obj_vgf.collectionheader_gid = 1
                            # obj_vgf.name = ''
                            # obj_vgf.date = ''
                            # obj_vgf.filter_json = json.dumps({'custqry_customer_gid': lst_sales[i].get("customer_gid")})
                            # obj_vgf.jsondata = json.dumps({'Entity_Gid': 1})
                            # df_obj_vgf = obj_vgf.get_vgfcollection()
                            #
                            # if not df_obj_vgf.empty:
                            #     ldict_vgf = df_obj_vgf.to_json(orient='records')
                            #     lst_sales[i].update({'Vgf_Details': json.loads(ldict_vgf)})
                            # else:
                            #     lst_sales[i].update({'Vgf_Details': []})

                                # # ### To Call the Model Lastbounce Details.

                        # # ### To Call the Model Lastbounce Details.

                        obj_Lastbounce = mCollection.Collection_model()

                        obj_Lastbounce.action = "CHEQUE"
                        obj_Lastbounce.type = "BOUNCE"
                        obj_Lastbounce.collectionheader_gid = 0
                        obj_Lastbounce.name = ''
                        obj_Lastbounce.date = ''
                        obj_Lastbounce.filter_json = json.dumps(
                            {"CustGroup_Gid": lst_sales[i].get("customer_custgroup_gid")})
                        obj_Lastbounce.jsondata = json.dumps({'Entity_Gid': [1]})
                        df_obj_Lastbounce = obj_Lastbounce.get_lastbounce_collection()

                        if not df_obj_Lastbounce.empty:
                            ldict_Lastbounce = df_obj_Lastbounce.to_json(orient='records')
                            lst_sales[i].update({'Lastbounce_Details': json.loads(ldict_Lastbounce)})
                        else:
                            lst_sales[i].update({'Lastbounce_Details': []})
                        # ldict_leads = dfout_message_leads.to_json(orient='records')
                        ####VGF Details
                        obj_vgf = mCollection.Collection_model()

                        obj_vgf.Action = "VGF"
                        obj_vgf.Type = "CALCULATION"
                        obj_vgf.collectionheader_gid = 1
                        obj_vgf.name = ''
                        obj_vgf.date = ''
                        obj_vgf.filter_json = json.dumps({'custqry_customer_gid': lst_sales[i].get("customer_gid")})
                        obj_vgf.jsondata = json.dumps({'Entity_Gid': 1})
                        df_obj_vgf = obj_vgf.get_vgfcollection()

                        if not df_obj_vgf.empty:
                            ldict_vgf = df_obj_vgf.to_json(orient='records')
                            lst_sales[i].update({'Vgf_Details': json.loads(ldict_vgf)})
                        else:
                            lst_sales[i].update({'Vgf_Details': []})

                        ### To Call the Model PDC Details.

                        obj_pending_collection = mCollection.Collection_model()

                        obj_pending_collection.action = "COLLECTION_INHAND"
                        obj_pending_collection.type = "PENDING"
                        obj_pending_collection.collectionheader_gid = 0
                        obj_pending_collection.name = ''
                        obj_pending_collection.date = ''
                        obj_pending_collection.jsonData = {"Customer_Gid": lst_sales[i].get("customer_gid")}
                        obj_pending_collection.jsondata = json.loads(request.body.decode('utf-8')).get('Classification')
                        df_pending_collection = obj_pending_collection.get_collection_inv_map()

                        if not df_pending_collection.empty:
                            ldict_pending_collection = df_pending_collection.to_json(orient='records')
                            lst_sales[i].update({'PDC_Pending': json.loads(ldict_pending_collection)})
                        else:
                            lst_sales[i].update({'PDC_Pending': []})

                    ldict_leads = dfout_message_leads.to_json(orient='records')

                    return Response(
                        {"MESSAGE": "FOUND", "DATA": {"SALES": lst_sales, "LEADS": json.loads(ldict_leads)}})

                else:
                    return Response({"MESSAGE": "NOT_FOUND"})
            elif obj_approve_sales.action == 'SALES_DATA':

                obj_approve_sales = views
                request.session['Emp_gid'] = self.request.query_params.get("Emp_Gid")
                request.session['Entity_gid'] = self.request.query_params.get("Entity_Gid")

                if request.session['Emp_gid'] == None or request.session['Emp_gid'] == '':
                    return Response({"MESSAGE": "ERROR_OCCURED", "DATA": "Emp Gid Is Needed"})

                if request.session['Entity_gid'] == None or request.session['Entity_gid'] == '':
                    return Response({"MESSAGE": "ERROR_OCCURED", "DATA": "Entity Gid Is Needed"})

                out_message = obj_approve_sales.sale_approval(request)
                out_message = json.loads(out_message.content.decode('utf-8'))

                if out_message == 'SUCCESS':
                    return Response({"MESSAGE": "SUCCESS"})
                else:
                    return Response({"MESSAGE": "FAIL", "DATA": str(out_message)})
            else:
                return Response({"MESSAGE": "ERROR_OCCURED", "DATA": "Incorrect Action"})



        except Exception as e:
            return Response({"MESSAGE": "ERROR_OCCURED", "DATA": str(e)})


class FET_Review(APIView):  ### Approve and Not Approve
    def post(self, request):
        try:
            obj_fetreview = mFET.FET_model()
            obj_fetreview.action = self.request.query_params.get("Action")
            obj_fetreview.jsonData = json.loads(request.body.decode('utf-8')).get('Filter')
            obj_fetreview.jsondata = json.loads(request.body.decode('utf-8')).get('Classification')
            obj_fetreview.jsonData = json.dumps(obj_fetreview.jsonData)
            obj_fetreview.jsondata = json.dumps(obj_fetreview.jsondata)
            dfout_message = obj_fetreview.get_empvsSchedule()

            if not dfout_message.empty:
                if obj_fetreview.action == 'SCHEDULE_SNAPSHOT':
                    dfout_message['lj_data'] = dfout_message['lj_data'].apply(json.loads)
                ldict = dfout_message.to_json(orient='records')
                return Response({"MESSAGE": "FOUND", "DATA": json.loads(ldict)})
            else:
                return Response({"MESSAGE": "NOT_FOUND"})

        except Exception as e:
            return Response({"MESSAGE": "ERROR_OCCURED", "DATA": str(e)})

    def get(self, request):
        if request.method == 'GET':
            data = {}
            obj_empvsschedule = mFET.FET_model()
            if (self.request.query_params.get('localaction') == 'noexcel'):
                obj_empvsschedule.action = self.request.query_params.get('action')
                if self.request.query_params.get('emp_gid') == '0':
                    data['employee_gid'] = self.request.query_params.get('login_emp_gid')
                else:
                    data['employee_gid'] = self.request.query_params.get('emp_gid')
                if (self.request.query_params.get('f_date') != ''):
                    data['fromdate'] = self.request.query_params.get('f_date')
                if (self.request.query_params.get('t_date') != ''):
                    data['todate'] = self.request.query_params.get('t_date')
                if (self.request.query_params.get('fu_f_date') != ''):
                    data['followUp_fromdate'] = self.request.query_params.get('fu_f_date')
                if (self.request.query_params.get('fu_t_date') != ''):
                    data['followUp_todate'] = self.request.query_params.get('fu_t_date')
                if (self.request.query_params.get('rs_f_date') != ''):
                    data['reschedule_fromdate'] = self.request.query_params.get('rs_f_date')
                if (self.request.query_params.get('rs_t_date') != ''):
                    data['reschedule_todate'] = self.request.query_params.get('rs_t_date')
                data['customer_gid'] = self.request.query_params.get('cus_gid')
                data['scheduletype_gid'] = self.request.query_params.get('type_gid')
                data['customergroup_gid'] = self.request.query_params.get('custgrp')
                data['location_gid'] = self.request.query_params.get('loc_gid')
                data['login_emp_gid'] = self.request.query_params.get('login_emp_gid')
                data['Hierarchy_checked'] = self.request.query_params.get('chckd')
                obj_empvsschedule.jsonData = json.dumps(data)
                obj_empvsschedule.jsondata = json.dumps(
                    {"entity_gid": [self.request.query_params.get('entity_gid')],
                     "client_gid": [self.request.query_params.get('Cname')]})
                df_preschedule = obj_empvsschedule.get_empvsSchedule()
                # df_preschedule['login_gid'] = request.session['Emp_gid']
                jdata = df_preschedule.to_json(orient='records')
                return Response({"MESSAGE": "FOUND", "DATA": json.loads(jdata)})
            else:
                obj_empvsschedule.action = self.request.query_params.get('action')
                if self.request.query_params.get('emp_gid') == '0':
                    data['employee_gid'] = self.request.query_params.get('login_emp_gid')
                else:
                    data['employee_gid'] = self.request.query_params.get('emp_gid')
                if (self.request.query_params.get('f_date') != ''):
                    data['fromdate'] = self.request.query_params.get('f_date')
                if (self.request.query_params.get('t_date') != ''):
                    data['todate'] = self.request.query_params.get('t_date')
                if (self.request.query_params.get('fu_f_date') != ''):
                    data['followUp_fromdate'] = self.request.query_params.get('fu_f_date')
                if (self.request.query_params.get('fu_t_date') != ''):
                    data['followUp_todate'] = self.request.query_params.get('fu_t_date')
                if (self.request.query_params.get('rs_f_date') != ''):
                    data['reschedule_fromdate'] = self.request.query_params.get('rs_f_date')
                if (self.request.query_params.get('rs_t_date') != ''):
                    data['reschedule_todate'] = self.request.query_params.get('rs_t_date')
                data['customer_gid'] = self.request.query_params.get('cus_gid')
                data['scheduletype_gid'] = self.request.query_params.get('type_gid')
                data['customergroup_gid'] = self.request.query_params.get('custgrp')
                data['location_gid'] = self.request.query_params.get('loc_gid')
                data['login_emp_gid'] = self.request.query_params.get('login_emp_gid')
                obj_empvsschedule.jsonData = json.dumps(data)
                obj_empvsschedule.jsondata = json.dumps(
                    {"entity_gid": [self.request.query_params.get('entity_gid')],
                     "client_gid": [self.request.query_params.get('Cname')]})
                XLSX_MIME = 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
                response = HttpResponse(content_type=XLSX_MIME)
                filename = Excelfilename('FET Review Details_')
                response['Content-Disposition'] = 'attachment; filename="{}"'.format(filename)
                # response['Content-Disposition'] = 'attachment; filename="FET Review Excel.xlsx"'
                writer = pd.ExcelWriter(response, engine='xlsxwriter')
                df_view = obj_empvsschedule.get_empvsSchedule()
                df_view.index = range(1, len(df_view) + 1)
                df_data = df_view[
                    ['employee_name', 'customer_name', 'schdate', 'scheduletype_name', 'schedule_status',
                     'followupreason_name', 'schedule_followup_date', 'schedule_reschedule_date',
                     'schedulereview_remarks',
                     'schedulereview_reviewstatus']]
                df_data.to_excel(writer, sheet_name='FET Review', index_label='SL NO', startrow=1, startcol=2,
                                 freeze_panes=(2, 0),
                                 header=['Employee Name', 'Customer Name', 'Date', 'Type', 'Status', 'Complete For',
                                         'Followup Date', 'Re-Schedule Date', 'Status Remark', 'Status'])
                writer.save()
                return response


### Common Classes.
class Comment(APIView):  ### Both Comment Set and Get.
    def post(self, request):
        try:
            obj_comment = MasterViews
            action = self.request.query_params.get("Action")
            request.session['Entity_gid'] = self.request.query_params.get("Entity_Gid")
            request.session['Emp_gid'] = self.request.query_params.get("Emp_Gid")
            if action == 'INSERT':
                ### Insert - Save the Record.
                out_message = obj_comment.commentset(request)
                out_message = json.loads(out_message.content.decode('utf-8'))
                if out_message == 'SUCCESS':
                    return Response({"MESSAGE": "SUCCESS"})
                else:
                    return Response({"MESSAGE": "FAIL", "DATA": str(out_message)})

            elif action == 'FETCH':
                ljout_message = obj_comment.commentget(request)
                lj_output = ljout_message.content.decode('utf-8')
                lj_output = json.loads(lj_output)

                if len(lj_output) > 0:
                    return Response({"MESSAGE": "FOUND", "DATA": lj_output})
                else:
                    return Response({"MESSAGE": "NOT_FOUND"})
            else:
                return Response({"MESSAGE": "FAIL", "DATA": "Incorrect Action Value."})

        except Exception as e:
            return Response({"MESSAGE": "ERROR_OCCURED", "DATA": str(e)})


class DeviceDetails(APIView):
    def post(self, request):
        try:
            if self.request.query_params.get("Action") == "DEVICEDETAILS_SET":

                obj_device = mMasters.Masters();
                obj_device.action = self.request.query_params.get("Action")
                obj_device.entity_gid = self.request.query_params.get("Entity_Gid")
                obj_device.employee_gid = self.request.query_params.get("Emp_Gid")
                obj_device.create_by = self.request.query_params.get("Emp_Gid")
                obj_device.jsonData = json.loads(request.body.decode('utf-8'))

                out_message = obj_device.set_ip()

                if out_message[0] == 'SUCCESS':
                    return Response({"MESSAGE": "SUCCESS"})
                else:
                    return Response({"MESSAGE": "FAIL", "DATA": str(out_message)})

        except Exception as e:
            return Response({"MESSAGE": "ERROR_OCCURED", "DATA": str(e)})


class FET_ReviewApprove(APIView):  # Pending
    def post(self, request):
        approvedtl = views
        request.session['Entity_gid'] = self.request.query_params.get("Entity_Gid")
        request.session['Emp_gid'] = self.request.query_params.get("Emp_Gid")
        approveset = approvedtl.setschedule_review(request)
        return Response({"MESSAGE": json.loads(approveset.content.decode('utf-8'))})


class FET_Version(APIView):
    def get(self, request):
        obj_Version = mMasters.Masters()
        obj_Version.entity_gid = self.request.query_params.get("Entity_gid")
        obj_Version.action = self.request.query_params.get("Action")
        obj_Version.version_flag = self.request.query_params.get("Version_flag")
        Out_Message = obj_Version.get_Version()
        if Out_Message.empty == False:
            return Response({"MESSAGE": "FOUND", "DATA": json.loads(Out_Message.to_json(orient='records'))})
        else:
            return Response({"MESSAGE": "NOT_FOUND"})


class Login_Get(APIView):
    def post(self, request):
        obj_Login = mMasters.Masters()
        obj_Login.entity_gid = self.request.query_params.get("Entity_gid")
        obj_Login.action = self.request.query_params.get("Action")
        obj_Login.type = self.request.query_params.get("Type")
        obj_Login.jsondata = json.loads(request.body.decode('utf-8'))
        Out_Message = obj_Login.get_Logindetail()
        if Out_Message.empty == False:
            return Response({"MESSAGE": "FOUND", "DATA": json.loads(Out_Message.to_json(orient='records'))})
        else:
            return Response({"MESSAGE": "NOT_FOUND"})


# SALES

class sales_planning_Set(APIView):
    def post(self, request):
        try:
            jsondata = json.loads(request.body.decode('utf-8'))
            obj_sales = mSales.Sales_Model()
            obj_sales.action = self.request.query_params.get("action")
            obj_sales.type = self.request.query_params.get("type")
            obj_sales.header = json.dumps(jsondata.get('parms').get('header'))
            obj_sales.detail = json.dumps(jsondata.get('parms').get('Details'))
            obj_sales.Classification = json.dumps(jsondata.get('parms').get('Classification'))
            obj_sales.sales = json.dumps(jsondata.get('parms').get('sales_sales'))
            request.session['Entity_gid'] = self.request.query_params.get("Entity_Gid")
            obj_sales.entity_gid = self.request.query_params.get("Entity_Gid")
            request.session['Emp_gid'] = self.request.query_params.get("Emp_Gid")
            plan = obj_sales.set_salesplanning()
            return Response({"MESSAGE": "FOUND", "DATA": plan[0]})
        except Exception as e:
            return Response({"MESSAGE": "ERROR_OCCURED", "DATA": str(e)})


class sales_planning_Get(APIView):
    def post(self, request):
        try:
            obj_sales = mSales.Sales_Model()
            jsondata = json.loads(request.body.decode('utf-8'))
            obj_sales.filter_json = json.dumps(jsondata.get('parms').get('filter'))
            obj_sales.Classification = json.dumps(jsondata.get('parms').get('classification'))
            obj_sales.type = self.request.query_params.get("type")
            obj_sales.customer_gid = self.request.query_params.get("cust_gid")
            obj_sales.year = self.request.query_params.get("year")
            obj_sales.product_type_gid = self.request.query_params.get("product_type_gid")
            obj_sales.product_gid = self.request.query_params.get("product_gid")
            obj_sales.employee_gid = self.request.query_params.get("Emp_Gid")
            plan_get = obj_sales.get_salesplanning()
            return Response({"MESSAGE": "FOUND", "DATA": json.loads(plan_get.to_json(orient='records'))})
        except Exception as e:
            return Response({"MESSAGE": "ERROR_OCCURED", "DATA": str(e)})


# --------------check_in and check_out---------------#
class Check_In_Check_Out(APIView):
    def post(self, request):
        try:
            if self.request.query_params.get("Group") == "EMPLOYEE_ACTIVITY":
                jsondata = json.loads(request.body.decode('utf-8'))
                obj_employee = mFET.FET_model()
                obj_employee.action = self.request.query_params.get("Action")
                obj_employee.type = self.request.query_params.get("Type")
                obj_employee.jsonData = json.dumps(jsondata.get('Params').get('HEADER'))
                obj_employee.jsondata = json.dumps(jsondata.get('Params').get('CLASSIFICATION'))
                obj_employee.create_by = self.request.query_params.get("Create_by")
                inv_out_message = obj_employee.set_check_in_check_out()
                if inv_out_message.get("MESSAGE") == 'SUCCESS':
                    ld_dict = {"MESSAGE": "SUCCESS"}
                elif inv_out_message.get("MESSAGE") == 'FAIL':
                    ld_dict = {"MESSAGE": inv_out_message.get("MESSAGE")}
                else:
                    ld_dict = {"MESSAGE": 'ERROR_OCCURED.' + inv_out_message.get("MESSAGE")}
                return Response(ld_dict)

            elif self.request.query_params.get("Group") == "SCHEDULED":
                jsondata = json.loads(request.body.decode('utf-8'))
                obj_employee = mFET.FET_model()
                obj_employee.action = self.request.query_params.get("Action")
                obj_employee.type = self.request.query_params.get("Type")
                obj_employee.jsonData = json.dumps(jsondata.get('Params').get('HEADER'))
                obj_employee.jsondata = json.dumps(jsondata.get('Params').get('CLASSIFICATION'))
                obj_employee.create_by = self.request.query_params.get("Create_by")
                inv_out_message = obj_employee.set_check_in_check_out()
                if inv_out_message.get("MESSAGE") == 'SUCCESS':
                    ld_dict = {"MESSAGE": "SUCCESS"}
                elif inv_out_message.get("MESSAGE") == 'FAIL':
                    ld_dict = {"MESSAGE": inv_out_message.get("MESSAGE")}
                else:
                    ld_dict = {"MESSAGE": 'ERROR_OCCURED.' + inv_out_message.get("MESSAGE")}
                return Response(ld_dict)

            elif self.request.query_params.get("Group") == "GET_CHECKIN_CHECKOUT_DATA":
                jsondata = json.loads(request.body.decode('utf-8'))
                obj_employee = mFET.FET_model()
                obj_employee.action = self.request.query_params.get("Action")
                obj_employee.type = self.request.query_params.get("Type")
                obj_employee.jsonData = json.dumps(jsondata.get('Params').get('FILTER'))
                obj_employee.json_classification = json.dumps(jsondata.get('Params').get('CLASSIFICATION'))
                ld_out_message = obj_employee.get_check_in_check_out()
                if ld_out_message.get("MESSAGE") == 'FOUND':
                    ld_dict = {"DATA": json.loads(ld_out_message.get("DATA").to_json(orient='records')),
                               "MESSAGE": "FOUND"}
                elif ld_out_message.get("MESSAGE") == 'NOT_FOUND':
                    ld_dict = {"MESSAGE": ld_out_message.get("MESSAGE")}
                else:
                    ld_dict = {"MESSAGE": 'ERROR_OCCURED.' + ld_out_message.get("MESSAGE")}

                return Response(ld_dict)


        except Exception as e:
            return Response({"MESSAGE": "ERROR_OCCURED", "DATA": str(e)})


# -------------------------------------------------------------------#

class sales_planningMIS(APIView):
    def get(self, request):
        try:
            object_sales = mSales.Sales_Model()
            object_sales.customer_gid = self.request.query_params.get("cust_gid")
            object_sales.from_date = self.request.query_params.get("fromyear")
            object_sales.to_date = self.request.query_params.get("toyear")
            object_sales.employee_gid = self.request.query_params.get("Emp_Gid")
            object_sales.product_gid = self.request.query_params.get("product_gid")
            object_sales.type = self.request.query_params.get("type")
            mis = object_sales.get_salesplanningmis()
            return Response({"MESSAGE": "FOUND", "DATA": json.loads(mis.to_json(orient='records'))})
        except Exception as e:
            return Response({"MESSAGE": "ERROR_OCCURED", "DATA": str(e)})


class sales_planning_history(APIView):
    def get(self, request):
        try:
            object_sales = mSales.Sales_Model()
            object_sales.from_date = self.request.query_params.get("fromdate")
            object_sales.to_date = self.request.query_params.get("todate")
            object_sales.customer_gid = self.request.query_params.get("cust_gid")
            object_sales.employee_gid = self.request.query_params.get("Emp_Gid")
            object_sales.entity_gid = self.request.query_params.get("entity_gid")
            object_sales.limit = self.request.query_params.get("limit")
            output = object_sales.get_salesplanning_historyget()
            return Response({"MESSAGE": "FOUND", "DATA": json.loads(output.to_json(orient='records'))})
        except Exception as e:
            return Response({"MESSAGE": "ERROR_OCCURED", "DATA": str(e)})


class sales_planning_Report(APIView):
    def get(self, request):
        try:
            object_sales = mSales.Sales_Model()
            object_sales.customer_gid = self.request.query_params.get("cust_gid")
            object_sales.from_date = self.request.query_params.get("fromyear")
            object_sales.to_date = self.request.query_params.get("toyear")
            object_sales.employee_gid = self.request.query_params.get("Emp_Gid")
            object_sales.product_gid = self.request.query_params.get("product_gid")
            object_sales.searchtype = self.request.query_params.get("searchtype")
            output = object_sales.get_salesplanning_reportget()
            return Response({"MESSAGE": "FOUND", "DATA": json.loads(output.to_json(orient='records'))})
        except Exception as e:
            return Response({"MESSAGE": "ERROR_OCCURED", "DATA": str(e)})


from Bigflow.Purchase.Model import mPurchase


class Purchase_request_API(APIView):
    def post(self, request):
        try:
            obj_prdata = mPurchase.Purchase_model()
            jsondata = json.loads(request.body.decode('utf-8'))
            prdetails = jsondata.get('params').get('prdetails')
            prheader_gid = prdetails[0].get('prheader_gid')
            # prdetail_details = jsondata.get('params').get('prdelete')
            # if prdetail_details != None:
            #     for x in prdetail_details:
            #         obj_prdata.prdetail_gid = x
            #         obj_prdata.Employee_gid = self.request.query_params.get("Employee_Gid")
            #         data = obj_prdata.set_prdelete()

            for y in prdetails:
                if prheader_gid == None:
                    obj_prdata.action = self.request.query_params.get("Action")
                    obj_prdata.date = datetime.datetime.now().strftime('%Y-%m-%d')
                    obj_prdata.Employee_gid = self.request.query_params.get("Employee_Gid")
                    obj_prdata.status = jsondata.get('params').get('status')
                    obj_prdata.branchcode = "1"
                    obj_prdata.mepnumber = ""
                    obj_prdata.totalamt = jsondata.get('params').get("pr_amt")
                    obj_prdata.commodity_gid = y.get('commdity_gid')
                    obj_prdata.entity_gid = self.request.query_params.get("entity_gid")
                    obj_prdata.create_by = self.request.query_params.get("Employee_Gid")
                    data = obj_prdata.set_prheader()[0].split(',')
                    if data != "Error":
                        # for x in prdetails:
                        obj_prdata.prheader_gid = data[0]
                        obj_prdata.product_gid = y.get('product_gid')
                        obj_prdata.product_qty = y.get('prdetails_qty')
                        obj_prdata.supplier_gid = "311"
                        # for local supplier gid =1 and for demo supplier gid=311
                        obj_prdata.Employee_gid = self.request.query_params.get("Employee_Gid")
                        obj_prdata.entity_gid = self.request.query_params.get("entity_gid")
                        data1 = obj_prdata.set_prdetails()[0].split(',')

                        # if obj_prdata.status == "Pending For Approval":
                        #     if data1[1] == "SUCCESS":
                        #         obj_prdata.action = 'Insert'
                        #         obj_prdata.ref_gid = 1
                        #         obj_prdata.reftable = obj_prdata.prheader_gid
                        #         obj_prdata.status = 'Pending For Approval'
                        #         obj_prdata.totype = 'I'
                        #         obj_prdata.to = 2
                        #         obj_prdata.remark = ''
                        #         tran = obj_prdata.set_trans()[0].split(',')
                        #         return Response({"MESSAGE": data1[1]})
                        #     else:
                        return Response({"MESSAGE": data1[1]})
                else:
                    obj_prdata.action = self.request.query_params.get("Action")
                    obj_prdata.prheader_gid = prheader_gid
                    obj_prdata.entity_gid = request.session['Entity_gid']
                    obj_prdata.create_by = request.session['Emp_gid']
                    data = obj_prdata.set_prheaderupdate()[0].split(',')
                    if data != "Error":
                        # for x in prdetails:
                        if y.get('prdetails_gid') == None:
                            obj_prdata.prheader_gid = prheader_gid
                            obj_prdata.product_gid = y.get('product_gid')
                            obj_prdata.product_qty = y.get('prdetails_qty')
                            obj_prdata.supplier_gid = "1"
                            obj_prdata.Employee_gid = self.request.query_params.get("Employee_Gid")
                            obj_prdata.entity_gid = self.request.query_params.get("entity_gid")
                            data1 = obj_prdata.set_prdetails()[0].split(',')
                            return Response({"MESSAGE": data1})
                        else:
                            obj_prdata.prdetail_gid = y.get('prdetails_gid')
                            obj_prdata.product_gid = y.get('product_gid')
                            obj_prdata.product_qty = y.get('prdetails_qty')
                            obj_prdata.supplier_gid = "1"
                            data1 = obj_prdata.set_prdetailupdate()[0].split(',')
                            return Response({"MESSAGE": data1})
                        #
                        # if obj_prdata.status == "Pending For Approval":
                        #     if data1[1] == "SUCCESS":
                        #         obj_prdata.action = 'Insert'
                        #         obj_prdata.ref_gid = 1
                        #         obj_prdata.reftable = obj_prdata.prheader_gid
                        #         obj_prdata.status = 'Pending For Approval'
                        #         obj_prdata.totype = 'I'
                        #         obj_prdata.to = 2
                        #         obj_prdata.remark = ''
                        #         tran = obj_prdata.set_trans()[0].split(',')
                        #
                        #         return Response({"MESSAGE": data1[1]})
                        #
                        #     else:
                        #         return Response({"MESSAGE": data})

        except Exception as e:
            return Response({"MESSAGE": "ERROR_OCCURED", "DATA": str(e)})


#### Scan and Save Files

class File_Save(APIView):
    def post(self, request):
        try:
            if self.request.query_params.get("Group") == 'SCAN_IMAGE_BARCODE':
                obj_file = mInvoice.inward_model
                jsondata = json.loads(request.body.decode('utf-8'))
                obj_file.json_file = json.dumps(jsondata.get('Params').get('File'))
                obj_file.pdf_name = self.request.query_params.get("pdf_name")
                obj_file.employee_gid = self.request.query_params.get("Employee_Gid")
                obj_file.entity = self.request.query_params.get("entity")
                file_list = json.loads(obj_file.json_file)
                if len(file_list) != 0:
                    lst_saved_file_list = []
                    for i in range(len(file_list)):
                        file_json = file_list[i]
                        file_data = file_json.get('File_Base64data')
                        file_data = base64.b64decode(file_data)
                        file_name = file_json.get('File_Name')
                        file_extension = file_json.get('File_Extension')
                        file_name_new = obj_file.employee_gid + '_' + file_name + str(
                            datetime.datetime.now().strftime("%y%m%d_%H%M%S"))
                        current_month = datetime.datetime.now().strftime('%m')
                        current_day = datetime.datetime.now().strftime('%d')
                        current_year_full = datetime.datetime.now().strftime('%Y')
                        # /media/  is the MEDIA_URL
                        lsfile_name = str((settings.MEDIA_ROOT) + '/INWARD/' + str(current_year_full) + '/' + str(
                            current_month) + '/' + str(current_day) + '/' + file_name_new + '.' + file_extension)
                        lsfile_name_db = "/media/INWARD/" + str(current_year_full) + '/' + str(
                            current_month) + '/' + str(current_day) + '/' + file_name_new + '.' + file_extension
                        path = Path(lsfile_name)
                        path.parent.mkdir(parents=True, exist_ok=True)
                        with open(lsfile_name, 'wb') as f:
                            f.write(file_data)
                            ld_saved_file = {"SavedFilePath": lsfile_name, "File_Name": file_name}
                            lst_saved_file_list.append(ld_saved_file)
                            inward_dtl = mAP.ap_model()
                            inward_dtl.action = 'UPDATE'
                            inward_dtl.type = 'FILE'
                            inward_dtl.header_json = {}
                            inward_dtl.debit_json = {}
                            inward_dtl.detail_json = {}
                            inward_dtl.status_json = {"Barcode_Name": file_name, "File_name": lsfile_name_db}
                            inward_dtl.entity_gid = obj_file.entity
                            inward_dtl.employee_gid = obj_file.employee_gid
                            # print(inward_dtl.status_json)
                            out = inward_dtl.set_Invoiceheader()[0].split(',')
            return out

            # return lsfile_name_db  ### Wip for Multiple Files
        except Exception as e:
            return Response({"MESSAGE": "ERROR_OCCURED", "DATA": str(e)})


# def File_Upload_Barcode(file_list, dir_folder, emp_id):
#         file_list = json.loads(file_list)
#         if len(file_list) != 0:
#             lst_saved_file_list = []
#             for i in range(len(file_list)):
#                 file_json = file_list[i]
#                 file_data = file_json.get('File_Base64data')
#                 file_data = base64.b64decode(file_data)
#                 file_name = file_json.get('File_Name')
#                 file_extension = file_json.get('File_Extension')
#                 file_name_new = emp_id + '_' + str(datetime.datetime.now().strftime("%y%m%d_%H%M%S"))
#                 current_month = datetime.datetime.now().strftime('%m')
#                 current_day = datetime.datetime.now().strftime('%d')
#                 current_year_full = datetime.datetime.now().strftime('%Y')
#                 # /media/  is the MEDIA_URL
#                 lsfile_name = str((BASE_DIR + '/Bigflow' + "/media/" + dir_folder + '/'
#                                    + str(current_year_full) + '/' + str(current_month) + '/' + str(
#                             current_day) + '/' +
#                                    file_name_new + '.' + file_extension))
#                 ### Added Newly
#                 lsfile_name_db = str((MEDIA_URL + dir_folder + '/'
#                                       + str(current_year_full) + '/' + str(current_month) + '/' + str(
#                             current_day) + '/' +
#                                       file_name_new + '.' + file_extension))
#                 path = Path(lsfile_name)
#                 path.parent.mkdir(parents=True, exist_ok=True)
#                 with open(lsfile_name, 'wb') as f:
#                     f.write(file_data)
#                     ld_saved_file = {"SavedFilePath": lsfile_name_db, "File_Name": file_name}
#                     lst_saved_file_list.append(ld_saved_file)
#                     # inward_dtl = mAP.ap_model()
#                     # inward_dtl.action = 'UPDATE'
#                     # inward_dtl.type = 'FILE'
#                     # inward_dtl.header_json = {}
#                     # inward_dtl.debit_json = {}
#                     # inward_dtl.detail_json = {}
#                     # inward_dtl.status_json = {"Barcode_Name": file_name , "File_name":  lsfile_name_db  }
#                     # inward_dtl.entity_gid = 1
#                     # inward_dtl.employee_gid = 1
#                     # print(inward_dtl.status_json)
#                     # out = inward_dtl.set_Invoiceheader()[0].split(',')
#             # return Response({"MESSAGE": out})
#
#             return lsfile_name_db  ### Wip for Multiple Files

class State_Process_Set(APIView):
    def post(self, request):
        try:
            if self.request.query_params.get("Action") == "insert":
                pro_exp = mMasters.Masters()
                pro_exp.Action = self.request.query_params.get('Action')
                pro_exp.City = json.dumps(self.request.data)
                pro_exp.Entity_gid = decry_data(self.request.query_params.get('Entity_gid'))
                pro_exp.Emp_gid = decry_data(self.request.query_params.get('Emp_gid'))
                pro_results = pro_exp.set_citys()
                return Response(pro_results)
            elif self.request.query_params.get("Action") == "Insert":
                pro_exp = mMasters.Masters()
                pro_exp.Action = self.request.query_params.get('Action')
                pro_exp.Type = self.request.query_params.get('Type')
                pro_exp.filter = json.dumps(self.request.data.get('filter'))
                clasification = decry_data(self.request.data.get('classification')['Entity_gid'])
                pro_exp.classification = json.dumps({'Entity_gid': clasification})
                pro_exp.Emp_gid = decry_data(self.request.query_params.get('Emp_gid'))
                pro_results = pro_exp.set_state()
                pro_results = pro_results[0]
                if pro_results == "SUCCESS":
                    return Response("SUCCESS")
                else:
                    return Response("FAIL")
        except Exception as e:
            return Response({"MESSAGE": "ERROR_OCCURED", "DATA": str(e)})


class prod_spec(APIView):
    def post(self, request):
        try:
            if self.request.query_params.get("Action") == "INSERT":
                pro_exp = mMasters.Masters()
                pro_exp.action = self.request.query_params.get('Action')
                pro_exp.jsondata = json.dumps(self.request.data.get('DATA'))
                entity = decry_data(self.request.data.get('Classification')['Entity_Gid'])
                create_by = decry_data(self.request.data.get('Classification')['Create_By'])
                pro_exp.classification = json.dumps({'Entity_Gid': entity,"Create_By":create_by})
                pro_results = pro_exp.set_spec_template()
                return Response(pro_results)
            elif self.request.query_params.get("Action") == "productspecification_Get":
                pro_exp = mMasters.Masters()
                pro_exp.action = self.request.query_params.get('Action')
                pro_exp.jsondata = json.dumps(self.request.data.get('DATA'))
                clasification = decry_data(self.request.data.get('Classification')['Entity_Gid'])
                pro_exp.classification = json.dumps({'Entity_Gid': clasification})
                pro_results = pro_exp.get_spec_template()
                ld_dict = {"DATA": json.loads(pro_results.to_json(orient='records')),
                           "MESSAGE": 'FOUND'}
                return Response(ld_dict)
        except Exception as e:
            return Response({"MESSAGE": "ERROR_OCCURED", "DATA": str(e)})

class Commondropdown(APIView):
    def post(self, request):
        try:
            if self.request.query_params.get("Group") == "COMMON_DROPDOWN":
                jsondata = json.loads(request.body.decode('utf-8'))
                obj_dropdown = mMasters.Masters()
                obj_dropdown.table_name = jsondata.get('Params').get('FILTER').get('Table_name')
                obj_dropdown.gid = jsondata.get('Params').get('FILTER').get('Search_gid')
                obj_dropdown.name = jsondata.get('Params').get('FILTER').get('Search_name')
                obj_dropdown.entity_gid = jsondata.get('Params').get('CLASSIFICATION').get('Entity_gid')
                ld_out_message = {"DATA": obj_dropdown.get_ddl()}
                ld_dict = {"DATA": json.loads(ld_out_message.get("DATA").to_json(orient='records')),
                           "MESSAGE": 'FOUND'}
                return Response(ld_dict)
        except Exception as e:
            return Response({"MESSAGE": "ERROR_OCCURED", "DATA": str(e)})

from rest_framework_simplejwt.serializers import TokenObtainPairSerializer,TokenVerifySerializer
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,TokenVerifyView
)
from Bigflow.Core import class1

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):

        # The default result (access/refresh tokens)
      #  data = super(CustomTokenObtainPairSerializer, self).validate(attrs)
        # Custom data you want to include
        common.logger.error([{"LG_APIJ_ATTR": str(attrs)[0:10]}])
        data = super().validate(attrs)
        common.logger.error([{"LG_APIJ_DATA": str(data)[0:10]}])

        refresh = self.get_token(self.user)
        try:
            if (self.context['request'].data['apitype']) == 'Indirect' :

                obj_location = class1.login()
                obj_location.code = (self.context['request'].data['employee_id'])
                obj_location.password = (self.context['request'].data['employee_pwd'])
                result = obj_location.get_login()
                if result[1][0] == 'SUCCESS':
                    data["refresh"] = str(refresh)
                    data["access"] = str(refresh.access_token)
                    return data
                else :
                    return {"Error":"Fail In Login"}
            elif (self.context['request'].data['apitype']) == 'Direct':
                datenow = str(datetime.datetime.now().strftime("%Y-%m-%d"))
                password = 'vsolv33'
                password = datenow+password[::-1]
                password = class1.converttoascii(password)
                auth_pwd = self.context['request'].data['auth_pwd']
                common.logger.error([{"LG_APIJ_Pass": str(password)[0:5]}])
                common.logger.error([{"LG_APIJ_AuthPass": str(auth_pwd)[0:5]}])
                if password != auth_pwd:
                    data["refresh"] = str(refresh)
                    data["access"] = str(refresh.access_token)
                    return data
                else:
                    return {"Error": "Authentication Failed."}
            else:
                return {"Error": "Enter Valid Type"}
        except Exception as e:
            return ({"MESSAGE": "ERROR_OCCURED", "DATA": str(e)})

class CustomTokenverifySerializer(TokenVerifySerializer):
    def validate(self, attrs):
        verify= TokenVerifySerializer.validate(self,attrs)

        return verify

def deff():
    TokenVerifySerializer().validate()



class CustomTokenObtainPairView(TokenObtainPairView):
    # Replace the serializer with your custom
    serializer_class = CustomTokenObtainPairSerializer
token_refresh = TokenRefreshView.as_view()

class verifyToken(TokenVerifyView):
    # Replace the serializer with your custom
    serializer_class = CustomTokenverifySerializer
