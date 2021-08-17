from rest_framework.views import APIView
from rest_framework.response import Response
import json
from Bigflow.ServiceManagement.Model import mServiceManagement
from Bigflow.API import views as commonview
from Bigflow.Core import models as common
import requests

class Service_Management_Get(APIView):
    def post(self,request):
        try:
            path = self.request.stream.path
            if self.request.query_params.get("type") == "Suppplier" and self.request.query_params.get("sub_type")=="DROPDOWN":
                jsondata = json.loads(request.body.decode('utf-8'))
                ser_mgmt_get = mServiceManagement.ServiceManagement()
                ser_mgmt_get.type = self.request.query_params.get("type")
                ser_mgmt_get.sub_type = self.request.query_params.get("sub_type")
                ser_mgmt_get.filter = json.dumps(jsondata.get("params").get("filter"))
                ser_mgmt_get.classification = json.dumps(jsondata.get("classification"))
                common.main_fun1(request.read(), path)
                result = ser_mgmt_get.get_supplier_data()
                json_data = json.loads(result.to_json(orient='records'))
                return Response(json_data)
            elif self.request.query_params.get("type") == "Mode" and self.request.query_params.get("sub_type")=="Summary":
                jsondata = json.loads(request.body.decode('utf-8'))
                ser_mgmt_get = mServiceManagement.ServiceManagement()
                ser_mgmt_get.type = self.request.query_params.get("type")
                ser_mgmt_get.sub_type = self.request.query_params.get("sub_type")
                ser_mgmt_get.filter = json.dumps(jsondata.get("params").get("filter"))
                ser_mgmt_get.classification = json.dumps(jsondata.get("classification"))
                common.main_fun1(request.read(), path)
                result = ser_mgmt_get.get_branch_name()
                json_data = json.loads(result.to_json(orient='records'))
                return Response(json_data)
            elif self.request.query_params.get("type") == "GET" and (self.request.query_params.get("sub_type") == "OVERALL_ASSET" or
                                                                     self.request.query_params.get("sub_type") == "TICKET_RISE_ASSETS" or
                                                                     self.request.query_params.get("sub_type") == "ASSET_DETAIL" or
                                                                     self.request.query_params.get("sub_type") == "ErrorCategory" or
                                                                     self.request.query_params.get("sub_type") == "TICKET_RISE_ASSETS_NEW" or
                                                                     self.request.query_params.get("sub_type") == "TICKET_HEADER_GET"):
                    jsondata = json.loads(request.body.decode('utf-8'))
                    ser_mgmt_get = mServiceManagement.ServiceManagement()
                    ser_mgmt_get.type = self.request.query_params.get("type")
                    ser_mgmt_get.sub_type = self.request.query_params.get("sub_type")
                    ser_mgmt_get.filter = json.dumps(jsondata.get("params").get("filter"))
                    ser_mgmt_get.classification = json.dumps(jsondata.get("classification"))
                    common.main_fun1(request.read(), path)
                    result = ser_mgmt_get.get_all_data()
                    json_data = json.loads(result.to_json(orient='records'))
                    return Response(json_data)

            elif self.request.query_params.get("type")=="GET" and self.request.query_params.get("sub_type")=="FOLLOW_UP_GET":
                jsondata = json.loads(request.body.decode('utf-8'))
                ser_mgmt_get = mServiceManagement.ServiceManagement()
                ser_mgmt_get.type = self.request.query_params.get("type")
                ser_mgmt_get.sub_type = self.request.query_params.get("sub_type")
                ser_mgmt_get.filter = json.dumps(jsondata.get("params").get("filter"))
                ser_mgmt_get.classification = json.dumps(jsondata.get("classification"))
                common.main_fun1(request.read(), path)
                result = ser_mgmt_get.get_follow_up_data()
                json_data = json.loads(result.to_json(orient='records'))
                return Response(json_data)
            elif self.request.query_params.get("type")=="GET" and (self.request.query_params.get("sub_type")=="SUPPLIER_PRODUCT_TYPE" or
                                                                   self.request.query_params.get("sub_type")=="GET_SUPPLIER" or
                                                                   self.request.query_params.get("sub_type")=="GET_COMMODITY"):
                    jsondata = json.loads(request.body.decode('utf-8'))
                    ser_mgmt_get = mServiceManagement.ServiceManagement()
                    ser_mgmt_get.type = self.request.query_params.get("type")
                    ser_mgmt_get.sub_type = self.request.query_params.get("sub_type")
                    ser_mgmt_get.filter = json.dumps(jsondata.get("params").get("filter"))
                    ser_mgmt_get.classification = json.dumps(jsondata.get("classification"))
                    common.main_fun1(request.read(), path)
                    result = ser_mgmt_get.get_product_data()
                    json_data = json.loads(result.to_json(orient='records'))
                    return Response(json_data)

        except Exception as e:
            common.logger.error(e)
            return Response({"MESSAGE": "ERROR_OCCURED", "DATA": str(e)})

