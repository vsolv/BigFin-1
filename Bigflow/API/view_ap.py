
# from barcode import EAN13
from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework.views import Response
import json
from Bigflow.AP.model import mAP
from Bigflow.Core import models as core_models
from Bigflow.Core import views as master_views
import requests
from Bigflow.Core import models as common
ip = common.localip()
import boto3
import barcode
# from barcode.writer import ImageWriter
# from num2words import num2words
# from camelcase import CamelCase
from rest_framework.decorators import authentication_classes, permission_classes
from rest_framework.permissions import AllowAny
import Bigflow.Core.class1 as core_calss1
import re
from Bigflow.settings import S3_BUCKET_NAME


class Emp_Bank_Details(APIView):
    def post(self, request):
        try:
            if self.request.query_params.get("Group") == "SET_EMP_BANK":
                jsondata = json.loads(request.body.decode('utf-8'))
                obj_ap = mAP.ap_model()
                obj_ap.action = self.request.query_params.get("Action")
                obj_ap.type = self.request.query_params.get("Type")
                obj_ap.sub_type = self.request.query_params.get("Sub_Type")
                obj_ap.employee_gid = self.request.query_params.get("Employee_Gid")
                obj_ap.jsondata = json.dumps(jsondata.get('Params').get('DETAILS'))
                obj_ap.json_classification = json.dumps(jsondata.get('Params').get('CLASSIFICATION'))
                ld_out_message = obj_ap.set_emp_bank()
                if ld_out_message.get("MESSAGE") == 'SUCCESS':
                    ld_dict = {"MESSAGE": "SUCCESS"}
                elif ld_out_message.get("MESSAGE") == 'FAIL':
                    ld_dict = {"MESSAGE": "FAIL"}
                else:
                    ld_dict = {"MESSAGE": 'ERROR_OCCURED.' + ld_out_message.get("MESSAGE")}
                return Response(ld_dict)
            elif self.request.query_params.get("Group") == "GET_EMP_BANK":
                jsondata = json.loads(request.body.decode('utf-8'))
                obj_ap = mAP.ap_model()
                obj_ap.type = self.request.query_params.get("Type")
                obj_ap.sub_type = self.request.query_params.get("Sub_Type")
                obj_ap.filter_json = json.dumps(jsondata.get('Params').get('FILTER'))
                obj_ap.json_classification = json.dumps(jsondata.get('Params').get('CLASSIFICATION'))
                ld_out_message = obj_ap.get_emp_bank()
                if ld_out_message.get("MESSAGE") == 'FOUND':
                    ld_dict = {"DATA": json.loads(ld_out_message.get("DATA").to_json(orient='records')),
                               "MESSAGE": 'FOUND'}
                elif ld_out_message.get("MESSAGE") == 'NOT_FOUND':
                    ld_dict = {"MESSAGE": 'NOT_FOUND'}
                else:
                    ld_dict = {"MESSAGE": 'ERROR_OCCURED.' + ld_out_message.get("MESSAGE")}
                return Response(ld_dict)
        except Exception as e:
            common.logger.error(e)
            return Response({"MESSAGE": "ERROR_OCCURED", "DATA": str(e)})



