from rest_framework.views import APIView
from rest_framework.response import Response
import json
import Bigflow.Core.models as common
from Bigflow.API import views as commonview
from Bigflow.Memo.model import mMemo

class Memo_Request_API(APIView):
    def post(self, request):
        try:
            if self.request.query_params.get("Group") == "MemoRequest_Group" or self.request.query_params.get("Group") == "MemoRequestnofile_Group":
                jsondata = json.loads(request.body.decode('utf-8'))
                obj_prodcat = mMemo.Memo_model()
                obj_prodcat.action = self.request.query_params.get("Action")
                obj_prodcat.type = self.request.query_params.get("Type")
                obj_prodcat.SubType = self.request.query_params.get("SubType")
                obj_prodcat.type1 = self.request.query_params.get("Entity_Gid")
                obj_prodcat.Entity_Gid1 = {"Entity_Gid":obj_prodcat.type1}
                obj_prodcat.status = json.dumps({"Request_Status":"PENDING-APPROVAL"})
                obj_prodcat.Create_By = self.request.query_params.get("Create_By")
                obj_prodcat.Create_By1 = int(obj_prodcat.Create_By)
                obj_prodcat.jsonData = json.dumps(jsondata)
                obj_prodcat.Entity_Gid = json.dumps(obj_prodcat.Entity_Gid1)
                obj_prodcat.create_id = self.request.query_params.get("Create_By")
                obj_prodcat.create_id1 = int(obj_prodcat.create_id)
                out_message = obj_prodcat.Set_MemoRequest()
                out_message = common.outputReturn(out_message, 1)

                if out_message == "SUCCESSFULLY INSERTED":
                    return Response({"MESSAGE": "SUCCESSFULLY INSERTED"})
                else:
                    return Response({"MESSAGE": out_message})
            if self.request.query_params.get("Group") == "MemoRequest_Groupnofileupdate" or self.request.query_params.get("Group") == "MemoRequest_Groupfileupdate":
                jsondata = json.loads(request.body.decode('utf-8'))
                obj_prodcat = mMemo.Memo_model()
                obj_prodcat.action = self.request.query_params.get("Action")
                obj_prodcat.type = self.request.query_params.get("Type")
                obj_prodcat.SubType = self.request.query_params.get("SubType")
                obj_prodcat.type1 = self.request.query_params.get("Entity_Gid")
                obj_prodcat.Entity_Gid1 = {"Entity_Gid": obj_prodcat.type1}
                obj_prodcat.status = json.dumps({})
                obj_prodcat.Create_By = self.request.query_params.get("Create_By")
                obj_prodcat.Create_By1 = int(obj_prodcat.Create_By)
                obj_prodcat.jsonData = json.dumps(jsondata)
                obj_prodcat.Entity_Gid = json.dumps(obj_prodcat.Entity_Gid1)
                obj_prodcat.create_id = self.request.query_params.get("Create_By")
                obj_prodcat.create_id1 = int(obj_prodcat.create_id)
                out_message = obj_prodcat.update_MemoRequest()
                out_message = common.outputReturn(out_message, 1)

                if out_message == "SUCCESSFULLY INSERTED":
                    return Response({"MESSAGE": "SUCCESSFULLY INSERTED"})
                else:
                    return Response({"MESSAGE": out_message})


        except Exception as e:
            return Response({"MESSAGE": "ERROR" + str(e), "DATA": str(e)})

class Memo_Request_GetAPI(APIView):
    def post(self, request):
        try:
            if self.request.query_params.get("Group") == "Memoget_Grp":
                path = self.request.stream.path
                jsondata = json.loads(request.body.decode('utf-8'))
                obj_prodcat = mMemo.Memo_model()
                obj_prodcat.action = self.request.query_params.get("Action")
                obj_prodcat.type = self.request.query_params.get("Type")
                obj_prodcat.dataw = json.dumps(jsondata.get('Filter'))
                obj_prodcat.create_id = self.request.query_params.get("Create_By")
                obj_prodcat.Entity_Gid = json.dumps(jsondata.get('Classification'))
                obj_prodcat.create_id1 = int(obj_prodcat.create_id)
                common.main_fun1(request.read(), path)
                out_message = obj_prodcat.Get_MemoReqeust()
                # out_message = common.outputReturn(out_message,1)
                if out_message.get("MESSAGE") == 'FOUND':
                    ld_dict = {"DATA": json.loads(out_message.get("DATA").to_json(orient='records')),
                               "MESSAGE": 'FOUND'}
                elif out_message.get("MESSAGE") == 'NOT_FOUND':
                    ld_dict = {"MESSAGE": 'NOT_FOUND'}
                else:
                    ld_dict = {"MESSAGE": 'ERROR_OCCURED.' + out_message.get("MESSAGE")}
                return Response(ld_dict)
            if self.request.query_params.get("Group") == "Memotransation_Grp":
                path = self.request.stream.path
                jsondata = json.loads(request.body.decode('utf-8'))
                obj_prodcat = mMemo.Memo_model()
                obj_prodcat.action = self.request.query_params.get("Action")
                obj_prodcat.type = self.request.query_params.get("Type")
                obj_prodcat.dataw = json.dumps(jsondata.get('Filter'))
                obj_prodcat.create_id = self.request.query_params.get("Create_By")
                obj_prodcat.Entity_Gid = json.dumps(jsondata.get('Classification'))
                #obj_prodcat.create_id1 = int(obj_prodcat.create_id)
                common.main_fun1(request.read(), path)
                out_message = obj_prodcat.Get_Memotransation()
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

