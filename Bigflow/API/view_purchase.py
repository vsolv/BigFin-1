

from rest_framework.views import APIView
from rest_framework.response import Response
import json
from Bigflow.Core.models import decrpt as decry_data
from Bigflow.API import views as commonview
from django.http import JsonResponse, HttpResponse
import pandas as pd
from Bigflow.Purchase.Model import mPurchase
from Bigflow.Core.models import MasterRequestObject

import Bigflow.Core.models as common
class Delmat(APIView):
    def post(self,request):
        try:
            if self.request.query_params.get("Type") == "pr_multi":
                path = self.request.stream.path
                jsondata = json.loads(request.body.decode('utf-8'))
                obj_ctrl = mPurchase.Purchase_model()
                obj_ctrl.action = self.request.query_params.get("Action")
                obj_ctrl.type = self.request.query_params.get("Type")
                entity_sync = json.loads(self.request.query_params.get("Entity_Gid"))
                entity = decry_data(entity_sync['entity_gid'])
                obj_ctrl.enty = json.dumps({'entity_gid':entity})
                obj_ctrl.crtby =decry_data(self.request.query_params.get("Employee_Gid"))
                create_by_sync=self.request.query_params.get("Employee_Gid")
                obj_ctrl.array = json.dumps(jsondata)
                common.main_fun1(request.read(), path)
                ld_out_message = obj_ctrl.set_delmatsave()
                #print(jsondata)
                #print('No of Records:',len(jsondata['filtervalue']))
                for data in jsondata['filtervalue']:

                    from Bigflow.Core.models import delmat_tran_to_type
                    data['type']=delmat_tran_to_type(data['delmat_tran'])
                    data = {"commodity_id": str(data['delmat_commoditygid']),
                            "employee_id": str(data['delmat_employeegid']), "limit": str(float(data['delmat_limit'])),
                            'Entity_Gid':entity_sync['entity_gid'],'create_by':create_by_sync,"type":data['type']}
                    if ld_out_message.get("MESSAGE") == 'SUCCESS':
                        ld_dict = {"MESSAGE": "SUCCESS"}
                        if (self.request.query_params.get("Type") == 'pr_multi'):
                            from Bigflow.Core.models import get_data_from_id as gdfi
                            codes=gdfi('DELMAT',data)
                            data.pop('commodity_id')
                            data.pop('employee_id')
                            data['commodity_code']=codes['commodity_code']
                            data['employee_code'] = codes['employee_code']
                            mrobject = MasterRequestObject('DELMAT', data, 'POST')
                    elif ld_out_message.get("MESSAGE") == 'FAIL':
                        ld_dict = {"MESSAGE": ld_out_message.get("MESSAGE")}
                return Response(ld_dict)
            elif self.request.query_params.get("Type") == "UPDATE":
                path = self.request.stream.path
                jsondata = json.loads(request.body.decode('utf-8'))
                obj_ctrl = mPurchase.Purchase_model()
                obj_ctrl.action = self.request.query_params.get("Action")
                obj_ctrl.type = self.request.query_params.get("Type")
                entity = json.loads(self.request.query_params.get("Entity_Gid"))
                entity = decry_data(entity['entity_gid'])
                obj_ctrl.enty = json.dumps({'entity_gid':entity})
                obj_ctrl.crtby = ''
                obj_ctrl.array = json.dumps(jsondata)
                common.main_fun1(request.read(), path)
                ld_out_message = obj_ctrl.set_delmatsave()
                if ld_out_message.get("MESSAGE") == 'SUCCESS':
                    ld_dict = {"MESSAGE": "SUCCESS"}
                elif ld_out_message.get("MESSAGE") == 'FAIL':
                    ld_dict = {"MESSAGE": ld_out_message.get("MESSAGE")}
                return Response(ld_dict)
            elif self.request.query_params.get("Action") == "get" or self.request.query_params.get(
                    "Action") == "get_po":
                path = self.request.stream.path
                obj_ctrl = mPurchase.Purchase_model()
                obj_ctrl.action = self.request.query_params.get("Action")
                obj_ctrl.enty = decry_data(self.request.query_params.get("Entity_Gid"))
                common.main_fun1(request.read(), path)
                ld_out_message = obj_ctrl.set_delmatget()
                ld_dict = {"DATA": json.loads(ld_out_message.to_json(orient='records'))}
                return Response(ld_dict)
            elif self.request.query_params.get("Type") == "pr_update":
                path = self.request.stream.path
                jsondata = json.loads(request.body.decode('utf-8'))
                obj_ctrl = mPurchase.Purchase_model()
                obj_ctrl.action = self.request.query_params.get("Action")
                obj_ctrl.type = self.request.query_params.get("Type")
                entity = json.loads(self.request.query_params.get("Entity_Gid"))
                entity = decry_data(entity['entity_gid'])
                obj_ctrl.enty = json.dumps({'entity_gid': entity})
                obj_ctrl.crtby = decry_data(self.request.query_params.get("Employee_Gid"))
                obj_ctrl.array = json.dumps(jsondata)
                common.main_fun1(request.read(), path)
                ld_out_message = obj_ctrl.set_delmatupdate()
                if ld_out_message.get("MESSAGE") == 'SUCCESSFULLY UPDATED':
                    ld_dict = {"MESSAGE": "SUCCESS"}
                elif ld_out_message.get("MESSAGE") == 'FAIL':
                    ld_dict = {"MESSAGE": ld_out_message.get("MESSAGE")}
                else:
                    dal=ld_out_message.get("MESSAGE")
                    ld_dict = {"MESSAGE": 'Alredy Exist',"Emp":dal}
                return Response(ld_dict)
        except Exception as e:
            common.logger.error(e)
            return Response({"MESSAGE":"ERROR_OCCURED","DATA":str(e)})
        #except:
        #traceback.print_exc()