class AP_Bank_API(APIView):
    def post(self, request):
        log_data=[]
        try:
            if self.request.query_params.get("Action") == "SET" and self.request.query_params.get("Type")=="NEFT":
                jsondata = json.loads(request.body.decode('utf-8'))
                Emp_gid=jsondata.get("Params").get("classification").get("Emp_gid")
                data=jsondata.get("Params").get("filter")

                log_data = [{"BEFORE_PAYEMENT_API_DATA": data}]
                common.logger.error(log_data)

                data=json.dumps(data)
                token_status=1
                generated_token_data=master_views.master_sync_Data_("GET","get_data",Emp_gid)
                token=generated_token_data.get("DATA")[0].get("clienttoken_name")
                if(token==" " or token==None):
                    token_status=0
                if token_status==1:
                    client_api = common.clientapi()
                    headers = {"Content-Type": "application/json", "Authorization": "Bearer " + token}
                    result = requests.post("" + client_api + "/nbfc//v1/mwr/payment", headers=headers,data=data,verify=False)
                    results = result.content.decode("utf-8")
                    return_data=json.loads(results)
                    log_data = [{"AFTER_PAYEMENT_API_DATA": return_data}]
                    common.logger.error(log_data)
                    return JsonResponse(return_data, safe=False)
                else:
                    return Response({"MESSAGE": "ERROR_OCCURED_ON_TOKEN_GENERATIONS OR INVALID AUTHENTICATONS"})

            elif self.request.query_params.get("Action") == "SET" and self.request.query_params.get("Type")=="AMOUNT_TRANSFER":
                jsondata = json.loads(request.body.decode('utf-8'))
                try:
                    Emp_gid=jsondata.get("Params").get("classification").get("Emp_gid")
                    data=jsondata.get("Params").get("filter")

                    log_data = [{"BEFORE_AMOUNT_TRANSFER_API_DATA": data}]
                    common.logger.error(log_data)

                    data=json.dumps(data)
                    token_status=1
                    generated_token_data=master_views.master_sync_Data_("GET","get_data",Emp_gid)
                    log_data=generated_token_data
                    token=generated_token_data.get("DATA")[0].get("clienttoken_name")
                    if(token==" " or token==None):
                        token_status=0
                    if token_status==1:
                        try:
                            client_api = common.clientapi()
                            headers = {"Content-Type": "application/json", "Authorization": "Bearer " + token}
                            result = requests.post("" + client_api + "/nbfc/v1/mwr/amount-transfer",headers=headers,data=data,verify=False)
                            log_data=result
                            results = result.content.decode("utf-8")
                            results_data=json.loads(results)

                            log_data = [{"AFTER_AMOUNT_TRANSFER_API_DATA": results_data}]
                            common.logger.error(log_data)

                            status=results_data.get("CbsStatus")[0].get("ErrorMessage")
                            if(status=="Success"):
                                CBSReferenceNo=results_data.get("CbsStatus")[0].get("CBSReferenceNo")
                                return Response({"MESSAGE":"SUCCESS","CBSREF_NO":CBSReferenceNo})
                            else:
                                return Response({"MESSAGE": "FAILED","FAILED_STATUS":results_data})
                        except Exception as e:
                            common.logger.error(e)
                            return Response({"MESSAGE": "ERROR_OCCURED_ON_AMOUNT_TRANSFER_CLINET_API", "DATA": str(e), "log_data": log_data})
                    else:
                        return Response({"MESSAGE": "ERROR_OCCURED_ON_TOKEN_GENERATIONS OR INVALID AUTHENTICATONS"})
                except Exception as e:
                    common.logger.error(e)
                    return Response({"MESSAGE": "ERROR_OCCURED_TOKEN_GENERATION", "DATA": str(e), "log_data": log_data})
        except Exception as e:
            common.logger.error(e)
            return Response({"MESSAGE": "ERROR_OCCURED_ON_API", "DATA": str(e)})

class AP_Bank_DD_API(APIView):
    def post(self, request):
        log_data=[]
        try:
            if self.request.query_params.get("Action") == "SET" and self.request.query_params.get("Type")=="DD":
                jsondata = json.loads(request.body.decode('utf-8'))
                Emp_gid=jsondata.get("Params").get("classification").get("Emp_gid")
                data=jsondata.get("Params").get("filter")

                log_data = [{"BEFORE_DD_PAYEMENT_API_DATA": data}]
                common.logger.error(log_data)

                data=json.dumps(data)
                token_status=1
                try:
                    generated_token_data=master_views.master_sync_Data_("GET","get_data",Emp_gid)
                    token=generated_token_data.get("DATA")[0].get("clienttoken_name")
                    if(token==" " or token==None):
                        token_status=0
                    if token_status==1:
                        try:
                            client_api = common.clientapi()
                            try:
                                headers = {"Content-Type": "application/json", "Authorization": "Bearer " + token}
                                result = requests.post("" + client_api + "/nbfc/v1/mwr/dd-payment", headers=headers,data=data,verify=False)
                                results = result.content.decode("utf-8")

                                return_data=json.loads(results)
                                log_data = [{"AFTER_DD_PAYEMENT_API_DATA": return_data}]
                                common.logger.error(log_data)

                                return JsonResponse(return_data, safe=False)
                            except Exception as e:
                                common.logger.error(e)
                                return Response({"MESSAGE": "ERROR_OCCURED_ON_CALLING_CLIENT_API", "DATA": str(e)})
                        except Exception as e:
                            common.logger.error(e)
                            return Response({"MESSAGE": "ERROR_OCCURED_ON_GETTING_CLIENT_URL_ON_LOCAL", "DATA": str(e)})
                    else:
                        return Response({"MESSAGE": "ERROR_OCCURED_ON_LOCAL_TOKEN_GENERATION OR INVALID AUTHENTICATONS"})
                except Exception as e:
                    common.logger.error(e)
                    return Response({"MESSAGE": "ERROR_OCCURED_ON_LOCAL_TOKEN_GENERATION", "DATA": str(e)})
        except Exception as e:
            common.logger.error(e)
            return Response({"MESSAGE": "ERROR_OCCURED_ON_LOCAL_DD_API", "DATA": str(e)})


