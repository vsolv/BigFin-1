from rest_framework.views import APIView
from rest_framework.response import Response
import json
from Bigflow.StandardInstructions.Model import mStandardInstructions
from Bigflow.API import views as commonview
from Bigflow.Core import models as common

class SI_Process_Set(APIView):
    def post(self,request):
        try:
            path = self.request.stream.path
            if self.request.query_params.get("action") == "INSERT" and self.request.query_params.get("type")=="INSERT_STANDARD_INSTRUCTION":
                jsondata = json.loads(request.body.decode('utf-8'))
                StandardInstructions = mStandardInstructions.StandardInstuctions();
                StandardInstructions.action = self.request.query_params.get("action")
                StandardInstructions.type = self.request.query_params.get("type")
                StandardInstructions.filter = json.dumps(jsondata.get("params").get("filter"))
                StandardInstructions.classification = json.dumps(jsondata.get("params").get("classification"))
                StandardInstructions.create_by = self.request.query_params.get("create_by")
                common.main_fun1(request.read(), path)
                result = StandardInstructions.set_SI()
                return Response(result)
            elif self.request.query_params.get("action")=="UPDATE" and ((self.request.query_params.get("type")=="UPDATE_STANDARD_INSTRUCTION_STATUS") or (self.request.query_params.get("type")=="UPDATE_STANDARD_INSTRUCTION_DETAIL_HOLD")):
                jsondata = json.loads(request.body.decode('utf-8'))
                StandardInstructions = mStandardInstructions.StandardInstuctions();
                StandardInstructions.action = self.request.query_params.get("action")
                StandardInstructions.type = self.request.query_params.get("type")
                StandardInstructions.filter = json.dumps(jsondata.get("params").get("filter"))
                StandardInstructions.classification = json.dumps(jsondata.get("params").get("classification"))
                StandardInstructions.create_by = self.request.query_params.get("create_by")
                common.main_fun1(request.read(), path)
                result = StandardInstructions.set_SI()
                return Response(result)

        except Exception as e:
            common.logger.error(e)
            return Response({"MESSAGE": "ERROR_OCCURED", "DATA": str(e)})

class SI_Process_Get(APIView):
    def post(self,request):
        try:
            path = self.request.stream.path
            if self.request.query_params.get("action") == "GET" and (self.request.query_params.get("type")=="STANDARD_INSTRUCTION_HEADER_DETAIL" or
                                                                     self.request.query_params.get("type")=="STANDARD_INSTRUCTION_CCBS_DETAIL" or
                                                                     self.request.query_params.get("type")=="SI_PENDING_FOR_APPROVAL"):
                jsondata = json.loads(request.body.decode('utf-8'))
                StandardInstructions = mStandardInstructions.StandardInstuctions();
                StandardInstructions.action = self.request.query_params.get("action")
                StandardInstructions.type = self.request.query_params.get("type")
                StandardInstructions.filter = json.dumps(jsondata.get("params").get("filter"))
                StandardInstructions.classification = json.dumps(jsondata.get("params").get("classification"))
                StandardInstructions.create_by = self.request.query_params.get("create_by")
                common.main_fun1(request.read(), path)
                result = StandardInstructions.get_SI()
                json_data = json.loads(result.to_json(orient='records'))
                return Response(json_data)

        except Exception as e:
            common.logger.error(e)
            return Response({"MESSAGE": "ERROR_OCCURED", "DATA": str(e)})