class PR_Header_DDl(APIView):
    def post(self, request):
        try:
            if self.request.query_params.get("Action") == "get":
                path = self.request.stream.path
                jsondata = json.loads(request.body.decode('utf-8'))
                obj_ctrl = mPurchase.Purchase_model()
                obj_ctrl.action = self.request.query_params.get("Action")
                obj_ctrl.data = json.dumps(jsondata.get('Params').get('FILTER'))
                obj_ctrl.Entity_gid =jsondata.get('Params').get('CLASSIFICATION').get('Entity_gid')
                obj_ctrl.Entity_gid['entity_gid'] =decry_data(  obj_ctrl.Entity_gid['entity_gid'] )
                obj_ctrl.Entity_gid =json.dumps(jsondata.get('Params').get('CLASSIFICATION').get('Entity_gid'))
                obj_ctrl.Employee_gid = decry_data(jsondata.get('Params').get('CLASSIFICATION').get('Employee_gid'))
                common.main_fun1(request.read(), path)
                ld_out_message = obj_ctrl.get_prheader()
                if ld_out_message.get("MESSAGE") == 'FOUND':
                    ld_dict = {"DATA": json.loads(ld_out_message.get("DATA").to_json(orient='records')),
                               "MESSAGE": "FOUND"}
                elif ld_out_message.get("MESSAGE") == 'NOT_FOUND':
                    ld_dict = {"MESSAGE": ld_out_message.get("MESSAGE")}
                else:
                    ld_dict = {"MESSAGE": 'ERROR_OCCURED.' + ld_out_message.get("MESSAGE")}
                return Response(ld_dict)
        except Exception as e:
            common.logger.error(e)
            return Response({"MESSAGE": "ERROR_OCCURED", "DATA": str(e)})



