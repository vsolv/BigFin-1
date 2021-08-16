from django.core.files.storage import default_storage
from rest_framework.views import APIView
from rest_framework.response import Response
import json
from Bigflow.Collection.Model import mCollection
from Bigflow.Collection.Model import mCollection
from Bigflow.Proofing.Model import mproofing
from Bigflow.Master import views as MasterViews
from Bigflow.Master.Model import mMasters
from Bigflow.Transaction import views
from Bigflow.Transaction.Model import mFET, mSales
from Bigflow.Service.Model import mService

from Bigflow.Core import models as common
from django.http import JsonResponse


class Integrity_API(APIView):
    def post(self, request):
        try:
            if (self.request.query_params.get("Group") == "INTEGRITY_UPLOAD") or (self.request.query_params.get("Group") =="INTEGRITY_PUSHDATA"):
                obj_cltn = mproofing.Proofing_model()
                obj_cltn.action = self.request.query_params.get("Action")
                obj_cltn.type = self.request.query_params.get("Type")
                obj_cltn.jsonData = json.loads(request.body.decode('utf-8')).get('params').get('DATA')
                obj_cltn.jsondata = json.loads(request.body.decode('utf-8')).get('params').get('FILE')
                obj_cltn.json_clsfn = json.loads(request.body.decode('utf-8')).get('params').get('CLASSIFICATION')
                obj_cltn.json_classification = json.dumps(obj_cltn.json_clsfn)
                obj_cltn.create_by = self.request.query_params.get("Employee_Gid")
                out_message = obj_cltn.set_integrity_upload()
                if out_message == 'SUCCESS':
                    return Response({"MESSAGE": "SUCCESS"})
                else:
                    return Response({"MESSAGE": "FAIL"})

            elif self.request.query_params.get("Group") == "INTEGRITY_SUMMARY":
                obj_cltn = mproofing.Proofing_model()
                obj_cltn.Type = self.request.query_params.get("Type")
                obj_cltn.sub_type = self.request.query_params.get("Sub_Type")
                obj_cltn.filter_json = json.loads(request.body.decode('utf-8')).get('params').get('Filter')
                obj_cltn.json_clsfn = json.loads(request.body.decode('utf-8')).get('params').get('Classification')
                obj_cltn.json_classification = json.dumps(obj_cltn.json_clsfn)
                df_lead_view = obj_cltn.Get_Mainentry()
                jdata = df_lead_view.to_json(orient='records')
                return JsonResponse(json.loads(jdata), safe=False)


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