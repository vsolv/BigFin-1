from rest_framework.views import APIView
from rest_framework.response import Response
import json
from Bigflow.Transaction.Model import mFET, mSales
from Bigflow.API import views as commonview
from Bigflow.Core.models import decrpt as decry_data
import Bigflow.Core.models as common
class Query_Summary(APIView):
    def post(self,request):
        try:
            if self.request.query_params.get("Group") == "QUERYSUMMARY":
                jsondata = json.loads(request.body.decode('utf-8'))
                object_query = mSales.Sales_Model()
                object_query.type = self.request.query_params.get("Type")
                object_query.sub_type = self.request.query_params.get("Sub_Type")
                object_query.json_classification = jsondata.get('Params').get('Classification')

                object_query.json_classification['Entity_Gid'] = decry_data(self.request.query_params.get("entity"))
                object_query.json_classification = json.dumps(jsondata.get('Params').get('Classification'))
                object_query.jsonData = json.dumps(jsondata.get('Params').get('Filter'))
                ld_out_message = object_query.get_salesquery_summary()
                if ld_out_message.get("MESSAGE") == 'FOUND':
                    ld_dict = {"DATA": json.loads(ld_out_message.get("DATA").to_json(orient='records')),
                               "MESSAGE": 'FOUND'}
                elif ld_out_message.get("MESSAGE") == 'NOT_FOUND':
                    ld_dict = {"MESSAGE": 'NOT_FOUND'}
                else:
                    ld_dict = {"MESSAGE": 'ERROR_OCCURED.' + ld_out_message.get("MESSAGE")}
                return Response(ld_dict)
        except Exception as e:
            return Response({"MESSAGE": "ERROR_OCCURED", "DATA": str(e)})

class Query_SummaryProduct(APIView):
    def post(self,request):
        try:
            if self.request.query_params.get("Group") == "QUERYSUMMARY":
                jsondata = json.loads(request.body.decode('utf-8'))
                object_query = mSales.Sales_Model()
                object_query.type = self.request.query_params.get("Type")
                object_query.sub_type = self.request.query_params.get("Sub_Type")
                object_query.json_classification = jsondata.get('Params').get('Classification')

                object_query.json_classification['Entity_Gid'] = decry_data( object_query.json_classification['Entity_Gid'])
                object_query.jsonData = json.dumps(jsondata.get('Params').get('Filter'))
                object_query.json_classification = json.dumps(jsondata.get('Params').get('Classification'))
                ld_out_message = object_query.get_salesquery_summaryProduct()
                if ld_out_message.get("MESSAGE") == 'FOUND':
                    ld_dict = {"DATA": json.loads(ld_out_message.get("DATA").to_json(orient='records')),
                               "MESSAGE": 'FOUND'}
                elif ld_out_message.get("MESSAGE") == 'NOT_FOUND':
                    ld_dict = {"MESSAGE": 'NOT_FOUND'}
                else:
                    ld_dict = {"MESSAGE": 'ERROR_OCCURED.' + ld_out_message.get("MESSAGE")}
                return Response(ld_dict)
        except Exception as e:
            return Response({"MESSAGE": "ERROR_OCCURED", "DATA": str(e)})

class Query_SummaryCollection(APIView):
    def post(self,request):
        try:
            if self.request.query_params.get("Group") == "QUERYSUMMARY":
                jsondata = json.loads(request.body.decode('utf-8'))
                object_query = mSales.Sales_Model()
                object_query.action="COLLECTION"
                object_query.type = self.request.query_params.get("Type")
                object_query.sub_type = self.request.query_params.get("Sub_Type")
                object_query.json_classification = jsondata.get('Params').get('Classification')

                object_query.json_classification['Entity_Gid'] = decry_data(self.request.query_params.get("entity"))
                object_query.json_classification = json.dumps(jsondata.get('Params').get('Classification'))
                object_query.jsonData = json.dumps(jsondata.get('Params').get('Filter'))
                ld_out_message = object_query.get_salesquery_summaryCollection()
                if ld_out_message.get("MESSAGE") == 'FOUND':
                    ld_dict = {"DATA": json.loads(ld_out_message.get("DATA").to_json(orient='records')),
                               "MESSAGE": 'FOUND'}
                elif ld_out_message.get("MESSAGE") == 'NOT_FOUND':
                    ld_dict = {"MESSAGE": 'NOT_FOUND'}
                else:
                    ld_dict = {"MESSAGE": 'ERROR_OCCURED.' + ld_out_message.get("MESSAGE")}
                return Response(ld_dict)
        except Exception as e:
            return Response({"MESSAGE": "ERROR_OCCURED", "DATA": str(e)})


class Query_Summarygetcollectionstatus(APIView):
    def post(self,request):
        try:
            if self.request.query_params.get("Group") == "QUERYSUMMARY":
                jsondata = json.loads(request.body.decode('utf-8'))
                object_query = mSales.Sales_Model()
                object_query.action="COLLECTIONSTATUS"
                object_query.type = self.request.query_params.get("Type")
                object_query.sub_type = self.request.query_params.get("Sub_Type")
                object_query.json_classification = jsondata.get('Params').get('Classification')
                object_query.json_classification['Entity_Gid'] = [decry_data(self.request.query_params.get("entity"))]
                object_query.json_classification = json.dumps(jsondata.get('Params').get('Classification'))
                object_query.jsonData = json.dumps(jsondata.get('Params').get('Filter'))
                ld_out_message = object_query.get_salesquery_summaryCollectionStatus()
                if ld_out_message.get("MESSAGE") == 'FOUND':
                    ld_dict = {"DATA": json.loads(ld_out_message.get("DATA").to_json(orient='records')),
                               "MESSAGE": 'FOUND'}
                elif ld_out_message.get("MESSAGE") == 'NOT_FOUND':
                    ld_dict = {"MESSAGE": 'NOT_FOUND'}
                else:
                    ld_dict = {"MESSAGE": 'ERROR_OCCURED.' + ld_out_message.get("MESSAGE")}
                return Response(ld_dict)
        except Exception as e:
            return Response({"MESSAGE": "ERROR_OCCURED", "DATA": str(e)})


class Query_SummaryOutstanding(APIView):
    def post(self,request):
        try:
            if self.request.query_params.get("Group") == "QUERYSUMMARY":
                jsondata = json.loads(request.body.decode('utf-8'))
                object_query = mSales.Sales_Model()
                object_query.action="OUTSTANDING"
                object_query.type = self.request.query_params.get("Type")
                object_query.sub_type = self.request.query_params.get("Sub_Type")
                object_query.json_classification = jsondata.get('Params').get('Classification')
                object_query.json_classification['Entity_Gid'] = decry_data(self.request.query_params.get("entity"))
                object_query.json_classification = json.dumps(jsondata.get('Params').get('Classification'))

                object_query.jsonData = json.dumps(jsondata.get('Params').get('Filter'))
                ld_out_message = object_query.get_salesquery_summaryOutstanding()
                if ld_out_message.get("MESSAGE") == 'FOUND':
                    ld_dict = {"DATA": json.loads(ld_out_message.get("DATA").to_json(orient='records')),
                               "MESSAGE": 'FOUND'}
                elif ld_out_message.get("MESSAGE") == 'NOT_FOUND':
                    ld_dict = {"MESSAGE": 'NOT_FOUND'}
                else:
                    ld_dict = {"MESSAGE": 'ERROR_OCCURED.' + ld_out_message.get("MESSAGE")}
                return Response(ld_dict)
        except Exception as e:
            return Response({"MESSAGE": "ERROR_OCCURED", "DATA": str(e)})