class Mep_In_PR(APIView):
    def post(self,request):
        try:
            if self.request.query_params.get("Group") == "PR_MEP":
                jsondata = json.loads(request.body.decode('utf-8'))
                obj_ctrl = mPurchase.Purchase_model()
                obj_ctrl.type = self.request.query_params.get("Type")
                obj_ctrl.sub_type = self.request.query_params.get("SubType")
                obj_ctrl.jsonData = json.dumps(jsondata.get('FILTER'))
                obj_ctrl.json_classification = jsondata.get('CLASSIFICATION')
                obj_ctrl.json_classification['Entity_Gid'] = decry_data(obj_ctrl.json_classification['Entity_Gid'])
                obj_ctrl.json_classification= json.dumps(jsondata.get('CLASSIFICATION'))
                ld_out_message = obj_ctrl.mep_pr()
                    # for i in json.loads(mep_detail):
                    #     for j in mep_product:
                    #         if i['mepdetails_productgid'] == j:
                    #             print(i['mepdetails_productgid'])
                                # pr_details.loc[(pr_details.prdetails_product_gid == j), 'MEP_amt_pd'] = i['mepdetails_totalamt']
                    # pr_details['Balance_pd_mepamt'] = pr_details['MEP_amt_pd'] - pr_details['total_qty']
                if ld_out_message.get("MESSAGE") == 'FOUND':
                    ld_dict = ld_out_message
                else:
                    ld_dict = {"MESSAGE": 'ERROR_OCCURED.' + ld_out_message.get("MESSAGE")}
                return Response(ld_dict)
            elif self.request.query_params.get("Group") == "MEP_PRODUCTLIST":
                jsondata = json.loads(request.body.decode('utf-8'))
                obj_ctrl = mPurchase.Purchase_model()
                obj_ctrl.type = self.request.query_params.get("Type")
                obj_ctrl.sub_type = self.request.query_params.get("SubType")
                obj_ctrl.jsonData = json.dumps(jsondata.get('FILTER'))
                obj_ctrl.json_classification = jsondata.get('CLASSIFICATION')
                obj_ctrl.json_classification['Entity_Gid'] = decry_data(obj_ctrl.json_classification['Entity_Gid'])
                obj_ctrl.json_classification= json.dumps(jsondata.get('CLASSIFICATION'))
                ld_out_message = obj_ctrl.mep_pr()
                    # for i in json.loads(mep_detail):
                    #     for j in mep_product:
                    #         if i['mepdetails_productgid'] == j:
                    #             print(i['mepdetails_productgid'])
                                # pr_details.loc[(pr_details.prdetails_product_gid == j), 'MEP_amt_pd'] = i['mepdetails_totalamt']
                    # pr_details['Balance_pd_mepamt'] = pr_details['MEP_amt_pd'] - pr_details['total_qty']
                if ld_out_message.get("MESSAGE") == 'FOUND':

                    ld_dict = {"DATA":json.loads(ld_out_message.get("DATA").to_json(orient='records')),
                               "MESSAGE": "FOUND"}
                else:
                    ld_dict = {"MESSAGE": 'ERROR_OCCURED.' + ld_out_message.get("MESSAGE")}
                return Response(ld_dict)
        except Exception as e:
            common.logger.error(e)
            return Response({"MESSAGE": "ERROR_OCCURED", "DATA": str(e)})

class PO_HeaderDDl(APIView):
    def post(self,request):
        try:
            if self.request.query_params.get("Action") == "Get":
                path=request.stream.path
                jsondata = json.loads(request.body.decode('utf-8'))
                obj_ctrl = mPurchase.Purchase_model()
                obj_ctrl.type = self.request.query_params.get("Type")
                obj_ctrl.action = self.request.query_params.get("Action")
                obj_ctrl.jsonData = json.dumps(jsondata.get('Params').get('filter'))
                obj_ctrl.json_classification = jsondata.get('Params').get('CLASSIFICATION')
                obj_ctrl.json_classification['Entity_Gid']=decry_data(obj_ctrl.json_classification['Entity_Gid'])
                common.main_fun1(request.read(), path)
                ld_out_message = obj_ctrl.PO_HeaderDDL()
                if ld_out_message.get("MESSAGE") == 'FOUND':
                    if self.request.query_params.get("Type") == "ASSET_DETAILS":
                       return generate_asst(ld_out_message.get("DATA"))
                    elif self.request.query_params.get("Type") == "ASSET_HEADER":
                       return generate_asst(ld_out_message.get("DATA"))

                    else:
                         ld_dict = {"DATA": json.loads(ld_out_message.get("DATA").to_json(orient='records')),
                               "MESSAGE": "FOUND"}
                elif ld_out_message.get("MESSAGE") == 'NOT_FOUND':
                    ld_dict = {"MESSAGE": ld_out_message.get("MESSAGE")}
                else:
                    ld_dict = {"MESSAGE": 'ERROR_OCCURED.' + ld_out_message.get("MESSAGE")}
                return Response(ld_dict)

            elif self.request.query_params.get("Action") == "GRN":
                path = request.stream.path
                jsondata = json.loads(request.body.decode('utf-8'))
                obj_ctrl = mPurchase.Purchase_model()
                obj_ctrl.type = self.request.query_params.get("Type")
                obj_ctrl.action = self.request.query_params.get("Sub_type")
                obj_ctrl.jsonData = json.dumps(jsondata.get('Params').get('filter'))
                obj_ctrl.json_classification = jsondata.get('Params').get('CLASSIFICATION')
                obj_ctrl.json_classification['Entity_Gid'] = decry_data(obj_ctrl.json_classification['Entity_Gid'])
                common.main_fun1(request.read(), path)
                ld_out_message = obj_ctrl.PO_HeaderDDL()
                if ld_out_message.get("MESSAGE") == 'FOUND':
                    ld_dict = {"DATA": json.loads(ld_out_message.get("DATA").to_json(orient='records')),
                               "MESSAGE": "FOUND"}
                elif ld_out_message.get("MESSAGE") == 'NOT_FOUND':
                    ld_dict = {"MESSAGE": ld_out_message.get("MESSAGE")}
                else:
                    ld_dict = {"MESSAGE": 'ERROR_OCCURED.' + ld_out_message.get("MESSAGE")}

            return Response(ld_dict)
        except Exception as e:
            common.logger.error(e)
            return Response({"MESSAGE": "ERROR_OCCURED", "DATA": str(e)})


