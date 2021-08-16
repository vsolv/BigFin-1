from rest_framework.views import APIView
from rest_framework.response import Response
import json
from Bigflow.BranchExp.model import mBranch
from Bigflow.Core import models as common

class Expense_Process(APIView):
    def post(self,request):
        try:
            path = self.request.stream.path
            if self.request.query_params.get("Group")== "EXPENSE_DATA":
                jsondata = json.loads(request.body.decode('utf-8'))
                exp_process= mBranch.BranchExp_model()
                exp_process.type=self.request.query_params.get("Type")
                exp_process.sub_type=self.request.query_params.get("SubType")
                exp_process.jsonData=json.dumps(jsondata.get('Params').get('FILTER'))
                exp_process.json_classification=json.dumps(jsondata.get('Params').get('CLASSIFICATION'))
                #exp_process.create_by=self.request.query_params.get("Create_by")
                #exp_process.is_commit = self.request.query_params.get("Is_Commit")
                common.main_fun1(request.read(), path)
                inv_out_message=exp_process.get_expensedetails()
                if inv_out_message.get("MESSAGE") == 'FOUND':
                    ld_dict = {"MESSAGE": 'SUCCESS' ,"DATA":json.loads(inv_out_message.get("DATA").to_json(orient='records'))}
                elif inv_out_message.get("MESSAGE") == 'FAIL':
                    ld_dict = {"MESSAGE": inv_out_message.get("MESSAGE")}
                else:
                    ld_dict = {"MESSAGE": 'ERROR_OCCURED',"DATA":inv_out_message}
                return Response(ld_dict)
            elif self.request.query_params.get("Group") == "INV_Process_Single_GET" :
                jsondata = json.loads(request.body.decode('utf-8'))
                exp_process = mBranch.BranchExp_model()
                exp_process.action = self.request.query_params.get("Action")
                exp_process.type = self.request.query_params.get("Type")
                exp_process.jsonData = json.dumps(jsondata.get('Params').get('HEADER'))
                exp_process.jsondata = json.dumps(jsondata.get('Params').get('DETAILS'))
                exp_process.json_rate = json.dumps(jsondata.get('Params').get('RATE'))
                exp_process.json_classification = json.dumps(jsondata.get('Params').get('CLASSIFICATION'))
                exp_process.create_by = self.request.query_params.get("Create_by")
                exp_process.is_commit = self.request.query_params.get("Is_Commit")
                common.main_fun1(request.read(), path)
                inv_out_message = exp_process.get_expensedetails()
                if inv_out_message.get("MESSAGE") == 'SUCCESS':
                    ld_dict = {"MESSAGE": "SUCCESS"}
                elif inv_out_message.get("MESSAGE") == 'FAIL':
                    ld_dict = {"MESSAGE": inv_out_message.get("MESSAGE")}
                else:
                    ld_dict = {"MESSAGE": 'ERROR_OCCURED.' + inv_out_message.get("MESSAGE")}
                return Response(ld_dict)
            elif self.request.query_params.get("action") == "GET" and \
                    (self.request.query_params.get("type")=="PROPERTY" or
                     self.request.query_params.get("type")=="EXPENSE_DETAIL" or
                     self.request.query_params.get("type")=="INVOICE_BRANEXP_SUMMARY" or
                     self.request.query_params.get("type")=="INVOICE_BRANEXP_SUMMARY_COUNT" or
                     self.request.query_params.get("type")=="INVOICE_APPROVAL_COUNT" or
                     self.request.query_params.get("type")=="INVOICE_APPROVAL"):
                jsondata = json.loads(request.body.decode('utf-8'))
                exp_process = mBranch.BranchExp_model()
                exp_process.type = self.request.query_params.get("action")
                exp_process.sub_type = self.request.query_params.get("type")
                exp_process.filter = json.dumps(jsondata.get("params").get("filter"))
                exp_process.classification = json.dumps(jsondata.get("params").get("classification"))
                common.main_fun1(request.read(), path)
                result = exp_process.get_expense_data()
                json_data = json.loads(result.to_json(orient='records'))
                return Response(json_data)

        except Exception as e:
            common.logger.error(e)
            return Response({"MESSAGE": "ERROR_OCCURED", "DATA": str(e)})

