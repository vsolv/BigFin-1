import sys
from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework.views import Response
import json
from Bigflow.API import views as commonview
from Bigflow.eClaim.model import meClaim
import Bigflow.Core.jwt_file as jwt
from Bigflow.eClaim import eClaim_verify as verify
from Bigflow.eClaim import android_interface as android
from Bigflow.settings import BASE_DIR,S3_BUCKET_NAME
import Bigflow.Core.models as common
ip = common.localip()
import requests
import boto3
import datetime
from datetime import date
import json
from django.http import HttpResponse
import pandas as pd

# today = date.today()
# from datetime import datetime
# import pytz
# IST = pytz.timezone('Asia/Kolkata')
# datetime_ist = datetime.now(IST)
# today_date = datetime_ist.strftime('%Y-%m-%d')

class eClaim_Master(APIView):
    def post(self,request):
        try:
            if self.request.query_params.get("Group") == "ECLAIM_MASTER_GET":
                jsondata = json.loads(request.body.decode('utf-8'))
                obj_fa = meClaim.eClaim_Model()
                obj_fa.type = self.request.query_params.get("Type")
                obj_fa.sub_type = self.request.query_params.get("Sub_Type")
                obj_fa.filter_json = json.dumps(jsondata.get('Params').get('FILTER'))
                obj_fa.json_classification = json.dumps(jsondata.get('Params').get('CLASSIFICATION'))
                ld_out_message = obj_fa.get_eClaim_Master()
                if ld_out_message.get("MESSAGE") == 'FOUND':
                    ld_dict = {"DATA": json.loads(ld_out_message.get("DATA").to_json(orient='records')),
                               "MESSAGE": 'FOUND'}
                elif ld_out_message.get("MESSAGE") == 'NOT_FOUND':
                    ld_dict = {"MESSAGE": 'NOT_FOUND'}
                else:
                    ld_dict = {"MESSAGE": 'ERROR_OCCURED.' + ld_out_message.get("MESSAGE")}
                return Response(ld_dict)
            elif self.request.query_params.get("Group") == "ECLAIM_MASTER_SET":
                jsondata = json.loads(request.body.decode('utf-8'))
                obj_eC = meClaim.eClaim_Model()
                obj_eC.action = self.request.query_params.get("Action")
                obj_eC.type = self.request.query_params.get("Type")
                obj_eC.sub_type = self.request.query_params.get("Sub_Type")
                obj_eC.employee_gid = self.request.query_params.get("Employee_Gid")
                obj_eC.jsondata = json.dumps(jsondata.get('Params').get('DETAILS'))
                obj_eC.json_classification = json.dumps(jsondata.get('Params').get('CLASSIFICATION'))
                ld_out_message = obj_eC.set_eClaim_Master()
                if ld_out_message.get("MESSAGE") == 'SUCCESS':
                    ld_dict = {"MESSAGE": "SUCCESS"}
                elif ld_out_message.get("MESSAGE") == 'FAIL':
                    ld_dict = {"MESSAGE": "FAIL"}
                else:
                    ld_dict = {"MESSAGE": 'ERROR_OCCURED.' + ld_out_message.get("MESSAGE")}
                return Response(ld_dict)
        except Exception as e:
            return Response({"MESSAGE": "ERROR_OCCURED", "DATA": str(e)})

class eClaim_Summary(APIView):
    def post(self,request):
        try:
            if self.request.query_params.get("Type") == "CLAIM_REQUEST":
                ld_out_message = ""
                if request.query_params.get("Api_Type") =="ANDROID":
                    filter = android.Android.post_summary(self,request)
                    obj_eclaim = meClaim.eClaim_Model()
                    obj_eclaim.filter_json = json.dumps(filter)
                    ld_out_message = obj_eclaim.eClaim_request_get()
                elif request.query_params.get("Api_Type") =="WEB":
                    jsondata = json.loads(request.body.decode('utf-8'))
                    obj_eclaim = meClaim.eClaim_Model()
                    obj_eclaim.filter_json = json.dumps(jsondata.get('Params').get('FILTER'))
                    ld_out_message = obj_eclaim.eClaim_request_get()
                if ld_out_message.get("MESSAGE") == 'FOUND':
                    data = json.loads(ld_out_message.get("DATA").to_json(orient='records'))
                    obj_eclaim = meClaim.eClaim_Model()
                    permit_gid = []
                    appcl_gid = []
                    appad_gid = []
                    emp_gid = data[0].get('empgid')
                    for i in data:
                        if i.get('approvedby') not in permit_gid and i.get('approvedby') != 0:
                            permit_gid.append(i.get('approvedby'))
                        if i.get('approvedby_cl') not in appcl_gid and i.get('approvedby_cl') != 0:
                            appcl_gid.append(i.get('approvedby_cl'))
                        if i.get('approvedby_ad') not in appad_gid and i.get('approvedby_ad') != 0:
                            appad_gid.append(i.get('approvedby_ad'))
                    emp_data = {
                        "empids" : emp_gid
                    }
                    obj_eclaim.filter_json = json.dumps(emp_data)
                    obj_eclaim.json_classification = json.dumps({})
                    emp_out_message = obj_eclaim.eClaim_employeename_get()
                    employee_data = json.loads(emp_out_message.get("DATA").to_json(orient='records'))
                    empprmit_data = {
                        "empids": permit_gid
                    }
                    obj_eclaim.filter_json = json.dumps(empprmit_data)
                    obj_eclaim.json_classification = json.dumps({})
                    permit_out_message = obj_eclaim.eClaim_employeename_get()
                    permit_data = json.loads(permit_out_message.get("DATA").to_json(orient='records'))
                    empcl_dict = {
                        "empids": appcl_gid
                    }
                    obj_eclaim.filter_json = json.dumps(empcl_dict)
                    obj_eclaim.json_classification = json.dumps({})
                    appcl_data_message = obj_eclaim.eClaim_employeename_get()
                    appcl_data = json.loads(appcl_data_message.get("DATA").to_json(orient='records'))
                    empad_dict = {
                        "empids": appad_gid
                    }
                    obj_eclaim.filter_json = json.dumps(empad_dict)
                    obj_eclaim.json_classification = json.dumps({})
                    appad_data_message = obj_eclaim.eClaim_employeename_get()
                    appad_data = json.loads(appad_data_message.get("DATA").to_json(orient='records'))
                    for d in data:
                        d["employee_name"] = employee_data[0].get('employee_name')
                        d["employee_code"] = employee_data[0].get('employee_code')
                        d["designation"] = employee_data[0].get('designation_name')
                        d["gstno"] = employee_data[0].get('gstno')
                    for d in data:
                        for i in range(0, len(permit_data)):
                            if permit_data[i].get('employee_gid') == int(d.get('approvedby')):
                                d["permit_byname"] = permit_data[i].get('employee_name')
                                d["permit_bycode"] = permit_data[i].get('employee_code')
                                break
                        for i in range(0, len(appcl_data)):
                            if appcl_data[i].get('employee_gid') == int(d.get('approvedby_cl')):
                                d["appcl_byname"] = appcl_data[i].get('employee_name')
                                d["appcl_bycode"] = appcl_data[i].get('employee_code')
                                break
                        for i in range(0, len(appad_data)):
                            if appad_data[i].get('employee_gid') == int(d.get('approvedby_ad')):
                                d["appad_byname"] = appad_data[i].get('employee_name')
                                d["appad_bycode"] = appad_data[i].get('employee_code')
                                break
                    ld_dict = {"DATA": data,"MESSAGE": 'FOUND',"STATUS":0}
                elif ld_out_message.get("MESSAGE") == 'NOT_FOUND':
                    ld_dict = {"MESSAGE": 'NOT_FOUND',"STATUS":1}
                else:
                    ld_dict = {"MESSAGE": 'ERROR_OCCURED.' + ld_out_message.get("MESSAGE"),"STATUS":1}
                return Response(ld_dict)
            elif self.request.query_params.get("Type") == "CLAIM_EXPENSE":
                obj_fa = meClaim.eClaim_Model()
                obj_fa.type = self.request.query_params.get("Type")
                ld_out_message = obj_fa.eClaim_expense_get()
                if json.loads(ld_out_message.get("DATA").to_json(orient='records')):
                    ld_dict = {"DATA": json.loads(ld_out_message.get("DATA").to_json(orient='records')),
                               "MESSAGE": 'FOUND    '}
                elif ld_out_message.get("MESSAGE") == 'NOT_FOUND':
                    ld_dict = {"MESSAGE": 'NOT_FOUND'}
                else:
                    ld_dict = {"MESSAGE": 'ERROR_OCCURED.' + ld_out_message.get("MESSAGE")}
                return Response(ld_dict)
            elif self.request.query_params.get("Type") == "CLAIMED_EXPENSE":
                jsondata = json.loads(request.body.decode('utf-8'))
                obj_eclaim = meClaim.eClaim_Model()
                obj_eclaim.filter_json = json.dumps(jsondata.get('Params').get('FILTER'))
                ld_out_message = obj_eclaim.eClaim_claimedexpense_get()
                if ld_out_message.get("MESSAGE") == 'FOUND':
                    obj_eclaim.employee_gid = jsondata.get('Params').get('FILTER').get('Claimrequest_Tourgid')
                    ld_out_file = obj_eclaim.eClaim_file_get()
                    out_data = json.loads(ld_out_message.get("DATA").to_json(orient='records'))
                    if out_data[0].get('approvedby') != 0:
                        emp_data = {
                            "empids": out_data[0].get('approvedby')
                        }
                        obj_eclaim.filter_json = json.dumps(emp_data)
                        obj_eclaim.json_classification = json.dumps(jsondata.get('Params').get('CLASSIFICATION'))
                        emp_out_message = obj_eclaim.eClaim_employee_get()
                        employee_data = json.loads(emp_out_message.get("DATA").to_json(orient='records'))
                        for d in out_data:
                            d["forwarder_name"] = employee_data[0].get('employee_name')
                            d["forwarder_code"] = employee_data[0].get('employee_code')
                            d["forwarder_branch"] = employee_data[0].get('branch_name')
                    if out_data[0].get('approvedby_fr') != 0:
                        emp_data = {
                            "empids": out_data[0].get('approvedby_fr')
                        }
                        obj_eclaim.filter_json = json.dumps(emp_data)
                        obj_eclaim.json_classification = json.dumps(jsondata.get('Params').get('CLASSIFICATION'))
                        emp_out_message = obj_eclaim.eClaim_employee_get()
                        employee_data = json.loads(emp_out_message.get("DATA").to_json(orient='records'))
                        for d in out_data:
                            d["approver_name"] = employee_data[0].get('employee_name')
                            d["approver_code"] = employee_data[0].get('employee_code')
                            d["approver_branch"] = employee_data[0].get('branch_name')

                    file = json.loads(ld_out_file.get("DATA").to_json(orient='records'))
                    filedata =[]
                    if len(file) != 0:
                        for i in file:
                            s3_client = boto3.client('s3','ap-south-1')
                            response = s3_client.generate_presigned_url('get_object',
                                                                        Params={'Bucket': S3_BUCKET_NAME,
                                                                                'Key': i.get('file_path')},
                                                                        ExpiresIn=None)
                            data ={
                                "file_gid":i.get('file_gid'),
                                "file_name":i.get('file_name'),
                                "file_path":response,
                                "file_refgid":i.get('file_refgid')
                            }
                            filedata.append(data)

                    ld_dict = {
                        "DATA": out_data,
                        "FILE": filedata,
                        "MESSAGE": 'FOUND'}
                elif ld_out_message.get("MESSAGE") == 'NOT_FOUND':
                    ld_dict = {"MESSAGE": 'NOT_FOUND'}
                else:
                    ld_dict = {"MESSAGE": 'ERROR_OCCURED.' + ld_out_message.get("MESSAGE")}
                return Response(ld_dict)
            elif self.request.query_params.get("Type") == "DLYDM":
                jsondata = json.loads(request.body.decode('utf-8'))
                obj_fa = meClaim.eClaim_Model()
                obj_fa.filter_json = json.dumps(jsondata.get('Params').get('FILTER'))
                ld_out_message = obj_fa.eClaim_dailydiem_get()
                if ld_out_message.get("MESSAGE") == 'FOUND':
                    token = str(request.auth.token)
                    tk = "Bearer  " + token[2:len(token)-1]
                    dict = verify.ccbs(self, json.loads(ld_out_message.get("DATA").to_json(orient='records')),jsondata.get('Params').get('FILTER').get('Entity_Gid_d'),tk)
                    ld_dict = {"DATA": dict,"MESSAGE": 'FOUND'}
                elif ld_out_message.get("MESSAGE") == 'NOT_FOUND':
                    ld_dict = {"MESSAGE": 'NOT_FOUND'}
                else:
                    ld_dict = {"MESSAGE": 'ERROR_OCCURED.' + ld_out_message.get("MESSAGE")}
                return Response(ld_dict)
            elif self.request.query_params.get("Type") == "LODG":
                jsondata = json.loads(request.body.decode('utf-8'))
                obj_fa = meClaim.eClaim_Model()
                obj_fa.filter_json = json.dumps(jsondata.get('Params').get('FILTER'))
                ld_out_message = obj_fa.eClaim_lodging_get()
                if ld_out_message.get("MESSAGE") == 'FOUND':
                    dict = verify.hsnget.hsndata(self, json.loads(ld_out_message.get("DATA").to_json(orient='records')))
                    ld_dict = {"DATA": dict, "MESSAGE": 'FOUND'}
                elif ld_out_message.get("MESSAGE") == 'NOT_FOUND':
                    ld_dict = {"MESSAGE": 'NOT_FOUND'}
                else:
                    ld_dict = {"MESSAGE": 'ERROR_OCCURED.' + ld_out_message.get("MESSAGE")}
                return Response(ld_dict)
            elif self.request.query_params.get("Type") == "LCONV":
                jsondata = json.loads(request.body.decode('utf-8'))
                obj_fa = meClaim.eClaim_Model()
                obj_fa.filter_json = json.dumps(jsondata.get('Params').get('FILTER'))
                ld_out_message = obj_fa.eClaim_loccon_get()
                if ld_out_message.get("MESSAGE") == 'FOUND':
                    token = str(request.auth.token)
                    tk = "Bearer  " + token[2:len(token) - 1]
                    dict = verify.ccbs(self, json.loads(ld_out_message.get("DATA").to_json(orient='records')),
                                       jsondata.get('Params').get('FILTER').get('Entity_Gid_d'), tk)
                    ld_dict = {"DATA": dict, "MESSAGE": 'FOUND'}
                elif ld_out_message.get("MESSAGE") == 'NOT_FOUND':
                    ld_dict = {"MESSAGE": 'NOT_FOUND'}
                else:
                    ld_dict = {"MESSAGE": 'ERROR_OCCURED.' + ld_out_message.get("MESSAGE")}
                return Response(ld_dict)
            elif self.request.query_params.get("Type") == "MISC":
                jsondata = json.loads(request.body.decode('utf-8'))
                obj_fa = meClaim.eClaim_Model()
                obj_fa.filter_json = json.dumps(jsondata.get('Params').get('FILTER'))
                ld_out_message = obj_fa.eClaim_miscellaneous_get()
                if ld_out_message.get("MESSAGE") == 'FOUND':
                    token = str(request.auth.token)
                    tk = "Bearer  " + token[2:len(token) - 1]
                    dict = verify.ccbs(self, json.loads(ld_out_message.get("DATA").to_json(orient='records')),
                                       jsondata.get('Params').get('FILTER').get('Entity_Gid_d'), tk)
                    ld_dict = {"DATA": dict, "MESSAGE": 'FOUND'}
                elif ld_out_message.get("MESSAGE") == 'NOT_FOUND':
                    ld_dict = {"MESSAGE": 'NOT_FOUND'}
                else:
                    ld_dict = {"MESSAGE": 'ERROR_OCCURED.' + ld_out_message.get("MESSAGE")}
                return Response(ld_dict)
            elif self.request.query_params.get("Type") == "PCKG":
                jsondata = json.loads(request.body.decode('utf-8'))
                obj_fa = meClaim.eClaim_Model()
                obj_fa.filter_json = json.dumps(jsondata.get('Params').get('FILTER'))
                ld_out_message = obj_fa.eClaim_packingmoving_get()
                if ld_out_message.get("MESSAGE") == 'FOUND':
                    dict = verify.hsnget.hsndata(self, json.loads(ld_out_message.get("DATA").to_json(orient='records')))
                    ld_dict = {"DATA": dict, "MESSAGE": 'FOUND'}
                elif ld_out_message.get("MESSAGE") == 'NOT_FOUND':
                    ld_dict = {"MESSAGE": 'NOT_FOUND'}
                else:
                    ld_dict = {"MESSAGE": 'ERROR_OCCURED.' + ld_out_message.get("MESSAGE")}
                return Response(ld_dict)
            elif self.request.query_params.get("Type") == "TRVL":
                jsondata = json.loads(request.body.decode('utf-8'))
                obj_fa = meClaim.eClaim_Model()
                obj_fa.filter_json = json.dumps(jsondata.get('Params').get('FILTER'))
                ld_out_message = obj_fa.eClaim_travelexp_get()
                if ld_out_message.get("MESSAGE") == 'FOUND':
                    dict = verify.hsnget.hsndata(self, json.loads(ld_out_message.get("DATA").to_json(orient='records')))
                    ld_dict = {"DATA": dict, "MESSAGE": 'FOUND'}
                elif ld_out_message.get("MESSAGE") == 'NOT_FOUND':
                    ld_dict = {"MESSAGE": 'NOT_FOUND'}
                else:
                    ld_dict = {"MESSAGE": 'ERROR_OCCURED.' + ld_out_message.get("MESSAGE")}
                return Response(ld_dict)
            elif self.request.query_params.get("Type") == "INCDL":
                jsondata = json.loads(request.body.decode('utf-8'))
                obj_fa = meClaim.eClaim_Model()
                obj_fa.filter_json = json.dumps(jsondata.get('Params').get('FILTER'))
                ld_out_message = obj_fa.eClaim_incidental_get()
                if ld_out_message.get("MESSAGE") == 'FOUND':
                    token = str(request.auth.token)
                    tk = "Bearer  " + token[2:len(token) - 1]
                    dict = verify.ccbs(self, json.loads(ld_out_message.get("DATA").to_json(orient='records')),
                                       jsondata.get('Params').get('FILTER').get('Entity_Gid_d'), tk)
                    ld_dict = {"DATA": dict, "MESSAGE": 'FOUND'}
                elif ld_out_message.get("MESSAGE") == 'NOT_FOUND':
                    ld_dict = {"MESSAGE": 'NOT_FOUND'}
                else:
                    ld_dict = {"MESSAGE": 'ERROR_OCCURED.' + ld_out_message.get("MESSAGE")}
                return Response(ld_dict)
            elif self.request.query_params.get("Type") == "EMP_BRANCH":
                jsondata = json.loads(request.body.decode('utf-8'))
                obj_fa = meClaim.eClaim_Model()
                obj_fa.filter_json = json.dumps(jsondata.get('Params').get('FILTER'))
                ld_out_message = obj_fa.eClaim_branchtoemp_get()
                if ld_out_message.get("MESSAGE") == 'FOUND':
                    ld_dict = {"DATA": json.loads(ld_out_message.get("DATA").to_json(orient='records')),
                               "MESSAGE": 'FOUND    '}
                elif ld_out_message.get("MESSAGE") == 'NOT_FOUND':
                    ld_dict = {"MESSAGE": 'NOT_FOUND'}
                else:
                    ld_dict = {"MESSAGE": 'ERROR_OCCURED.' + ld_out_message.get("MESSAGE")}
                return Response(ld_dict)
            elif self.request.query_params.get("Type") == "APPROVER_LIST":
                jsondata = json.loads(request.body.decode('utf-8'))
                obj_eclaim = meClaim.eClaim_Model()
                obj_eclaim.filter_json = json.dumps(jsondata.get('Params').get('FILTER'))
                ld_out_message = obj_eclaim.eClaim_approverlist_get()
                if ld_out_message.get("MESSAGE") == 'FOUND':
                    data = json.loads(ld_out_message.get("DATA").to_json(orient='records'))
                    emp_gid = []
                    for i in data:
                        emp_gid.append(i.get('employeegid'))
                    emp_data = {
                        "empids": emp_gid
                    }
                    obj_eclaim.filter_json = json.dumps(emp_data)
                    emp_out_message = obj_eclaim.eClaim_employeename_get()
                    employee_data = json.loads(emp_out_message.get("DATA").to_json(orient='records'))
                    for d in data:
                        for i in range(0, len(employee_data)):
                            if employee_data[i].get('employee_gid') == int(d.get('employeegid')):
                                d["employee_name"] = employee_data[i].get('employee_name')
                                d["employee_code"] = employee_data[i].get('employee_code')
                                d["employee_gid"] = d.get('employeegid')
                                break
                    ld_dict = {"DATA": data,
                               "MESSAGE": 'FOUND'}
                elif ld_out_message.get("MESSAGE") == 'NOT_FOUND':
                    ld_dict = {"MESSAGE": 'NOT_FOUND'}
                else:
                    ld_dict = {"MESSAGE": 'ERROR_OCCURED.' + ld_out_message.get("MESSAGE")}
                return Response(ld_dict)
            elif self.request.query_params.get("Type") == "GET_BRANCH":
                jsondata = json.loads(request.body.decode('utf-8'))
                obj_fa = meClaim.eClaim_Model()
                obj_fa.filter_json = json.dumps(jsondata.get('Params').get('FILTER'))
                ld_out_message = obj_fa.eClaim_branch_get()
                if ld_out_message.get("MESSAGE") == 'FOUND':
                    ld_dict = {"DATA": json.loads(ld_out_message.get("DATA").to_json(orient='records')),
                               "MESSAGE": 'FOUND    '}
                elif ld_out_message.get("MESSAGE") == 'NOT_FOUND':
                    ld_dict = {"MESSAGE": 'NOT_FOUND'}
                else:
                    ld_dict = {"MESSAGE": 'ERROR_OCCURED.' + ld_out_message.get("MESSAGE")}
                return Response(ld_dict)
            elif self.request.query_params.get("Type") == "GET_CITY":
                jsondata = json.loads(request.body.decode('utf-8'))
                obj_fa = meClaim.eClaim_Model()
                obj_fa.filter_json = json.dumps(jsondata.get('Params').get('FILTER'))
                ld_out_message = obj_fa.eClaim_expensecity_get()
                if ld_out_message.get("MESSAGE") == 'FOUND':
                    ld_dict = {"DATA": json.loads(ld_out_message.get("DATA").to_json(orient='records')),
                               "MESSAGE": 'FOUND    '}
                elif ld_out_message.get("MESSAGE") == 'NOT_FOUND':
                    ld_dict = {"MESSAGE": 'NOT_FOUND'}
                else:
                    ld_dict = {"MESSAGE": 'ERROR_OCCURED.' + ld_out_message.get("MESSAGE")}
                return Response(ld_dict)
            elif self.request.query_params.get("Type") == "GET_APPROVAL":
                jsondata = json.loads(request.body.decode('utf-8'))
                obj_eclaim = meClaim.eClaim_Model()
                ld_out_message = ""
                if request.query_params.get("Api_Type") == "ANDROID":
                    filter = android.Android.post_summary(self, request)
                    filter['approvedby'] = filter.get('Employee_gid')
                    obj_eclaim.filter_json = json.dumps(filter)
                    ld_out_message = obj_eclaim.eClaim_approval_get()
                elif request.query_params.get("Api_Type") == "WEB":
                    data =  jsondata.get('Params').get('FILTER')
                    data['approvedby'] = data.get('Employee_gid')
                    obj_eclaim.filter_json = json.dumps(data)
                    ld_out_message = obj_eclaim.eClaim_approval_get()
                if ld_out_message.get("MESSAGE") == 'FOUND':
                    data = json.loads(ld_out_message.get("DATA").to_json(orient='records'))
                    emp_gid = []
                    for i in data:
                        if i.get('empgid') not in emp_gid and i.get('empgid') != 0:
                            emp_gid.append(i.get('empgid'))
                    emp_data = {
                        "empids": emp_gid
                    }
                    obj_eclaim.filter_json = json.dumps(emp_data)
                    obj_eclaim.json_classification = '{}'
                    emp_out_message = obj_eclaim.eClaim_employee_get()
                    employee_data = json.loads(emp_out_message.get("DATA").to_json(orient='records'))
                    for d in data:
                        for i in range(0, len(employee_data)):
                            if employee_data[0].get('employee_gid') == d.get('empgid'):
                                d["employee_name"] = employee_data[0].get('employee_name')
                                d["employee_code"] = employee_data[0].get('employee_code')
                                d["designation"] = employee_data[0].get('designation_name')
                                d["gstno"] = employee_data[0].get('gstno')
                                break
                    ld_dict = {"DATA": data,"MESSAGE": 'FOUND',"STATUS":0}

                elif ld_out_message.get("MESSAGE") == 'NOT_FOUND':
                    ld_dict = {"MESSAGE": 'NOT_FOUND',"STATUS":1}
                else:
                    ld_dict = {"MESSAGE": 'ERROR_OCCURED.' + ld_out_message.get("MESSAGE"),"STATUS":1}
                return Response(ld_dict)
            elif self.request.query_params.get("Type") == "ELIGIBLE":
                jsondata = json.loads(request.body.decode('utf-8'))
                grade =  jsondata.get('Params').get('FILTER').get('GRADE')
                data_eligible = verify.travel_exp.grade_eligible(self, grade.upper())
                ld_dict = {"DATA": data_eligible.get('type').get('type'),
                           "MESSAGE": 'FOUND'}
                return Response(ld_dict)
            elif self.request.query_params.get("Type") == "ELIGIBLE_AMOUNT_DAILYDIEM":
                jsondata = json.loads(request.body.decode('utf-8'))
                ld_dict = verify.dailydiem.eligible_amount(self, jsondata)
                return Response(ld_dict)
            elif self.request.query_params.get("Type") == "ELIGIBLE_AMOUNT_TRAVEL":
                jsondata = json.loads(request.body.decode('utf-8'))
                grade = jsondata.get('Params').get('FILTER').get('grade')
                data_eligible = verify.travel_exp.grade_eligible(self, grade.upper())

                eligible_amount = verify.travel_exp.ticket_fare(self,jsondata,data_eligible.get('type').get('type'))


                priorpermission = jsondata.get('Params').get('FILTER').get('priorpermission')
                claimedamount = jsondata.get('Params').get('FILTER').get('claimedamount')
                tktbybank = jsondata.get('Params').get('FILTER').get('tktbybank')


                amount = 0
                if priorpermission != "" and claimedamount != "":
                    amount = verify.travel_exp.check_eligbility(self,int(priorpermission),int(claimedamount),int(eligible_amount))

                if tktbybank != "":
                    amount = verify.travel_exp.check_ticket(self, int(tktbybank),int(amount))


                eligible_value = {
                    "Eligible_amount": eligible_amount,
                    "Athorised_amount": amount,
                }
                ld_dict = {"DATA": eligible_value,
                           "MESSAGE": 'FOUND'}

                return Response(ld_dict)
            elif self.request.query_params.get("Type") == "ELIGIBLE_AMOUNT_INCI":
                jsondata = json.loads(request.body.decode('utf-8'))
                amount = verify.incidental.validation(self, jsondata)
                eligible_value = {
                    "Eligible_amount": amount,
                }
                ld_dict = {"DATA": eligible_value,
                           "MESSAGE": 'FOUND'}
                return Response(ld_dict)
            elif self.request.query_params.get("Type") == "ELIGIBLE_AMOUNT_LODG":
                jsondata = json.loads(request.body.decode('utf-8'))
                amount = verify.lodging.date_valid(self, jsondata)
                noofdays = amount.get('noofdays')
                accbybank = jsondata.get('Params').get('FILTER').get('accbybank')
                claimedamount = jsondata.get('Params').get('FILTER').get('claimedamount')
                if accbybank != "" and claimedamount != "":
                    amount = verify.lodging.calc_accbybank(self,jsondata,int(claimedamount),amount.get('Eligible_amount'))

                city = jsondata.get('Params').get('FILTER').get('city')
                hsncode = jsondata.get('Params').get('FILTER').get('hsn_gid')
                emp_gid = int(jsondata.get('Params').get('FILTER').get('emp_gid'))
                Entity_Gid = int(jsondata.get('Params').get('FILTER').get('Entity_Gid'))

                eligible_value = {
                    "Eligible_amount": amount.get('Eligible_amount'),
                    "noofdays": noofdays
                }

                ld_dict = {"DATA": eligible_value,
                           "MESSAGE": 'FOUND'}

                return Response(ld_dict)
            elif self.request.query_params.get("Type") == "ELIGIBLE_AMOUNT_LOC":
                jsondata = json.loads(request.body.decode('utf-8'))
                eligible_value = verify.localcon.validate_data(self,jsondata)

                ld_dict = {"DATA": eligible_value,
                           "MESSAGE": 'FOUND'}
                return Response(ld_dict)
            elif self.request.query_params.get("Type") == "ELIGIBLE_AMOUNT_PKG":
                jsondata = json.loads(request.body.decode('utf-8'))
                eligible_value = verify.pkg_moving.validate_data(self, jsondata)
                driverbatta = 0
                daysdrivereng = 0
                traveltimeinhours = jsondata.get('Params').get('FILTER').get('traveltimeinhours')
                if traveltimeinhours != "":
                    amountandadys = verify.pkg_moving.calck_driverbata(self, jsondata)
                    driverbatta = amountandadys.get("driverbatta")
                    daysdrivereng = amountandadys.get("daysdrivereng")
                breakagecharge = verify.pkg_moving.calc_breakage(self, jsondata)

                eligible = {
                    "Eligible_amount": eligible_value,
                    "driverbatta": driverbatta,
                    "daysdrivereng": daysdrivereng,
                    "breakagecharge": breakagecharge
                }
                ld_dict = {"DATA": eligible,
                           "MESSAGE": 'FOUND'}

                return Response(ld_dict)
            elif self.request.query_params.get("Type") == "ELIGIBLE_PKG":
                jsondata = json.loads(request.body.decode('utf-8'))
                obj_claim = meClaim.eClaim_Model()
                grade =  jsondata.get('Params').get('FILTER').get('GRADE')
                datas = {
                    "Grade": grade.upper()
                }
                obj_claim.filter_json = json.dumps(datas)
                ld_eligible = obj_claim.eClaim_gradetoelig_get()
                ld_elig = json.loads(ld_eligible.get("DATA").to_json(orient='records'))
                ld_dict = {"DATA": ld_elig,
                           "MESSAGE": 'FOUND'}
                return Response(ld_dict)
            elif self.request.query_params.get("Type") == "TOUR_REASON":
                jsondata = json.loads(request.body.decode('utf-8'))
                obj_claim = meClaim.eClaim_Model()
                obj_claim.filter_json = json.dumps(jsondata.get('Params').get('FILTER'))
                out_data = obj_claim.eClaim_tourreason_get()
                ld_elig = json.loads(out_data.get("DATA").to_json(orient='records'))
                ld_dict = {"DATA": ld_elig,
                           "MESSAGE": 'FOUND'}
                return Response(ld_dict)
            elif self.request.query_params.get("Type") == "EMPLOYEE_DATA":
                obj_claim = meClaim.eClaim_Model()
                jsondata = json.loads(request.body.decode('utf-8'))
                emp_gid = []
                emp_gid.append(jsondata.get('Params').get('FILTER').get('Employee_gid'))
                emp_data = {
                    "empids": emp_gid
                }
                obj_claim.filter_json = json.dumps(emp_data)
                obj_claim.json_classification = json.dumps(jsondata.get('Params').get('CLASSIFICATION'))
                emp_out_message = obj_claim.eClaim_employee_get()
                employee_data = json.loads(emp_out_message.get("DATA").to_json(orient='records'))
                ld_dict = {"DATA": employee_data,
                           "MESSAGE": 'FOUND'}
                return Response(ld_dict)
            elif self.request.query_params.get("Type") == "TOUR_DETAILS":
                obj_claim = meClaim.eClaim_Model()
                jsondata = json.loads(request.body.decode('utf-8'))
                obj_claim.filter_json = json.dumps(jsondata.get('Params').get('FILTER'))
                out_data = obj_claim.eClaim_tourdetails_get()
                if out_data.get("MESSAGE") == 'FOUND':
                    out_data = json.loads(out_data.get("DATA").to_json(orient='records'))
                    emp_gid = []
                    emp_data = {
                        "empids": out_data[0].get('empgid')
                    }
                    obj_claim.filter_json = json.dumps(emp_data)
                    obj_claim.json_classification = json.dumps(jsondata.get('Params').get('CLASSIFICATION'))
                    emp_out_message = obj_claim.eClaim_employee_get()
                    employee_data = json.loads(emp_out_message.get("DATA").to_json(orient='records'))
                    for d in out_data:
                        d["employee_name"] = employee_data[0].get('employee_name')
                        d["employee_code"] = employee_data[0].get('employee_code')
                        d["designation"] = employee_data[0].get('designation_name')
                        d["branch_name"] = employee_data[0].get('branch_name')
                    permit_data = {
                        "empids": out_data[0].get('permittedby')
                    }
                    obj_claim.filter_json = json.dumps(permit_data)
                    obj_claim.json_classification = json.dumps(jsondata.get('Params').get('CLASSIFICATION'))
                    permit_out_message = obj_claim.eClaim_employee_get()
                    permitemp_data = json.loads(permit_out_message.get("DATA").to_json(orient='records'))
                    for d in out_data:
                        d["permit_empname"] = permitemp_data[0].get('employee_name')
                        d["permit_empcode"] = permitemp_data[0].get('employee_code')
                        d["permit_branch"] = permitemp_data[0].get('branch_name')

                    approval_data = {
                        "empids": out_data[0].get('approvedby')
                    }
                    obj_claim.filter_json = json.dumps(approval_data)
                    obj_claim.json_classification = json.dumps(jsondata.get('Params').get('CLASSIFICATION'))
                    approval_out_message = obj_claim.eClaim_employee_get()
                    approval_data = json.loads(approval_out_message.get("DATA").to_json(orient='records'))
                    for d in out_data:
                        d["approval_empname"] = approval_data[0].get('employee_name')
                        d["approval_empcode"] = approval_data[0].get('employee_code')
                        d["approval_branch"] = approval_data[0].get('branch_name')

                    ld_dict = {"DATA": out_data,"MESSAGE": 'FOUND'}
                elif out_data.get("MESSAGE") == 'NOT_FOUND':
                    ld_dict = {"MESSAGE": 'NOT_FOUND'}
                else:
                    ld_dict = {"MESSAGE": 'ERROR_OCCURED.' + out_data.get("MESSAGE")}
                return Response(ld_dict)
            elif self.request.query_params.get("Type") == "HSN_CODE":
                obj_claim = meClaim.eClaim_Model()
                out_data = obj_claim.eClaim_hsncode_get()
                out_data = json.loads(out_data.get("DATA").to_json(orient='records'))
                ld_dict = {"DATA": out_data,"MESSAGE": 'FOUND'}
                return Response(ld_dict)
            elif self.request.query_params.get("Type") == "APPROVAL_FLOW":
                obj_claim = meClaim.eClaim_Model()
                jsondata = json.loads(request.body.decode('utf-8'))
                obj_claim.filter_json = json.dumps(jsondata.get('Params').get('FILTER'))
                out_data = obj_claim.eClaim_approvalflow_get()
                if out_data.get("MESSAGE") == 'FOUND':
                    out_data = json.loads(out_data.get("DATA").to_json(orient='records'))
                    emp_gid = []
                    for d in out_data:
                        emp_gid.append(d.get('approvedby'))

                    emp_data = {
                        "empids":emp_gid
                    }
                    obj_claim.filter_json = json.dumps(emp_data)
                    obj_claim.json_classification = json.dumps(jsondata.get('Params').get('CLASSIFICATION'))
                    emp_out_message = obj_claim.eClaim_employee_get()
                    employee_data = json.loads(emp_out_message.get("DATA").to_json(orient='records'))
                    for d in out_data:
                        for i in range(0, len(employee_data)):
                            if employee_data[i].get('employee_gid') == d.get('approvedby'):
                                d["employee_name"] = employee_data[i].get('employee_name')
                                d["employee_code"] = employee_data[i].get('employee_code')
                                break
                    ld_dict = {"DATA": out_data, "MESSAGE": 'FOUND'}

                elif out_data.get("MESSAGE") == 'NOT_FOUND':
                    ld_dict = {"MESSAGE": 'NOT_FOUND'}
                else:
                    ld_dict = {"MESSAGE": 'ERROR_OCCURED.' + out_data.get("MESSAGE")}
                return Response(ld_dict)
            elif self.request.query_params.get("Type") == "EMP_DEPENDENT":
                obj_claim = meClaim.eClaim_Model()
                jsondata = json.loads(request.body.decode('utf-8'))
                obj_claim.employee_gid = jsondata.get('Params').get('FILTER').get('Emp_gid')
                out_data = obj_claim.eClaim_emptodependent_get()
                out_data = json.loads(out_data.get("DATA").to_json(orient='records'))
                ld_dict = {"DATA": out_data,"MESSAGE": 'FOUND'}
                return Response(ld_dict)
            elif self.request.query_params.get("Type") == "TOUR_ADVANCE_GET":
                obj_claim = meClaim.eClaim_Model()
                jsondata = json.loads(request.body.decode('utf-8'))
                obj_claim.filter_json = json.dumps(jsondata.get('Params').get('FILTER'))
                out_data = obj_claim.eClaim_touradvance_get()
                out_datas = json.loads(out_data.get("DATA").to_json(orient='records'))
                out_data = out_datas[0].get('advance')
                out_data = json.loads(out_data)
                emp_data = {
                    "empids": out_data[0].get('approvedby')
                }
                obj_claim.filter_json = json.dumps(emp_data)
                obj_claim.json_classification = json.dumps(jsondata.get('Params').get('CLASSIFICATION'))
                emp_out_message = obj_claim.eClaim_employee_get()
                employee_data = json.loads(emp_out_message.get("DATA").to_json(orient='records'))
                for d in out_data:
                    for i in range(0, len(employee_data)):
                        if employee_data[i].get('employee_gid') == d.get('approvedby'):
                            d["approval_empname"] = employee_data[i].get('employee_name')
                            d["approval_empcode"] = employee_data[i].get('employee_code')
                            d["approval_branch"] = employee_data[i].get('branch_name')
                ld_dict = {"DATA": out_data,"MESSAGE": 'FOUND'}
                return Response(ld_dict)
            elif self.request.query_params.get("Type") == "CITY_GST":
                obj_claim = meClaim.eClaim_Model()
                jsondata = json.loads(request.body.decode('utf-8'))
                obj_claim.filter_json = json.dumps(jsondata.get('Params').get('FILTER'))
                ld_out_message = obj_claim.eClaim_citytogst_get()
                if ld_out_message.get("MESSAGE") == 'FOUND':
                    ld_dict = {"DATA": json.loads(ld_out_message.get("DATA").to_json(orient='records')),
                               "MESSAGE": 'FOUND    '}
                elif ld_out_message.get("MESSAGE") == 'NOT_FOUND':
                    ld_dict = {"MESSAGE": 'NOT_FOUND'}
                else:
                    ld_dict = {"MESSAGE": 'ERROR_OCCURED.' + ld_out_message.get("MESSAGE")}
                return Response(ld_dict)
        except Exception as e:
            er = "Erro Line no :"+str(format(sys.exc_info()[-1].tb_lineno))+" "+"Error :"+str(e)
            return Response({"MESSAGE": "ERROR_OCCURED", "DATA":er,"STATUS":1})

    def get(self,request):
        try:
            if self.request.query_params.get("Type") == "CLAIM_REQUEST":
                jsondata = json.loads(request.body.decode('utf-8'))
                obj_fa = meClaim.eClaim_Model()
                obj_fa.filter_json = json.dumps(jsondata.get('Params').get('FILTER'))
                ld_out_message = obj_fa.eClaim_request_get()
                if ld_out_message.get("MESSAGE") == 'FOUND':
                    data = json.loads(ld_out_message.get("DATA").to_json(orient='records'))
                    emp_gid = []
                    permit_gid = []
                    for i in data:
                        emp_gid.append(i.get('empgid'))
                        permit_gid.append(i.get('approvedby'))
                    emp_data = {
                        "empids" : emp_gid
                    }
                    obj_fa.filter_json = json.dumps(emp_data)
                    obj_fa.json_classification = json.dumps(jsondata.get('Params').get('CLASSIFICATION'))
                    emp_out_message = obj_fa.eClaim_employee_get()
                    employee_data = json.loads(emp_out_message.get("DATA").to_json(orient='records'))
                    empprmit_data = {
                        "empids": permit_gid
                    }
                    obj_fa.filter_json = json.dumps(empprmit_data)
                    obj_fa.json_classification = json.dumps(jsondata.get('Params').get('CLASSIFICATION'))
                    permit_out_message = obj_fa.eClaim_employee_get()
                    permit_data = json.loads(permit_out_message.get("DATA").to_json(orient='records'))
                    for d in data:
                        d["employee_name"] = employee_data[0].get('employee_name')
                        d["employee_code"] = employee_data[0].get('employee_code')
                        d["designation"] = employee_data[0].get('designation_name')
                        d["gstno"] = employee_data[0].get('gstno')
                    for d in data:
                        for i in range(0, len(permit_data)):
                            if permit_data[i].get('employee_gid') == int(d.get('approvedby')):
                                d["permit_byname"] = permit_data[i].get('employee_name')
                                d["permit_bycode"] = permit_data[i].get('employee_code')
                                break

                    ld_dict = {"DATA": data,"MESSAGE": 'FOUND'}
                elif ld_out_message.get("MESSAGE") == 'NOT_FOUND':
                    ld_dict = {"MESSAGE": 'NOT_FOUND'}
                else:
                    ld_dict = {"MESSAGE": 'ERROR_OCCURED.' + ld_out_message.get("MESSAGE")}
                return Response(ld_dict)
            elif self.request.query_params.get("Type") == "CLAIM_EXPENSE":
                obj_fa = meClaim.eClaim_Model()
                obj_fa.type = self.request.query_params.get("Type")
                ld_out_message = obj_fa.eClaim_expense_get()
                if json.loads(ld_out_message.get("DATA").to_json(orient='records')):
                    ld_dict = {"DATA": json.loads(ld_out_message.get("DATA").to_json(orient='records')),
                               "MESSAGE": 'FOUND    '}
                elif ld_out_message.get("MESSAGE") == 'NOT_FOUND':
                    ld_dict = {"MESSAGE": 'NOT_FOUND'}
                else:
                    ld_dict = {"MESSAGE": 'ERROR_OCCURED.' + ld_out_message.get("MESSAGE")}
                return Response(ld_dict)
            elif self.request.query_params.get("Type") == "CLAIMED_EXPENSE":
                jsondata = json.loads(request.body.decode('utf-8'))
                obj_eclaim = meClaim.eClaim_Model()
                obj_eclaim.filter_json = json.dumps(jsondata.get('Params').get('FILTER'))
                ld_out_message = obj_eclaim.eClaim_claimedexpense_get()
                if ld_out_message.get("MESSAGE") == 'FOUND':
                    obj_eclaim.employee_gid = jsondata.get('Params').get('FILTER').get('Claimrequest_Tourgid')
                    ld_out_file = obj_eclaim.eClaim_file_get()
                    ld_dict = {
                        "DATA": json.loads(ld_out_message.get("DATA").to_json(orient='records')),
                        "FILE": json.loads(ld_out_file.get("DATA").to_json(orient='records')),
                        "MESSAGE": 'FOUND'}
                elif ld_out_message.get("MESSAGE") == 'NOT_FOUND':
                    ld_dict = {"MESSAGE": 'NOT_FOUND'}
                else:
                    ld_dict = {"MESSAGE": 'ERROR_OCCURED.' + ld_out_message.get("MESSAGE")}
                return Response(ld_dict)
            elif self.request.query_params.get("Type") == "DLYDM":
                jsondata = json.loads(request.body.decode('utf-8'))
                obj_fa = meClaim.eClaim_Model()
                obj_fa.filter_json = json.dumps(jsondata.get('Params').get('FILTER'))
                ld_out_message = obj_fa.eClaim_dailydiem_get()
                if ld_out_message.get("MESSAGE") == 'FOUND':
                    ld_dict = {"DATA": json.loads(ld_out_message.get("DATA").to_json(orient='records')),
                               "MESSAGE": 'FOUND    '}
                elif ld_out_message.get("MESSAGE") == 'NOT_FOUND':
                    ld_dict = {"MESSAGE": 'NOT_FOUND'}
                else:
                    ld_dict = {"MESSAGE": 'ERROR_OCCURED.' + ld_out_message.get("MESSAGE")}
                return Response(ld_dict)
            elif self.request.query_params.get("Type") == "LODG":
                jsondata = json.loads(request.body.decode('utf-8'))
                obj_fa = meClaim.eClaim_Model()
                obj_fa.filter_json = json.dumps(jsondata.get('Params').get('FILTER'))
                ld_out_message = obj_fa.eClaim_lodging_get()
                if ld_out_message.get("MESSAGE") == 'FOUND':
                    ld_dict = {"DATA": json.loads(ld_out_message.get("DATA").to_json(orient='records')),
                               "MESSAGE": 'FOUND    '}
                elif ld_out_message.get("MESSAGE") == 'NOT_FOUND':
                    ld_dict = {"MESSAGE": 'NOT_FOUND'}
                else:
                    ld_dict = {"MESSAGE": 'ERROR_OCCURED.' + ld_out_message.get("MESSAGE")}
                return Response(ld_dict)
            elif self.request.query_params.get("Type") == "LCONV":
                jsondata = json.loads(request.body.decode('utf-8'))
                obj_fa = meClaim.eClaim_Model()
                obj_fa.filter_json = json.dumps(jsondata.get('Params').get('FILTER'))
                ld_out_message = obj_fa.eClaim_loccon_get()
                if ld_out_message.get("MESSAGE") == 'FOUND':
                    ld_dict = {"DATA": json.loads(ld_out_message.get("DATA").to_json(orient='records')),
                               "MESSAGE": 'FOUND    '}
                elif ld_out_message.get("MESSAGE") == 'NOT_FOUND':
                    ld_dict = {"MESSAGE": 'NOT_FOUND'}
                else:
                    ld_dict = {"MESSAGE": 'ERROR_OCCURED.' + ld_out_message.get("MESSAGE")}
                return Response(ld_dict)
            elif self.request.query_params.get("Type") == "MISC":
                jsondata = json.loads(request.body.decode('utf-8'))
                obj_fa = meClaim.eClaim_Model()
                obj_fa.filter_json = json.dumps(jsondata.get('Params').get('FILTER'))
                ld_out_message = obj_fa.eClaim_miscellaneous_get()
                if ld_out_message.get("MESSAGE") == 'FOUND':
                    ld_dict = {"DATA": json.loads(ld_out_message.get("DATA").to_json(orient='records')),
                               "MESSAGE": 'FOUND    '}
                elif ld_out_message.get("MESSAGE") == 'NOT_FOUND':
                    ld_dict = {"MESSAGE": 'NOT_FOUND'}
                else:
                    ld_dict = {"MESSAGE": 'ERROR_OCCURED.' + ld_out_message.get("MESSAGE")}
                return Response(ld_dict)
            elif self.request.query_params.get("Type") == "PCKG":
                jsondata = json.loads(request.body.decode('utf-8'))
                obj_fa = meClaim.eClaim_Model()
                obj_fa.filter_json = json.dumps(jsondata.get('Params').get('FILTER'))
                ld_out_message = obj_fa.eClaim_packingmoving_get()
                if ld_out_message.get("MESSAGE") == 'FOUND':
                    ld_dict = {"DATA": json.loads(ld_out_message.get("DATA").to_json(orient='records')),
                               "MESSAGE": 'FOUND    '}
                elif ld_out_message.get("MESSAGE") == 'NOT_FOUND':
                    ld_dict = {"MESSAGE": 'NOT_FOUND'}
                else:
                    ld_dict = {"MESSAGE": 'ERROR_OCCURED.' + ld_out_message.get("MESSAGE")}
                return Response(ld_dict)
            elif self.request.query_params.get("Type") == "TRVL":
                jsondata = json.loads(request.body.decode('utf-8'))
                obj_fa = meClaim.eClaim_Model()
                obj_fa.filter_json = json.dumps(jsondata.get('Params').get('FILTER'))
                ld_out_message = obj_fa.eClaim_travelexp_get()
                if ld_out_message.get("MESSAGE") == 'FOUND':
                    ld_dict = {"DATA": json.loads(ld_out_message.get("DATA").to_json(orient='records')),
                               "MESSAGE": 'FOUND    '}
                elif ld_out_message.get("MESSAGE") == 'NOT_FOUND':
                    ld_dict = {"MESSAGE": 'NOT_FOUND'}
                else:
                    ld_dict = {"MESSAGE": 'ERROR_OCCURED.' + ld_out_message.get("MESSAGE")}
                return Response(ld_dict)
            elif self.request.query_params.get("Type") == "INCDL":
                jsondata = json.loads(request.body.decode('utf-8'))
                obj_fa = meClaim.eClaim_Model()
                obj_fa.filter_json = json.dumps(jsondata.get('Params').get('FILTER'))
                ld_out_message = obj_fa.eClaim_incidental_get()
                if ld_out_message.get("MESSAGE") == 'FOUND':
                    ld_dict = {"DATA": json.loads(ld_out_message.get("DATA").to_json(orient='records')),
                               "MESSAGE": 'FOUND    '}
                elif ld_out_message.get("MESSAGE") == 'NOT_FOUND':
                    ld_dict = {"MESSAGE": 'NOT_FOUND'}
                else:
                    ld_dict = {"MESSAGE": 'ERROR_OCCURED.' + ld_out_message.get("MESSAGE")}
                return Response(ld_dict)
            elif self.request.query_params.get("Type") == "EMP_BRANCH":
                obj_claim = meClaim.eClaim_Model()
                out_data = ""
                if request.query_params.get("Api_Type") == "ANDROID":
                    filter = android.Android.get_method(self, request)
                    obj_eclaim = meClaim.eClaim_Model()
                    obj_claim.filter_json = json.dumps(filter)
                    out_data = obj_claim.eClaim_branchtoemp_get()
                elif request.query_params.get("Api_Type") == "WEB":
                    emp_gid = request.query_params.get("Employee_gid")
                    entity = request.query_params.get("Entity_Gid")
                    br = request.query_params.get("Branch_Gid")
                    obj_claim.filter_json = json.dumps({"Employee_gid": emp_gid, "Entity_Gid": entity,"Branch_Gid":br})
                    out_data = obj_claim.eClaim_branchtoemp_get()
                if out_data.get("MESSAGE") == 'FOUND':
                    ld_dict = {"DATA": json.loads(out_data.get("DATA").to_json(orient='records')),
                               "MESSAGE": 'FOUND',"STATUS":0}
                elif out_data.get("MESSAGE") == 'NOT_FOUND':
                    ld_dict = {"MESSAGE": 'NOT_FOUND',"STATUS":1}
                else:
                    ld_dict = {"MESSAGE": 'ERROR_OCCURED.' + out_data.get("MESSAGE"),"STATUS":0}
                return Response(ld_dict)
            elif self.request.query_params.get("Type") == "APPROVER_LIST":
                ld_out_message = 0
                obj_claim = meClaim.eClaim_Model()
                if request.query_params.get("Api_Type") == "WEB":
                    entity = request.query_params.get("Entity_Gid")
                    br = request.query_params.get("Branch_Gid")
                    apptype = request.query_params.get("App_Type")
                    obj_claim.filter_json = json.dumps({"App_Type":apptype, "Entity_Gid": entity, "Branch_Gid": br})
                    ld_out_message = obj_claim.eClaim_approverlist_get()
                if ld_out_message.get("MESSAGE") == 'FOUND':
                    data = json.loads(ld_out_message.get("DATA").to_json(orient='records'))
                    emp_gid = []
                    for i in data:
                        if request.auth.payload.get('user_id') != i.get('employeegid'):
                            emp_gid.append(i.get('employeegid'))
                    emp_data = {
                        "empids": emp_gid
                    }
                    obj_claim.filter_json = json.dumps(emp_data)
                    emp_out_message = obj_claim.eClaim_employeename_get()
                    employee_data = json.loads(emp_out_message.get("DATA").to_json(orient='records'))
                    for d in data:
                        for i in range(0, len(employee_data)):
                            if employee_data[i].get('employee_gid') == int(d.get('employeegid')):
                                d["employee_name"] = employee_data[i].get('employee_name')
                                d["employee_code"] = employee_data[i].get('employee_code')
                                d["employee_gid"] = d.get('employeegid')
                                break
                    ld_dict = {"DATA": data,
                               "MESSAGE": 'FOUND'}
                elif ld_out_message.get("MESSAGE") == 'NOT_FOUND':
                    ld_dict = {"MESSAGE": 'NOT_FOUND'}
                else:
                    ld_dict = {"MESSAGE": 'ERROR_OCCURED.' + ld_out_message.get("MESSAGE")}
                return Response(ld_dict)
            elif self.request.query_params.get("Type") == "GET_BRANCH":
                obj_claim = meClaim.eClaim_Model()
                ld_out_message = ''
                if request.query_params.get("Api_Type") == "ANDROID":
                    filter = android.Android.get_method(self, request)
                    obj_claim.filter_json = json.dumps(filter)
                    ld_out_message = obj_claim.eClaim_branch_get()
                elif request.query_params.get("Api_Type") == "WEB":
                    emp_gid = request.query_params.get("Employee_gid")
                    entity = request.query_params.get("Entity_Gid")
                    obj_claim.filter_json = json.dumps({"Employee_gid":emp_gid,"Entity_Gid":entity})
                    ld_out_message = obj_claim.eClaim_branch_get()
                if ld_out_message.get("MESSAGE") == 'FOUND':
                    ld_dict = {"DATA": json.loads(ld_out_message.get("DATA").to_json(orient='records')),
                               "MESSAGE": 'FOUND',"STATUS":0}
                elif ld_out_message.get("MESSAGE") == 'NOT_FOUND':
                    ld_dict = {"MESSAGE": 'NOT_FOUND',"STATUS":1}
                else:
                    ld_dict = {"MESSAGE": 'ERROR_OCCURED.' + ld_out_message.get("MESSAGE"),"STATUS":1}
                return Response(ld_dict)
            elif self.request.query_params.get("Type") == "GET_CITY":
                jsondata = json.loads(request.body.decode('utf-8'))
                obj_fa = meClaim.eClaim_Model()
                obj_fa.filter_json = json.dumps(jsondata.get('Params').get('FILTER'))
                ld_out_message = obj_fa.eClaim_expensecity_get()
                if ld_out_message.get("MESSAGE") == 'FOUND':
                    ld_dict = {"DATA": json.loads(ld_out_message.get("DATA").to_json(orient='records')),
                               "MESSAGE": 'FOUND    '}
                elif ld_out_message.get("MESSAGE") == 'NOT_FOUND':
                    ld_dict = {"MESSAGE": 'NOT_FOUND'}
                else:
                    ld_dict = {"MESSAGE": 'ERROR_OCCURED.' + ld_out_message.get("MESSAGE")}
                return Response(ld_dict)
            elif self.request.query_params.get("Type") == "GET_APPROVAL":
                jsondata = json.loads(request.body.decode('utf-8'))
                obj_fa = meClaim.eClaim_Model()
                data =  jsondata.get('Params').get('FILTER')
                data['approvedby'] = data.get('Employee_gid')
                obj_fa.filter_json = json.dumps(data)
                ld_out_message = obj_fa.eClaim_approval_get()
                if ld_out_message.get("MESSAGE") == 'FOUND':
                    data = json.loads(ld_out_message.get("DATA").to_json(orient='records'))
                    emp_gid = []
                    permit_gid = []
                    for i in data:
                        emp_gid.append(i.get('empgid'))
                        permit_gid.append(i.get('permittedby'))
                    emp_data = {
                        "empids": emp_gid
                    }
                    obj_fa.filter_json = json.dumps(emp_data)
                    obj_fa.json_classification = '{}'
                    emp_out_message = obj_fa.eClaim_employee_get()
                    employee_data = json.loads(emp_out_message.get("DATA").to_json(orient='records'))
                    for d in data:
                        for i in range(0, len(employee_data)):
                            if employee_data[0].get('employee_gid') == d.get('empgid'):
                                d["employee_name"] = employee_data[0].get('employee_name')
                                d["employee_code"] = employee_data[0].get('employee_code')
                                d["designation"] = employee_data[0].get('designation_name')
                                d["gstno"] = employee_data[0].get('gstno')
                                break
                    ld_dict = {"DATA": data,"MESSAGE": 'FOUND'}

                elif ld_out_message.get("MESSAGE") == 'NOT_FOUND':
                    ld_dict = {"MESSAGE": 'NOT_FOUND'}
                else:
                    ld_dict = {"MESSAGE": 'ERROR_OCCURED.' + ld_out_message.get("MESSAGE")}
                return Response(ld_dict)
            elif self.request.query_params.get("Type") == "ELIGIBLE":
                grade = request.query_params.get("GRADE")
                data_eligible = verify.travel_exp.grade_eligible(self, grade.upper())
                ld_dict = {"DATA": data_eligible.get('type').get('type'),
                           "MESSAGE": 'FOUND',"STATUS":0}
                return Response(ld_dict)
            elif self.request.query_params.get("Type") == "ELIGIBLE_AMOUNT_DAILYDIEM":
                jsondata = json.loads(request.body.decode('utf-8'))
                ld_dict = verify.dailydiem.eligible_amount(self, jsondata)
                return Response(ld_dict)
            elif self.request.query_params.get("Type") == "ELIGIBLE_AMOUNT_TRAVEL":
                jsondata = json.loads(request.body.decode('utf-8'))
                grade = jsondata.get('Params').get('FILTER').get('grade')
                data_eligible = verify.travel_exp.grade_eligible(self, grade.upper())

                eligible_amount = verify.travel_exp.ticket_fare(self,jsondata,data_eligible.get('type').get('type'))


                priorpermission = jsondata.get('Params').get('FILTER').get('priorpermission')
                claimedamount = jsondata.get('Params').get('FILTER').get('claimedamount')
                tktbybank = jsondata.get('Params').get('FILTER').get('tktbybank')


                amount = 0
                if priorpermission != "" and claimedamount != "":
                    amount = verify.travel_exp.check_eligbility(self,int(priorpermission),int(claimedamount),int(eligible_amount))

                if tktbybank != "":
                    amount = verify.travel_exp.check_ticket(self, int(tktbybank),int(amount))

                eligible_value = {
                    "Eligible_amount": eligible_amount,
                    "Athorised_amount": amount,
                }
                ld_dict = {"DATA": eligible_value,
                           "MESSAGE": 'FOUND'}
                return Response(ld_dict)
            elif self.request.query_params.get("Type") == "ELIGIBLE_AMOUNT_INCI":
                jsondata = json.loads(request.body.decode('utf-8'))
                amount = verify.incidental.validation(self, jsondata)
                eligible_value = {
                    "Eligible_amount": amount,
                }
                ld_dict = {"DATA": eligible_value,
                           "MESSAGE": 'FOUND'}
                return Response(ld_dict)
            elif self.request.query_params.get("Type") == "ELIGIBLE_AMOUNT_LODG":
                jsondata = json.loads(request.body.decode('utf-8'))
                amount = verify.lodging.date_valid(self, jsondata)
                noofdays = amount.get('noofdays')
                accbybank = jsondata.get('Params').get('FILTER').get('accbybank')
                claimedamount = jsondata.get('Params').get('FILTER').get('claimedamount')
                if accbybank != "" and claimedamount != "":
                    amount = verify.lodging.calc_accbybank(self,jsondata,int(claimedamount),amount.get('Eligible_amount'))

                city = jsondata.get('Params').get('FILTER').get('city')
                hsncode = jsondata.get('Params').get('FILTER').get('hsn_gid')
                emp_gid = int(jsondata.get('Params').get('FILTER').get('emp_gid'))
                Entity_Gid = int(jsondata.get('Params').get('FILTER').get('Entity_Gid'))

                eligible_value = {
                    "Eligible_amount": amount.get('Eligible_amount'),
                    "noofdays": noofdays
                }

                ld_dict = {"DATA": eligible_value,
                           "MESSAGE": 'FOUND'}
                return Response(ld_dict)
            elif self.request.query_params.get("Type") == "ELIGIBLE_AMOUNT_LOC":
                jsondata = json.loads(request.body.decode('utf-8'))
                eligible_value = verify.localcon.validate_data(self,jsondata)

                ld_dict = {"DATA": eligible_value,
                           "MESSAGE": 'FOUND'}
                return Response(ld_dict)
            elif self.request.query_params.get("Type") == "ELIGIBLE_AMOUNT_PKG":
                jsondata = json.loads(request.body.decode('utf-8'))
                eligible_value = verify.pkg_moving.validate_data(self, jsondata)
                driverbatta = 0
                daysdrivereng = 0
                traveltimeinhours = jsondata.get('Params').get('FILTER').get('traveltimeinhours')
                if traveltimeinhours != "":
                    amountandadys = verify.pkg_moving.calck_driverbata(self, jsondata)
                    driverbatta = amountandadys.get("driverbatta")
                    daysdrivereng = amountandadys.get("daysdrivereng")
                breakagecharge = verify.pkg_moving.calc_breakage(self, jsondata)

                eligible = {
                    "Eligible_amount": eligible_value,
                    "driverbatta": driverbatta,
                    "daysdrivereng": daysdrivereng,
                    "breakagecharge": breakagecharge
                }
                ld_dict = {"DATA": eligible,
                           "MESSAGE": 'FOUND'}
                return Response(ld_dict)
            elif self.request.query_params.get("Type") == "ELIGIBLE_PKG":
                jsondata = json.loads(request.body.decode('utf-8'))
                obj_claim = meClaim.eClaim_Model()
                grade =  jsondata.get('Params').get('FILTER').get('GRADE')
                datas = {
                    "Grade": grade.upper()
                }
                obj_claim.filter_json = json.dumps(datas)
                ld_eligible = obj_claim.eClaim_gradetoelig_get()
                ld_elig = json.loads(ld_eligible.get("DATA").to_json(orient='records'))
                ld_dict = {"DATA": ld_elig,
                           "MESSAGE": 'FOUND'}
                return Response(ld_dict)
            elif self.request.query_params.get("Type") == "TOUR_REASON":
                obj_claim = meClaim.eClaim_Model()
                out_data = ''
                if request.query_params.get("Api_Type") == "ANDROID":
                    filter = android.Android.get_method(self, request)
                    obj_claim.filter_json = json.dumps(filter)
                    out_data = obj_claim.eClaim_tourreason_get()
                elif request.query_params.get("Api_Type") == "WEB":
                    emp_gid = request.query_params.get("Employee_gid")
                    entity = request.query_params.get("Entity_Gid")
                    obj_claim.filter_json = json.dumps({"Employee_gid": emp_gid, "Entity_Gid": entity})
                    out_data = obj_claim.eClaim_tourreason_get()
                ld_elig = json.loads(out_data.get("DATA").to_json(orient='records'))
                ld_dict = {"DATA": ld_elig,
                           "MESSAGE": 'FOUND',"STATUS":0}
                return Response(ld_dict)
            elif self.request.query_params.get("Type") == "EMPLOYEE_DATA":
                obj_claim = meClaim.eClaim_Model()
                entity = request.query_params.get("Entity_Gid")
                emp_gid = []
                emp_gid.append(request.query_params.get("Employee_gid"))
                emp_data = {
                    "empids": emp_gid
                }
                obj_claim.filter_json = json.dumps(emp_data)
                obj_claim.json_classification = json.dumps({"Entity_Gid":entity})
                emp_out_message = obj_claim.eClaim_employee_get()
                employee_data = json.loads(emp_out_message.get("DATA").to_json(orient='records'))
                ld_dict = {"DATA": employee_data,
                           "MESSAGE": 'FOUND'}
                return Response(ld_dict)
            elif self.request.query_params.get("Type") == "TOUR_DETAILS":
                obj_claim = meClaim.eClaim_Model()
                out_data = ""
                if request.query_params.get("Api_Type") == "ANDROID":
                    filter = android.Android.get_method(self, request)
                    obj_claim.filter_json = json.dumps(filter)
                    out_data = obj_claim.eClaim_tourdetails_get()
                elif request.query_params.get("Api_Type") == "WEB":
                    emp_gid = request.query_params.get("Employee_gid")
                    entity = request.query_params.get("Entity_Gid")
                    Tour_Gid = request.query_params.get("Tour_Gid")
                    obj_claim.filter_json = json.dumps({"Employee_gid": emp_gid, "Entity_Gid": entity,"Tour_Gid":Tour_Gid})
                    out_data = obj_claim.eClaim_tourdetails_get()
                if out_data.get("MESSAGE") == 'FOUND':
                    out_data = json.loads(out_data.get("DATA").to_json(orient='records'))
                    emp_gid = []
                    emp_data = {
                        "empids": out_data[0].get('empgid')
                    }
                    obj_claim.filter_json = json.dumps(emp_data)
                    obj_claim.json_classification = json.dumps({})
                    emp_out_message = obj_claim.eClaim_employee_get()
                    employee_data = json.loads(emp_out_message.get("DATA").to_json(orient='records'))
                    for d in out_data:
                        d["employee_name"] = employee_data[0].get('employee_name')
                        d["employee_code"] = employee_data[0].get('employee_code')
                        d["designation"] = employee_data[0].get('designation_name')
                        d["branch_name"] = employee_data[0].get('branch_name')
                    permit_data = {
                        "empids": out_data[0].get('permittedby')
                    }
                    obj_claim.filter_json = json.dumps(permit_data)
                    obj_claim.json_classification = json.dumps({})
                    permit_out_message = obj_claim.eClaim_employee_get()
                    permitemp_data = json.loads(permit_out_message.get("DATA").to_json(orient='records'))
                    for d in out_data:
                        d["permit_empname"] = permitemp_data[0].get('employee_name')
                        d["permit_empcode"] = permitemp_data[0].get('employee_code')
                        d["permit_branch"] = permitemp_data[0].get('branch_name')

                    approval_data = {
                        "empids": out_data[0].get('approvedby')
                    }
                    obj_claim.filter_json = json.dumps(approval_data)
                    obj_claim.json_classification = json.dumps({})
                    approval_out_message = obj_claim.eClaim_employee_get()
                    approval_data = json.loads(approval_out_message.get("DATA").to_json(orient='records'))
                    for d in out_data:
                        d["approval_empname"] = approval_data[0].get('employee_name')
                        d["approval_empcode"] = approval_data[0].get('employee_code')
                        d["approval_branch"] = approval_data[0].get('branch_name')

                    ld_dict = {"DATA": out_data,"MESSAGE": 'FOUND',"STATUS":0}
                elif out_data.get("MESSAGE") == 'NOT_FOUND':
                    ld_dict = {"MESSAGE": 'NOT_FOUND',"STATUS":1}
                else:
                    ld_dict = {"MESSAGE": 'ERROR_OCCURED.' + out_data.get("MESSAGE"),"STATUS":1}
                return Response(ld_dict)
            elif self.request.query_params.get("Type") == "HSN_CODE":
                obj_claim = meClaim.eClaim_Model()
                out_data = obj_claim.eClaim_hsncode_get()
                out_data = json.loads(out_data.get("DATA").to_json(orient='records'))
                ld_dict = {"DATA": out_data,"MESSAGE": 'FOUND'}
                return Response(ld_dict)
            elif self.request.query_params.get("Type") == "APPROVAL_FLOW":
                obj_claim = meClaim.eClaim_Model()
                out_data = ""
                if request.query_params.get("Api_Type") == "ANDROID":
                    filter = android.Android.get_method(self, request)
                    obj_claim.filter_json = json.dumps(filter)
                    out_data = obj_claim.eClaim_approvalflow_get()
                elif request.query_params.get("Api_Type") == "WEB":
                    emp_gid = request.query_params.get("Employee_gid")
                    entity = request.query_params.get("Entity_Gid")
                    TourGid = request.query_params.get("TourGid")
                    AppType = request.query_params.get("AppType")
                    obj_claim.filter_json = json.dumps({"Employee_gid": emp_gid, "Entity_Gid": entity,"TourGid":TourGid,"AppType":AppType})
                    out_data = obj_claim.eClaim_approvalflow_get()
                if out_data.get("MESSAGE") == 'FOUND':
                    out_data = json.loads(out_data.get("DATA").to_json(orient='records'))
                    emp_gid = []
                    for d in out_data:
                        emp_gid.append(d.get('approvedby'))

                    emp_data = {
                        "empids":emp_gid
                    }
                    obj_claim.filter_json = json.dumps(emp_data)
                    obj_claim.json_classification = json.dumps({})
                    emp_out_message = obj_claim.eClaim_employee_get()
                    employee_data = json.loads(emp_out_message.get("DATA").to_json(orient='records'))
                    for d in out_data:
                        for i in range(0, len(employee_data)):
                            if employee_data[i].get('employee_gid') == d.get('approvedby'):
                                d["employee_name"] = employee_data[i].get('employee_name')
                                d["employee_code"] = employee_data[i].get('employee_code')
                                break
                    ld_dict = {"DATA": out_data, "MESSAGE": 'FOUND',"STATUS":0}

                elif out_data.get("MESSAGE") == 'NOT_FOUND':
                    ld_dict = {"MESSAGE": 'NOT_FOUND',"STATUS":1}
                else:
                    ld_dict = {"MESSAGE": 'ERROR_OCCURED.' + out_data.get("MESSAGE"),"STATUS":1}
                return Response(ld_dict)
            elif self.request.query_params.get("Type") == "EMP_DEPENDENT":
                obj_claim = meClaim.eClaim_Model()
                jsondata = json.loads(request.body.decode('utf-8'))
                obj_claim.employee_gid = jsondata.get('Params').get('FILTER').get('Emp_gid')
                out_data = obj_claim.eClaim_emptodependent_get()
                out_data = json.loads(out_data.get("DATA").to_json(orient='records'))
                ld_dict = {"DATA": out_data,"MESSAGE": 'FOUND'}
                return Response(ld_dict)
            elif self.request.query_params.get("Type") == "TOUR_ADVANCE_GET":
                obj_claim = meClaim.eClaim_Model()
                jsondata = json.loads(request.body.decode('utf-8'))
                obj_claim.filter_json = json.dumps(jsondata.get('Params').get('FILTER'))
                out_data = obj_claim.eClaim_touradvance_get()
                out_data = json.loads(out_data.get("DATA").to_json(orient='records'))
                emp_data = {
                    "empids": out_data[0].get('approvedby')
                }
                obj_claim.filter_json = json.dumps(emp_data)
                obj_claim.json_classification = json.dumps(jsondata.get('Params').get('CLASSIFICATION'))
                emp_out_message = obj_claim.eClaim_employee_get()
                employee_data = json.loads(emp_out_message.get("DATA").to_json(orient='records'))
                for d in out_data:
                    for i in range(0, len(employee_data)):
                        if employee_data[i].get('employee_gid') == d.get('approvedby'):
                            d["approval_empname"] = employee_data[i].get('employee_name')
                            d["approval_empcode"] = employee_data[i].get('employee_code')
                            d["approval_branch"] = employee_data[i].get('branch_name')
                ld_dict = {"DATA": out_data,"MESSAGE": 'FOUND'}
                return Response(ld_dict)
        except Exception as e:
            return Response({"MESSAGE": "ERROR_OCCURED", "DATA": str(e),"STATUS":1})

class eClaim_Tran(APIView):
    def post(self,request):
        try:
            if self.request.query_params.get("Type") == "DAILY_DIEM":
                jsondata = json.loads(request.body.decode('utf-8'))
                obj_fa = meClaim.eClaim_Model()
                outer_data = jsondata.get('Params').get('DETAILS')
                valid_data = jsondata.get('Params').get('CHANGE').get('DATA')
                logic = verify.dailydiem.submit_data(self,valid_data,outer_data)
                if logic == "True":
                    obj_fa.jsondata = json.dumps(outer_data)
                    obj_fa.jsonData = json.dumps({"DATA":valid_data})
                    ld_out_message = obj_fa.eClaim_dailydiem_set()
                    msg = ld_out_message.get("MESSAGE").split(",")
                    if msg[0] == 'SUCCESS':
                        ld_dict = {"MESSAGE":ld_out_message.get("MESSAGE")}
                    elif msg[0] == 'FAIL':
                        ld_dict = {"MESSAGE": "FAIL"}
                    else:
                        ld_dict = {"MESSAGE": 'ERROR_OCCURED.' + ld_out_message.get("MESSAGE")}
                    return Response(ld_dict)
                else:
                    return Response(logic[1])
            elif self.request.query_params.get("Type") == "LODGING":
                jsondata = json.loads(request.body.decode('utf-8'))
                obj_fa = meClaim.eClaim_Model()
                outer_data = jsondata.get('Params').get('DETAILS')
                valid_data = jsondata.get('Params').get('CHANGE').get('DATA')
                logic = verify.lodging.calck_totalamt(self, valid_data, outer_data)
                if logic == "True":
                    obj_fa.jsondata = json.dumps(outer_data)
                    obj_fa.jsonData = json.dumps({"DATA":valid_data})
                    ld_out_message = obj_fa.eClaim_lodging_set()
                    msg = ld_out_message.get("MESSAGE").split(",")
                    if msg[0] == 'SUCCESS':
                        ld_dict = {"MESSAGE": ld_out_message.get("MESSAGE")}
                    elif msg[0] == 'FAIL':
                        ld_dict = {"MESSAGE": "FAIL"}
                    else:
                        ld_dict = {"MESSAGE": 'ERROR_OCCURED.' + ld_out_message.get("MESSAGE")}
                    return Response(ld_dict)
            elif self.request.query_params.get("Type") == "LOC_CON":
                jsondata = json.loads(request.body.decode('utf-8'))
                obj_fa = meClaim.eClaim_Model()
                outer_data = jsondata.get('Params').get('DETAILS')
                valid_data = jsondata.get('Params').get('CHANGE').get('DATA')
                logic = verify.localcon.calck_totalamt(self, valid_data, outer_data)
                if logic == "True":
                    obj_fa.jsondata = json.dumps(outer_data)
                    obj_fa.jsonData = json.dumps({"DATA": valid_data})
                    ld_out_message = obj_fa.eClaim_loccon_set()
                    msg = ld_out_message.get("MESSAGE").split(",")
                    if msg[0] == 'SUCCESS':
                        ld_dict = {"MESSAGE": ld_out_message.get("MESSAGE")}
                    elif msg[0] == 'FAIL':
                        ld_dict = {"MESSAGE": "FAIL"}
                    else:
                        ld_dict = {"MESSAGE": 'ERROR_OCCURED.' + ld_out_message.get("MESSAGE")}
                    return Response(ld_dict)
            elif self.request.query_params.get("Type") == "MISCELLANEOUS":
                jsondata = json.loads(request.body.decode('utf-8'))
                obj_fa = meClaim.eClaim_Model()
                outer_data = jsondata.get('Params').get('DETAILS')
                valid_data = jsondata.get('Params').get('CHANGE').get('DATA')
                logic = verify.miscellaneous.validate_data(self, valid_data, outer_data)
                if logic == "True":
                    obj_fa.jsondata = json.dumps(outer_data)
                    obj_fa.jsonData = json.dumps({"DATA": valid_data})
                    ld_out_message = obj_fa.eClaim_miscellaneous_set()
                    msg = ld_out_message.get("MESSAGE").split(",")
                    if msg[0] == 'SUCCESS':
                        ld_dict = {"MESSAGE": ld_out_message.get("MESSAGE")}
                    elif msg[0] == 'FAIL':
                        ld_dict = {"MESSAGE": "FAIL"}
                    else:
                        ld_dict = {"MESSAGE": 'ERROR_OCCURED.' + ld_out_message.get("MESSAGE")}
                    return Response(ld_dict)
            elif self.request.query_params.get("Type") == "PKG_MOVING":
                jsondata = json.loads(request.body.decode('utf-8'))
                obj_fa = meClaim.eClaim_Model()
                outer_data = jsondata.get('Params').get('DETAILS')
                valid_data = jsondata.get('Params').get('CHANGE').get('DATA')
                logic = verify.pkg_moving.calck_totalamt(self, valid_data, outer_data)
                if logic == "True":
                    obj_fa.jsondata = json.dumps(outer_data)
                    obj_fa.jsonData = json.dumps({"DATA":valid_data})
                    ld_out_message = obj_fa.eClaim_pkgmoving_set()
                    msg = ld_out_message.get("MESSAGE").split(",")
                    if msg[0] == 'SUCCESS':
                        ld_dict = {"MESSAGE": ld_out_message.get("MESSAGE")}
                    elif msg[0] == 'FAIL':
                        ld_dict = {"MESSAGE": "FAIL"}
                    else:
                        ld_dict = {"MESSAGE": 'ERROR_OCCURED.' + ld_out_message.get("MESSAGE")}
                    return Response(ld_dict)
                else:
                    return Response(logic[1])
            elif self.request.query_params.get("Type") == "TRAVEL_EXP":
                jsondata = json.loads(request.body.decode('utf-8'))
                obj_claim = meClaim.eClaim_Model()
                outer_data = jsondata.get('Params').get('DETAILS')
                valid_data = jsondata.get('Params').get('CHANGE')
                logic = verify.travel_exp.calck_totalamt(self,valid_data.get('DATA'),outer_data)
                if logic == "True":
                    obj_claim.jsonData = json.dumps(valid_data)
                    obj_claim.jsondata = json.dumps(outer_data)
                    ld_out_message = obj_claim.eClaim_travelexp_set()
                    msg = ld_out_message.get("MESSAGE").split(",")
                    if msg[0] == 'SUCCESS':
                        ld_dict = {"MESSAGE": ld_out_message.get("MESSAGE")}
                    elif msg[0] == 'FAIL':
                        ld_dict = {"MESSAGE": "FAIL"}
                    else:
                        ld_dict = {"MESSAGE": 'ERROR_OCCURED.' + ld_out_message.get("MESSAGE")}
                    return Response(ld_dict)
            elif self.request.query_params.get("Type") == "INCIDENTAL":
                jsondata = json.loads(request.body.decode('utf-8'))
                obj_fa = meClaim.eClaim_Model()
                outer_data = jsondata.get('Params').get('DETAILS')
                valid_data = jsondata.get('Params').get('CHANGE').get('DATA')
                logic = verify.incidental.calck_totalamt(self, valid_data, outer_data)
                if logic == "True":
                    obj_fa.jsondata = json.dumps(outer_data)
                    obj_fa.jsonData = json.dumps({"DATA":valid_data})
                    ld_out_message = obj_fa.eClaim_incidental_set()
                    msg = ld_out_message.get("MESSAGE").split(",")
                    if msg[0] == 'SUCCESS':
                        ld_dict = {"MESSAGE": ld_out_message.get("MESSAGE")}
                    elif msg[0] == 'FAIL':
                        ld_dict = {"MESSAGE": "FAIL"}
                    else:
                        ld_dict = {"MESSAGE": 'ERROR_OCCURED.' + ld_out_message.get("MESSAGE")}
                    return Response(ld_dict)
            elif self.request.query_params.get("Type") == "MOVE_APPROVE":
                jsondata = json.loads(request.body.decode('utf-8'))
                obj_eclaim = meClaim.eClaim_Model()
                obj_eclaim.jsonData = json.dumps(jsondata.get('Params').get('DETAILS'))
                ld_out_message = obj_eclaim.eClaim_movetoapproval_set()
                if ld_out_message.get("MESSAGE") == 'SUCCESS':
                    file_data =  jsondata.get('Params').get('FILE').get('File')
                    if file_data != []:
                        obj_eclaim.jsonData = json.dumps(jsondata.get('Params').get('FILE'))
                        out_message = obj_eclaim.eClaim_file_set()
                        if out_message.get("MESSAGE") == 'SUCCESS':
                            ld_dict = {"MESSAGE": "SUCCESS"}
                    else:
                        ld_dict = {"MESSAGE": "SUCCESS"}
                elif ld_out_message.get("MESSAGE") == 'FAIL':
                    ld_dict = {"MESSAGE": "FAIL"}
                else:
                    ld_dict = {"MESSAGE": 'ERROR_OCCURED.' + ld_out_message.get("MESSAGE")}
                return Response(ld_dict)
            elif self.request.query_params.get("Type") == "MOVE_APPROVE_II":
                ld_out_message = ""
                jsondata = json.loads(request.body.decode('utf-8'))
                obj_claim = meClaim.eClaim_Model()
                if request.query_params.get("Api_Type") == "ANDROID":
                    obj_claim.jsonData = json.dumps(jsondata)
                    ld_out_message = obj_claim.eClaim_movetoapproval2_set()
                elif request.query_params.get("Api_Type") == "WEB":
                    tourgid = jsondata.get('Params').get('DETAILS').get('tourgid')
                    obj_claim.employee_gid = tourgid
                    ld_out_emp = obj_claim.eClaim_tourtoemp_get()
                    ld_dict = json.loads(ld_out_emp.get("DATA").to_json(orient='records'))
                    emp_gid = ld_dict[0].get('empgid')
                    emp_data = {
                        "empids": emp_gid
                    }
                    obj_claim.filter_json = json.dumps(emp_data)
                    emp_bnk = obj_claim.eClaim_employeebnk_get()
                    bank_data = json.loads(emp_bnk.get("DATA").to_json(orient='records'))
                    if len(bank_data) == 0:
                        return {"MESSAGE": "Employee Bank Data Missing"}
                    obj_claim.jsonData = json.dumps(jsondata.get('Params').get('DETAILS'))
                    ld_out_message = obj_claim.eClaim_movetoapproval2_set()
                if ld_out_message.get("MESSAGE") == 'SUCCESS':
                    if jsondata.get('Params').get('DETAILS').get('apptype') == "TOURADV" and jsondata.get('Params').get('DETAILS').get('approvedby') == 0 :
                        response = verify.ecf_entry.invoice_header(self,request)
                        if response.get('MESSAGE') == "SUCCESS":

                            tourgid = jsondata.get('Params').get('DETAILS').get('tourgid')
                            processedby = jsondata.get('Params').get('DETAILS').get('processedby')
                            header_gid = response.get('Header_Gid')

                            response_data = verify.ecf_entry.invoice_detail(self, request,response)
                            if response_data.get('MESSAGE') == "SUCCESS":
                                obj_claim.jsondata = json.dumps({"Tour_gid": tourgid,"Invoice_Header_Gid": header_gid,"processedby":processedby})
                                out_data = obj_claim.eClaim_advinv_set()
                                if out_data.get("MESSAGE") == 'SUCCESS':
                                    ld_dict = {"MESSAGE": "SUCCESS","STATUS":0}
                                elif out_data.get("MESSAGE") == 'FAIL':
                                    ld_dict = {"MESSAGE": "FAIL", "STATUS": 1}
                                else:
                                    ld_dict = {"MESSAGE": 'ERROR_OCCURED.' + out_data.get("MESSAGE"), "STATUS": 1}
                            else:
                                ld_dict = {"MESSAGE": 'ERROR_OCCURED.' + response_data, "STATUS": 1}
                    elif jsondata.get('Params').get('DETAILS').get('apptype') == "CLAIM" and jsondata.get('Params').get('DETAILS').get('approvedby') == 0 :
                        response = verify.ecf_entry.invoice_header(self,request)
                        if response.get('MESSAGE') == "SUCCESS":

                            tourgid = jsondata.get('Params').get('DETAILS').get('tourgid')
                            processedby = jsondata.get('Params').get('DETAILS').get('processedby')
                            header_gid = response.get('Header_Gid')

                            response_data = verify.ecf_entry.invoice_detail(self, request,response)
                            if response_data.get('MESSAGE') == "SUCCESS":
                                obj_claim.jsondata = json.dumps({"Tour_gid": tourgid,"Invoice_Header_Gid": header_gid,"processedby":processedby})
                                out_data = obj_claim.eClaim_expinv_set()
                                if out_data.get("MESSAGE") == 'SUCCESS':
                                    ld_dict = {"MESSAGE": "SUCCESS","STATUS":0}
                                elif out_data.get("MESSAGE") == 'FAIL':
                                    ld_dict = {"MESSAGE": "FAIL", "STATUS": 1}
                                else:
                                    ld_dict = {"MESSAGE": 'ERROR_OCCURED.' + out_data.get("MESSAGE"), "STATUS": 1}
                            else:
                                ld_dict = {"MESSAGE": 'ERROR_OCCURED.' + response_data, "STATUS": 1}

                    else:
                        ld_dict = {"MESSAGE": "SUCCESS", "STATUS": 0}
                elif ld_out_message.get("MESSAGE") == 'FAIL':
                    ld_dict = {"MESSAGE": "FAIL","STATUS":1}
                else:
                    ld_dict = {"MESSAGE": 'ERROR_OCCURED.' + ld_out_message.get("MESSAGE"),"STATUS":1}
                return Response(ld_dict)
            elif self.request.query_params.get("Type") == "ECLAIM_RETURN":
                ld_out_message = ""
                jsondata = json.loads(request.body.decode('utf-8'))
                obj_claim = meClaim.eClaim_Model()
                if request.query_params.get("Api_Type") == "ANDROID":
                    obj_claim.jsonData = json.dumps(jsondata)
                    ld_out_message = obj_claim.eClaim_return_set()
                elif request.query_params.get("Api_Type") == "WEB":
                    obj_claim.jsonData = json.dumps(jsondata.get('Params').get('DETAILS'))
                    ld_out_message = obj_claim.eClaim_return_set()
                if ld_out_message.get("MESSAGE") == 'SUCCESS':
                    ld_dict = {"MESSAGE": "SUCCESS","STATUS":0}
                elif ld_out_message.get("MESSAGE") == 'FAIL':
                    ld_dict = {"MESSAGE": "FAIL","STATUS":1}
                else:
                    ld_dict = {"MESSAGE": 'ERROR_OCCURED.' + ld_out_message.get("MESSAGE"),"STATUS":1}
                return Response(ld_dict)
            elif self.request.query_params.get("Type") == "ECLAIM_FORWARD":
                ld_out_message = ""
                jsondata = json.loads(request.body.decode('utf-8'))
                obj_claim = meClaim.eClaim_Model()
                obj_claim.jsonData = json.dumps(jsondata.get('Params').get('DETAILS'))
                ld_out_message = obj_claim.eClaim_forward_set()

                if ld_out_message.get("MESSAGE") == 'SUCCESS':
                    ld_dict = {"MESSAGE": "SUCCESS","STATUS":0}
                elif ld_out_message.get("MESSAGE") == 'FAIL':
                    ld_dict = {"MESSAGE": "FAIL","STATUS":1}
                else:
                    ld_dict = {"MESSAGE": 'ERROR_OCCURED.' + ld_out_message.get("MESSAGE"),"STATUS":1}
                return Response(ld_dict)
            elif self.request.query_params.get("Type") == "MOVE_REJECT":
                jsondata = json.loads(request.body.decode('utf-8'))
                obj_claim = meClaim.eClaim_Model()
                if request.query_params.get("Api_Type") == "ANDROID":
                    obj_claim.jsonData = json.dumps(jsondata)
                    ld_out_message = obj_claim.eClaim_reject_set()
                elif request.query_params.get("Api_Type") == "WEB":
                    obj_claim.jsonData = json.dumps(jsondata.get('Params').get('DETAILS'))
                    ld_out_message = obj_claim.eClaim_reject_set()
                if ld_out_message.get("MESSAGE") == 'SUCCESS':
                    ld_dict = {"MESSAGE": "SUCCESS","STATUS":0}
                elif ld_out_message.get("MESSAGE") == 'FAIL':
                    ld_dict = {"MESSAGE": "FAIL","STATUS":1}
                else:
                    ld_dict = {"MESSAGE": 'ERROR_OCCURED.' + ld_out_message.get("MESSAGE"),"STATUS":1}
                return Response(ld_dict)
            elif self.request.query_params.get("Type") == "APPROVE_AMT":
                jsondata = json.loads(request.body.decode('utf-8'))
                obj_fa = meClaim.eClaim_Model()
                obj_fa.jsondata = json.dumps(jsondata.get('Params').get('DETAILS'))
                obj_fa.jsonData = json.dumps(jsondata.get('Params').get('CHANGE'))
                ld_out_message = obj_fa.eClaim_approveamount_set()
                if ld_out_message.get("MESSAGE") == 'SUCCESS':
                    ld_dict = {"MESSAGE": "SUCCESS"}
                elif ld_out_message.get("MESSAGE") == 'FAIL':
                    ld_dict = {"MESSAGE": "FAIL"}
                else:
                    ld_dict = {"MESSAGE": 'ERROR_OCCURED.' + ld_out_message.get("MESSAGE")}
                return Response(ld_dict)
            elif self.request.query_params.get("Type") == "TOUR_MAKER":
                ld_out_message = ""
                jsondata = json.loads(request.body.decode('utf-8'))
                obj_claim = meClaim.eClaim_Model()
                if request.query_params.get("Api_Type") == "ANDROID":
                    DETAILS = android.Android.set_data_dtl(self, request)
                    CHANGE = android.Android.set_data_chng(self, request)
                    obj_claim.jsondata = json.dumps(DETAILS)
                    obj_claim.jsonData = json.dumps(CHANGE)
                    ld_out_message = obj_claim.eClaim_tourrequest_set()
                elif request.query_params.get("Api_Type") == "WEB":
                    obj_claim.jsondata = json.dumps(jsondata.get('Params').get('DETAILS'))
                    obj_claim.jsonData = json.dumps(jsondata.get('Params').get('CHANGE'))
                    ld_out_message = obj_claim.eClaim_tourrequest_set()
                if ld_out_message.get("MESSAGE") == 'SUCCESS':
                    ld_dict = {"MESSAGE": "SUCCESS","STATUS":0}
                elif ld_out_message.get("MESSAGE") == 'FAIL':
                    ld_dict = {"MESSAGE": "FAIL","STATUS":1}
                else:
                    ld_dict = {"MESSAGE": 'ERROR_OCCURED.' + ld_out_message.get("MESSAGE"),"STATUS":1}
                return Response(ld_dict)
            elif self.request.query_params.get("Type") == "TOUR_ADVANCE":
                jsondata = json.loads(request.body.decode('utf-8'))
                obj_fa = meClaim.eClaim_Model()
                obj_fa.jsondata = json.dumps(jsondata.get('Params').get('DETAILS'))
                ld_out_message = obj_fa.eClaim_touradvance_set()
                if ld_out_message.get("MESSAGE") == 'SUCCESS':
                    ld_dict = {"MESSAGE": "SUCCESS"}
                elif ld_out_message.get("MESSAGE") == 'FAIL':
                    ld_dict = {"MESSAGE": "FAIL"}
                else:
                    ld_dict = {"MESSAGE": 'ERROR_OCCURED.' + ld_out_message.get("MESSAGE")}
                return Response(ld_dict)
        except Exception as e:
            return Response({"MESSAGE": "ERROR_OCCURED","STATUS":1,"DATA": str(e)})

# import datetime
# class file_up(APIView):
#     def post(self, request):
#         try:
#             jsondata = request.body
#             file_data = request.FILES['file']
#             file_name = request.POST['name']
#             file_extension = ".jpg"
#             file_name_new = file_name + str(datetime.datetime.now().strftime("%Y-%m-%d:%H:%M:%S"))
#             # open(BASE_DIR + '/Bigflow/media/' + file_name + file_extension, 'wb')
#             lsfile_name = str((BASE_DIR + '/Bigflow/media/' + file_name_new + file_extension))
#             with open(lsfile_name, 'wb') as f:
#                 f.write(file_data)
#                 ld_dict = {"MESSAGE": "SUCCESS"}
#             return Response(ld_dict)
#         except Exception as e:
#             return Response({"MESSAGE": "ERROR_OCCURED", "DATA": str(e)})
class Tour_Request(APIView):
    def post(self,request):
        try:
            path = self.request.stream.path
            ld_out_message = ""
            if request.query_params.get("Api_Type") =="WEB":
                jsondata = json.loads(request.body.decode('utf-8'))
                common.main_fun1(request.read(), path)
                obj_eclaim = meClaim.eClaim_Model()
                obj_eclaim.filter_json = json.dumps(jsondata.get('Params').get('FILTER'))
                ld_out_message = obj_eclaim.eClaim_request_get()
            else:
                filter = android.Android.post_summary(self,request)
                common.main_fun1(request.read(), path)
                obj_eclaim = meClaim.eClaim_Model()
                obj_eclaim.filter_json = json.dumps(filter)
                ld_out_message = obj_eclaim.eClaim_request_get()
            if ld_out_message.get("MESSAGE") == 'FOUND':
                out_data = json.loads(ld_out_message.get("DATA").to_json(orient='records'))
                common.logger.error([{"out_data": str(out_data)}])
                data = []
                for d in out_data:
                    if 'Total_Row' in d:
                        pass
                    else :
                        d['Total_Row'] = len(out_data)
                    tmp={}
                    tmp['gid'] = d.get('gid')
                    tmp['requestno'] = d.get('requestno')
                    tmp['requestdate'] = d.get('requestdate')
                    tmp['empgid'] = d.get('empgid')
                    tmp['empgrade'] = d.get('empgrade')
                    tmp['tourreason'] = d.get('name')
                    tmp['startdate'] = d.get('startdate')
                    tmp['enddate'] = d.get('enddate')
                    tmp['enddate'] = d.get('enddate')
                    tmp['tourstatus'] = d.get('tourstatus')
                    tmp['approvedby'] = d.get('approvedby')
                    tmp['Total_Row'] = d.get('Total_Row')
                    data.append(tmp)
                common.logger.error([{"data": str(data)}])
                permit_gid = []
                emp_gid = data[0].get('empgid')

                for i in data:
                    if i.get('approvedby') not in permit_gid and i.get('approvedby') != 0:
                        permit_gid.append(i.get('approvedby'))
                emp_data = {
                    "empids" : emp_gid
                }
                obj_eclaim.filter_json = json.dumps(emp_data)
                obj_eclaim.json_classification = json.dumps({})
                emp_out_message = obj_eclaim.eClaim_employee_get()
                employee_data = json.loads(emp_out_message.get("DATA").to_json(orient='records'))
                common.logger.error([{"employee_data": str(employee_data)}])
                if len(employee_data) == 0:
                    ld_dict = {"MESSAGE": 'NOT_FOUND', "STATUS": 1}
                    return Response(ld_dict)
                empprmit_data = {
                    "empids": permit_gid
                }
                obj_eclaim.filter_json = json.dumps(empprmit_data)
                obj_eclaim.json_classification = json.dumps({})
                permit_out_message = obj_eclaim.eClaim_employee_get()
                permit_data = json.loads(permit_out_message.get("DATA").to_json(orient='records'))
                common.logger.error([{"permit_data": str(permit_data)}])
                if len(permit_data) == 0:
                    ld_dict = {"MESSAGE": 'NOT_FOUND', "STATUS": 1}
                    return Response(ld_dict)

                for d in data:
                    d["employee_name"] = employee_data[0].get('employee_name')
                    d["employee_code"] = employee_data[0].get('employee_code')
                    d["employee_designation"] = employee_data[0].get('designation_name')
                for d in data:
                    for i in range(0, len(permit_data)):
                        if permit_data[i].get('employee_gid') == int(d.get('approvedby')):
                            d["permit_byname"] = permit_data[i].get('employee_name')
                            d["permit_bycode"] = permit_data[i].get('employee_code')
                            break

                common.logger.error([{"data2": str(data)}])
                ld_dict = {"DATA": data,"MESSAGE": 'FOUND',"STATUS":0}

            elif ld_out_message.get("MESSAGE") == 'NOT_FOUND':
                ld_dict = {"MESSAGE": 'NOT_FOUND',"STATUS":1}
            else:
                ld_dict = {"MESSAGE": 'ERROR_OCCURED.' + ld_out_message.get("MESSAGE"),"STATUS":1}
            return Response(ld_dict)
        except Exception as e:
            common.logger.error(e)
            e = "Erro Line no :" + str(format(sys.exc_info()[-1].tb_lineno)) + " " + "Error :" + str(e)
            return Response({"MESSAGE": "ERROR_OCCURED", "DATA": str(e), "STATUS": 1})
class Approval(APIView):
    def post(self,request):
        try:
            path = self.request.stream.path
            jsondata = json.loads(request.body.decode('utf-8'))
            obj_eclaim = meClaim.eClaim_Model()
            ld_out_message = ""
            if request.query_params.get("Api_Type") == "WEB":
                data = jsondata.get('Params').get('FILTER')
                common.main_fun1(request.read(), path)
                data['approvedby'] = data.get('Employee_gid')
                obj_eclaim.filter_json = json.dumps(data)
                ld_out_message = obj_eclaim.eClaim_approval_get()
            else:
                filter = android.Android.post_summary(self, request)
                common.main_fun1(request.read(), path)
                filter['approvedby'] = filter.get('Employee_gid')
                obj_eclaim.filter_json = json.dumps(filter)
                ld_out_message = obj_eclaim.eClaim_approval_get()
            if ld_out_message.get("MESSAGE") == 'FOUND':
                data = json.loads(ld_out_message.get("DATA").to_json(orient='records'))
                common.logger.error([{"Aprovaldata2": str(data)}])
                emp_gid = []
                onbehalf_gid = []
                for i in data:
                    if i.get('empgid') not in emp_gid and i.get('empgid') != 0:
                        emp_gid.append(i.get('empgid'))
                    if i.get('onbehalof') not in onbehalf_gid and i.get('onbehalof') != 0:
                        onbehalf_gid.append(i.get('onbehalof'))

                emp_data = {
                    "empids": emp_gid
                }
                obj_eclaim.filter_json = json.dumps(emp_data)
                obj_eclaim.json_classification = '{}'
                emp_out_message = obj_eclaim.eClaim_employee_get()
                employee_data = json.loads(emp_out_message.get("DATA").to_json(orient='records'))
                common.logger.error([{"Aprovaldata_employee_data": str(employee_data)}])
                for d in data:
                    for i in employee_data:
                        if i.get('employee_gid') == d.get('empgid'):
                            d["employee_name"] = i.get('employee_name')
                            d["employee_code"] = i.get('employee_code')
                            d["employee_designation"] = i.get('designation_name')
                            d["gstno"] = i.get('gstno')
                            break

                if onbehalf_gid != []:
                    emp_data = {
                        "empids": onbehalf_gid
                    }
                    obj_eclaim.filter_json = json.dumps(emp_data)
                    obj_eclaim.json_classification = '{}'
                    emp_out_message = obj_eclaim.eClaim_employee_get()
                    onbehalof_employee = json.loads(emp_out_message.get("DATA").to_json(orient='records'))
                    common.logger.error([{"Aprovaldata_onbehalof_employee": str(onbehalof_employee)}])
                    for d in data:
                        for i in onbehalof_employee:
                            if i.get('employee_gid') == d.get('onbehalof'):
                                d["onbehalof_employeename"] = i.get('employee_name')
                                d["onbehalof_employeecode"] = i.get('employee_code')
                                break
                common.logger.error([{"Aprovaldata_data2": str(data)}])
                ld_dict = {"DATA": data, "MESSAGE": 'FOUND', "STATUS": 0}

            elif ld_out_message.get("MESSAGE") == 'NOT_FOUND':
                ld_dict = {"MESSAGE": 'NOT_FOUND', "STATUS": 1}
            else:
                ld_dict = {"MESSAGE": 'ERROR_OCCURED.' + ld_out_message.get("MESSAGE"), "STATUS": 1}
            return Response(ld_dict)
        except Exception as e:
            common.logger.error(e)
            e = "Erro Line no :" + str(format(sys.exc_info()[-1].tb_lineno)) + " " + "Error :" + str(e)
            return Response({"MESSAGE": "ERROR_OCCURED", "DATA": str(e), "STATUS": 1})
class Approval_Flow(APIView):
    def get(self,request):
        try:
            obj_claim = meClaim.eClaim_Model()
            out_data = ""
            if request.query_params.get("Api_Type") == "WEB":
                emp_gid = request.query_params.get("Employee_gid")
                entity = request.query_params.get("Entity_Gid")
                TourGid = request.query_params.get("TourGid")
                AppType = request.query_params.get("AppType")
                obj_claim.filter_json = json.dumps(
                    {"Employee_gid": emp_gid, "Entity_Gid": entity, "TourGid": TourGid, "AppType": AppType})
                out_data = obj_claim.eClaim_approvalflow_get()
            else:
                filter = android.Android.get_method(self, request)
                obj_claim.filter_json = json.dumps(filter)
                out_data = obj_claim.eClaim_approvalflow_get()

            if out_data.get("MESSAGE") == 'FOUND':
                out_data = json.loads(out_data.get("DATA").to_json(orient='records'))
                emp_gid = []
                onbehalf_gid = []
                for d in out_data:
                    emp_gid.append(d.get('approvedby'))
                    if d.get('onbehalof') not in onbehalf_gid and d.get('onbehalof') != 0:
                        onbehalf_gid.append(d.get('onbehalof'))

                emp_data = {
                    "empids": emp_gid
                }
                obj_claim.filter_json = json.dumps(emp_data)
                obj_claim.json_classification = json.dumps({})
                emp_out_message = obj_claim.eClaim_employee_get()
                employee_data = json.loads(emp_out_message.get("DATA").to_json(orient='records'))
                for d in out_data:
                    for i in range(0, len(employee_data)):
                        if employee_data[i].get('employee_gid') == d.get('approvedby'):
                            d["employee_name"] = employee_data[i].get('employee_name')
                            d["employee_code"] = employee_data[i].get('employee_code')
                            break
                if onbehalf_gid != []:
                    emp_data = {
                        "empids": onbehalf_gid
                    }
                    obj_claim.filter_json = json.dumps(emp_data)
                    obj_claim.json_classification = json.dumps({})
                    emp_out_message = obj_claim.eClaim_employee_get()
                    onbehalof_employee = json.loads(emp_out_message.get("DATA").to_json(orient='records'))
                    for d in out_data:
                        for i in range(0, len(onbehalof_employee)):
                            if onbehalof_employee[i].get('employee_gid') == d.get('onbehalof'):
                                d["onbehalof_employeename"] = onbehalof_employee[i].get('employee_name')
                                d["onbehalof_employeecode"] = onbehalof_employee[i].get('employee_code')
                                break

                ld_dict = {"DATA": out_data, "MESSAGE": 'FOUND', "STATUS": 0}

            elif out_data.get("MESSAGE") == 'NOT_FOUND':
                ld_dict = {"MESSAGE": 'NOT_FOUND', "STATUS": 1}
            else:
                ld_dict = {"MESSAGE": 'ERROR_OCCURED.' + out_data.get("MESSAGE"), "STATUS": 1}
            return Response(ld_dict)
        except Exception as e:
            common.logger.error(e)
            return Response({"MESSAGE": "ERROR_OCCURED", "DATA": str(e),"STATUS":1})
class Approval_Flow_Pdf(APIView):
    def get(self,request):
        try:
            obj_claim = meClaim.eClaim_Model()
            InvhdGid = request.query_params.get("Invoice_Header_Gid")
            AppType = request.query_params.get("AppType")
            obj_claim.filter_json = json.dumps({"Invoice_Header_Gid": InvhdGid, "AppType": AppType})
            out_data = obj_claim.eClaim_approvalflow_pdf_get()
            if out_data.get("MESSAGE") == 'FOUND':
                out_data = json.loads(out_data.get("DATA").to_json(orient='records'))
                emp_gid = []
                onbehalf_gid = []
                for d in out_data:
                    emp_gid.append(d.get('approvedby'))
                    if d.get('onbehalof') not in onbehalf_gid and d.get('onbehalof') != 0:
                        onbehalf_gid.append(d.get('onbehalof'))

                emp_data = {
                    "empids": emp_gid
                }
                obj_claim.filter_json = json.dumps(emp_data)
                obj_claim.json_classification = json.dumps({})
                emp_out_message = obj_claim.eClaim_employee_get()
                employee_data = json.loads(emp_out_message.get("DATA").to_json(orient='records'))
                for d in out_data:
                    for i in range(0, len(employee_data)):
                        if employee_data[i].get('employee_gid') == d.get('approvedby'):
                            d["employee_name"] = employee_data[i].get('employee_name')
                            d["employee_code"] = employee_data[i].get('employee_code')
                            break
                if onbehalf_gid != []:
                    emp_data = {
                        "empids": onbehalf_gid
                    }
                    obj_claim.filter_json = json.dumps(emp_data)
                    obj_claim.json_classification = json.dumps({})
                    emp_out_message = obj_claim.eClaim_employee_get()
                    onbehalof_employee = json.loads(emp_out_message.get("DATA").to_json(orient='records'))
                    for d in out_data:
                        for i in range(0, len(onbehalof_employee)):
                            if onbehalof_employee[i].get('employee_gid') == d.get('onbehalof'):
                                d["onbehalof_employeename"] = onbehalof_employee[i].get('employee_name')
                                d["onbehalof_employeecode"] = onbehalof_employee[i].get('employee_code')
                                break

                ld_dict = {"DATA": out_data, "MESSAGE": 'FOUND', "STATUS": 0}

            elif out_data.get("MESSAGE") == 'NOT_FOUND':
                ld_dict = {"MESSAGE": 'NOT_FOUND', "STATUS": 1}
            else:
                ld_dict = {"MESSAGE": 'ERROR_OCCURED.' + out_data.get("MESSAGE"), "STATUS": 1}
            return Response(ld_dict)
        except Exception as e:
            common.logger.error(e)
            return Response({"MESSAGE": "ERROR_OCCURED", "DATA": str(e),"STATUS":1})
class Tour_Details(APIView):
    def get(self,request):
        try:
            obj_claim = meClaim.eClaim_Model()
            emp_gid = request.auth.payload.get('user_id')
            obj_claim.employee_gid = emp_gid
            emp_bnk = obj_claim.eClaim_entity_get()
            bank_data = json.loads(emp_bnk.get("DATA").to_json(orient='records'))
            entity = bank_data[0].get('entity_gid')
            Tour_Gid = request.query_params.get("Tour_Gid")
            obj_claim.filter_json = json.dumps(
                {"Employee_gid": emp_gid, "Entity_Gid": entity, "Tour_Gid": Tour_Gid})
            out_data = obj_claim.eClaim_tourdetails_get()
            if out_data.get("MESSAGE") == 'FOUND':
                data = json.loads(out_data.get("DATA").to_json(orient='records'))
                out_data = []
                for d in data:
                    tmp = {}
                    tmp['gid'] = d.get('gid')
                    tmp['requestno'] = d.get('requestno')
                    tmp['requestdate'] = d.get('requestdate')
                    tmp['tourreason'] = d.get('name')
                    tmp['empgid'] = d.get('empgid')
                    tmp['empgrade'] = d.get('empgrade')
                    tmp['empdesignation'] = d.get('empdesignation')
                    tmp['reason'] = d.get('reason')
                    tmp['startdate'] = d.get('startdate')
                    tmp['enddate'] = d.get('enddate')
                    tmp['permittedby'] = d.get('permittedby')
                    tmp['durationdays'] = d.get('durationdays')
                    tmp['eligiblemodeoftravel'] = d.get('eligiblemodeoftravel')
                    tmp['ordernoremarks'] = d.get('ordernoremarks')
                    tmp['tourdetails'] = json.loads(d.get('tourdetails'))
                    tmp['approvedby'] = d.get('approvedby')
                    tmp['quantum_offunds'] = d.get('quantum_offunds')
                    tmp['opening_balance'] = d.get('opening_balance')
                    out_data.append(tmp)
                emp_gid = []
                emp_data = {
                    "empids": out_data[0].get('empgid')
                }
                obj_claim.filter_json = json.dumps(emp_data)
                obj_claim.json_classification = json.dumps({})
                emp_out_message = obj_claim.eClaim_employee_get()
                employee_data = json.loads(emp_out_message.get("DATA").to_json(orient='records'))
                for d in out_data:
                    d["employee_name"] = employee_data[0].get('employee_name')
                    d["employee_code"] = employee_data[0].get('employee_code')
                    d["employee_branch"] = employee_data[0].get('branch_name')
                    d["employee_designation"] = employee_data[0].get('designation_name')

                if out_data[0].get('permittedby') != None or out_data[0].get('permittedby') != 0 or out_data[0].get('permittedby') != '0':
                    permit_data = {
                        "empids": out_data[0].get('permittedby')
                    }
                    obj_claim.filter_json = json.dumps(permit_data)
                    obj_claim.json_classification = json.dumps({})
                    permit_out_message = obj_claim.eClaim_employee_get()
                    permitemp_data = json.loads(permit_out_message.get("DATA").to_json(orient='records'))
                    for d in out_data:
                        d["permit_empname"] = permitemp_data[0].get('employee_name')
                        d["permit_empcode"] = permitemp_data[0].get('employee_code')

                approval_data = {
                    "empids": out_data[0].get('approvedby')
                }
                obj_claim.filter_json = json.dumps(approval_data)
                obj_claim.json_classification = json.dumps({})
                approval_out_message = obj_claim.eClaim_employee_get()
                approval_data = json.loads(approval_out_message.get("DATA").to_json(orient='records'))
                if approval_data != []:
                    for d in out_data:
                        d["approval_empname"] = approval_data[0].get('employee_name')
                        d["approval_empcode"] = approval_data[0].get('employee_code')
                        d["approval_branch"] = approval_data[0].get('branch_name')

                obj_claim.filter_json = json.dumps({"Tour_gid": Tour_Gid})
                ld_out_file = obj_claim.eClaim_file_get()

                file = json.loads(ld_out_file.get("DATA").to_json(orient='records'))
                filedata = []
                for i in file:
                    s3_client = boto3.client('s3','ap-south-1')
                    response = s3_client.generate_presigned_url('get_object',
                                                                Params={'Bucket': S3_BUCKET_NAME,
                                                                        'Key': i.get('file_path')},
                                                                ExpiresIn=None)
                    data = {
                        "file_gid": i.get('file_gid'),
                        "file_key": i.get('file_path'),
                        "file_name": i.get('file_name'),
                        "file_path": response,
                        "file_refgid": i.get('file_refgid')
                    }
                    filedata.append(data)

                ld_dict = {"DATA": out_data[0],
                           "FILE": filedata,
                           "MESSAGE": 'FOUND', "STATUS": 0}
            elif out_data.get("MESSAGE") == 'NOT_FOUND':
                ld_dict = {"MESSAGE": 'NOT_FOUND', "STATUS": 1}
            else:
                ld_dict = {"MESSAGE": 'ERROR_OCCURED.' + out_data.get("MESSAGE"), "STATUS": 1}
            return Response(ld_dict)
        except Exception as e:
            common.logger.error(e)
            return Response({"MESSAGE": "ERROR_OCCURED", "DATA": str(e),"STATUS":1})
class Branch(APIView):
    def get(self,request):
        try:
            ld_out_message = ""
            obj_claim = meClaim.eClaim_Model()
            ld_out_message = ''
            if request.query_params.get("Api_Type") == "WEB":
                emp_gid = request.query_params.get("Employee_gid")
                entity = request.query_params.get("Entity_Gid")
                Limit_Start = request.query_params.get("Limit_Start")
                Limit_End = request.query_params.get("Limit_End")
                branch_name = request.query_params.get("branch_name")
                branch_code = request.query_params.get("branch_code")
                branch_detail = request.query_params.get("branch_detail")
                obj_claim.filter_json = json.dumps({
                    "Employee_gid":emp_gid,
                    "Entity_Gid":entity,
                    "Limit_Start":Limit_Start,
                    "Limit_End":Limit_End,
                    "branch_name":branch_name,
                    "branch_code":branch_code,
                    "branch_detail":branch_detail
                })
                ld_out_message = obj_claim.eClaim_branch_get()
            else:
                filter = android.Android.get_method(self, request)
                # filter['Limit_Start'] = 0
                # filter['Limit_End'] = 30
                obj_claim.filter_json = json.dumps(filter)
                ld_out_message = obj_claim.eClaim_branch_get()

            if ld_out_message.get("MESSAGE") == 'FOUND':
                data = json.loads(ld_out_message.get("DATA").to_json(orient='records'))
                if 'Total_Row' in data[0]:
                    length = data[0].get('Total_Row')
                    ld_dict = {"DATA": data,"MESSAGE": 'FOUND',"STATUS":0,"LENGTH":length}
                else:
                    ld_dict = {"DATA": data,"MESSAGE": 'FOUND', "STATUS": 0}
            elif ld_out_message.get("MESSAGE") == 'NOT_FOUND':
                ld_dict = {"MESSAGE": 'NOT_FOUND',"STATUS":1}
            else:
                ld_dict = {"MESSAGE": 'ERROR_OCCURED.' + ld_out_message.get("MESSAGE"),"STATUS":1}
            return Response(ld_dict)
        except Exception as e:
            common.logger.error(e)
            return Response({"MESSAGE": "ERROR_OCCURED", "DATA": str(e),"STATUS":1})
class Tour_Reason(APIView):
    def get(self,request):
        try:
            obj_claim = meClaim.eClaim_Model()
            out_data = ''
            if request.query_params.get("Api_Type") == "WEB":
                emp_gid = request.query_params.get("Employee_gid")
                entity = request.query_params.get("Entity_Gid")
                obj_claim.filter_json = json.dumps({"Employee_gid": emp_gid, "Entity_Gid": entity})
                out_data = obj_claim.eClaim_tourreason_get()
            else:
                filter = android.Android.get_method(self, request)
                obj_claim.filter_json = json.dumps(filter)
                out_data = obj_claim.eClaim_tourreason_get()

            ld_elig = json.loads(out_data.get("DATA").to_json(orient='records'))
            ld_dict = {"DATA": ld_elig,
                       "MESSAGE": 'FOUND', "STATUS": 0}
            return Response(ld_dict)
        except Exception as e:
            common.logger.error(e)
            return Response({"MESSAGE": "ERROR_OCCURED", "DATA": str(e),"STATUS":1})
class Eligible(APIView):
    def get(self,request):
        try:
            grade = request.query_params.get("GRADE")
            data_eligible = verify.travel_exp.grade_eligible(self, grade.upper())
            ld_dict = {"DATA": data_eligible.get('type').get('type'),
                       "MESSAGE": 'FOUND', "STATUS": 0}
            return Response(ld_dict)
        except Exception as e:
            common.logger.error(e)
            return Response({"MESSAGE": "ERROR_OCCURED", "DATA": str(e),"STATUS":1})
class Employee_Data(APIView):
    def get(self,request):
        try:
            obj_claim = meClaim.eClaim_Model()
            if request.query_params.get("Type") == "ONBEHALF":
                employee_gid = request.query_params.get("Employee_gid")
            else:
                employee_gid = request.auth.payload.get('user_id')
            emp_gid = []
            emp_gid.append(employee_gid)
            emp_data = {
                "empids": emp_gid
            }
            obj_claim.filter_json = json.dumps(emp_data)
            obj_claim.json_classification = json.dumps({})
            emp_out_message = obj_claim.eClaim_employee_get()
            employee_data = json.loads(emp_out_message.get("DATA").to_json(orient='records'))
            common.logger.error([{"employee_data": str(employee_data)}])
            employee_code = employee_data[0].get('employee_code')
            #employee_code ="002892"
            # if employee_code[0:2].upper() == 'VS':
            obj_claim.employee_gid = employee_gid
            emp_bnk = obj_claim.eClaim_entity_get()
            bank_data = json.loads(emp_bnk.get("DATA").to_json(orient='records'))
            if len(bank_data) != 0:
                entity = bank_data[0].get('entity_gid')
                emp_gid = []
                emp_gid.append(employee_gid)
                emp_data = {
                    "empids": emp_gid
                }
                obj_claim.filter_json = json.dumps(emp_data)
                obj_claim.json_classification = json.dumps({"Entity_Gid": entity})
                emp_out_message = obj_claim.eClaim_employee_get()
                employee_data = json.loads(emp_out_message.get("DATA").to_json(orient='records'))
                if employee_code[0:2].upper() == 'VS':
                    designation = obj_claim.eClaim_empgrade_get()
                    designation = json.loads(designation.get("DATA").to_json(orient='records'))
                    for i in employee_data:
                        for j in designation:
                            if i.get('designation_name').upper() == j.get('designation').upper():
                                i['grade'] = j.get('grade')
                                break
                #else:
                #    for i in employee_data:
                #       i['grade'] = i.get('employee_grade2')

                employee = employee_data[0]
                #employee['employee_code'] = "002892"
                common.logger.error([{"employee": str(employee)}])
                employee['entity_gid'] = bank_data[0].get('entity_gid')
                ld_dict = {"DATA": employee,
                           "MESSAGE": 'FOUND'}
                return Response(ld_dict)
            else:
                ld_dict = {"MESSAGE": 'NOT FOUND'}
                return Response(ld_dict)
            # else:
            #     obj_claim.filter_json = json.dumps({"employeecode": employee_code})
            #     emp = obj_claim.eClaim_employee_tmp_get()
            #     data = json.loads(emp.get("DATA").to_json(orient='records'))
            #     data = data[0]
            #     token_status = 1
            #     generated_token_data = master_views.master_sync_Data_("GET", "get_data", employee_gid)
            #     log_data = generated_token_data
            #     token = generated_token_data.get("DATA")[0].get("clienttoken_name")
            #     if (token == " " or token == None):
            #         token_status = 0
            #     if token_status == 1:
            #         try:
            #             client_api = common.clientapi()
            #             headers = {"Content-Type": "application/json", "Authorization": "Bearer " + token}
            #             data_depent = {
            #                 "UserName": "EMCUSER",
            #                 "Password": "9f",
            #                 "EmpId": str(employee_code),
            #                 "DtlsToBeFetch": "DependentDetails"
            #             }
            #             data_depent = json.dumps(data_depent)
            #             result2 = requests.post("" + client_api + "/next/v1/mw/employee-detail", headers=headers,
            #                                    data=data_depent,
            #                                    verify=False)
            #             results_data2 = json.loads(result2.content.decode("utf-8"))
            #             status2 = results_data2.get("out_msg").get("ErrorMessage")
            #             if (status2 == "Success"):
            #                 data_dependent = results_data2.get("out_msg")
            #                 push_data = {
            #                     "Employee_gid":employee_gid,
            #                      "Base_details":{},
            #                      "Dependent_details":data_dependent,
            #                      "processedby":employee_gid
            #                     }
            #                 obj_claim.jsonData = json.dumps(push_data)
            #                 hrd_set = obj_claim.eClaim_hrd_employeedtl_set()
            #                 if hrd_set.get("MESSAGE") == 'SUCCESS':
            #                     obj_claim.employee_gid = employee_gid
            #                     emp_bnk = obj_claim.eClaim_entity_get()
            #                     bank_data = json.loads(emp_bnk.get("DATA").to_json(orient='records'))
            #                     if len(bank_data) != 0:
            #                         entity = bank_data[0].get('entity_gid')
            #                         emp_gid = []
            #                         emp_gid.append(employee_gid)
            #                         emp_data = {
            #                             "empids": emp_gid
            #                         }
            #                         obj_claim.filter_json = json.dumps(emp_data)
            #                         obj_claim.json_classification = json.dumps({"Entity_Gid": entity})
            #                         emp_out_message = obj_claim.eClaim_employee_get()
            #                         employee_data = json.loads(
            #                             emp_out_message.get("DATA").to_json(orient='records'))
            #                         employee = employee_data[0]
            #                         employee['designation_name'] = data.get('edesig')
            #                         employee['grade'] = data.get('egrade2')
            #                         employee['entity_gid'] = bank_data[0].get('entity_gid')
            #                         ld_dict = {"DATA": employee,
            #                                    "MESSAGE": 'FOUND'}
            #                         return Response(ld_dict)
            #                     else:
            #                         ld_dict = {"MESSAGE": 'NOT FOUND'}
            #                         return Response(ld_dict)
            #                 else:
            #                     ld_dict = {"MESSAGE": 'ERROR_OCCURED.' + hrd_set.get("MESSAGE"), "STATUS": 1}
            #             else:
            #                 return Response({"MESSAGE": "FAILED", "FAILED_STATUS": results_data2})
            #         except Exception as e:
            #             common.logger.error(e)
            #             return Response({"MESSAGE": "ERROR_OCCURED_ON_AMOUNT_TRANSFER_CLINET_API", "DATA": str(e),
            #                              "log_data": log_data})
            #     else:
            #         return Response({"MESSAGE": "ERROR_OCCURED_ON_TOKEN_GENERATIONS OR INVALID AUTHENTICATONS"})
        except Exception as e:
            common.logger.error(e)
            return Response({"MESSAGE": "ERROR_OCCURED", "DATA": str(e),"STATUS":1})
class Emp_Branch(APIView):
    def get(self,request):
        try:
            obj_claim = meClaim.eClaim_Model()
            out_data = ""
            if request.query_params.get("Api_Type") == "WEB":
                emp_gid = request.query_params.get("Employee_gid")
                type = request.query_params.get("Type")
                entity_gid = request.query_params.get("Entity_Gid")
                branch = request.query_params.get("Branch_Gid")
                obj_claim.filter_json = json.dumps({"Employee_gid": emp_gid, "Entity_Gid": entity_gid, "Branch_Gid": branch})
                out_data = obj_claim.eClaim_branchtoemp_get()
                if out_data.get("MESSAGE") == 'FOUND':
                    empdata = json.loads(out_data.get("DATA").to_json(orient='records'))
                    if type == "APPROVER":
                        obj_claim.filter_json = json.dumps({"Entity_Gid": entity_gid, "Branch_Gid": branch})
                        ld_out_message = obj_claim.eClaim_approverlist_get()
                        if ld_out_message.get("MESSAGE") == 'FOUND':
                            app_data = json.loads(ld_out_message.get("DATA").to_json(orient='records'))
                            final_data = []
                            app_data1 = app_data[0].get('employee_gid')
                            app_data2 = json.loads(app_data1)
                            for i in empdata:
                                if i.get('employee_gid') not  in app_data2:
                                    final_data.append(i)
                            ld_dict = {"DATA": final_data,
                                       "MESSAGE": 'FOUND', "STATUS": 0}

                        else:
                            ld_dict = {"DATA": empdata,
                                       "MESSAGE": 'FOUND', "STATUS": 0}
                    else:
                        ld_dict = {"DATA": empdata,
                                   "MESSAGE": 'FOUND', "STATUS": 0}

                elif out_data.get("MESSAGE") == 'NOT_FOUND':
                    ld_dict = {"MESSAGE": 'NOT_FOUND', "STATUS": 1}
                else:
                    ld_dict = {"MESSAGE": 'ERROR_OCCURED.' + out_data.get("MESSAGE"), "STATUS": 0}
                return Response(ld_dict)
            else:
                type = request.query_params.get("Type")
                branch = request.query_params.get("Branch_Gid")
                empgid = request.auth.payload.get('user_id')
                obj_claim = meClaim.eClaim_Model()
                obj_claim.employee_gid = empgid
                emp_bnk = obj_claim.eClaim_entity_get()
                bank_data = json.loads(emp_bnk.get("DATA").to_json(orient='records'))
                entity_gid = bank_data[0].get('entity_gid')
                if type == "SELF":
                    filter = {
                        "Entity_Gid": entity_gid,
                        "Branch_Gid": branch
                    }
                else:
                    filter = {
                        "Employee_gid": empgid,
                        "Branch_Gid": branch,
                        "Entity_Gid": entity_gid
                    }
                obj_eclaim = meClaim.eClaim_Model()
                obj_claim.filter_json = json.dumps(filter)
                out_data = obj_claim.eClaim_branchtoemp_get()

                if out_data.get("MESSAGE") == 'FOUND':
                    empdata = json.loads(out_data.get("DATA").to_json(orient='records'))
                    if type == "APPROVER":
                        obj_claim.filter_json = json.dumps({"Entity_Gid": entity_gid, "Branch_Gid": branch})
                        ld_out_message = obj_claim.eClaim_approverlist_get()
                        if ld_out_message.get("MESSAGE") == 'FOUND':
                            app_data = json.loads(ld_out_message.get("DATA").to_json(orient='records'))
                            final_data = []
                            app_data1 = app_data[0].get('employee_gid')
                            app_data2 = json.loads(app_data1)
                            for i in empdata:
                                if i.get('employee_gid') not  in app_data2:
                                    final_data.append(i)
                            ld_dict = {"DATA": final_data,
                                       "MESSAGE": 'FOUND', "STATUS": 0}
                        else:
                            ld_dict = {"DATA": empdata,
                                       "MESSAGE": 'FOUND', "STATUS": 0}
                    else:
                        ld_dict = {"DATA": empdata,
                                   "MESSAGE": 'FOUND', "STATUS": 0}

                elif out_data.get("MESSAGE") == 'NOT_FOUND':
                    ld_dict = {"MESSAGE": 'NOT_FOUND', "STATUS": 1}
                else:
                    ld_dict = {"MESSAGE": 'ERROR_OCCURED.' + out_data.get("MESSAGE"), "STATUS": 0}
                return Response(ld_dict)
        except Exception as e:
            common.logger.error(e)
            return Response({"MESSAGE": "ERROR_OCCURED", "DATA": str(e),"STATUS":1})
class Forward_Get(APIView):
    def get(self,request):
        try:
            obj_claim = meClaim.eClaim_Model()
            out_data = ""
            if request.query_params.get("Api_Type") == "WEB":
                approvedby = request.query_params.get("approvedby")
                entity = request.query_params.get("Entity_Gid")
                apptype = request.query_params.get("apptype")
                obj_claim.filter_json = json.dumps({"approvedby": approvedby, "Entity_Gid": entity, "apptype": apptype})
                out_data = obj_claim.eClaim_forward_get()

            else:
                filter = android.Android.get_method(self, request)
                empid = request.auth.payload.get('user_id')
                filter['approvedby'] = empid
                obj_claim.filter_json = json.dumps(filter)
                out_data = obj_claim.eClaim_forward_get()

            if out_data.get("MESSAGE") == 'FOUND':
                data =  json.loads(out_data.get("DATA").to_json(orient='records'))
                emp_gid = []

                for i in data:
                    if i.get('empgid') not in emp_gid and i.get('empgid') != 0:
                        emp_gid.append(i.get('empgid'))
                emp_data = {
                    "empids": emp_gid
                }
                obj_claim.filter_json = json.dumps(emp_data)
                obj_claim.json_classification = json.dumps({})
                emp_out_message = obj_claim.eClaim_employee_get()
                employee_data = json.loads(emp_out_message.get("DATA").to_json(orient='records'))
                if len(employee_data) == 0:
                    ld_dict = {"MESSAGE": 'Not Found Employee Data', "STATUS": 1}
                    return Response(ld_dict)

                for d in data:
                    for i in range(0, len(employee_data)):
                        if employee_data[i].get('employee_gid') == int(d.get('empgid')):
                            d["employee_name"] = employee_data[i].get('employee_name')
                            d["employee_code"] = employee_data[i].get('employee_code')
                            break
                ld_dict = {"DATA": data,"MESSAGE": 'FOUND',"STATUS":0}

            elif out_data.get("MESSAGE") == 'NOT_FOUND':
                ld_dict = {"MESSAGE": 'NOT_FOUND', "STATUS": 1}
            else:
                ld_dict = {"MESSAGE": 'ERROR_OCCURED.' + out_data.get("MESSAGE"), "STATUS": 0}
            return Response(ld_dict)
        except Exception as e:
            common.logger.error(e)
            er = "Erro Line no :" + str(format(sys.exc_info()[-1].tb_lineno)) + " " + "Error :" + str(e)
            return Response({"MESSAGE": "ERROR_OCCURED", "DATA": er, "STATUS": 1})
import time
class Tour_Maker(APIView):
    def post(self,request):
        try:
            ld_out_message = ""
            path = self.request.stream.path

            obj_claim = meClaim.eClaim_Model()
            if request.query_params.get("Api_Type") == "WEB":
                jsondata = json.loads(request.body.decode('utf-8'))
                obj_claim.jsondata = json.dumps(jsondata.get('Params').get('DETAILS'))
                obj_claim.jsonData = json.dumps(jsondata.get('Params').get('CHANGE'))
                common.main_fun1(request.read(), path)
                ld_out_message = obj_claim.eClaim_tourrequest_set()
                msg = ld_out_message.get("MESSAGE").split(",")
                print(msg)
                if msg[0] == 'SUCCESS':
                    file_data = jsondata.get('Params').get('FILE').get('File')
                    if file_data != []:
                        for i in jsondata.get('Params').get('FILE').get('File'):
                            i['RefGid'] = msg[1]
                        obj_claim.jsonData = json.dumps(jsondata.get('Params').get('FILE'))
                        out_message = obj_claim.eClaim_file_set()
                        if out_message.get("MESSAGE") == 'SUCCESS':
                            ld_out_message = {"MESSAGE": "SUCCESS"}
                    else:
                        ld_out_message = {"MESSAGE": "SUCCESS"}
                else:
                    ld_out_message = {"MESSAGE": msg[1]}
            else:
                common.logger.error([{"Mobile": str("Yes")}])
                jsondata = request.POST['Tour']
                jsondata = json.loads(request.POST['Tour'])
                common.logger.error([{"jsondata": str(jsondata)}])
                DETAILS = jsondata.get('DETAILS')
                DETAILS = android.Android.gid_check(self, DETAILS)
                common.logger.error([{"DETAILS": str(DETAILS)}])
                change = jsondata.get('DATA')
                final = {
                    "DATA": change
                }
                CHANGE = final
                CHANGE = android.Android.gid_array_check(self, CHANGE)
                common.logger.error([{"CHANGE": str(CHANGE)}])
                if 'onbehalfof' in DETAILS:
                    empgid = DETAILS.get('onbehalfof')
                    DETAILS['onbehalfof'] = request.auth.payload.get('user_id')
                else :
                    empgid = request.auth.payload.get('user_id')

                emp_data = {
                    "empids": empgid
                }
                obj_claim.filter_json = json.dumps(emp_data)
                emp_bnk = obj_claim.eClaim_employeebnk_get()
                bank_data = json.loads(emp_bnk.get("DATA").to_json(orient='records'))
                entity = bank_data[0].get('entity_gid')
                files = []
                if request.FILES:
                    for i in range(0, len(request.FILES)):
                        name = "file" + str(i)
                        for j in request.FILES.getlist(name):
                            file_data = j
                            millis = int(round(time.time() * 1000))
                            file_name_new = str(empgid) + '_' + str(millis) + '_' + str(i) + str(j.name)
                            contents = file_data
                            s3 = boto3.resource('s3')
                            s3_obj = s3.Object(bucket_name=S3_BUCKET_NAME, key=file_name_new)
                            s3_obj.put(Body=contents)
                            content = {
                                "File_path": file_name_new,
                                "File_name": str(request.FILES[name].name),
                                "Entity_gid": entity,
                                "createby": empgid
                            }

                            files.append(content)

                common.logger.error([{"files": str(files)}])
                emp_gid = []
                emp_gid.append(empgid)
                emp_data = {
                    "empids": emp_gid
                }
                obj_claim.filter_json = json.dumps(emp_data)
                obj_claim.json_classification = json.dumps({"Entity_Gid": entity})
                emp_out_message = obj_claim.eClaim_employee_get()
                employee_data = json.loads(emp_out_message.get("DATA").to_json(orient='records'))

                # common.main_fun1(request.read(), path)
                common.logger.error([{"MAKER_employee_data": str(employee_data)}])
                # request_date = now.strftime("%Y-%m-%d %H:%M")
                strdt = DETAILS.get('startdate')
                frdt = DETAILS.get('enddate')
                datetimeFormat = '%Y-%m-%d %H:%M'
                diff = datetime.datetime.strptime(frdt, datetimeFormat) - datetime.datetime.strptime(strdt, datetimeFormat)
                day = str(diff).split()
                days = diff.days

                obj_claim.date = 'DATE'
                date = obj_claim.get_server_date()

                DETAILS['durationdays'] =days
                DETAILS['requestdate'] =date
                DETAILS['empgid'] = empgid
                DETAILS['empdesignation'] = employee_data[0].get('employee_designation_gid')
                DETAILS['empdepartmentgid'] = employee_data[0].get('employee_dept_gid')
                DETAILS['empgrade'] = "S3"
                DETAILS['empbranchgid'] = employee_data[0].get('branch_gid')
                DETAILS['stategid'] = employee_data[0].get('state_gid')
                DETAILS['processedby'] =  empgid
                DETAILS['createby'] =  empgid
                common.logger.error([{"DETAILS2": str(DETAILS)}])
                obj_claim.jsondata = json.dumps(DETAILS)
                obj_claim.jsonData = json.dumps(CHANGE)
                ld_out_message = obj_claim.eClaim_tourrequest_set()
                msg = ld_out_message.get("MESSAGE").split(",")
                print(msg)
                if msg[0] == 'SUCCESS':
                    common.logger.error([{"msg[1]": str(msg[1])}])
                    #file_data = jsondata.get('Params').get('FILE').get('File')
                    if files != []:
                        for i in files:
                            i['RefGid'] = msg[1]
                        filedata = {
                                "File": files
                            }
                        obj_claim.jsonData = json.dumps(filedata)
                        common.logger.error([{"filedata": str(filedata)}])
                        out_message = obj_claim.eClaim_file_set()
                        if out_message.get("MESSAGE") == 'SUCCESS':
                            ld_out_message = {"MESSAGE": "SUCCESS"}
                        else:
                            ld_out_message = {"MESSAGE": 'ERROR_OCCURED.' + ld_out_message.get("MESSAGE"), "STATUS": 1}
                    else:
                        ld_out_message = {"MESSAGE": "SUCCESS"}
                    ld_out_message = {"MESSAGE": "SUCCESS"}
                else:
                    ld_out_message = {"MESSAGE": msg[1]}
            if ld_out_message.get("MESSAGE") == 'SUCCESS':
                ld_dict = {"MESSAGE": "SUCCESS", "STATUS": 0}
            elif ld_out_message.get("MESSAGE") == 'FAIL':
                ld_dict = {"MESSAGE": "FAIL", "STATUS": 1}
            else:
                ld_dict = {"MESSAGE": 'ERROR_OCCURED.' + ld_out_message.get("MESSAGE"), "STATUS": 1}
            return Response(ld_dict)
        except Exception as e:
            common.logger.error(e)
            e = "Erro Line no :" + str(format(sys.exc_info()[-1].tb_lineno)) + " " + "Error :" + str(e)
            return Response({"MESSAGE": "ERROR_OCCURED", "DATA": str(e), "STATUS": 1})
class eClaim_Approve(APIView):
    def post(self,request):
        try:
            ld_out_message = ""
            path = self.request.stream.path
            jsondata = json.loads(request.body.decode('utf-8'))
            entity = 0
            emp_gid = 0
            obj_claim = meClaim.eClaim_Model()
            if request.query_params.get("Api_Type") == "WEB":
                tourgid = jsondata.get('Params').get('DETAILS').get('tourgid')
                common.main_fun1(request.read(), path)
                obj_claim.employee_gid = tourgid
                ld_out_emp = obj_claim.eClaim_tourtoemp_get()
                ld_dict = json.loads(ld_out_emp.get("DATA").to_json(orient='records'))
                common.logger.error([{"tourtoemp_get": str(ld_dict)}])
                emp_gid = ld_dict[0].get('empgid')
                obj_claim.employee_gid = emp_gid
                emp_bnk = obj_claim.eClaim_entity_get()
                data = json.loads(emp_bnk.get("DATA").to_json(orient='records'))
                if len(data) != 0:
                    entity = data[0].get('entity_gid')

                obj_claim.action = "GET"
                obj_claim.type = "EMPLOYEE_DETAILS"
                filter = {"employee_gid": emp_gid}
                obj_claim.filter = json.dumps(filter)
                obj_claim.classification = json.dumps({"Entity_Gid": int(entity)})
                emp_bnk = obj_claim.get_APbankdetails()
                bank_data = json.loads(emp_bnk.get("DATA").to_json(orient='records'))
                common.logger.error([{"bankdata": str(bank_data)}])
                if len(bank_data) != 0:
                    empBank = bank_data[0].get('bankdetails_gid')
                    accno = bank_data[0].get('bankdetails_acno')
                else:
                    return Response({"MESSAGE": "Employee Bank Data Missing"})
                obj_claim.jsonData = json.dumps(jsondata.get('Params').get('DETAILS'))
            else:
                common.logger.error([{"Approvedata": str(jsondata)}])
                tourgid = jsondata.get('tourgid')
                obj_claim.employee_gid = tourgid
                ld_out_emp = obj_claim.eClaim_tourtoemp_get()
                ld_dict = json.loads(ld_out_emp.get("DATA").to_json(orient='records'))
                emp_gid = ld_dict[0].get('empgid')
                common.logger.error([{"empid": str(emp_gid)}])
                entity =0
                obj_claim.employee_gid = emp_gid
                emp_bnk = obj_claim.eClaim_entity_get()
                data = json.loads(emp_bnk.get("DATA").to_json(orient='records'))
                if len(data) != 0:
                    entity = data[0].get('entity_gid')
                common.logger.error([{"entity": str(entity)}])
                obj_claim.action = "GET"
                obj_claim.type = "EMPLOYEE_DETAILS"
                filter = {"employee_gid": emp_gid}
                obj_claim.filter = json.dumps(filter)
                obj_claim.classification = json.dumps({"Entity_Gid": int(entity)})
                emp_bnk = obj_claim.get_APbankdetails()
                bank_data = json.loads(emp_bnk.get("DATA").to_json(orient='records'))
                common.logger.error([{"bankdata": str(bank_data)}])
                if len(bank_data) != 0 or bank_data != [] or bank_data != '[]':
                    empBank = bank_data[0].get('bankdetails_gid')
                    accno = bank_data[0].get('bankdetails_acno')
                else:
                    return Response({"MESSAGE": "Employee Bank Data Missing"})

                common.main_fun1(request.read(), path)
                jsondata = android.Android.param_conversion2(self, jsondata,entity,emp_gid)
                jsondata['Params']['DETAILS']['approvedby'] = int(jsondata.get('Params').get('DETAILS').get('approvedby'))
                jsondata['Params']['DETAILS']['applevel'] = int(jsondata.get('Params').get('DETAILS').get('applevel'))
                common.logger.error([{"jsondata": str(jsondata)}])
                obj_claim.jsonData = json.dumps(jsondata.get('Params').get('DETAILS'))

            if jsondata.get('Params').get('DETAILS').get('apptype') == "TOURADV" and jsondata.get('Params').get(
                    'DETAILS').get('approvedby') == 0:
                response = verify.ecf_entry.invoice_header(self, request,jsondata)
                common.logger.error([{"response": str(response)}])
                if response.get('MESSAGE') == "SUCCESS":
                    tourgid = jsondata.get('Params').get('DETAILS').get('tourgid')
                    processedby = jsondata.get('Params').get('DETAILS').get('processedby')
                    header_gid = response.get('Header_Gid')
                    advancegid = response.get('advancegid')

                    response_data = verify.ecf_entry.invoice_detail(self, request, response,jsondata)
                    common.logger.error([{"response_data": str(response_data)}])
                    if response_data.get('MESSAGE') == "SUCCESS":
                        ld_out_message = obj_claim.eClaim_movetoapproval2_set()
                        if ld_out_message.get("MESSAGE") == 'SUCCESS':
                            obj_claim.filter_json = json.dumps(
                                {"Invoice_headergid": header_gid})
                            out_data = obj_claim.eClaim_Crnno_get()
                            common.logger.error([{"out_data": str(out_data)}])
                            if out_data.get("MESSAGE") == 'FOUND':
                                data = json.loads(out_data.get("DATA").to_json(orient='records'))
                                crnno = data[0].get('invoiceheader_crno')
                                obj_claim.jsondata = json.dumps(
                                    {"Advance_gid": advancegid,"Invoice_headergid":header_gid,"CRN_No": crnno, "processedby": processedby})
                                out_data = obj_claim.eClaim_advinv_set()
                                if out_data.get("MESSAGE") == 'SUCCESS':
                                    ld_dict = {"MESSAGE": "SUCCESS", "STATUS": 0}
                                elif out_data.get("MESSAGE") == 'FAIL':
                                    ld_dict = {"MESSAGE": "FAIL", "STATUS": 1}
                                else:
                                    er = "Erro Line no :" + str(format(sys.exc_info()[-1].tb_lineno))
                                    ld_dict = {"MESSAGE": 'ERROR_OCCURED.CRNNO UPDATE' + out_data.get("MESSAGE")+str(er), "STATUS": 1}

                            elif out_data.get("MESSAGE") == 'NOT_FOUND':
                                ld_dict = {"MESSAGE": ' CRN NO NOT_FOUND', "STATUS": 1}

                            else:
                                er = "Erro Line no :" + str(format(sys.exc_info()[-1].tb_lineno))
                                ld_dict = {"MESSAGE": 'ERROR_OCCURED.CRN NO GET' + out_data.get("MESSAGE") + str(er),
                                           "STATUS": 1}
                        elif ld_out_message.get("MESSAGE") == 'FAIL':
                            ld_dict = {"MESSAGE": "FAIL", "STATUS": 1}
                        else:
                            er = "Erro Line no :" + str(format(sys.exc_info()[-1].tb_lineno))
                            ld_dict = {"MESSAGE": 'ERROR_OCCURED.' + ld_out_message.get("MESSAGE")+str(er), "STATUS": 1}
                        return Response(ld_dict)

                    else:
                        er = "Erro Line no :" + str(format(sys.exc_info()[-1].tb_lineno))
                        ld_dict = {"MESSAGE": 'ERROR_OCCURED.' + str(response_data.get('MESSAGE'))+str(er), "STATUS": 1}
                        return Response(ld_dict)
                else:
                    er = "Erro Line no :" + str(format(sys.exc_info()[-1].tb_lineno))
                    ld_dict = {"MESSAGE": 'ERROR_OCCURED.' + str(response.get('MESSAGE'))+str(er), "STATUS": 1}
                    return Response(ld_dict)

            elif jsondata.get('Params').get('DETAILS').get('apptype') == "CLAIM" and jsondata.get('Params').get(
                    'DETAILS').get('approvedby') == 0:
                response = verify.ecf_entry.invoice_header(self, request,jsondata)
                common.logger.error([{"invoiceheader_return": str(response)}])
                if response.get('MESSAGE') == "SUCCESS":
                    tourgid = jsondata.get('Params').get('DETAILS').get('tourgid')
                    processedby = jsondata.get('Params').get('DETAILS').get('processedby')
                    header_gid = response.get('Header_Gid')
                    response_data = verify.ecf_entry.invoice_detail(self, request, response,jsondata)
                    common.logger.error([{"invoicedtl_return": str(response_data)}])
                    if response_data.get('MESSAGE') == "SUCCESS":
                        ld_out_message = obj_claim.eClaim_movetoapproval2_set()
                        common.logger.error([{"Approve_entry": str(ld_out_message)}])
                        if ld_out_message.get("MESSAGE") == 'SUCCESS':
                            obj_claim.jsondata = json.dumps(
                                {"Tour_gid": tourgid, "Invoice_Header_Gid": header_gid, "processedby": processedby})
                            out_data = obj_claim.eClaim_expinv_set()
                            if out_data.get("MESSAGE") == 'SUCCESS':
                                ld_dict = {"MESSAGE": "SUCCESS", "STATUS": 0}
                            elif out_data.get("MESSAGE") == 'FAIL':
                                ld_dict = {"MESSAGE": "FAIL", "STATUS": 1}
                            else:
                                ld_dict = {"MESSAGE": 'ERROR_OCCURED.' + out_data.get("MESSAGE"), "STATUS": 1}
                        elif ld_out_message.get("MESSAGE") == 'FAIL':
                            ld_dict = {"MESSAGE": "FAIL", "STATUS": 1}
                        else:
                            ld_dict = {"MESSAGE": 'ERROR_OCCURED.' + str(ld_out_message.get("MESSAGE")), "STATUS": 1}
                        return Response(ld_dict)

                    else:
                        ld_dict = {"MESSAGE": str(response_data.get('MESSAGE')), "STATUS": 1}
                        return Response(ld_dict)
                else:
                    ld_dict = {"MESSAGE": str(response.get('MESSAGE')), "STATUS": 1}
                    return Response(ld_dict)

            elif jsondata.get('Params').get('DETAILS').get('apptype') == "ADVANCECANCEL" and jsondata.get('Params').get(
                    'DETAILS').get('approvedby') == 0:
                response = verify.ecf_reverse_entry.ecf_status_update(self, request, jsondata,entity,emp_gid)
                if response == True:
                    ld_out_message = obj_claim.eClaim_movetoapproval2_set()
                    if ld_out_message.get("MESSAGE") == 'SUCCESS':
                        ld_dict = {"MESSAGE": "SUCCESS", "STATUS": 0}
                    elif ld_out_message.get("MESSAGE") == 'FAIL':
                        ld_dict = {"MESSAGE": "FAIL", "STATUS": 1}
                    else:
                        ld_dict = {"MESSAGE": 'ERROR_OCCURED.' + ld_out_message.get("MESSAGE"), "STATUS": 1}
                    return Response(ld_dict)
                else:
                    ld_dict = {"MESSAGE": 'ERROR_OCCURED.' + response.get("MESSAGE"), "STATUS": 1}
                    return Response(ld_dict)
            else:
                ld_out_message = obj_claim.eClaim_movetoapproval2_set()
                common.logger.error([{"ld_out_message": str(ld_out_message)}])
                if ld_out_message.get("MESSAGE") == 'SUCCESS':
                    ld_dict = {"MESSAGE": "SUCCESS", "STATUS": 0}
                elif ld_out_message.get("MESSAGE") == 'FAIL':
                    ld_dict = {"MESSAGE": "FAIL", "STATUS": 1}
                else:
                    ld_dict = {"MESSAGE": 'ERROR_OCCURED.' + str(ld_out_message.get("MESSAGE")), "STATUS": 1}
                return Response(ld_dict)
        except Exception as e:
            common.logger.error(e)
            return Response({"MESSAGE": "ERROR_OCCURED", "DATA": str(e)+str(response_data),"STATUS":1})
class eClaim_Return(APIView):
    def post(self,request):
        try:
            ld_out_message = ""
            path = self.request.stream.path
            jsondata = json.loads(request.body.decode('utf-8'))
            obj_claim = meClaim.eClaim_Model()
            common.main_fun1(request.read(), path)
            if request.query_params.get("Api_Type") == "WEB":
                obj_claim.jsonData = json.dumps(jsondata.get('Params').get('DETAILS'))
                ld_out_message = obj_claim.eClaim_return_set()
            else:
                common.logger.error([{"return": str(jsondata)}])
                filter = android.Android.post_summary(self, request)
                obj_claim.jsonData = json.dumps(filter)
                ld_out_message = obj_claim.eClaim_return_set()

            if ld_out_message.get("MESSAGE") == 'SUCCESS':
                ld_dict = {"MESSAGE": "SUCCESS", "STATUS": 0}
            elif ld_out_message.get("MESSAGE") == 'FAIL':
                ld_dict = {"MESSAGE": "FAIL", "STATUS": 1}
            else:
                ld_dict = {"MESSAGE": 'ERROR_OCCURED.' + ld_out_message.get("MESSAGE"), "STATUS": 1}
            return Response(ld_dict)
        except Exception as e:
            common.logger.error(e)
            return Response({"MESSAGE": "ERROR_OCCURED", "DATA": str(e),"STATUS":1})
class eClaim_Reject(APIView):
    def post(self,request):
        try:
            path = self.request.stream.path
            jsondata = json.loads(request.body.decode('utf-8'))
            obj_claim = meClaim.eClaim_Model()
            common.main_fun1(request.read(), path)
            if request.query_params.get("Api_Type") == "WEB":
                obj_claim.jsonData = json.dumps(jsondata.get('Params').get('DETAILS'))
                ld_out_message = obj_claim.eClaim_reject_set()
            else:
                common.logger.error([{"reject": str(jsondata)}])
                filter = android.Android.post_summary(self, request)
                obj_claim.jsonData = json.dumps(filter)
                ld_out_message = obj_claim.eClaim_reject_set()

            if ld_out_message.get("MESSAGE") == 'SUCCESS':
                ld_dict = {"MESSAGE": "SUCCESS", "STATUS": 0}
            elif ld_out_message.get("MESSAGE") == 'FAIL':
                ld_dict = {"MESSAGE": "FAIL", "STATUS": 1}
            else:
                ld_dict = {"MESSAGE": 'ERROR_OCCURED.' + ld_out_message.get("MESSAGE"), "STATUS": 1}
            return Response(ld_dict)
        except Exception as e:
            common.logger.error(e)
            return Response({"MESSAGE": "ERROR_OCCURED", "DATA": str(e),"STATUS":1})
class Tour_Forward(APIView):
    def post(self,request):
        try:
            path = self.request.stream.path
            jsondata = json.loads(request.body.decode('utf-8'))
            obj_claim = meClaim.eClaim_Model()
            common.main_fun1(request.read(), path)
            if request.query_params.get("Api_Type") == "WEB":
                obj_claim.jsonData = json.dumps(jsondata.get('Params').get('DETAILS'))
                ld_out_message = obj_claim.eClaim_forward_set()
            else:
                filter = android.Android.post_summary(self, request)
                obj_claim.jsonData = json.dumps(filter)
                ld_out_message = obj_claim.eClaim_forward_set()

            if ld_out_message.get("MESSAGE") == 'SUCCESS':
                ld_dict = {"MESSAGE": "SUCCESS", "STATUS": 0}
            elif ld_out_message.get("MESSAGE") == 'FAIL':
                ld_dict = {"MESSAGE": "FAIL", "STATUS": 1}
            else:
                ld_dict = {"MESSAGE": 'ERROR_OCCURED.' + ld_out_message.get("MESSAGE"), "STATUS": 1}
            return Response(ld_dict)
        except Exception as e:
            common.logger.error(e)
            return Response({"MESSAGE": "ERROR_OCCURED", "DATA": str(e),"STATUS":1})
class Approver_List(APIView):
    def get(self,request):
        try:
            obj_claim = meClaim.eClaim_Model()
            ld_out_message = 0
            if request.query_params.get("Type") == "ONBEHALF":
                employeegid = int(request.query_params.get("Employee_gid"))
            else:
                employeegid = int(request.auth.payload.get('user_id'))
            obj_claim.employee_gid = employeegid
            emp_bnk = obj_claim.eClaim_entity_get()
            bank_data = json.loads(emp_bnk.get("DATA").to_json(orient='records'))
            entity = bank_data[0].get('entity_gid')
            br = request.query_params.get("Branch_Gid")
            apptype = request.query_params.get("App_Type")
            if apptype == 'TOURADV':
                obj_claim.filter_json = json.dumps({"App_Type": apptype, "Entity_Gid": entity, "Branch_Gid": br})
                ld_out_message = obj_claim.eClaim_approverlist_get_galley()
                if ld_out_message.get("MESSAGE") == 'FOUND':
                    data = json.loads(ld_out_message.get("DATA").to_json(orient='records'))
                    common.logger.error([{"Employee_data": str(data)}])
                    ld_dict = {"DATA": data,
                               "MESSAGE": 'FOUND', "STATUS": 0}
                elif ld_out_message.get("MESSAGE") == 'NOT_FOUND':
                    ld_dict = {"MESSAGE": 'NOT_FOUND'}
                else:
                    ld_dict = {"MESSAGE": 'ERROR_OCCURED.' + ld_out_message.get("MESSAGE")}
                return Response(ld_dict)

            if apptype == 'CLAIM':
                obj_claim.filter_json = json.dumps({"App_Type": apptype, "Entity_Gid": entity, "Branch_Gid": br})
                ld_out_message = obj_claim.eClaim_approverlist_get()
                if ld_out_message.get("MESSAGE") == 'FOUND':
                    data = json.loads(ld_out_message.get("DATA").to_json(orient='records'))
                    emp_gid = []
                    tourgid = request.query_params.get("Tour_Gid")
                    obj_claim.employee_gid = tourgid
                    ld_out_emp = obj_claim.eClaim_tourtoemp_get()
                    ld_dict = json.loads(ld_out_emp.get("DATA").to_json(orient='records'))
                    common.logger.error([{"tourtoemp_get": str(ld_dict)}])
                    maker_empgid = int(ld_dict[0].get('empgid'))
                    empgrade = ld_dict[0].get('empgrade')

                    for i in data:
                        if maker_empgid != 0:
                            if i.get('employeegid') not in emp_gid and i.get('employeegid') != employeegid and \
                                    i.get('employeegid') != maker_empgid:
                                emp_gid.append(i.get('employeegid'))
                        else:
                            if i.get('employeegid') not in emp_gid and i.get('employeegid') != employeegid:
                                emp_gid.append(i.get('employeegid'))

                    emp_data = {
                        "empids": emp_gid
                    }
                    obj_claim.filter_json = json.dumps(emp_data)
                    obj_claim.json_classification = json.dumps({})
                    emp_out_message = obj_claim.eClaim_employee_get()
                    if emp_out_message.get("MESSAGE") == 'FOUND':
                        employee_tmp_data = json.loads(emp_out_message.get("DATA").to_json(orient='records'))
                        common.logger.error([{"employee_data": str(employee_tmp_data)}])
                        employee_data = []
                        a = empgrade[1]
                        print(a.isdigit())
                        if a.isdigit():
                            if int(a) > 3:
                                for i in employee_tmp_data:
                                    if int(i.get('employee_grade1')[1]) >= int(a):
                                        if i.get('branch_code') == '1101' or  i.get('branch_code') == '2135':
                                            employee_data.append(i)

                                if len(employee_data) == 0 :
                                    ld_dict = {"MESSAGE": "No Higher grade Approver/Please Choose 1101 Branch because Employee Grade is Higher"}
                                    return Response(ld_dict)
                                else:
                                    ld_dict = {"DATA": employee_data,
                                               "MESSAGE": 'FOUND', "STATUS": 0}
                                    return Response(ld_dict)
                            else:
                                ld_dict = {"DATA": employee_tmp_data,
                                           "MESSAGE": 'FOUND', "STATUS": 0}
                                return Response(ld_dict)
                        else:
                            ld_dict = {"DATA": employee_tmp_data,
                                       "MESSAGE": 'FOUND', "STATUS": 0}
                            return Response(ld_dict)
                    else:
                        ld_dict = {"MESSAGE": "Employee Data Missing" + str(ld_out_message.get("MESSAGE"))}
                        return Response(ld_dict)
                else:
                    ld_dict = {"MESSAGE": "Approver Data Missing" + str(ld_out_message.get("MESSAGE"))}
                    return Response(ld_dict)

            else:
                obj_claim.filter_json = json.dumps({"App_Type": apptype, "Entity_Gid": entity, "Branch_Gid": br})
                ld_out_message = obj_claim.eClaim_approverlist_get()
                if ld_out_message.get("MESSAGE") == 'FOUND':
                    data = json.loads(ld_out_message.get("DATA").to_json(orient='records'))
                    emp_gid = []
                    maker_empgid = 0
                    if "Tour_Gid" in request.query_params:
                        tourgid = request.query_params.get("Tour_Gid")
                        obj_claim.employee_gid = tourgid
                        ld_out_emp = obj_claim.eClaim_tourtoemp_get()
                        ld_dict = json.loads(ld_out_emp.get("DATA").to_json(orient='records'))
                        common.logger.error([{"tourtoemp_get": str(ld_dict)}])
                        maker_empgid = int(ld_dict[0].get('empgid'))
                        empgrade = ld_dict[0].get('empgrade')

                    for i in data:
                        if maker_empgid != 0:
                            if i.get('employeegid') not in emp_gid and i.get('employeegid') != employeegid and \
                                    i.get('employeegid') != maker_empgid:
                                emp_gid.append(i.get('employeegid'))
                        else:
                            if i.get('employeegid') not in emp_gid and i.get('employeegid') != employeegid:
                                emp_gid.append(i.get('employeegid'))

                    emp_data = {
                        "empids": emp_gid
                    }
                    obj_claim.filter_json = json.dumps(emp_data)
                    obj_claim.json_classification = json.dumps({})
                    emp_out_message = obj_claim.eClaim_employee_get()
                    if emp_out_message.get("MESSAGE") == 'FOUND':
                        employee_data = json.loads(emp_out_message.get("DATA").to_json(orient='records'))
                        common.logger.error([{"employee_data": str(employee_data)}])

                    else:
                        ld_dict = {"MESSAGE": "Employee Data Missing" + str(ld_out_message.get("DATA"))}
                        return Response(ld_dict)
                    # emp_data = {
                    #     "empids": employeegid
                    # }
                    # obj_claim.filter_json = json.dumps(emp_data)
                    # obj_claim.json_classification = json.dumps({})
                    # emp_out = obj_claim.eClaim_employee_get()
                    # if emp_out.get("MESSAGE") == 'FOUND':
                    #     login_employee = json.loads(emp_out.get("DATA").to_json(orient='records'))
                    #     common.logger.error([{"login_employee": str(login_employee)}])
                    # else:
                    #     ld_dict = {"MESSAGE": "Login employee" + str(ld_out_message.get("DATA"))}
                    #     return Response(ld_dict)
                    # designation = obj_claim.eClaim_empgrade_get()
                    # designation = json.loads(designation.get("DATA").to_json(orient='records'))

                    #order = 0
                    #for i in login_employee:
                     #   for j in designation:
                      #      if i.get('designation_name').upper() == j.get('designation').upper():
                       #         order = int(j.get('orderno'))
                        #        break
                         #       break
                    #common.logger.error([{"order": str(order)}])

                    #for i in employee_data:
                     #   for j in designation:
                      #      if i.get('designation_name').upper() == j.get('designation').upper():
                       #         i['hierarchy_order'] = j.get('orderno')
                        #        break
                        #else:
                         #   i['hierarchy_order'] = 0

                    #common.logger.error([{"employee_data2": str(employee_data)}])
                    # app_data = []
                    # for d in data:
                    #     for e in employee_data:
                    #         if int(e.get('employee_gid')) == int(d.get('employeegid')):
                    #             common.logger.error([{"hierarchy_order": str(e.get('hierarchy_order'))}])
                    #             common.logger.error([{"order": str(order)}])
                    #             #if e.get('hierarchy_order') != None:
                    #              #   if order > int(e.get('hierarchy_order')):
                    #             app={}
                    #             app["employee_name"] = e.get('employee_name')
                    #             app["employee_code"] = e.get('employee_code')
                    #             app["employee_gid"] = d.get('employeegid')
                    #             app_data.append(app)
                    #
                    #                 break
                    common.logger.error([{"app_data": str(employee_data)}])
                    ld_dict = {"DATA": employee_data,
                               "MESSAGE": 'FOUND',"STATUS":0}
                elif ld_out_message.get("MESSAGE") == 'NOT_FOUND':
                    ld_dict = {"MESSAGE": 'NOT_FOUND'}
                else:
                    ld_dict = {"MESSAGE": 'ERROR_OCCURED.' + ld_out_message.get("MESSAGE")}
                return Response(ld_dict)
        except Exception as e:
            common.logger.error(e)
            er = "Erro Line no :" + str(format(sys.exc_info()[-1].tb_lineno)) + " " + "Error :" + str(e)
            return Response({"MESSAGE": "ERROR_OCCURED", "DATA": er, "STATUS": 1})

class Claim_Summary(APIView):
    def post(self,request):
        try:
            ld_out_message = ""
            path = self.request.stream.path
            if request.query_params.get("Api_Type") =="WEB":
                jsondata = json.loads(request.body.decode('utf-8'))
                obj_eclaim = meClaim.eClaim_Model()
                common.main_fun1(request.read(), path)
                obj_eclaim.filter_json = json.dumps(jsondata.get('Params').get('FILTER'))
                ld_out_message = obj_eclaim.eClaim_expensemaker_get()
            else:
                filter = android.Android.post_summary(self,request)
                obj_eclaim = meClaim.eClaim_Model()
                common.main_fun1(request.read(), path)
                filter['summarytype'] = "CLAIM_MAKER"
                obj_eclaim.filter_json = json.dumps(filter)
                ld_out_message = obj_eclaim.eClaim_expensemaker_get()
            if ld_out_message.get("MESSAGE") == 'FOUND':
                out_data = json.loads(ld_out_message.get("DATA").to_json(orient='records'))
                data = []

                for d in out_data:
                    if 'Total_Row' in d:
                        pass
                    else:
                        d['Total_Row'] = len(out_data)
                    tmp={}
                    tmp['tourgid'] = d.get('gid')
                    tmp['advancegid'] = d.get('advancegid')
                    tmp['requestno'] = d.get('requestno')
                    tmp['requestdate'] = d.get('requestdate')
                    tmp['empgid'] = d.get('empgid')
                    tmp['empgrade'] = d.get('empgrade')
                    tmp['tourreason'] = d.get('name')
                    tmp['startdate'] = d.get('startdate')
                    tmp['enddate'] = d.get('enddate')
                    tmp['claimstatus'] = d.get('claimstatus')
                    tmp['approvedby'] = int(d.get('approvedby'))
                    tmp['applevel'] = d.get('applevel')
                    tmp['Total_Row'] = d.get('Total_Row')

                    data.append(tmp)
                if len(data) != 0:
                    emp_gid = []
                    permit_gid = []
                    for i in data:
                        if i.get('empgid') not in emp_gid and i.get('empgid') != 0:
                            emp_gid.append(i.get('empgid'))
                        if i.get('approvedby') not in permit_gid and i.get('approvedby') != 0:
                            permit_gid.append(i.get('approvedby'))
                    emp_data = {
                        "empids" : emp_gid
                    }
                    obj_eclaim.filter_json = json.dumps(emp_data)
                    obj_eclaim.json_classification = json.dumps({})
                    emp_out_message = obj_eclaim.eClaim_employee_get()
                    employee_data = json.loads(emp_out_message.get("DATA").to_json(orient='records'))
                    if permit_gid !=[]:
                        empprmit_data = {
                            "empids": permit_gid
                        }
                        obj_eclaim.filter_json = json.dumps(empprmit_data)
                        obj_eclaim.json_classification = json.dumps({})
                        permit_out_message = obj_eclaim.eClaim_employee_get()
                        permit_data = json.loads(permit_out_message.get("DATA").to_json(orient='records'))
                    for d in data:
                        d["employee_name"] = employee_data[0].get('employee_name')
                        d["employee_code"] = employee_data[0].get('employee_code')
                    if permit_gid != []:
                        for d in data:
                            for i in range(0, len(permit_data)):
                                if permit_data[i].get('employee_gid') == int(d.get('approvedby')):
                                    d["permit_byname"] = permit_data[i].get('employee_name')
                                    d["permit_bycode"] = permit_data[i].get('employee_code')
                                    break

                    ld_dict = {"DATA": data,"MESSAGE": 'FOUND',"STATUS":0}
                else:
                    ld_dict = {"MESSAGE": 'NOT_FOUND', "STATUS": 1}
            elif ld_out_message.get("MESSAGE") == 'NOT_FOUND':
                ld_dict = {"MESSAGE": 'NOT_FOUND',"STATUS":1}
            else:
                ld_dict = {"MESSAGE": 'ERROR_OCCURED.' + ld_out_message.get("MESSAGE"),"STATUS":1}
            return Response(ld_dict)
        except Exception as e:
            common.logger.error(e)
            return Response({"MESSAGE": "ERROR_OCCURED", "DATA": str(e),"STATUS":1})
class Advance_Summary(APIView):
    def post(self,request):
        try:
            ld_out_message = ""
            path = self.request.stream.path
            if request.query_params.get("Api_Type") =="WEB":
                jsondata = json.loads(request.body.decode('utf-8'))
                common.main_fun1(request.read(), path)
                obj_eclaim = meClaim.eClaim_Model()
                obj_eclaim.filter_json = json.dumps(jsondata.get('Params').get('FILTER'))
                ld_out_message = obj_eclaim.eClaim_advancemaker_get()
            else:
                filter = android.Android.post_summary(self,request)
                common.main_fun1(request.read(), path)
                obj_eclaim = meClaim.eClaim_Model()
                obj_eclaim.filter_json = json.dumps(filter)
                ld_out_message = obj_eclaim.eClaim_advancemaker_get()
            if ld_out_message.get("MESSAGE") == 'FOUND':
                out_data = json.loads(ld_out_message.get("DATA").to_json(orient='records'))
                data = []
                for d in out_data:
                    if 'Total_Row' in d:
                        pass
                    else:
                        d['Total_Row'] = len(out_data)
                    tmp={}
                    tmp['tourgid'] = d.get('gid')
                    tmp['advancegid'] = d.get('advancegid')
                    tmp['requestno'] = d.get('requestno')
                    tmp['requestdate'] = d.get('requestdate')
                    tmp['empgid'] = d.get('empgid')
                    tmp['empgrade'] = d.get('empgrade')
                    tmp['tourreason'] = d.get('name')
                    tmp['startdate'] = d.get('startdate')
                    tmp['enddate'] = d.get('enddate')
                    tmp['advanceamt'] = d.get('advanceamt')
                    tmp['advancestatus'] = d.get('advancestatus')
                    tmp['approvedby'] = d.get('approvedby')
                    tmp['Total_Row'] = d.get('Total_Row')
                    data.append(tmp)
                if len(data) != 0:
                    emp_gid = []
                    permit_gid = []
                    for i in data:
                        if i.get('empgid') not in emp_gid and i.get('empgid') != 0:
                            emp_gid.append(i.get('empgid'))
                        if i.get('approvedby') not in permit_gid and i.get('approvedby') != 0:
                            permit_gid.append(i.get('approvedby'))
                    emp_data = {
                        "empids" : emp_gid
                    }
                    obj_eclaim.filter_json = json.dumps(emp_data)
                    obj_eclaim.json_classification = json.dumps({})
                    emp_out_message = obj_eclaim.eClaim_employee_get()
                    employee_data = json.loads(emp_out_message.get("DATA").to_json(orient='records'))
                    empprmit_data = {
                        "empids": permit_gid
                    }
                    obj_eclaim.filter_json = json.dumps(empprmit_data)
                    obj_eclaim.json_classification = json.dumps({})
                    permit_out_message = obj_eclaim.eClaim_employee_get()
                    permit_data = json.loads(permit_out_message.get("DATA").to_json(orient='records'))
                    for d in data:
                        d["employee_name"] = employee_data[0].get('employee_name')
                        d["employee_code"] = employee_data[0].get('employee_code')
                    for d in data:
                        for i in range(0, len(permit_data)):
                            if permit_data[i].get('employee_gid') == int(d.get('approvedby')):
                                d["permit_byname"] = permit_data[i].get('employee_name')
                                d["permit_bycode"] = permit_data[i].get('employee_code')
                                break

                    ld_dict = {"DATA": data,"MESSAGE": 'FOUND',"STATUS":0}
                else:
                    ld_dict = {"MESSAGE": 'NOT_FOUND', "STATUS": 1}
            elif ld_out_message.get("MESSAGE") == 'NOT_FOUND':
                ld_dict = {"MESSAGE": 'NOT_FOUND',"STATUS":1}
            else:
                ld_dict = {"MESSAGE": 'ERROR_OCCURED.' + ld_out_message.get("MESSAGE"),"STATUS":1}
            return Response(ld_dict)
        except Exception as e:
            common.logger.error(e)
            return Response({"MESSAGE": "ERROR_OCCURED", "DATA": str(e),"STATUS":1})
class Advance_Maker_Summary(APIView):
    def post(self,request):
        try:
            ld_out_message = ""
            path = self.request.stream.path
            if request.query_params.get("Api_Type") =="WEB":
                jsondata = json.loads(request.body.decode('utf-8'))
                common.main_fun1(request.read(), path)
                obj_eclaim = meClaim.eClaim_Model()
                obj_eclaim.date = 'DATE'
                date = obj_eclaim.get_server_date()
                jsondata['Params']['FILTER']['date'] = date
                obj_eclaim.filter_json = json.dumps(jsondata.get('Params').get('FILTER'))
                ld_out_message = obj_eclaim.eClaim_request_get()

            else:
                filter = android.Android.post_summary(self,request)
                common.main_fun1(request.read(), path)
                obj_eclaim = meClaim.eClaim_Model()
                obj_eclaim.date = 'DATE'
                date = obj_eclaim.get_server_date()
                filter['date'] = date
                obj_eclaim.filter_json = json.dumps(filter)
                ld_out_message = obj_eclaim.eClaim_request_get()
            if ld_out_message.get("MESSAGE") == 'FOUND':
                out_data = json.loads(ld_out_message.get("DATA").to_json(orient='records'))
                data = []
                for d in out_data:
                    if d.get('tourstatus') == "APPROVED" and d.get('claimstatus') == "" and d.get('advancegid') ==0 :
                        if 'Total_Row' in d:
                            pass
                        else:
                            d['Total_Row'] = len(out_data)
                        tmp={}
                        tmp['gid'] = d.get('gid')
                        tmp['requestno'] = d.get('requestno')
                        tmp['requestdate'] = d.get('requestdate')
                        tmp['empgid'] = d.get('empgid')
                        tmp['empgrade'] = d.get('empgrade')
                        tmp['tourreason'] = d.get('name')
                        tmp['startdate'] = d.get('startdate')
                        tmp['enddate'] = d.get('enddate')
                        tmp['enddate'] = d.get('enddate')
                        tmp['tourstatus'] = d.get('tourstatus')
                        tmp['approvedby'] = d.get('approvedby')
                        tmp['Total_Row'] = d.get('Total_Row')
                        data.append(tmp)
                if len(data) != 0:
                    emp_gid = []
                    permit_gid = []
                    for i in data:
                        if i.get('empgid') not in emp_gid and i.get('empgid') != 0:
                            emp_gid.append(i.get('empgid'))
                        if i.get('approvedby') not in permit_gid and i.get('approvedby') != 0:
                            permit_gid.append(i.get('approvedby'))
                    emp_data = {
                        "empids" : emp_gid
                    }
                    obj_eclaim.filter_json = json.dumps(emp_data)
                    obj_eclaim.json_classification = json.dumps({})
                    emp_out_message = obj_eclaim.eClaim_employee_get()
                    employee_data = json.loads(emp_out_message.get("DATA").to_json(orient='records'))
                    empprmit_data = {
                        "empids": permit_gid
                    }
                    obj_eclaim.filter_json = json.dumps(empprmit_data)
                    obj_eclaim.json_classification = json.dumps({})
                    permit_out_message = obj_eclaim.eClaim_employee_get()
                    permit_data = json.loads(permit_out_message.get("DATA").to_json(orient='records'))
                    for d in data:
                        d["employee_name"] = employee_data[0].get('employee_name')
                        d["employee_code"] = employee_data[0].get('employee_code')
                    for d in data:
                        for i in range(0, len(permit_data)):
                            if permit_data[i].get('employee_gid') == int(d.get('approvedby')):
                                d["permit_byname"] = permit_data[i].get('employee_name')
                                d["permit_bycode"] = permit_data[i].get('employee_code')
                                break

                    ld_dict = {"DATA": data,"MESSAGE": 'FOUND',"STATUS":0}
                else :
                    ld_dict = {"MESSAGE": 'NOT_FOUND', "STATUS": 1}
            elif ld_out_message.get("MESSAGE") == 'NOT_FOUND':
                ld_dict = {"MESSAGE": 'NOT_FOUND',"STATUS":1}
            else:
                ld_dict = {"MESSAGE": 'ERROR_OCCURED.' + ld_out_message.get("MESSAGE"),"STATUS":1}
            return Response(ld_dict)
        except Exception as e:
            common.logger.error(e)
            return Response({"MESSAGE": "ERROR_OCCURED", "DATA": str(e),"STATUS":1})
class Cancel_Maker_Summary(APIView):
    def post(self,request):
        try:
            ld_out_message = ""
            path = self.request.stream.path
            if request.query_params.get("Api_Type") =="WEB":
                jsondata = json.loads(request.body.decode('utf-8'))
                common.main_fun1(request.read(), path)
                obj_eclaim = meClaim.eClaim_Model()
                tourtype = jsondata.get('Params').get('FILTER').get('tourtype')
                obj_eclaim.filter_json = json.dumps(jsondata.get('Params').get('FILTER'))
                ld_out_message = obj_eclaim.eClaim_tourcancel_get()

            else:
                filter = android.Android.post_summary(self,request)
                common.main_fun1(request.read(), path)
                obj_eclaim = meClaim.eClaim_Model()
                tourtype = filter.get('tourtype')
                obj_eclaim.filter_json = json.dumps(filter)
                ld_out_message = obj_eclaim.eClaim_tourcancel_get()
            if ld_out_message.get("MESSAGE") == 'FOUND':
                out_data = json.loads(ld_out_message.get("DATA").to_json(orient='records'))
                data = []
                for d in out_data:
                    if d.get('type') == tourtype:
                        tmp={}
                        tmp['gid'] = d.get('gid')
                        tmp['tourgid'] = d.get('tourgid')
                        tmp['requestno'] = d.get('requestno')
                        tmp['requestdate'] = d.get('requestdate')
                        tmp['empgid'] = d.get('empgid')
                        tmp['empgrade'] = d.get('empgrade')
                        tmp['tourreason'] = d.get('name')
                        tmp['startdate'] = d.get('startdate')
                        tmp['enddate'] = d.get('enddate')
                        tmp['enddate'] = d.get('enddate')
                        tmp['tourstatus'] = d.get('tourstatus')
                        tmp['approvedby'] = d.get('approvedby')
                        data.append(tmp)
                if len(data) != 0:
                    emp_gid = []
                    permit_gid = []
                    for i in data:
                        if i.get('empgid') not in emp_gid and i.get('empgid') != 0:
                            emp_gid.append(i.get('empgid'))
                        if i.get('approvedby') not in permit_gid and i.get('approvedby') != 0:
                            permit_gid.append(i.get('approvedby'))
                    emp_data = {
                        "empids" : emp_gid
                    }
                    obj_eclaim.filter_json = json.dumps(emp_data)
                    obj_eclaim.json_classification = json.dumps({})
                    emp_out_message = obj_eclaim.eClaim_employee_get()
                    employee_data = json.loads(emp_out_message.get("DATA").to_json(orient='records'))
                    empprmit_data = {
                        "empids": permit_gid
                    }
                    obj_eclaim.filter_json = json.dumps(empprmit_data)
                    obj_eclaim.json_classification = json.dumps({})
                    permit_out_message = obj_eclaim.eClaim_employee_get()
                    permit_data = json.loads(permit_out_message.get("DATA").to_json(orient='records'))
                    for d in data:
                        d["employee_name"] = employee_data[0].get('employee_name')
                        d["employee_code"] = employee_data[0].get('employee_code')
                    for d in data:
                        for i in range(0, len(permit_data)):
                            if permit_data[i].get('employee_gid') == int(d.get('approvedby')):
                                d["permit_byname"] = permit_data[i].get('employee_name')
                                d["permit_bycode"] = permit_data[i].get('employee_code')
                                break

                    ld_dict = {"DATA": data,"MESSAGE": 'FOUND',"STATUS":0}
                else :
                    ld_dict = {"MESSAGE": 'NOT_FOUND', "STATUS": 1}
            elif ld_out_message.get("MESSAGE") == 'NOT_FOUND':
                ld_dict = {"MESSAGE": 'NOT_FOUND',"STATUS":1}
            else:
                ld_dict = {"MESSAGE": 'ERROR_OCCURED.' + ld_out_message.get("MESSAGE"),"STATUS":1}
            return Response(ld_dict)
        except Exception as e:
            common.logger.error(e)
            return Response({"MESSAGE": "ERROR_OCCURED", "DATA": str(e),"STATUS":1})
class Tour_Cancel_List(APIView):
    def post(self,request):
        try:
            ld_out_message = ""
            path = self.request.stream.path
            if request.query_params.get("Api_Type") =="WEB":
                jsondata = json.loads(request.body.decode('utf-8'))
                common.main_fun1(request.read(), path)
                obj_eclaim = meClaim.eClaim_Model()
                obj_eclaim.filter_json = json.dumps(jsondata.get('Params').get('FILTER'))
                ld_out_message = obj_eclaim.eClaim_tourcancelmaker_get()

            else:
                filter = android.Android.post_summary(self,request)
                common.main_fun1(request.read(), path)
                obj_eclaim = meClaim.eClaim_Model()
                obj_eclaim.filter_json = json.dumps(filter)
                ld_out_message = obj_eclaim.eClaim_tourcancelmaker_get()
            if ld_out_message.get("MESSAGE") == 'FOUND':
                out_data = json.loads(ld_out_message.get("DATA").to_json(orient='records'))
                data = []
                for d in out_data:
                    tmp = {}
                    tmp['gid'] = d.get('gid')
                    tmp['requestno'] = d.get('requestno')
                    tmp['requestdate'] = d.get('requestdate')
                    tmp['empgid'] = d.get('empgid')
                    tmp['empgrade'] = d.get('empgrade')
                    tmp['tourreason'] = d.get('name')
                    tmp['startdate'] = d.get('startdate')
                    tmp['enddate'] = d.get('enddate')
                    tmp['enddate'] = d.get('enddate')
                    tmp['approvedby'] = d.get('approvedby')
                    data.append(tmp)
                if len(data) != 0:
                    emp_gid = []
                    permit_gid = []
                    for i in data:
                        if i.get('empgid') not in emp_gid and i.get('empgid') != 0:
                            emp_gid.append(i.get('empgid'))
                        if i.get('approvedby') not in permit_gid and i.get('approvedby') != 0:
                            permit_gid.append(i.get('approvedby'))
                    emp_data = {
                        "empids" : emp_gid
                    }
                    obj_eclaim.filter_json = json.dumps(emp_data)
                    obj_eclaim.json_classification = json.dumps({})
                    emp_out_message = obj_eclaim.eClaim_employee_get()
                    employee_data = json.loads(emp_out_message.get("DATA").to_json(orient='records'))
                    empprmit_data = {
                        "empids": permit_gid
                    }
                    obj_eclaim.filter_json = json.dumps(empprmit_data)
                    obj_eclaim.json_classification = json.dumps({})
                    permit_out_message = obj_eclaim.eClaim_employee_get()
                    permit_data = json.loads(permit_out_message.get("DATA").to_json(orient='records'))
                    for d in data:
                        d["employee_name"] = employee_data[0].get('employee_name')
                        d["employee_code"] = employee_data[0].get('employee_code')
                    for d in data:
                        for i in range(0, len(permit_data)):
                            if permit_data[i].get('employee_gid') == int(d.get('approvedby')):
                                d["permit_byname"] = permit_data[i].get('employee_name')
                                d["permit_bycode"] = permit_data[i].get('employee_code')
                                break

                    ld_dict = {"DATA": data,"MESSAGE": 'FOUND',"STATUS":0}
                else :
                    ld_dict = {"MESSAGE": 'NOT_FOUND', "STATUS": 1}
            elif ld_out_message.get("MESSAGE") == 'NOT_FOUND':
                ld_dict = {"MESSAGE": 'NOT_FOUND',"STATUS":1}
            else:
                ld_dict = {"MESSAGE": 'ERROR_OCCURED.' + ld_out_message.get("MESSAGE"),"STATUS":1}
            return Response(ld_dict)
        except Exception as e:
            common.logger.error(e)
            return Response({"MESSAGE": "ERROR_OCCURED", "DATA": str(e),"STATUS":1})

class Advance_Cancel_List(APIView):
    def post(self,request):
        try:
            ld_out_message = ""
            path = self.request.stream.path
            if request.query_params.get("Api_Type") =="WEB":
                jsondata = json.loads(request.body.decode('utf-8'))
                common.main_fun1(request.read(), path)
                obj_eclaim = meClaim.eClaim_Model()
                obj_eclaim.filter_json = json.dumps(jsondata.get('Params').get('FILTER'))
                ld_out_message = obj_eclaim.eClaim_advancecancelmaker_get()

            else:
                filter = android.Android.post_summary(self,request)
                common.main_fun1(request.read(), path)
                obj_eclaim = meClaim.eClaim_Model()
                obj_eclaim.filter_json = json.dumps(filter)
                ld_out_message = obj_eclaim.eClaim_advancecancelmaker_get()
            if ld_out_message.get("MESSAGE") == 'FOUND':
                out_data = json.loads(ld_out_message.get("DATA").to_json(orient='records'))
                data = []
                for d in out_data:
                    tmp={}
                    tmp['gid'] = d.get('gid')
                    tmp['requestno'] = d.get('requestno')
                    tmp['requestdate'] = d.get('requestdate')
                    tmp['empgid'] = d.get('empgid')
                    tmp['empgrade'] = d.get('empgrade')
                    tmp['tourreason'] = d.get('name')
                    tmp['startdate'] = d.get('startdate')
                    tmp['enddate'] = d.get('enddate')
                    tmp['enddate'] = d.get('enddate')
                    tmp['tourstatus'] = d.get('advancestatus')
                    tmp['approvedby'] = d.get('approvedby')
                    data.append(tmp)
                if len(data) != 0:
                    emp_gid = []
                    permit_gid = []
                    for i in data:
                        if i.get('empgid') not in emp_gid and i.get('empgid') != 0:
                            emp_gid.append(i.get('empgid'))
                        if i.get('approvedby') not in permit_gid and i.get('approvedby') != 0:
                            permit_gid.append(i.get('approvedby'))
                    emp_data = {
                        "empids" : emp_gid
                    }
                    obj_eclaim.filter_json = json.dumps(emp_data)
                    obj_eclaim.json_classification = json.dumps({})
                    emp_out_message = obj_eclaim.eClaim_employee_get()
                    employee_data = json.loads(emp_out_message.get("DATA").to_json(orient='records'))
                    empprmit_data = {
                        "empids": permit_gid
                    }
                    obj_eclaim.filter_json = json.dumps(empprmit_data)
                    obj_eclaim.json_classification = json.dumps({})
                    permit_out_message = obj_eclaim.eClaim_employee_get()
                    permit_data = json.loads(permit_out_message.get("DATA").to_json(orient='records'))
                    for d in data:
                        d["employee_name"] = employee_data[0].get('employee_name')
                        d["employee_code"] = employee_data[0].get('employee_code')
                    for d in data:
                        for i in range(0, len(permit_data)):
                            if permit_data[i].get('employee_gid') == int(d.get('approvedby')):
                                d["permit_byname"] = permit_data[i].get('employee_name')
                                d["permit_bycode"] = permit_data[i].get('employee_code')
                                break

                    ld_dict = {"DATA": data,"MESSAGE": 'FOUND',"STATUS":0}
                else :
                    ld_dict = {"MESSAGE": 'NOT_FOUND', "STATUS": 1}
            elif ld_out_message.get("MESSAGE") == 'NOT_FOUND':
                ld_dict = {"MESSAGE": 'NOT_FOUND',"STATUS":1}
            else:
                ld_dict = {"MESSAGE": 'ERROR_OCCURED.' + ld_out_message.get("MESSAGE"),"STATUS":1}
            return Response(ld_dict)
        except Exception as e:
            common.logger.error(e)
            return Response({"MESSAGE": "ERROR_OCCURED", "DATA": str(e),"STATUS":1})
class Tour_Advance_Get(APIView):
    def get(self,request):
        try:
            obj_claim = meClaim.eClaim_Model()
            if request.query_params.get("Api_Type") =="WEB":
                entity = request.query_params.get("Entity_Gid")
                Tour_gid = request.query_params.get("Tour_gid")
                obj_claim.filter_json = json.dumps({"Entity_Gid": entity, "Tour_gid": Tour_gid })
                ld_out_message = obj_claim.eClaim_touradvance_get()
                out_datas = json.loads(ld_out_message.get("DATA").to_json(orient='records'))
                tourreason = out_datas[0].get('tourreason')
                out_data = out_datas[0].get('advance')

                enddate = out_datas[0].get('enddate')

                out_data = json.loads(out_data)
                emp_data = {
                    "empids": out_data[0].get('approvedby')
                }
                obj_claim.filter_json = json.dumps(emp_data)
                obj_claim.json_classification = json.dumps({})
                emp_out_message = obj_claim.eClaim_employee_get()
                employee_data = json.loads(emp_out_message.get("DATA").to_json(orient='records'))
                for d in out_data:
                    for i in range(0, len(employee_data)):
                        if employee_data[i].get('employee_gid') == d.get('approvedby'):
                            d["approval_empname"] = employee_data[i].get('employee_name')
                            d["approval_empcode"] = employee_data[i].get('employee_code')
                            d["approval_branch"] = employee_data[i].get('branch_name')
                            d["tourreason"] = tourreason
                ld_dict = {"DATA": out_data, "MESSAGE": 'FOUND'}
            else:
                filter = android.Android.get_method(self, request)
                obj_claim.filter_json = json.dumps(filter)
                ld_out_message = obj_claim.eClaim_touradvance_get()
                out_datas = json.loads(ld_out_message.get("DATA").to_json(orient='records'))
                out_data = json.loads(out_datas[0].get('advance'))
                enddate = out_datas[0].get('enddate')
                obj_claim.date = 'DATE'
                date = obj_claim.get_server_date()

                datetimeFormat = '%d-%b-%Y'
                enddate1 = datetime.datetime.strptime(enddate, datetimeFormat).strftime('%Y-%m-%d')

                if date > enddate1:
                    out_datas[0]["istour_end"] = "True"
                else :
                    out_datas[0]["istour_end"] = "False"

                emp_data = {
                    "empids": out_data[0].get('approvedby')
                }
                obj_claim.filter_json = json.dumps(emp_data)
                obj_claim.json_classification = json.dumps({})
                emp_out_message = obj_claim.eClaim_employee_get()
                employee_data = json.loads(emp_out_message.get("DATA").to_json(orient='records'))
                for d in out_data:
                    for i in range(0, len(employee_data)):
                        if employee_data[i].get('employee_gid') == d.get('approvedby'):
                            d["approval_empname"] = employee_data[i].get('employee_name')
                            d["approval_empcode"] = employee_data[i].get('employee_code')
                            d["approval_branch"] = employee_data[i].get('branch_name')

                out_datas[0]["advance"] = out_data
                ld_dict = {"DATA": out_datas[0], "MESSAGE": 'FOUND'}

            if ld_dict.get("MESSAGE") == 'FOUND':
                ld_dict = {"DATA": ld_dict.get("DATA"),
                           "MESSAGE": 'FOUND',"STATUS":0}
            elif ld_dict.get("MESSAGE") == 'NOT_FOUND':
                ld_dict = {"MESSAGE": 'NOT_FOUND',"STATUS":1}
            else:
                ld_dict = {"MESSAGE": 'ERROR_OCCURED.' + ld_out_message.get("MESSAGE"),"STATUS":1}
            return Response(ld_dict)
        except Exception as e:
            common.logger.error(e)
            return Response({"MESSAGE": "ERROR_OCCURED", "DATA": str(e),"STATUS":1})
class Tour_Advance_Set(APIView):
    def post(self,request):
        try:
            ld_out_message = ""
            path = self.request.stream.path
            jsondata = json.loads(request.body.decode('utf-8'))
            obj_claim = meClaim.eClaim_Model()
            if request.query_params.get("Api_Type") == "WEB":
                obj_claim.jsondata = json.dumps(jsondata.get('Params').get('DETAILS'))
                common.main_fun1(request.read(), path)
                ld_out_message = obj_claim.eClaim_touradvance_set()
            else:
                obj_claim.employee_gid = request.auth.payload.get('user_id')
                emp_bnk = obj_claim.eClaim_entity_get()
                bank_data = json.loads(emp_bnk.get("DATA").to_json(orient='records'))
                entity_gid = bank_data[0].get('entity_gid')
                CHANGE = android.Android.set_data_chng(self, request)
                CHANGE = android.Android.gid_array_check(self, CHANGE)
                common.main_fun1(request.read(), path)
                CHANGE['processedby'] = request.auth.payload.get('user_id')
                CHANGE['createby'] = request.auth.payload.get('user_id')
                CHANGE['Entity_Gid'] = entity_gid
                obj_claim.jsondata = json.dumps(CHANGE)
                ld_out_message = obj_claim.eClaim_touradvance_set()

            if ld_out_message.get("MESSAGE") == 'SUCCESS':
                ld_dict = {"MESSAGE": "SUCCESS", "STATUS": 0}
            elif ld_out_message.get("MESSAGE") == 'FAIL':
                ld_dict = {"MESSAGE": "FAIL", "STATUS": 1}
            else:
                ld_dict = {"MESSAGE": 'ERROR_OCCURED.' + ld_out_message.get("MESSAGE"), "STATUS": 1}
            return Response(ld_dict)
        except Exception as e:
            common.logger.error(e)
            return Response({"MESSAGE": "ERROR_OCCURED", "DATA": str(e),"STATUS":1})

class Advance_Approveamount_Set(APIView):
    def post(self,request):
        try:
            ld_out_message = ""
            path = self.request.stream.path
            jsondata = json.loads(request.body.decode('utf-8'))
            obj_claim = meClaim.eClaim_Model()
            if request.query_params.get("Api_Type") == "WEB":
                obj_claim.jsondata = json.dumps(jsondata.get('Params').get('DETAILS'))
                common.main_fun1(request.read(), path)
                ld_out_message = obj_claim.eClaim_advance_approvedamount_set()
            else:
                obj_claim.employee_gid = request.auth.payload.get('user_id')
                emp_bnk = obj_claim.eClaim_entity_get()
                bank_data = json.loads(emp_bnk.get("DATA").to_json(orient='records'))
                entity_gid = bank_data[0].get('entity_gid')
                jsondata = json.loads(request.body.decode('utf-8'))
                common.main_fun1(request.read(), path)
                jsondata['processedby'] = request.auth.payload.get('user_id')
                jsondata['createby'] = request.auth.payload.get('user_id')
                jsondata['Entity_Gid'] = entity_gid
                obj_claim.jsondata = json.dumps(jsondata)
                ld_out_message = obj_claim.eClaim_advance_approvedamount_set()

            if ld_out_message.get("MESSAGE") == 'SUCCESS':
                ld_dict = {"MESSAGE": "SUCCESS", "STATUS": 0}
            elif ld_out_message.get("MESSAGE") == 'FAIL':
                ld_dict = {"MESSAGE": "FAIL", "STATUS": 1}
            else:
                ld_dict = {"MESSAGE": 'ERROR_OCCURED.' + ld_out_message.get("MESSAGE"), "STATUS": 1}
            return Response(ld_dict)
        except Exception as e:
            common.logger.error(e)
            return Response({"MESSAGE": "ERROR_OCCURED", "DATA": str(e),"STATUS":1})

class Tour_Cancel_Set(APIView):
    def post(self,request):
        try:
            ld_out_message = ""
            path = self.request.stream.path
            jsondata = json.loads(request.body.decode('utf-8'))
            obj_claim = meClaim.eClaim_Model()
            if request.query_params.get("Api_Type") == "WEB":
                obj_claim.jsondata = json.dumps(jsondata.get('Params').get('DETAILS'))
                common.main_fun1(request.read(), path)
                ld_out_message = obj_claim.eClaim_tourcancel_set()
            else:
                obj_claim.employee_gid = request.auth.payload.get('user_id')
                emp_bnk = obj_claim.eClaim_entity_get()
                bank_data = json.loads(emp_bnk.get("DATA").to_json(orient='records'))
                entity_gid = bank_data[0].get('entity_gid')
                CHANGE = android.Android.set_data_chng(self, request)
                CHANGE = android.Android.gid_array_check(self, CHANGE)
                common.main_fun1(request.read(), path)
                CHANGE['processedby'] = request.auth.payload.get('user_id')
                CHANGE['createby'] = request.auth.payload.get('user_id')
                CHANGE['Entity_Gid'] = entity_gid
                obj_claim.jsondata = json.dumps(CHANGE)
                ld_out_message = obj_claim.eClaim_tourcancel_set()

            if ld_out_message.get("MESSAGE") == 'SUCCESS':
                ld_dict = {"MESSAGE": "SUCCESS", "STATUS": 0}
            elif ld_out_message.get("MESSAGE") == 'FAIL':
                ld_dict = {"MESSAGE": "FAIL", "STATUS": 1}
            else:
                ld_dict = {"MESSAGE": 'ERROR_OCCURED.' + ld_out_message.get("MESSAGE"), "STATUS": 1}
            return Response(ld_dict)
        except Exception as e:
            common.logger.error(e)
            return Response({"MESSAGE": "ERROR_OCCURED", "DATA": str(e),"STATUS":1})
class Claimed_expense(APIView):
    def get(self, request):
        try:
            obj_eclaim = meClaim.eClaim_Model()
            if request.query_params.get("Api_Type") =="WEB":
                entity = request.query_params.get("Entity_Gid")
                Claimrequest_Tourgid = request.query_params.get("Claimrequest_Tourgid")
                obj_eclaim.filter_json = json.dumps({"Entity_Gid": entity, "Claimrequest_Tourgid": Claimrequest_Tourgid })
                ld_out_message = obj_eclaim.eClaim_claimedexpense_get()
            else:
                filter = android.Android.get_method(self, request)
                obj_eclaim.filter_json = json.dumps(filter)
                ld_out_message = obj_eclaim.eClaim_claimedexpense_get()
            if ld_out_message.get("MESSAGE") == 'FOUND':

                obj_eclaim.filter_json = json.dumps({"Tour_gid": request.query_params.get("Claimrequest_Tourgid")})
                ld_out_file = obj_eclaim.eClaim_file_get()
                out_data = json.loads(ld_out_message.get("DATA").to_json(orient='records'))
                enddate = out_data[0].get('enddate')
                startdate = out_data[0].get('startdate')
                obj_eclaim.date = 'DATE'
                date = obj_eclaim.get_server_date()

                datetimeFormat = '%d-%b-%Y'
                enddate1 = datetime.datetime.strptime(enddate, datetimeFormat).strftime('%Y-%m-%d')

                datetimeFormat = '%d-%b-%Y'
                startdate1 = datetime.datetime.strptime(startdate, datetimeFormat).strftime('%Y-%m-%d')

                if date > enddate1:
                    istour_end = "True"
                else:
                    istour_end = "False"

                if date > startdate1:
                    istour_start = "True"
                else:
                    istour_start = "False"
                emp_data = {
                    "empids": out_data[0].get('empgid')
                }
                obj_eclaim.filter_json = json.dumps(emp_data)
                obj_eclaim.json_classification = json.dumps({})
                emp_out_message = obj_eclaim.eClaim_employee_get()
                employee1_data = json.loads(emp_out_message.get("DATA").to_json(orient='records'))
                for d in out_data:
                    d["employee_name"] = employee1_data[0].get('employee_name')
                    d["employee_code"] = employee1_data[0].get('employee_code')
                    d["employee_designation"] = employee1_data[0].get('designation_name')
                    d["employee_branch"] = employee1_data[0].get('branch_name')
                    d["istour_end"] = istour_end
                    d["istour_start"] = istour_start
                if out_data[0].get('approvedby') != 0:
                    emp_data = {
                        "empids": out_data[0].get('approvedby')
                    }
                    obj_eclaim.filter_json = json.dumps(emp_data)
                    obj_eclaim.json_classification = json.dumps({})
                    emp_out_message = obj_eclaim.eClaim_employee_get()
                    employee1_data = json.loads(emp_out_message.get("DATA").to_json(orient='records'))
                    for d in out_data:
                        d["forwarder_name"] = employee1_data[0].get('employee_name')
                        d["forwarder_code"] = employee1_data[0].get('employee_code')
                        d["forwarder_branch"] = employee1_data[0].get('branch_name')
                if out_data[0].get('approvedby_fr') != 0:
                    emp_data = {
                        "empids": out_data[0].get('approvedby_fr')
                    }
                    obj_eclaim.filter_json = json.dumps(emp_data)
                    obj_eclaim.json_classification = json.dumps({})
                    emp_out_message = obj_eclaim.eClaim_employee_get()
                    employee_data = json.loads(emp_out_message.get("DATA").to_json(orient='records'))
                    if employee_data != []:
                        for d in out_data:
                            d["approver_name"] = employee_data[0].get('employee_name')
                            d["approver_code"] = employee_data[0].get('employee_code')
                            d["approver_branch"] = employee_data[0].get('branch_name')

                file = json.loads(ld_out_file.get("DATA").to_json(orient='records'))
                filedata = []
                for i in file:
                    s3_client = boto3.client('s3','ap-south-1')
                    response = s3_client.generate_presigned_url('get_object',
                                                                Params={'Bucket': S3_BUCKET_NAME,
                                                                        'Key': i.get('file_path')},
                                                                ExpiresIn=None)
                    data = {
                        "file_gid": i.get('file_gid'),
                        "file_name": i.get('file_name'),
                        "file_key": i.get('file_path'),
                        "file_path": response,
                        "file_refgid": i.get('file_refgid')
                    }
                    filedata.append(data)



                ld_dict = {
                    "DATA": out_data,
                    "FILE": filedata,
                    "MESSAGE": 'FOUND',"STATUS": 0}
            elif ld_out_message.get("MESSAGE") == 'NOT_FOUND':
                ld_dict = {"MESSAGE": 'NOT_FOUND',"STATUS": 1}
            else:
                ld_dict = {"MESSAGE": 'ERROR_OCCURED.' + ld_out_message.get("MESSAGE"),"STATUS": 1}
            return Response(ld_dict)
        except Exception as e:
            common.logger.error(e)
            return Response({"MESSAGE": "ERROR_OCCURED", "DATA": str(e), "STATUS": 1})
class Expense_Get(APIView):
    def get(self, request):
        try:
            obj_eclaim = meClaim.eClaim_Model()
            ld_out_message = obj_eclaim.eClaim_expense_get()
            if json.loads(ld_out_message.get("DATA").to_json(orient='records')):
                ld_dict = {"DATA": json.loads(ld_out_message.get("DATA").to_json(orient='records')),
                           "MESSAGE": 'FOUND',"STATUS": 0}
            elif ld_out_message.get("MESSAGE") == 'NOT_FOUND':
                ld_dict = {"MESSAGE": 'NOT_FOUND',"STATUS": 1}
            else:
                ld_dict = {"MESSAGE": 'ERROR_OCCURED.' + ld_out_message.get("MESSAGE"),"STATUS": 1}
            return Response(ld_dict)
        except Exception as e:
            common.logger.error(e)
            return Response({"MESSAGE": "ERROR_OCCURED", "DATA": str(e), "STATUS": 1})
class Onbehalfof_get(APIView):
    def get(self, request):
        try:
            obj_eclaim = meClaim.eClaim_Model()
            employee = request.auth.payload.get('user_id')
            obj_eclaim.filter_json = json.dumps({"employeegid":employee })
            ld_out_message = obj_eclaim.eClaim_onbehalf_get()
            if ld_out_message.get("MESSAGE") == 'FOUND':
                data = json.loads(ld_out_message.get("DATA").to_json(orient='records'))
                emp_gid = []
                onbehalf_gid = []
                for i in data:
                    if i.get('employeegid') not in emp_gid and i.get('employeegid') != 0:
                        emp_gid.append(i.get('employeegid'))
                    if i.get('onbehalf_employeegid') not in onbehalf_gid and i.get('onbehalf_employeegid') != 0:
                        onbehalf_gid.append(i.get('onbehalf_employeegid'))

                emp_data = {
                    "empids": emp_gid
                }
                obj_eclaim.filter_json = json.dumps(emp_data)
                obj_eclaim.json_classification = '{}'
                emp_out_message = obj_eclaim.eClaim_employee_get()
                employee_data = json.loads(emp_out_message.get("DATA").to_json(orient='records'))
                for d in data:
                    for i in employee_data:
                        if i.get('employee_gid') == d.get('employeegid'):
                            d["employee_name"] = i.get('employee_name')
                            d["employee_code"] = i.get('employee_code')
                            break

                emp_data = {
                    "empids": onbehalf_gid
                }
                obj_eclaim.filter_json = json.dumps(emp_data)
                obj_eclaim.json_classification = '{}'
                emp_out_message = obj_eclaim.eClaim_employee_get()
                employee_data = json.loads(emp_out_message.get("DATA").to_json(orient='records'))
                for d in data:
                    for i in employee_data:
                        if i.get('employee_gid') == d.get('onbehalf_employeegid'):
                            d["onbehalf_employeename"] = i.get('employee_name')
                            d["onbehalf_employeecode"] = i.get('employee_code')
                            d["onbehalf_branch_name"] = i.get('branch_name')
                            break

                ld_dict = {"DATA": data,"MESSAGE": 'FOUND',"STATUS": 0}
            elif ld_out_message.get("MESSAGE") == 'NOT_FOUND':
                ld_dict = {"MESSAGE": 'NOT_FOUND',"STATUS": 1}
            else:
                ld_dict = {"MESSAGE": 'ERROR_OCCURED.' + ld_out_message.get("MESSAGE"),"STATUS": 1}
            return Response(ld_dict)
        except Exception as e:
            common.logger.error(e)
            return Response({"MESSAGE": "ERROR_OCCURED", "DATA": str(e), "STATUS": 1})
class Onbehalfof_Employee_get(APIView):
    def get(self, request):
        try:
            obj_eclaim = meClaim.eClaim_Model()
            employee = request.auth.payload.get('user_id')
            obj_eclaim.filter_json = json.dumps({"employeegid":employee,"type":"CHECK"})
            ld_out_message = obj_eclaim.eClaim_onbehalf_get()
            if ld_out_message.get("MESSAGE") == 'FOUND':
                data = json.loads(ld_out_message.get("DATA").to_json(orient='records'))
                if data !=[]:
                    ld_dict = {"DATA":"ONBEHALF", "MESSAGE":'FOUND',"STATUS": 0}
                else:
                    ld_dict = {"DATA":"NOT_ONBEHALF","MESSAGE":'FOUND',"STATUS": 0}
            elif ld_out_message.get("MESSAGE") == 'NOT_FOUND':
                ld_dict = {"DATA":"NOT_ONBEHALF","MESSAGE": 'NOT_FOUND',"STATUS": 1}
            else:
                ld_dict = {"MESSAGE": 'ERROR_OCCURED.' + ld_out_message.get("MESSAGE"),"STATUS": 1}
            return Response(ld_dict)
        except Exception as e:
            common.logger.error(e)
            return Response({"MESSAGE": "ERROR_OCCURED", "DATA": str(e), "STATUS": 1})
class Onbehalfof_dropdown_get(APIView):
    def get(self, request):
        try:
            obj_eclaim = meClaim.eClaim_Model()
            employee = request.auth.payload.get('user_id')
            br = request.query_params.get("Branch_Gid")
            obj_eclaim.filter_json = json.dumps({"employeegid": employee,"type":"DROPDOWN","branchgid":br})
            ld_out_message = obj_eclaim.eClaim_onbehalf_get()
            if ld_out_message.get("MESSAGE") == 'FOUND':
                data = json.loads(ld_out_message.get("DATA").to_json(orient='records'))
                emp_gid = []
                for i in data:
                    if i.get('employee_gid') not in emp_gid and i.get('employee_gid') != 0:
                        emp_gid.append(i.get('employee_gid'))

                emp_data = {
                    "empids": emp_gid
                }
                obj_eclaim.filter_json = json.dumps(emp_data)
                obj_eclaim.json_classification = '{}'
                emp_out_message = obj_eclaim.eClaim_employee_get()
                employee_data = json.loads(emp_out_message.get("DATA").to_json(orient='records'))
                for d in data:
                    for i in employee_data:
                        if i.get('employee_gid') == d.get('employee_gid'):
                            d["employee_name"] = i.get('employee_name')
                            d["employee_code"] = i.get('employee_code')
                            break

                ld_dict = {"DATA": data, "MESSAGE": 'FOUND',"STATUS": 0}
            elif ld_out_message.get("MESSAGE") == 'NOT_FOUND':
                ld_dict = {"MESSAGE": 'NOT_FOUND',"STATUS": 1}
            else:
                ld_dict = {"MESSAGE": 'ERROR_OCCURED.' + ld_out_message.get("MESSAGE"),"STATUS": 1}
            return Response(ld_dict)
        except Exception as e:
            common.logger.error(e)
            return Response({"MESSAGE": "ERROR_OCCURED", "DATA": str(e), "STATUS": 1})
class TourApprover_get(APIView):
    def get(self, request):
        try:
            obj_eclaim = meClaim.eClaim_Model()
            ld_out_message = obj_eclaim.eClaim_tourapprover_get()
            data = json.loads(ld_out_message.get("DATA").to_json(orient='records'))
            if data!= [] :
                emp_gid = []
                for i in data:
                    if i.get('employeegid') not in emp_gid and i.get('employeegid') != 0:
                        emp_gid.append(i.get('employeegid'))
                emp_data = {
                    "empids": emp_gid
                }
                obj_eclaim.filter_json = json.dumps(emp_data)
                obj_eclaim.json_classification = '{}'
                emp_out_message = obj_eclaim.eClaim_employee_get()
                employee_data = json.loads(emp_out_message.get("DATA").to_json(orient='records'))
                if emp_out_message.get("MESSAGE") == 'FOUND':
                    for d in data:
                        for i in employee_data:
                            if i.get('employee_gid') == d.get('employeegid'):
                                d["employee_name"] = i.get('employee_name')
                                d["employee_code"] = i.get('employee_code')
                                break

                    ld_dict = {"DATA": data, "MESSAGE": 'FOUND'}
                else:
                    ld_dict = {"MESSAGE": 'NOT_FOUND.' + ld_out_message.get("MESSAGE")}
            elif ld_out_message.get("MESSAGE") == 'NOT_FOUND':
                ld_dict = {"MESSAGE": 'NOT_FOUND'}
            else:
                ld_dict = {"MESSAGE": 'ERROR_OCCURED.' + ld_out_message.get("MESSAGE")}
            return Response(ld_dict)
        except Exception as e:
            common.logger.error(e)
            er = "Erro Line no :" + str(format(sys.exc_info()[-1].tb_lineno)) + " " + "Error :" + str(e)
            return Response({"MESSAGE": "ERROR_OCCURED", "DATA": er, "STATUS": 1})
class Onbehalfof_set(APIView):
    def post(self,request):
        try:
            path = self.request.stream.path
            jsondata = json.loads(request.body.decode('utf-8'))
            obj_claim = meClaim.eClaim_Model()
            if request.query_params.get("Api_Type") == "WEB":
                obj_claim.jsondata = json.dumps(jsondata.get('Params').get('DETAILS'))
                common.main_fun1(request.read(), path)
                ld_out_message = obj_claim.eClaim_onbehalf_set()
                if ld_out_message.get("MESSAGE") == 'SUCCESS':
                    ld_dict = {"MESSAGE": "SUCCESS"}
                elif ld_out_message.get("MESSAGE") == 'FAIL':
                    ld_dict = {"MESSAGE": "FAIL"}
                else:
                    ld_dict = {"MESSAGE": 'ERROR_OCCURED.' + ld_out_message.get("MESSAGE")}
                return Response(ld_dict)
            else:
                DETAILS = android.Android.set_data_dtl(self, request)
                common.main_fun1(request.read(), path)
                obj_claim.jsonData = json.dumps(DETAILS)
                ld_out_message = obj_claim.eClaim_onbehalf_set()
                if ld_out_message.get("MESSAGE") == 'SUCCESS':
                    ld_dict = {"MESSAGE": "SUCCESS"}
                elif ld_out_message.get("MESSAGE") == 'FAIL':
                    ld_dict = {"MESSAGE": "FAIL"}
                else:
                    ld_dict = {"MESSAGE": 'ERROR_OCCURED.' + ld_out_message.get("MESSAGE")}
                return Response(ld_dict)
        except Exception as e:
            common.logger.error(e)
            return Response({"MESSAGE": "ERROR_OCCURED", "DATA": str(e),"STATUS":1})
class Approver_set(APIView):
    def post(self,request):
        try:
            path = self.request.stream.path
            jsondata = json.loads(request.body.decode('utf-8'))
            obj_claim = meClaim.eClaim_Model()
            if request.query_params.get("Api_Type") == "WEB":
                data = jsondata.get('Params').get('DETAILS')
                common.main_fun1(request.read(), path)
                obj_claim.jsondata = json.dumps(data)
                ld_out_message = obj_claim.eClaim_approver_set()
                if ld_out_message.get("MESSAGE") == 'SUCCESS':
                    ld_dict = {"MESSAGE": "SUCCESS"}
                elif ld_out_message.get("MESSAGE") == 'FAIL':
                    ld_dict = {"MESSAGE": "FAIL"}
                else:
                    ld_dict = {"MESSAGE": 'ERROR_OCCURED.' + ld_out_message.get("MESSAGE")}
                return Response(ld_dict)
            else:
                DETAILS = android.Android.set_data_dtl(self, request)
                common.main_fun1(request.read(), path)
                obj_claim.jsonData = json.dumps(DETAILS)
                ld_out_message = obj_claim.eClaim_onbehalf_set()
                if ld_out_message.get("MESSAGE") == 'SUCCESS':
                    ld_dict = {"MESSAGE": "SUCCESS"}
                elif ld_out_message.get("MESSAGE") == 'FAIL':
                    ld_dict = {"MESSAGE": "FAIL"}
                else:
                    ld_dict = {"MESSAGE": 'ERROR_OCCURED.' + ld_out_message.get("MESSAGE")}
                return Response(ld_dict)
        except Exception as e:
            common.logger.error(e)
            er = "Erro Line no :" + str(format(sys.exc_info()[-1].tb_lineno)) + " " + "Error :" + str(e)
            return Response({"MESSAGE": "ERROR_OCCURED", "DATA": er, "STATUS": 1})
class Expense_Maker(APIView):
    def post(self,request):
        try:
            obj_claim = meClaim.eClaim_Model()
            if request.query_params.get("Api_Type") == "WEB":
                path = self.request.stream.path
                jsondata = json.loads(request.body.decode('utf-8'))
                obj_claim.jsonData = json.dumps(jsondata.get('Params').get('DETAILS'))
                common.main_fun1(request.read(), path)
                # data_return = verify.advance_adjust(self,request,jsondata.get('Params').get('DETAILS').get('tourgid'))
                # if data_return.get("MESSAGE") == 'SUCCESS':
                ld_out_message = obj_claim.eClaim_movetoapproval_set()
                if ld_out_message.get("MESSAGE") == 'SUCCESS':
                    file_data = jsondata.get('Params').get('FILE').get('File')
                    if file_data != []:
                        obj_claim.jsonData = json.dumps(jsondata.get('Params').get('FILE'))
                        out_message = obj_claim.eClaim_file_set()
                        if out_message.get("MESSAGE") == 'SUCCESS':
                            ld_dict = {"MESSAGE": "SUCCESS"}
                    else:
                        ld_dict = {"MESSAGE": "SUCCESS"}
                elif ld_out_message.get("MESSAGE") == 'FAIL':
                    ld_dict = {"MESSAGE": "FAIL"}
                else:
                    ld_dict = {"MESSAGE": 'ERROR_OCCURED.' + ld_out_message.get("MESSAGE")}
                # else:
                #     ld_dict = {"MESSAGE": 'ERROR_OCCURED.' + data_return.get("MESSAGE")}
                return Response(ld_dict)
            else:
                empgid = request.auth.payload.get('user_id')
                emp_data = {
                    "empids": empgid
                }
                obj_claim.filter_json = json.dumps(emp_data)
                emp_bnk = obj_claim.eClaim_employeebnk_get()
                bank_data = json.loads(emp_bnk.get("DATA").to_json(orient='records'))
                entity = bank_data[0].get('entity_gid')
                files = []
                if request.FILES:
                    for i in range(0, len(request.FILES)):
                        name = "file" + str(i)
                        for j in request.FILES.getlist(name):
                            file_data = j
                            millis = int(round(time.time() * 1000))
                            file_name_new = str(empgid) + '_' + str(millis) + '_' + str(i) + str(j.name)
                            contents = file_data
                            s3 = boto3.resource('s3')
                            s3_obj = s3.Object(bucket_name=S3_BUCKET_NAME, key=file_name_new)
                            s3_obj.put(Body=contents)
                            content = {
                                "File_path": file_name_new,
                                "File_name": str(request.FILES[name].name),
                                "Entity_gid": entity,
                                "createby": empgid
                            }

                            files.append(content)
                # jsondata = request.POST['Tour']
                jsondata = json.loads(request.POST['Claim'])
                jsondata['Entity_Gid'] = entity
                jsondata['Employee_gid'] = empgid
                jsondata['processedby'] = empgid
                jsondata['createby'] = empgid
                tourgid = jsondata.get('tourgid')
                DETAILS = jsondata
                DETAILS = android.Android.gid_ccbsarray_check(self,DETAILS)
                # common.main_fun1(request.read(), path)
                obj_claim.jsonData = json.dumps(DETAILS)
                ld_out_message = obj_claim.eClaim_movetoapproval_set()
                if ld_out_message.get("MESSAGE") == 'SUCCESS':
                    if files != []:
                        for i in files:
                            i['RefGid'] = tourgid
                        filedata = {
                            "File": files
                        }
                        obj_claim.jsonData = json.dumps(filedata)
                        out_message = obj_claim.eClaim_file_set()
                        if out_message.get("MESSAGE") == 'SUCCESS':
                            ld_dict = {"MESSAGE": "SUCCESS","STATUS":0}
                        else:
                            ld_dict = {"MESSAGE": 'ERROR_OCCURED.' + ld_out_message.get("MESSAGE"), "STATUS": 1}
                    else:
                        ld_dict = {"MESSAGE": "SUCCESS","STATUS":0}
                elif ld_out_message.get("MESSAGE") == 'FAIL':
                    ld_dict = {"MESSAGE": "FAIL","STATUS":1}
                else:
                    ld_dict = {"MESSAGE": 'ERROR_OCCURED.' + ld_out_message.get("MESSAGE"),"STATUS":1}
                return Response(ld_dict)
        except Exception as e:
            common.logger.error(e)
            return Response({"MESSAGE": "ERROR_OCCURED", "DATA": str(e),"STATUS":1})
class Expense_City(APIView):
    def get(self,request):
        try:
            obj_claim = meClaim.eClaim_Model()
            out_data = ''
            if request.query_params.get("Api_Type") == "WEB":
                Expensegid = request.query_params.get("Expensegid")
                Emp_Grade = request.query_params.get("Emp_Grade")
                entity = request.query_params.get("Entity_Gid")
                if 'Type' in request.query_params :
                    if request.query_params.get('Type') =='LOCAL_DEP':
                        garde = Emp_Grade
                        obj_claim.filter_json = json.dumps({"Grade": garde})
                        designation = obj_claim.eClaim_empwise_grade_get()
                        designation = json.loads(designation.get("DATA").to_json(orient='records'))
                        Emp_Grade = designation[0].get('designation')
                obj_claim.filter_json = json.dumps({"Expensegid": Expensegid, "Entity_Gid": entity,"Emp_Grade":Emp_Grade})
                out_data = obj_claim.eClaim_expensecity_get()
            else:
                filter = android.Android.get_method(self, request)
                obj_claim.filter_json = json.dumps(filter)
                out_data = obj_claim.eClaim_expensecity_get()

            if out_data.get("MESSAGE") == 'FOUND':
                ld_dict = {"DATA": json.loads(out_data.get("DATA").to_json(orient='records')),
                           "MESSAGE": 'FOUND',"STATUS":0}
            elif out_data.get("MESSAGE") == 'NOT_FOUND':
                ld_dict = {"MESSAGE": 'NOT_FOUND',"STATUS":1}
            else:
                ld_dict = {"MESSAGE": 'ERROR_OCCURED.' + out_data.get("MESSAGE"),"STATUS":1}
            return Response(ld_dict)
        except Exception as e:
            common.logger.error(e)
            return Response({"MESSAGE": "ERROR_OCCURED", "DATA": str(e),"STATUS":1})
class Invoice_PaymentStatus(APIView):
    def get(self,request):
        try:
            obj_claim = meClaim.eClaim_Model()
            out_data = ''
            if request.query_params.get("Api_Type") == "WEB":
                Invoice_Header_Gid = request.query_params.get("Invoice_Header_Gid")
                entity = request.query_params.get("Entity_Gid")
                obj_claim.filter_json = json.dumps({"Invoice_Header_Gid": Invoice_Header_Gid, "Entity_Gid": entity})
                out_data = obj_claim.eClaim_paymentstatus_get()
            else:
                filter = android.Android.get_method(self, request)
                obj_claim.filter_json = json.dumps(filter)
                out_data = obj_claim.eClaim_paymentstatus_get()

            if out_data.get("MESSAGE") == 'FOUND':
                ld_dict = {"DATA": json.loads(out_data.get("DATA").to_json(orient='records')),
                           "MESSAGE": 'FOUND    '}
            elif out_data.get("MESSAGE") == 'NOT_FOUND':
                ld_dict = {"MESSAGE": 'NOT_FOUND'}
            else:
                ld_dict = {"MESSAGE": 'ERROR_OCCURED.' + out_data.get("MESSAGE")}
            return Response(ld_dict)
        except Exception as e:
            common.logger.error(e)
            return Response({"MESSAGE": "ERROR_OCCURED", "DATA": str(e),"STATUS":1})
class Gst_Get(APIView):
    def get(self, request):
        try:
            obj_claim = meClaim.eClaim_Model()
            if request.query_params.get("Api_Type") == "WEB":
                entity = request.query_params.get("Entity_Gid")
                obj_claim.filter_json = json.dumps({"Entity_Gid": entity})
                ld_out_message = obj_claim.eClaim_citytogst_get()
            else:
                emp_data = {
                    "empids": request.auth.payload.get('user_id')
                }
                Limit_End = 30
                Limit_Start = 0
                Branch_name = request.query_params.get("Branch_name")
                obj_claim.filter_json = json.dumps(emp_data)
                emp_bnk = obj_claim.eClaim_employeebnk_get()
                bank_data = json.loads(emp_bnk.get("DATA").to_json(orient='records'))
                entity = bank_data[0].get('entity_gid')
                obj_claim.filter_json = json.dumps({"Entity_Gid": entity,"Limit_Start":Limit_Start,"Limit_End":Limit_End,"Branch_name":Branch_name})
                ld_out_message = obj_claim.eClaim_citytogst_get()
            if ld_out_message.get("MESSAGE") == 'FOUND':
                ld_dict = {"DATA": json.loads(ld_out_message.get("DATA").to_json(orient='records')),
                           "MESSAGE": 'FOUND    '}
            elif ld_out_message.get("MESSAGE") == 'NOT_FOUND':
                ld_dict = {"MESSAGE": 'NOT_FOUND'}
            else:
                ld_dict = {"MESSAGE": 'ERROR_OCCURED.' + ld_out_message.get("MESSAGE")}
            return Response(ld_dict)
        except Exception as e:
            common.logger.error(e)
            return Response({"MESSAGE": "ERROR_OCCURED", "DATA": str(e), "STATUS": 1})
class Hsn_Get(APIView):
    def get(self, request):
        try:
            obj_eclaim = meClaim.eClaim_Model()
            hsn_code = request.query_params.get("Hsn_code")
            emp_data = {
                "empids": request.auth.payload.get('user_id')
            }
            obj_eclaim.filter_json = json.dumps(emp_data)
            emp_bnk = obj_eclaim.eClaim_employeebnk_get()
            bank_data = json.loads(emp_bnk.get("DATA").to_json(orient='records'))
            entity = bank_data[0].get('entity_gid')
            obj_eclaim.filter_json = json.dumps({"Entity_Gid": entity})
            tk = str(request.auth.token)
            token = "Bearer  " + tk[2:len(tk) - 1]
            grp = "GET_EMP_DATA"
            limit = "0,30"
            typ = "HSN"
            sub = "HSN_ALL"
            params = {"Group": grp, "Type": typ, "Sub_Type": sub, "Limit": limit}
            headers = {"content-type": "application/json", "Authorization": "" + token + ""}
            jsondata={
                "Params":{
                    "FILTER":{
                        "hsn_code": hsn_code
                    }
                }
            }
            classify = {
                "CLASSIFICATION": {
                    "Entity_Gid": entity
                }}
            jsondata['Params'].update(classify)
            datas = json.dumps(jsondata)
            resp = requests.post("" + ip + "/MASTER_DATA", params=params, data=datas, headers=headers,
                                 verify=False)
            ld_out_message = json.loads(resp.content.decode("utf-8"))
            if ld_out_message.get("MESSAGE") == 'FOUND':
                ld_dict = {"DATA": ld_out_message.get("DATA"),
                           "MESSAGE": 'FOUND    '}
            elif ld_out_message.get("MESSAGE") == 'NOT_FOUND':
                ld_dict = {"MESSAGE": 'NOT_FOUND'}
            else:
                ld_dict = {"MESSAGE": 'ERROR_OCCURED.' + ld_out_message.get("MESSAGE")}
            return Response(ld_dict)
        except Exception as e:
            common.logger.error(e)
            return Response({"MESSAGE": "ERROR_OCCURED", "DATA": str(e), "STATUS": 1})
class pkg_eligible_Get(APIView):
    def get(self, request):
        try:
            obj_eclaim = meClaim.eClaim_Model()
            grade = emp_grade(request.query_params.get("Tour_Gid"))
            datas = {
                "Grade": grade.upper()
            }
            obj_eclaim.filter_json = json.dumps(datas)
            ld_eligible = obj_eclaim.eClaim_gradetoelig_get()
            ld_elig = json.loads(ld_eligible.get("DATA").to_json(orient='records'))
            ld_dict = {"DATA": ld_elig,
                       "MESSAGE": 'FOUND'}
            return Response(ld_dict)

        except Exception as e:
            common.logger.error(e)
            return Response({"MESSAGE": "ERROR_OCCURED", "DATA": str(e), "STATUS": 1})
class Employee_Dependent(APIView):
    def get(self, request):
        try:
            obj_eclaim = meClaim.eClaim_Model()
            out_data = 0
            if request.query_params.get("Api_Type") =="WEB":
                obj_eclaim.employee_gid  = request.query_params.get("Employee_gid")
                out_data = obj_eclaim.eClaim_emptodependent_get()
                ld_dict = {"DATA": json.loads(out_data.get("DATA").to_json(orient='records')), "MESSAGE": 'FOUND'}
            else:
                obj_eclaim.employee_gid  = request.auth.payload.get('user_id')
                out_data = obj_eclaim.eClaim_emptodependent_get()
                ld_dict = {"DATA": json.loads(out_data.get("DATA").to_json(orient='records')), "MESSAGE": 'FOUND'}
            return Response(ld_dict)

        except Exception as e:
            common.logger.error(e)
            return Response({"MESSAGE": "ERROR_OCCURED", "DATA": str(e), "STATUS": 1})
class Travel_Eligible(APIView):
    def get(self, request):
        try:
            grade = emp_grade(request.query_params.get("Tour_Gid"))
            data_eligible = verify.travel_exp.grade_eligible(self, grade.upper())
            ld_dict = {"DATA": data_eligible.get('type').get('type'),
                       "MESSAGE": 'FOUND', "STATUS": 0}
            return Response(ld_dict)
        except Exception as e:
            common.logger.error(e)
            return Response({"MESSAGE": "ERROR_OCCURED", "DATA": str(e), "STATUS": 1})
def emp_grade(tourgid):
    obj_claim = meClaim.eClaim_Model()
    obj_claim.employee_gid = tourgid
    ld_out_emp = obj_claim.eClaim_tourtoemp_get()
    ld_dict = json.loads(ld_out_emp.get("DATA").to_json(orient='records'))
    common.logger.error([{"tourtoemp_get": str(ld_dict)}])
    empgrade = ld_dict[0].get('empgrade')
    return empgrade
class BS_Data_Get(APIView):
    def get(self, request):
        try:
            obj_eclaim = meClaim.eClaim_Model()
            obj_eclaim.employee_gid = request.auth.payload.get('user_id')
            emp_bnk = obj_eclaim.eClaim_entity_get()
            bank_data = json.loads(emp_bnk.get("DATA").to_json(orient='records'))
            entity = bank_data[0].get('entity_gid')
            drop_b = {
                "Table_name": "ap_mst_tbs",
                "Column_1": "tbs_gid as bs_gid,tbs_code as bs_code,tbs_no as bs_no,tbs_name as bs_name",
                "Column_2": "",
                "Where_Common": "tbs",
                "Where_Primary": "",
                "Primary_Value": "",
                "Order_by": "no"
            }
            drop_tables = {"data": drop_b}
            action = 'Debit'
            params = {'Action': action, 'Entity_Gid': entity}
            datas = json.dumps(drop_tables.get('data'))
            tk = str(request.auth.token)
            token = "Bearer  " + tk[2:len(tk) - 1]
            headers = {"content-type": "application/json", "Authorization": "" + token + ""}
            resp = requests.post("" + ip + "/All_Tables_Values_Get", params=params, data=datas, headers=headers,
                                 verify=False)
            response_data = resp.content.decode("utf-8")
            response_data = json.loads(response_data)
            if response_data.get('MESSAGE') == "FOUND":
                response_data['STATUS'] = 1
            else:
                response_data['STATUS'] = 0
            return Response(response_data)
        except Exception as e:
            common.logger.error(e)
            return Response({"MESSAGE": "ERROR_OCCURED", "DATA": str(e), "STATUS": 1})
class CC_Data_Get(APIView):
    def get(self, request):
        try:
            obj_eclaim = meClaim.eClaim_Model()
            obj_eclaim.employee_gid = request.auth.payload.get('user_id')
            emp_bnk = obj_eclaim.eClaim_entity_get()
            bank_data = json.loads(emp_bnk.get("DATA").to_json(orient='records'))
            entity = bank_data[0].get('entity_gid')
            bs_gid = request.query_params.get("Bs_gid")
            drop_b = {
                "Table_name": "ap_mst_tcc",
                "Column_1": "tcc_gid as cc_gid,tcc_code as cc_code,tcc_no as cc_no,tcc_name as cc_name",
                "Column_2": "",
                "Where_Common": "tcc",
                "Where_Primary": "bsgid",
                "Primary_Value": bs_gid,
                "Order_by": "no"
            }
            drop_tables = {"data": drop_b}
            action = 'Debit'
            params = {'Action': action, 'Entity_Gid': entity}
            datas = json.dumps(drop_tables.get('data'))
            tk = str(request.auth.token)
            token = "Bearer  " + tk[2:len(tk) - 1]
            headers = {"content-type": "application/json", "Authorization": "" + token + ""}
            resp = requests.post("" + ip + "/All_Tables_Values_Get", params=params, data=datas, headers=headers,
                                 verify=False)
            response_data = resp.content.decode("utf-8")
            response_data = json.loads(response_data)
            if response_data.get('MESSAGE') == "FOUND":
                response_data['STATUS'] = 1
            else:
                response_data['STATUS'] = 0
            return Response(response_data)
        except Exception as e:
            common.logger.error(e)
            return Response({"MESSAGE": "ERROR_OCCURED", "DATA": str(e), "STATUS": 1})
class CCBS_Data_Get(APIView):
    def get(self, request):
        try:
            obj_eclaim = meClaim.eClaim_Model()
            tourgid = request.query_params.get("Tour_Gid")
            CCBS_Type = request.query_params.get("CCBS_Type")
            obj_eclaim.filter_json = json.dumps({"Tour_Gid": tourgid,"CCBS_Type":CCBS_Type})
            out_data = obj_eclaim.eClaim_ccbs_get()
            if out_data.get("MESSAGE") == 'FOUND':
                obj_eclaim.employee_gid = request.auth.payload.get('user_id')
                emp_bnk = obj_eclaim.eClaim_entity_get()
                bank_data = json.loads(emp_bnk.get("DATA").to_json(orient='records'))
                entity = bank_data[0].get('entity_gid')
                tk = str(request.auth.token)
                token = "Bearer  " + tk[2:len(tk) - 1]
                data = verify.ccbs(self,json.loads(out_data.get("DATA").to_json(orient='records')),entity,token)
                ld_dict = {"DATA": data,"MESSAGE": 'FOUND',"STATUS": 0}
            elif out_data.get("MESSAGE") == 'NOT_FOUND':
                ld_dict = {"MESSAGE": 'NOT_FOUND',"STATUS": 1}
            else:
                ld_dict = {"MESSAGE": 'ERROR_OCCURED.' + out_data.get("MESSAGE"),"STATUS": 1}
            return Response(ld_dict)
        except Exception as e:
            common.logger.error(e)
            return Response({"MESSAGE": "ERROR_OCCURED", "DATA": str(e), "STATUS": 1})
def exp_onbehalf_emp(self,request):
    if request.query_params.get("Api_Type") == "WEB":
        jsondata = json.loads(request.body.decode('utf-8'))
        if request.query_params.get("Type") == "ONBEHALF":
            empid = jsondata.get('Params').get('DETAILS').get('processedby')
        else:
            empid = request.auth.payload.get('user_id')
    else:
        if request.query_params.get("Type") == "ONBEHALF":
            jsondata = json.loads(request.body.decode('utf-8'))
            empid = jsondata.get('DETAILS').get('processedby')
        else:
            empid = request.auth.payload.get('user_id')

    return empid
class Dailydiem_Get(APIView):
    def get(self, request):
        try:
            obj_eclaim = meClaim.eClaim_Model()
            if request.query_params.get("Api_Type") =="WEB":
                entity = request.query_params.get("Entity_Gid")
                Claimreqgid = request.query_params.get("Claimreqgid")
                obj_eclaim.filter_json = json.dumps({"Entity_Gid": entity, "Claimreqgid": Claimreqgid})
                ld_out_message = obj_eclaim.eClaim_dailydiem_get()
            else:
                filter = android.Android.get_method(self, request)
                obj_eclaim.filter_json = json.dumps(filter)
                ld_out_message = obj_eclaim.eClaim_dailydiem_get()
            if ld_out_message.get("MESSAGE") == 'FOUND':
                ld_dict = {"DATA": json.loads(ld_out_message.get("DATA").to_json(orient='records')), "MESSAGE": 'FOUND'}
            elif ld_out_message.get("MESSAGE") == 'NOT_FOUND':
                ld_dict = {"MESSAGE": 'NOT_FOUND'}
            else:
                ld_dict = {"MESSAGE": 'ERROR_OCCURED.' + ld_out_message.get("MESSAGE")}
            return Response(ld_dict)
        except Exception as e:
            common.logger.error(e)
            return Response({"MESSAGE": "ERROR_OCCURED", "DATA": str(e), "STATUS": 1})
class Dailydiem_Logic(APIView):
    def post(self, request):
        try:
            path = self.request.stream.path
            jsondata = json.loads(request.body.decode('utf-8'))
            common.main_fun1(request.read(), path)
            empid = 0
            if request.query_params.get("Type") == "ONBEHALF":
                empid = jsondata.get('Employee_gid')
            else:
                empid = request.auth.payload.get('user_id')
            obj_claim = meClaim.eClaim_Model()
            obj_claim.employee_gid = empid
            emp_bnk = obj_claim.eClaim_entity_get()
            bank_data = json.loads(emp_bnk.get("DATA").to_json(orient='records'))
            entity_gid = bank_data[0].get('entity_gid')
            tourgid = jsondata.get('tourgid')
            grade = emp_grade(tourgid)
            json_param = android.Android.param_conversion(self, jsondata,entity_gid)
            ld_dict = verify.dailydiem.eligible_amount(self, json_param,grade,empid)
            return Response(ld_dict)
        except Exception as e:
            common.logger.error(e)
            return Response({"MESSAGE": "ERROR_OCCURED", "DATA": str(e), "STATUS": 1})
class Dailydiem(APIView):
    def post(self,request):
        try:
            obj_claim = meClaim.eClaim_Model()
            path = self.request.stream.path
            if request.query_params.get("Api_Type") =="WEB":
                jsondata = json.loads(request.body.decode('utf-8'))
                DETAILS = jsondata.get('Params').get('DETAILS')
                CHANGE = jsondata.get('Params').get('CHANGE').get('DATA')
                common.main_fun1(request.read(), path)
                empid = exp_onbehalf_emp(self,request)
                grade = emp_grade(DETAILS.get('tourgid'))
                obj_claim.employee_gid = empid
                emp_bnk = obj_claim.eClaim_entity_get()
                bank_data = json.loads(emp_bnk.get("DATA").to_json(orient='records'))
                entity = bank_data[0].get('entity_gid')
                for i in CHANGE:
                    json_param = android.Android.param_conversion(self, i, entity)
                    json_param['Params']['FILTER']['expensegid'] = DETAILS.get('expensegid')
                    json_param['Params']['FILTER']['from_date'] = json_param.get('Params').get('FILTER').get('fromdate')
                    json_param['Params']['FILTER']['to_date'] = json_param.get('Params').get('FILTER').get('todate')
                    ld_dict = verify.dailydiem.eligible_amount(self, json_param, grade,empid)
                    i['eligibleamount'] = ld_dict.get('DATA').get('Eligible_amount')
                    i['syshours'] = ld_dict.get('DATA').get('sys_hours')
                logic = verify.dailydiem.submit_data(self, CHANGE, DETAILS)
                if logic == "True":
                    obj_claim.jsondata = json.dumps(DETAILS)
                    obj_claim.jsonData = json.dumps({"DATA": CHANGE})
                    ld_out_message = obj_claim.eClaim_dailydiem_set()
                    msg = ld_out_message.get("MESSAGE").split(",")
                    if msg[0] == 'SUCCESS':
                        ld_dict = {"MESSAGE": ld_out_message.get("MESSAGE")}
                    elif msg[0] == 'FAIL':
                        ld_dict = {"MESSAGE": "FAIL"}
                    else:
                        ld_dict = {"MESSAGE": 'ERROR_OCCURED.' + ld_out_message.get("MESSAGE")}
                    return Response(ld_dict)
                else:
                    return Response(logic[1])
            else:
                obj_claim.employee_gid = request.auth.payload.get('user_id')
                emp_bnk = obj_claim.eClaim_entity_get()
                bank_data = json.loads(emp_bnk.get("DATA").to_json(orient='records'))
                entity = bank_data[0].get('entity_gid')
                DETAILS = android.Android.set_data_dtl(self, request)
                DETAILS = android.Android.gid_check(self, DETAILS)
                CHANGE = android.Android.set_data_chng(self, request)
                CHANGE = android.Android.gid_array_check(self, CHANGE)
                common.main_fun1(request.read(), path)
                empid = exp_onbehalf_emp(self, request)
                DETAILS['Entity_Gid'] = entity
                DETAILS['processedby'] =  empid
                DETAILS['createby'] =  empid
                CHANGE = CHANGE.get('DATA')
                grade = emp_grade(DETAILS.get('tourgid'))
                for i in CHANGE:
                    json_param = android.Android.param_conversion(self, i, entity)
                    json_param['Params']['FILTER']['expensegid'] = DETAILS.get('expensegid')
                    json_param['Params']['FILTER']['from_date'] = json_param.get('Params').get('FILTER').get('fromdate')
                    json_param['Params']['FILTER']['to_date'] = json_param.get('Params').get('FILTER').get('todate')
                    ld_dict = verify.dailydiem.eligible_amount(self, json_param, grade,empid)
                    i['eligibleamount'] = ld_dict.get('DATA').get('Eligible_amount')
                    i['syshours'] = ld_dict.get('DATA').get('sys_hours')
                logic = verify.dailydiem.submit_data(self, CHANGE, DETAILS)
                if logic == "True":
                    obj_claim.jsondata = json.dumps(DETAILS)
                    obj_claim.jsonData = json.dumps({"DATA": CHANGE})
                    ld_out_message = obj_claim.eClaim_dailydiem_set()
                    msg = ld_out_message.get("MESSAGE").split(",")
                    if msg[0] == 'SUCCESS':
                        ld_dict = {"MESSAGE": msg[0]}
                    elif msg[0] == 'FAIL':
                        ld_dict = {"MESSAGE": "FAIL"}
                    else:
                        ld_dict = {"MESSAGE": 'ERROR_OCCURED.' + ld_out_message.get("MESSAGE")}
                    return Response(ld_dict)
                else:
                    return Response(logic[1])
        except Exception as e:
            common.logger.error(e)
            return Response({"MESSAGE": "ERROR_OCCURED", "DATA": str(e),"STATUS":1})
class Approve_amount(APIView):
    def post(self,request):
        try:
            obj_claim = meClaim.eClaim_Model()
            path = self.request.stream.path
            ld_out_message = ''
            if request.query_params.get("Api_Type") =="WEB":
                jsondata = json.loads(request.body.decode('utf-8'))
                obj_claim.jsondata = json.dumps(jsondata.get('Params').get('DETAILS'))
                obj_claim.jsonData = json.dumps(jsondata.get('Params').get('CHANGE'))
                common.main_fun1(request.read(), path)
                ld_out_message = obj_claim.eClaim_approveamount_set()

            else:
                obj_claim.employee_gid = request.auth.payload.get('user_id')
                emp_bnk = obj_claim.eClaim_entity_get()
                bank_data = json.loads(emp_bnk.get("DATA").to_json(orient='records'))
                entity = bank_data[0].get('entity_gid')
                DETAILS = android.Android.set_data_dtl(self, request)
                DETAILS = android.Android.gid_check(self, DETAILS)
                CHANGE = android.Android.set_data_chng(self, request)
                CHANGE = android.Android.gid_array_check(self, CHANGE)
                common.main_fun1(request.read(), path)
                DETAILS['Entity_Gid'] = entity
                DETAILS['processedby'] =  request.auth.payload.get('user_id')
                DETAILS['createby'] =  request.auth.payload.get('user_id')
                obj_claim.jsondata = json.dumps(DETAILS)
                obj_claim.jsonData = json.dumps(CHANGE)
                ld_out_message = obj_claim.eClaim_approveamount_set()

            if ld_out_message.get("MESSAGE") == 'SUCCESS':
                ld_dict = {"MESSAGE": "SUCCESS"}
            elif ld_out_message.get("MESSAGE") == 'FAIL':
                ld_dict = {"MESSAGE": "FAIL"}
            else:
                ld_dict = {"MESSAGE": 'ERROR_OCCURED.' + ld_out_message.get("MESSAGE")}
            return Response(ld_dict)
        except Exception as e:
            common.logger.error(e)
            return Response({"MESSAGE": "ERROR_OCCURED", "DATA": str(e),"STATUS":1})
class Travel_Get(APIView):
    def get(self, request):
        try:
            obj_eclaim = meClaim.eClaim_Model()
            if request.query_params.get("Api_Type") == "WEB":
                entity = request.query_params.get("Entity_Gid")
                Claimreqgid = request.query_params.get("Claimreqgid")
                obj_eclaim.filter_json = json.dumps({"Entity_Gid": entity, "Claimreqgid": Claimreqgid})
                ld_out_message = obj_eclaim.eClaim_travelexp_get()
            else:
                filter = android.Android.get_method(self, request)
                obj_eclaim.filter_json = json.dumps(filter)
                ld_out_message = obj_eclaim.eClaim_travelexp_get()

            if ld_out_message.get("MESSAGE") == 'FOUND':
                dict = json.loads(ld_out_message.get("DATA").to_json(orient='records'))
                ld_dict = {"DATA": dict, "MESSAGE": 'FOUND'}
            elif ld_out_message.get("MESSAGE") == 'NOT_FOUND':
                ld_dict = {"MESSAGE": 'NOT_FOUND'}
            else:
                ld_dict = {"MESSAGE": 'ERROR_OCCURED.' + ld_out_message.get("MESSAGE")}
            return Response(ld_dict)
        except Exception as e:
            common.logger.error(e)
            return Response({"MESSAGE": "ERROR_OCCURED", "DATA": str(e), "STATUS": 1})
class Travel_Logic(APIView):
    def post(self, request):
        try:
            path = self.request.stream.path
            jsondata = json.loads(request.body.decode('utf-8'))
            common.main_fun1(request.read(), path)
            empid = 0
            if request.query_params.get("Type") == "ONBEHALF":
                empid = jsondata.get('Employee_gid')

            else:
                empid = request.auth.payload.get('user_id')
            obj_claim = meClaim.eClaim_Model()
            obj_claim.employee_gid = empid
            emp_bnk = obj_claim.eClaim_entity_get()
            bank_data = json.loads(emp_bnk.get("DATA").to_json(orient='records'))
            entity_gid = bank_data[0].get('entity_gid')
            json_param = android.Android.param_conversion(self, jsondata, entity_gid)
            eligible_value = travel_logic(self, empid, json_param)
            ld_dict = {"DATA": eligible_value,
                       "MESSAGE": 'FOUND'}
            return Response(ld_dict)
        except Exception as e:
            common.logger.error(e)
            return Response({"MESSAGE": "ERROR_OCCURED", "DATA": str(e), "STATUS": 1})
def travel_logic(self,empid,json_param):
    #tourgid = json_param.get('Params').get('FILTER').get('tourgid')
    #grade = emp_grade(tourgid)
    # data_eligible = verify.travel_exp.grade_eligible(self, grade.upper())
    # eligible_amount = verify.travel_exp.ticket_fare(self, json_param, data_eligible.get('type').get('type'))
    priorpermission = json_param.get('Params').get('FILTER').get('priorpermission')
    claimedamount = json_param.get('Params').get('FILTER').get('claimedamount')
    tktbybank = json_param.get('Params').get('FILTER').get('tktbybank')
    # amount = 0
    # if priorpermission != "" and claimedamount != "":
    #     amount = verify.travel_exp.check_eligbility(self, int(priorpermission), float(claimedamount),
    #                                                 float(eligible_amount))
    # if tktbybank != "":
    #     amount = verify.travel_exp.check_ticket(self, int(tktbybank), int(amount))
    #
    # eligible_value = {
    #     "Eligible_amount": eligible_amount,
    #     "Athorised_amount": amount,
    # }
    eligible_value = {
        "Eligible_amount": claimedamount
    }
    return eligible_value
class Travel(APIView):
    def post(self, request):
        try:
            obj_claim = meClaim.eClaim_Model()
            path = self.request.stream.path
            if request.query_params.get("Api_Type") == "WEB":
                jsondata = json.loads(request.body.decode('utf-8'))
                DETAILS = jsondata.get('Params').get('DETAILS')
                CHANGE = jsondata.get('Params').get('CHANGE').get('DATA')
                common.main_fun1(request.read(), path)
                empid = exp_onbehalf_emp(self, request)
                obj_claim.employee_gid = empid
                emp_bnk = obj_claim.eClaim_entity_get()
                bank_data = json.loads(emp_bnk.get("DATA").to_json(orient='records'))
                entity = bank_data[0].get('entity_gid')
                for i in CHANGE:
                    json_param = android.Android.param_conversion(self, i, entity)
                    json_param['Params']['FILTER']['expensegid'] = DETAILS.get('expensegid')
                    ld_dict =  travel_logic(self, empid, json_param)
                    i['eligibleamount'] = ld_dict.get('Eligible_amount')
                logic = verify.travel_exp.calck_totalamt(self, CHANGE, DETAILS)
                if logic == "True":
                    obj_claim.jsondata = json.dumps(DETAILS)
                    obj_claim.jsonData = json.dumps({"DATA": CHANGE})
                    ld_out_message = obj_claim.eClaim_travelexp_set()
                    msg = ld_out_message.get("MESSAGE").split(",")
                    if msg[0] == 'SUCCESS':
                        ld_dict = {"MESSAGE": ld_out_message.get("MESSAGE")}
                    elif msg[0] == 'FAIL':
                        ld_dict = {"MESSAGE": "FAIL"}
                    else:
                        ld_dict = {"MESSAGE": 'ERROR_OCCURED.' + ld_out_message.get("MESSAGE")}
                    return Response(ld_dict)
                else:
                    return Response(logic[1])
            else:
                obj_claim.employee_gid = request.auth.payload.get('user_id')
                emp_bnk = obj_claim.eClaim_entity_get()
                bank_data = json.loads(emp_bnk.get("DATA").to_json(orient='records'))
                entity = bank_data[0].get('entity_gid')
                DETAILS = android.Android.set_data_dtl(self, request)
                DETAILS = android.Android.gid_check(self, DETAILS)
                CHANGE = android.Android.set_data_chng(self, request)
                CHANGE = android.Android.gid_array_check(self, CHANGE)
                common.main_fun1(request.read(), path)
                empid = exp_onbehalf_emp(self, request)
                DETAILS['Entity_Gid'] = entity
                DETAILS['processedby'] = empid
                DETAILS['createby'] = empid
                CHANGE = CHANGE.get('DATA')
                # for i in CHANGE:
                #     json_param = android.Android.param_conversion(self, i, entity)
                #     json_param['Params']['FILTER']['expensegid'] = DETAILS.get('expensegid')
                #     ld_dict =  travel_logic(self, empid, json_param)
                #     i['eligibleamount'] = ld_dict.get('Eligible_amount')
                logic = verify.travel_exp.calck_totalamt(self, CHANGE, DETAILS)
                if logic == "True":
                    obj_claim.jsondata = json.dumps(DETAILS)
                    obj_claim.jsonData = json.dumps({"DATA": CHANGE})
                    ld_out_message = obj_claim.eClaim_travelexp_set()
                    msg = ld_out_message.get("MESSAGE").split(",")
                    if msg[0] == 'SUCCESS':
                        ld_dict = {"MESSAGE": msg[0]}
                    elif msg[0] == 'FAIL':
                        ld_dict = {"MESSAGE": "FAIL"}
                    else:
                        ld_dict = {"MESSAGE": 'ERROR_OCCURED.' + ld_out_message.get("MESSAGE")}
                    return Response(ld_dict)
                else:
                    return Response(logic[1])
        except Exception as e:
            common.logger.error(e)
            return Response({"MESSAGE": "ERROR_OCCURED", "DATA": str(e), "STATUS": 1})
class Lodging_Get(APIView):
    def get(self, request):
        try:
            obj_eclaim = meClaim.eClaim_Model()
            if request.query_params.get("Api_Type") == "WEB":
                entity = request.query_params.get("Entity_Gid")
                Claimreqgid = request.query_params.get("Claimreqgid")
                obj_eclaim.filter_json = json.dumps({"Entity_Gid": entity, "Claimreqgid": Claimreqgid})
                ld_out_message = obj_eclaim.eClaim_lodging_get()
            else:
                filter = android.Android.get_method(self, request)
                obj_eclaim.filter_json = json.dumps(filter)
                ld_out_message = obj_eclaim.eClaim_lodging_get()

            if ld_out_message.get("MESSAGE") == 'FOUND':
                dict = json.loads(ld_out_message.get("DATA").to_json(orient='records'))
                ld_dict = {"DATA": dict, "MESSAGE": 'FOUND'}
            elif ld_out_message.get("MESSAGE") == 'NOT_FOUND':
                ld_dict = {"MESSAGE": 'NOT_FOUND'}
            else:
                ld_dict = {"MESSAGE": 'ERROR_OCCURED.' + ld_out_message.get("MESSAGE")}
            return Response(ld_dict)
        except Exception as e:
            common.logger.error(e)
            return Response({"MESSAGE": "ERROR_OCCURED", "DATA": str(e), "STATUS": 1})
class Lodging_Logic(APIView):
    def post(self, request):
        try:
            path = self.request.stream.path
            jsondata = json.loads(request.body.decode('utf-8'))
            common.main_fun1(request.read(), path)
            empid = 0
            if request.query_params.get("Type") == "ONBEHALF":
                empid = jsondata.get('Employee_gid')

            else:
                empid = request.auth.payload.get('user_id')
            obj_claim = meClaim.eClaim_Model()
            obj_claim.employee_gid = empid
            emp_bnk = obj_claim.eClaim_entity_get()
            bank_data = json.loads(emp_bnk.get("DATA").to_json(orient='records'))
            entity_gid = bank_data[0].get('entity_gid')
            json_param = android.Android.param_conversion(self, jsondata, entity_gid)
            eligible_value = lodging_logic(self, empid, json_param)
            ld_dict = {"DATA": eligible_value,
                       "MESSAGE": 'FOUND'}
            return Response(ld_dict)
        except Exception as e:
            common.logger.error(e)
            return Response({"MESSAGE": "ERROR_OCCURED", "DATA": str(e), "STATUS": 1})
def lodging_logic(self,empid,json_param):
    tourgid = json_param.get('Params').get('FILTER').get('tourgid')
    grade = emp_grade(tourgid)
    common.logger.error([{"grade": str(grade)}])
    amount = verify.lodging.date_valid(self, json_param, grade)
    noofdays = amount.get('noofdays')
    accbybank = json_param.get('Params').get('FILTER').get('accbybank')
    # claimedamount = json_param.get('Params').get('FILTER').get('claimedamount')
    if accbybank != "":
        amount = verify.lodging.calc_accbybank(self, json_param,float(amount.get('Eligible_amount')))
    eligible_value = {
        "Eligible_amount": amount.get('Eligible_amount'),
        "noofdays": noofdays
    }
    return eligible_value
class Lodging(APIView):
    def post(self, request):
        try:
            obj_claim = meClaim.eClaim_Model()
            path = self.request.stream.path
            if request.query_params.get("Api_Type") == "WEB":
                jsondata = json.loads(request.body.decode('utf-8'))
                DETAILS = jsondata.get('Params').get('DETAILS')
                CHANGE = jsondata.get('Params').get('CHANGE').get('DATA')
                common.main_fun1(request.read(), path)
                empid = exp_onbehalf_emp(self, request)
                obj_claim.employee_gid = empid
                emp_bnk = obj_claim.eClaim_entity_get()
                bank_data = json.loads(emp_bnk.get("DATA").to_json(orient='records'))
                entity = bank_data[0].get('entity_gid')
                for i in CHANGE:
                    json_param = android.Android.param_conversion(self, i, entity)
                    json_param['Params']['FILTER']['expensegid'] = DETAILS.get('expensegid')
                    ld_dict = lodging_logic(self, empid, json_param)
                    i['eligibleamount'] = ld_dict.get('Eligible_amount')
                    i['noofdays'] = ld_dict.get('noofdays')
                logic = verify.lodging.calck_totalamt(self, CHANGE, DETAILS)
                if logic == "True":
                    obj_claim.jsondata = json.dumps(DETAILS)
                    obj_claim.jsonData = json.dumps({"DATA": CHANGE})
                    ld_out_message = obj_claim.eClaim_lodging_set()
                    msg = ld_out_message.get("MESSAGE").split(",")
                    if msg[0] == 'SUCCESS':
                        ld_dict = {"MESSAGE": ld_out_message.get("MESSAGE")}
                    elif msg[0] == 'FAIL':
                        ld_dict = {"MESSAGE": "FAIL"}
                    else:
                        ld_dict = {"MESSAGE": 'ERROR_OCCURED.' + ld_out_message.get("MESSAGE")}
                    return Response(ld_dict)
                else:
                    return Response(logic[1])
            else:
                obj_claim.employee_gid = request.auth.payload.get('user_id')
                emp_bnk = obj_claim.eClaim_entity_get()
                bank_data = json.loads(emp_bnk.get("DATA").to_json(orient='records'))
                entity = bank_data[0].get('entity_gid')

                DETAILS = android.Android.set_data_dtl(self, request)
                DETAILS = android.Android.gid_check(self, DETAILS)
                CHANGE = android.Android.set_data_chng(self, request)
                CHANGE = android.Android.gid_array_check(self, CHANGE)
                common.main_fun1(request.read(), path)
                empid = exp_onbehalf_emp(self, request)
                DETAILS['Entity_Gid'] = entity
                DETAILS['processedby'] = empid
                DETAILS['createby'] = empid
                CHANGE = CHANGE.get('DATA')
                obj_claim.employee_gid = empid
                emp_bnk = obj_claim.eClaim_entity_get()
                bank_data = json.loads(emp_bnk.get("DATA").to_json(orient='records'))
                entity = bank_data[0].get('entity_gid')
                for i in CHANGE:
                    json_param = android.Android.param_conversion(self, i, entity)
                    json_param['Params']['FILTER']['expensegid'] = DETAILS.get('expensegid')
                    ld_dict = lodging_logic(self, empid, json_param)
                    i['eligibleamount'] = ld_dict.get('Eligible_amount')
                    i['noofdays'] = ld_dict.get('noofdays')
                logic = verify.lodging.calck_totalamt(self, CHANGE, DETAILS)
                if logic == "True":
                    obj_claim.jsondata = json.dumps(DETAILS)
                    obj_claim.jsonData = json.dumps({"DATA": CHANGE})
                    ld_out_message = obj_claim.eClaim_lodging_set()
                    msg = ld_out_message.get("MESSAGE").split(",")
                    if msg[0] == 'SUCCESS':
                        ld_dict = {"MESSAGE": msg[0]}
                    elif msg[0] == 'FAIL':
                        ld_dict = {"MESSAGE": "FAIL"}
                    else:
                        ld_dict = {"MESSAGE": 'ERROR_OCCURED.' + ld_out_message.get("MESSAGE")}
                    return Response(ld_dict)
                else:
                    return Response(logic[1])
        except Exception as e:
            common.logger.error(e)
            return Response({"MESSAGE": "ERROR_OCCURED", "DATA": str(e), "STATUS": 1})
class Locconv_Get(APIView):
    def get(self, request):
        try:
            obj_eclaim = meClaim.eClaim_Model()
            if request.query_params.get("Api_Type") == "WEB":
                entity = request.query_params.get("Entity_Gid")
                Claimreqgid = request.query_params.get("Claimreqgid")
                obj_eclaim.filter_json = json.dumps({"Entity_Gid": entity, "Claimreqgid": Claimreqgid})
                ld_out_message = obj_eclaim.eClaim_loccon_get()
            else:
                filter = android.Android.get_method(self, request)
                obj_eclaim.filter_json = json.dumps(filter)
                ld_out_message = obj_eclaim.eClaim_loccon_get()

            if ld_out_message.get("MESSAGE") == 'FOUND':
                ld_dict = {"DATA": json.loads(ld_out_message.get("DATA").to_json(orient='records')), "MESSAGE": 'FOUND'}
            elif ld_out_message.get("MESSAGE") == 'NOT_FOUND':
                ld_dict = {"MESSAGE": 'NOT_FOUND'}
            else:
                ld_dict = {"MESSAGE": 'ERROR_OCCURED.' + ld_out_message.get("MESSAGE")}
            return Response(ld_dict)
        except Exception as e:
            common.logger.error(e)
            return Response({"MESSAGE": "ERROR_OCCURED", "DATA": str(e), "STATUS": 1})
class Locconv_Logic(APIView):
    def post(self, request):
        try:
            path = self.request.stream.path
            jsondata = json.loads(request.body.decode('utf-8'))
            common.main_fun1(request.read(), path)
            empid = 0
            if request.query_params.get("Type") == "ONBEHALF":
                empid = jsondata.get('Employee_gid')
            else:
                empid = request.auth.payload.get('user_id')
            obj_claim = meClaim.eClaim_Model()
            obj_claim.employee_gid = empid
            emp_bnk = obj_claim.eClaim_entity_get()
            bank_data = json.loads(emp_bnk.get("DATA").to_json(orient='records'))
            entity_gid = bank_data[0].get('entity_gid')
            json_param = android.Android.param_conversion(self, jsondata, entity_gid)
            eligible_value = locconv_logic(self,empid,json_param)
            ld_dict = {"DATA": eligible_value,
                       "MESSAGE": 'FOUND'}
            return Response(ld_dict)
        except Exception as e:
            common.logger.error(e)
            return Response({"MESSAGE": "ERROR_OCCURED", "DATA": str(e), "STATUS": 1})
def locconv_logic(self,empid,json_param):
    tourgid = json_param.get('Params').get('FILTER').get('tourgid')
    grade = emp_grade(tourgid)
    eligible_value = verify.localcon.validate_data(self, json_param, grade)
    return eligible_value
class Locconv(APIView):
    def post(self, request):
        try:
            obj_claim = meClaim.eClaim_Model()
            path = self.request.stream.path
            if request.query_params.get("Api_Type") == "WEB":
                jsondata = json.loads(request.body.decode('utf-8'))
                DETAILS = jsondata.get('Params').get('DETAILS')
                CHANGE = jsondata.get('Params').get('CHANGE').get('DATA')
                common.main_fun1(request.read(), path)
                empid = exp_onbehalf_emp(self, request)
                obj_claim.employee_gid = empid
                emp_bnk = obj_claim.eClaim_entity_get()
                bank_data = json.loads(emp_bnk.get("DATA").to_json(orient='records'))
                entity = bank_data[0].get('entity_gid')
                for i in CHANGE:
                    json_param = android.Android.param_conversion(self, i, entity)
                    json_param['Params']['FILTER']['expensegid'] = DETAILS.get('expensegid')
                    ld_dict = locconv_logic(self, empid, json_param)
                    i['eligibleamount'] = ld_dict.get('Eligible_amount')
                logic = verify.localcon.calck_totalamt(self, CHANGE, DETAILS)
                if logic == "True":
                    obj_claim.jsondata = json.dumps(DETAILS)
                    obj_claim.jsonData = json.dumps({"DATA": CHANGE})
                    ld_out_message = obj_claim.eClaim_loccon_set()
                    msg = ld_out_message.get("MESSAGE").split(",")
                    if msg[0] == 'SUCCESS':
                        ld_dict = {"MESSAGE": ld_out_message.get("MESSAGE")}
                    elif msg[0] == 'FAIL':
                        ld_dict = {"MESSAGE": "FAIL"}
                    else:
                        ld_dict = {"MESSAGE": 'ERROR_OCCURED.' + ld_out_message.get("MESSAGE")}
                    return Response(ld_dict)
                else:
                    return Response(logic[1])
            else:
                obj_claim.employee_gid = request.auth.payload.get('user_id')
                emp_bnk = obj_claim.eClaim_entity_get()
                bank_data = json.loads(emp_bnk.get("DATA").to_json(orient='records'))
                entity = bank_data[0].get('entity_gid')

                DETAILS = android.Android.set_data_dtl(self, request)
                DETAILS = android.Android.gid_check(self, DETAILS)
                CHANGE = android.Android.set_data_chng(self, request)
                CHANGE = android.Android.gid_array_check(self, CHANGE)
                common.main_fun1(request.read(), path)
                empid = exp_onbehalf_emp(self, request)
                DETAILS['Entity_Gid'] = entity
                DETAILS['processedby'] = empid
                DETAILS['createby'] = empid
                CHANGE = CHANGE.get('DATA')
                obj_claim.employee_gid = empid
                emp_bnk = obj_claim.eClaim_entity_get()
                bank_data = json.loads(emp_bnk.get("DATA").to_json(orient='records'))
                entity = bank_data[0].get('entity_gid')
                for i in CHANGE:
                    json_param = android.Android.param_conversion(self, i, entity)
                    json_param['Params']['FILTER']['expensegid'] = DETAILS.get('expensegid')
                    ld_dict = locconv_logic(self, empid, json_param)
                    i['eligibleamount'] = ld_dict.get('Eligible_amount')
                logic = verify.localcon.calck_totalamt(self, CHANGE, DETAILS)
                if logic == "True":
                    obj_claim.jsondata = json.dumps(DETAILS)
                    obj_claim.jsonData = json.dumps({"DATA": CHANGE})
                    ld_out_message = obj_claim.eClaim_loccon_set()
                    msg = ld_out_message.get("MESSAGE").split(",")
                    if msg[0] == 'SUCCESS':
                        ld_dict = {"MESSAGE": msg[0]}
                    elif msg[0] == 'FAIL':
                        ld_dict = {"MESSAGE": "FAIL"}
                    else:
                        ld_dict = {"MESSAGE": 'ERROR_OCCURED.' + ld_out_message.get("MESSAGE")}
                    return Response(ld_dict)
                else:
                    return Response(logic[1])
        except Exception as e:
            common.logger.error(e)
            return Response({"MESSAGE": "ERROR_OCCURED", "DATA": str(e), "STATUS": 1})
class Pkgmvg_Get(APIView):
    def get(self, request):
        try:
            obj_eclaim = meClaim.eClaim_Model()
            if request.query_params.get("Api_Type") == "WEB":
                entity = request.query_params.get("Entity_Gid")
                Claimreqgid = request.query_params.get("Claimreqgid")
                obj_eclaim.filter_json = json.dumps({"Entity_Gid": entity, "Claimreqgid": Claimreqgid})
                ld_out_message = obj_eclaim.eClaim_packingmoving_get()
            else:
                filter = android.Android.get_method(self, request)
                obj_eclaim.filter_json = json.dumps(filter)
                ld_out_message = obj_eclaim.eClaim_packingmoving_get()

            if ld_out_message.get("MESSAGE") == 'FOUND':
                dict = json.loads(ld_out_message.get("DATA").to_json(orient='records'))
                ld_dict = {"DATA": dict, "MESSAGE": 'FOUND'}
            elif ld_out_message.get("MESSAGE") == 'NOT_FOUND':
                ld_dict = {"MESSAGE": 'NOT_FOUND'}
            else:
                ld_dict = {"MESSAGE": 'ERROR_OCCURED.' + ld_out_message.get("MESSAGE")}
            return Response(ld_dict)
        except Exception as e:
            common.logger.error(e)
            return Response({"MESSAGE": "ERROR_OCCURED", "DATA": str(e), "STATUS": 1})
class Pkgmvg_Logic(APIView):
    def post(self, request):
        try:
            path = self.request.stream.path
            jsondata = json.loads(request.body.decode('utf-8'))
            common.main_fun1(request.read(), path)
            empid = 0
            if request.query_params.get("Type") == "ONBEHALF":
                empid = jsondata.get('Employee_gid')
            else:
                empid = request.auth.payload.get('user_id')

            obj_claim = meClaim.eClaim_Model()
            obj_claim.employee_gid = empid
            emp_bnk = obj_claim.eClaim_entity_get()
            bank_data = json.loads(emp_bnk.get("DATA").to_json(orient='records'))
            entity_gid = bank_data[0].get('entity_gid')
            json_param = android.Android.param_conversion(self, jsondata, entity_gid)
            eligible = pkgmvg_logic(self,empid,json_param)
            ld_dict = {"DATA": eligible,
                       "MESSAGE": 'FOUND'}
            return Response(ld_dict)
        except Exception as e:
            common.logger.error(e)
            e = "Erro Line no :" + str(format(sys.exc_info()[-1].tb_lineno)) + " " + "Error :" + str(e)
            return Response({"MESSAGE": "ERROR_OCCURED", "DATA": str(e) + str(eligible), "STATUS": 1})
def pkgmvg_logic(self,empid,json_param):
    tourgid = json_param.get('Params').get('FILTER').get('tourgid')
    grade = emp_grade(tourgid)
    eligible_value = verify.pkg_moving.validate_data(self, json_param, grade)
    common.logger.error([{"eligible_value": str(eligible_value)}])
    driverbatta = 0
    daysdrivereng = 0
    traveltimeinhours = ""
    if 'traveltimeinhours' in json_param.get('Params').get('FILTER'):
        traveltimeinhours = json_param.get('Params').get('FILTER').get('traveltimeinhours')
    else:
        traveltimeinhours = ""
    if  traveltimeinhours != "":
        amountandadys = verify.pkg_moving.calck_driverbata(self, json_param, grade)
        common.logger.error([{"amountandadys": str(amountandadys)}])
        if amountandadys != 0:
            if 'driverbatta' in amountandadys and 'daysdrivereng' in amountandadys :
                driverbatta = amountandadys.get("driverbatta")
                daysdrivereng = amountandadys.get("daysdrivereng")
    breakagecharge = verify.pkg_moving.calc_breakage(self, json_param, grade)
    common.logger.error([{"breakagecharge": str(breakagecharge)}])
    eligible = {
        "Eligible_amount": eligible_value,
        "driverbatta": str(driverbatta),
        "daysdrivereng": str(daysdrivereng),
        "breakagecharge": str(breakagecharge)
    }
    common.logger.error([{"eligible": str(eligible)}])
    return eligible
class Pkgmvg(APIView):
    def post(self, request):
        try:
            obj_claim = meClaim.eClaim_Model()
            path = self.request.stream.path
            if request.query_params.get("Api_Type") == "WEB":
                jsondata = json.loads(request.body.decode('utf-8'))
                DETAILS = jsondata.get('Params').get('DETAILS')
                CHANGE = jsondata.get('Params').get('CHANGE').get('DATA')
                common.main_fun1(request.read(), path)
                empid = exp_onbehalf_emp(self, request)
                obj_claim.employee_gid = empid
                emp_bnk = obj_claim.eClaim_entity_get()
                bank_data = json.loads(emp_bnk.get("DATA").to_json(orient='records'))
                entity = bank_data[0].get('entity_gid')
                for i in CHANGE:
                    json_param = android.Android.param_conversion(self, i, entity)
                    json_param['Params']['FILTER']['expensegid'] = DETAILS.get('expensegid')
                    ld_dict = pkgmvg_logic(self, empid, json_param)
                    i['eligibleamount'] = float(ld_dict.get('Eligible_amount'))+float(ld_dict.get('driverbatta'))+float(ld_dict.get('breakagecharge'))
                    i['driverbatta'] = ld_dict.get('driverbatta')
                    i['daysdrivereng'] = ld_dict.get('daysdrivereng')
                    i['eligbreakagecharge'] = ld_dict.get('breakagecharge')
                logic = verify.pkg_moving.calck_totalamt(self, CHANGE, DETAILS)
                if logic == "True":
                    obj_claim.jsondata = json.dumps(DETAILS)
                    obj_claim.jsonData = json.dumps({"DATA": CHANGE})
                    ld_out_message = obj_claim.eClaim_pkgmoving_set()
                    msg = ld_out_message.get("MESSAGE").split(",")
                    if msg[0] == 'SUCCESS':
                        ld_dict = {"MESSAGE": ld_out_message.get("MESSAGE")}
                    elif msg[0] == 'FAIL':
                        ld_dict = {"MESSAGE": "FAIL"}
                    else:
                        ld_dict = {"MESSAGE": 'ERROR_OCCURED.' + ld_out_message.get("MESSAGE")}
                    return Response(ld_dict)
                else:
                    return Response(logic[1])
            else:
                obj_claim.employee_gid = request.auth.payload.get('user_id')
                emp_bnk = obj_claim.eClaim_entity_get()
                bank_data = json.loads(emp_bnk.get("DATA").to_json(orient='records'))
                entity = bank_data[0].get('entity_gid')
                DETAILS = android.Android.set_data_dtl(self, request)
                DETAILS = android.Android.gid_check(self, DETAILS)
                CHANGE = android.Android.set_data_chng(self, request)
                CHANGE = android.Android.gid_array_check(self, CHANGE)
                common.main_fun1(request.read(), path)
                empid = exp_onbehalf_emp(self, request)
                DETAILS['Entity_Gid'] = entity
                DETAILS['processedby'] = empid
                DETAILS['createby'] = empid
                CHANGE = CHANGE.get('DATA')
                obj_claim.employee_gid = empid
                emp_bnk = obj_claim.eClaim_entity_get()
                bank_data = json.loads(emp_bnk.get("DATA").to_json(orient='records'))
                entity = bank_data[0].get('entity_gid')
                for i in CHANGE:
                    json_param = android.Android.param_conversion(self, i, entity)
                    json_param['Params']['FILTER']['expensegid'] = DETAILS.get('expensegid')
                    ld_dict = pkgmvg_logic(self, empid, json_param)
                    i['eligibleamount'] = ld_dict.get('Eligible_amount')
                    i['driverbatta'] = ld_dict.get('driverbatta')
                    i['daysdrivereng'] = ld_dict.get('daysdrivereng')
                    i['breakagecharges'] = ld_dict.get('breakagecharge')
                logic = verify.pkg_moving.calck_totalamt(self, CHANGE, DETAILS)
                if logic == "True":
                    obj_claim.jsondata = json.dumps(DETAILS)
                    obj_claim.jsonData = json.dumps({"DATA": CHANGE})
                    ld_out_message = obj_claim.eClaim_pkgmoving_set()
                    msg = ld_out_message.get("MESSAGE").split(",")
                    if msg[0] == 'SUCCESS':
                        ld_dict = {"MESSAGE": msg[0]}
                    elif msg[0] == 'FAIL':
                        ld_dict = {"MESSAGE": "FAIL"}
                    else:
                        ld_dict = {"MESSAGE": 'ERROR_OCCURED.' + ld_out_message.get("MESSAGE")}
                    return Response(ld_dict)
                else:
                    return Response(logic[1])
        except Exception as e:
            common.logger.error(e)
            return Response({"MESSAGE": "ERROR_OCCURED", "DATA": str(e), "STATUS": 1})
class Incidental_Get(APIView):
    def get(self, request):
        try:
            obj_eclaim = meClaim.eClaim_Model()
            if request.query_params.get("Api_Type") == "WEB":
                entity = request.query_params.get("Entity_Gid")
                Claimreqgid = request.query_params.get("Claimreqgid")
                obj_eclaim.filter_json = json.dumps({"Entity_Gid": entity, "Claimreqgid": Claimreqgid})
                ld_out_message = obj_eclaim.eClaim_incidental_get()
            else:
                filter = android.Android.get_method(self, request)
                obj_eclaim.filter_json = json.dumps(filter)
                ld_out_message = obj_eclaim.eClaim_incidental_get()

            if ld_out_message.get("MESSAGE") == 'FOUND':
                ld_dict = {"DATA": json.loads(ld_out_message.get("DATA").to_json(orient='records')), "MESSAGE": 'FOUND'}
            elif ld_out_message.get("MESSAGE") == 'NOT_FOUND':
                ld_dict = {"MESSAGE": 'NOT_FOUND'}
            else:
                ld_dict = {"MESSAGE": 'ERROR_OCCURED.' + ld_out_message.get("MESSAGE")}
            return Response(ld_dict)
        except Exception as e:
            common.logger.error(e)
            return Response({"MESSAGE": "ERROR_OCCURED", "DATA": str(e), "STATUS": 1})
class Incidental_Logic(APIView):
    def post(self, request):
        try:
            path = self.request.stream.path
            jsondata = json.loads(request.body.decode('utf-8'))
            common.main_fun1(request.read(), path)
            empid = 0
            if request.query_params.get("Type") == "ONBEHALF":
                empid = jsondata.get('Employee_gid')
            else:
                empid = request.auth.payload.get('user_id')

            obj_claim = meClaim.eClaim_Model()
            obj_claim.employee_gid = empid
            emp_bnk = obj_claim.eClaim_entity_get()
            bank_data = json.loads(emp_bnk.get("DATA").to_json(orient='records'))
            entity_gid = bank_data[0].get('entity_gid')
            json_param = android.Android.param_conversion(self, jsondata, entity_gid)
            eligible_value =incidental_logic(self,json_param)
            ld_dict = {"DATA": eligible_value,
                       "MESSAGE": 'FOUND'}
            return Response(ld_dict)
        except Exception as e:
            common.logger.error(e)
            return Response({"MESSAGE": "ERROR_OCCURED", "DATA": str(e), "STATUS": 1})
def incidental_logic(self,json_param):
    amount = verify.incidental.validation(self, json_param)
    eligible_value = {
        "Eligible_amount": amount,
    }
    return eligible_value
class Incidental(APIView):
    def post(self, request):
        try:
            path = self.request.stream.path
            obj_claim = meClaim.eClaim_Model()
            if request.query_params.get("Api_Type") == "WEB":
                jsondata = json.loads(request.body.decode('utf-8'))
                DETAILS = jsondata.get('Params').get('DETAILS')
                CHANGE = jsondata.get('Params').get('CHANGE').get('DATA')
                common.main_fun1(request.read(), path)
                empid = exp_onbehalf_emp(self, request)
                obj_claim.employee_gid = empid
                emp_bnk = obj_claim.eClaim_entity_get()
                bank_data = json.loads(emp_bnk.get("DATA").to_json(orient='records'))
                entity = bank_data[0].get('entity_gid')
                for i in CHANGE:
                    json_param = android.Android.param_conversion(self, i, entity)
                    json_param['Params']['FILTER']['expensegid'] = DETAILS.get('expensegid')
                    ld_dict = incidental_logic(self,json_param)
                    i['eligibleamount'] = ld_dict.get('Eligible_amount')
                logic = verify.incidental.calck_totalamt(self, CHANGE, DETAILS)
                if logic == "True":
                    obj_claim.jsondata = json.dumps(DETAILS)
                    obj_claim.jsonData = json.dumps({"DATA": CHANGE})
                    ld_out_message = obj_claim.eClaim_incidental_set()
                    msg = ld_out_message.get("MESSAGE").split(",")
                    if msg[0] == 'SUCCESS':
                        ld_dict = {"MESSAGE": ld_out_message.get("MESSAGE")}
                    elif msg[0] == 'FAIL':
                        ld_dict = {"MESSAGE": "FAIL"}
                    else:
                        ld_dict = {"MESSAGE": 'ERROR_OCCURED.' + ld_out_message.get("MESSAGE")}
                    return Response(ld_dict)
                else:
                    return Response(logic[1])
            else:
                obj_claim.employee_gid = request.auth.payload.get('user_id')
                emp_bnk = obj_claim.eClaim_entity_get()
                bank_data = json.loads(emp_bnk.get("DATA").to_json(orient='records'))
                entity = bank_data[0].get('entity_gid')
                DETAILS = android.Android.set_data_dtl(self, request)
                DETAILS = android.Android.gid_check(self, DETAILS)
                CHANGE = android.Android.set_data_chng(self, request)
                CHANGE = android.Android.gid_array_check(self, CHANGE)
                common.main_fun1(request.read(), path)
                empid = exp_onbehalf_emp(self, request)
                DETAILS['Entity_Gid'] = entity
                DETAILS['processedby'] = empid
                DETAILS['createby'] = empid
                CHANGE = CHANGE.get('DATA')
                obj_claim.employee_gid = empid
                emp_bnk = obj_claim.eClaim_entity_get()
                bank_data = json.loads(emp_bnk.get("DATA").to_json(orient='records'))
                entity = bank_data[0].get('entity_gid')
                for i in CHANGE:
                    json_param = android.Android.param_conversion(self, i, entity)
                    json_param['Params']['FILTER']['expensegid'] = DETAILS.get('expensegid')
                    ld_dict = incidental_logic(self,json_param)
                    i['eligibleamount'] = ld_dict.get('Eligible_amount')
                logic = verify.incidental.calck_totalamt(self, CHANGE, DETAILS)
                if logic == "True":
                    obj_claim.jsondata = json.dumps(DETAILS)
                    obj_claim.jsonData = json.dumps({"DATA": CHANGE})
                    ld_out_message = obj_claim.eClaim_incidental_set()
                    msg = ld_out_message.get("MESSAGE").split(",")
                    if msg[0] == 'SUCCESS':
                        ld_dict = {"MESSAGE": msg[0]}
                    elif msg[0] == 'FAIL':
                        ld_dict = {"MESSAGE": "FAIL"}
                    else:
                        ld_dict = {"MESSAGE": 'ERROR_OCCURED.' + ld_out_message.get("MESSAGE")}
                    return Response(ld_dict)
                else:
                    return Response(logic[1])
        except Exception as e:
            common.logger.error(e)
            return Response({"MESSAGE": "ERROR_OCCURED", "DATA": str(e), "STATUS": 1})

class Misc_Get(APIView):
    def get(self, request):
        try:
            obj_eclaim = meClaim.eClaim_Model()
            if request.query_params.get("Api_Type") == "WEB":
                entity = request.query_params.get("Entity_Gid")
                Claimreqgid = request.query_params.get("Claimreqgid")
                obj_eclaim.filter_json = json.dumps({"Entity_Gid": entity, "Claimreqgid": Claimreqgid})
                ld_out_message = obj_eclaim.eClaim_miscellaneous_get()
            else:
                filter = android.Android.get_method(self, request)
                obj_eclaim.filter_json = json.dumps(filter)
                ld_out_message = obj_eclaim.eClaim_miscellaneous_get()

            if ld_out_message.get("MESSAGE") == 'FOUND':
                ld_dict = {"DATA": json.loads(ld_out_message.get("DATA").to_json(orient='records')), "MESSAGE": 'FOUND'}
            elif ld_out_message.get("MESSAGE") == 'NOT_FOUND':
                ld_dict = {"MESSAGE": 'NOT_FOUND'}
            else:
                ld_dict = {"MESSAGE": 'ERROR_OCCURED.' + ld_out_message.get("MESSAGE")}
            return Response(ld_dict)
        except Exception as e:
            common.logger.error(e)
            return Response({"MESSAGE": "ERROR_OCCURED", "DATA": str(e), "STATUS": 1})
class Misc_Logic(APIView):
    def post(self, request):
        try:
            path = self.request.stream.path
            jsondata = json.loads(request.body.decode('utf-8'))
            common.main_fun1(request.read(), path)
            empid = 0
            if request.query_params.get("Type") == "ONBEHALF":
                empid = jsondata.get('Employee_gid')
            else:
                empid = request.auth.payload.get('user_id')
            obj_claim = meClaim.eClaim_Model()
            obj_claim.employee_gid = empid
            emp_bnk = obj_claim.eClaim_entity_get()
            bank_data = json.loads(emp_bnk.get("DATA").to_json(orient='records'))
            entity_gid = bank_data[0].get('entity_gid')
            json_param = android.Android.param_conversion(self, jsondata, entity_gid)
            eligible_value = misc_logic(self,empid,json_param)
            ld_dict = {"DATA": eligible_value,
                       "MESSAGE": 'FOUND'}
            return Response(ld_dict)
        except Exception as e:
            common.logger.error(e)
            return Response({"MESSAGE": "ERROR_OCCURED", "DATA": str(e), "STATUS": 1})

def misc_logic(self,empid,json_param):
    tourgid = json_param.get('Params').get('FILTER').get('tourgid')
    grade = emp_grade(tourgid)
    amount = verify.miscellaneous.elegibility_data(self, json_param,grade)
    eligible_value = {
        "Eligible_amount": amount,
    }
    return eligible_value
class Misc(APIView):
    def post(self, request):
        try:
            obj_claim = meClaim.eClaim_Model()
            path = self.request.stream.path
            if request.query_params.get("Api_Type") == "WEB":
                jsondata = json.loads(request.body.decode('utf-8'))
                DETAILS = jsondata.get('Params').get('DETAILS')
                CHANGE = jsondata.get('Params').get('CHANGE').get('DATA')
                common.main_fun1(request.read(), path)
                empid = exp_onbehalf_emp(self, request)
                obj_claim.employee_gid = empid
                emp_bnk = obj_claim.eClaim_entity_get()
                bank_data = json.loads(emp_bnk.get("DATA").to_json(orient='records'))
                entity = bank_data[0].get('entity_gid')
                for i in CHANGE:
                    json_param = android.Android.param_conversion(self, i, entity)
                    json_param['Params']['FILTER']['expensegid'] = DETAILS.get('expensegid')
                    ld_dict = misc_logic(self,empid,json_param)
                    i['eligibleamount'] = ld_dict.get('Eligible_amount')
                logic = verify.miscellaneous.validate_data(self, CHANGE, DETAILS)
                if logic == "True":
                    obj_claim.jsondata = json.dumps(DETAILS)
                    obj_claim.jsonData = json.dumps({"DATA": CHANGE})
                    ld_out_message = obj_claim.eClaim_miscellaneous_set()
                    msg = ld_out_message.get("MESSAGE").split(",")
                    if msg[0] == 'SUCCESS':
                        ld_dict = {"MESSAGE": ld_out_message.get("MESSAGE")}
                    elif msg[0] == 'FAIL':
                        ld_dict = {"MESSAGE": "FAIL"}
                    else:
                        ld_dict = {"MESSAGE": 'ERROR_OCCURED.' + ld_out_message.get("MESSAGE")}
                    return Response(ld_dict)
                else:
                    return Response(logic[1])
            else:
                obj_claim.employee_gid = request.auth.payload.get('user_id')
                emp_bnk = obj_claim.eClaim_entity_get()
                bank_data = json.loads(emp_bnk.get("DATA").to_json(orient='records'))
                entity = bank_data[0].get('entity_gid')

                DETAILS = android.Android.set_data_dtl(self, request)
                DETAILS = android.Android.gid_check(self, DETAILS)
                CHANGE = android.Android.set_data_chng(self, request)
                CHANGE = android.Android.gid_array_check(self, CHANGE)
                common.main_fun1(request.read(), path)
                empid = exp_onbehalf_emp(self, request)
                DETAILS['Entity_Gid'] = entity
                DETAILS['processedby'] = empid
                DETAILS['createby'] = empid
                CHANGE = CHANGE.get('DATA')
                obj_claim.employee_gid = empid
                emp_bnk = obj_claim.eClaim_entity_get()
                bank_data = json.loads(emp_bnk.get("DATA").to_json(orient='records'))
                entity = bank_data[0].get('entity_gid')
                for i in CHANGE:
                    json_param = android.Android.param_conversion(self, i, entity)
                    json_param['Params']['FILTER']['expensegid'] = DETAILS.get('expensegid')
                    ld_dict = misc_logic(self,empid,json_param)
                    i['eligibleamount'] = ld_dict.get('Eligible_amount')
                logic = verify.miscellaneous.validate_data(self, CHANGE, DETAILS)
                if logic == "True":
                    obj_claim.jsondata = json.dumps(DETAILS)
                    obj_claim.jsonData = json.dumps({"DATA": CHANGE})
                    ld_out_message = obj_claim.eClaim_miscellaneous_set()
                    msg = ld_out_message.get("MESSAGE").split(",")
                    if msg[0] == 'SUCCESS':
                        ld_dict = {"MESSAGE": msg[0]}
                    elif msg[0] == 'FAIL':
                        ld_dict = {"MESSAGE": "FAIL"}
                    else:
                        ld_dict = {"MESSAGE": 'ERROR_OCCURED.' + ld_out_message.get("MESSAGE")}
                    return Response(ld_dict)
                else:
                    return Response(logic[1])
        except Exception as e:
            common.logger.error(e)
            return Response({"MESSAGE": "ERROR_OCCURED", "DATA": str(e), "STATUS": 1})

class LocalDeputation_Get(APIView):
    def get(self, request):
        try:
            obj_eclaim = meClaim.eClaim_Model()
            if request.query_params.get("Api_Type") == "WEB":
                entity = request.query_params.get("Entity_Gid")
                Claimreqgid = request.query_params.get("Claimreqgid")
                obj_eclaim.filter_json = json.dumps({"Entity_Gid": entity, "Claimreqgid": Claimreqgid})
                ld_out_message = obj_eclaim.eClaim_localdeputation_get()
            else:
                filter = android.Android.get_method(self, request)
                obj_eclaim.filter_json = json.dumps(filter)
                ld_out_message = obj_eclaim.eClaim_localdeputation_get()

            if ld_out_message.get("MESSAGE") == 'FOUND':
                ld_dict = {"DATA": json.loads(ld_out_message.get("DATA").to_json(orient='records')), "MESSAGE": 'FOUND'}
            elif ld_out_message.get("MESSAGE") == 'NOT_FOUND':
                ld_dict = {"MESSAGE": 'NOT_FOUND'}
            else:
                ld_dict = {"MESSAGE": 'ERROR_OCCURED.' + ld_out_message.get("MESSAGE")}
            return Response(ld_dict)
        except Exception as e:
            common.logger.error(e)
            return Response({"MESSAGE": "ERROR_OCCURED", "DATA": str(e), "STATUS": 1})
class LocalDeputation_Logic(APIView):
    def post(self, request):
        try:
            path = self.request.stream.path
            jsondata = json.loads(request.body.decode('utf-8'))
            common.main_fun1(request.read(), path)
            empid = 0
            if request.query_params.get("Type") == "ONBEHALF":
                empid = jsondata.get('Employee_gid')
            else:
                empid = request.auth.payload.get('user_id')
            obj_claim = meClaim.eClaim_Model()
            obj_claim.employee_gid = empid
            emp_bnk = obj_claim.eClaim_entity_get()
            bank_data = json.loads(emp_bnk.get("DATA").to_json(orient='records'))
            entity_gid = bank_data[0].get('entity_gid')
            json_param = android.Android.param_conversion(self, jsondata, entity_gid)
            eligible_value = LocalDeputation_logic(self,empid,json_param)
            ld_dict = {"DATA": eligible_value,
                       "MESSAGE": 'FOUND'}
            return Response(ld_dict)
        except Exception as e:
            common.logger.error(e)
            return Response({"MESSAGE": "ERROR_OCCURED", "DATA": str(e), "STATUS": 1})

def LocalDeputation_logic(self,empid,json_param):
    tourgid = json_param.get('Params').get('FILTER').get('tourgid')
    grade = emp_grade(tourgid)
    amount = verify.local_deputation.elegibility_data(self, json_param,grade)
    return amount

class LocalDeputation(APIView):
    def post(self, request):
        try:
            obj_claim = meClaim.eClaim_Model()
            path = self.request.stream.path
            if request.query_params.get("Api_Type") == "WEB":
                jsondata = json.loads(request.body.decode('utf-8'))
                DETAILS = jsondata.get('Params').get('DETAILS')
                CHANGE = jsondata.get('Params').get('CHANGE').get('DATA')
                common.main_fun1(request.read(), path)
                empid = exp_onbehalf_emp(self, request)
                obj_claim.employee_gid = empid
                emp_bnk = obj_claim.eClaim_entity_get()
                bank_data = json.loads(emp_bnk.get("DATA").to_json(orient='records'))
                entity = bank_data[0].get('entity_gid')
                for i in CHANGE:
                    json_param = android.Android.param_conversion(self, i, entity)
                    json_param['Params']['FILTER']['expensegid'] = DETAILS.get('expensegid')
                    ld_dict = LocalDeputation_logic(self,empid,json_param)
                    i['eligibleamount'] = ld_dict.get('Eligible_amount')
                logic = verify.local_deputation.validate_data(self, CHANGE, DETAILS)
                if logic == "True":
                    obj_claim.jsondata = json.dumps(DETAILS)
                    obj_claim.jsonData = json.dumps({"DATA": CHANGE})
                    ld_out_message = obj_claim.eClaim_localdeputation_set()
                    msg = ld_out_message.get("MESSAGE").split(",")
                    if msg[0] == 'SUCCESS':
                        ld_dict = {"MESSAGE": ld_out_message.get("MESSAGE")}
                    elif msg[0] == 'FAIL':
                        ld_dict = {"MESSAGE": "FAIL"}
                    else:
                        ld_dict = {"MESSAGE": 'ERROR_OCCURED.' + ld_out_message.get("MESSAGE")}
                    return Response(ld_dict)
                else:
                    return Response(logic[1])
            else:
                obj_claim.employee_gid = request.auth.payload.get('user_id')
                emp_bnk = obj_claim.eClaim_entity_get()
                bank_data = json.loads(emp_bnk.get("DATA").to_json(orient='records'))
                entity = bank_data[0].get('entity_gid')

                DETAILS = android.Android.set_data_dtl(self, request)
                DETAILS = android.Android.gid_check(self, DETAILS)
                CHANGE = android.Android.set_data_chng(self, request)
                CHANGE = android.Android.gid_array_check(self, CHANGE)
                common.main_fun1(request.read(), path)
                empid = exp_onbehalf_emp(self, request)
                DETAILS['Entity_Gid'] = entity
                DETAILS['processedby'] = empid
                DETAILS['createby'] = empid
                CHANGE = CHANGE.get('DATA')
                obj_claim.employee_gid = empid
                emp_bnk = obj_claim.eClaim_entity_get()
                bank_data = json.loads(emp_bnk.get("DATA").to_json(orient='records'))
                entity = bank_data[0].get('entity_gid')
                for i in CHANGE:
                    json_param = android.Android.param_conversion(self, i, entity)
                    json_param['Params']['FILTER']['expensegid'] = DETAILS.get('expensegid')
                    ld_dict = LocalDeputation_logic(self,empid,json_param)
                    i['eligibleamount'] = ld_dict.get('Eligible_amount')
                logic = verify.local_deputation.validate_data(self, CHANGE, DETAILS)
                if logic == "True":
                    obj_claim.jsondata = json.dumps(DETAILS)
                    obj_claim.jsonData = json.dumps({"DATA": CHANGE})
                    ld_out_message = obj_claim.eClaim_localdeputation_set()
                    msg = ld_out_message.get("MESSAGE").split(",")
                    if msg[0] == 'SUCCESS':
                        ld_dict = {"MESSAGE": msg[0]}
                    elif msg[0] == 'FAIL':
                        ld_dict = {"MESSAGE": "FAIL"}
                    else:
                        ld_dict = {"MESSAGE": 'ERROR_OCCURED.' + ld_out_message.get("MESSAGE")}
                    return Response(ld_dict)
                else:
                    return Response(logic[1])
        except Exception as e:
            common.logger.error(e)
            return Response({"MESSAGE": "ERROR_OCCURED", "DATA": str(e), "STATUS": 1})

class Expense_delete(APIView):
    def post(self, request):
        try:
            obj_claim = meClaim.eClaim_Model()
            if request.query_params.get("Api_Type") == "WEB":
                jsondata = json.loads(request.body.decode('utf-8'))
                obj_claim.filter_json = json.dumps(jsondata.get('Params').get('FILTER'))
                ld_out_message = obj_claim.eClaim_exp_delete_set()
            else:
                jsondata = json.loads(request.body.decode('utf-8'))
                obj_claim.filter_json = json.dumps(jsondata)
                ld_out_message = obj_claim.eClaim_exp_delete_set()

            if ld_out_message.get("MESSAGE") == 'SUCCESS':
                ld_dict = {"MESSAGE": "SUCCESS", "STATUS": 0}
            elif ld_out_message.get("MESSAGE") == 'FAIL':
                ld_dict = {"MESSAGE": "FAIL", "STATUS": 1}
            else:
                ld_dict = {"MESSAGE": 'ERROR_OCCURED.' + ld_out_message.get("MESSAGE"), "STATUS": 1}
            return Response(ld_dict)
        except Exception as e:
            common.logger.error(e)
            return Response({"MESSAGE": "ERROR_OCCURED", "DATA": str(e), "STATUS": 1})
 #mobile Api
class Tour_Dailydiem_Get(APIView):
    def get(self, request):
        try:
            obj_eclaim = meClaim.eClaim_Model()
            if request.query_params.get("Api_Type") == "WEB":
                entity = request.query_params.get("Entity_Gid")
                Claimreqgid = request.query_params.get("Tourgid")
                obj_eclaim.filter_json = json.dumps({"Entity_Gid": entity, "Tourgid": Claimreqgid})
                ld_out_message = obj_eclaim.eClaim_tour_dailydiem_get()
            else:
                filter = android.Android.get_method(self, request)
                obj_eclaim.filter_json = json.dumps(filter)
                ld_out_message = obj_eclaim.eClaim_tour_dailydiem_get()

            if ld_out_message.get("MESSAGE") == 'FOUND':
                ld_dict = {"DATA": json.loads(ld_out_message.get("DATA").to_json(orient='records')), "MESSAGE": 'FOUND',"STATUS": 0}
            elif ld_out_message.get("MESSAGE") == 'NOT_FOUND':
                ld_dict = {"MESSAGE": 'NOT_FOUND',"STATUS": 1}
            else:
                ld_dict = {"MESSAGE": 'ERROR_OCCURED.' + ld_out_message.get("MESSAGE"),"STATUS": 1}
            return Response(ld_dict)
        except Exception as e:
            common.logger.error(e)
            return Response({"MESSAGE": "ERROR_OCCURED", "DATA": str(e), "STATUS": 1})

class Tour_Travel_Get(APIView):
    def get(self, request):
        try:
            obj_eclaim = meClaim.eClaim_Model()
            if request.query_params.get("Api_Type") == "WEB":
                entity = request.query_params.get("Entity_Gid")
                Claimreqgid = request.query_params.get("Tourgid")
                obj_eclaim.filter_json = json.dumps({"Entity_Gid": entity, "Tourgid": Claimreqgid})
                ld_out_message = obj_eclaim.eClaim_tour_travel_get()
            else:
                filter = android.Android.get_method(self, request)
                obj_eclaim.filter_json = json.dumps(filter)
                ld_out_message = obj_eclaim.eClaim_tour_travel_get()

            if ld_out_message.get("MESSAGE") == 'FOUND':
                ld_dict = {"DATA": json.loads(ld_out_message.get("DATA").to_json(orient='records')), "MESSAGE": 'FOUND',"STATUS": 0}
            elif ld_out_message.get("MESSAGE") == 'NOT_FOUND':
                ld_dict = {"MESSAGE": 'NOT_FOUND',"STATUS": 1}
            else:
                ld_dict = {"MESSAGE": 'ERROR_OCCURED.' + ld_out_message.get("MESSAGE"),"STATUS": 1}
            return Response(ld_dict)
        except Exception as e:
            common.logger.error(e)
            return Response({"MESSAGE": "ERROR_OCCURED", "DATA": str(e), "STATUS": 1})

class Tour_Incidental_Get(APIView):
    def get(self, request):
        try:
            obj_eclaim = meClaim.eClaim_Model()
            if request.query_params.get("Api_Type") == "WEB":
                entity = request.query_params.get("Entity_Gid")
                Claimreqgid = request.query_params.get("Tourgid")
                obj_eclaim.filter_json = json.dumps({"Entity_Gid": entity, "Tourgid": Claimreqgid})
                ld_out_message = obj_eclaim.eClaim_tour_incidental_get()
            else:
                filter = android.Android.get_method(self, request)
                obj_eclaim.filter_json = json.dumps(filter)
                ld_out_message = obj_eclaim.eClaim_tour_incidental_get()

            if ld_out_message.get("MESSAGE") == 'FOUND':
                ld_dict = {"DATA": json.loads(ld_out_message.get("DATA").to_json(orient='records')), "MESSAGE": 'FOUND',"STATUS": 0}
            elif ld_out_message.get("MESSAGE") == 'NOT_FOUND':
                ld_dict = {"MESSAGE": 'NOT_FOUND',"STATUS": 1}
            else:
                ld_dict = {"MESSAGE": 'ERROR_OCCURED.' + ld_out_message.get("MESSAGE"),"STATUS": 1}
            return Response(ld_dict)
        except Exception as e:
            common.logger.error(e)
            return Response({"MESSAGE": "ERROR_OCCURED", "DATA": str(e), "STATUS": 1})

class Tour_Lodging_Get(APIView):
    def get(self, request):
        try:
            obj_eclaim = meClaim.eClaim_Model()
            if request.query_params.get("Api_Type") == "WEB":
                entity = request.query_params.get("Entity_Gid")
                Claimreqgid = request.query_params.get("Tourgid")
                obj_eclaim.filter_json = json.dumps({"Entity_Gid": entity, "Tourgid": Claimreqgid})
                ld_out_message = obj_eclaim.eClaim_tour_lodging_get()
            else:
                filter = android.Android.get_method(self, request)
                obj_eclaim.filter_json = json.dumps(filter)
                ld_out_message = obj_eclaim.eClaim_tour_lodging_get()

            if ld_out_message.get("MESSAGE") == 'FOUND':
                ld_dict = {"DATA": json.loads(ld_out_message.get("DATA").to_json(orient='records')), "MESSAGE": 'FOUND',"STATUS": 0}
            elif ld_out_message.get("MESSAGE") == 'NOT_FOUND':
                ld_dict = {"MESSAGE": 'NOT_FOUND',"STATUS": 1}
            else:
                ld_dict = {"MESSAGE": 'ERROR_OCCURED.' + ld_out_message.get("MESSAGE"),"STATUS": 1}
            return Response(ld_dict)
        except Exception as e:
            common.logger.error(e)
            return Response({"MESSAGE": "ERROR_OCCURED", "DATA": str(e), "STATUS": 1})

class Tour_Loccon_Get(APIView):
    def get(self, request):
        try:
            obj_eclaim = meClaim.eClaim_Model()
            if request.query_params.get("Api_Type") == "WEB":
                entity = request.query_params.get("Entity_Gid")
                Claimreqgid = request.query_params.get("Tourgid")
                obj_eclaim.filter_json = json.dumps({"Entity_Gid": entity, "Tourgid": Claimreqgid})
                ld_out_message = obj_eclaim.eClaim_tour_localconveyence_get()
            else:
                filter = android.Android.get_method(self, request)
                obj_eclaim.filter_json = json.dumps(filter)
                ld_out_message = obj_eclaim.eClaim_tour_localconveyence_get()

            if ld_out_message.get("MESSAGE") == 'FOUND':
                ld_dict = {"DATA": json.loads(ld_out_message.get("DATA").to_json(orient='records')), "MESSAGE": 'FOUND',"STATUS": 0}
            elif ld_out_message.get("MESSAGE") == 'NOT_FOUND':
                ld_dict = {"MESSAGE": 'NOT_FOUND',"STATUS": 1}
            else:
                ld_dict = {"MESSAGE": 'ERROR_OCCURED.' + ld_out_message.get("MESSAGE"),"STATUS": 1}
            return Response(ld_dict)
        except Exception as e:
            common.logger.error(e)
            return Response({"MESSAGE": "ERROR_OCCURED", "DATA": str(e), "STATUS": 1})

class Tour_Pkmvg_Get(APIView):
    def get(self, request):
        try:
            obj_eclaim = meClaim.eClaim_Model()
            if request.query_params.get("Api_Type") == "WEB":
                entity = request.query_params.get("Entity_Gid")
                Claimreqgid = request.query_params.get("Tourgid")
                obj_eclaim.filter_json = json.dumps({"Entity_Gid": entity, "Tourgid": Claimreqgid})
                ld_out_message = obj_eclaim.eClaim_tour_packingmoving_get()
            else:
                filter = android.Android.get_method(self, request)
                obj_eclaim.filter_json = json.dumps(filter)
                ld_out_message = obj_eclaim.eClaim_tour_packingmoving_get()

            if ld_out_message.get("MESSAGE") == 'FOUND':
                ld_dict = {"DATA": json.loads(ld_out_message.get("DATA").to_json(orient='records')), "MESSAGE": 'FOUND',"STATUS": 0}
            elif ld_out_message.get("MESSAGE") == 'NOT_FOUND':
                ld_dict = {"MESSAGE": 'NOT_FOUND',"STATUS": 1}
            else:
                ld_dict = {"MESSAGE": 'ERROR_OCCURED.' + ld_out_message.get("MESSAGE"),"STATUS": 1}
            return Response(ld_dict)
        except Exception as e:
            common.logger.error(e)
            return Response({"MESSAGE": "ERROR_OCCURED", "DATA": str(e), "STATUS": 1})

class Tour_Misc_Get(APIView):
    def get(self, request):
        try:
            obj_eclaim = meClaim.eClaim_Model()
            if request.query_params.get("Api_Type") == "WEB":
                entity = request.query_params.get("Entity_Gid")
                Claimreqgid = request.query_params.get("Tourgid")
                obj_eclaim.filter_json = json.dumps({"Entity_Gid": entity, "Tourgid": Claimreqgid})
                ld_out_message = obj_eclaim.eClaim_tour_misc_get()
            else:
                filter = android.Android.get_method(self, request)
                obj_eclaim.filter_json = json.dumps(filter)
                ld_out_message = obj_eclaim.eClaim_tour_misc_get()

            if ld_out_message.get("MESSAGE") == 'FOUND':
                ld_dict = {"DATA": json.loads(ld_out_message.get("DATA").to_json(orient='records')), "MESSAGE": 'FOUND',"STATUS": 0}
            elif ld_out_message.get("MESSAGE") == 'NOT_FOUND':
                ld_dict = {"MESSAGE": 'NOT_FOUND',"STATUS": 1}
            else:
                ld_dict = {"MESSAGE": 'ERROR_OCCURED.' + ld_out_message.get("MESSAGE"),"STATUS": 1}
            return Response(ld_dict)
        except Exception as e:
            common.logger.error(e)
            return Response({"MESSAGE": "ERROR_OCCURED", "DATA": str(e), "STATUS": 1})

class Recovery_Get(APIView):
    def get(self, request):
        try:
            obj_eclaim = meClaim.eClaim_Model()
            if request.query_params.get("Type") == "ONBEHALF":
                empid = request.query_params.get('Employee_gid')
            else:
                empid = request.auth.payload.get('user_id')
            obj_eclaim.filter_json = json.dumps({"Employee_gid": empid})
            ld_out_message = obj_eclaim.eClaim_Recovery_get()
            if ld_out_message.get("MESSAGE") == 'FOUND':
                ld_dict = {"DATA": json.loads(ld_out_message.get("DATA").to_json(orient='records')), "MESSAGE": 'FOUND',"STATUS": 0}
            elif ld_out_message.get("MESSAGE") == 'NOT_FOUND':
                ld_dict = {"MESSAGE": 'NOT_FOUND',"STATUS": 1}
            else:
                ld_dict = {"MESSAGE": 'ERROR_OCCURED.' + ld_out_message.get("MESSAGE"),"STATUS": 1}
            return Response(ld_dict)
        except Exception as e:
            common.logger.error(e)
            return Response({"MESSAGE": "ERROR_OCCURED", "DATA": str(e), "STATUS": 1})

class AP_Advance_Get(APIView):
    def get(self, request):
        try:
            obj_claim = meClaim.eClaim_Model()
            ld_dict =''
            if request.query_params.get("Api_Type") == "WEB":
                entity = request.query_params.get("Entity_Gid")
                Tour_gid = request.query_params.get("TourGid")
                obj_claim.filter_json = json.dumps({"Entity_Gid": entity, "Tour_gid": Tour_gid})
                ld_out_message = obj_claim.eClaim_touradvance_get()
                out_datas = json.loads(ld_out_message.get("DATA").to_json(orient='records'))
                out_data = json.loads(out_datas[0].get('advance'))
                crnno = []
                for i in out_data:
                    if i.get('crnno') not in crnno and i.get('crnno') != 0:
                        crnno.append(i.get('crnno'))
                emp_data = {
                    "crnno": crnno
                }
                obj_claim.filter_json = json.dumps(emp_data)
                emp_out_message = obj_claim.eClaim_Crnno_advance_get()
                crndata = json.loads(emp_out_message.get("DATA").to_json(orient='records'))
                if emp_out_message.get("MESSAGE") == 'FOUND':
                    for d in range(0,len(crndata)):
                        crndata[d]["advancegid"] = out_data[d].get('gid')
                        crndata[d]["adjustamount"] = out_data[d].get('adjustamount')

                    ld_dict = {"DATA": crndata, "MESSAGE": 'FOUND',"STATUS": 0}
                elif emp_out_message.get("MESSAGE") == 'NOT_FOUND':
                    ld_dict = {"MESSAGE": 'NOT_FOUND', "STATUS": 1}

            else:
                filter = android.Android.get_method(self, request)
                obj_claim.filter_json = json.dumps(filter)
                ld_out_message = obj_claim.eClaim_touradvance_get()
                out_datas = json.loads(ld_out_message.get("DATA").to_json(orient='records'))
                out_data = json.loads(out_datas[0].get('advance'))
                crnno = []
                for i in out_data:
                    if i.get('crnno') not in crnno and i.get('crnno') != 0:
                        crnno.append(i.get('crnno'))
                emp_data = {
                    "crnno": crnno
                }
                obj_claim.filter_json = json.dumps(emp_data)
                emp_out_message = obj_claim.eClaim_Crnno_advance_get()
                crndata = json.loads(emp_out_message.get("DATA").to_json(orient='records'))
                if emp_out_message.get("MESSAGE") == 'FOUND':
                    for d in range(0, len(crndata)):
                        crndata[d]["advancegid"] = out_data[d].get('gid')
                        crndata[d]["adjustamount"] = out_data[d].get('adjustamount')
                    ld_dict = {"DATA": crndata, "MESSAGE": 'FOUND',"STATUS": 0}
                elif emp_out_message.get("MESSAGE") == 'NOT_FOUND':
                    ld_dict = {"MESSAGE": 'NOT_FOUND', "STATUS": 1}

            if ld_dict.get("MESSAGE") == 'FOUND':
                ld_dict = {"DATA": ld_dict.get("DATA"),
                           "MESSAGE": 'FOUND', "STATUS": 0}
            elif ld_dict.get("MESSAGE") == 'NOT_FOUND':
                ld_dict = {"MESSAGE": 'NOT_FOUND', "STATUS": 1}
            else:
                ld_dict = {"MESSAGE": 'ERROR_OCCURED.' + ld_out_message.get("MESSAGE"), "STATUS": 1}
            return Response(ld_dict)
        except Exception as e:
            common.logger.error(e)
            return Response({"MESSAGE": "ERROR_OCCURED", "DATA": str(e), "STATUS": 1})

class Advance_Adjust(APIView):
    def post(self,request):
        try:
            ld_out_message = ""
            path = self.request.stream.path
            jsondata = json.loads(request.body.decode('utf-8'))
            obj_claim = meClaim.eClaim_Model()
            if request.query_params.get("Api_Type") == "WEB":
                obj_claim.jsondata = json.dumps(jsondata.get('Params').get('DETAILS'))
                common.main_fun1(request.read(), path)
                ld_out_message = obj_claim.eClaim_advance_adjust_set()
            else:
                obj_claim.employee_gid = request.auth.payload.get('user_id')
                emp_bnk = obj_claim.eClaim_entity_get()
                bank_data = json.loads(emp_bnk.get("DATA").to_json(orient='records'))
                entity_gid = bank_data[0].get('entity_gid')
                CHANGE = android.Android.set_data_chng(self, request)
                CHANGE = android.Android.gid_array_check(self, CHANGE)
                common.main_fun1(request.read(), path)
                CHANGE['processedby'] = request.auth.payload.get('user_id')
                CHANGE['createby'] = request.auth.payload.get('user_id')
                CHANGE['Entity_Gid'] = entity_gid
                obj_claim.jsondata = json.dumps(CHANGE)
                ld_out_message = obj_claim.eClaim_advance_adjust_set()

            if ld_out_message.get("MESSAGE") == 'SUCCESS':
                ld_dict = {"MESSAGE": "SUCCESS", "STATUS": 0}
            elif ld_out_message.get("MESSAGE") == 'FAIL':
                ld_dict = {"MESSAGE": "FAIL", "STATUS": 1}
            else:
                ld_dict = {"MESSAGE": 'ERROR_OCCURED.' + ld_out_message.get("MESSAGE"), "STATUS": 1}
            return Response(ld_dict)
        except Exception as e:
            common.logger.error(e)
            return Response({"MESSAGE": "ERROR_OCCURED", "DATA": str(e),"STATUS":1})
class Advance_Recovery(APIView):
    def post(self,request):
        try:
            ld_out_message = ""
            ld_dict =""
            path = self.request.stream.path
            jsondata = json.loads(request.body.decode('utf-8'))
            obj_claim = meClaim.eClaim_Model()
            if request.query_params.get("Api_Type") == "WEB":
                obj_claim.jsondata = json.dumps(jsondata.get('Params').get('DETAILS'))
                common.main_fun1(request.read(), path)
                data = verify.ecf_reverse_entry.jv_entry(self,request,jsondata)
                if data.get("MESSAGE")[0] == 'SUCCESS':
                    ld_dict = {"MESSAGE": "SUCCESS", "STATUS": 0}
                elif data.get("MESSAGE")[0] == 'FAIL':
                    ld_dict = {"MESSAGE": "FAIL", "STATUS": 1}
                else:
                    return Response(data)
                return Response(ld_dict)
            else:
                obj_claim.employee_gid = request.auth.payload.get('user_id')
                emp_bnk = obj_claim.eClaim_entity_get()
                bank_data = json.loads(emp_bnk.get("DATA").to_json(orient='records'))
                entity_gid = bank_data[0].get('entity_gid')
                CHANGE = android.Android.set_data_chng(self, request)
                CHANGE = android.Android.gid_array_check(self, CHANGE)
                common.main_fun1(request.read(), path)
                CHANGE['processedby'] = request.auth.payload.get('user_id')
                CHANGE['createby'] = request.auth.payload.get('user_id')
                CHANGE['Entity_Gid'] = entity_gid
                obj_claim.jsondata = json.dumps(CHANGE)
                data = verify.ecf_reverse_entry.jv_entry(self, request, jsondata)
                if data.get("MESSAGE")[0] == 'SUCCESS':
                    ld_dict = {"MESSAGE": "SUCCESS", "STATUS": 0}
                elif data.get("MESSAGE")[0] == 'FAIL':
                    ld_dict = {"MESSAGE": "FAIL", "STATUS": 1}
                else:
                    return Response(data)
                return Response(ld_dict)

            if ld_out_message.get("MESSAGE") == 'SUCCESS':
                ld_dict = {"MESSAGE": "SUCCESS", "STATUS": 0}
            elif ld_out_message.get("MESSAGE") == 'FAIL':
                ld_dict = {"MESSAGE": "FAIL", "STATUS": 1}
            else:
                ld_dict = {"MESSAGE": 'ERROR_OCCURED.' + ld_out_message.get("MESSAGE"), "STATUS": 1}
            return Response(ld_dict)
        except Exception as e:
            common.logger.error(e)
            return Response({"MESSAGE": "ERROR_OCCURED", "DATA": str(e),"STATUS":1})

class Ongoing_Tour(APIView):
    def post(self,request):
        try:
            path = self.request.stream.path
            ld_out_message = ""
            if request.query_params.get("Api_Type") =="WEB":
                jsondata = json.loads(request.body.decode('utf-8'))
                common.main_fun1(request.read(), path)
                obj_eclaim = meClaim.eClaim_Model()
                filter = jsondata.get('Params').get('FILTER')
                if 'tourdate' not in filter:
                    obj_eclaim.date = 'DATE'
                    date = obj_eclaim.get_server_date()
                    filter['tourdate'] = date
                obj_eclaim.filter_json = json.dumps(filter)
                ld_out_message = obj_eclaim.eClaim_ongoingtour_get()
            else:
                filter = android.Android.post_summary(self,request)
                common.main_fun1(request.read(), path)
                obj_eclaim = meClaim.eClaim_Model()
                if 'tourdate' not in filter:
                    obj_eclaim.date ='DATE'
                    date = obj_eclaim.get_server_date()
                    filter['tourdate'] = date
                obj_eclaim.filter_json = json.dumps(filter)
                ld_out_message = obj_eclaim.eClaim_ongoingtour_get()
            if ld_out_message.get("MESSAGE") == 'FOUND':
                out_data = json.loads(ld_out_message.get("DATA").to_json(orient='records'))
                data = []
                for d in out_data:
                    if 'Total_Row' in d:
                        pass
                    else :
                        d['Total_Row'] = len(out_data)
                    tmp={}
                    tmp['gid'] = d.get('gid')
                    tmp['requestno'] = d.get('requestno')
                    tmp['requestdate'] = d.get('requestdate')
                    tmp['empgid'] = d.get('empgid')
                    tmp['empgrade'] = d.get('empgrade')
                    tmp['tourreason'] = d.get('name')
                    tmp['startdate'] = d.get('startdate')
                    tmp['enddate'] = d.get('enddate')
                    tmp['enddate'] = d.get('enddate')
                    tmp['tourstatus'] = d.get('tourstatus')
                    tmp['approvedby'] = d.get('approvedby')
                    tmp['Total_Row'] = d.get('Total_Row')
                    data.append(tmp)
                permit_gid = []
                emp_gid = data[0].get('empgid')

                for i in data:
                    if i.get('approvedby') not in permit_gid and i.get('approvedby') != 0:
                        permit_gid.append(i.get('approvedby'))
                emp_data = {
                    "empids" : emp_gid
                }
                obj_eclaim.filter_json = json.dumps(emp_data)
                obj_eclaim.json_classification = json.dumps({})
                emp_out_message = obj_eclaim.eClaim_employee_get()
                employee_data = json.loads(emp_out_message.get("DATA").to_json(orient='records'))
                if len(employee_data) == 0:
                    ld_dict = {"MESSAGE": 'NOT_FOUND', "STATUS": 1}
                    return Response(ld_dict)
                empprmit_data = {
                    "empids": permit_gid
                }
                obj_eclaim.filter_json = json.dumps(empprmit_data)
                obj_eclaim.json_classification = json.dumps({})
                permit_out_message = obj_eclaim.eClaim_employee_get()
                permit_data = json.loads(permit_out_message.get("DATA").to_json(orient='records'))
                if len(permit_data) == 0:
                    ld_dict = {"MESSAGE": 'NOT_FOUND', "STATUS": 1}
                    return Response(ld_dict)

                for d in data:
                    d["employee_name"] = employee_data[0].get('employee_name')
                    d["employee_code"] = employee_data[0].get('employee_code')
                    d["employee_designation"] = employee_data[0].get('designation_name')
                for d in data:
                    for i in range(0, len(permit_data)):
                        if permit_data[i].get('employee_gid') == int(d.get('approvedby')):
                            d["permit_byname"] = permit_data[i].get('employee_name')
                            d["permit_bycode"] = permit_data[i].get('employee_code')
                            break

                ld_dict = {"DATA": data,"MESSAGE": 'FOUND',"STATUS":0}
            elif ld_out_message.get("MESSAGE") == 'NOT_FOUND':
                ld_dict = {"MESSAGE": 'NOT_FOUND',"STATUS":1}
            else:
                ld_dict = {"MESSAGE": 'ERROR_OCCURED.' + ld_out_message.get("MESSAGE"),"STATUS":1}
            return Response(ld_dict)
        except Exception as e:
            common.logger.error(e)
            return Response({"MESSAGE": "ERROR_OCCURED", "DATA": str(e),"STATUS":1})

class Expense_amount(APIView):
    def get(self, request):
        try:
            obj_eclaim = meClaim.eClaim_Model()
            empid = request.auth.payload.get('user_id')
            Tour_gid = request.query_params.get("TourGid")
            obj_eclaim.filter_json = json.dumps({"Employee_gid": empid,"tourgid":Tour_gid})
            ld_out_message = obj_eclaim.eClaim_Expense_Amount_get()
            if ld_out_message.get("MESSAGE") == 'FOUND':
                ld_dict = {"DATA": json.loads(ld_out_message.get("DATA").to_json(orient='records')),
                           "MESSAGE": 'FOUND',"STATUS": 0}
            elif ld_out_message.get("MESSAGE") == 'NOT_FOUND':
                ld_dict = {"MESSAGE": 'NOT_FOUND',"STATUS": 1}
            else:
                ld_dict = {"MESSAGE": 'ERROR_OCCURED.' + ld_out_message.get("MESSAGE"),"STATUS": 1}
            return Response(ld_dict)
        except Exception as e:
            common.logger.error(e)
            return Response({"MESSAGE": "ERROR_OCCURED", "DATA": str(e), "STATUS": 1})

class Tour_Report_Summary(APIView):
    def post(self,request):
        try:
            path = self.request.stream.path
            ld_out_message = ""
            if request.query_params.get("Api_Type") =="WEB":
                jsondata = json.loads(request.body.decode('utf-8'))
                common.main_fun1(request.read(), path)
                obj_eclaim = meClaim.eClaim_Model()
                obj_eclaim.filter_json = json.dumps(jsondata.get('Params').get('FILTER'))
                ld_out_message = obj_eclaim.eClaim_tourrequest_report_get()
            else:
                jsondata = json.loads(request.body.decode('utf-8'))
                common.main_fun1(request.read(), path)
                obj_eclaim = meClaim.eClaim_Model()
                obj_eclaim.filter_json = json.dumps(jsondata)
                ld_out_message = obj_eclaim.eClaim_tourrequest_report_get()
            if ld_out_message.get("MESSAGE") == 'FOUND':
                out_data = json.loads(ld_out_message.get("DATA").to_json(orient='records'))
                data = []
                for d in out_data:
                    if 'Total_Row' in d:
                        pass
                    else :
                        d['Total_Row'] = len(out_data)
                    tmp={}
                    tmp['gid'] = d.get('gid')
                    tmp['requestno'] = d.get('requestno')
                    tmp['requestdate'] = d.get('requestdate')
                    tmp['empgid'] = d.get('empgid')
                    tmp['empgrade'] = d.get('empgrade')
                    tmp['tourreason'] = d.get('name')
                    tmp['startdate'] = d.get('startdate')
                    tmp['enddate'] = d.get('enddate')
                    tmp['enddate'] = d.get('enddate')
                    tmp['tourstatus'] = d.get('tourstatus')
                    tmp['claimstatus'] = d.get('claimstatus')
                    tmp['advancestatus'] = d.get('advancestatus')
                    tmp['approvedby'] = d.get('approvedby')
                    tmp['advanceamt'] = d.get('advanceamt')
                    tmp['expenseamt'] = d.get('expenseamt')
                    tmp['Total_Row'] = d.get('Total_Row')
                    data.append(tmp)
                permit_gid = []
                emp_gid = data[0].get('empgid')

                for i in data:
                    if i.get('approvedby') not in permit_gid and i.get('approvedby') != 0:
                        permit_gid.append(i.get('approvedby'))
                emp_data = {
                    "empids" : emp_gid
                }
                obj_eclaim.filter_json = json.dumps(emp_data)
                obj_eclaim.json_classification = json.dumps({})
                emp_out_message = obj_eclaim.eClaim_employee_get()
                employee_data = json.loads(emp_out_message.get("DATA").to_json(orient='records'))
                if len(employee_data) == 0:
                    ld_dict = {"MESSAGE": 'NOT_FOUND', "STATUS": 1}
                    return Response(ld_dict)
                empprmit_data = {
                    "empids": permit_gid
                }
                obj_eclaim.filter_json = json.dumps(empprmit_data)
                obj_eclaim.json_classification = json.dumps({})
                permit_out_message = obj_eclaim.eClaim_employee_get()
                permit_data = json.loads(permit_out_message.get("DATA").to_json(orient='records'))
                if len(permit_data) == 0:
                    ld_dict = {"MESSAGE": 'NOT_FOUND', "STATUS": 1}
                    return Response(ld_dict)

                for d in data:
                    d["employee_name"] = employee_data[0].get('employee_name')
                    d["employee_code"] = employee_data[0].get('employee_code')
                    d["employee_designation"] = employee_data[0].get('designation_name')
                    d["branch_name"] = employee_data[0].get('branch_name')
                    d["branch_code"] = employee_data[0].get('branch_code')
                for d in data:
                    for i in range(0, len(permit_data)):
                        if permit_data[i].get('employee_gid') == int(d.get('approvedby')):
                            d["permit_byname"] = permit_data[i].get('employee_name')
                            d["permit_bycode"] = permit_data[i].get('employee_code')
                            break

                ld_dict = {"DATA": data,"MESSAGE": 'FOUND',"STATUS":0}
            elif ld_out_message.get("MESSAGE") == 'NOT_FOUND':
                ld_dict = {"MESSAGE": 'NOT_FOUND',"STATUS":1}
            else:
                ld_dict = {"MESSAGE": 'ERROR_OCCURED.' + ld_out_message.get("MESSAGE"),"STATUS":1}
            return Response(ld_dict)
        except Exception as e:
            common.logger.error(e)
            return Response({"MESSAGE": "ERROR_OCCURED", "DATA": str(e),"STATUS":1})

class Tour_Report_Download(APIView):
    def post(self,request):
        try:
            path = self.request.stream.path
            ld_out_message = ""
            if request.query_params.get("Api_Type") =="WEB":
                jsondata = json.loads(request.body.decode('utf-8'))
                common.main_fun1(request.read(), path)
                obj_eclaim = meClaim.eClaim_Model()
                obj_eclaim.filter_json = json.dumps(jsondata.get('Params').get('FILTER'))
                ld_out_message = obj_eclaim.eClaim_tourrequest_report_get()
            else:
                jsondata = json.loads(request.body.decode('utf-8'))
                common.main_fun1(request.read(), path)
                obj_eclaim = meClaim.eClaim_Model()
                obj_eclaim.filter_json = json.dumps(jsondata)
                ld_out_message = obj_eclaim.eClaim_tourrequest_report_get()
            if ld_out_message.get("MESSAGE") == 'FOUND':
                out_data = json.loads(ld_out_message.get("DATA").to_json(orient='records'))
                data = []
                for d in out_data:
                    if 'Total_Row' in d:
                        pass
                    else :
                        d['Total_Row'] = len(out_data)
                    tmp={}
                    tmp['gid'] = d.get('gid')
                    tmp['requestno'] = d.get('requestno')
                    tmp['requestdate'] = d.get('requestdate')
                    tmp['empgid'] = d.get('empgid')
                    tmp['empgrade'] = d.get('empgrade')
                    tmp['tourreason'] = d.get('name')
                    tmp['startdate'] = d.get('startdate')
                    tmp['enddate'] = d.get('enddate')
                    tmp['tourstatus'] = d.get('tourstatus')
                    tmp['claimstatus'] = d.get('claimstatus')
                    tmp['advancestatus'] = d.get('advancestatus')
                    tmp['approvedby'] = d.get('approvedby')
                    tmp['advanceamt'] = d.get('advanceamt')
                    tmp['expenseamt'] = d.get('expenseamt')
                    tmp['Total_Row'] = d.get('Total_Row')
                    data.append(tmp)
                permit_gid = []
                emp_gid = data[0].get('empgid')

                for i in data:
                    if i.get('approvedby') not in permit_gid and i.get('approvedby') != 0:
                        permit_gid.append(i.get('approvedby'))
                emp_data = {
                    "empids" : emp_gid
                }
                obj_eclaim.filter_json = json.dumps(emp_data)
                obj_eclaim.json_classification = json.dumps({})
                emp_out_message = obj_eclaim.eClaim_employee_get()
                employee_data = json.loads(emp_out_message.get("DATA").to_json(orient='records'))
                if len(employee_data) == 0:
                    ld_dict = {"MESSAGE": 'NOT_FOUND', "STATUS": 1}
                    return Response(ld_dict)
                empprmit_data = {
                    "empids": permit_gid
                }
                obj_eclaim.filter_json = json.dumps(empprmit_data)
                obj_eclaim.json_classification = json.dumps({})
                permit_out_message = obj_eclaim.eClaim_employee_get()
                permit_data = json.loads(permit_out_message.get("DATA").to_json(orient='records'))
                if len(permit_data) == 0:
                    ld_dict = {"MESSAGE": 'NOT_FOUND', "STATUS": 1}
                    return Response(ld_dict)

                for d in data:
                    d["employee_name"] = employee_data[0].get('employee_name')
                    d["employee_code"] = employee_data[0].get('employee_code')
                    d["employee_designation"] = employee_data[0].get('designation_name')
                    d["branch_name"] = employee_data[0].get('branch_name')
                    d["branch_code"] = employee_data[0].get('branch_code')
                for d in data:
                    for i in range(0, len(permit_data)):
                        if permit_data[i].get('employee_gid') == int(d.get('approvedby')):
                            d["permit_byname"] = permit_data[i].get('employee_name')
                            d["permit_bycode"] = permit_data[i].get('employee_code')
                            break

                d1 = json.dumps(data)
                response_data = pd.read_json(d1)
                # grn_dtl = pd.DataFrame(rows, columns=columns)
                XLSX_MIME = 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
                response = HttpResponse(content_type=XLSX_MIME)
                response['Content-Disposition'] = 'attachment; filename="TA_Report.xlsx"'
                writer = pd.ExcelWriter(response, engine='xlsxwriter')
                final_df = response_data[
                    ['employee_code','employee_name','employee_designation','branch_name','branch_code',
                     'requestno', 'tourreason','requestdate',  'startdate', 'enddate',
                     'expenseamt','advanceamt','claimstatus']]
                final_df.columns = ['Employee Code','Employee Name','Employee Designation','Branch Name','Branch Code',
                                    'Tour NO', 'Tour Reason', 'Tour Request Date',  'Start Date', 'End Date',
                                    'Total Claim Amount','Total Advance Amount','Claim Status']
                final_df.to_excel(writer, index=False)
                writer.save()
                return HttpResponse(response)
                # ld_dict = {"DATA": data,"MESSAGE": 'FOUND',"STATUS":0}
            elif ld_out_message.get("MESSAGE") == 'NOT_FOUND':
                ld_dict = {"MESSAGE": 'NOT_FOUND',"STATUS":1}
                return Response(ld_dict)
            else:
                ld_dict = {"MESSAGE": 'ERROR_OCCURED.' + ld_out_message.get("MESSAGE"),"STATUS":1}
                return Response(ld_dict)
        except Exception as e:
            common.logger.error(e)
            return Response({"MESSAGE": "ERROR_OCCURED", "DATA": str(e),"STATUS":1})

class TourDetail_Report_Download(APIView):
    def get(self,request):
        try:
            obj_claim = meClaim.eClaim_Model()
            emp_gid = request.auth.payload.get('user_id')
            obj_claim.employee_gid = emp_gid
            emp_bnk = obj_claim.eClaim_entity_get()
            bank_data = json.loads(emp_bnk.get("DATA").to_json(orient='records'))
            entity = bank_data[0].get('entity_gid')
            Tour_Gid = request.query_params.get("Tour_Gid")
            obj_claim.filter_json = json.dumps(
                {"Employee_gid": emp_gid, "Entity_Gid": entity, "Tour_Gid": Tour_Gid})
            out_data = obj_claim.eClaim_tourdetails_get()
            if out_data.get("MESSAGE") == 'FOUND':
                data = json.loads(out_data.get("DATA").to_json(orient='records'))
                out_data = []
                for d in data:
                    # tmp['tourdetails'] = json.loads(d.get('tourdetails'))
                    for i in json.loads(d.get('tourdetails')):
                        i['requestno'] = d.get('requestno')
                        i['requestdate'] = d.get('requestdate')
                        i['tourreason'] = d.get('name')
                        i['tourstartdate'] = d.get('startdate')
                        i['tourenddate'] = d.get('enddate')
                        i['permittedby'] = d.get('permittedby')
                        i['approvedby'] = d.get('approvedby')
                        i['empgid'] = d.get('empgid')
                        out_data.append(i)
                emp_gid = []
                emp_data = {
                    "empids": out_data[0].get('empgid')
                }
                obj_claim.filter_json = json.dumps(emp_data)
                obj_claim.json_classification = json.dumps({})
                emp_out_message = obj_claim.eClaim_employee_get()
                employee_data = json.loads(emp_out_message.get("DATA").to_json(orient='records'))
                for d in out_data:
                    d["employee_name"] = employee_data[0].get('employee_name')
                    d["employee_code"] = employee_data[0].get('employee_code')
                permit_data = {
                    "empids": out_data[0].get('permittedby')
                }
                obj_claim.filter_json = json.dumps(permit_data)
                obj_claim.json_classification = json.dumps({})
                permit_out_message = obj_claim.eClaim_employee_get()
                permitemp_data = json.loads(permit_out_message.get("DATA").to_json(orient='records'))
                for d in out_data:
                    d["permit_empname"] = permitemp_data[0].get('employee_name')
                    d["permit_empcode"] = permitemp_data[0].get('employee_code')

                approval_data = {
                    "empids": out_data[0].get('approvedby')
                }
                obj_claim.filter_json = json.dumps(approval_data)
                obj_claim.json_classification = json.dumps({})
                approval_out_message = obj_claim.eClaim_employee_get()
                approval_data = json.loads(approval_out_message.get("DATA").to_json(orient='records'))
                if approval_data != []:
                    for d in out_data:
                        d["approval_empname"] = approval_data[0].get('employee_name')
                        d["approval_empcode"] = approval_data[0].get('employee_code')
                        d["approval_branch"] = approval_data[0].get('branch_name')

                # d1 = json.loads(out_data[0].get('tourdetails'))
                d1 = json.dumps(out_data)
                response_data = pd.read_json(d1)
                # grn_dtl = pd.DataFrame(rows, columns=columns)
                XLSX_MIME = 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
                response = HttpResponse(content_type=XLSX_MIME)
                response['Content-Disposition'] = 'attachment; filename="TA_Report.xlsx"'
                writer = pd.ExcelWriter(response, engine='xlsxwriter')

                final_df = response_data[['requestno','requestdate','tourreason','tourstartdate','tourenddate','employee_name','employee_code','permit_empname','permit_empcode',
                  'startdate','enddate','startingpoint','placeofvisit','purposeofvisit','approval_empname','approval_empcode']]
                final_df.columns = ['Tour NO', 'Tour Request Date', 'Tour Reason', 'Tour Start Date', 'Tour End Date',
                                    'Employee Name', 'Employee Code', 'Permitted By Name', 'Permitted By Code',
                                    'Tour Detail Start Date','Tour Detail End Date','Starting Point','Place of Visit',
                                    'Purpose of Visit','Approver Name','Approver Code']
                final_df.to_excel(writer, index=False)
                writer.save()
                return HttpResponse(response)
                # ld_dict = {"DATA": data,"MESSAGE": 'FOUND',"STATUS":0}
            elif out_data.get("MESSAGE") == 'NOT_FOUND':
                ld_dict = {"MESSAGE": 'NOT_FOUND', "STATUS": 1}
            else:
                ld_dict = {"MESSAGE": 'ERROR_OCCURED.' + out_data.get("MESSAGE"), "STATUS": 1}
            return Response(ld_dict)
        except Exception as e:
            common.logger.error(e)
            return Response({"MESSAGE": "ERROR_OCCURED", "DATA": str(e),"STATUS":1})

class TourExpense_Report_Download(APIView):
    def get(self,request):
        try:
            obj_eclaim = meClaim.eClaim_Model()
            emp_gid = request.auth.payload.get('user_id')
            obj_eclaim.employee_gid = emp_gid
            emp_bnk = obj_eclaim.eClaim_entity_get()
            bank_data = json.loads(emp_bnk.get("DATA").to_json(orient='records'))
            entity = bank_data[0].get('entity_gid')
            Claimrequest_Tourgid = request.query_params.get("Tour_Gid")
            obj_eclaim.filter_json = json.dumps(
                {"Entity_Gid": entity, "Claimrequest_Tourgid": Claimrequest_Tourgid})
            ld_out_message = obj_eclaim.eClaim_claimedexpense_get()
            if ld_out_message.get("MESSAGE") == 'FOUND':
                out_data = json.loads(ld_out_message.get("DATA").to_json(orient='records'))
                emp_data = {
                    "empids": out_data[0].get('empgid')
                }
                obj_eclaim.filter_json = json.dumps(emp_data)
                obj_eclaim.json_classification = json.dumps({})
                emp_out_message = obj_eclaim.eClaim_employee_get()
                employee1_data = json.loads(emp_out_message.get("DATA").to_json(orient='records'))
                for d in out_data:
                    d["employee_name"] = employee1_data[0].get('employee_name')
                    d["employee_code"] = employee1_data[0].get('employee_code')
                    d["employee_designation"] = employee1_data[0].get('designation_name')
                if out_data[0].get('approvedby') != 0:
                    emp_data = {
                        "empids": out_data[0].get('approvedby')
                    }
                    obj_eclaim.filter_json = json.dumps(emp_data)
                    obj_eclaim.json_classification = json.dumps({})
                    emp_out_message = obj_eclaim.eClaim_employee_get()
                    employee1_data = json.loads(emp_out_message.get("DATA").to_json(orient='records'))
                    for d in out_data:
                        d["forwarder_name"] = employee1_data[0].get('employee_name')
                        d["forwarder_code"] = employee1_data[0].get('employee_code')
                        d["forwarder_branch"] = employee1_data[0].get('branch_name')
                else:
                    for d in out_data:
                        d["forwarder_name"] = ''
                        d["forwarder_code"] = ''
                        d["forwarder_branch"] = ''

                if out_data[0].get('approvedby_fr') != 0:
                    emp_data = {
                        "empids": out_data[0].get('approvedby_fr')
                    }
                    obj_eclaim.filter_json = json.dumps(emp_data)
                    obj_eclaim.json_classification = json.dumps({})
                    emp_out_message = obj_eclaim.eClaim_employee_get()
                    employee_data = json.loads(emp_out_message.get("DATA").to_json(orient='records'))
                    if employee_data != []:
                        for d in out_data:
                            d["approver_name"] = employee_data[0].get('employee_name')
                            d["approver_code"] = employee_data[0].get('employee_code')
                            d["approver_branch"] = employee_data[0].get('branch_name')
                else:
                    for d in out_data:
                        d["approver_name"] = ''
                        d["approver_code"] = ''
                        d["approver_branch"] = ''

                d1 = json.dumps(out_data)
                response_data = pd.read_json(d1)
                # grn_dtl = pd.DataFrame(rows, columns=columns)
                XLSX_MIME = 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
                response = HttpResponse(content_type=XLSX_MIME)
                response['Content-Disposition'] = 'attachment; filename="TA_Report.xlsx"'
                writer = pd.ExcelWriter(response, engine='xlsxwriter')
                final_df = response_data[
                    ['requestno', 'requestdate', 'tourreason', 'startdate', 'enddate', 'employee_name',
                     'employee_code', 'employee_designation', 'expsensecode', 'description',
                     'requestorcomment','claimedamount','eligibleamount','approvedamount','appcomment',
                     'forwarder_name','forwarder_code','approver_name','approver_code']]
                final_df.columns = ['Tour NO', 'Tour Request Date', 'Tour Reason', 'Start Date', 'End Date',
                                    'Employee Name', 'Employee Code', 'Employee Designation','Expsense Code',
                                    'Description','Requestor Comment','Claimed Amount','Eligible Amount','Approved Amount','Approver Comment',
                                    'Forwarder Name','Forwarder Code','Approver Name','Approver Code']
                final_df.to_excel(writer, index=False)
                writer.save()
                return HttpResponse(response)
                # ld_dict = {"DATA": data,"MESSAGE": 'FOUND',"STATUS":0}
            elif ld_out_message.get("MESSAGE") == 'NOT_FOUND':
                ld_dict = {"MESSAGE": 'NOT_FOUND',"STATUS":1}
                return Response(ld_dict)
            else:
                ld_dict = {"MESSAGE": 'ERROR_OCCURED.' + ld_out_message.get("MESSAGE"),"STATUS":1}
                return Response(ld_dict)
        except Exception as e:
            common.logger.error(e)
            return Response({"MESSAGE": "ERROR_OCCURED", "DATA": str(e),"STATUS":1})

class TournoExpense_Report(APIView):
    def get(self,request):
        try:
            obj_eclaim = meClaim.eClaim_Model()
            emp_gid = request.auth.payload.get('user_id')
            Tourno = request.query_params.get("Tour_no")
            obj_eclaim.filter_json = json.dumps(
                {"tourno": Tourno})
            ld_out_message = obj_eclaim.eClaim_tournoexpense_get()
            if ld_out_message.get("MESSAGE") == 'FOUND':
                out_data = json.loads(ld_out_message.get("DATA").to_json(orient='records'))
                emp_data = {
                    "empids": out_data[0].get('empgid')
                }
                obj_eclaim.filter_json = json.dumps(emp_data)
                obj_eclaim.json_classification = json.dumps({})
                emp_out_message = obj_eclaim.eClaim_employee_get()
                employee1_data = json.loads(emp_out_message.get("DATA").to_json(orient='records'))
                for d in out_data:
                    d["employee_name"] = employee1_data[0].get('employee_name')
                    d["employee_code"] = employee1_data[0].get('employee_code')
                    d["employee_designation"] = employee1_data[0].get('designation_name')
                    d["employee_branch_name"] = employee1_data[0].get('branch_name')

                ld_dict = {"DATA": out_data,"MESSAGE": 'FOUND',"STATUS":0}
                return Response(ld_dict)
            elif ld_out_message.get("MESSAGE") == 'NOT_FOUND':
                ld_dict = {"MESSAGE": 'NOT_FOUND',"STATUS":1}
                return Response(ld_dict)
            else:
                ld_dict = {"MESSAGE": 'ERROR_OCCURED.' + ld_out_message.get("MESSAGE"),"STATUS":1}
                return Response(ld_dict)
        except Exception as e:
            common.logger.error(e)
            return Response({"MESSAGE": "ERROR_OCCURED", "DATA": str(e),"STATUS":1})

class Branch_Wise_Count(APIView):
    def get(self,request):
        try:
            obj_eclaim = meClaim.eClaim_Model()
            emp_gid = request.auth.payload.get('user_id')
            Type = request.query_params.get("Type")
            if Type == "SELF":
                obj_eclaim.employee_gid = emp_gid
                obj_eclaim.date = 'DATE'
                date = obj_eclaim.get_server_date()
                obj_eclaim.filter_json = json.dumps(
                    {"employeegid": emp_gid, "todaydate": date})
            elif Type == "OTHER"  :
                obj_eclaim.employee_gid = emp_gid
                obj_eclaim.date = 'DATE'
                date = obj_eclaim.get_server_date()
                obj_eclaim.filter_json = json.dumps(
                    {"todaydate": date})
            ld_out_message = obj_eclaim.eClaim_branch_wisecount_get()
            if ld_out_message.get("MESSAGE") == 'FOUND':
                out_data = json.loads(ld_out_message.get("DATA").to_json(orient='records'))
                finaldata = []
                emp_data = {
                    "empids": emp_gid
                }
                obj_eclaim.filter_json = json.dumps(emp_data)
                emp_bnk = obj_eclaim.eClaim_employeebnk_get()
                bank_data = json.loads(emp_bnk.get("DATA").to_json(orient='records'))
                entity_gid = bank_data[0].get('entity_gid')
                # out_data = [{"empbranchgid":259,"datacount":'[0,9,10,14,15,16,17,20,21,22,23,24,26,27,28,29,30,35,36,37,38,39,40,41,42,48,52,54,56,57,59,61,62,63,64,65,66,68,70,71,72,75,76,77,78,79,80,82,83,84,86,87,89,90,91,93,94,96,97,99,100,101,103,104,105,106,108,109,110,111,112,113,114,117,118,119,120,122,124,125,127,129,131,133,134,135,136,138,141,150,156,157,159]'}]
                for i in out_data:
                    branch = i.get('empbranchgid')
                    data = json.loads(i.get('datacount'))
                    onetotwo = 0
                    threetoten = 0
                    eleventothirty = 0
                    thirtyonetosixty = 0
                    more = 0
                    onetotwo_tmp = []
                    threetoten_tmp = []
                    eleventothirty_tmp = []
                    thirtyonetosixty_tmp = []
                    more_tmp = []
                    tmp = {}
                    if len(data) !=0:
                        for j in data:
                            if int(j.get('diff')) <=2 :
                                onetotwo += 1
                                onetotwo_data = {"requestno":j.get('requestno')}
                                onetotwo_tmp.append(onetotwo_data)
                            elif 3 <= int(j.get('diff')) <=10 :
                                threetoten += 1
                                threetoten_data = {"requestno": j.get('requestno')}
                                threetoten_tmp.append(threetoten_data)
                            elif 11 <= int(j.get('diff')) <=30 :
                                eleventothirty += 1
                                eleventothirty_data = {"requestno": j.get('requestno')}
                                eleventothirty_tmp.append(eleventothirty_data)
                            elif 31 <= int(j.get('diff')) <=60 :
                                thirtyonetosixty += 1
                                thirtyonetosixty_data = {"requestno": j.get('requestno')}
                                thirtyonetosixty_tmp.append(thirtyonetosixty_data)
                            else:
                                more += 1
                                more_data = {"requestno": j.get('requestno')}
                                more_tmp.append(more_data)
                    data_branch = verify.branch_apicall(self, request,entity_gid, branch)
                    tmp.update(data_branch[0])
                    onetotwo_dict= {"count":onetotwo,
                                    "data": onetotwo_tmp}
                    tmp['onetotwo']= onetotwo_dict
                    a = threetoten - onetotwo
                    if a <0:
                        tt = 0
                    else :
                        tt = a
                    threetoten_dict = {"count": tt,
                                       "data": threetoten_tmp}
                    tmp['threetoten']= threetoten_dict
                    b = eleventothirty -threetoten
                    if b < 0:
                        et = 0
                    else:
                        et = b
                    eleventothirty_dict = {"count": et,
                                           "data": eleventothirty_tmp}
                    tmp['eleventothirty']= eleventothirty_dict
                    c = thirtyonetosixty -eleventothirty
                    if c < 0:
                        te = 0
                    else:
                        te = c
                    thirtyonetosixty_dict = {"count": te,
                                             "data": thirtyonetosixty_tmp}
                    tmp['thirtyonetosixty']= thirtyonetosixty_dict
                    d = more - thirtyonetosixty
                    if d < 0:
                        mt = 0
                    else:
                        mt = d
                    more_dict = {"count": mt,
                                 "data": more_tmp}
                    tmp['more']= more_dict
                    finaldata.append(tmp)
                ld_dict = {"DATA": finaldata,"MESSAGE": 'FOUND',"STATUS":0}
                return Response(ld_dict)
            elif ld_out_message.get("MESSAGE") == 'NOT_FOUND':
                ld_dict = {"MESSAGE": 'NOT_FOUND',"STATUS":1}
                return Response(ld_dict)
            else:
                ld_dict = {"MESSAGE": 'ERROR_OCCURED.' + ld_out_message.get("MESSAGE"),"STATUS":1}
                return Response(ld_dict)
        except Exception as e:
            common.logger.error(e)
            return Response({"MESSAGE": "ERROR_OCCURED", "DATA": str(e),"STATUS":1})
class Allowance(APIView):
    def get(self,request):
        try:
            obj_eclaim = meClaim.eClaim_Model()
            query = request.query_params
            filter= {}
            if dict(query) != {}:
                for key, value in query.items():
                    filter[key] = value
            obj_eclaim.filter_json = json.dumps(filter)
            ld_out_message = obj_eclaim.eClaim_allowance_summary_get()
            if ld_out_message.get("MESSAGE") == 'FOUND':
                out_data = json.loads(ld_out_message.get("DATA").to_json(orient='records'))
                ld_dict = {"DATA": out_data,"MESSAGE": 'FOUND',"STATUS":0}
                return Response(ld_dict)
            elif ld_out_message.get("MESSAGE") == 'NOT_FOUND':
                ld_dict = {"MESSAGE": 'NOT_FOUND',"STATUS":1}
                return Response(ld_dict)
            else:
                ld_dict = {"MESSAGE": 'ERROR_OCCURED.' + ld_out_message.get("MESSAGE"),"STATUS":1}
                return Response(ld_dict)
        except Exception as e:
            common.logger.error(e)
            return Response({"MESSAGE": "ERROR_OCCURED", "DATA": str(e),"STATUS":1})
    def post(self,request):
        try:
            ld_out_message = ""
            obj_eclaim = meClaim.eClaim_Model()
            emp_gid = request.auth.payload.get('user_id')
            if request.FILES:
                # name = "file"
                # for j in request.FILES.getlist(name):
                contents = request.FILES['file']
                # file_name_new =j.name
                df = pd.read_excel(contents)
                df['Effectivefrom'] = df['Effectivefrom'].dt.strftime('%Y-%m-%d')
                df['Effectiveto'] = df['Effectiveto'].dt.strftime('%Y-%m-%d')
                # entitygid = df['Entitygid']
                # createdby = df['Createdby']
                df = pd.DataFrame(
                    {'gid': df['Gid'], 'expensegid': df['Expensegid'], 'salarygrade': df['Salarygrade'],
                     'city': df['City'], "amount": df['Amount'], "applicableto": df['Applicableto'], "effectivefrom": df['Effectivefrom'],
                     "effectiveto": df['Effectiveto'],"entitygid":df['Entitygid'],"createdby":df['Createdby'],"status":df['Status']})
                ff = df.to_dict('records')
                obj_eclaim.jsondata = json.dumps({"DATA":ff})
                ld_out_message = obj_eclaim.eClaim_allowance_set()

            else :
                jsondata = json.loads(request.body.decode('utf-8'))
                obj_eclaim.jsondata = json.dumps({"DATA": jsondata})
                ld_out_message = obj_eclaim.eClaim_allowance_set()
            if ld_out_message.get("MESSAGE") == 'SUCCESS':
                ld_dict = {"MESSAGE": "SUCCESS", "STATUS": 0}
            elif ld_out_message.get("MESSAGE") == 'FAIL':
                ld_dict = {"MESSAGE": "FAIL", "STATUS": 1}
            else:
                ld_dict = {"MESSAGE": 'ERROR_OCCURED.' + ld_out_message.get("MESSAGE"), "STATUS": 1}
            return Response(ld_dict)
        except Exception as e:
            common.logger.error(e)
            return Response({"MESSAGE": "ERROR_OCCURED", "DATA": str(e),"STATUS":1})

class Tour_Relaxation(APIView):
    def get(self,request):
        try:
            obj_eclaim = meClaim.eClaim_Model()
            query = request.query_params
            filter= {}
            if dict(query) != {}:
                for key, value in query.items():
                    filter[key] = value
            obj_eclaim.filter_json = json.dumps(filter)
            ld_out_message = obj_eclaim.eClaim_tourrelaxation_summary_get()
            if ld_out_message.get("MESSAGE") == 'FOUND':
                out_data = json.loads(ld_out_message.get("DATA").to_json(orient='records'))
                emp_data =[]
                for i in out_data:
                    if i.get('empgid') not in emp_data:
                        emp_data.append(i.get('empgid'))
                empprmit_data = {
                    "empids": emp_data
                }
                obj_eclaim.filter_json = json.dumps(empprmit_data)
                obj_eclaim.json_classification = json.dumps({})
                emp_out_message = obj_eclaim.eClaim_employee_get()
                emp_data = json.loads(emp_out_message.get("DATA").to_json(orient='records'))
                common.logger.error([{"emp_out_message": str(emp_data)}])
                if len(emp_data) == 0:
                    ld_dict = {"MESSAGE": 'NOT_FOUND', "STATUS": 1}
                    return Response(ld_dict)

                for d in out_data:
                    for i in range(0, len(emp_data)):
                        if emp_data[i].get('employee_gid') == int(d.get('empgid')):
                            d["employee_name"] = emp_data[i].get('employee_name')
                            d["employee_code"] = emp_data[i].get('employee_code')
                            d["employee_designation"] = emp_data[i].get('designation_name')
                            break
                common.logger.error([{"data2": str(out_data)}])
                ld_dict = {"DATA": out_data, "MESSAGE": 'FOUND', "STATUS": 0}
                return Response(ld_dict)
            elif ld_out_message.get("MESSAGE") == 'NOT_FOUND':
                ld_dict = {"MESSAGE": 'NOT_FOUND',"STATUS":1}
                return Response(ld_dict)
            else:
                ld_dict = {"MESSAGE": 'ERROR_OCCURED.' + ld_out_message.get("MESSAGE"),"STATUS":1}
                return Response(ld_dict)
        except Exception as e:
            common.logger.error(e)
            return Response({"MESSAGE": "ERROR_OCCURED", "DATA": str(e),"STATUS":1})
    def post(self,request):
        try:
            ld_out_message = ""
            obj_eclaim = meClaim.eClaim_Model()
            emp_gid = request.auth.payload.get('user_id')
            jsondata = json.loads(request.body.decode('utf-8'))
            jsondata['createby'] = emp_gid
            obj_eclaim.jsondata = json.dumps(jsondata)
            ld_out_message = obj_eclaim.eClaim_tourrelaxation_set()
            if ld_out_message.get("MESSAGE") == 'SUCCESS':
                ld_dict = {"MESSAGE": "SUCCESS", "STATUS": 0}
            elif ld_out_message.get("MESSAGE") == 'FAIL':
                ld_dict = {"MESSAGE": "FAIL", "STATUS": 1}
            else:
                ld_dict = {"MESSAGE": 'ERROR_OCCURED.' + ld_out_message.get("MESSAGE"), "STATUS": 1}
            return Response(ld_dict)
        except Exception as e:
            common.logger.error(e)
            return Response({"MESSAGE": "ERROR_OCCURED", "DATA": str(e),"STATUS":1})


class Dependent_Details(APIView):
    def get(self,request):
        try:
            obj_claim = meClaim.eClaim_Model()
            if request.query_params.get("Type") == "ONBEHALF":
                employee_gid = request.query_params.get("Employee_gid")
            else:
                employee_gid = request.auth.payload.get('user_id')
            emp_gid = []
            emp_gid.append(employee_gid)
            emp_data = {
                "empids": emp_gid
            }
            obj_claim.filter_json = json.dumps(emp_data)
            obj_claim.json_classification = json.dumps({})
            emp_out_message = obj_claim.eClaim_employee_get()
            employee_data = json.loads(emp_out_message.get("DATA").to_json(orient='records'))
            common.logger.error([{"employee_data": str(employee_data)}])
            employee_code = employee_data[0].get('employee_code')
            # employee_code = "003443"
            if employee_code[0:2].upper() == 'VS':
                obj_claim.employee_gid = employee_gid
                out_data = obj_claim.eClaim_emptodependent_get()
                outdata = json.loads(out_data.get("DATA").to_json(orient='records'))
                if outdata != []:
                    data_dependent = outdata
                    for i in data_dependent:
                        i['employee_gid'] = employee_gid
                    ld_dict = {"DATA": data_dependent, "MESSAGE": 'FOUND'}
                    return Response(ld_dict)
                elif outdata == []:
                    ld_dict = {"MESSAGE": 'NOT_FOUND', "STATUS": 1}
                    return Response(ld_dict)

            else:
                token_status = 1
                generated_token_data = master_views.master_sync_Data_("GET", "get_data", employee_gid)
                log_data = generated_token_data
                token = generated_token_data.get("DATA")[0].get("clienttoken_name")
                if (token == " " or token == None):
                    token_status = 0
                if token_status == 1:
                    try:
                        client_api = common.clientapi()
                        apiname = common.Apiname()
                        apipassword = common.ApiPassword()
                        headers = {"Content-Type": "application/json", "Authorization": "Bearer " + token}
                        data_depent = {
                            "UserName": apiname,
                            "Password": apipassword,
                            "EmpId": str(employee_code),
                            "DtlsToBeFetch": "DependentDetails"
                        }
                        data_depent = json.dumps(data_depent)
                        result2 = requests.post("" + client_api + "/next/v1/mw/employee-detail", headers=headers,
                                               data=data_depent,
                                               verify=False)
                        results_data2 = json.loads(result2.content.decode("utf-8"))
                        status2 = results_data2.get("out_msg").get("ErrorMessage")
                        if (status2 == "Success"):
                            data_dependent = results_data2.get("out_msg").get('item')
                            for i in data_dependent:
                                i['employee_gid'] = employee_gid
                                i['dependentname'] = i.get('FamilyMemberName')
                                i['deprelation'] = i.get('FamilyMemberRelation')
                                i['dependentid'] = i.get('FamilyMemberId')
                            ld_dict = {"DATA": data_dependent,
                                       "MESSAGE": 'FOUND'}
                            return Response(ld_dict)

                        else:
                            return Response({"MESSAGE": "FAILED", "FAILED_STATUS": results_data2})
                    except Exception as e:
                        common.logger.error(e)
                        return Response({"MESSAGE": "ERROR_OCCURED_ON_AMOUNT_TRANSFER_CLINET_API", "DATA": str(e),
                                         "log_data": log_data})
        except Exception as e:
            common.logger.error(e)
            return Response({"MESSAGE": "ERROR_OCCURED", "DATA": str(e),"STATUS":1})
    def post(self,request):
        try:
            ld_out_message = ""
            obj_eclaim = meClaim.eClaim_Model()
            emp_gid = request.auth.payload.get('user_id')
            jsondata = json.loads(request.body.decode('utf-8'))
            jsondata['createby'] = emp_gid
            obj_eclaim.jsondata = json.dumps(jsondata)
            ld_out_message = obj_eclaim.eClaim_tourrelaxation_set()
            if ld_out_message.get("MESSAGE") == 'SUCCESS':
                ld_dict = {"MESSAGE": "SUCCESS", "STATUS": 0}
            elif ld_out_message.get("MESSAGE") == 'FAIL':
                ld_dict = {"MESSAGE": "FAIL", "STATUS": 1}
            else:
                ld_dict = {"MESSAGE": 'ERROR_OCCURED.' + ld_out_message.get("MESSAGE"), "STATUS": 1}
            return Response(ld_dict)
        except Exception as e:
            common.logger.error(e)
            return Response({"MESSAGE": "ERROR_OCCURED", "DATA": str(e),"STATUS":1})

class Glmapping(APIView):
    def get(self,request):
        try:
            obj_eclaim = meClaim.eClaim_Model()
            emp_gid = request.auth.payload.get('user_id')
            obj_eclaim.employee_gid = emp_gid
            obj_eclaim.date = 'DATE'
            date = obj_eclaim.get_server_date()
            obj_eclaim.filter_json = json.dumps(
                {"employeegid": emp_gid, "todaydate": date})
            ld_out_message = obj_eclaim.eClaim_branch_wisecount_get()
            if ld_out_message.get("MESSAGE") == 'FOUND':
                out_data = json.loads(ld_out_message.get("DATA").to_json(orient='records'))
                finaldata = []
                emp_data = {
                    "empids": emp_gid
                }
                obj_eclaim.filter_json = json.dumps(emp_data)
                emp_bnk = obj_eclaim.eClaim_employeebnk_get()
                bank_data = json.loads(emp_bnk.get("DATA").to_json(orient='records'))
                entity_gid = bank_data[0].get('entity_gid')
                for i in out_data:
                    branch = i.get('empbranchgid')
                    data = json.loads(i.get('datacount'))
                    onetotwo = 0
                    threetoten = 0
                    eleventothirty = 0
                    thirtyonetosixty = 0
                    more = 0
                    tmp = {}
                    for j in data:
                        if int(j) <=2 :
                            onetotwo += 1
                        elif 3 <= int(j) <=10 :
                            threetoten += 1
                        elif 11 <= int(j) <=30 :
                            eleventothirty += 1
                        elif 31 <= int(j) <=60 :
                            thirtyonetosixty += 1
                        else:
                            more += 1
                    data_branch = verify.branch_apicall(self, request,entity_gid, branch)
                    tmp.update(data_branch[0])
                    tmp['onetotwo']= onetotwo
                    tmp['threetoten']= threetoten
                    tmp['eleventothirty']= eleventothirty
                    tmp['thirtyonetosixty']= thirtyonetosixty
                    tmp['more']= more
                    finaldata.append(tmp)
                ld_dict = {"DATA": finaldata,"MESSAGE": 'FOUND',"STATUS":0}
                return Response(ld_dict)
            elif ld_out_message.get("MESSAGE") == 'NOT_FOUND':
                ld_dict = {"MESSAGE": 'NOT_FOUND',"STATUS":1}
                return Response(ld_dict)
            else:
                ld_dict = {"MESSAGE": 'ERROR_OCCURED.' + ld_out_message.get("MESSAGE"),"STATUS":1}
                return Response(ld_dict)
        except Exception as e:
            common.logger.error(e)
            return Response({"MESSAGE": "ERROR_OCCURED", "DATA": str(e),"STATUS":1})
class Gradeeligibility(APIView):
    def get(self,request):
        try:
            obj_eclaim = meClaim.eClaim_Model()
            emp_gid = request.auth.payload.get('user_id')
            obj_eclaim.employee_gid = emp_gid
            obj_eclaim.date = 'DATE'
            date = obj_eclaim.get_server_date()
            obj_eclaim.filter_json = json.dumps(
                {"employeegid": emp_gid, "todaydate": date})
            ld_out_message = obj_eclaim.eClaim_branch_wisecount_get()
            if ld_out_message.get("MESSAGE") == 'FOUND':
                out_data = json.loads(ld_out_message.get("DATA").to_json(orient='records'))
                finaldata = []
                emp_data = {
                    "empids": emp_gid
                }
                obj_eclaim.filter_json = json.dumps(emp_data)
                emp_bnk = obj_eclaim.eClaim_employeebnk_get()
                bank_data = json.loads(emp_bnk.get("DATA").to_json(orient='records'))
                entity_gid = bank_data[0].get('entity_gid')
                for i in out_data:
                    branch = i.get('empbranchgid')
                    data = json.loads(i.get('datacount'))
                    onetotwo = 0
                    threetoten = 0
                    eleventothirty = 0
                    thirtyonetosixty = 0
                    more = 0
                    tmp = {}
                    for j in data:
                        if int(j) <=2 :
                            onetotwo += 1
                        elif 3 <= int(j) <=10 :
                            threetoten += 1
                        elif 11 <= int(j) <=30 :
                            eleventothirty += 1
                        elif 31 <= int(j) <=60 :
                            thirtyonetosixty += 1
                        else:
                            more += 1
                    data_branch = verify.branch_apicall(self, request,entity_gid, branch)
                    tmp.update(data_branch[0])
                    tmp['onetotwo']= onetotwo
                    tmp['threetoten']= threetoten
                    tmp['eleventothirty']= eleventothirty
                    tmp['thirtyonetosixty']= thirtyonetosixty
                    tmp['more']= more
                    finaldata.append(tmp)
                ld_dict = {"DATA": finaldata,"MESSAGE": 'FOUND',"STATUS":0}
                return Response(ld_dict)
            elif ld_out_message.get("MESSAGE") == 'NOT_FOUND':
                ld_dict = {"MESSAGE": 'NOT_FOUND',"STATUS":1}
                return Response(ld_dict)
            else:
                ld_dict = {"MESSAGE": 'ERROR_OCCURED.' + ld_out_message.get("MESSAGE"),"STATUS":1}
                return Response(ld_dict)
        except Exception as e:
            common.logger.error(e)
            return Response({"MESSAGE": "ERROR_OCCURED", "DATA": str(e),"STATUS":1})

class Ccbs_Set(APIView):
    def post(self,request):
        try:
            ld_out_message = ""
            path = self.request.stream.path
            jsondata = json.loads(request.body.decode('utf-8'))
            obj_claim = meClaim.eClaim_Model()
            if request.query_params.get("Api_Type") == "WEB":
                empgid = request.auth.payload.get('user_id')
                data = jsondata.get('Params').get('CCBS')
                for i in data :
                    i['createby'] = empgid
                obj_claim.jsondata = json.dumps({"CCBS":data})
                common.main_fun1(request.read(), path)
                ld_out_message = obj_claim.eClaim_ccbs_set()

            if ld_out_message.get("MESSAGE") == 'SUCCESS':
                ld_dict = {"MESSAGE": "SUCCESS", "STATUS": 0}
            elif ld_out_message.get("MESSAGE") == 'FAIL':
                ld_dict = {"MESSAGE": "FAIL", "STATUS": 1}
            else:
                ld_dict = {"MESSAGE": 'ERROR_OCCURED.' + ld_out_message.get("MESSAGE"), "STATUS": 1}
            return Response(ld_dict)
        except Exception as e:
            common.logger.error(e)
            return Response({"MESSAGE": "ERROR_OCCURED", "DATA": str(e),"STATUS":1})

from Bigflow.Core import views as master_views
class HRD_Employee_Data(APIView):
    def get(self, request):
        try:
            obj_claim = meClaim.eClaim_Model()
            if request.query_params.get("Type") == "ONBEHALF":
                employee_gid = request.query_params.get("Employee_gid")
            else:
                employee_gid = request.auth.payload.get('user_id')
            emp_gid = []
            emp_gid.append(employee_gid)
            emp_data = {
                "empids": emp_gid
            }
            obj_claim.filter_json = json.dumps(emp_data)
            obj_claim.json_classification = json.dumps({})
            emp_out_message = obj_claim.eClaim_employee_get()
            employee_data = json.loads(emp_out_message.get("DATA").to_json(orient='records'))
            employee_code = employee_data[0].get('employee_code')

            if employee_code[0:2].upper() == 'VS':
                obj_claim.employee_gid = employee_gid
                emp_bnk = obj_claim.eClaim_entity_get()
                bank_data = json.loads(emp_bnk.get("DATA").to_json(orient='records'))
                if len(bank_data) != 0:
                    entity = bank_data[0].get('entity_gid')
                    emp_gid = []
                    emp_gid.append(employee_gid)
                    emp_data = {
                        "empids": emp_gid
                    }
                    obj_claim.filter_json = json.dumps(emp_data)
                    obj_claim.json_classification = json.dumps({"Entity_Gid": entity})
                    emp_out_message = obj_claim.eClaim_employee_get()
                    employee_data = json.loads(emp_out_message.get("DATA").to_json(orient='records'))
                    designation = obj_claim.eClaim_empgrade_get()
                    designation = json.loads(designation.get("DATA").to_json(orient='records'))
                    for i in employee_data:
                        for j in designation:
                            if i.get('designation_name').upper() == j.get('designation').upper():
                                i['grade'] = j.get('grade')
                                break

                    employee = employee_data[0]
                    employee['entity_gid'] = bank_data[0].get('entity_gid')
                    ld_dict = {"DATA": employee,
                               "MESSAGE": 'FOUND'}
                else:
                    ld_dict = {"MESSAGE": 'NOT FOUND'}
            else:
                token_status = 1
                generated_token_data = master_views.master_sync_Data_("GET", "get_data", employee_gid)
                log_data = generated_token_data
                token = generated_token_data.get("DATA")[0].get("clienttoken_name")
                if (token == " " or token == None):
                    token_status = 0
                if token_status == 1:
                    try:
                        client_api = common.clientapi()
                        headers = {"Content-Type": "application/json", "Authorization": "Bearer " + token}
                        data = {
                            "UserName": "EMCUSER",
                            "Password": "9f",
                            "EmpId": str(employee_code),
                            "DtlsToBeFetch": "BaseDetails"
                        }
                        data = json.dumps(data)
                        result = requests.post("" + client_api + "/next/v1/mw/employee-detail", headers=headers,
                                               data=data,
                                               verify=False)
                        results_data = json.loads(result.content.decode("utf-8"))
                        status = results_data.get("out_msg").get("ErrorMessage")
                        if (status == "Success"):
                            data = results_data.get("out_msg")
                            data_depent = {
                                "UserName": "EMCUSER",
                                "Password": "9f",
                                "EmpId": str(employee_code),
                                "DtlsToBeFetch": "DependentDetails"
                            }
                            data_depent = json.dumps(data_depent)
                            result2 = requests.post("" + client_api + "/next/v1/mw/employee-detail", headers=headers,
                                                    data=data_depent,
                                                    verify=False)
                            results_data2 = json.loads(result2.content.decode("utf-8"))
                            status2 = results_data2.get("out_msg").get("ErrorMessage")
                            if (status2 == "Success"):
                                data_dependent = results_data2.get("out_msg")
                                push_data = {
                                    "Employee_gid": employee_gid,
                                    "Base_details": data,
                                    "Dependent_details": data_dependent,
                                    "processedby": employee_gid
                                }
                                obj_claim.jsonData = json.dumps(push_data)
                                hrd_set = obj_claim.eClaim_hrd_employeedtl_set()
                                if hrd_set.get("MESSAGE") == 'SUCCESS':
                                    obj_claim.employee_gid = employee_gid
                                    emp_bnk = obj_claim.eClaim_entity_get()
                                    bank_data = json.loads(emp_bnk.get("DATA").to_json(orient='records'))
                                    if len(bank_data) != 0:
                                        entity = bank_data[0].get('entity_gid')
                                        emp_gid = []
                                        emp_gid.append(employee_gid)
                                        emp_data = {
                                            "empids": emp_gid
                                        }
                                        obj_claim.filter_json = json.dumps(emp_data)
                                        obj_claim.json_classification = json.dumps({"Entity_Gid": entity})
                                        emp_out_message = obj_claim.eClaim_employee_get()
                                        employee_data = json.loads(
                                            emp_out_message.get("DATA").to_json(orient='records'))
                                        employee = employee_data[0]
                                        employee['designation_name'] = data.get('edesig')
                                        employee['grade'] = data.get('egrade2')
                                        employee['entity_gid'] = bank_data[0].get('entity_gid')
                                        ld_dict = {"DATA": employee,
                                                   "MESSAGE": 'FOUND'}
                                        return Response(ld_dict)
                                    else:
                                        ld_dict = {"MESSAGE": 'NOT FOUND'}
                                        return Response(ld_dict)
                                else:
                                    ld_dict = {"MESSAGE": 'ERROR_OCCURED.' + hrd_set.get("MESSAGE"), "STATUS": 1}
                            else:
                                return Response({"MESSAGE": "FAILED", "FAILED_STATUS": results_data2})
                        else:
                            return Response({"MESSAGE": "FAILED", "FAILED_STATUS": results_data})
                    except Exception as e:
                        common.logger.error(e)
                        return Response({"MESSAGE": "ERROR_OCCURED_ON_AMOUNT_TRANSFER_CLINET_API", "DATA": str(e),
                                         "log_data": log_data})
                else:
                    return Response({"MESSAGE": "ERROR_OCCURED_ON_TOKEN_GENERATIONS OR INVALID AUTHENTICATONS"})
        except Exception as e:
            common.logger.error(e)
            return Response({"MESSAGE": "ERROR_OCCURED", "DATA": str(e), "STATUS": 1})
