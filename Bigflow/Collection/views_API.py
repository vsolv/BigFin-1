from django.core.files.storage import default_storage
from rest_framework.views import APIView
from rest_framework.response import Response
import json
from Bigflow.Collection.Model import mCollection
from Bigflow.Master import views as MasterViews
from Bigflow.Master.Model import mMasters
from Bigflow.Transaction import views
from Bigflow.Transaction.Model import mFET, mSales
from Bigflow.Service.Model import mService
from Bigflow.UserMgmt import views as UM_View
from Bigflow.Core import class1
from Bigflow.Core.models import decrpt as decry_data
import Bigflow

class Collection_API(APIView):

    def post(self, request):
        try:
            if self.request.query_params.get("Group") == "GET_CLTN_INV_MAP":
                obj_cltn = mCollection.Collection_model()
                obj_cltn.action = self.request.query_params.get("Action")
                obj_cltn.type = self.request.query_params.get("Type")
                obj_cltn.collectionheader_gid = self.request.query_params.get("Collection_Gid")
                obj_cltn.name = ''
                obj_cltn.date = ''
                obj_cltn.jsonData = json.loads(request.body.decode('utf-8')).get('params').get('DATA')

                obj_cltn.jsondata = json.loads(request.body.decode('utf-8')).get('params').get ('CLASSIFICATION')

                obj_cltn.entity = json.loads(request.body.decode('utf-8')).get('params').get ('CLASSIFICATION').get('Entity_Gid')
                obj_cltn.jsondata['Entity_Gid'] = [decry_data(obj_cltn.entity)]
                out_message = obj_cltn.get_collection_inv_map()
                if out_message.empty == False:
                    json_data = json.loads(out_message.to_json(orient='records'))
                    return Response({"MESSAGE": "FOUND", "DATA": json_data})
                else:
                    return Response({"MESSAGE": "NOT_FOUND"})

            elif self.request.query_params.get("Group") == "GET_CLTN_PAYMENT_SUMMARY":
                obj_cltn = mCollection.Collection_model()
                obj_cltn.action = self.request.query_params.get("Action")
                obj_cltn.type = self.request.query_params.get("Type")
                obj_cltn.collectionheader_gid = 0
                obj_cltn.name = ''
                obj_cltn.date = ''
                obj_cltn.jsonData = json.loads(request.body.decode('utf-8')).get('params').get('DATA')
                obj_cltn.jsondata = json.loads(request.body.decode('utf-8')).get('params').get('CLASSIFICATION')
                # print(json.loads(request.body.decode('utf-8')).get('params').get('DATA').get("entity"))
                obj_cltn.jsondata['Entity_Gid'] = [1]
                out_message = obj_cltn.get_collection_inv_map()
                if out_message.empty == False:
                    json_data = json.loads(out_message.to_json(orient='records'))
                    return Response({"MESSAGE": "FOUND", "DATA": json_data})
                else:
                    return Response({"MESSAGE": "NOT_FOUND"})

        except Exception as e:
                return Response({"MESSAGE": "ERROR","DATA":str(e)})

    def get(self, request):
        try:
            if self.request.query_params.get("Group") == "GET_OUTSTAND":
                obj_outstand = mFET.FET_model()
                obj_outstand.action = self.request.query_params.get("Action")
                obj_outstand.from_date = self.request.query_params.get("From_date")
                obj_outstand.to_date = self.request.query_params.get("To_date")
                obj_outstand.customer_gid = self.request.query_params.get("Cust_gid")
                obj_outstand.employee_gid = decry_data(self.request.query_params.get("Emp_gid"))
                obj_outstand.limit = self.request.query_params.get("limit")
                obj_outstand.entity_gid=decry_data(self.request.query_params.get("Entity_gid"))
                out_message=obj_outstand.get_outstanding_fet()
                if out_message.empty == False:
                    json_data = json.loads(out_message.to_json(orient='records'))
                    return Response({"MESSAGE": "FOUND", "DATA": json_data})
                else:
                    return Response({"MESSAGE": "NOT_FOUND"})
        except Exception as e:
            return Response({"MESSAGE": "ERROR_OCCURED","DATA":str(e)})
                # Save the Data

from Bigflow.API import views as commonview