class Expense_Process_Set(APIView):
    def post(self,request):
        try:
            path = self.request.stream.path
            if self.request.query_params.get("Group")== "EXPENSE_DATA":
                jsondata = json.loads(request.body.decode('utf-8'))
                exp_process= mBranch.BranchExp_model()
                exp_process.action=self.request.query_params.get("Action")
                exp_process.type=self.request.query_params.get("Type")
                exp_process.create_by=self.request.query_params.get("create_by")
                exp_process.jsonData=json.dumps(jsondata.get('Params').get('FILTER'))
                exp_process.json_classification=json.dumps(jsondata.get('Params').get('CLASSIFICATION'))
                exp_process.create_by=jsondata.get("Params").get("CLASSIFICATION").get("employee_gid")
                #exp_process.create_by=self.request.query_params.get("Create_by")
                #exp_process.is_commit = self.request.query_params.get("Is_Commit")
                common.main_fun1(request.read(), path)
                inv_out_message=exp_process.set_expensedetails()
                if inv_out_message.get("MESSAGE") == 'FOUND':
                    ld_dict = {"MESSAGE": 'SUCCESS' ,"DATA":json.loads(inv_out_message.get("DATA").to_json(orient='records'))}
                elif inv_out_message.get("MESSAGE") == 'FAIL':
                    ld_dict = {"MESSAGE": inv_out_message.get("MESSAGE")}
                elif inv_out_message.get("MESSAGE") == 'SUCCESS':
                    ld_dict = {"MESSAGE": inv_out_message.get("MESSAGE")}
                else:
                    ld_dict = {"MESSAGE": 'ERROR_OCCURED',"DATA":inv_out_message.get("MESSAGE")}
                return Response(ld_dict)
            elif self.request.query_params.get("Group") == "INV_Process_Single_GET" :
                jsondata = json.loads(request.body.decode('utf-8'))
                exp_process = mBranch.BranchExp_model()
                exp_process.action = self.request.query_params.get("Action")
                exp_process.type = self.request.query_params.get("Type")
                exp_process.jsonData = json.dumps(jsondata.get('Params').get('HEADER'))
                exp_process.jsondata = json.dumps(jsondata.get('Params').get('DETAILS'))
                exp_process.json_rate = json.dumps(jsondata.get('Params').get('RATE'))
                exp_process.json_classification = json.dumps(jsondata.get('Params').get('CLASSIFICATION'))
                exp_process.create_by = self.request.query_params.get("Create_by")
                exp_process.is_commit = self.request.query_params.get("Is_Commit")
                common.main_fun1(request.read(), path)
                inv_out_message = exp_process.set_expensedetails()
                if inv_out_message.get("MESSAGE") == 'SUCCESS':
                    ld_dict = {"MESSAGE": "SUCCESS"}
                elif inv_out_message.get("MESSAGE") == 'FAIL':
                    ld_dict = {"MESSAGE": inv_out_message.get("MESSAGE")}
                else:
                    ld_dict = {"MESSAGE": 'ERROR_OCCURED.' + inv_out_message.get("MESSAGE")}
                return Response(ld_dict)

        except Exception as e:
            common.logger.error(e)
            return Response({"MESSAGE": "ERROR_OCCURED", "DATA": str(e)})


class Property_Process_Get(APIView):
    def post(self,request):
        try:
            path = self.request.stream.path
            if self.request.query_params.get("Type")=="PRODUCT":
                jsondata = json.loads(request.body.decode('utf-8'))
                property_types=mBranch.BranchExp_model()
                property_types.type=self.request.query_params.get("Type")
                property_types.entity_gid=self.request.query_params.get("entity_gid")
                property_types.table_values=json.dumps(jsondata.get('filters'))
                common.main_fun1(request.read(), path)
                result =property_types.get_alltablevalue()
                json_data = json.loads(result.to_json(orient='records'))
                return Response(json_data)
            elif self.request.query_params.get("Type")=="PROPERTY":
                if self.request.query_params.get("Sub_Type")=="SUMMARY":
                    jsondata = json.loads(request.body.decode('utf-8'))
                    pro_det=mBranch.BranchExp_model()
                    pro_det.Type=self.request.query_params.get('Type')
                    pro_det.Sub_Type=self.request.query_params.get('Sub_Type')
                    pro_det.filter=json.dumps(jsondata.get('data').get('params').get('filters'))
                    pro_det.classification=json.dumps(jsondata.get('data').get('classification'))
                    common.main_fun1(request.read(), path)
                    pro_result=pro_det.get_pro_details()
                    if pro_result.empty== False:
                        json_data = json.loads(pro_result.to_json(orient='records'))
                        return Response({"MESSAGE":pro_result.get("MESSAGE") , "DATA": json_data})
                    else:
                        return Response({"MESSAGE": "NOT_FOUND"})
            elif self.request.query_params.get("Type")=="GET":
                if self.request.query_params.get("Sub_Type")=="PROPERTY_BRANCH_MAPPING":
                    jsondata = json.loads(request.body.decode('utf-8'))
                    pro_det=mBranch.BranchExp_model()
                    pro_det.Type=self.request.query_params.get('Type')
                    pro_det.Sub_Type=self.request.query_params.get('Sub_Type')
                    pro_det.filter=json.dumps(jsondata.get('data').get('filters'))
                    pro_det.classification=json.dumps(jsondata.get('data').get('classification'))
                    common.main_fun1(request.read(), path)
                    pro_result=pro_det.get_pro_details()
                    if pro_result.empty== False:
                        json_data = json.loads(pro_result.to_json(orient='records'))
                        return Response({"MESSAGE": "FOUND", "DATA": json_data})
                    else:
                        return Response({"MESSAGE":pro_result.get('MESSAGE')})
        except Exception as e:
            common.logger.error(e)
            return Response({"MESSAGE": "ERROR_OCCURED", "DATA": str(e)})