class SalesOrder_Register(APIView):
    def post(self,request):
        try:
            if self.request.query_params.get("Group") == "SO_Register":
                jsondata = json.loads(request.body.decode('utf-8'))
                object_sales = mSales.Sales_Model()
                object_sales.action = self.request.query_params.get("Action")
                object_sales.date = self.request.query_params.get("date")
                object_sales.customer_gid = self.request.query_params.get("cust_gid")
                object_sales.employee_gid = decry_data(self.request.query_params.get("Emp_Gid"))
                object_sales.limit = self.request.query_params.get("limit")
                object_sales.jsonData = jsondata.get('Parms').get('Classification')
                object_sales.jsonData['Entity_Gid'] = [decry_data(self.request.query_params.get("entity"))]
                object_sales.jsonData = json.dumps(jsondata.get('Parms').get('Classification'))
                object_sales.jsondata = json.dumps(jsondata.get('Parms').get('Filter'))
                common.main_fun1(request.read(), request.path)
                output = object_sales.get_sales_order()
                if len(output) > 0: # Remove The Quotes
                    output['so_details'] = output['so_details'].apply(json.loads)

                    return Response({"MESSAGE": "FOUND","DATA":json.loads(output.to_json(orient='records'))})
                else:
                   return Response({"MESSAGE": "NO_DATA"})
            elif self.request.query_params.get("Group") == "SO_Invoice_Register":
                jsondata = json.loads(request.body.decode('utf-8'))
                object_sales = mSales.Sales_Model()
                object_sales.action = self.request.query_params.get("Action")
                object_sales.date = self.request.query_params.get("date")
                object_sales.customer_gid = self.request.query_params.get("cust_gid")
                object_sales.employee_gid = self.request.query_params.get("Emp_Gid")
                object_sales.limit = self.request.query_params.get("limit")
                object_sales.jsonData = jsondata.get('Parms').get('Classification')
                object_sales.jsonData['Entity_Gid'] = [decry_data(self.request.query_params.get("entity"))]
                object_sales.jsonData = json.dumps(jsondata.get('Parms').get('Classification'))
                object_sales.jsondata = json.dumps(jsondata.get('Parms').get('Filter'))
                common.main_fun1(request.read(), request.path)
                output = object_sales.get_sales_order()
                if len(output) > 0:
                    output['Tax_Calculate'] = output['Tax_Calculate'].apply(json.loads)
                    # Remove The Quotes
                    # if output.lj_campaign != 'FAIL':
                    output['lj_campaign'] = output['lj_campaign'].apply(json.loads)
                    # output = output[output.lj_campaign != 'FAIL']
                    return Response({"MESSAGE": "FOUND", "DATA": json.loads(output.to_json(orient='records'))})
                else:
                    return Response({"MESSAGE": "NO_DATA"})
        except Exception as e:
            return Response({"MESSAGE": "ERROR_OCCURED", "DATA": str(e)})


##### MASTER
class Dealer_Price_API(APIView):
    def post(self,request):
        try:
            if self.request.query_params.get("Group") == "SUMMARY":
                jsondata = json.loads(request.body.decode('utf-8'))
                obj_dealerprice = mSales.Sales_Model()
                obj_dealerprice.type = self.request.query_params.get("Type")
                obj_dealerprice.entity = self.request.query_params.get("entity")
                obj_dealerprice.sub_type = self.request.query_params.get("Sub_Type")
                obj_dealerprice.jsonData = json.dumps(jsondata.get('Params').get('FILTER'))
                obj_dealerprice.json_classification = jsondata.get('Params').get('CLASSIFICATION')
                obj_dealerprice.entity = self.request.query_params.get("entity")
                obj_dealerprice.json_classification['entity_gid'] =decry_data(obj_dealerprice.entity  )
                obj_dealerprice.create_by = decry_data(self.request.query_params.get("Employee_Gid"))
                obj_dealerprice.json_classification =json.dumps(jsondata.get('Params').get('CLASSIFICATION'))
                common.main_fun1(request.read(), request.path)
                ld_out_message = obj_dealerprice.get_dealer_price()

                if ld_out_message.get("MESSAGE") == 'FOUND':
                    ld_dict = {"DATA":json.loads(ld_out_message.get("DATA").to_json(orient='records')),"MESSAGE":"FOUND"}
                elif ld_out_message.get("MESSAGE") == 'NOT_FOUND':
                    ld_dict = {"MESSAGE":ld_out_message.get("MESSAGE")}
                else:
                    ld_dict = {"MESSAGE":'ERROR_OCCURED.' + ld_out_message.get("MESSAGE")}

                return Response(ld_dict)

            elif self.request.query_params.get("Group") == "MAKER":
                jsondata = json.loads(request.body.decode('utf-8'))
                obj_dealerprice = mSales.Sales_Model()
                obj_dealerprice.action = self.request.query_params.get("Action")
                obj_dealerprice.type = self.request.query_params.get("Type")
                obj_dealerprice.jsonData = json.dumps(jsondata.get('Params').get('DATA'))
                obj_dealerprice.json_classification = jsondata.get('Params').get('CLASSIFICATION')
                obj_dealerprice.entity = self.request.query_params.get("entity")
                obj_dealerprice.json_classification['Entity_Gid'] = decry_data(obj_dealerprice.entity)
                obj_dealerprice.create_by = decry_data(self.request.query_params.get("Employee_Gid"))
                obj_dealerprice.json_classification = json.dumps(jsondata.get('Params').get('CLASSIFICATION'))
                common.main_fun1(request.read(), request.path)
                ld_out_message = obj_dealerprice.set_dealer_price()

                if ld_out_message.get("MESSAGE") == 'SUCCESS':
                    ld_dict = {"MESSAGE":"SUCCESS"}
                elif ld_out_message.get("MESSAGE") == 'FAIL':
                    ld_dict = {"MESSAGE":ld_out_message.get("MESSAGE")}
                else:
                    ld_dict = {"MESSAGE":'ERROR_OCCURED.' + ld_out_message.get("MESSAGE")}

                return Response(ld_dict)

            elif self.request.query_params.get("Group") == "STATUS":

                jsondata = json.loads(request.body.decode('utf-8'))
                obj_dealerprice = mSales.Sales_Model()
                obj_dealerprice.action = self.request.query_params.get("Action")
                obj_dealerprice.type = self.request.query_params.get("Type")
                obj_dealerprice.jsonData = json.dumps(jsondata.get('Params').get('DATA'))
                obj_dealerprice.json_classification = jsondata.get('Params').get('CLASSIFICATION')
                obj_dealerprice.entity = self.request.query_params.get("entity")
                obj_dealerprice.json_classification['entity_gid'] = decry_data(obj_dealerprice.entity)
                obj_dealerprice.create_by = decry_data(self.request.query_params.get("Employee_Gid"))
                obj_dealerprice.json_classification = json.dumps(jsondata.get('Params').get('CLASSIFICATION'))
                common.main_fun1(request.read(), request.path)
                ld_out_message = obj_dealerprice.set_dealer_price()

                if ld_out_message.get("MESSAGE") == 'SUCCESS':
                    ld_dict = {"MESSAGE": "SUCCESS"}
                elif ld_out_message.get("MESSAGE") == 'FAIL':
                    ld_dict = {"MESSAGE": ld_out_message.get("MESSAGE")}
                else:
                    ld_dict = {"MESSAGE": 'ERROR_OCCURED.' + ld_out_message.get("MESSAGE")}

                return Response(ld_dict)

            elif self.request.query_params.get("Group") == "DEALER_PRICE_UNIQUE":
                jsondata = json.loads(request.body.decode('utf-8'))
                obj_dealerprice = mSales.Sales_Model()

                obj_dealerprice.type = self.request.query_params.get("Type")
                obj_dealerprice.sub_type = self.request.query_params.get("Sub_Type")
                obj_dealerprice.jsonData = json.dumps(jsondata.get('Params').get('FILTER'))
                obj_dealerprice.json_classification = jsondata.get('Params').get('CLASSIFICATION')
                obj_dealerprice.entity = self.request.query_params.get("entity")
                obj_dealerprice.json_classification['entity_gid'] = decry_data(obj_dealerprice.entity)
                obj_dealerprice.create_by = decry_data(self.request.query_params.get("Employee_Gid"))
                obj_dealerprice.json_classification = json.dumps(jsondata.get('Params').get('CLASSIFICATION'))
                common.main_fun1(request.read(), request.path)
                ld_out_message = obj_dealerprice.get_dealer_price()

                if ld_out_message.get("MESSAGE") == 'FOUND':
                    ld_dict = {"DATA":json.loads(ld_out_message.get("DATA").to_json(orient='records')),"MESSAGE":"FOUND"}
                elif ld_out_message.get("MESSAGE") == 'NOT_FOUND':
                    ld_dict = {"MESSAGE":ld_out_message.get("MESSAGE")}
                else:
                    ld_dict = {"MESSAGE":'ERROR_OCCURED.' + ld_out_message.get("MESSAGE")}

                return Response(ld_dict)
        except Exception as e:
            return Response({"MESSAGE": "ERROR_OCCURED", "DATA": str(e)})

