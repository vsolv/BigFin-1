from rest_framework.views import APIView
from rest_framework.response import Response
import json
import Bigflow.Core.models as common
from Bigflow.API import views as commonview
from Bigflow.MEP.model import mMEP
from Bigflow.Core.models import decrpt as decry_data
import boto3
import time
import datetime

class PARSET_API(APIView):
    def post(self, request):
        try:
            if self.request.query_params.get("Group") == "Add_Par":
                jsondata = json.loads(request.body.decode('utf-8'))
                obj_prodcat = mMEP.MEP_model()
                obj_prodcat.action = self.request.query_params.get("Action")
                obj_prodcat.type = self.request.query_params.get("Type")
                obj_prodcat.jsonData = json.dumps(jsondata.get('Params'))
                entity = decry_data(jsondata.get('Classification')['Entity_Gid'])
                obj_prodcat.dataw = json.dumps({'Entity_Gid':entity})
                obj_prodcat.create_id = self.request.query_params.get("Create_By")
                obj_prodcat.create_id1 = decry_data(obj_prodcat.create_id)
                par_json = jsondata.get('par')
                notepad = jsondata.get('Notepad')
                if notepad != "":
                    millis = int(round(time.time() * 1000))
                    filename = self.request.query_params.get("Create_By") + "_" + str(millis)+'.txt'
                    s3 = boto3.resource('s3')
                    object = s3.Object(common.s3_bucket_name(), filename)
                    object.put(Body=notepad)
                else:
                    filename = ""
                obj_prodcat.filename = filename
                par_json.update({"par_filepath":filename})
                obj_prodcat.par_json = json.dumps(par_json)
                obj_prodcat.pardet_json111 = json.dumps(jsondata.get('par_detail').get('pardetails_insert'))
                obj_prodcat.pardet_json11 = jsondata.get('par_detail').get('pardetails_insert')
                obj_prodcat.a=json.dumps({"pardetails_insert":obj_prodcat.pardet_json11})
                out_message = obj_prodcat.Set_PAR_PARDET()
                out_message = common.outputReturn(out_message, 1)

                if out_message == "SUCCESSFULLY INSERTED":
                    return Response({"MESSAGE": "SUCCESSFULLY INSERTED"})
                else:
                    return Response({"MESSAGE": out_message})
            if self.request.query_params.get("Group") == "Add_Update":
                jsondata = json.loads(request.body.decode('utf-8'))
                obj_prodcat = mMEP.MEP_model()
                obj_prodcat.action = self.request.query_params.get("Action")
                obj_prodcat.type = self.request.query_params.get("Type")
                obj_prodcat.jsonData = json.dumps(jsondata.get('Params'))
                entity = decry_data(jsondata.get('Classification')['Entity_Gid'])
                obj_prodcat.dataw = json.dumps({'Entity_Gid': entity})
                obj_prodcat.create_id = decry_data(self.request.query_params.get("Create_By"))
                obj_prodcat.create_id1 = int(obj_prodcat.create_id)
                par_json = jsondata.get('par')
                notepad = par_json.get('Notepad')
                if notepad != "" and (jsondata.get('par').get('par_status')) == 'PENDING-APPROVAL':
                    millis = int(round(time.time() * 1000))
                    filename = self.request.query_params.get("Create_By") + "_" + str(millis) + '.txt'
                    s3 = boto3.resource('s3')
                    object = s3.Object(common.s3_bucket_name(), filename)
                    object.put(Body=notepad)
                else:
                    filename = ""
                obj_prodcat.filename = filename
                par_json.update({"par_filepath": filename})
                obj_prodcat.par_json = json.dumps(par_json)
                obj_prodcat.a = json.dumps(jsondata.get('par_detail'))
                obj_prodcat.pardet_json111 = json.dumps(jsondata.get('par_detail').get('pardetails_insert'))
                obj_prodcat.pardet_json11 = jsondata.get('par_detail').get('pardetails_insert')
                obj_prodcat.pardet_json1 = json.dumps(jsondata.get('file'))
                out_message = obj_prodcat.Set_PAR_PARDET()
                out_message = common.outputReturn(out_message, 1)

                if out_message == "SUCCESSFULLY INSERTED":
                    return Response({"MESSAGE": "SUCCESSFULLY INSERTED"})
                else:
                    return Response({"MESSAGE": out_message})

        except Exception as e:
            return Response({"MESSAGE": "ERROR" + str(e), "DATA": str(e)})