class Service_Management_Set(APIView):
    def post(self,request):
        try:
            path = self.request.stream.path
            jsondata = json.loads(request.body.decode('utf-8'))
            if self.request.query_params.get("action") == "INSERT" and\
                    (self.request.query_params.get("type")=="INSERT_TICKET_HEADER_DETAIL"
                     or self.request.query_params.get("type")=="INSERT_ERROR_CATEGORY"):
                jsondata = json.loads(request.body.decode('utf-8'))
                ser_mgmt_set = mServiceManagement.ServiceManagement()
                ser_mgmt_set.action = self.request.query_params.get("action")
                ser_mgmt_set.type = self.request.query_params.get("type")
                ser_mgmt_set.filter = json.dumps(jsondata.get("params").get("filter"))
                ser_mgmt_set.classification = json.dumps(jsondata.get("params").get("classification"))
                ser_mgmt_set.create_by = self.request.query_params.get("create_by")
                #common.main_fun1(request.read(), path)
                result = ser_mgmt_set.create_ticket()
                return Response(result)
            elif self.request.query_params.get("action") == "INSERT" and self.request.query_params.get("type")=="INSERT_FOLLOWUP":
                jsondata = json.loads(request.body.decode('utf-8'))
                ser_mgmt_set = mServiceManagement.ServiceManagement()
                ser_mgmt_set.action = self.request.query_params.get("action")
                ser_mgmt_set.type = self.request.query_params.get("type")
                ser_mgmt_set.filter = json.dumps(jsondata.get("params").get("filter"))
                ser_mgmt_set.classification = json.dumps(jsondata.get("params").get("classification"))
                ser_mgmt_set.create_by = self.request.query_params.get("create_by")
                #common.main_fun1(request.read(), path)
                result = ser_mgmt_set.set_followup()
                return Response(result)


        except Exception as e:
            common.logger.error(e)
            return Response({"MESSAGE": "ERROR_OCCURED", "DATA": str(e)})



class AMC_Details_Set(APIView):
    def post(self,request):
        try:
            path = self.request.stream.path
            if self.request.query_params.get("action") == "INSERT" and self.request.query_params.get("type")=="SM_AMC_INSERT":
                jsondata = json.loads(request.body.decode('utf-8'))
                ser_mgmt_set = mServiceManagement.ServiceManagement()
                ser_mgmt_set.action = self.request.query_params.get("action")
                ser_mgmt_set.type = self.request.query_params.get("type")
                ser_mgmt_set.filter = json.dumps(jsondata.get("params").get("filter"))
                ser_mgmt_set.classification = json.dumps(jsondata.get("params").get("classification"))
                ser_mgmt_set.create_by = self.request.query_params.get("create_by")
                common.main_fun1(request.read(), path)
                result = ser_mgmt_set.create_amc()
                return Response(result)
            elif self.request.query_params.get("action") == "UPDATE" and (self.request.query_params.get("type")=="ACTIVE_INACTIVE"
                                                                          or self.request.query_params.get("type")=="SM_AMC_UPDATE"
                                                                          or self.request.query_params.get("type")=="AMC_STATUS"):
                jsondata = json.loads(request.body.decode('utf-8'))
                ser_mgmt_set = mServiceManagement.ServiceManagement()
                ser_mgmt_set.action = self.request.query_params.get("action")
                ser_mgmt_set.type = self.request.query_params.get("type")
                ser_mgmt_set.filter = json.dumps(jsondata.get("params").get("filter"))
                ser_mgmt_set.classification = json.dumps(jsondata.get("params").get("classification"))
                ser_mgmt_set.create_by = self.request.query_params.get("create_by")
                #common.main_fun1(request.read(), path)
                result = ser_mgmt_set.amc_Update()
                return Response(result)
        except Exception as e:
            common.logger.error(e)
            return Response({"MESSAGE": "ERROR_OCCURED", "DATA": str(e)})