class Rate_Card_API(APIView):
    def post(self,request):
        try:
            if self.request.query_params.get("Group") == "SUMMARY":
                jsondata = json.loads(request.body.decode('utf-8'))
                obj_dealerprice = mSales.Sales_Model()

                obj_dealerprice.type = self.request.query_params.get("Type")
                obj_dealerprice.sub_type = self.request.query_params.get("Sub_Type")
                obj_dealerprice.jsonData = json.dumps(jsondata.get('Params').get('FILTER'))
                obj_dealerprice.json_classification = jsondata.get('Params').get('CLASSIFICATION')
                obj_dealerprice.entity = self.request.query_params.get("entity")
                obj_dealerprice.json_classification['Entity_Gid'] = decry_data(obj_dealerprice.entity)
                obj_dealerprice.json_classification = json.dumps(obj_dealerprice.json_classification)
                obj_dealerprice.create_by = decry_data(self.request.query_params.get("Employee_Gid"))
                common.main_fun1(request.read(), request.path)
                ld_out_message = obj_dealerprice.get_rate_card()

                if ld_out_message.get("MESSAGE") == 'FOUND':
                    ld_dict = {"DATA":json.loads(ld_out_message.get("DATA").to_json(orient='records')),"MESSAGE":"FOUND"}
                elif ld_out_message.get("MESSAGE") == 'NOT_FOUND':
                    ld_dict = {"MESSAGE":ld_out_message.get("MESSAGE")}
                else:
                    ld_dict = {"MESSAGE":'ERROR_OCCURED.' + ld_out_message.get("MESSAGE")}

                return Response(ld_dict)

            elif self.request.query_params.get("Group") == "MAKER":
                jsondata = json.loads(request.body.decode('utf-8'))
                obj_dealerprice = mSales.Sales_Model()
                obj_dealerprice.action = self.request.query_params.get("Action")
                obj_dealerprice.type = self.request.query_params.get("Type")
                obj_dealerprice.jsonData = json.dumps(jsondata.get('Params').get('DATA'))
                obj_dealerprice.json_classification = jsondata.get('Params').get('CLASSIFICATION')
                obj_dealerprice.entity = self.request.query_params.get("entity")
                obj_dealerprice.json_classification['Entity_Gid'] = decry_data(obj_dealerprice.entity)
                obj_dealerprice.json_classification = json.dumps(obj_dealerprice.json_classification)
                obj_dealerprice.create_by = decry_data(self.request.query_params.get("Employee_Gid"))

                ld_out_message = obj_dealerprice.set_rate_card()

                if ld_out_message.get("MESSAGE") == 'SUCCESS':
                    ld_dict = {"MESSAGE":"SUCCESS"}
                elif ld_out_message.get("MESSAGE") == 'FAIL':
                    ld_dict = {"MESSAGE":ld_out_message.get("MESSAGE")}
                else:
                    ld_dict = {"MESSAGE":'ERROR_OCCURED.' + ld_out_message.get("MESSAGE")}

                return Response(ld_dict)

            elif self.request.query_params.get("Group") == "STATUS":

                jsondata = json.loads(request.body.decode('utf-8'))
                obj_dealerprice = mSales.Sales_Model()
                obj_dealerprice.action = self.request.query_params.get("Action")
                obj_dealerprice.type = self.request.query_params.get("Type")
                obj_dealerprice.jsonData = json.dumps(jsondata.get('Params').get('DATA'))
                obj_dealerprice.json_classification = jsondata.get('Params').get('CLASSIFICATION')
                obj_dealerprice.entity = self.request.query_params.get("entity")
                obj_dealerprice.json_classification['Entity_Gid'] = decry_data(obj_dealerprice.entity)
                obj_dealerprice.json_classification = json.dumps(obj_dealerprice.json_classification)
                obj_dealerprice.create_by = decry_data(self.request.query_params.get("Employee_Gid"))

                ld_out_message = obj_dealerprice.set_rate_card()

                if ld_out_message.get("MESSAGE") == 'SUCCESS':
                    ld_dict = {"MESSAGE": "SUCCESS"}
                elif ld_out_message.get("MESSAGE") == 'FAIL':
                    ld_dict = {"MESSAGE": ld_out_message.get("MESSAGE")}
                else:
                    ld_dict = {"MESSAGE": 'ERROR_OCCURED.' + ld_out_message.get("MESSAGE")}

                return Response(ld_dict)

            elif self.request.query_params.get("Group") == "BULK_SUMMARY":
                jsondata = json.loads(request.body.decode('utf-8'))
                obj_salesrate = mSales.Sales_Model()
                obj_salesrate.type = self.request.query_params.get("Type")
                obj_salesrate.sub_type = self.request.query_params.get("Sub_Type")
                obj_salesrate.jsonData = json.dumps(jsondata.get('Params').get('Filter'))
                obj_salesrate.json_classification = jsondata.get('Params').get('CLASSIFICATION')
                obj_salesrate.entity = self.request.query_params.get("entity")
                obj_salesrate.json_classification['Entity_Gid'] = decry_data(obj_salesrate.entity)
                obj_salesrate.json_classification = json.dumps(obj_salesrate.json_classification)
                obj_salesrate.create_by = decry_data(self.request.query_params.get("Employee_Gid"))
                ld_out_message = obj_salesrate.get_rate_card()
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