#@api_view(['POST'])
@permission_classes((AllowAny,))
@authentication_classes([])
class AP_DD_Status_Update(APIView):
    def post(self, request):
        log_data = []
        try:
            jsondata = json.loads(request.body.decode('utf-8'))
            log_data = [{"DD_STATUS_UPDATE_LOG": jsondata}]
            common.logger.error(log_data)

            User_Code_Password_Data = request.META.get("HTTP_USERLOGIN")
            if(User_Code_Password_Data==None):
                return Response(
                    {"MESSAGE": "ERROR_OCCURED", "ERROR_MESSAGE": "USERLOGIN IS MISSING"})

            User_Code_Password = re.split('_+', User_Code_Password_Data)
            if (len(User_Code_Password) == 2):
                User_Code = User_Code_Password[0]
                Password = User_Code_Password[1]
            else:
                return Response(
                    {"MESSAGE": "ERROR_OCCURED", "DATA": "GIVE USER CODE AND PASSWORD LIKE,USERCODE_PASSWORD"})
            obj_location = core_calss1.login()
            obj_location.type = "LOGIN_LOCAL"
            new_password = core_calss1.converttoascii(Password)
            obj_location.jsondata = json.dumps({"Employee_Gid": "0", "EmployeeCode": User_Code, "Password": new_password})
            try:
                result = obj_location.get_login()
                if result[1][0] == 'SUCCESS':
                    serviceName=jsondata.get('serviceName')
                    if serviceName == "DD_Payment_Api":
                        try:
                            return_message={}
                            inward_dtl = mAP.ap_model()
                            inward_dtl.action = "Update"
                            inward_dtl.type = "CALLBACK"
                            inward_dtl.header_json = {}
                            inward_dtl.detail_json = {}
                            inward_dtl.other_json = {}
                            inward_dtl.status_json = jsondata
                            inward_dtl.entity_gid = 1
                            inward_dtl.employee_gid = 6493
                            out = outputSplit(inward_dtl.set_payment(), 1)
                            if(out=="SUCCESS"):
                                return_message={"MESSAGE":out}
                                return JsonResponse(return_message, safe=False)
                            return_message={"MESSAGE":out}
                            return JsonResponse(return_message, safe=False)
                        except Exception as e:
                            common.logger.error(e)
                            return Response({"MESSAGE": "ERROR_OCCURED","ERROR_MESSAGE":"ERROR_OCCURED_ON_DD_PAYMENT_SET","DATA": str(e)})
                    else:
                        return Response(
                            {"MESSAGE": "ERROR_OCCURED", "ERROR_MESSAGE": "INVALID SERVICE NAME"})
                else:
                    return Response(
                        {"MESSAGE": "ERROR_OCCURED", "ERROR_MESSAGE": "INVALID USERCODE AND PASSWORD"})
            except Exception as e:
                common.logger.error(e)
                return Response(
                    {"MESSAGE": "ERROR_OCCURED", "ERROR_MESSAGE": "INVALID USERCODE AND PASSWORD","DATA":str(e)})

        except Exception as e:
            common.logger.error(e)
            return Response({"MESSAGE": "ERROR_OCCURED","DATA": str(e)})