class Property_Process_Set(APIView):
    def post(self, request):
        try:
            path = self.request.stream.path
            if self.request.query_params.get("Type") == "INSERT" and ((self.request.query_params.get("Sub_Type") == "property") or
                                                                      (self.request.query_params.get("Sub_Type") == "Property_Branch") or
                                                                      (self.request.query_params.get("Sub_Type") == "Property_Branch_Insert")):
                jsondata = json.loads(request.body.decode('utf-8'))
                exp_process = mBranch.BranchExp_model()
                exp_process.type = self.request.query_params.get("Type")
                exp_process.sub_type = self.request.query_params.get("Sub_Type")
                exp_process.filters = json.dumps(jsondata.get("data").get('params').get("filters"))
                exp_process.classification = json.dumps(jsondata.get("data").get("classification"))
                common.main_fun1(request.read(), path)
                result = exp_process.property_set()
                if(exp_process.sub_type=="property"):
                    property_data=result.get("MESSAGE")
                    data=property_data.split(",")
                    return Response(data)
                if result.get("MESSAGE") == "SUCCESS":
                    return Response("SUCCESS")
                else:
                    return Response("FAIL")
            if ((self.request.query_params.get("Type") == "update") and ((self.request.query_params.get("Sub_Type") == "ACTIVE_STATUS")
                                                                         or (self.request.query_params.get("Sub_Type") == "property"))):
                    jsondata = json.loads(request.body.decode('utf-8'))
                    exp_process = mBranch.BranchExp_model()
                    exp_process.type = self.request.query_params.get("Type")
                    exp_process.sub_type = self.request.query_params.get("Sub_Type")
                    exp_process.filters = json.dumps(jsondata.get("data").get('params').get("filters"))
                    exp_process.classification = json.dumps(jsondata.get("data").get("classification"))
                    common.main_fun1(request.read(), path)
                    result = exp_process.property_set()
                    if result.get("MESSAGE") == "SUCCESS":
                        return Response("SUCCESS")
                    else:
                        return Response("FAIL")
        except Exception as e:
            common.logger.error(e)
            return Response({"MESSAGE": "ERROR_OCCURED", "DATA": str(e)})

class Premises_Process_Set(APIView):
    def post(self,request):
        try:
            path = self.request.stream.path
            jsondata = json.loads(request.body.decode('utf-8'))
            group=self.request.query_params.get("group")
            action=self.request.query_params.get("action")
            type=self.request.query_params.get("type")
            if(group=="PREMISES" and (action=="INSERT" or action=="ANY" or action=="UPDATE")):
                jsondata = json.loads(request.body.decode('utf-8'))
                exp_process = mBranch.BranchExp_model()
                exp_process.action = self.request.query_params.get("action")
                exp_process.type = self.request.query_params.get("type")
                exp_process.filter = json.dumps(jsondata.get("filter"))
                exp_process.classification = json.dumps(jsondata.get("classification"))
                exp_process.create_by = self.request.query_params.get("create_by")
                common.main_fun1(request.read(), path)
                result = exp_process.premises_set()
                return Response(result)
        except Exception as e:
            common.logger.error(e)
            return Response({"MESSAGE": "ERROR_OCCURED", "DATA": str(e)})

class Premises_Process_Get(APIView):
    def post(self,request):
        try:
            path = self.request.stream.path
            jsondata = json.loads(request.body.decode('utf-8'))
            group = self.request.query_params.get("group")
            action = self.request.query_params.get("action")
            type = self.request.query_params.get("type")
            if (group == "PREMISES" and action == "GET"):
                jsondata = json.loads(request.body.decode('utf-8'))
                exp_process = mBranch.BranchExp_model()
                exp_process.action = self.request.query_params.get("action")
                exp_process.type = self.request.query_params.get("type")
                exp_process.filter = json.dumps(jsondata.get("filter"))
                exp_process.classification = json.dumps(jsondata.get("classification"))
                exp_process.create_by = self.request.query_params.get("create_by")
                common.main_fun1(request.read(), path)
                result =exp_process.premises_get()
                json_data = json.loads(result.to_json(orient='records'))
                return Response(json_data)

        except Exception as e:
            common.logger.error(e)
            return Response({"MESSAGE": "ERROR_OCCURED", "DATA": str(e)})