class FET_Collection_API(APIView):

    def post(self, request):
        try:
            #   Group = SET_INITIAL, UPDATE_STATUS
            if self.request.query_params.get("Group") == "SET_INITIAL":
                jsondata = json.loads(request.body.decode('utf-8'))
                obj_cltn = mFET.FET_model()
                obj_cltn.action = self.request.query_params.get("Action")
                obj_cltn.type = self.request.query_params.get("Type")
                obj_cltn.collectionheader_gid = self.request.query_params.get("Collection_Gid")
                obj_cltn.customer_gid = (self.request.query_params.get("Customer_Gid"))
                obj_cltn.employee_gid = decry_data(self.request.query_params.get("Employee_Gid"))
                obj_cltn.mode = self.request.query_params.get("Collection_Mode")
                obj_cltn.amount = self.request.query_params.get("Collection_Amount")
                obj_cltn.date = self.request.query_params.get("Collection_Date")
                obj_cltn.cheque_no = '';
                obj_cltn.remark = self.request.query_params.get("Collection_Description")
                obj_cltn.entity_gid = decry_data(self.request.query_params.get("Entity_Gid"))
                obj_cltn.create_by = decry_data(self.request.query_params.get("Employee_Gid"))
                obj_cltn.jsonData = jsondata.get("Params").get("CHEQUE")
                file  = json.dumps(jsondata.get('Params').get('File'))
                if file != '[]':
                    lst_saved_filepath = commonview.File_Upload(file, 'CHEQUE', obj_cltn.create_by)
                    obj_cltn.json_file = json.dumps({'File':lst_saved_filepath})
                else:
                    obj_cltn.json_file = json.dumps(jsondata.get('Params').get('File'))

                out_message = obj_cltn.set_collection()
                if out_message[0] == "SUCCESS":
                    return Response({"MESSAGE": "SUCCESS"})
                else:
                    return Response({"MESSAGE": "FAIL","DATA":str(out_message[0])})

            elif self.request.query_params.get("Group") == "UPDATE_STATUS":
                obj_cltn = mFET.FET_model()
                obj_cltn.action = self.request.query_params.get("Action")
                obj_cltn.type = self.request.query_params.get("Type")
                obj_cltn.collectionheader_gid = 0
                obj_cltn.customer_gid = 0
                obj_cltn.employee_gid = decry_data(self.request.query_params.get("Employee_Gid"))
                obj_cltn.mode = ''
                obj_cltn.amount = 0
                obj_cltn.date = ''
                obj_cltn.cheque_no = ''
                obj_cltn.remark = ''
                obj_cltn.entity_gid = decry_data(self.request.query_params.get("Entity_Gid"))
                obj_cltn.create_by =decry_data(self.request.query_params.get("Employee_Gid"))
                obj_cltn.jsonData = json.loads(request.body.decode('utf-8'))

                out_message = obj_cltn.set_collection()
                if out_message[0] == "SUCCESS":
                    return Response({"MESSAGE": "SUCCESS"})
                else:
                    return Response({"MESSAGE": "FAIL", "DATA": str(out_message[0])})

            elif self.request.query_params.get("Group") == "COLLECTION_DELETE":
                obj_cltn = mFET.FET_model()
                obj_cltn.action = self.request.query_params.get("Action")
                obj_cltn.type = self.request.query_params.get("Type")
                obj_cltn.collectionheader_gid = self.request.query_params.get("Collection_Gid")
                obj_cltn.customer_gid = 0
                obj_cltn.employee_gid = decry_data(self.request.query_params.get("Employee_Gid"))
                obj_cltn.mode = ''
                obj_cltn.amount = 0
                obj_cltn.date = ''
                obj_cltn.cheque_no = ''
                obj_cltn.remark = ''
                obj_cltn.entity_gid = decry_data(self.request.query_params.get("Entity_Gid"))
                obj_cltn.create_by = decry_data(self.request.query_params.get("Employee_Gid"))
                obj_cltn.jsonData = {}
                out_message = obj_cltn.set_collection()
                if out_message[0] == "SUCCESS":
                    return Response({"MESSAGE": "SUCCESS"})
                else:
                    return Response({"MESSAGE": "FAIL", "DATA": str(out_message[0])})

            elif self.request.query_params.get("Group") == "UPDATE_DISPATCH":
                obj_cltn = mService.Service_model()
                obj_cltn.action = self.request.query_params.get("Action")
                obj_cltn.type = self.request.query_params.get("Type")
                obj_cltn.in_out = self.request.query_params.get("In_Out")
                obj_cltn.courier_gid = self.request.query_params.get("Courier_Gid")
                obj_cltn.Dispatch_date = self.request.query_params.get("Dispatch_Date")
                obj_cltn.send_by = self.request.query_params.get("Send_By")
                obj_cltn.awbno = self.request.query_params.get("AWB_No")
                obj_cltn.dispatch_mode = self.request.query_params.get("Dispatch_Mode")
                obj_cltn.dispatch_type = self.request.query_params.get("Packets")
                obj_cltn.weight = self.request.query_params.get("Weight")
                obj_cltn.dispatch_to = self.request.query_params.get("Dispatch_To")
                obj_cltn.address = self.request.query_params.get("Address")
                obj_cltn.city = self.request.query_params.get("City")
                obj_cltn.state = self.request.query_params.get("State")
                obj_cltn.pincode =self.request.query_params.get("Pincode")
                obj_cltn.remark = self.request.query_params.get("Remark")
                obj_cltn.returned = self.request.query_params.get("Returned")
                obj_cltn.returned_on = ''
                obj_cltn.returned_remark = ''
                obj_cltn.pod = ''
                obj_cltn.pod_image = ''
                obj_cltn.isactive = ''
                obj_cltn.isremoved = ''
                obj_cltn.dispatch_gid = 0
                obj_cltn.SERVICE_JSON = json.loads(request.body.decode('utf-8'))
                obj_cltn.status = self.request.query_params.get("Status")
                obj_cltn.entity_gid = decry_data(self.request.query_params.get("Entity_Gid"))
                obj_cltn.employee_gid = decry_data(self.request.query_params.get("Employee_Gid"))

                out_message = obj_cltn.set_Dispatch()

                if out_message[0] == "SUCCESS":
                    return Response({"MESSAGE": "SUCCESS"})
                else:
                    return Response({"MESSAGE": "FAIL", "DATA": str(out_message[0])})



            elif self.request.query_params.get("Group") == "INV_RECEIPT":
                obj_cltn = mCollection.Collection_model()
                obj_cltn.action = self.request.query_params.get("Action")
                obj_cltn.type = self.request.query_params.get("Type")
                obj_cltn.commit = self.request.query_params.get("commit")
                obj_cltn.create_by = decry_data(self.request.query_params.get("Create_by"))
                obj_cltn.jsonData = json.loads(request.body.decode('utf-8')).get('params').get('DATA')
                obj_cltn.json_classification = json.loads(request.body.decode('utf-8')).get('params').get('Classification')
                obj_cltn.json_classification['entity_gid'] = decry_data(self.request.query_params.get("entity"))

                out_message = outputReturn(obj_cltn.set_invreceipt_map(), 1)
                if out_message == "SUCCESS":
                    return Response({"MESSAGE": "SUCCESS"})
                else:
                    return Response({"MESSAGE": "FAIL", "DATA": str(out_message)})



        except Exception as e:
                return Response({"MESSAGE": "ERROR","DATA":str(e)})