@permission_classes((AllowAny,))
@authentication_classes([])
class AP_NEFT_Status_Update(APIView):
    def post(self, request):
        log_data = []
        try:
            jsondata = json.loads(request.body.decode('utf-8'))
            log_data = [{"NEFT_STATUS_UPDATE_LOG": jsondata}]
            common.logger.error(log_data)

            User_Code_Password_Data = request.META.get("HTTP_USERLOGIN")
            if (User_Code_Password_Data == None):
                return Response(
                    {"MESSAGE": "ERROR_OCCURED", "ERROR_MESSAGE": "USERLOGIN IS MISSING"})
            User_Code_Password = re.split('_+', User_Code_Password_Data)
            if (len(User_Code_Password) == 2):
                User_Code = User_Code_Password[0]
                Password = User_Code_Password[1]
            else:
                return Response(
                    {"MESSAGE": "ERROR_OCCURED", "DATA": "GIVE USER CODE AND PASSWORD LIKE,USERCODE_PASSWORD"})
            obj_location = core_calss1.login()
            obj_location.type = "LOGIN_LOCAL"
            new_password = core_calss1.converttoascii(Password)
            obj_location.jsondata = json.dumps({"Employee_Gid": "0", "EmployeeCode": User_Code, "Password": new_password})
            try:
                result = obj_location.get_login()
                if result[1][0] == 'SUCCESS':
                    serviceName=jsondata.get('serviceName')
                    if serviceName == "Electronic_Fund_Transfer":
                        try:
                            return_message={}
                            inward_dtl = mAP.ap_model()
                            inward_dtl.action = "Update"
                            inward_dtl.type = "CALLBACK_NEFT"
                            inward_dtl.header_json = {}
                            inward_dtl.detail_json = {}
                            inward_dtl.other_json = {}
                            inward_dtl.status_json = jsondata
                            inward_dtl.entity_gid = 1
                            inward_dtl.employee_gid = 6493
                            out = outputSplit(inward_dtl.set_payment(), 1)
                            if(out=="SUCCESS"):
                                return_message={"MESSAGE":out}
                                return JsonResponse(return_message, safe=False)
                            return_message={"MESSAGE":out}
                            return JsonResponse(return_message, safe=False)
                        except Exception as e:
                            common.logger.error(e)
                            return Response({"MESSAGE": "ERROR_OCCURED","ERROR_MESSAGE":"ERROR_OCCURED_ON_NEFT_PAYMENT_SET","DATA": str(e)})
                    else:
                        return Response(
                            {"MESSAGE": "ERROR_OCCURED", "ERROR_MESSAGE": "INVALID SERVICE NAME"})
                else:
                    return Response(
                        {"MESSAGE": "ERROR_OCCURED", "ERROR_MESSAGE": "INVALID USERCODE AND PASSWORD"})
            except Exception as e:
                common.logger.error(e)
                return Response(
                    {"MESSAGE": "ERROR_OCCURED", "ERROR_MESSAGE": "INVALID USERCODE AND PASSWORD","DATA":str(e)})

        except Exception as e:
            common.logger.error(e)
            return Response({"MESSAGE": "ERROR_OCCURED","DATA": str(e)})