class Sales_Invoice_Process(APIView):
    def post(self,request):
        try:
            if self.request.query_params.get("Group")== "SALES_INV_PROCESS":
                jsondata = json.loads(request.body.decode('utf-8'))
                obj_soinvprocess=mSales.Sales_Model()
                obj_soinvprocess.action=self.request.query_params.get("Action")
                obj_soinvprocess.type=self.request.query_params.get("Type")
                obj_soinvprocess.jsonData = jsondata.get('Params').get('HEADER')
                obj_soinvprocess.jsonData['Employee_Gid']=decry_data(jsondata.get('Params').get('HEADER').get('Employee_Gid'))
                obj_soinvprocess.jsonData = json.dumps(jsondata.get('Params').get('HEADER'))
                obj_soinvprocess.jsondata=json.dumps(jsondata.get('Params').get('DETAILS'))
                obj_soinvprocess.json_rate=json.dumps(jsondata.get('Params').get('RATE'))
                obj_soinvprocess.json_classification=jsondata.get('Params').get('CLASSIFICATION')

                obj_soinvprocess.json_classification['Entity_Gid'] =[decry_data(self.request.query_params.get("entity"))]
                obj_soinvprocess.json_classification=json.dumps(jsondata.get('Params').get('CLASSIFICATION'))
                obj_soinvprocess.create_by=decry_data(self.request.query_params.get("Create_by"))
                obj_soinvprocess.is_commit = self.request.query_params.get("Is_Commit")
                common.main_fun1(request.read(), request.path)
                inv_out_message=obj_soinvprocess.set_invprocess()
                if inv_out_message.get("MESSAGE") == 'SUCCESS':
                    ld_dict = {"MESSAGE": "SUCCESS"}
                elif inv_out_message.get("MESSAGE") == 'FAIL':
                    ld_dict = {"MESSAGE": inv_out_message.get("MESSAGE")}
                else:
                    ld_dict = {"MESSAGE": 'ERROR_OCCURED.' + inv_out_message.get("MESSAGE")}
                return Response(ld_dict)
            elif self.request.query_params.get("Group") == "INV_Process_Single_GET" :
                jsondata = json.loads(request.body.decode('utf-8'))
                obj_soinvprocess = mSales.Sales_Model()
                obj_soinvprocess.type = self.request.query_params.get("Type")
                obj_soinvprocess.sub_type = self.request.query_params.get("Sub_Type")
                obj_soinvprocess.jsonData = jsondata.get('Params').get('HEADER')
                obj_soinvprocess.jsonData['Employee_Gid'] = decry_data(jsondata.get('Params').get('HEADER').get('Employee_Gid'))
                obj_soinvprocess.jsonData = json.dumps(jsondata.get('Params').get('HEADER'))
                obj_soinvprocess.jsondata = json.dumps(jsondata.get('Params').get('DETAILS'))
                obj_soinvprocess.json_classification = jsondata.get('Params').get('CLASSIFICATION')
                obj_soinvprocess.json_classification['Entity_Gid'] = [decry_data(self.request.query_params.get("entity"))]
                obj_soinvprocess.json_classification = json.dumps(jsondata.get('Params').get('CLASSIFICATION'))
                # obj_soinvprocess.json_classification = json.dumps(jsondata.get('Params').get('CLASSIFICATION'))
                common.main_fun1(request.read(), request.path)
                ld_out_message = obj_soinvprocess.get_invprocess()
                if ld_out_message.get("MESSAGE") == 'FOUND':
                    ld_dict = {"DATA": json.loads(ld_out_message.get("DATA").to_json(orient='records')),
                               "MESSAGE": "FOUND"}
                elif ld_out_message.get("MESSAGE") == 'NOT_FOUND':
                    ld_dict = {"MESSAGE": ld_out_message.get("MESSAGE")}
                else:
                    ld_dict = {"MESSAGE": 'ERROR_OCCURED.' + ld_out_message.get("MESSAGE")}

                return Response(ld_dict)

            elif self.request.query_params.get("Group")== "SALES_INV_CANCEL":
                jsondata = json.loads(request.body.decode('utf-8'))
                obj_soinvprocess=mSales.Sales_Model()
                obj_soinvprocess.action=self.request.query_params.get("Action")
                obj_soinvprocess.type=self.request.query_params.get("Type")
                obj_soinvprocess.jsonData = jsondata.get('Params').get('HEADER')
                obj_soinvprocess.jsonData['Employee_Gid'] = decry_data(jsondata.get('Params').get('HEADER').get('Employee_Gid'))
                obj_soinvprocess.jsonData=json.dumps(jsondata.get('Params').get('HEADER'))
                obj_soinvprocess.jsondata=json.dumps(jsondata.get('Params').get('DETAILS'))
                obj_soinvprocess.json_rate=json.dumps(jsondata.get('Params').get('RATE'))
                obj_soinvprocess.json_classification = jsondata.get('Params').get('CLASSIFICATION')
                obj_soinvprocess.json_classification['Entity_Gid'] = [decry_data(self.request.query_params.get("entity"))]
                obj_soinvprocess.json_classification = json.dumps(jsondata.get('Params').get('CLASSIFICATION'))
                obj_soinvprocess.create_by=decry_data(self.request.query_params.get("Create_by"))
                obj_soinvprocess.is_commit = self.request.query_params.get("Is_Commit")
                common.main_fun1(request.read(), request.path)
                inv_out_message=obj_soinvprocess.set_invprocess()
                if inv_out_message.get("MESSAGE") == 'SUCCESS':
                    ld_dict = {"MESSAGE": "SUCCESS"}
                elif inv_out_message.get("MESSAGE") == 'FAIL':
                    ld_dict = {"MESSAGE": inv_out_message.get("MESSAGE")}
                else:
                    ld_dict = {"MESSAGE": 'ERROR_OCCURED.' + inv_out_message.get("MESSAGE")}
                return Response(ld_dict)

            elif self.request.query_params.get("Group")== "SALES_PARTIAL_CANCEL":
                jsondata = json.loads(request.body.decode('utf-8'))
                obj_soinvprocess=mSales.Sales_Model()
                obj_soinvprocess.action=self.request.query_params.get("Action")
                obj_soinvprocess.jsonData=json.dumps(jsondata.get('Header_Data'))
                obj_soinvprocess.json_classification = jsondata.get('CLASSIFICATION')
                obj_soinvprocess.json_classification['Entity_Gid'] = [decry_data(self.request.query_params.get("entity"))]
                obj_soinvprocess.json_classification = json.dumps(jsondata.get('CLASSIFICATION'))
                obj_soinvprocess.create_by=decry_data(self.request.query_params.get("Create_by"))
                common.main_fun1(request.read(), request.path)
                inv_out_message=obj_soinvprocess.set_invprocess()
                if inv_out_message.get("MESSAGE") == 'SUCCESS':
                    ld_dict = {"MESSAGE": "SUCCESS"}
                elif inv_out_message.get("MESSAGE") == 'FAIL':
                    ld_dict = {"MESSAGE": inv_out_message.get("MESSAGE")}
                else:
                    ld_dict = {"MESSAGE": 'ERROR_OCCURED.' + inv_out_message.get("MESSAGE")}
                return Response(ld_dict)

            elif self.request.query_params.get("Group")== "UPDATE_STATUS":
                jsondata = json.loads(request.body.decode('utf-8'))
                obj_soinvprocess=mSales.Sales_Model()
                obj_soinvprocess.action=self.request.query_params.get("Action")
                obj_soinvprocess.type=self.request.query_params.get("Type")
                obj_soinvprocess.jsonData = jsondata.get('Params').get('HEADER')
                obj_soinvprocess.jsonData['Employee_Gid'] = decry_data(jsondata.get('Params').get('HEADER').get('Employee_Gid'))
                obj_soinvprocess.jsonData=json.dumps(jsondata.get('Params').get('HEADER'))
                obj_soinvprocess.jsondata=json.dumps(jsondata.get('Params').get('DETAILS'))
                obj_soinvprocess.json_rate=json.dumps(jsondata.get('Params').get('RATE'))
                obj_soinvprocess.json_classification = jsondata.get('Params').get('CLASSIFICATION')
                obj_soinvprocess.json_classification['Entity_Gid'] = [decry_data(self.request.query_params.get("entity"))]
                obj_soinvprocess.json_classification = json.dumps(jsondata.get('Params').get('CLASSIFICATION'))
                obj_soinvprocess.create_by=decry_data(self.request.query_params.get("Create_by"))
                obj_soinvprocess.is_commit = self.request.query_params.get("Is_Commit")
                common.main_fun1(request.read(), request.path)
                inv_out_message=obj_soinvprocess.set_invprocess()
                if inv_out_message.get("MESSAGE") == 'SUCCESS':
                    ld_dict = {"MESSAGE": "SUCCESS"}
                elif inv_out_message.get("MESSAGE") == 'FAIL':
                    ld_dict = {"MESSAGE": inv_out_message.get("MESSAGE")}
                else:
                    ld_dict = {"MESSAGE": 'ERROR_OCCURED.' + inv_out_message.get("MESSAGE")}
                return Response(ld_dict)

            elif self.request.query_params.get("Group") == "INV_CANCEL_SINGLE_GET" :
                jsondata = json.loads(request.body.decode('utf-8'))
                obj_soinvprocess = mSales.Sales_Model()
                obj_soinvprocess.type = self.request.query_params.get("Type")
                obj_soinvprocess.sub_type = self.request.query_params.get("Sub_Type")
                obj_soinvprocess.jsonData = json.dumps(jsondata.get('Params').get('FILTER'))
                obj_soinvprocess.json_classification = jsondata.get('Params').get('CLASSIFICATION')
                obj_soinvprocess.json_classification['Entity_Gid'] = [ decry_data(self.request.query_params.get("entity"))]
                obj_soinvprocess.json_classification = json.dumps(jsondata.get('Params').get('CLASSIFICATION'))
                obj_soinvprocess.create_by = [decry_data(self.request.query_params.get("entity"))]
                ld_out_message = obj_soinvprocess.get_invprocess()
                common.main_fun1(request.read(), request.path)
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


