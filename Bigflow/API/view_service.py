from rest_framework.views import APIView
from rest_framework.response import Response
from Bigflow.Service.Model import mService
import Bigflow.Service.views as serviceview
from Bigflow.Core.models import decrpt as decry_data
import json


class Service_SetAPI(APIView):
    def post(self,request):
        Object_serviceset = serviceview.Service_set(request)
        return Response({"MESSAGE":json.loads(Object_serviceset.content.decode('utf-8'))})

class Service_SummaryGetAPI(APIView):
    def post(self,request):
        request.session['Entity_gid'] = decry_data(self.request.query_params.get("Entity_gid"))
        request.session['Emp_gid'] = decry_data(self.request.query_params.get("Emp_gid"))
        Object_summaryget = serviceview.ServiceDtl_get(request)
        if len(json.loads(Object_summaryget.content.decode('utf-8'))) > 0:
           return Response({"MESSAGE":"FOUND","DATA":json.loads(Object_summaryget.content.decode('utf-8'))})
        else:
            return Response({"MESSAGE": "NOT_FOUND"})

class CourierName_get(APIView):
    def post(self,request):
        request.session['Entity_gid'] = decry_data(self.request.query_params.get("Entity_gid"))
        Object_courierget = serviceview.Courier_dtl(request)
        if len(json.loads(Object_courierget.content.decode('utf-8'))) > 0:
            return Response({"MESSAGE": "FOUND", "DATA": json.loads(Object_courierget.content.decode('utf-8'))})
        else:
            return Response({"MESSAGE": "NOT_FOUND"})


class Dispatch_set(APIView):
    def post(self,request):
        try:
            request.session['Emp_gid'] =  decry_data(self.request.query_params.get("Employee_Gid"))
            Object_serviceset = serviceview.Dispatch_Set(request)
            return Response({"MESSAGE":json.loads(Object_serviceset.content.decode('utf-8'))})
        except Exception as e:
            return Response({"MESSAGE": "ERROR_OCCURED", "DATA": str(e)})