class ECFInvoice_set(APIView):
    def post(self, request):
        try:
            # path = request.path
            if self.request.query_params.get("action") == "INSERT" and self.request.query_params.get("type")=="INVOICE_HEADER":
                inward_dtl = mAP.ap_model()
                jsondata = json.loads(request.body.decode('utf-8'))
                inward_dtl.action = request.query_params.get("action")
                inward_dtl.type = request.query_params.get("type")
                inward_dtl.header_json = jsondata.get('params').get('header_json')
                inward_dtl.debit_json = jsondata.get('params').get('debit_json')
                inward_dtl.detail_json = jsondata.get('params').get('detail_json')
                inward_dtl.status_json = jsondata.get('params').get('status_json')
                inward_dtl.entity_gid = request.query_params.get("entity_gid")
                inward_dtl.employee_gid = request.query_params.get("employee_gid")
                # common.main_fun1(request.read(), path)
                ld_out_message = inward_dtl.set_ECFInvoiceheader()
                msg = ld_out_message[0].split(",")
                print(msg)
                if msg[1] == 'SUCCESS':
                    ld_dict = {"MESSAGE": msg[1],"Header_Gid":msg[0] ,"STATUS":0}
                else:
                    ld_dict = {"MESSAGE": 'ERROR_OCCURED.' + ld_out_message,"STATUS":1}
                return Response(ld_dict)
            if self.request.query_params.get("action") == "INSERT" and self.request.query_params.get("type")=="INVOICE_DETAILS":
                inward_dtl = mAP.ap_model()
                jsondata = json.loads(request.body.decode('utf-8'))
                inward_dtl.action = request.query_params.get("action")
                inward_dtl.type = request.query_params.get("type")
                inward_dtl.header_json = jsondata.get('params').get('header_json')
                inward_dtl.detail_json = jsondata.get('params').get('detail_json')
                inward_dtl.invoice_json = jsondata.get('params').get('invoice_json')
                inward_dtl.debit_json = jsondata.get('params').get('debit_json')
                inward_dtl.credit_json = jsondata.get('params').get('credit_json')
                inward_dtl.status_json = jsondata.get('params').get('status_json')
                inward_dtl.entity_gid = request.query_params.get("entity_gid")
                inward_dtl.employee_gid = request.query_params.get("employee_gid")
                # common.main_fun1(request.read(), path)
                ld_out_message = inward_dtl.ECFset_Invoice()
                if ld_out_message[0] == 'SUCCESS':
                    ld_dict = {"MESSAGE": "SUCCESS","STATUS":0}
                elif ld_out_message[0] == 'FAIL':
                    ld_dict = {"MESSAGE": "FAIL","STATUS":1}
                else:
                    ld_dict = {"MESSAGE": 'ERROR_OCCURED.' + ld_out_message[0],"STATUS":1}
                return Response(ld_dict)
        except Exception as e:
            common.logger.error(e)
            return Response({"MESSAGE": "ERROR_OCCURED_ON_API", "DATA": str(e)})