class Invoice_Dispatch(APIView):
    def post(self, request):
        try:
            if self.request.query_params.get("Group") == "INV_DISPATCH_PROCESS":
                jsondata = json.loads(request.body.decode('utf-8'))
                obj_invdipatch = mSales.Sales_Model()
                obj_invdipatch.type = self.request.query_params.get("Type")
                obj_invdipatch.sub_type = self.request.query_params.get("Sub_Type")
                obj_invdipatch.jsonData = json.dumps(jsondata.get('Params').get('FILTER'))
                obj_invdipatch.json_classification = jsondata.get('Params').get('CLASSIFICATION')
                obj_invdipatch.json_classification['Entity_Gid'] =[decry_data( self.request.query_params.get("entity"))]
                obj_invdipatch.json_classification = json.dumps(jsondata.get('Params').get('CLASSIFICATION'))
                obj_invdipatch.create_by = decry_data(self.request.query_params.get("Employee_Gid"))
                ld_out_message = obj_invdipatch.get_INV_Dispatch()
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


class Customer_Performance_Report(APIView):
    def post(self,request):
        try:
            if self.request.query_params.get("Group") == "Customer_Performance_Report":
                jsondata = json.loads(request.body.decode('utf-8'))
                obj_totalsales=mSales.Sales_Model()
                obj_totalsales.type=self.request.query_params.get("Type")
                obj_totalsales.sub_type = self.request.query_params.get("Sub_Type")
                obj_totalsales.jsonData = json.dumps(jsondata.get('Params').get('FILTER'))
                obj_totalsales.json_classification = jsondata.get('Params').get('CLASSIFICATION')
                obj_totalsales.json_classification['Entity_Gid'] = decry_data(self.request.query_params.get("entity"))
                obj_totalsales.json_classification = json.dumps(jsondata.get('Params').get('CLASSIFICATION'))
                ld_out_message = obj_totalsales.get_total_sales()
                if ld_out_message.get("MESSAGE") == 'FOUND':
                    ld_dict={"DATA":json.loads(ld_out_message.get("DATA").to_json(orient='records')),
                             "MESSAGE":"FOUND"}

                elif ld_out_message.get("MESSAGE") == 'NOT_FOUND':
                    ld_dict={"MESSAGE":ld_out_message.get("MESSAGE")}
                else:
                    ld_dict={"MESSAGE":"ERROR OCCURED.","DATA":ld_out_message.get("MESSAGE")}
                return Response (ld_dict)

        except Exception as a:
            return Response({"MESSAGE":"ERROR_OCCURED","DATA":str(a)})