class AMC_Details_Get(APIView):
    def post(self,request):
        try:
            path = self.request.stream.path
            if self.request.query_params.get("action") == "GET" and (self.request.query_params.get("type")=="AMC_HEADER_DETAIL" or
                                                                     self.request.query_params.get("type")=="AMC_HEADER"):
                jsondata = json.loads(request.body.decode('utf-8'))
                ser_mgmt_set = mServiceManagement.ServiceManagement()
                ser_mgmt_set.action = self.request.query_params.get("action")
                ser_mgmt_set.type = self.request.query_params.get("type")
                ser_mgmt_set.filter = json.dumps(jsondata.get("params").get("filter"))
                ser_mgmt_set.classification = json.dumps(jsondata.get("params").get("classification"))
                common.main_fun1(request.read(), path)
                result = ser_mgmt_set.get_amc_data()
                json_data = json.loads(result.to_json(orient='records'))
                return Response(json_data)
        except Exception as e:
            common.logger.error(e)
            return Response({"MESSAGE": "ERROR_OCCURED", "DATA": str(e)})


class All_Tables_Values_Get_Metadata(APIView):
    def post(self, request):
        try:
            path = self.request.stream.path
            ser_mgmt_set = mServiceManagement.ServiceManagement()
            ser_mgmt_set.action = self.request.query_params.get("Action")
            ser_mgmt_set.jsonData = request.body.decode('utf-8')
            ser_mgmt_set.entity_gid = self.request.query_params.get("Entity_Gid")
            common.main_fun1(request.read(), path)
            out_message = ser_mgmt_set.get_alltablevalue_metadata()
            if out_message.empty == False:
                json_data = json.loads(out_message.to_json(orient='records'))
                return Response({"MESSAGE": "FOUND", "DATA": json_data})
            else:
                return Response({"MESSAGE": "NOT_FOUND"})
        except Exception as e:
            common.logger.error(e)
            return Response({"MESSAGE": "ERROR_OCCURED", "DATA": str(e)})


class All_Tables_Values_Get_Data(APIView):
    def post(self, request):
        try:
            path = self.request.stream.path
            if self.request.query_params.get("table_name") == "employee" and self.request.query_params.get("gid") == '0':
                ser_mgmt_set = mServiceManagement.ServiceManagement()
                ser_mgmt_set.table_name = self.request.query_params.get("table_name")
                ser_mgmt_set.gid = self.request.query_params.get("gid")
                ser_mgmt_set.entity_gid = self.request.query_params.get("entity_gid")
                #common.main_fun1(request.read(), path)
                result = ser_mgmt_set.get_emp_data()
                json_data = json.loads(result.to_json(orient='records'))
                return Response(json_data)
        except Exception as e:
            common.logger.error(e)
            return Response({"MESSAGE": "ERROR_OCCURED", "DATA": str(e)})

class Pr_Creation(APIView):
    def post(self, request):
        try:
            path = self.request.stream.path
            if self.request.query_params.get("action") == "insert" and self.request.query_params.get("type") == "PR_DETAILS_INSERT":
                jsondata = json.loads(request.body.decode('utf-8'))
                ser_mgmt_set = mServiceManagement.ServiceManagement()
                ser_mgmt_set.action = self.request.query_params.get("action")
                ser_mgmt_set.type = self.request.query_params.get("type")
                ser_mgmt_set.filter = json.dumps(jsondata.get("params").get("filter"))
                ser_mgmt_set.classification = json.dumps(jsondata.get("params").get("classification"))
                ser_mgmt_set.draft = {"entity_gid":self.request.query_params.get("type")}
                objdata1 = self.request.query_params.get("entity_gid")
                ser_mgmt_set.classification_json = json.dumps({"Entity_Gid": [objdata1]})
                ser_mgmt_set.create_by = self.request.query_params.get("create_by")
                common.main_fun1(request.read(), path)
                result = ser_mgmt_set.set_pr_detils()
                return Response(result)
        except Exception as e:
            common.logger.error(e)
            return Response({"MESSAGE": "ERROR_OCCURED", "DATA": str(e)})