import tempfile
class ECFInvoice_get(APIView):
    def post(self, request):
        try:
            # path = request.path
            ecf_obj = mAP.ap_model()
            jsondata = json.loads(request.body.decode('utf-8'))
            ecf_obj.action = jsondata.get('filter').get('action')
            ecf_obj.type = jsondata.get('filter').get('type')
            ecf_obj.filter = json.dumps(jsondata.get('filter'))
            ecf_obj.classification = json.dumps(jsondata.get('CLASSIFICATION'))
            create_by = jsondata.get('filter').get('create_by')
            ecf_obj.create_by = jsondata.get('filter').get('create_by')
            output = ecf_obj.get_ecf_pdf_data()
            Entity_gid = jsondata.get('CLASSIFICATION').get('CLASSIFICATION')
            ecf_no = str(output.get('INVOICE_HEADER')[0].get('invoiceheader_crno'))
            # print(ecf_no)
            # if output.get('INVOICE_DETAIL')[0].get('invoicedetails_item') == 'ADVANCE':
            #     data_type = "TOURADV"
            # else:
            #     data_type = "CLAIM"
            # params = {"Invoice_Header_Gid":jsondata.get('filter').get('InvoiceHeader_Gid'),
            #           "AppType":data_type}
            # tk = str(request.auth.token)
            # token = "Bearer  " + tk[2:len(tk) - 1]
            # headers = {"content-type": "application/json", "Authorization": "" + token + ""}
            # resp = requests.get("" + ip + "/APPROVAL_FLOW_PDF", params=params, data={}, headers=headers,
            #                     verify=False)
            # apprl_hstry = json.loads(resp.content.decode("utf-8"))
            # jdata = apprl_hstry.get('DATA')
            # trandata = []
            # level = output.get('INVOICE_HEADER')[0].get('invoiceheader_invoiceno')
            # lvl = level.split('_')
            # if output.get('INVOICE_DETAIL')[0].get('invoicedetails_item') == 'ADVANCE':
            #     for i in jdata:
            #         if int(i.get('applevel')) == int(lvl[1]):
            #             trandata.append(i)
            #     if trandata ==[]:
            #         trandata = jdata
            # else:
            #     trandata = jdata
            # output['TRAN_DATA'] = trandata
            # invoice_set = mAP.ap_model()
            ecf_obj.action = 'GET'
            ecf_obj.type = 'ECF_TRANS_GET'
            filter = {
                "Ref_Name": "ECF_INVOICE",
                "RefTable_Gid": output.get('INVOICE_HEADER')[0].get('invoiceheader_gid')
            }
            ecf_obj.filter = json.dumps(filter)
            ecf_obj.classification = json.dumps(jsondata.get('CLASSIFICATION'))
            ecf_obj.create_by = jsondata.get('filter').get('create_by')
            out = ecf_obj.get_invoice_all()
            jdata = out.to_json(orient='records')
            jdata = json.loads(jdata)
            output['TRAN_DATA'] = jdata
            EAN = barcode.get_barcode_class('Code128')
            concat_filename = str(create_by) + "_" + str(ecf_no) + "_" + "ecf_barcode" + ".png"
            print(concat_filename)
            tmp = tempfile.NamedTemporaryFile()
            with open(tmp.name, 'wb') as f:
                EAN(ecf_no, writer=ImageWriter()).write(f)

            with open(tmp.name, 'rb') as f:
                contents = f.read()

            s3 = boto3.resource('s3')
            s3_obj = s3.Object(bucket_name=S3_BUCKET_NAME, key=concat_filename)
            s3_obj.put(Body=contents)
            s3_client = boto3.client('s3','ap-south-1')
            response = s3_client.generate_presigned_url('get_object',
                                                        Params={'Bucket': S3_BUCKET_NAME,
                                                                'Key': concat_filename},
                                                        ExpiresIn=3600)
            print(response)
            classify = {
                "bar_code_path": response,
                "logo_path": ip + "/static/Images/vsolvLogo.png",
                "icon_path": ip + "/static/Images/vsolvLogo.png"
            }
            output['INVOICE_HEADER'][0].update(classify)
            invoicedetails_totalamt = 0
            for i in output.get('INVOICE_DETAIL'):
                invoicedetails_totalamt = invoicedetails_totalamt + i.get('invoicedetails_totalamt')

            debit_amount = 0
            for i in output.get('DEBIT'):
                debit_amount = debit_amount + i.get('debit_amount')

            credit_amount = 0
            for i in output.get('CREDIT'):
                credit_amount = credit_amount + i.get('credit_amount')

            no_to_words = num2words(int(invoicedetails_totalamt))
            if output.get('INVOICE_DETAIL')[0].get('invoicedetails_item') == 'ADVANCE':
                output['title_pdf'] = "Tour Advance Form"
            else:
                output['title_pdf'] = "Tour Claim Form"
            c = CamelCase()
            no_to_words = str(no_to_words)
            output['no_to_words'] = c.hump(no_to_words)
            output['credit_amount'] = str(credit_amount)+"0"
            output['debit_amount'] = str(debit_amount)+"0"
            output['invoicedetails_totalamt'] = str(invoicedetails_totalamt)+"0"

            return JsonResponse(output, safe=False)
        except Exception as e:
            common.logger.error(e)
            return Response({"MESSAGE": "ERROR_OCCURED_ON_API", "DATA": str(e)})


class ECFstatus_get(APIView):
    def post(self, request):
        try:
            ecf_obj = mAP.ap_model()
            jsondata = json.loads(request.body.decode('utf-8'))
            ecf_obj.action = request.query_params.get("action")
            ecf_obj.type = request.query_params.get("type")
            ecf_obj.filter = json.dumps(jsondata.get('params').get('filter'))
            ecf_obj.classification = json.dumps({"Entity_Gid": request.query_params.get("entity_gid")})
            # ecf_obj.create_by = request.query_params.get("employee_gid")
            # common.main_fun1(request.read(), path)
            output = ecf_obj.get_ecf_details()
            jdata = output.to_json(orient='records')
            return JsonResponse(json.loads(jdata), safe=False)
        except Exception as e:
            common.logger.error(e)
            return Response({"MESSAGE": "ERROR_OCCURED_ON_API", "DATA": str(e)})