class Alltable_ccbs(APIView):
    def post(self,request):
        try:
            if(request.method=='POST'):

                object_query = mPurchase.Purchase_model()
                jsondata = json.loads(request.body.decode('utf-8'))
                object_query.action = self.request.query_params.get("Action")
                object_query.enty = self.request.query_params.get("Entity_Gid")
                # object_query.json_classification = json.dumps(jsondata.get('Params').get('Classification'))
                object_query.jdata = json.dumps(jsondata)
                ld_out_message = object_query.alltable_data()
                if ld_out_message.get("MESSAGE") == 'FOUND':
                    ld_dict = {"DATA": json.loads(ld_out_message.get("DATA").to_json(orient='records')),
                               "MESSAGE": "FOUND"}
                elif ld_out_message.get("MESSAGE") == 'NOT_FOUND':
                    ld_dict = {"MESSAGE": ld_out_message.get("MESSAGE")}
                else:
                    ld_dict = {"MESSAGE": 'ERROR_OCCURED.' + ld_out_message.get("MESSAGE")}

                return Response(ld_dict)


        except Exception as e:
            common.logger.error(e)
            return Response({"MESSAGE": "ERROR_OCCURED", "DATA": str(e)})


class Grn_Details(APIView):
   def post(self,request):
       try:
           if(request.method=='POST'):
               path = request.path
               jsondata = json.loads(request.body.decode('utf-8'))
               object_query = mPurchase.Purchase_model()
               object_query.type=self.request.query_params.get('type')
               object_query.sub_type=self.request.query_params.get('sub_type')
               object_query.filter_json= jsondata
               common.main_fun1(request.read(),path)
               result=object_query.grndetails_get_()
               json_data = json.loads(result.to_json(orient='records'))
               return Response(json_data)
       except Exception as e:
           common.logger.error(e)
           return Response({"MESSAGE": "ERROR_OCCURED", "DATA": str(e)})

class Expense_Line_API(APIView):
   def post(self,request):
       try:
           if(request.method=='POST'):
               object_query = mPurchase.Purchase_model()
               if(self.request.query_params.get("action") == 'INSERT') and (self.request.query_params.get("type") == 'INSERT_EXPENSE_LINE'):
                   object_query.action=self.request.query_params.get('action')
                   object_query.type=self.request.query_params.get('type')
                   object_query.filter=json.dumps(self.request.data.get("params").get("filter"))
                   object_query.classification=json.dumps(self.request.data.get("params").get("classification"))
                   object_query.create_by=self.request.query_params.get("create_by")
                   result=object_query.set_expense_line()
                   return Response(result)
               elif (self.request.query_params.get("action") == 'GET') and (self.request.query_params.get("type") == 'EXPENSE_LINE'):
                   object_query.action = self.request.query_params.get('action')
                   object_query.type = self.request.query_params.get('type')
                   clasification = decry_data(self.request.data.get("params").get("classification").get("Entity_Gid"))
                   object_query.classification = json.dumps({'Entity_Gid':clasification})
                   result = object_query.get_expense_line()
                   json_data = json.loads(result.to_json(orient='records'))
                   return Response(json_data)
               elif (self.request.query_params.get("action") == 'UPDATE') and (self.request.query_params.get("type") == 'UPDATE_EXPENSE_LINE'):
                   object_query.action = self.request.query_params.get('action')
                   object_query.type = self.request.query_params.get('type')
                   object_query.filter = json.dumps(self.request.data.get("params").get("filter"))
                   object_query.classification = json.dumps(self.request.data.get("params").get("classification"))
                   object_query.create_by = self.request.query_params.get("create_by")
                   result = object_query.set_expense_line()
                   return Response(result)
       except Exception as e:
           common.logger.error(e)
           return Response({"MESSAGE": "ERROR_OCCURED", "DATA": str(e)})


