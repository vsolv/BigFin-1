from rest_framework.views import APIView
from rest_framework.views import Response
import json
from Bigflow.Claim.model import mClaim
from Bigflow.API import views as commonview
from Bigflow.Core.models import decrpt as decry_data
class TA_Initial(APIView):
    def post(self,request):
        try:
            if self.request.query_params.get("Group") == "CLAIM_INITIAL_SUMMARY":
                ##### Get The Data To Show the Temp Data In Summary
                jsondata = json.loads(request.body.decode('utf-8'))
                obj_ta = mClaim.Claim_model()
                obj_ta.type = self.request.query_params.get("Type")
                obj_ta.sub_type = self.request.query_params.get("Sub_Type")
                obj_ta.jsonData = json.dumps(jsondata.get('Params').get('FILTER'))
                obj_ta.json_classification = jsondata.get('Params').get('CLASSIFICATION')
                obj_ta.json_classification['Entity_Gid'] =[decry_data(jsondata.get('Params').get('CLASSIFICATION').get('Entity_Gid'))]

                obj_ta.json_classification =json.dumps(obj_ta.json_classification)
                ld_out_message = obj_ta.get_claim_summary()
                if ld_out_message.get("MESSAGE") == 'FOUND':
                    ld_dict = {"DATA":json.loads(ld_out_message.get("DATA").to_json(orient='records')),"MESSAGE":'FOUND'}
                elif ld_out_message.get("MESSAGE") == 'NOT_FOUND':
                    ld_dict = {"MESSAGE":'NOT_FOUND'}
                else:
                    ld_dict = {"MESSAGE": 'ERROR_OCCURED.' + ld_out_message.get("MESSAGE")}
                return Response(ld_dict)

            elif self.request.query_params.get("Group") == "Claim_Process_get":
                jsondata = json.loads(request.body.decode('utf-8'))
                obj_claim = mClaim.Claim_model()
                obj_claim.type = self.request.query_params.get("Type")
                obj_claim.sub_type = self.request.query_params.get("Sub_Type")
                obj_claim.jsonData = json.dumps(jsondata.get('Params').get('FILTER'))
                obj_claim.jsondata = '{}'
                obj_claim.json_classification = jsondata.get('Params').get('CLASSIFICATION')
                obj_claim.json_classification['Entity_Gid'] = [decry_data(jsondata.get('Params').get('CLASSIFICATION').get('Entity_Gid'))]
                obj_claim.json_classification = json.dumps(obj_claim.json_classification)

                obj_claim.employee_gid = decry_data(self.request.query_params.get("Employee_Gid"))
                ld_out_message = obj_claim.get_claim_summary()
                if ld_out_message.get("MESSAGE") == 'FOUND':
                    ld_dict = {"DATA": json.loads(ld_out_message.get("DATA").to_json(orient='records')),
                               "MESSAGE": 'FOUND'}
                elif ld_out_message.get("MESSAGE") == 'NOT_FOUND':
                    ld_dict = {"MESSAGE": 'NOT_FOUND'}
                else:
                    ld_dict = {"MESSAGE": 'ERROR_OCCURED.' + ld_out_message.get("MESSAGE")}
                return Response(ld_dict)

            elif self.request.query_params.get("Group") == "CLAIM_INITIAL_SET":
                jsondata = json.loads(request.body.decode('utf-8'))
                obj_claim = mClaim.Claim_model()
                obj_claim.action = self.request.query_params.get("Action")
                obj_claim.type = self.request.query_params.get("Type")
                obj_claim.sub_type = self.request.query_params.get("Sub_Type")
                obj_claim.jsonData = json.dumps(jsondata.get('Params').get('DETAILS'))
                obj_claim.jsondata = '{}'
                obj_claim.json_classification = jsondata.get('Params').get('CLASSIFICATION')
                obj_claim.json_classification['Entity_Gid'] = [decry_data(jsondata.get('Params').get('CLASSIFICATION').get('Entity_Gid'))]
                obj_claim.json_classification = json.dumps(obj_claim.json_classification)
                obj_claim.employee_gid = decry_data(self.request.query_params.get("Employee_Gid"))
                ###
                # Here To Save The File In a Directory
                obj_claim.json_file = json.dumps(jsondata.get('Params').get('File'))

                saved_filepath = commonview.File_Upload(obj_claim.json_file,'CLAIM',obj_claim.employee_gid)
                obj_claim.json_file = json.dumps(saved_filepath)
                ###


                ld_out_message = obj_claim.set_claim()

                if ld_out_message.get("MESSAGE") == 'SUCCESS':
                    ld_dict = {"MESSAGE": "SUCCESS"}
                elif ld_out_message.get("MESSAGE") == 'FAIL':
                    ld_dict = {"MESSAGE": "FAIL"}
                else:
                    ld_dict = {"MESSAGE": 'ERROR_OCCURED.' + ld_out_message.get("MESSAGE")}
                return Response(ld_dict)

            elif self.request.query_params.get("Group") == "CLAIM_APPROVE_PROCESS":
                jsondata = json.loads(request.body.decode('utf-8'))
                obj_claim = mClaim.Claim_model()
                obj_claim.action = self.request.query_params.get("Action")
                obj_claim.type = self.request.query_params.get("Type")
                obj_claim.sub_type = self.request.query_params.get("Sub_Type")
                obj_claim.jsonData = json.dumps(jsondata.get('Params').get('DETAILS'))
                obj_claim.jsondata = '{}'
                obj_claim.json_classification = jsondata.get('Params').get('CLASSIFICATION')
                obj_claim.json_classification['Entity_Gid'] = [decry_data(jsondata.get('Params').get('CLASSIFICATION').get('Entity_Gid'))]
                obj_claim.json_classification = json.dumps(obj_claim.json_classification)
                obj_claim.employee_gid = decry_data(self.request.query_params.get("Employee_Gid"))
                ld_out_message = obj_claim.set_claim()

                if ld_out_message.get("MESSAGE") == 'SUCCESS':
                    ld_dict = {"MESSAGE": "SUCCESS"}
                elif ld_out_message.get("MESSAGE") == 'FAIL':
                    ld_dict = {"MESSAGE": "FAIL"}
                else:
                    ld_dict = {"MESSAGE": 'ERROR_OCCURED.' + ld_out_message.get("MESSAGE")}
                return Response(ld_dict)


        except Exception as e:
            return Response({"MESSAGE":"ERROR_OCCURED","DATA":str(e)})

class ScanModule(APIView):
    def post(self,request):
        jsondata = json.loads(request.body.decode('utf-8'))
        obj_claim = mClaim.Claim_model()
        obj_claim.action = self.request.query_params.get("Action")
        obj_claim.type = self.request.query_params.get("Type")
        obj_claim.sub_type = self.request.query_params.get("Sub_Type")
        obj_claim.jsonData = json.dumps(jsondata.get('Params').get('DETAILS'))
        obj_claim.jsondata = '{}'
        obj_claim.json_classification = json.dumps(jsondata.get('Params').get('CLASSIFICATION'))
        obj_claim.employee_gid = self.request.query_params.get("Employee_Gid")
        obj_claim.File_count = self.request.query_params.get("PDF_count")
        obj_claim.json_file = json.dumps(jsondata.get('Params').get('File'))
        saved_filepath = commonview.File_Uploadforscan(obj_claim.json_file, 'INWARD', obj_claim.employee_gid,obj_claim.File_count)
        obj_claim.json_file = json.dumps(saved_filepath)
        return Response("data:{MESSAGE:SUCCESS1222}")