def outputReturn(tubledtl, index):
   temp = tubledtl[0].split(',')
   if (len(temp) > 1):
       if (index == 0):
           return int(temp[0])
       else:
           return temp[1]
   else:
       return temp[0]

   #### Bank Upload the Files. Excel
from django.conf import settings
from datetime import datetime
class Bankimageapi(APIView):
    def post(self, request):
        if request.method == 'POST' and request.FILES['file']:
            try:
                current_month = datetime.now().strftime('%m')
                current_day = datetime.now().strftime('%d')
                current_year_full = datetime.now().strftime('%Y')
                save_path = str(settings.MEDIA_ROOT)+ '/Bank_Doc/'+str(current_year_full)+'/'+str(current_day)+'/'+str(current_month)+'/'+str(request.FILES['file'])
                path = default_storage.save(str(save_path), request.FILES['file'])
                return Response({"MESSAGE":"SUCCESS","DATA":default_storage.path(path)})
            except Exception as ex:
                return Response({"DATA": str(ex)})


class BankUpload_API(APIView):
    def post(self,request):
        try:
            if self.request.query_params.get("Group") == "BANK_UPLOAD_AR":
                obj_bank = mCollection.Collection_model()
                obj_bank.action = self.request.query_params.get("Action")
                obj_bank.type = self.request.query_params.get("Type")
                obj_bank.create_by = decry_data(self.request.query_params.get("Employee_Gid"))
                obj_bank.jsonData = json.loads(request.body.decode('utf-8')).get('params').get('DATA')
                obj_bank.json_classification = json.loads(request.body.decode('utf-8')).get('params').get('CLASSIFICATION')
                obj_bank.json_classification['entity_gid'] = [decry_data(json.loads(request.body.decode('utf-8')).get('params').get('CLASSIFICATION').get('entity_gid'))]
                obj_bank.jsondata = json.loads(request.body.decode('utf-8')).get('params').get('FILE')

                out_message = obj_bank.set_bank_upload()
                if out_message[0] == 'SUCCESS':
                    return Response({"MESSAGE": "SUCCESS"})
                else:
                    return Response({"MESSAGE": out_message[0]})
            elif self.request.query_params.get("Group") == "BANK_STMT_MAPPING_GET":
                obj_bank_get = mCollection.Collection_model()
                obj_bank_get.type = self.request.query_params.get("Type")
                obj_bank_get.sub_type = self.request.query_params.get("Sub_Type")
                obj_bank_get.jsonData = json.loads(request.body.decode('utf-8')).get('params').get('FILTERS')
                obj_bank_get.json_classification = json.loads(request.body.decode('utf-8')).get('params').get('CLASSIFICATION')
                obj_bank_get.json_classification['Entity_Gid'] = [decry_data(self.request.query_params.get("entity"))]

                out_message = obj_bank_get.get_bank_upload()

                if out_message.empty == False:
                    json_data = json.loads(out_message.to_json(orient='records'))
                    return Response({"MESSAGE": "FOUND", "DATA": json_data})
                else:
                    return Response({"MESSAGE": "NOT_FOUND"})
            elif self.request.query_params.get("Group") == "BANK_STMT_MAPPING_SET":
                #### To Set the Bank and cltn ::: BRS :: Collection Mapping
                obj_bank_set = mCollection.Collection_model()
                obj_bank_set.action = self.request.query_params.get("Action")
                obj_bank_set.type = self.request.query_params.get("Type")
                obj_bank_set.create_by = decry_data(self.request.query_params.get("Employee_Gid"))
                obj_bank_set.jsonData = json.loads(request.body.decode('utf-8')).get('params').get('DATA')
                obj_bank_set.json_classification = json.loads(request.body.decode('utf-8')).get('params').get('CLASSIFICATION')
                # obj_bank.json_classification = json.loads(request.body.decode('utf-8')).get('params').get('CLASSIFICATION')
                obj_bank_set.json_classification['Entity_Gid'] = [decry_data(json.loads(request.body.decode('utf-8')).get('params').get('CLASSIFICATION').get('Entity_Gid'))]
                obj_bank_set.jsondata = '{}'


                out_message = obj_bank_set.set_bank_upload()
                if out_message[0] == 'SUCCESS':
                    return Response({"MESSAGE": "SUCCESS"})
                else:
                    return Response({"MESSAGE": "FAIL","DATA":out_message})

        except Exception as e:
            return Response({"MESSAGE":"ERROR","DATA":str(e)})