class Get_allreport(APIView):
   def post(self,request):
       try:
           if(request.method=='POST'):
               jsondata = json.loads(request.body.decode('utf-8'))
               object_query = mPurchase.Purchase_model()
               if(self.request.query_params.get("Action") == 'Overall_Report'):
                   object_query.action=self.request.query_params.get('Action')
                   object_query.jsondata = json.dumps(jsondata.get("Params").get('FILTER'))
                   object_query.classification = jsondata.get("Params").get("CLASSIFICATION")
                   decpt=decry_data(object_query.classification['Entity_Gid'])
                   object_query.classification['Entity_Gid'] = int(decpt)
                   object_query.classification = json.dumps(object_query.classification)
                   # common.main_fun1(request.read(), path)
                   result=object_query.get_reportdatas()
                   ld_dict = {"DATA": json.loads(result.to_json(orient='records')),
                                  "MESSAGE": "FOUND"}
                   return Response(ld_dict)

       except Exception as e:
           common.logger.error(e)
           return Response({"MESSAGE": "ERROR_OCCURED", "DATA": str(e)})


class Set_Poterms(APIView):
   def post(self,request):
       try:
           if(request.method=='POST'):
               path=request.stream.path
               jsondata = json.loads(request.body.decode('utf-8'))
               object_query = mPurchase.Purchase_model()
               if(self.request.query_params.get("Action") == 'INSERT') and (self.request.query_params.get("Type") == 'PO_TERMS'):
                   object_query.action=self.request.query_params.get('Action')
                   object_query.type=self.request.query_params.get('Type')
                   object_query.jsondata=json.dumps(jsondata.get("Params"))
                   object_query.classification = jsondata.get("CLASSIFICATION")
                   decpt = decry_data(object_query.classification['Entity_Gid'])
                   object_query.classification['Entity_Gid'] = [int(decpt)]
                   object_query.classification = json.dumps(object_query.classification)
                   object_query.create_by = decry_data(self.request.query_params.get("create_by"))
                   # common.main_fun1(request.read(), path)
                   result=object_query.set_poterms()
                   return Response(result)
               if (self.request.query_params.get("Action") == 'INSERT') and (
                       self.request.query_params.get("Type") == 'PO_TERMS_TEMPLATE'):
                   object_query.action = self.request.query_params.get('Action')
                   object_query.type = self.request.query_params.get('Type')
                   object_query.jsondata = json.dumps(jsondata.get("Params"))
                   object_query.classification = jsondata.get("CLASSIFICATION")
                   decpt = decry_data(object_query.classification['Entity_Gid'])
                   object_query.classification['Entity_Gid'] = [int(decpt)]
                   object_query.classification = json.dumps(object_query.classification)
                   object_query.create_by = decry_data(self.request.query_params.get("create_by"))
                   # common.main_fun1(request.read(), path)
                   result = object_query.set_poterms_temp()
                   return Response({"DATA": result})
               elif(self.request.query_params.get("Action") == 'GET_ALLTEMPLATE') or (self.request.query_params.get("Action") == 'GET_ALLTERM') or (self.request.query_params.get("Action") == 'VIEW_ALLTEMPLATE'):

                   object_query.action=self.request.query_params.get('Action')
                   object_query.type=self.request.query_params.get('Type')
                   object_query.jsondata = json.dumps(jsondata.get("Params"))
                   # object_query.classification=json.dumps(jsondata.get("CLASSIFICATION"))
                   # object_query.create_by=self.request.query_params.get("create_by")
                   object_query.classification = jsondata.get("CLASSIFICATION")
                   decpt=decry_data(object_query.classification['Entity_Gid'])
                   object_query.classification['Entity_Gid'] = [int(decpt)]

                   object_query.classification = json.dumps(object_query.classification)
                   # print(object_query.classification)
                   object_query.create_by = decry_data(self.request.query_params.get("create_by"))
                   # .create_by = decry_data(create_by)
                   # common.main_fun1(request.read(), path)
                   result=object_query.get_poterms()
                   ld_dict = {"DATA": json.loads(result.to_json(orient='records')),
                                  "MESSAGE": "FOUND"}
                   return Response(ld_dict)

       except Exception as e:
           common.logger.error(e)
           return Response({"MESSAGE": "ERROR_OCCURED", "DATA": str(e)})

