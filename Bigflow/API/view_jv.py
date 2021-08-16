from rest_framework.views import APIView
from rest_framework.response import Response
import json
from Bigflow.JV.Model import mJV
from Bigflow.API import views as commonview
from Bigflow.Core import models as common
import Bigflow.Core.jwt_file as jwt
token = common.token()
ip = common.localip()
import requests


class JV_Process_Set_API(APIView):
    def post(self,request):
        try:
            path = self.request.stream.path
            if self.request.query_params.get("action") == "INSERT" and self.request.query_params.get("type")=="JV_CREATION" or "JV_ENTRY_UPDATE":
                jsondata = json.loads(request.body.decode('utf-8'))
                jv_Object = mJV.JV()
                jv_Object.action = self.request.query_params.get("action")
                jv_Object.type = self.request.query_params.get("type")
                jv_Object.filter = json.dumps(jsondata.get("filter"))
                jv_Object.classification = json.dumps(jsondata.get("classification"))
                jv_Object.create_by = self.request.query_params.get("create_by")
                common.main_fun1(request.read(), path)
                result = jv_Object.jv_process_set_model()
                return Response(result)
        except Exception as e:
            common.logger.error(e)
            return Response({"MESSAGE": "ERROR_OCCURED", "DATA": str(e)})

    def outputSplit(tubledtl, index):
        temp = tubledtl[0].split(',')
        if (len(temp) > 1):
            if (index == 0):
                return int(temp[0])
            else:
                return temp[1]
        else:
            return temp[0]

class JV_Process_Get_API(APIView):
    def post(self,request):
        try:
            path = self.request.stream.path
            if self.request.query_params.get("action") == "GET" and (self.request.query_params.get("type")=="JV_HEADER_SUMMARY" or "JV_DETAILS" or "JV_TRANS_GET"):
                jsondata = json.loads(request.body.decode('utf-8'))
                jv_Object = mJV.JV()
                jv_Object.action = self.request.query_params.get("action")
                jv_Object.type = self.request.query_params.get("type")
                jv_Object.filter = json.dumps(jsondata.get("filter"))
                jv_Object.classification = json.dumps(jsondata.get("classification"))
                jv_Object.create_by = self.request.query_params.get("create_by")
                common.main_fun1(request.read(), path)
                result = jv_Object.jv_process_get_model()
                json_data = json.loads(result.to_json(orient='records'))
                return Response(json_data)

        except Exception as e:
            common.logger.error(e)
            return Response({"MESSAGE": "ERROR_OCCURED", "DATA": str(e)})