class Receipt_AR(APIView):
    def post(self,request):
        try:
            if self.request.query_params.get("Group") == "AR_RECEIPT_COLLECTION":
                obj_receipt = mCollection.Collection_model()
                obj_receipt.type = self.request.query_params.get("Type")
                obj_receipt.sub_type = self.request.query_params.get("Sub_Type")
                obj_receipt.jsonData = json.loads(request.body.decode('utf-8')).get('params').get('FILTERS')
                obj_receipt.json_classification = json.loads(request.body.decode('utf-8')).get('params').get('CLASSIFICATION')
                obj_receipt.json_classification['entity_gid'] = [decry_data(self.request.query_params.get("entity"))]

                out_message = obj_receipt.get_receipt_ar()
                if out_message.empty == False:
                    json_data = json.loads(out_message.to_json(orient='records'))
                    return Response({"MESSAGE": "FOUND", "DATA": json_data})
                else:
                    return Response({"MESSAGE": "NOT_FOUND"})

            elif self.request.query_params.get("Group") == "AR_INV_MAPPING_RECEIPT_SET":
                obj_receipt_set=mCollection.Collection_model()
                obj_receipt_set.action=self.request.query_params.get("Action")
                obj_receipt_set.type=self.request.query_params.get("Type")
                obj_receipt_set.commit=self.request.query_params.get("Commit")
                obj_receipt_set.create_by=decry_data(self.request.query_params.get("Create_by"))
                obj_receipt_set.jsonData=json.loads(request.body.decode('utf-8')).get('params').get('DATA')
                obj_receipt_set.json_classification=json.loads(request.body.decode('utf-8')).get('params').get('CLASSIFICATION')
                obj_receipt_set.json_classification['Entity_Gid'] = [decry_data(self.request.query_params.get("entity"))]
                out_message = obj_receipt_set.set_receipt_ar()
                if out_message[0] == 'SUCCESS':
                    return Response({"MESSAGE": "SUCCESS"})
                else:
                    return Response({"MESSAGE": "FAIL","DATA":out_message[0]})

            elif self.request.query_params.get("Group") == "INV_RECEIPT_SUMMARY":
                obj_receipt = mCollection.Collection_model()
                obj_receipt.type = self.request.query_params.get("Type")
                obj_receipt.sub_type = self.request.query_params.get("Sub_Type")
                obj_receipt.jsonData = json.loads(request.body.decode('utf-8')).get('params').get('FILTERS')
                obj_receipt.json_classification = json.loads(request.body.decode('utf-8')).get('params').get('CLASSIFICATION')
                obj_receipt.json_classification['entity_gid'] = [decry_data( self.request.query_params.get("entity"))]

                out_message = obj_receipt.get_receipt_ar()
                if out_message.empty == False:
                    json_data = json.loads(out_message.to_json(orient='records'))
                    return Response({"MESSAGE": "FOUND", "DATA": json_data})
                else:
                    return Response({"MESSAGE": "NOT_FOUND"})

        except Exception as e:
            return Response({"MESSAGE":"ERROR","DATA":str(e)})