class Get_Poamend(APIView):
   def post(self,request):
       try:
           if(request.method=='POST'):
               path=request.stream.path
               jsondata = json.loads(request.body.decode('utf-8'))
               object_query = mPurchase.Purchase_model()
               if self.request.query_params.get("Group") == 'AMENDMENT_SUMMARY':
                   object_query.action=self.request.query_params.get('Action')
                   object_query.type=self.request.query_params.get('Type')
                   object_query.jsondata= json.dumps(jsondata.get("FILTER"))
                   object_query.classification = jsondata.get("CLASSIFICATION")
                   decpt = decry_data(object_query.classification['Entity_Gid'])
                   object_query.classification['Entity_Gid'] = decpt
                   object_query.classification = json.dumps(object_query.classification)
                   object_query.create_by = decry_data(self.request.query_params.get("create_by"))
                   result=object_query.get_poamend()
                   ld_dict = {"DATA": json.loads(result.to_json(orient='records')),
                              "MESSAGE": "FOUND"}
                   return Response(ld_dict)
               elif self.request.query_params.get("Group") == 'MODIFICATION_AMENDMENT':
                   object_query.action = self.request.query_params.get('Action')
                   object_query.type = self.request.query_params.get('Type')
                   object_query.jsondata = json.dumps(jsondata.get("FILTER"))
                   object_query.classification = jsondata.get("CLASSIFICATION")
                   decpt = decry_data(object_query.classification['Entity_Gid'])
                   object_query.classification['Entity_Gid'] = decpt
                   object_query.classification = json.dumps(object_query.classification)
                   object_query.create_by = decry_data(self.request.query_params.get("create_by"))
                   result = object_query.get_poamend()
                   ld_dict = {"DATA": json.loads(result.to_json(orient='records')),
                              "MESSAGE": "FOUND"}
                   return Response(ld_dict)
               elif self.request.query_params.get("Group") == 'UPDATE_AMENDMENT':
                   object_query.action = self.request.query_params.get('Action')
                   object_query.type = self.request.query_params.get('Type')
                   object_query.jsondata = json.dumps(jsondata.get("FILTER"))
                   object_query.classification = jsondata.get("CLASSIFICATION")
                   decpt = decry_data(object_query.classification['Entity_Gid'])
                   object_query.classification['Entity_Gid'] = decpt
                   object_query.classification = json.dumps(object_query.classification)
                   object_query.create_by = decry_data(self.request.query_params.get("create_by"))
                   result = object_query.set_poamend()
                   ld_dict = {"DATA": result,
                              "MESSAGE": result[0]}
                   return Response(ld_dict)

       except Exception as e:
           common.logger.error(e)
           return Response({"MESSAGE": "ERROR_OCCURED", "DATA": str(e)})



from reportlab.graphics.barcode import code128
from reportlab.lib.units import mm
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
import boto3
from io import  BytesIO
import barcode
# from barcode.writer import ImageWriter
from io import StringIO # python3; python2: BytesIO
import boto3
bucket = 'my_bucket_name' # already created on S3
csv_buffer = StringIO()
import tempfile
import os
def generate_asst(df1):
    df=pd.DataFrame()
    pdf = BytesIO()
    df=df1['assetid_assetid']
    # print(df)
    list_of_images = []
    codeName=[]
    for k in df:
        codeName.append(str(k))
    #     for i in codeName:
    pdf = BytesIO()
    c = canvas.Canvas(pdf, pagesize=letter)
    margin_x = 7.526
    margin_y = 13.876
    padding_x = 7.526
    font_size = 15
    width, height = letter
    extra_padding = 20

    bars_width = (float(width - margin_x * 2) - 3 * padding_x) / 4
    bars_height = float(height - margin_y * 2) / 15
    bar_height = bars_height - font_size
    z = 0
    for j in range(len(codeName)):

        try:
            for i in range(0, 4):
                bar_width = (bars_width - extra_padding) / (len(codeName[z]) * 11 + 35)
                barcode128 = code128.Code128(
                    codeName[z],
                    barHeight=bar_height,
                    barWidth=bar_width,
                    humanReadable=True)
                x = margin_x + i * (bars_width + padding_x)
                y = margin_y + j * bars_height
                barcode128.drawOn(c, x, y)
                z = z + 1
        except:
            break

    filename = c.save()
    p = pdf.getvalue()
    # print(p)
    s3 = boto3.resource('s3')

    s3_obj = s3.Object(bucket_name=common.s3_bucket_name(), key="asd.pdf").put(Body=p)
    #     s3_client = boto3.client('s3')
    s3_client =boto3.client('s3','ap-south-1')
    response = s3_client.generate_presigned_url('get_object',
    Params={'Bucket': common.s3_bucket_name(), 'Key': "asd.pdf",

            "ResponseContentType": 'application/pdf',

            }, ExpiresIn=3000)
    # print(response)
    list_of_images.append({"imagepath":response})
    df=pd.DataFrame(list_of_images)
    df=json.loads(df.to_json(orient='records'))
    # print(df)
    # return fullname
    return JsonResponse(df,safe=False)