class Memo_Approvel_SetAPI(APIView):
    def post(self, request):
        try:
            if self.request.query_params.get("Group") == "MemoApprovelset_Group":
                path = self.request.stream.path
                jsondata = json.loads(request.body.decode('utf-8'))
                obj_prodcat = mMemo.Memo_model()
                obj_prodcat.action = self.request.query_params.get("Action")
                obj_prodcat.type = self.request.query_params.get("Type")
                obj_prodcat.SubType = self.request.query_params.get("SubType")
                obj_prodcat.type1 = self.request.query_params.get("Entity_Gid")
                obj_prodcat.Entity_Gid1 = {"Entity_Gid":obj_prodcat.type1}
                obj_prodcat.status12 = self.request.query_params.get("status_request")
                obj_prodcat.status = json.dumps({"Requesttran_Status": obj_prodcat.status12})
                obj_prodcat.Create_By = self.request.query_params.get("Create_By")
                obj_prodcat.Create_By1 = int(obj_prodcat.Create_By)
                obj_prodcat.jsonData = json.dumps(jsondata)
                obj_prodcat.Entity_Gid = json.dumps(obj_prodcat.Entity_Gid1)
                obj_prodcat.create_id = self.request.query_params.get("Create_By")
                obj_prodcat.create_id1 = int(obj_prodcat.create_id)
                common.main_fun1(request.read(), path)
                out_message = obj_prodcat.Set_MemoApproval()
                out_message = common.outputReturn(out_message, 1)

                if out_message == "SUCCESSFULLY INSERTED":
                    return Response({"MESSAGE": "SUCCESSFULLY INSERTED"})
                else:
                    return Response({"MESSAGE": out_message})

            if self.request.query_params.get("Group") == "MemoApprovelsetnofile_Group":
                path = self.request.stream.path
                jsondata = json.loads(request.body.decode('utf-8'))
                obj_prodcat = mMemo.Memo_model()
                obj_prodcat.action = self.request.query_params.get("Action")
                obj_prodcat.type = self.request.query_params.get("Type")
                obj_prodcat.SubType = self.request.query_params.get("SubType")
                obj_prodcat.type1 = self.request.query_params.get("Entity_Gid")
                obj_prodcat.Entity_Gid1 = {"Entity_Gid":obj_prodcat.type1}
                obj_prodcat.status12 = self.request.query_params.get("status_request")
                obj_prodcat.status = json.dumps({"Requesttran_Status":obj_prodcat.status12})
                obj_prodcat.Create_By = self.request.query_params.get("Create_By")
                obj_prodcat.Create_By1 = int(obj_prodcat.Create_By)
                obj_prodcat.jsonData = json.dumps(jsondata)
                obj_prodcat.Entity_Gid = json.dumps(obj_prodcat.Entity_Gid1)
                obj_prodcat.create_id = self.request.query_params.get("Create_By")
                obj_prodcat.create_id1 = int(obj_prodcat.create_id)
                common.main_fun1(request.read(), path)
                out_message = obj_prodcat.Set_MemoApproval()
                out_message = common.outputReturn(out_message, 1)

                if out_message == "SUCCESSFULLY INSERTED":
                    return Response({"MESSAGE": "SUCCESSFULLY INSERTED"})
                else:
                    return Response({"MESSAGE": out_message})
            if self.request.query_params.get('Group')=='Active_Inactive':
                path = self.request.stream.path
                jsondata = json.loads(request.body.decode('utf-8'))
                obj_active = mMemo.Memo_model()
                obj_active.Action = self.request.query_params.get("Action")
                obj_active.Type = self.request.query_params.get("Type")
                obj_active.SubType = self.request.query_params.get("Subtype")
                obj_active.Update_By1 = (self.request.query_params.get("Create_By"))
                obj_active.Update_By = int(obj_active.Update_By1)
                obj_active.Filter = json.dumps(jsondata.get('Filter'))
                obj_active.Classification = json.dumps(jsondata.get("Classification"))
                obj_active.AddJson = json.dumps(jsondata.get("AddJson"))
                common.main_fun1(request.read(), path)
                out_message = obj_active.Update_Isactive()
                out_message = common.outputReturn(out_message,0)
                if out_message == "SUCCESSFULLY INSERTED":
                    return Response({"MESSAGE": "SUCCESSFULLY INSERTED"})
                else:
                    return Response({"MESSAGE": out_message})
            if self.request.query_params.get('Group')=='Memotransationset_Grp':
                path = self.request.stream.path
                jsondata = json.loads(request.body.decode('utf-8'))
                obj_active = mMemo.Memo_model()
                obj_active.Action = self.request.query_params.get("Action")
                obj_active.Type = self.request.query_params.get("Type")
                obj_active.SubType = self.request.query_params.get("Subtype")
                obj_active.Update_By1 = (self.request.query_params.get("Create_By"))
                obj_active.Update_By = int(obj_active.Update_By1)
                obj_active.Filter = json.dumps(jsondata.get('Filter'))
                obj_active.Classification = json.dumps(jsondata.get("Classification"))
                obj_active.AddJson = json.dumps(jsondata.get("status_json"))
                common.main_fun1(request.read(), path)
                out_message = obj_active.Update_transaction()
                out_message = common.outputReturn(out_message,0)
                if out_message == "SUCCESS":
                    return Response({"MESSAGE": "SUCCESS"})
                else:
                    return Response({"MESSAGE": out_message})


        except Exception as e:
            return Response({"MESSAGE": "ERROR" + str(e), "DATA": str(e)})