class Receipt_Process_API(APIView):
    def post(self,request):
        try:
            if self.request.query_params.get("Group") == "RECEIPT_CANCEL_COLLECTION":
                obj_receipt = mCollection.Collection_model()
                obj_receipt.action = self.request.query_params.get("Action")
                obj_receipt.type = self.request.query_params.get("Type")
                obj_receipt.sub_type = self.request.query_params.get("Sub_Type")
                obj_receipt.create_by = decry_data(self.request.query_params.get('Employee_Gid'))
                obj_receipt.jsonData = json.loads(request.body.decode('utf-8')).get('params').get('DATA')
                obj_receipt.json_classification = json.loads(request.body.decode('utf-8')).get('params').get('CLASSIFICATION')
                obj_receipt.json_classification['Entity_Gid'] = [decry_data(obj_receipt.json_classification['Entity_Gid'] )]
                obj_receipt.json_classification = obj_receipt.json_classification

                out_message = obj_receipt.set_receiptprocess_ar()
                if out_message[0] == 'SUCCESS':
                    return Response({"MESSAGE": "SUCCESS"})
                else:
                    return Response({"MESSAGE": "FAIL","DATA":out_message[0]})
            elif self.request.query_params.get("Group") == "RECEIPT_MAKE_DISCOUNT":
                obj_receipt = mCollection.Collection_model()
                obj_receipt.action = self.request.query_params.get("Action")
                obj_receipt.type = self.request.query_params.get("Type")
                obj_receipt.sub_type = self.request.query_params.get("Sub_Type")
                obj_receipt.create_by = decry_data(self.request.query_params.get('Employee_Gid'))
                obj_receipt.jsonData = json.loads(request.body.decode('utf-8')).get('params').get('DATA')
                obj_receipt.json_classification = json.loads(request.body.decode('utf-8')).get('params').get('CLASSIFICATION')
                obj_receipt.json_classification['Entity_Gid'] = [decry_data(obj_receipt.json_classification['Entity_Gid'])]
                obj_receipt.json_classification = obj_receipt.json_classification
                out_message = obj_receipt.set_receiptprocess_ar()
                if out_message[0] == 'SUCCESS':
                    return Response({"MESSAGE": "SUCCESS"})
                else:
                    return Response({"MESSAGE": "FAIL","DATA":out_message[0]})



        except Exception as e:
            return  Response({"MESSAGE":"ERROR","DATA":str(e)})