class Tran_History_Get(APIView):
    def post(self,request):
        try:
            if self.request.query_params.get("Group") == "PR_HISTORY" or "PO_HISTORY" or "POCANCEL_HISTORY" or "POCLOSE_HISTORY" or "GRN_HISTORY":
                jsondata = json.loads(request.body.decode('utf-8'))
                obj_ctrl = mPurchase.Purchase_model()
                obj_ctrl.type = self.request.query_params.get("Type")
                obj_ctrl.sub_type = self.request.query_params.get("SubType")
                obj_ctrl.jsonData = json.dumps(jsondata.get('DETAIL'))
                obj_ctrl.json_classification = jsondata.get('CLASSIFICATION')
                obj_ctrl.json_classification['Entity_Gid'] = decry_data(obj_ctrl.json_classification['Entity_Gid'])
                obj_ctrl.json_classification= json.dumps(jsondata.get('CLASSIFICATION'))
                ld_out_message = obj_ctrl.get_trandata()
                if ld_out_message.get("MESSAGE") == 'FOUND':
                    ld_dict = {"DATA": json.loads(ld_out_message.get("DATA").to_json(orient='records')),
                               "MESSAGE": "FOUND"}
                else:
                    ld_dict = {"MESSAGE": 'ERROR_OCCURED.' + ld_out_message.get("MESSAGE")}
                return Response(ld_dict)
            elif self.request.query_params.get("Group") == "MEP_PRODUCTLIST":
                jsondata = json.loads(request.body.decode('utf-8'))
                obj_ctrl = mPurchase.Purchase_model()
                obj_ctrl.type = self.request.query_params.get("Type")
                obj_ctrl.sub_type = self.request.query_params.get("SubType")
                obj_ctrl.jsonData = json.dumps(jsondata.get('FILTER'))
                obj_ctrl.json_classification = jsondata.get('CLASSIFICATION')
                obj_ctrl.json_classification['Entity_Gid'] = decry_data(obj_ctrl.json_classification['Entity_Gid'])
                obj_ctrl.json_classification= json.dumps(jsondata.get('CLASSIFICATION'))
                ld_out_message = obj_ctrl.mep_pr()
                if ld_out_message.get("MESSAGE") == 'FOUND':

                    ld_dict = {"DATA":json.loads(ld_out_message.get("DATA").to_json(orient='records')),
                               "MESSAGE": "FOUND"}
                else:
                    ld_dict = {"MESSAGE": 'ERROR_OCCURED.' + ld_out_message.get("MESSAGE")}
                return Response(ld_dict)
        except Exception as e:
            common.logger.error(e)
            return Response({"MESSAGE": "ERROR_OCCURED", "DATA": str(e)})