class PARGET_API(APIView):
    def post(self, request):
        try:
            if self.request.query_params.get("Group") == "PAR_GET":
                jsondata = json.loads(request.body.decode('utf-8'))
                obj_prodcat = mMEP.MEP_model()
                obj_prodcat.action = self.request.query_params.get("Action")
                obj_prodcat.type = self.request.query_params.get("Type")
                obj_prodcat.dataw = json.dumps(jsondata.get('Filter'))
                obj_prodcat.create_id = decry_data(self.request.query_params.get("Create_By"))
                Entity_Gid = decry_data(jsondata.get('Classification')['Entity_Gid'])
                obj_prodcat.Entity_Gid = json.dumps({'Entity_Gid':Entity_Gid})
                obj_prodcat.create_id1 = obj_prodcat.create_id
                out_message = obj_prodcat.Get_PAR_PARDET()
                # out_message = common.outputReturn(out_message,1)
                if out_message.get("MESSAGE") == 'FOUND':
                    ld_dict = {"DATA": json.loads(out_message.get("DATA").to_json(orient='records')),
                               "MESSAGE": 'FOUND'}
                elif out_message.get("MESSAGE") == 'NOT_FOUND':
                    ld_dict = {"MESSAGE": 'NOT_FOUND'}
                else:
                    ld_dict = {"MESSAGE": 'ERROR_OCCURED.' + out_message.get("MESSAGE")}
                return Response(ld_dict)
        except Exception as e:
            return Response({"MESSAGE": "ERROR" + str(e), "DATA": str(e)})

class MEPSET_API(APIView):
    def post(self, request):
        try:
            if self.request.query_params.get("Group") == "Add_Mep":
                jsondata = json.loads(request.body.decode('utf-8'))
                obj_prodcat = mMEP.MEP_model()
                obj_prodcat.action = self.request.query_params.get("Action")
                obj_prodcat.type = self.request.query_params.get("Type")
                obj_prodcat.jsonData = json.dumps(jsondata.get('Params'))
                dataw = jsondata.get('Classification')
                dataw['Entity_Gid'] = decry_data(jsondata.get('Classification')['Entity_Gid'])
                obj_prodcat.dataw = json.dumps(dataw)
                obj_prodcat.create_id = self.request.query_params.get("Create_By")
                obj_prodcat.create_id1 = decry_data(obj_prodcat.create_id)
                par_json = jsondata.get('par')
                notepad = par_json.get('Notepad')
                if notepad != "" and (jsondata.get('par').get('mep_status')) == 'PENDING-APPROVAL':
                    millis = int(round(time.time() * 1000))
                    filename = self.request.query_params.get("Create_By") + "_" + str(millis)+".txt"
                    s3 = boto3.resource('s3')
                    object = s3.Object(common.s3_bucket_name(), filename)
                    object.put(Body=notepad)
                else:
                    filename = ""
                obj_prodcat.filename = filename
                par_json.update({"mep_filepath": filename})
                obj_prodcat.par_json = json.dumps(par_json)
                obj_prodcat.pardet_json = json.dumps(jsondata.get('par_detail'))

                out_message = obj_prodcat.Set_MEP_PARDET()
                out_message = common.outputReturn(out_message, 1)

                if out_message == "SUCCESSFULLY INSERTED":
                    return Response({"MESSAGE": "SUCCESSFULLY INSERTED"})
                else:
                    return Response({"MESSAGE": out_message})
        except Exception as e:
            return Response({"MESSAGE": "ERROR" + str(e), "DATA": str(e)})

class MEPGET_API(APIView):
    def post(self, request):
        try:
            if self.request.query_params.get("Group") == "MEP_GET":
                jsondata = json.loads(request.body.decode('utf-8'))
                obj_prodcat = mMEP.MEP_model()
                obj_prodcat.action = self.request.query_params.get("Action")
                obj_prodcat.type = self.request.query_params.get("Type")
                obj_prodcat.dataw = json.dumps(jsondata.get('Filter'))
                obj_prodcat.create_id = self.request.query_params.get("Create_By")
                clasification = jsondata.get('Classification')
                entity =  decry_data(jsondata.get('Classification')['Entity_Gid'])
                clasification['Entity_Gid'] = entity
                obj_prodcat.Entity_Gid = json.dumps(clasification)
                create = obj_prodcat.create_id
                obj_prodcat.create_id1 = decry_data(create)
                out_message = obj_prodcat.Get_MEP_PARDET()
                # out_message = common.outputReturn(out_message,1)
                if out_message.get("MESSAGE") == 'FOUND':
                    ld_dict = {"DATA": json.loads(out_message.get("DATA").to_json(orient='records')),
                               "MESSAGE": 'FOUND'}
                elif out_message.get("MESSAGE") == 'NOT_FOUND':
                    ld_dict = {"MESSAGE": 'NOT_FOUND'}
                else:
                    ld_dict = {"MESSAGE": 'ERROR_OCCURED.' + out_message.get("MESSAGE")}
                return Response(ld_dict)
        except Exception as e:
            return Response({"MESSAGE": "ERROR" + str(e), "DATA": str(e)})