class Dispatch_Process(APIView):
    def post(self, request):
        try:
            if self.request.query_params.get("Group") == "SALES_SPLIT_QUANTITY":
                jsondata = json.loads(request.body.decode('utf-8'))
                obj_invdipatch = mSales.Sales_Model()
                obj_invdipatch.type = self.request.query_params.get("Type")
                obj_invdipatch.sub_type = self.request.query_params.get("Sub_Type")
                obj_invdipatch.jsonData = jsondata.get('Params').get('FILTER')
                obj_invdipatch.jsonData['Employee_Gid'] = decry_data(obj_invdipatch.jsonData['Employee_Gid'])
                obj_invdipatch.jsonData= json.dumps(jsondata.get('Params').get('FILTER'))
                obj_invdipatch.json_classification = jsondata.get('Params').get('CLASSIFICATION')
                obj_invdipatch.json_classification['Entity_Gid'] = [decry_data(self.request.query_params.get("entity"))]
                obj_invdipatch.json_classification = json.dumps(jsondata.get('Params').get('CLASSIFICATION'))
                common.main_fun1(request.read(), request.path)
                ld_out_message = obj_invdipatch.get_Dispatch_Process()
                if ld_out_message.get("MESSAGE") == 'FOUND':
                    ld_dict = {"DATA": json.loads(ld_out_message.get("DATA").to_json(orient='records')),
                               "MESSAGE": "FOUND"}
                elif ld_out_message.get("MESSAGE") == 'NOT_FOUND':
                    ld_dict = {"MESSAGE": ld_out_message.get("MESSAGE")}
                else:
                    ld_dict = {"MESSAGE": 'ERROR_OCCURED.' + ld_out_message.get("MESSAGE")}

                return Response(ld_dict)


            elif self.request.query_params.get("Group") == "DISPATCH_POD_SUMMARY":
                jsondata = json.loads(request.body.decode('utf-8'))
                obj_invdipatch = mSales.Sales_Model()
                obj_invdipatch.type = self.request.query_params.get("Type")
                obj_invdipatch.sub_type = self.request.query_params.get("Sub_Type")
                obj_invdipatch.jsonData = jsondata.get('Params').get('FILTER')
                obj_invdipatch.jsonData['Employee_Gid'] = decry_data(obj_invdipatch.jsonData['Employee_Gid'])
                obj_invdipatch.jsonData = json.dumps(jsondata.get('Params').get('FILTER'))
                obj_invdipatch.json_classification = jsondata.get('Params').get('CLASSIFICATION')
                obj_invdipatch.json_classification['Entity_Gid'] = [decry_data(self.request.query_params.get("entity"))]
                obj_invdipatch.json_classification = json.dumps(jsondata.get('Params').get('CLASSIFICATION'))
                ld_out_message = obj_invdipatch.get_Dispatch_Process()
                if ld_out_message.get("MESSAGE") == 'FOUND':
                    ld_dict = {"DATA": json.loads(ld_out_message.get("DATA").to_json(orient='records')),
                               "MESSAGE": "FOUND"}
                elif ld_out_message.get("MESSAGE") == 'NOT_FOUND':
                    ld_dict = {"MESSAGE": ld_out_message.get("MESSAGE")}
                else:
                    ld_dict = {"MESSAGE": 'ERROR_OCCURED.' + ld_out_message.get("MESSAGE")}

                return Response(ld_dict)

            elif self.request.query_params.get("Group") == "LABEL_PRINT_SALES":
                jsondata = json.loads(request.body.decode('utf-8'))
                obj_invdipatch = mSales.Sales_Model()
                obj_invdipatch.type = self.request.query_params.get("Type")
                obj_invdipatch.sub_type = self.request.query_params.get("Sub_Type")
                obj_invdipatch.jsonData = jsondata.get('Params').get('FILTER')
                obj_invdipatch.jsonData['Employee_Gid'] = decry_data(obj_invdipatch.jsonData['Employee_Gid'])
                obj_invdipatch.jsonData = json.dumps(jsondata.get('Params').get('FILTER'))
                obj_invdipatch.json_classification = jsondata.get('Params').get('CLASSIFICATION')
                obj_invdipatch.json_classification['Entity_Gid'] = [decry_data(self.request.query_params.get("entity"))]
                obj_invdipatch.json_classification = json.dumps(jsondata.get('Params').get('CLASSIFICATION'))
                ld_out_message = obj_invdipatch.get_Dispatch_Process()
                if ld_out_message.get("MESSAGE") == 'FOUND':

                    ld_dict = {"DATA": json.loads(ld_out_message.get("DATA").to_json(orient='records')),
                               "MESSAGE": "FOUND"}
                elif ld_out_message.get("MESSAGE") == 'NOT_FOUND':
                    ld_dict = {"MESSAGE": ld_out_message.get("MESSAGE")}
                else:
                    ld_dict = {"MESSAGE": 'ERROR_OCCURED.' + ld_out_message.get("MESSAGE")}

                return Response(ld_dict)


            elif self.request.query_params.get("Group") == "SALES_FULL_QUANTITY":
                jsondata = json.loads(request.body.decode('utf-8'))
                obj_invdipatch = mSales.Sales_Model()
                obj_invdipatch.type = self.request.query_params.get("Type")
                obj_invdipatch.sub_type = self.request.query_params.get("Sub_Type")
                obj_invdipatch.jsonData = jsondata.get('Params').get('FILTER')
                obj_invdipatch.jsonData['Employee_Gid'] = decry_data(obj_invdipatch.jsonData['Employee_Gid'])
                obj_invdipatch.jsonData = json.dumps(jsondata.get('Params').get('FILTER'))
                obj_invdipatch.json_classification = jsondata.get('Params').get('CLASSIFICATION')
                obj_invdipatch.json_classification['Entity_Gid'] = [decry_data(self.request.query_params.get("entity"))]
                obj_invdipatch.json_classification = json.dumps(jsondata.get('Params').get('CLASSIFICATION'))
                ld_out_message = obj_invdipatch.get_Dispatch_Process()
                if ld_out_message.get("MESSAGE") == 'FOUND':
                    ld_dict = {"DATA": json.loads(ld_out_message.get("DATA").to_json(orient='records')),
                               "MESSAGE": "FOUND"}
                elif ld_out_message.get("MESSAGE") == 'NOT_FOUND':
                    ld_dict = {"MESSAGE": ld_out_message.get("MESSAGE")}
                else:
                    ld_dict = {"MESSAGE": 'ERROR_OCCURED.' + ld_out_message.get("MESSAGE")}

                return Response(ld_dict)

            elif self.request.query_params.get("Group") == "CONSIGNMENT_DETAILS":
                jsondata = json.loads(request.body.decode('utf-8'))
                obj_invdipatch = mSales.Sales_Model()
                obj_invdipatch.type = self.request.query_params.get("Type")
                obj_invdipatch.sub_type = self.request.query_params.get("Sub_Type")
                obj_invdipatch.jsonData = jsondata.get('Params').get('FILTER')
                obj_invdipatch.jsonData['Employee_Gid'] = decry_data(obj_invdipatch.jsonData['Employee_Gid'])
                obj_invdipatch.jsonData = json.dumps(jsondata.get('Params').get('FILTER'))
                obj_invdipatch.json_classification = jsondata.get('Params').get('CLASSIFICATION')
                obj_invdipatch.json_classification['Entity_Gid'] = [decry_data(self.request.query_params.get("entity"))]
                obj_invdipatch.json_classification = json.dumps(jsondata.get('Params').get('CLASSIFICATION'))
                ld_out_message = obj_invdipatch.get_Dispatch_Process()
                if ld_out_message.get("MESSAGE") == 'FOUND':
                    ld_dict = {"DATA": json.loads(ld_out_message.get("DATA").to_json(orient='records')),
                               "MESSAGE": "FOUND"}
                elif ld_out_message.get("MESSAGE") == 'NOT_FOUND':
                    ld_dict = {"MESSAGE": ld_out_message.get("MESSAGE")}
                else:
                    ld_dict = {"MESSAGE": 'ERROR_OCCURED.' + ld_out_message.get("MESSAGE")}

                return Response(ld_dict)

            elif self.request.query_params.get("Group")== "CARTON_SALES":
                jsondata = json.loads(request.body.decode('utf-8'))
                obj_soinvprocess=mSales.Sales_Model()
                obj_soinvprocess.action=self.request.query_params.get("Action")
                obj_soinvprocess.type=self.request.query_params.get("Type")
                obj_soinvprocess.sub_type = self.request.query_params.get("Sub_Type")
                obj_soinvprocess.jsonData=json.dumps(jsondata.get('Params').get('HEADER'))
                obj_soinvprocess.jsondata=json.dumps(jsondata.get('Params').get('DETAILS'))
                obj_soinvprocess.json_classification=jsondata.get('Params').get('CLASSIFICATION')
                obj_soinvprocess.json_classification['Entity_Gid'] = [decry_data(self.request.query_params.get("entity"))]
                obj_soinvprocess.json_classification = json.dumps(jsondata.get('Params').get('CLASSIFICATION'))
                obj_soinvprocess.create_by=decry_data(self.request.query_params.get("Create_by"))
                inv_out_message=obj_soinvprocess.set_Dispatch_Process()
                if inv_out_message.get("MESSAGE") == 'SUCCESS':
                    ld_dict = {"MESSAGE": "SUCCESS"}
                elif inv_out_message.get("MESSAGE") == 'PROCESS_DATA':
                    ld_dict = {"MESSAGE":"PROCESS_DATA","DATA": json.loads(inv_out_message.get("DATA").to_json(orient='records')) }
                elif inv_out_message.get("MESSAGE") == 'FAIL':
                    ld_dict = {"MESSAGE": inv_out_message.get("MESSAGE")}
                else:
                    ld_dict = {"MESSAGE": 'ERROR_OCCURED.' + inv_out_message.get("MESSAGE")}
                return Response(ld_dict)
            elif self.request.query_params.get("Group")== "LABEL_PRINT_FLAG":
                jsondata = json.loads(request.body.decode('utf-8'))
                obj_soinvprocess=mSales.Sales_Model()
                obj_soinvprocess.action=self.request.query_params.get("Action")
                obj_soinvprocess.type=self.request.query_params.get("Type")
                obj_soinvprocess.sub_type = self.request.query_params.get("Sub_Type")
                obj_soinvprocess.jsonData=json.dumps(jsondata.get('Params').get('HEADER'))
                obj_soinvprocess.jsondata=json.dumps(jsondata.get('Params').get('DETAILS'))
                obj_soinvprocess.json_classification = jsondata.get('Params').get('CLASSIFICATION')
                obj_soinvprocess.json_classification['Entity_Gid'] = [decry_data(self.request.query_params.get("entity"))]
                obj_soinvprocess.json_classification = json.dumps(jsondata.get('Params').get('CLASSIFICATION'))
                obj_soinvprocess.create_by = decry_data(self.request.query_params.get("Create_by"))
                inv_out_message=obj_soinvprocess.set_Dispatch_Process()
                if inv_out_message.get("MESSAGE") == 'SUCCESS':
                    ld_dict = {"MESSAGE": "SUCCESS"}
                elif inv_out_message.get("MESSAGE") == 'FAIL':
                    ld_dict = {"MESSAGE": inv_out_message.get("MESSAGE")}
                else:
                    ld_dict = {"MESSAGE": 'ERROR_OCCURED.' + inv_out_message.get("MESSAGE")}
                return Response(ld_dict)

            elif self.request.query_params.get("Group")== "CARTON_SPLIT":
                jsondata = json.loads(request.body.decode('utf-8'))
                obj_soinvprocess=mSales.Sales_Model()
                obj_soinvprocess.action=self.request.query_params.get("Action")
                obj_soinvprocess.type=self.request.query_params.get("Type")
                obj_soinvprocess.sub_type = self.request.query_params.get("Sub_Type")
                obj_soinvprocess.jsonData=json.dumps(jsondata.get('Params').get('HEADER'))
                obj_soinvprocess.jsondata=json.dumps(jsondata.get('Params').get('DETAILS'))
                obj_soinvprocess.json_classification = jsondata.get('Params').get('CLASSIFICATION')
                obj_soinvprocess.json_classification['Entity_Gid'] = [ decry_data(self.request.query_params.get("entity"))]
                obj_soinvprocess.json_classification = json.dumps(jsondata.get('Params').get('CLASSIFICATION'))
                obj_soinvprocess.create_by = decry_data(self.request.query_params.get("Create_by"))
                inv_out_message=obj_soinvprocess.set_Dispatch_Process()
                if inv_out_message.get("MESSAGE") == 'SUCCESS':
                    ld_dict = {"MESSAGE": "SUCCESS"}
                elif inv_out_message.get("MESSAGE") == 'FAIL':
                    ld_dict = {"MESSAGE": inv_out_message.get("MESSAGE")}
                else:
                    ld_dict = {"MESSAGE": 'ERROR_OCCURED.' + inv_out_message.get("MESSAGE")}
                return Response(ld_dict)

            elif self.request.query_params.get("Group")== "UPDATE_STATUS":
                jsondata = json.loads(request.body.decode('utf-8'))
                obj_soinvprocess=mSales.Sales_Model()
                obj_soinvprocess.action=self.request.query_params.get("Action")
                obj_soinvprocess.type=self.request.query_params.get("Type")
                obj_soinvprocess.sub_type = self.request.query_params.get("Sub_Type")
                obj_soinvprocess.jsonData=json.dumps(jsondata.get('Params').get('HEADER'))
                obj_soinvprocess.jsondata=json.dumps(jsondata.get('Params').get('DETAILS'))
                obj_soinvprocess.json_classification = json.dumps(jsondata.get('Params').get('CLASSIFICATION'))
                obj_soinvprocess.json_classification['Entity_Gid'] = [ decry_data(self.request.query_params.get("entity"))]
                obj_soinvprocess.json_classification = json.dumps(jsondata.get('Params').get('CLASSIFICATION'))
                obj_soinvprocess.create_by = decry_data(self.request.query_params.get("Create_by"))
                inv_out_message=obj_soinvprocess.set_Dispatch_Process()
                if inv_out_message.get("MESSAGE") == 'SUCCESS':
                    ld_dict = {"MESSAGE": "SUCCESS"}
                elif inv_out_message.get("MESSAGE") == 'FAIL':
                    ld_dict = {"MESSAGE": inv_out_message.get("MESSAGE")}
                else:
                    ld_dict = {"MESSAGE": 'ERROR_OCCURED.' + inv_out_message.get("MESSAGE")}
                return Response(ld_dict)


            elif self.request.query_params.get("Group")== "DISPATCH_WEIGHT_UPDATE":
                jsondata = json.loads(request.body.decode('utf-8'))
                obj_soinvprocess=mSales.Sales_Model()
                obj_soinvprocess.action=self.request.query_params.get("Action")
                obj_soinvprocess.type=self.request.query_params.get("Type")
                obj_soinvprocess.sub_type = self.request.query_params.get("Sub_Type")
                obj_soinvprocess.jsonData=json.dumps(jsondata.get('Params').get('HEADER'))
                obj_soinvprocess.jsondata=json.dumps(jsondata.get('Params').get('DETAILS'))
                obj_soinvprocess.json_classification = jsondata.get('Params').get('CLASSIFICATION')
                obj_soinvprocess.json_classification['Entity_Gid'] = [decry_data(self.request.query_params.get("entity"))]
                obj_soinvprocess.json_classification = json.dumps(jsondata.get('Params').get('CLASSIFICATION'))
                obj_soinvprocess.create_by = decry_data(self.request.query_params.get("Create_by"))
                #common.main_fun1(request.read(), request.path)
                inv_out_message=obj_soinvprocess.set_Dispatch_Process()
                if inv_out_message.get("MESSAGE") == 'SUCCESS':
                    ld_dict = {"MESSAGE": "SUCCESS"}
                elif inv_out_message.get("MESSAGE") == 'FAIL':
                    ld_dict = {"MESSAGE": inv_out_message.get("MESSAGE")}
                else:
                    ld_dict = {"MESSAGE": 'ERROR_OCCURED.' + inv_out_message.get("MESSAGE")}
                return Response(ld_dict)
            elif self.request.query_params.get("Group")== "GENERATE_AWB_NO":
                jsondata = json.loads(request.body.decode('utf-8'))
                obj_invdipatch = mSales.Sales_Model()
                obj_invdipatch.type = self.request.query_params.get("Type")
                obj_invdipatch.sub_type = self.request.query_params.get("Sub_Type")
                obj_invdipatch.jsonData = json.dumps(jsondata.get('Params').get('FILTER'))
                obj_invdipatch.json_classification = jsondata.get('Params').get('CLASSIFICATION')
                obj_invdipatch.json_classification['Entity_Gid'] = [  decry_data(self.request.query_params.get("entity"))]
                obj_invdipatch.json_classification = json.dumps(jsondata.get('Params').get('CLASSIFICATION'))
                #obj_soinvprocess.create_by = decry_data(self.request.query_params.get("Create_by"))
                common.main_fun1(request.read(), request.path)
                ld_out_message = obj_invdipatch.get_Dispatch_Process()
                if ld_out_message.get("MESSAGE") == 'FOUND':
                    ld_dict = {"DATA": json.loads(ld_out_message.get("DATA").to_json(orient='records')),
                               "MESSAGE": "FOUND"}
                elif ld_out_message.get("MESSAGE") == 'NOT_FOUND':
                    ld_dict = {"MESSAGE": ld_out_message.get("MESSAGE")}
                else:
                    ld_dict = {"MESSAGE": 'ERROR_OCCURED.' + ld_out_message.get("MESSAGE")}

                return Response(ld_dict)


            elif self.request.query_params.get("Group") == "Courier_Explorer":
                jsondata = json.loads(request.body.decode('utf-8'))
                obj_invdipatch = mSales.Sales_Model()
                obj_invdipatch.type = self.request.query_params.get("Type")
                obj_invdipatch.sub_type = self.request.query_params.get("Sub_Type")
                obj_invdipatch.jsonData = json.dumps(jsondata.get('Params').get('FILTER'))

                obj_invdipatch.json_classification = jsondata.get('Params').get('CLASSIFICATION')
                obj_invdipatch.json_classification['Entity_Gid'] = [decry_data(self.request.query_params.get("entity"))]
                obj_invdipatch.json_classification = json.dumps(jsondata.get('Params').get('CLASSIFICATION'))

                ld_out_message = obj_invdipatch.get_Dispatch_Process()
                if ld_out_message.get("MESSAGE") == 'FOUND':
                    ld_dict = {"DATA": json.loads(ld_out_message.get("DATA").to_json(orient='records')),
                               "MESSAGE": "FOUND"}
                elif ld_out_message.get("MESSAGE") == 'NOT_FOUND':
                    ld_dict = {"MESSAGE": ld_out_message.get("MESSAGE")}
                else:
                    ld_dict = {"MESSAGE": 'ERROR_OCCURED.' + ld_out_message.get("MESSAGE")}

                return Response(ld_dict)



            elif self.request.query_params.get("Group")== "COURIER_PROCESS":
                jsondata = json.loads(request.body.decode('utf-8'))
                obj_soinvprocess = mSales.Sales_Model()
                obj_soinvprocess.action = self.request.query_params.get("Action")
                obj_soinvprocess.type = self.request.query_params.get("Type")
                obj_soinvprocess.sub_type = self.request.query_params.get("Sub_Type")
                obj_soinvprocess.jsonData = json.dumps(jsondata.get('Params').get('HEADER'))
                obj_soinvprocess.json_classification = jsondata.get('Params').get('CLASSIFICATION')
                obj_soinvprocess.json_classification['Entity_Gid'] = [decry_data(self.request.query_params.get("entity"))]
                obj_soinvprocess.json_classification = json.dumps(jsondata.get('Params').get('CLASSIFICATION'))
                obj_soinvprocess.create_by = decry_data(self.request.query_params.get("Create_by"))

                ###
                # Here To Save The File In a Directory
                obj_soinvprocess.json_file = json.dumps(jsondata.get('Params').get('File'))
                lst_saved_filepath = commonview.File_Upload(obj_soinvprocess.json_file, 'COURIER',obj_soinvprocess.create_by)
                # obj_soinvprocess.jsondata = {"SavedFilePath": saved_filepath}
                obj_soinvprocess.jsondata = json.dumps(lst_saved_filepath)
                ###

                inv_out_message = obj_soinvprocess.set_Dispatch_Process()
                if inv_out_message.get("MESSAGE") == 'File Updated' or inv_out_message.get("MESSAGE") == 'Partially Updated' or inv_out_message.get("MESSAGE") == 'None Record is Updated' :
                    ld_dict = {"MESSAGE": inv_out_message.get("MESSAGE")}
                elif inv_out_message.get("MESSAGE") == 'FAIL':
                    ld_dict = {"MESSAGE": inv_out_message.get("MESSAGE")}
                else:
                    ld_dict = {"MESSAGE": 'ERROR_OCCURED.' + inv_out_message.get("MESSAGE")}
                return Response(ld_dict)
        except Exception as e:
            return Response({"MESSAGE": "ERROR_OCCURED", "DATA": str(e)})