class MS_PO_FA_Asset_Make(APIView):
    def post(self,request):
        try:
            if self.request.query_params.get("Group") == "FA_ASSET_MAKE":
                path = self.request.stream.path
                jsondata = json.loads(request.body.decode('utf-8'))
                #
                obj_fa = mPurchase.Purchase_model()
                obj_fa.action = self.request.query_params.get("Action")
                obj_fa.type = self.request.query_params.get("Type")
                obj_fa.sub_type = self.request.query_params.get("Sub_Type")
                obj_fa.employee_gid = self.request.query_params.get("Employee_Gid")
                obj_fa.jsondata = json.dumps(jsondata.get('Params').get('DETAILS'))
                obj_fa.json_file = json.dumps(jsondata.get('Params').get('File'))
                obj_fa.jsonData = json.dumps(jsondata.get('Params').get('CHANGE'))
                obj_fa.jsonData_sec = json.dumps(jsondata.get('Params').get('STATUS'))
                obj_fa.json_classification = json.dumps(jsondata.get('Params').get('CLASSIFICATION'))
                # common.main_fun1(request.read(), path)
                ld_out_message = obj_fa.set_fa_maker_from_ms()
                if ld_out_message.get("MESSAGE") == 'SUCCESS':
                    ld_dict = {"MESSAGE": "SUCCESS"}
                elif ld_out_message.get("MESSAGE") == 'FAIL':
                    ld_dict = {"MESSAGE": "FAIL"}
                else:
                    ld_dict = {"MESSAGE": 'ERROR_OCCURED.' + ld_out_message.get("MESSAGE")}
                return Response(ld_dict)
            elif self.request.query_params.get("Group") == "GRN":
                path = self.request.stream.path
                jsondata = json.loads(request.body.decode('utf-8'))

                obj_fa = mPurchase.Purchase_model()
                obj_fa.action = self.request.query_params.get("Action")
                obj_fa.type = self.request.query_params.get("Type")
                obj_fa.sub_type = self.request.query_params.get("Sub_Type")
                obj_fa.employee_gid = self.request.query_params.get("Employee_Gid")
                obj_fa.jsondata = json.dumps(jsondata.get('Params').get('DETAILS'))
                obj_fa.json_file = json.dumps(jsondata.get('Params').get('File'))
                obj_fa.jsonData = json.dumps(jsondata.get('Params').get('CHANGE'))
                obj_fa.jsonData_sec = json.dumps(jsondata.get('Params').get('STATUS'))
                obj_fa.json_classification = json.dumps(jsondata.get('Params').get('CLASSIFICATION'))
                ld_out_message = obj_fa.set_fa_maker_from_ms()
                ld_dict = {"DATA":ld_out_message}
                return Response(ld_dict)
        except Exception as e:
            common.logger.error(e)
            return Response({"MESSAGE": "ERROR_OCCURED", "DATA": str(e)})

class MS_PO_FA_PO_GET(APIView):
    def post(self,request):
        try:
            if self.request.query_params.get("Action") == "Get":
                path=request.stream.path
                jsondata = json.loads(request.body.decode('utf-8'))
                obj_ctrl = mPurchase.Purchase_model()
                obj_ctrl.type = self.request.query_params.get("Type")
                obj_ctrl.action = self.request.query_params.get("Action")
                obj_ctrl.jsonData = json.dumps(jsondata.get('Params').get('filter'))
                obj_ctrl.json_classification = jsondata.get('Params').get('CLASSIFICATION')
                ld_out_message = obj_ctrl.PO_HeaderDDL()
                if ld_out_message.get("MESSAGE") == 'FOUND':
                     ld_dict = {"DATA": json.loads(ld_out_message.get("DATA").to_json(orient='records')),
                               "MESSAGE": "FOUND"}
                elif ld_out_message.get("MESSAGE") == 'NOT_FOUND':
                    ld_dict = {"MESSAGE": ld_out_message.get("MESSAGE")}
                else:
                    ld_dict = {"MESSAGE": 'ERROR_OCCURED.' + ld_out_message.get("MESSAGE")}
                return Response(ld_dict)

            elif self.request.query_params.get("Action") == "GRN":
                path = request.stream.path
                jsondata = json.loads(request.body.decode('utf-8'))
                obj_ctrl = mPurchase.Purchase_model()
                obj_ctrl.type = self.request.query_params.get("Type")
                obj_ctrl.action = self.request.query_params.get("Sub_type")
                obj_ctrl.jsonData = json.dumps(jsondata.get('Params').get('filter'))
                obj_ctrl.json_classification = jsondata.get('Params').get('CLASSIFICATION')
                ld_out_message = obj_ctrl.PO_HeaderDDL()
                if ld_out_message.get("MESSAGE") == 'FOUND':
                    ld_dict = {"DATA": json.loads(ld_out_message.get("DATA").to_json(orient='records')),
                               "MESSAGE": "FOUND"}
                elif ld_out_message.get("MESSAGE") == 'NOT_FOUND':
                    ld_dict = {"MESSAGE": ld_out_message.get("MESSAGE")}
                else:
                    ld_dict = {"MESSAGE": 'ERROR_OCCURED.' + ld_out_message.get("MESSAGE")}

            return Response(ld_dict)
        except Exception as e:
            common.logger.error(e)
            return Response({"MESSAGE": "ERROR_OCCURED", "DATA": str(e)})