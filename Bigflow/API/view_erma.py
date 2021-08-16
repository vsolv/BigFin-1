from rest_framework.views import APIView
from rest_framework.response import Response
import json
import Bigflow.Core.models as common

from Bigflow.eRMA.model import mERMA

### eRMA

class eRMAArchival_API(APIView):
    def post(self, request):
        try:
            if self.request.query_params.get("Group") == "ARCHIVAL":
                jsondata = json.loads(request.body.decode('utf-8'))
                obj_prodcat = mERMA.ERMA_model()
                obj_prodcat.action = self.request.query_params.get("Action")
                obj_prodcat.type = self.request.query_params.get("Type")
                obj_prodcat.jsonData = json.dumps(jsondata.get('Params'))
                obj_prodcat.dataw = json.dumps(jsondata.get('Classification'))
                out_message = obj_prodcat.ermaarchivalset()
                if out_message == "SUCCESSFULLY INSERTED":
                    return Response({"MESSAGE": "SUCCESSFULLY INSERTED"})
                else:
                    return Response({"MESSAGE": out_message})



        except Exception as e:
            return Response({"MESSAGE": "ERROR", "DATA": str(e)})

class Erma_Barcode_API(APIView):
    def post(self, request):
        try:
            if self.request.query_params.get("Group") == "Barcoderequest_summary":
                jsondata = json.loads(request.body.decode('utf-8'))
                obj_barcode = mERMA.ERMA_model()
                obj_barcode.action = self.request.query_params.get("Action")
                obj_barcode.type = self.request.query_params.get("Type")
                obj_barcode.filter = json.dumps(jsondata.get('Filter'))
                obj_barcode.classification = json.dumps(jsondata.get('Classification'))
                out_message = obj_barcode.Get_barcode()
                # out_message = common.outputReturn(out_message,1)
                if out_message.get("MESSAGE") == 'FOUND':
                    ld_dict = {"DATA": json.loads(out_message.get("DATA").to_json(orient='records')),
                               "MESSAGE": 'FOUND'}
                elif out_message.get("MESSAGE") == 'NOT_FOUND':
                    ld_dict = {"MESSAGE": 'NOT_FOUND'}
                else:
                    ld_dict = {"MESSAGE": 'ERROR_OCCURED.' + out_message.get("MESSAGE")}
                return Response(ld_dict)
            if self.request.query_params.get("Group") == "Barcoderequest_add":
                jsondata = json.loads(request.body.decode('utf-8'))
                obj_barcode = mERMA.ERMA_model()
                obj_barcode.action = self.request.query_params.get("Action")
                obj_barcode.type = self.request.query_params.get("Type")
                obj_barcode.subtype = self.request.query_params.get("Sub_Type")
                obj_barcode.Filter = json.dumps(jsondata.get('Filter'))
                obj_barcode.Classification = json.dumps(jsondata.get('Classification'))
                obj_barcode.Status = json.dumps(jsondata.get('Status'))
                obj_barcode.Changes = json.dumps(jsondata.get('Changes'))
                obj_barcode.create_id = self.request.query_params.get("Create_By")
                obj_barcode.create_id1 = int(obj_barcode.create_id)
                obj_barcode.par_json = json.dumps(jsondata.get('par'))
                obj_barcode.pardet_json = json.dumps(jsondata.get('par_detail'))

                out_message = obj_barcode.Set_barcoderequest()
                out_message = common.outputReturn(out_message, 1)

                if out_message == "SUCCESS":
                    return Response({"MESSAGE": "SUCCESS"})
                else:
                    return Response({"MESSAGE": out_message})
        except Exception as e:
            return Response({"MESSAGE": "ERROR" + str(e), "DATA": str(e)})