class Memo_Master_SetAPI(APIView):
    def post(self, request):
        try:
            if self.request.query_params.get("Group") == "Category_Grp":
                jsondata = json.loads(request.body.decode('utf-8'))
                obj_active = mMemo.Memo_model()
                obj_active.Action = self.request.query_params.get("Action")
                obj_active.Type = self.request.query_params.get("Type")
                obj_active.SubType = self.request.query_params.get("Subtype")
                obj_active.Update_By1 = (self.request.query_params.get("Create_By"))
                obj_active.Update_By = int(obj_active.Update_By1)
                obj_active.Filter = json.dumps(jsondata.get('Filter'))
                obj_active.Classification = json.dumps(jsondata.get("Classification"))
                obj_active.AddJson = json.dumps(jsondata.get("AddJson"))
                out_message = obj_active.Category_Set()
                out_message = common.outputReturn(out_message, 0)

                if out_message == "SUCCESS":
                    return Response({"MESSAGE": "SUCCESS"})
                else:
                    return Response({"MESSAGE": out_message})
            if self.request.query_params.get("Group") == "SubCategory_Grp":
                jsondata = json.loads(request.body.decode('utf-8'))
                obj_active = mMemo.Memo_model()
                obj_active.Action = self.request.query_params.get("Action")
                obj_active.Type = self.request.query_params.get("Type")
                obj_active.SubType = self.request.query_params.get("Subtype")
                obj_active.Update_By1 = (self.request.query_params.get("Create_By"))
                obj_active.Update_By = int(obj_active.Update_By1)
                obj_active.Filter = json.dumps(jsondata.get('Filter'))
                obj_active.Classification = json.dumps(jsondata.get("Classification"))
                obj_active.AddJson = json.dumps(jsondata.get("AddJson"))
                out_message = obj_active.SubCategory_Set()
                out_message = common.outputReturn(out_message, 0)

                if out_message == "SUCCESS":
                    return Response({"MESSAGE": "SUCCESS"})
                else:
                    return Response({"MESSAGE": out_message})
            if self.request.query_params.get("Group") == "UpdateCategory_Grp":
                jsondata = json.loads(request.body.decode('utf-8'))
                obj_active = mMemo.Memo_model()
                obj_active.Action = self.request.query_params.get("Action")
                obj_active.Type = self.request.query_params.get("Type")
                obj_active.SubType = self.request.query_params.get("Subtype")
                obj_active.Update_By1 = (self.request.query_params.get("Create_By"))
                obj_active.Update_By = int(obj_active.Update_By1)
                obj_active.Filter = json.dumps(jsondata.get('Filter'))
                obj_active.Classification = json.dumps(jsondata.get("Classification"))
                obj_active.AddJson = json.dumps(jsondata.get("AddJson"))
                out_message = obj_active.updateCategory_Set()
                out_message = common.outputReturn(out_message, 0)

                if out_message == "SUCCESS":
                    return Response({"MESSAGE": "SUCCESS"})
                else:
                    return Response({"MESSAGE": out_message})
            if self.request.query_params.get("Group") == "Active_Inactive":
                jsondata = json.loads(request.body.decode('utf-8'))
                obj_active = mMemo.Memo_model()
                obj_active.Action = self.request.query_params.get("Action")
                obj_active.Type = self.request.query_params.get("Type")
                obj_active.SubType = self.request.query_params.get("Subtype")
                obj_active.Update_By1 = (self.request.query_params.get("Create_By"))
                obj_active.Update_By = int(obj_active.Update_By1)
                obj_active.Filter = json.dumps(jsondata.get('Filter'))
                obj_active.Classification = json.dumps(jsondata.get("Classification"))
                obj_active.AddJson = json.dumps(jsondata.get("AddJson"))
                out_message = obj_active.Updatecategory_Isactive()
                out_message = common.outputReturn(out_message, 0)

                if out_message == "SUCCESS":
                    return Response({"MESSAGE": "SUCCESS"})
                else:
                    return Response({"MESSAGE": out_message})
            if self.request.query_params.get("Group") == "subActive_Inactive":
                jsondata = json.loads(request.body.decode('utf-8'))
                obj_active = mMemo.Memo_model()
                obj_active.Action = self.request.query_params.get("Action")
                obj_active.Type = self.request.query_params.get("Type")
                obj_active.SubType = self.request.query_params.get("Subtype")
                obj_active.Update_By1 = (self.request.query_params.get("Create_By"))
                obj_active.Update_By = int(obj_active.Update_By1)
                obj_active.Filter = json.dumps(jsondata.get('Filter'))
                obj_active.Classification = json.dumps(jsondata.get("Classification"))
                obj_active.AddJson = json.dumps(jsondata.get("AddJson"))
                out_message = obj_active.Updatesubcategory_Isactive()
                out_message = common.outputReturn(out_message, 0)

                if out_message == "SUCCESS":
                    return Response({"MESSAGE": "SUCCESS"})
                else:
                    return Response({"MESSAGE": out_message})
            if self.request.query_params.get("Group") == "UpdatesubCategory_Grp":
                jsondata = json.loads(request.body.decode('utf-8'))
                obj_active = mMemo.Memo_model()
                obj_active.Action = self.request.query_params.get("Action")
                obj_active.Type = self.request.query_params.get("Type")
                obj_active.SubType = self.request.query_params.get("Subtype")
                obj_active.Update_By1 = (self.request.query_params.get("Create_By"))
                obj_active.Update_By = int(obj_active.Update_By1)
                obj_active.Filter = json.dumps(jsondata.get('Filter'))
                obj_active.Classification = json.dumps(jsondata.get("Classification"))
                obj_active.AddJson = json.dumps(jsondata.get("AddJson"))
                out_message = obj_active.updatesubCategory_Set()
                out_message = common.outputReturn(out_message, 0)

                if out_message == "SUCCESS":
                    return Response({"MESSAGE": "SUCCESS"})
                else:
                    return Response({"MESSAGE": out_message})
        except Exception as e:
            return Response({"MESSAGE": "ERROR" + str(e), "DATA": str(e)})