#### Masters.
class Customer_API(APIView):
    def post(self,request):
        try:
            if self.request.query_params.get("Group") == "CUST_GROUP_GET":
                obj_custgroup = mMasters.Masters()
                obj_custgroup.custgrp_gid = self.request.query_params.get("Cust_Group_Gid")
                obj_custgroup.custgrp_code = self.request.query_params.get("Cust_Group_Code")
                obj_custgroup.custgrp_name = self.request.query_params.get("Cust_Group_Name")
                obj_custgroup.entity_gid = decry_data(self.request.query_params.get("Entity_Gid"))
                obj_custgroup.mysql_limit = self.request.query_params.get("Query_Limit")

                df_out_message = obj_custgroup.get_custgrp()

                if df_out_message.empty == False:
                    json_data = json.loads(df_out_message.to_json(orient='records'))
                    return Response({"MESSAGE": "FOUND", "DATA": json_data})
                else:
                    return Response({"MESSAGE": "NOT_FOUND"})
            elif self.request.query_params.get("Group") == "CUST_GET":
                obj_cust = mMasters.Masters()
                obj_cust.customer_gid = 0;
                obj_cust.jsonData = json.loads(request.body.decode('utf-8')).get('params').get('FILTER')
                obj_cust.customer_code = 0;
                obj_cust.customer_name = '';
                obj_cust.entity_gid = decry_data(self.request.query_params.get("Entity_Gid"))
                obj_cust.jsonData = json.dumps(obj_cust.jsonData)

                df_out_message = obj_cust.get_customer()
                if df_out_message.empty == False:
                    json_data = json.loads(df_out_message.to_json(orient='records'))
                    return Response({"MESSAGE": "FOUND", "DATA": json_data})
                else:
                    return Response({"MESSAGE": "NOT_FOUND"})

        except Exception as e:
            return Response({"MESSAGE":"ERROR","DATA":str(e)})
####Prakash

class Customer_Get_API(APIView):
    def post(self, request):
        try:
            if self.request.query_params.get("Group") == "CUST_All_GROUP_GET":
                obj_allcustomer = mMasters.Masters()
                obj_allcustomer.type = self.request.query_params.get("Type")
                obj_allcustomer.sub_type = self.request.query_params.get("Sub_Type")
                obj_allcustomer.jsonData = json.loads(request.body.decode('utf-8')).get('Params').get('FILTER')
                obj_allcustomer.jsonData = json.dumps(obj_allcustomer.jsonData)
                obj_allcustomer.limit = self.request.query_params.get("Limit")
                obj_allcustomer.json_classification = json.loads(request.body.decode('utf-8')).get('Params').get('CLASSIFICATION')
                # obj_soinvprocess.json_classification = jsondata.get('Params').get('CLASSIFICATION')
                obj_allcustomer.json_classification['Entity_Gid'] = [ decry_data(self.request.query_params.get("entity"))]

                obj_allcustomer.json_classification = json.dumps(obj_allcustomer.json_classification)
                ld_out_message = obj_allcustomer.get_AllCustomer()
                if ld_out_message.get("MESSAGE") == 'FOUND':
                    ld_dict = {"DATA": json.loads(ld_out_message.get("DATA").to_json(orient='records')),
                               "MESSAGE": "FOUND"}
                elif ld_out_message.get("MESSAGE") == 'NOT_FOUND':
                    ld_dict = {"MESSAGE": ld_out_message.get("MESSAGE")}
                else:
                    ld_dict = {"MESSAGE": 'ERROR_OCCURED.' + ld_out_message.get("MESSAGE")}

                return Response(ld_dict)

            elif self.request.query_params.get("Group") == "CUST_All_GET":
                obj_allproduct = mMasters.Masters()
                obj_allproduct.type = self.request.query_params.get("Type")
                obj_allproduct.sub_type = self.request.query_params.get("Sub_Type")
                obj_allproduct.jsonData = json.loads(request.body.decode('utf-8')).get('Params').get('FILTER')
                obj_allproduct.jsonData = json.dumps(obj_allproduct.jsonData)
                obj_allproduct.limit = self.request.query_params.get("Limit")
                obj_allproduct.json_classification = json.loads(request.body.decode('utf-8')).get('Params').get('CLASSIFICATION')
                obj_allproduct.json_classification['Entity_Gid'] = [decry_data(self.request.query_params.get("entity"))]
                obj_allproduct.json_classification = json.dumps(obj_allproduct.json_classification)
                ld_out_message = obj_allproduct.get_AllCustomer()
                if ld_out_message.get("MESSAGE") == 'FOUND':
                    ld_dict = {"DATA": json.loads(ld_out_message.get("DATA").to_json(orient='records')),
                               "MESSAGE": "FOUND"}
                elif ld_out_message.get("MESSAGE") == 'NOT_FOUND':
                    ld_dict = {"MESSAGE": ld_out_message.get("MESSAGE")}
                else:
                    ld_dict = {"MESSAGE": 'ERROR_OCCURED.' + ld_out_message.get("MESSAGE")}

                return Response(ld_dict)
            elif self.request.query_params.get("Group") == "CUSTOMER_ADDRESS":
                obj_allproduct = mMasters.Masters()
                obj_allproduct.type = self.request.query_params.get("Type")
                obj_allproduct.sub_type = self.request.query_params.get("Sub_Type")
                obj_allproduct.jsonData = json.loads(request.body.decode('utf-8')).get('Params').get('FILTER')
                obj_allproduct.jsonData = json.dumps(obj_allproduct.jsonData)
                obj_allproduct.limit = self.request.query_params.get("Limit")
                obj_allproduct.json_classification = json.loads(request.body.decode('utf-8')).get('Params').get('CLASSIFICATION')
                obj_allproduct.json_classification = json.dumps(obj_allproduct.json_classification)
                ld_out_message = obj_allproduct.get_AllCustomer()
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