class ECFStatus_set(APIView):
    def post(self, request):
        try:
            inward_dtl = mAP.ap_model()
            jsondata = json.loads(request.body.decode('utf-8'))
            inward_dtl.action = request.query_params.get("action")
            inward_dtl.type = request.query_params.get("type")
            inward_dtl.header_json = jsondata.get('params').get('header_json')
            inward_dtl.detail_json = jsondata.get('params').get('detail_json')
            inward_dtl.invoice_json = jsondata.get('params').get('invoice_json')
            inward_dtl.debit_json = jsondata.get('params').get('debit_json')
            inward_dtl.credit_json = jsondata.get('params').get('credit_json')
            inward_dtl.status_json = jsondata.get('params').get('status_json')
            inward_dtl.entity_gid = int(request.query_params.get("entity_gid"))
            inward_dtl.employee_gid = int(request.query_params.get("employee_gid"))
            # common.main_fun1(request.read(), path)
            ld_out_message = inward_dtl.set_ECFInvoice_Status()
            if ld_out_message[0] == 'SUCCESS':
                ld_dict = {"MESSAGE": "SUCCESS", "STATUS": 0}
            elif ld_out_message[0] == 'FAIL':
                ld_dict = {"MESSAGE": "FAIL", "STATUS": 1}
            else:
                ld_dict = {"MESSAGE": 'ERROR_OCCURED.AP API' + ld_out_message[0], "STATUS": 1}
            return Response(ld_dict)
        except Exception as e:
            common.logger.error(e)
            return Response({"MESSAGE": "ERROR_OCCURED_ON_API", "DATA": str(e)})

class APStatus_set(APIView):
    def post(self, request):
        try:
            inward_dtl = mAP.ap_model()
            jsondata = json.loads(request.body.decode('utf-8'))
            inward_dtl.action = request.query_params.get("action")
            inward_dtl.type = request.query_params.get("type")
            inward_dtl.header_json = jsondata.get('params').get('header_json')
            inward_dtl.debit_json = jsondata.get('params').get('debit_json')
            inward_dtl.detail_json = jsondata.get('params').get('detail_json')
            inward_dtl.status_json = jsondata.get('params').get('status_json')
            inward_dtl.entity_gid = request.query_params.get("entity_gid")
            inward_dtl.employee_gid = request.query_params.get("employee_gid")
            final_out = outputSplit(inward_dtl.set_Invoiceheader_status_update(),1)
            if final_out == 'SUCCESS':
                ld_dict = {"MESSAGE": "SUCCESS", "STATUS": 0}
            elif final_out == 'FAIL':
                ld_dict = {"MESSAGE": "FAIL", "STATUS": 1}
            else:
                ld_dict = {"MESSAGE": 'ERROR_OCCURED.' + final_out, "STATUS": 1}
            return Response(ld_dict)
        except Exception as e:
            common.logger.error(e)
            return Response({"MESSAGE": "ERROR_OCCURED_ON_API", "DATA": str(e)})

class WS_PROFFING_API(APIView):
    def post(self, request):
        try:
            data=json.loads(request.body.decode('utf-8'))
            if data['Type'] == "GET" and data['Sub_Type']=="PROFFING":
                # Get The Data And Shown in Assert Maker Summary :: Pending Data.
                print("we profing")
                # path = self.request.stream.path
                jsondata = json.loads(request.body.decode('utf-8'))
                obj_ap = mAP.ap_model()
                obj_ap.type = data["Type"]
                obj_ap.sub_type = data["Sub_Type"]
                obj_ap.filter = json.dumps(jsondata.get('Params').get('FILTER'))
                obj_ap.classification = json.dumps(jsondata.get('Params').get('CLASSIFICATION'))
                ld_out_message = obj_ap.get_WS_PROFFING_API_details()
                if ld_out_message.get("MESSAGE") == 'FOUND':
                    ld_dict = {"DATA": json.loads(ld_out_message.get("DATA").to_json(orient='records')),
                               "MESSAGE": 'FOUND'}
                elif ld_out_message.get("MESSAGE") == 'NOT_FOUND':
                    ld_dict = {"MESSAGE": 'NOT_FOUND'}
                else:
                    ld_dict = {"MESSAGE": 'ERROR_OCCURED.' + ld_out_message.get("MESSAGE")}
                return Response(ld_dict)
        except Exception as e:
            common.logger.error(e)
            return Response({"MESSAGE": "ERROR_OCCURED_ON_API", "DATA": str(e)})

def outputSplit(tubledtl, index):
    temp = tubledtl[0].split(',')
    if (len(temp) > 1):
        if (index == 0):
            return int(temp[0])
        else:
            return temp[1]
    else:
        return temp[0]