class Memo_Master_GetAPI(APIView):
    def post(self, request):
        try:
            if self.request.query_params.get("Group") == "Memocategeory_Grp":
                jsondata = json.loads(request.body.decode('utf-8'))
                obj_prodcat = mMemo.Memo_model()
                obj_prodcat.action = self.request.query_params.get("Action")
                obj_prodcat.type = self.request.query_params.get("Type")
                obj_prodcat.dataw = json.dumps(jsondata.get('Filter'))
                obj_prodcat.create_id = self.request.query_params.get("Create_By")
                obj_prodcat.Entity_Gid = json.dumps(jsondata.get('Classification'))
                obj_prodcat.create_id1 = int(obj_prodcat.create_id)
                out_message = obj_prodcat.Get_Category()
                # out_message = common.outputReturn(out_message,1)
                if out_message.get("MESSAGE") == 'FOUND':
                    ld_dict = {"DATA": json.loads(out_message.get("DATA").to_json(orient='records')),
                               "MESSAGE": 'FOUND'}
                elif out_message.get("MESSAGE") == 'NOT_FOUND':
                    ld_dict = {"MESSAGE": 'NOT_FOUND'}
                else:
                    ld_dict = {"MESSAGE": 'ERROR_OCCURED.' + out_message.get("MESSAGE")}
                return Response(ld_dict)
            if self.request.query_params.get("Group") == "Memosubcategeory_Grp":
                jsondata = json.loads(request.body.decode('utf-8'))
                obj_prodcat = mMemo.Memo_model()
                obj_prodcat.action = self.request.query_params.get("Action")
                obj_prodcat.type = self.request.query_params.get("Type")
                obj_prodcat.dataw = json.dumps(jsondata.get('Filter'))
                obj_prodcat.create_id = self.request.query_params.get("Create_By")
                obj_prodcat.Entity_Gid = json.dumps(jsondata.get('Classification'))
                obj_prodcat.create_id1 = int(obj_prodcat.create_id)
                out_message = obj_prodcat.Get_SubCategory()
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