class common_dataAPI(APIView):
    def get(self,request):
        try:
            common = mMasters.Masters()
            common.table_name = self.request.query_params.get("table_name")
            common.gid = self.request.query_params.get("search_gid")
            common.name = self.request.query_params.get("search_name")
            common.entity_gid = self.request.query_params.get("entity_gid")
            output = common.get_ddl()
            return Response({"MESSAGE": "FOUND","DATA":json.loads(output.to_json(orient='records'))})
        except Exception as e:
            return Response({"MESSAGE": "ERROR_OCCURED", "DATA": str(e)})


class OutstandingCustomer_Get(APIView):
    def post(self,request):
     try:
        obj_collection = mCollection.Collection_model()
        jsondata = json.loads(request.body.decode('utf-8'))
        obj_collection.filter_json = json.dumps(jsondata.get('parms').get('filter'))
        obj_collection.Classification = jsondata.get('parms').get('classification')
        # obj_collection.entity = self.request.query_params.get("entity")
        #obj_collection.Classification['Entity_Gid'] = decry_data(jsondata.get('parms').get('classification').get('Entity_Gid'))
        obj_collection.Classification = json.dumps(obj_collection.Classification)
        obj_collection.type =self.request.query_params.get("Type")
        obj_collection.sub_type =self.request.query_params.get("Sub_Type")
        Output = obj_collection.get_OutstandingCustomer()
        return Response({"MESSAGE": "FOUND","DATA":json.loads(Output.to_json(orient='records'))})
     except Exception as e:
         return Response({"MESSAGE": "ERROR_OCCURED", "DATA": str(e)})

    def get(self,request):
        try:
            obj_collection = mCollection.Collection_model()
            jsondata = '{}'
            obj_collection.filter_json = jsondata
            obj_collection.Classification = jsondata
            obj_collection.type = self.request.query_params.get("Type")
            obj_collection.sub_type = self.request.query_params.get("Sub_Type")
            obj_collection.Classification = json.dumps(jsondata.get('parms').get('classification'))
            # obj_collection.entity = self.request.query_params.get("entity")
            obj_collection.Classification['Entity_Gid'] = decry_data(jsondata.get('parms').get('classification').get('Entity_Gid'))
            obj_collection.Classification = json.dumps(obj_collection.Classification)
            Output = obj_collection.get_OutstandingCustomer()
            return Response(json.loads(Output.to_json(orient='records')))
        except Exception as e:
            return Response({"MESSAGE": "ERROR_OCCURED", "DATA": str(e)})


