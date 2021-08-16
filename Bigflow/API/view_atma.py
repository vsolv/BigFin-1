from rest_framework.views import APIView
from rest_framework.response import Response
import json
import Bigflow.Core.models as common

from Bigflow.ATMA.model import mATMA
from Bigflow.Core.models import decrpt as decry_data



### ATMA
class atmaCatalog_Setapi(APIView):
    def post(self, request):
        try:
            if self.request.query_params.get("Group") == "Catalog Details":
                path = self.request.stream.path
                jsondata = json.loads(request.body.decode('utf-8'))
                obj_prodcat = mATMA.ATMA_model()
                obj_prodcat.action = self.request.query_params.get("Action")
                obj_prodcat.type = self.request.query_params.get("Type")
                obj_prodcat.jsonData = json.dumps(jsondata.get('Params'))
                obj_prodcat.dataw = decrypt_data(jsondata.get('Classification'))
                # common.main_fun1(request.read(), path)
                log_data = [{"ATMA_BEFORE_atmacatalogset_+Catalog Details": jsondata}]
                common.logger.error(log_data)
                out_message = obj_prodcat.atmaSet_Catalog()
                log_data = [{"ATMA_AFTER_atmacatalogset_+Catalog Details": len(out_message)}]
                common.logger.error(log_data)
                if out_message == "SUCCESSFULLY INSERTED":
                    return Response({"MESSAGE": "SUCCESSFULLY INSERTED"})
                else:
                    return Response({"MESSAGE": out_message})

            if self.request.query_params.get("Group") == "Catalog_Details_Update":
                path = self.request.stream.path
                jsondata = json.loads(request.body.decode('utf-8'))
                obj_prodcat = mATMA.ATMA_model()
                obj_prodcat.Group = self.request.query_params.get("Group")
                obj_prodcat.action = self.request.query_params.get("Action")
                obj_prodcat.jsonData = json.dumps(jsondata.get('Params'))
                obj_prodcat.dataw = decrupt_generalData_Update(jsondata.get('Classification'))
                # common.main_fun1(request.read(), path)
                log_data = [{"ATMA_BEFORE_atmacatalogset_+Catalog_Details_Update": jsondata}]
                common.logger.error(log_data)
                out_message = obj_prodcat.update_catalogdetails()
                log_data = [{"ATMA_AFTER_atmacatalogset_+Catalog_Details_Update": len(out_message)}]
                common.logger.error(log_data)
                if out_message[0] == "SUCCESSFULLY UPDATED":
                    return Response({"SUCCESS"})
                else:
                    return Response(out_message)

            if self.request.query_params.get("Group") == "CATALOG_ASSIGN":
                path = self.request.stream.path # not used this in page
                jsondata = json.loads(request.body.decode('utf-8'))
                obj_prodcat = mATMA.ATMA_model()
                obj_prodcat.action = self.request.query_params.get("Action")
                obj_prodcat.type = self.request.query_params.get("Type")
                obj_prodcat.jsonData = json.dumps(jsondata.get('Params'))
                obj_prodcat.dataw = decrypt_data(jsondata.get('Classification'))
                # common.main_fun1(request.read(), path)
                log_data = [{"ATMA_BEFORE_atmacatalogset_+CATALOG_ASSIGN": jsondata}]
                common.logger.error(log_data)
                out_message = obj_prodcat.atmaSet_AssginCatalog()
                log_data = [{"ATMA_AFTER_atmacatalogset_+CATALOG_ASSIGN": len(out_message)}]
                common.logger.error(log_data)
                if out_message == "SUCCESSFULLY INSERTED":
                    return Response({"MESSAGE": "SUCCESSFULLY INSERTED"})
                else:
                    return Response({"MESSAGE": out_message})
        except Exception as e:
            common.logger.error(e)
            return Response({"MESSAGE": "ERROR", "DATA": str(e)})


class atma_main_setapi(APIView):
    def post(self, request):
        try:
            if self.request.query_params.get("Group") == "New_Atma_Api_frm_Memo":
                path = self.request.stream.path
                jsondata = json.loads(request.body.decode('utf-8'))
                obj_prodcat = mATMA.ATMA_model()
                obj_prodcat.action = self.request.query_params.get("Action")
                obj_prodcat.type = self.request.query_params.get("Type")
                obj_prodcat.jsonData = json.dumps(jsondata.get('Params'))
                obj_prodcat.dataw = json.dumps(jsondata.get('Classification'))
                # common.main_fun1(request.read(), path)
                log_data = [{"ATMA_BEFORE_atmacatalogset_+Catalog Details": jsondata}]
                common.logger.error(log_data)
                out_message = obj_prodcat.Set_newAPI_atma_frm_memo()
                log_data = [{"ATMA_AFTER_atmacatalogset_+Catalog Details": len(out_message)}]
                common.logger.error(log_data)
                if out_message == "SUCCESSFULLY INSERTED":
                    return Response({"MESSAGE": "SUCCESSFULLY INSERTED"})
                else:
                    return Response({"MESSAGE": out_message})
        except Exception as e:
            common.logger.error(e)
            return Response({"MESSAGE": "ERROR", "DATA": str(e)})

class atmaCatalog_Getapi(APIView):
   def post(self,request):
       try:
           if self.request.query_params.get("Group") == "Catalog_Details":
               path = self.request.stream.path
               jsondata = json.loads(request.body.decode('utf-8'))
               object_query =  mATMA.ATMA_model()
               object_query.type = self.request.query_params.get("Type")
               # object_query.json_classification = json.dumps(jsondata.get('Params').get('Classification'))
               object_query.json_classification = decrypt_data(jsondata.get('Params').get('Classification'))
               object_query.jsonData = json.dumps(jsondata.get('Params').get('Filter'))
               common.main_fun1(request.read(), path)

               log_data = [{"ATMA_BEFORE_atmacatalog_get_+Catalog_Details": jsondata}]
               common.logger.error(log_data)

               ld_out_message = object_query.atmaget_catalog()

               log_data = [{"ATMA_AFTER_atmacatalog_get_+Catalog_Details": len(ld_out_message)}]
               common.logger.error(log_data)
               if ld_out_message.get("MESSAGE") == 'FOUND':
                   ld_dict = {"DATA": json.loads(ld_out_message.get("DATA").to_json(orient='records')),
                              "MESSAGE": 'FOUND'}
               elif ld_out_message.get("MESSAGE") == 'NOT_FOUND':
                   ld_dict = {"MESSAGE": 'NOT_FOUND'}
               else:
                   ld_dict = {"MESSAGE": 'ERROR_OCCURED.' + ld_out_message.get("MESSAGE")}
               return Response(ld_dict)

           if self.request.query_params.get("Group") == "partner_product":
               path = self.request.stream.path  # not used in app
               jsondata = json.loads(request.body.decode('utf-8'))
               object_query = mATMA.ATMA_model()
               object_query.type = self.request.query_params.get("Type")
               # object_query.json_classification = json.dumps(jsondata.get('Params').get('Classification'))
               object_query.json_classification = decrypt_data(jsondata.get('Params').get('Classification'))
               object_query.jsonData = json.dumps(jsondata.get('Params').get('Filter'))
               common.main_fun1(request.read(), path)
               log_data = [{"ATMA_BEFORE_atmacatalog_get_+partner_product": jsondata}]
               common.logger.error(log_data)
               ld_out_message = object_query.getcatalog_partnerproduct()
               log_data = [{"ATMA_AFTER_atmacatalog_get_+partner_product": len(ld_out_message)}]
               common.logger.error(log_data)
               if ld_out_message.get("MESSAGE") == 'FOUND':
                   ld_dict = {"DATA": json.loads(ld_out_message.get("DATA").to_json(orient='records')),
                              "MESSAGE": 'FOUND'}
               elif ld_out_message.get("MESSAGE") == 'NOT_FOUND':
                   ld_dict = {"MESSAGE": 'NOT_FOUND'}
               else:
                   ld_dict = {"MESSAGE": 'ERROR_OCCURED.' + ld_out_message.get("MESSAGE")}
               return Response(ld_dict)
       except Exception as e:
           common.logger.error(e)
           return Response({"MESSAGE": "ERROR_OCCURED", "DATA": str(e)})

def decrypt_data(lj_data):
    entitiy_gid = decry_data(lj_data['Entity_Gid'])

    if 'Create_By' in lj_data and 'Update_By' in lj_data :
        create_by = decry_data(lj_data['Create_By'])
        update_by = decry_data(lj_data['Update_By'])

        lj_data["Create_By"] =create_by
        lj_data["Update_By"]= update_by
        lj_data["Entity_Gid"]=entitiy_gid

        return json.dumps(lj_data)
    elif 'Create_By' in lj_data and 'Update_By' not in lj_data :
        create_by = decry_data(lj_data['Create_By'])
        lj_data["Create_By"] = create_by
        lj_data["Entity_Gid"] = entitiy_gid
        return json.dumps(lj_data)
    else:
        lj_data["Entity_Gid"] = entitiy_gid
        return json.dumps(lj_data)

def decrupt_generalData(lj_data):
    if 'Entity_Gid' in lj_data:
        entitiy_gid = decry_data(lj_data['Entity_Gid'])
        lj_data["Entity_Gid"] = entitiy_gid

    if 'Create_By' in lj_data:
        create_by = decry_data(lj_data['Create_By'])
        lj_data["Create_By"] =create_by
        return json.dumps(lj_data)
    else:
        lj_data = json.dumps(lj_data)
        return lj_data
    return json.dumps(lj_data)

def decrupt_generalData_Update(lj_data):
    if 'Entity_Gid' in lj_data:
        entitiy_gid = decry_data(lj_data['Entity_Gid'])
        lj_data["Entity_Gid"] = entitiy_gid

    if 'Update_By' in lj_data:
        Update_By = decry_data(lj_data['Update_By'])
        lj_data["Update_By"] =Update_By
        return json.dumps(lj_data)
    else:
        lj_data = json.dumps(lj_data)
        return lj_data
    return json.dumps(lj_data)


class GET_ATMA_Data(APIView):
    def post(self, request):
        try:
            if self.request.query_params.get("Group") == "ATMASUMMARY":
                path = self.request.stream.path
                jsondata = json.loads(request.body.decode('utf-8'))
                obj_atma = mATMA.ATMA_model()
                obj_atma.Group = self.request.query_params.get("Group")
                obj_atma.Action = self.request.query_params.get("Action")
                obj_atma.jsonData = json.dumps(jsondata.get('Params').get('Filter'))
                # obj_atma.json_classification1 = jsondata.get('Params').get('Classification')
                # create_by = decry_data(obj_atma.json_classification1['Create_By'])
                # entitiy_gid = decry_data(obj_atma.json_classification1['Entity_Gid'])
                # obj_atma.json_classification=json.dumps({'Create_By':create_by,'Entity_Gid':entitiy_gid})
                obj_atma.json_classification = decrypt_data(jsondata.get('Params').get('Classification'))
                common.main_fun1(request.read(), path)
                ld_out_message = obj_atma.atma_summary()
                if ld_out_message.get("MESSAGE") == 'FOUND':
                    ld_dict = {"DATA": json.loads(ld_out_message.get("DATA").to_json(orient='records')),
                               "MESSAGE": "FOUND"}
                elif ld_out_message.get("MESSAGE") == 'NOT_FOUND':
                    ld_dict = {"MESSAGE": ld_out_message.get("MESSAGE")}
                else:
                    ld_dict = {"MESSAGE": 'ERROR_OCCURED.' + ld_out_message.get("MESSAGE")}

                return Response(ld_dict)
            if self.request.query_params.get("Group") == "ATMA_APPROVAL_SUMMARY":
                path = self.request.stream.path
                jsondata = json.loads(request.body.decode('utf-8'))
                obj_atma = mATMA.ATMA_model()
                obj_atma.Group = self.request.query_params.get("Group")
                obj_atma.Action = self.request.query_params.get("Action")

                obj_atma.jsonData = json.dumps(jsondata.get('Params').get('Filter'))

                # obj_atma.json_classification1 = jsondata.get('Params').get('Classification')
                # create_by = decry_data(obj_atma.json_classification1['Create_By'])
                # entitiy_gid = decry_data(obj_atma.json_classification1['Entity_Gid'])
                # obj_atma.json_classification=json.dumps({'Create_By':create_by,'Entity_Gid':entitiy_gid})

                entity = decry_data(jsondata.get('Params').get('Classification')['Entity_Gid'])
                logingid = decry_data(jsondata.get('Params').get('Classification')['Login_By'])
                obj_atma.json_classification = json.dumps({'Entity_Gid': entity, 'Login_By': logingid})
                common.main_fun1(request.read(), path)
                ld_out_message = obj_atma.atma_summary()
                if ld_out_message.get("MESSAGE") == 'FOUND':
                    ld_dict = {"DATA": json.loads(ld_out_message.get("DATA").to_json(orient='records')),
                               "MESSAGE": "FOUND"}
                elif ld_out_message.get("MESSAGE") == 'NOT_FOUND':
                    ld_dict = {"MESSAGE": ld_out_message.get("MESSAGE")}
                else:
                    ld_dict = {"MESSAGE": 'ERROR_OCCURED.' + ld_out_message.get("MESSAGE")}

                return Response(ld_dict)
            if self.request.query_params.get("Group") == "QUERYSUMMARY":
                path = self.request.stream.path
                jsondata = json.loads(request.body.decode('utf-8'))
                obj_atma = mATMA.ATMA_model()
                obj_atma.Group = self.request.query_params.get("Group")
                obj_atma.Action = self.request.query_params.get("Action")
                # obj_atma.json_classification = json.dumps(jsondata.get('Params').get('Classification'))
                obj_atma.json_classification = decrypt_data(jsondata.get('Params').get('Classification'))
                obj_atma.jsonData = json.dumps(jsondata.get('Params').get('Filter'))
                common.main_fun1(request.read(), path)
                ld_out_message = obj_atma.query_summary()
                if ld_out_message.get("MESSAGE") == 'FOUND':
                    ld_dict = {"DATA": json.loads(ld_out_message.get("DATA").to_json(orient='records')),
                               "MESSAGE": "FOUND"}
                elif ld_out_message.get("MESSAGE") == 'NOT_FOUND':
                    ld_dict = {"MESSAGE": ld_out_message.get("MESSAGE")}
                else:
                    ld_dict = {"MESSAGE": 'ERROR_OCCURED.' + ld_out_message.get("MESSAGE")}

                return Response(ld_dict)

            if self.request.query_params.get("Group") == "Transaction_Group":
                path = self.request.stream.path
                jsondata = json.loads(request.body.decode('utf-8'))
                obj_atma = mATMA.ATMA_model()
                obj_atma.Group = self.request.query_params.get("Group")
                obj_atma.Action = self.request.query_params.get("Action")
                # obj_atma.json_classification = json.dumps(jsondata.get('Params').get('Classification'))
                obj_atma.json_classification = decrypt_data(jsondata.get('Params').get('Classification'))
                obj_atma.jsonData = json.dumps(jsondata.get('Params').get('Filter'))
                common.main_fun1(request.read(), path)
                ld_out_message = obj_atma.History_Get()
                if ld_out_message.get("MESSAGE") == 'FOUND':
                    ld_dict = {"DATA": json.loads(ld_out_message.get("DATA").to_json(orient='records')),
                               "MESSAGE": "FOUND"}
                elif ld_out_message.get("MESSAGE") == 'NOT_FOUND':
                    ld_dict = {"MESSAGE": ld_out_message.get("MESSAGE")}
                else:
                    ld_dict = {"MESSAGE": 'ERROR_OCCURED.' + ld_out_message.get("MESSAGE")}

                return Response(ld_dict)
            elif self.request.query_params.get("Group") == "ATMAPAYMENTSUMMARY":
                path = self.request.stream.path
                jsondata = json.loads(request.body.decode('utf-8'))
                obj_prodcat = mATMA.ATMA_model()
                obj_prodcat.Group = self.request.query_params.get("Group")
                obj_prodcat.action = self.request.query_params.get("Action")
                obj_prodcat.jsonData = json.dumps(jsondata.get('Params').get('Filter'))
                # obj_prodcat.cls = json.dumps(jsondata.get('Params').get('Classification'))
                obj_prodcat.cls = decrypt_data(jsondata.get('Params').get('Classification'))
                common.main_fun1(request.read(), path)
                ld_out_message = obj_prodcat.atma_paymentsummary()
                if ld_out_message.get("MESSAGE") == 'FOUND':
                    ld_dict = {"DATA": json.loads(ld_out_message.get("DATA").to_json(orient='records')),
                               "MESSAGE": "FOUND"}
                elif ld_out_message.get("MESSAGE") == 'NOT_FOUND':
                    ld_dict = {"MESSAGE": ld_out_message.get("MESSAGE")}
                else:
                    ld_dict = {"MESSAGE": 'ERROR_OCCURED.' + ld_out_message.get("MESSAGE")}

                return Response(ld_dict)
        except Exception as e:
            common.logger.error(e)
            return Response({"MESSAGE": "ERROR_OCCURED"+ str(e), "DATA": str(e)})

class GET_ATMA_Directors_Data(APIView):
    def post(self, request):
        try:
            if self.request.query_params.get("Group") == "ATMASUMMARY":
                path = self.request.stream.path
                jsondata = json.loads(request.body.decode('utf-8'))
                obj_atma = mATMA.ATMA_model()
                obj_atma.Group = self.request.query_params.get("Group")
                obj_atma.Action = self.request.query_params.get("Action")
                obj_atma.json_classification = decrypt_data(jsondata.get('Params').get('Classification'))
                obj_atma.jsonData = json.dumps(jsondata.get('Params').get('Filter'))
                common.main_fun1(request.read(), path)

                log_data = [{"ATMA_BEFORE_atma_getdirectordata": jsondata}]
                common.logger.error(log_data)

                ld_out_message = obj_atma.atmadirector_summary()

                log_data = [{"ATMA_AFTER_atma_getdirectordata": len(ld_out_message)}]
                common.logger.error(log_data)

                if ld_out_message.get("MESSAGE") == 'FOUND':
                    ld_dict = {"DATA": json.loads(ld_out_message.get("DATA").to_json(orient='records')),
                               "MESSAGE": "FOUND"}
                elif ld_out_message.get("MESSAGE") == 'NOT_FOUND':
                    ld_dict = {"MESSAGE": ld_out_message.get("MESSAGE")}
                else:
                    ld_dict = {"MESSAGE": 'ERROR_OCCURED.' + ld_out_message.get("MESSAGE")}

                return Response(ld_dict)

        except Exception as e:
            common.logger.error(e)
            return Response({"MESSAGE": "ERROR_OCCURED"+ str(e), "DATA": str(e)})

class atma_Activitydetails_Set_api(APIView):
   def post(self, request):
       try:
           if self.request.query_params.get("Group") == "Activity_Details":
               path = self.request.stream.path
               jsondata = json.loads(request.body.decode('utf-8'))
               obj_modname = mATMA.ATMA_model()
               obj_modname.action = self.request.query_params.get("Action")
               obj_modname.type = self.request.query_params.get("Type")
               obj_modname.jsonData = json.dumps(jsondata.get('Params'))
               obj_modname.dataw = decrypt_data(jsondata.get('Classification'))
               common.main_fun1(request.read(), path)
               log_data = [{"ATMA_BEFORE_atma_activitydetailsset_+Activity_Details": jsondata}]
               common.logger.error(log_data)
               out_message = obj_modname.Set_Activitydetails()
               log_data = [{"ATMA_AFTER_atma_activitydetailsset_+Activity_Details": len(out_message)}]
               common.logger.error(log_data)
               if out_message[0] == "SUCCESSFULLY INSERTED":
                   return Response({"MESSAGE": "SUCCESSFULLY INSERTED"})
               else:
                   return Response({"MESSAGE": out_message})

           if self.request.query_params.get("Group") == "Activity_Details_Update":
               path = self.request.stream.path
               jsondata = json.loads(request.body.decode('utf-8'))
               obj_prodcat = mATMA.ATMA_model()
               obj_prodcat.Group = self.request.query_params.get("Group")
               obj_prodcat.action = self.request.query_params.get("Action")
               obj_prodcat.jsonData = json.dumps(jsondata.get('Params'))
               dataw = decry_data(jsondata.get('Classification')['Update_By'])
               obj_prodcat.dataw = json.dumps({'Update_By':dataw})
               common.main_fun1(request.read(), path)
               log_data = [{"ATMA_BEFORE_atma_activitydetailsset_+Activity_Details_Update": jsondata}]
               common.logger.error(log_data)
               out_message = obj_prodcat.update_activitydetails()
               log_data = [{"ATMA_AFTER_atma_activitydetailsset_+Activity_Details_Update": len(out_message)}]
               common.logger.error(log_data)
               if out_message[0] == "SUCCESSFULLY UPDATED":
                   return Response({"SUCCESS"})

               else:
                   return Response(out_message)
       except Exception as e:
           common.logger.error(e)
           return Response({"MESSAGE": "ERROR" + str(e), "DATA": str(e)})

class atma_Activitydetails_Get_api(APIView):
   def post(self,request):
       try:
           if self.request.query_params.get("Group") == "Activity_Details":
               path = self.request.stream.path
               jsondata = json.loads(request.body.decode('utf-8'))
               object_query =mATMA.ATMA_model()
               object_query.type = self.request.query_params.get("Type")
               object_query.json_classification = decrypt_data(jsondata.get('Params').get('Classification'))
               object_query.jsonData = json.dumps(jsondata.get('Params').get('Filter'))
               common.main_fun1(request.read(), path)
               log_data = [{"ATMA_BEFORE_atma_activitydetailsget": jsondata}]
               common.logger.error(log_data)
               ld_out_message = object_query.atma_Activitydetails_Get()
               log_data = [{"ATMA_AFTER_atma_activitydetailsget": len(ld_out_message)}]
               common.logger.error(log_data)
               if ld_out_message.get("MESSAGE") == 'FOUND':
                   ld_dict = {"DATA": json.loads(ld_out_message.get("DATA").to_json(orient='records')),
                              "MESSAGE": 'FOUND'}
               elif ld_out_message.get("MESSAGE") == 'NOT_FOUND':
                   ld_dict = {"MESSAGE": 'NOT_FOUND'}
               else:
                   ld_dict = {"MESSAGE": 'ERROR_OCCURED.' + ld_out_message.get("MESSAGE")}
               return Response(ld_dict)
       except Exception as e:
           common.logger.error(e)
           return Response({"MESSAGE": "ERROR_OCCURED"+ str(e), "DATA": str(e)})

class atmaPartnerPayment_Setapi(APIView):
    def post(self, request):
        try:
            if self.request.query_params.get("Group") == "Header Details":
                path = self.request.stream.path
                jsondata = json.loads(request.body.decode('utf-8'))
                obj_prodcat = mATMA.ATMA_model()
                obj_prodcat.action = self.request.query_params.get("Action")
                obj_prodcat.type = self.request.query_params.get("Type")
                obj_prodcat.jsonData = decrupt_generalData(jsondata.get('Params'))
                dataw = json.loads(decrypt_data(jsondata.get('Classification')))
                update = decry_data(jsondata.get('Classification')['Update_By'])
                dataw['Update_By']= update
                obj_prodcat.dataw = json.dumps(dataw)
                common.main_fun1(request.read(), path)

                log_data = [{"ATMA_BEFORE_atmaPartnerPayment_Set_+Header Details": jsondata}]
                common.logger.error(log_data)

                out_message = obj_prodcat.Set_Header()

                log_data = [{"ATMA_AFTER_atmaPartnerPayment_Set_+Header Details": len(out_message)}]
                common.logger.error(log_data)
                out_message1=common.outputReturns(out_message,1)
                out_message2 = common.outputReturns(out_message, 0)
                out_message3 = common.outputReturns(out_message, 2)
                out_message4 = common.outputReturns(out_message, 3)
                if out_message1 == "SUCCESS":
                    return Response({"MESSAGE": "SUCCESS","DATA":out_message2,"RM_GID":out_message3,"p_code":out_message4})

                else:
                    return Response({"MESSAGE": 'NOTE'+" : " + out_message2})

            if self.request.query_params.get("Group") == "MoveToRM":
                path = self.request.stream.path
                jsondata = json.loads(request.body.decode('utf-8'))
                obj_prodcat = mATMA.ATMA_model()
                obj_prodcat.action = self.request.query_params.get("Action")
                obj_prodcat.type = self.request.query_params.get("Type")
                obj_prodcat.jsonData = decrupt_generalData(jsondata.get('Params').get('Filter'))
                obj_prodcat.dataw = decrypt_data(jsondata.get('Params').get('Classification'))
                common.main_fun1(request.read(), path)

                log_data = [{"ATMA_BEFORE_atmaPartnerPayment_Set_+MoveToRM": jsondata}]
                common.logger.error(log_data)
                out_message = obj_prodcat.Set_movetorm()
                log_data = [{"ATMA_AFTER_atmaPartnerPayment_Set_+MoveToRM": len(out_message)}]
                common.logger.error(log_data)

                out_message1=common.outputReturn(out_message,1)
                out_message2 = common.outputReturn(out_message, 0)
                if out_message1 == "SUCCESS":
                    return Response({"MESSAGE": "SUCCESS","DATA":out_message2})

                else:
                    return Response({ out_message1})

            if self.request.query_params.get("Group") == "PAYMODESUMMARY":
                path = self.request.stream.path
                jsondata = json.loads(request.body.decode('utf-8'))
                obj_prodcat = mATMA.ATMA_model()
                obj_prodcat.Group = self.request.query_params.get("Group")
                obj_prodcat.action = self.request.query_params.get("Action")
                obj_prodcat.jsonData = decrupt_generalData(jsondata.get('Params').get('Filter'))
                obj_prodcat.dataw = decrypt_data(jsondata.get('Params').get('Classification'))
                common.main_fun1(request.read(), path)

                log_data = [{"ATMA_BEFORE_atmaPartnerPayment_Set_+PAYMODESUMMARY": jsondata}]
                common.logger.error(log_data)
                out_message = obj_prodcat.set_paymode()
                log_data = [{"ATMA_AFTER_atmaPartnerPayment_Set_+PAYMODESUMMARY": len(out_message)}]
                common.logger.error(log_data)
                if out_message[0] == "SUCCESS":
                    return Response({"SUCCESS"})

                else:
                    return Response(out_message)
            if self.request.query_params.get("Group") == "UPDATEPAYMODESUMMARY":
                path = self.request.stream.path
                jsondata = json.loads(request.body.decode('utf-8'))
                obj_prodcat = mATMA.ATMA_model()
                obj_prodcat.Group = self.request.query_params.get("Group")
                obj_prodcat.action = self.request.query_params.get("Action")
                obj_prodcat.jsonData = decrupt_generalData(jsondata.get('Params').get('Filter'))
                obj_prodcat.dataw = decrypt_data(jsondata.get('Params').get('Classification'))
                common.main_fun1(request.read(), path)

                log_data = [{"ATMA_BEFORE_atmaPartnerPayment_Set_+UPDATEPAYMODESUMMARY": jsondata}]
                common.logger.error(log_data)
                out_message = obj_prodcat.update_paymode()

                log_data = [{"ATMA_AFTER_atmaPartnerPayment_Set_+UPDATEPAYMODESUMMARY": len(out_message)}]
                common.logger.error(log_data)

                if out_message[0] == "SUCCESS":
                    return Response({"SUCCESS"})

                else:
                    return Response(out_message)

        except Exception as e:
            common.logger.error(e)
            return Response({"MESSAGE": 'ERROR_OCCURED' + str(e), "DATA": str(e)})


class atma_AttachmentApi_get(APIView):
   def post(self,request):
       try:
           if self.request.query_params.get("Group") == "Document_Group":
               path = self.request.stream.path #not used in app
               jsondata = json.loads(request.body.decode('utf-8'))
               object_query = mATMA.ATMA_model()
               object_query.type = self.request.query_params.get("Type")
               object_query.json_classification = decrypt_data(jsondata.get('Params').get('Classification'))
               jsonData1=jsondata.get('Params').get('Filter')
               object_query.jsonData = json.dumps(jsonData1)
               common.main_fun1(request.read(), path)
               ld_out_message = object_query.get_AttachmentSummary_model()
               if ld_out_message.get("MESSAGE") == 'FOUND':
                   ld_dict = {"DATA": json.loads(ld_out_message.get("DATA").to_json(orient='records')),
                              "MESSAGE": 'FOUND'}
               elif ld_out_message.get("MESSAGE") == 'NOT_FOUND':
                   ld_dict = {"MESSAGE": 'NOT_FOUND'}
               else:
                   ld_dict = {"MESSAGE": 'ERROR_OCCURED.' + ld_out_message.get("MESSAGE")}
               return Response(ld_dict)
       except Exception as e:
           common.logger.error(e)
           return Response({"MESSAGE": "ERROR_OCCURED"+ str(e), "DATA": str(e)})

class atma_Docgroup_Set(APIView):
   def post(self, request):
       try:
           if self.request.query_params.get("Group") == "Document_Group":
               path = self.request.stream.path
               obj_modname = mATMA.ATMA_model()
               obj_modname.action = self.request.query_params.get("Action")
               obj_modname.type = self.request.query_params.get("Type")
               jsonData1= json.loads(request.body.decode('utf-8'))
               obj_modname.jsonData = decrupt_generalData(jsonData1)
               common.main_fun1(request.read(), path)
               out_message = obj_modname.Set_Docgroup()
               if out_message == "SUCCESSFULLY INSERTED":
                   return Response({"MESSAGE": "SUCCESSFULLY INSERTED"})
               else:
                   return Response({"MESSAGE": out_message})
       except Exception as e:
           common.logger.error(e)
           return Response({"MESSAGE": "ERROR" + str(e), "DATA": str(e)})



class Gettaxdetails(APIView):
    def post(self, request):
        try:
            if self.request.query_params.get("Group") == "GETTAXTYPE":
                path = self.request.stream.path
                jsondata = json.loads(request.body.decode('utf-8'))
                obj_atma = mATMA.ATMA_model()
                obj_atma.Group = self.request.query_params.get("Group")
                obj_atma.Action = self.request.query_params.get("Action")
                obj_atma.emptyjsonone = json.dumps({})
                obj_atma.emptyjsontwo = json.dumps({})
                common.main_fun1(request.read(), path)

                log_data = [{"ATMA_BEFORE_atma_gettaxdetails": jsondata}]
                common.logger.error(log_data)

                ld_out_message = obj_atma.gettaxdetails()

                log_data = [{"ATMA_AFTER_atma_gettaxdetails": len(ld_out_message)}]
                common.logger.error(log_data)
                if ld_out_message.get("MESSAGE") == 'FOUND':
                    ld_dict = {"DATA": json.loads(ld_out_message.get("DATA").to_json(orient='records')),
                               "MESSAGE": "FOUND"}
                elif ld_out_message.get("MESSAGE") == 'NOT_FOUND':
                    ld_dict = {"MESSAGE": ld_out_message.get("MESSAGE")}
                else:
                    ld_dict = {"MESSAGE": 'ERROR_OCCURED.' + ld_out_message.get("MESSAGE")}
                return Response(ld_dict)
            elif self.request.query_params.get(
                    "Group") == "TAXINSERTSUMMARYEXEMPTEDYES" or self.request.query_params.get(
                    "Group") == "TAXINSERTSUMMARYEXEMPTEDNO":
                path = self.request.stream.path
                jsondata = json.loads(request.body.decode('utf-8'))
                obj_atma = mATMA.ATMA_model()
                obj_atma.Group = self.request.query_params.get("Group")
                obj_atma.Action = self.request.query_params.get("Action")
                obj_atma.filterjson = json.loads(request.body.decode('utf-8'))
                # obj_atma.clsjson2 = json.dumps(obj_atma.filterjson[0])
                # obj_atma.clsjson3 = json.dumps(obj_atma.filterjson[1]) ## Ramesh apr 5 2020
                obj_atma.clsjson2 = decrupt_generalData(obj_atma.filterjson[0])
                obj_atma.clsjson3 = decrupt_generalData(obj_atma.filterjson[1])
                common.main_fun1(request.read(), path)

                log_data = [{"ATMA_BEFORE_atma_gettaxdetails": jsondata}]
                common.logger.error(log_data)

                ld_out_message = obj_atma.set_taxdetailsdata()

                log_data = [{"ATMA_AFTER_atma_gettaxdetails": len(ld_out_message)}]
                common.logger.error(log_data)
                if ld_out_message[0] == "SUCCESSFULLY INSERTED":
                    return Response({"MESSAGE": "SUCCESSFULLY INSERTED"})
                else:
                    return Response(ld_out_message)
            elif self.request.query_params.get(
                    "Group") == "TAXINSERTSUMMARYEXEMPTEDUPDATEYES" or self.request.query_params.get(
                    "Group") == "TAXINSERTSUMMARYEXEMPTEDUPDATENO" or self.request.query_params.get(
                    "Group") == "TAXINSERTSUMMARYEXEMPTEDUPDATEYESNOFILE":
                path = self.request.stream.path
                jsondata = json.loads(request.body.decode('utf-8'))
                obj_atma = mATMA.ATMA_model()
                obj_atma.Group = self.request.query_params.get("Group")
                obj_atma.Action = self.request.query_params.get("Action")
                obj_atma.filterjson = json.loads(request.body.decode('utf-8'))
                # obj_atma.clsjson2 = json.dumps(obj_atma.filterjson[0])
                # obj_atma.clsjson3 = json.dumps(obj_atma.filterjson[1])
                obj_atma.clsjson2 = decrupt_generalData(obj_atma.filterjson[0])
                obj_atma.clsjson3 = decrupt_generalData_Update(obj_atma.filterjson[1])
                common.main_fun1(request.read(), path)

                log_data = [{"ATMA_BEFORE_atma_gettaxdetails": jsondata}]
                common.logger.error(log_data)
                ld_out_message = obj_atma.update_taxdetailsdata()
                log_data = [{"ATMA_AFTER_atma_gettaxdetails": len(ld_out_message)}]
                common.logger.error(log_data)

                if ld_out_message[0] == "SUCCESSFULLY UPDATED":
                    return Response({"SUCCESS"})
                else:
                    return Response(ld_out_message)

            if self.request.query_params.get("Group") == "ATMATAXSUMMARY":
                path = self.request.stream.path
                jsondata = json.loads(request.body.decode('utf-8'))
                obj_atma = mATMA.ATMA_model()
                obj_atma.Group = self.request.query_params.get("Group")
                obj_atma.Action = self.request.query_params.get("Action")
                # obj_atma.jsonData = json.dumps(jsondata.get('Params').get('Filter'))
                # obj_atma.cls = json.dumps(jsondata.get('Params').get('Classification'))
                obj_atma.jsonData = decrupt_generalData(jsondata.get('Params').get('Filter'))
                obj_atma.cls = decrypt_data(jsondata.get('Params').get('Classification'))
                common.main_fun1(request.read(), path)
                log_data = [{"ATMA_BEFORE_atma_gettaxdetails+ATMATAXSUMMARY": jsondata}]
                common.logger.error(log_data)
                ld_out_message = obj_atma.get_taxsummary()
                log_data = [{"ATMA_AFTER_atma_gettaxdetails+ATMATAXSUMMARY": len(ld_out_message)}]
                common.logger.error(log_data)
                if ld_out_message.get("MESSAGE") == 'FOUND':
                    ld_dict = {"DATA": json.loads(ld_out_message.get("DATA").to_json(orient='records')),
                               "MESSAGE": "FOUND"}
                elif ld_out_message.get("MESSAGE") == 'NOT_FOUND':
                    ld_dict = {"MESSAGE": ld_out_message.get("MESSAGE")}
                else:
                    ld_dict = {"MESSAGE": 'ERROR_OCCURED.' + ld_out_message.get("MESSAGE")}

                return Response(ld_dict)

        except Exception as e:
            common.logger.error(e)
            return Response({"MESSAGE": "ERROR" + str(e), "DATA": str(e)})

class atma_ProductCatSubCat_getAPI(APIView):
  def post(self,request):
      try:
          if self.request.query_params.get("Group") == "Activity_Group":
              path = self.request.stream.path
              jsondata = json.loads(request.body.decode('utf-8'))
              object_query = mATMA.ATMA_model()
              object_query.type = self.request.query_params.get("Type")
              object_query.json_classification = decrypt_data(jsondata.get('Params').get('Classification'))
              object_query.jsonData = json.dumps(jsondata.get('Params').get('Filter'))
              common.main_fun1(request.read(), path)

              log_data = [{"ATMA_BEFORE_atma_ProductCatSubCat_get": jsondata}]
              common.logger.error(log_data)

              ld_out_message = object_query.atmaget_ProductCatSubCat()

              log_data = [{"ATMA_AFTER_atma_ProductCatSubCat_get": len(ld_out_message)}]
              common.logger.error(log_data)

              if ld_out_message.get("MESSAGE") == 'FOUND':
                  ld_dict = {"DATA": json.loads(ld_out_message.get("DATA").to_json(orient='records')),
                             "MESSAGE": 'FOUND'}
              elif ld_out_message.get("MESSAGE") == 'NOT_FOUND':
                  ld_dict = {"MESSAGE": 'NOT_FOUND'}
              else:
                  ld_dict = {"MESSAGE": 'ERROR_OCCURED.' + ld_out_message.get("MESSAGE")}
              return Response(ld_dict)
      except Exception as e:
          common.logger.error(e)
          return Response({"MESSAGE": "ERROR_OCCURED"+ str(e), "DATA": str(e)})

class atma_Activityget(APIView):
  def post(self,request):
      try:
          if self.request.query_params.get("Group") == "Activity_Group":
              path = self.request.stream.path
              jsondata = json.loads(request.body.decode('utf-8'))
              object_query = mATMA.ATMA_model()
              object_query.type = self.request.query_params.get("Type")
              object_query.json_classification = decrypt_data(jsondata.get('Params').get('Classification'))
              object_query.jsonData = json.dumps(jsondata.get('Params').get('Filter'))
              common.main_fun1(request.read(), path)

              log_data = [{"ATMA_BEFORE_atma_activity_get": jsondata}]
              common.logger.error(log_data)

              ld_out_message = object_query.atmaget_activity()

              log_data = [{"ATMA_AFTER_atma_activity_get": len(ld_out_message)}]
              common.logger.error(log_data)

              if ld_out_message.get("MESSAGE") == 'FOUND':
                  ld_dict = {"DATA": json.loads(ld_out_message.get("DATA").to_json(orient='records')),
                             "MESSAGE": 'FOUND'}
              elif ld_out_message.get("MESSAGE") == 'NOT_FOUND':
                  ld_dict = {"MESSAGE": 'NOT_FOUND'}
              else:
                  ld_dict = {"MESSAGE": 'ERROR_OCCURED.' + ld_out_message.get("MESSAGE")}
              return Response(ld_dict)
      except Exception as e:
          common.logger.error(e)
          return Response({"MESSAGE": "ERROR_OCCURED"+ str(e), "DATA": str(e)})

class atma_ActivitySet_API(APIView):
  def post(self, request):
      try:
          if self.request.query_params.get("Group") == "Activity_ADD":
              path = self.request.stream.path
              jsondata = json.loads(request.body.decode('utf-8'))
              obj_modname =  mATMA.ATMA_model()
              obj_modname.action = self.request.query_params.get("Action")
              obj_modname.type = self.request.query_params.get("Type")
              obj_modname.jsonData = decrupt_generalData(jsondata.get('Params'))
              obj_modname.dataw = decrypt_data(jsondata.get('Classification'))
              common.main_fun1(request.read(), path)

              log_data = [{"ATMA_BEFORE_atma_activityaddedit_+Activity_ADD": jsondata}]
              common.logger.error(log_data)
              out_message = obj_modname.atma_activityadd()
              log_data = [{"ATMA_AFTER_atma_activityaddedit_+Activity_ADD": len(out_message)}]
              common.logger.error(log_data)

              if out_message == "SUCCESS":
                  return Response({"MESSAGE": "SUCCESS"})
              else:
                  return Response({"MESSAGE": out_message})
          if self.request.query_params.get("Group") == "Activity_UPDATE":
              path = self.request.stream.path
              jsondata = json.loads(request.body.decode('utf-8'))
              obj_modname = mATMA.ATMA_model()
              obj_modname.action = self.request.query_params.get("Action")
              obj_modname.type = self.request.query_params.get("Type")
              obj_modname.jsonData = decrupt_generalData(jsondata.get('Params'))
              dataw = decry_data(jsondata.get('Classification')['Update_By'])
              obj_modname.dataw = json.dumps({'Update_By':dataw})
              common.main_fun1(request.read(), path)
              log_data = [{"ATMA_BEFORE_atma_activityaddedit_+Activity_UPDATE": jsondata}]
              common.logger.error(log_data)
              out_message = obj_modname.update_Actgroup()
              log_data = [{"ATMA_AFTER_atma_activityaddedit_+Activity_UPDATE": len(out_message)}]
              common.logger.error(log_data)
              if out_message == "SUCCESSFULLY UPDATED":
                  return Response({"MESSAGE": "SUCCESS"})
              else:
                  return Response({"MESSAGE": out_message})
      except Exception as e:
          common.logger.error(e)
          return Response({"MESSAGE": "ERROR " + str(e), "DATA": str(e)})
class atma_Updateattachment(APIView):
   def post(self,request):
       try:
           if self.request.query_params.get("Group") == "Document_Update" or self.request.query_params.get("Group") == "Document_Updatenofile":
               path = self.request.stream.path
               jsondata = json.loads(request.body.decode('utf-8'))
               obj_atma = mATMA.ATMA_model()
               obj_atma.Group = self.request.query_params.get("Group")
               obj_atma.Action = self.request.query_params.get("Action")
               obj_atma.filterjson = json.loads(request.body.decode('utf-8'))
               filterjson1 = decry_data(obj_atma.filterjson['Update_By'])
               obj_atma.filterjson['Update_By'] =  json.dumps(filterjson1)
               obj_atma.filterjson1 = json.dumps(obj_atma.filterjson)
               common.main_fun1(request.read(), path)
               ld_out_message = obj_atma.atmaupdateattachment()
               return Response(ld_out_message)
       except Exception as e:
           common.logger.error(e)
           return Response({"MESSAGE": "ERROR" + str(e), "DATA": str(e)})
class atma_clientdetails_api(APIView):
    def post(self, request):
        try:
            if self.request.query_params.get("Group") == "ClientDetails_ADD":
                path = self.request.stream.path
                jsondata = json.loads(request.body.decode('utf-8'))
                obj_modname = mATMA.ATMA_model()
                obj_modname.action = self.request.query_params.get("Action")
                obj_modname.type = self.request.query_params.get("Type")
                obj_modname.jsonData = json.dumps(jsondata.get('Params'))
                obj_modname.dataw = decrypt_data(jsondata.get('Classification'))
                common.main_fun1(request.read(), path)

                log_data = [{"ATMA_BEFORE_atma_SetClientdetails_+ClientDetails_ADD": jsondata}]
                common.logger.error(log_data)
                out_message = obj_modname.Set_clientgroup()
                log_data = [{"ATMA_AFTER_atma_SetClientdetails_+ClientDetails_ADD": len(out_message)}]
                common.logger.error(log_data)
                if out_message == "SUCCESSFULLY INSERTED":
                    return Response({"MESSAGE": "SUCCESS"})
                else:
                    return Response({"MESSAGE": out_message})
            if self.request.query_params.get("Group") == "ClientDetails_GET":
                path = self.request.stream.path
                jsondata = json.loads(request.body.decode('utf-8'))
                object_query = mATMA.ATMA_model()
                object_query.action = self.request.query_params.get("Action")
                object_query.type = self.request.query_params.get("Type")
                object_query.json_classification = decrypt_data(jsondata.get('Classification'))
                object_query.jsonData = json.dumps(jsondata.get('Params'))
                common.main_fun1(request.read(), path)
                log_data = [{"ATMA_BEFORE_atma_SetClientdetails_+ClientDetails_GET": jsondata}]
                common.logger.error(log_data)
                ld_out_message = object_query.get_clientgroup()
                log_data = [{"ATMA_AFTER_atma_SetClientdetails_+ClientDetails_GET": len(ld_out_message)}]
                common.logger.error(log_data)
                if ld_out_message.get("MESSAGE") == 'FOUND':
                    ld_dict = {"DATA": json.loads(ld_out_message.get("DATA").to_json(orient='records')),
                               "MESSAGE": 'FOUND'}
                elif ld_out_message.get("MESSAGE") == 'NOT_FOUND':
                    ld_dict = {"MESSAGE": 'NOT_FOUND'}
                else:
                    ld_dict = {"MESSAGE": 'ERROR_OCCURED.' + ld_out_message.get("MESSAGE")}
                return Response(ld_dict)
            if self.request.query_params.get("Group") == "ClientDetails_Update":
                path = self.request.stream.path
                jsondata = json.loads(request.body.decode('utf-8'))
                obj_prodcat = mATMA.ATMA_model()
                obj_prodcat.Group = self.request.query_params.get("Group")
                obj_prodcat.action = self.request.query_params.get("Action")
                obj_prodcat.jsonData = json.dumps(jsondata.get('Params'))
                dataw = decry_data(jsondata.get('Classification')['Update_By'])
                obj_prodcat.dataw = json.dumps({'Update_By':dataw})
                common.main_fun1(request.read(), path)
                log_data = [{"ATMA_BEFORE_atma_SetClientdetails_+ClientDetails_Update": jsondata}]
                common.logger.error(log_data)
                out_message = obj_prodcat.update_clientdetails()
                log_data = [{"ATMA_AFTER_atma_SetClientdetails_+ClientDetails_Update": len(out_message)}]
                common.logger.error(log_data)
                if out_message[0] == "SUCCESSFULLY UPDATED":
                    return Response({"SUCCESS"})

                else:
                    return Response(out_message)
        except Exception as e:
            common.logger.error(e)
            return Response({"MESSAGE": "ERROR" + str(e), "DATA": str(e)})

class atma_contractdetails_api(APIView):
    def post(self, request):
        try:
            if self.request.query_params.get("Group") == "ContractDetails_SET":
                path = self.request.stream.path
                jsondata = json.loads(request.body.decode('utf-8'))
                obj_modname = mATMA.ATMA_model()
                obj_modname.action = self.request.query_params.get("Action")
                obj_modname.type = self.request.query_params.get("Type")
                obj_modname.jsonData = json.dumps(jsondata.get('Params'))
                obj_modname.dataw = decrypt_data(jsondata.get('Classification'))
                common.main_fun1(request.read(), path)
                log_data = [{"ATMA_BEFORE_atma_SetContractdetails_+ContractDetails_SET": jsondata}]
                common.logger.error(log_data)
                out_message = obj_modname.Set_contractgroup()
                log_data = [{"ATMA_AFTER_atma_SetContractdetails_+ContractDetails_SET": len(out_message)}]
                common.logger.error(log_data)
                if out_message[0] == "SUCCESSFULLY INSERTED":
                    return Response({"MESSAGE": "SUCCESS"})
                else:
                    return Response({"MESSAGE": out_message})
            if self.request.query_params.get("Group") == "ContractDetails_GET":
                path = self.request.stream.path
                jsondata = json.loads(request.body.decode('utf-8'))
                object_query = mATMA.ATMA_model()
                object_query.action = self.request.query_params.get("Action")
                object_query.type = self.request.query_params.get("Type")
                object_query.json_classification = decrypt_data(jsondata.get('Classification'))
                object_query.jsonData = json.dumps(jsondata.get('Params'))
                common.main_fun1(request.read(), path)
                log_data = [{"ATMA_BEFORE_atma_SetContractdetails_+ContractDetails_GET": jsondata}]
                common.logger.error(log_data)
                ld_out_message = object_query.get_contractgroup()
                log_data = [{"ATMA_AFTER_atma_SetContractdetails_+ContractDetails_GET": len(ld_out_message)}]
                common.logger.error(log_data)
                if ld_out_message.get("MESSAGE") == 'FOUND':
                    ld_dict = {"DATA": json.loads(ld_out_message.get("DATA").to_json(orient='records')),
                               "MESSAGE": 'FOUND'}
                elif ld_out_message.get("MESSAGE") == 'NOT_FOUND':
                    ld_dict = {"MESSAGE": 'NOT_FOUND'}
                else:
                    ld_dict = {"MESSAGE": 'ERROR_OCCURED.' + ld_out_message.get("MESSAGE")}
                return Response(ld_dict)

            if self.request.query_params.get("Group") == "ContractDetails_Update":
                path = self.request.stream.path
                jsondata = json.loads(request.body.decode('utf-8'))
                obj_prodcat = mATMA.ATMA_model()
                obj_prodcat.Group = self.request.query_params.get("Group")
                obj_prodcat.action = self.request.query_params.get("Action")
                obj_prodcat.jsonData = json.dumps(jsondata.get('Params'))
                dataw = decry_data(jsondata.get('Classification')['Update_By'])
                obj_prodcat.dataw = json.dumps({'Update_By':dataw})
                common.main_fun1(request.read(), path)
                log_data = [{"ATMA_BEFORE_atma_SetContractdetails_+ContractDetails_Update": jsondata}]
                common.logger.error(log_data)
                out_message = obj_prodcat.update_contractdetails()
                log_data = [{"ATMA_AFTER_atma_SetContractdetails_+ContractDetails_Update": len(out_message)}]
                common.logger.error(log_data)
                if out_message[0] == "SUCCESSFULLY UPDATED":
                    return Response({"SUCCESS"})

                else:
                    return Response(out_message)
        except Exception as e:
            common.logger.error(e)
            return Response({"MESSAGE": "ERROR" + str(e), "DATA": str(e)})

class atma_branchdetails_api(APIView):
    def post(self, request):
        try:
            if self.request.query_params.get("Group") == "BranchDetails_Set":
                path = self.request.stream.path
                jsondata = json.loads(request.body.decode('utf-8'))
                obj_modname = mATMA.ATMA_model()
                obj_modname.action = self.request.query_params.get("Action")
                obj_modname.type = self.request.query_params.get("Type")
                obj_modname.jsonData = json.dumps(jsondata.get('Params'))
                obj_modname.dataw = decrypt_data(jsondata.get('Classification'))
                common.main_fun1(request.read(), path)
                log_data = [{"ATMA_BEFORE_atma_SetBranchdetails_+BranchDetails_Set": jsondata}]
                common.logger.error(log_data)
                out_message = obj_modname.Set_branchgroup()
                log_data = [{"ATMA_AFTER_atma_SetBranchdetails_+BranchDetails_Set": len(out_message)}]
                common.logger.error(log_data)
                if out_message[0] == "SUCCESSFULLY INSERTED":
                    return Response({"MESSAGE": "SUCCESS"})
                else:
                    return Response({"MESSAGE": out_message})
            if self.request.query_params.get("Group") == "BranchDetails_GET":
                path = self.request.stream.path
                jsondata = json.loads(request.body.decode('utf-8'))
                object_query = mATMA.ATMA_model()
                object_query.action = self.request.query_params.get("Action")
                object_query.type = self.request.query_params.get("Type")
                object_query.json_classification = decrypt_data(jsondata.get('Classification'))
                object_query.jsonData = json.dumps(jsondata.get('Params'))
                common.main_fun1(request.read(), path)
                log_data = [{"ATMA_BEFORE_atma_SetBranchdetails_+BranchDetails_GET": jsondata}]
                common.logger.error(log_data)
                ld_out_message = object_query.get_branchgroup()
                log_data = [{"ATMA_AFTER_atma_SetBranchdetails_+BranchDetails_GET": len(ld_out_message)}]
                common.logger.error(log_data)
                if ld_out_message.get("MESSAGE") == 'FOUND':
                    ld_dict = {"DATA": json.loads(ld_out_message.get("DATA").to_json(orient='records')),
                               "MESSAGE": 'FOUND'}
                elif ld_out_message.get("MESSAGE") == 'NOT_FOUND':
                    ld_dict = {"MESSAGE": 'NOT_FOUND'}
                else:
                    ld_dict = {"MESSAGE": 'ERROR_OCCURED.' + ld_out_message.get("MESSAGE")}
                return Response(ld_dict)

            if self.request.query_params.get("Group") == "BranchDetails_Update":
                path = self.request.stream.path
                jsondata = json.loads(request.body.decode('utf-8'))
                obj_prodcat = mATMA.ATMA_model()
                obj_prodcat.Group = self.request.query_params.get("Group")
                obj_prodcat.action = self.request.query_params.get("Action")
                obj_prodcat.jsonData = json.dumps(jsondata.get('Params'))
                dataw = decry_data(jsondata.get('Classification')['Update_By'])
                obj_prodcat.dataw = json.dumps({'Update_By':dataw})
                common.main_fun1(request.read(), path)
                log_data = [{"ATMA_BEFORE_atma_SetBranchdetails_+BranchDetails_Update": jsondata}]
                common.logger.error(log_data)
                out_message = obj_prodcat.update_branchdetails()
                log_data = [{"ATMA_AFTER_atma_SetBranchdetails_+BranchDetails_Update": len(out_message)}]
                common.logger.error(log_data)
                if out_message[0] == "SUCCESSFULLY UPDATED":
                    return Response({"SUCCESS"})

                else:
                    return Response(out_message)
        except Exception as e:
            common.logger.error(e)
            return Response({"MESSAGE": "ERROR" + str(e), "DATA": str(e)})


class atma_basicprofiledetails_api(APIView):
    def post(self, request):
        try:
            if self.request.query_params.get("Group") == "BasicProfile_Set":
                path = self.request.stream.path
                jsondata = json.loads(request.body.decode('utf-8'))
                obj_modname = mATMA.ATMA_model()
                obj_modname.action = self.request.query_params.get("Action")
                obj_modname.type = self.request.query_params.get("Type")
                obj_modname.jsonData = json.dumps(jsondata.get('Params'))
                obj_modname.dataw = decrypt_data(jsondata.get('Classification'))
                common.main_fun1(request.read(), path)
                log_data = [{"ATMA_BEFORE_atma_Setbasicprofildedetails_+BasicProfile_Set": jsondata}]
                common.logger.error(log_data)
                out_message = obj_modname.Set_basicprofilegroup()
                log_data = [{"ATMA_AFTER_atma_Setbasicprofildedetails_+BasicProfile_Set": len(out_message)}]
                common.logger.error(log_data)
                if out_message[0] == "SUCCESSFULLY INSERTED":
                    return Response({"MESSAGE": "SUCCESS"})
                else:
                    return Response({"MESSAGE": out_message})
            if self.request.query_params.get("Group") == "Partnerprofile_Get":
                path = self.request.stream.path
                jsondata = json.loads(request.body.decode('utf-8'))
                object_query = mATMA.ATMA_model()
                object_query.action = self.request.query_params.get("Action")
                object_query.type = self.request.query_params.get("Type")
                object_query.json_classification = decrypt_data(jsondata.get('Classification'))
                object_query.jsonData = json.dumps(jsondata.get('Params'))
                common.main_fun1(request.read(), path)
                log_data = [{"ATMA_BEFORE_atma_Setbasicprofildedetails_+Partnerprofile_Get": jsondata}]
                common.logger.error(log_data)
                ld_out_message = object_query.get_basicprofiledetailsgroup()
                log_data = [{"ATMA_AFTER_atma_Setbasicprofildedetails_+BasicProfile_Set": len(ld_out_message)}]
                common.logger.error(log_data)
                if ld_out_message.get("MESSAGE") == 'FOUND':
                    ld_dict = {"DATA": json.loads(ld_out_message.get("DATA").to_json(orient='records')),
                               "MESSAGE": 'FOUND'}
                elif ld_out_message.get("MESSAGE") == 'NOT_FOUND':
                    ld_dict = {"MESSAGE": 'NOT_FOUND'}
                else:
                    ld_dict = {"MESSAGE": 'ERROR_OCCURED.' + ld_out_message.get("MESSAGE")}
                return Response(ld_dict)
        except Exception as e:
            common.logger.error(e)
            return Response({"MESSAGE": "ERROR" + str(e), "DATA": str(e)})

class atma_getcheckerdetails_api(APIView):
    def post(self, request):
        try:
            if self.request.query_params.get("Group") == "Checker_Get":
                path = self.request.stream.path
                jsondata = json.loads(request.body.decode('utf-8'))
                object_query = mATMA.ATMA_model()
                object_query.action = self.request.query_params.get("Action")
                object_query.type = self.request.query_params.get("Type")
                object_query.json_classification = decrypt_data(jsondata.get('Classification'))
                object_query.jsonData = json.dumps(jsondata.get('Params'))
                common.main_fun1(request.read(), path)
                log_data = [{"ATMA_BEFORE_atma_CheckerDetails_+Checker_Get": jsondata}]
                common.logger.error(log_data)
                ld_out_message = object_query.get_checker_detailsgroup()
                log_data = [{"ATMA_AFTER_atma_CheckerDetails_+Checker_Get": len(ld_out_message)}]
                common.logger.error(log_data)
                if ld_out_message.get("MESSAGE") == 'FOUND':
                    ld_dict = {"DATA": json.loads(ld_out_message.get("DATA").to_json(orient='records')),
                               "MESSAGE": 'FOUND'}
                elif ld_out_message.get("MESSAGE") == 'NOT_FOUND':
                    ld_dict = {"MESSAGE": 'NOT_FOUND'}
                else:
                    ld_dict = {"MESSAGE": 'ERROR_OCCURED.' + ld_out_message.get("MESSAGE")}
                return Response(ld_dict)

            if self.request.query_params.get("Group") == "Checker_Status":
                path = self.request.stream.path
                jsondata = json.loads(request.body.decode('utf-8'))
                obj_prodcat = mATMA.ATMA_model()
                obj_prodcat.Group = self.request.query_params.get("Group")
                obj_prodcat.action = self.request.query_params.get("Action")
                obj_prodcat.jsonData = json.dumps(jsondata.get('Params'))
                obj_prodcat.dataw = decrupt_generalData_Update(jsondata.get('Classification'))
                common.main_fun1(request.read(), path)
                log_data = [{"ATMA_BEFORE_atma_CheckerDetails_+Checker_Status": jsondata}]
                common.logger.error(log_data)
                out_message = obj_prodcat.update_productstatusdetails()
                log_data = [{"ATMA_AFTER_atma_CheckerDetails_+Checker_Status": len(out_message)}]
                common.logger.error(log_data)
                if out_message[0] == "SUCCESSFULLY UPDATED":
                    return Response({"SUCCESS"})

                else:
                    return Response(out_message)
        except Exception as e:
            common.logger.error(e)
            return Response({"MESSAGE": "ERROR" + str(e), "DATA": str(e)})

class Prmaker_Set(APIView):
    def post(self, request):
        try:
            if self.request.query_params.get("Group") == "PRMAKER Details":
                path = self.request.stream.path
                jsondata = json.loads(request.body.decode('utf-8'))
                obj_prodcat = mATMA.ATMA_model()
                obj_prodcat.action = self.request.query_params.get("Action")
                obj_prodcat.type = self.request.query_params.get("Type")
                obj_prodcat.jsonData = json.dumps(jsondata.get('Params'))
                obj_prodcat.dataw = decrypt_data(jsondata.get('Classification'))
                common.main_fun1(request.read(), path)
                out_message = obj_prodcat.Set_Prmaker()
                if out_message == "SUCCESSFULLY INSERTED":
                    return Response({"MESSAGE": "SUCCESSFULLY INSERTED"})
                else:
                    return Response({"MESSAGE": out_message})
        except Exception as e:
            common.logger.error(e)
            return Response({"MESSAGE": "ERROR", "DATA": str(e)})

class PRMAKER(APIView):
   def post(self,request):
       try:
           if self.request.query_params.get("Group") == "PRMAKER Details":
               path = self.request.stream.path # not used in app
               jsondata = json.loads(request.body.decode('utf-8'))
               object_query = mATMA.ATMA_model()
               object_query.type = self.request.query_params.get("Type")
               object_query.json_classification = decrypt_data(jsondata.get('Params').get('Classification'))
               object_query.jsonData = json.dumps(jsondata.get('Params').get('Filter'))
               common.main_fun1(request.read(), path)
               ld_out_message = object_query.get_prmaker()
               if ld_out_message.get("MESSAGE") == 'FOUND':
                   ld_dict = {"DATA": json.loads(ld_out_message.get("DATA").to_json(orient='records')),
                              "MESSAGE": 'FOUND'}
               elif ld_out_message.get("MESSAGE") == 'NOT_FOUND':
                   ld_dict = {"MESSAGE": 'NOT_FOUND'}
               else:
                   ld_dict = {"MESSAGE": 'ERROR_OCCURED.' + ld_out_message.get("MESSAGE")}
               return Response(ld_dict)

           if self.request.query_params.get("Group") == "GetProduct_Details":
               path = self.request.stream.path
               jsondata = json.loads(request.body.decode('utf-8'))
               object_query = mATMA.ATMA_model()
               object_query.type = self.request.query_params.get("Action")
               object_query.json_classification = decrypt_data(jsondata.get('Params').get('Classification'))
               object_query.jsonData = json.dumps(jsondata.get('Params').get('Filter'))
               common.main_fun1(request.read(), path)
               ld_out_message = object_query.catalog_getproduct()
               if ld_out_message.get("MESSAGE") == 'FOUND':
                   ld_dict = {"DATA": json.loads(ld_out_message.get("DATA").to_json(orient='records')),
                              "MESSAGE": 'FOUND'}
               elif ld_out_message.get("MESSAGE") == 'NOT_FOUND':
                   ld_dict = {"MESSAGE": 'NOT_FOUND'}
               else:
                   ld_dict = {"MESSAGE": 'ERROR_OCCURED.' + ld_out_message.get("MESSAGE")}
               return Response(ld_dict)
       except Exception as e:
           common.logger.error(e)
           return Response({"MESSAGE": "ERROR_OCCURED", "DATA": str(e)})

class Partnerproductapi_get(APIView):
   def post(self,request):
       try:
           if self.request.query_params.get("Group") == "Partner Product":
               path = self.request.stream.path
               jsondata = json.loads(request.body.decode('utf-8'))
               object_query = mATMA.ATMA_model()
               object_query.type = self.request.query_params.get("Type")
               object_query.json_classification = decrypt_data(jsondata.get('Params').get('Classification'))
               object_query.jsonData = json.dumps(jsondata.get('Params').get('Filter'))
               common.main_fun1(request.read(), path)

               log_data = [{"ATMA_BEFORE_atma_profileproduct_getapi": jsondata}]
               common.logger.error(log_data)
               ld_out_message = object_query.get_profileProduct()
               log_data = [{"ATMA_AFTER_atma_profileproduct_getapi": len(ld_out_message)}]
               common.logger.error(log_data)

               if ld_out_message.get("MESSAGE") == 'FOUND':
                   ld_dict = {"DATA": json.loads(ld_out_message.get("DATA").to_json(orient='records')),
                              "MESSAGE": 'FOUND'}
               elif ld_out_message.get("MESSAGE") == 'NOT_FOUND':
                   ld_dict = {"MESSAGE": 'NOT_FOUND'}
               else:
                   ld_dict = {"MESSAGE": 'ERROR_OCCURED.' + ld_out_message.get("MESSAGE")}
               return Response(ld_dict)
       except Exception as e:
           common.logger.error(e)
           return Response({"MESSAGE": "ERROR_OCCURED", "DATA": str(e)})

class Partnerproductapi_set(APIView):
   def post(self, request):
       try:
           if self.request.query_params.get("Group") == "Partner Product" and self.request.query_params.get("Action") == "Product_Update":
               path = self.request.stream.path
               jsondata = json.loads(request.body.decode('utf-8'))
               obj_modname =  mATMA.ATMA_model()
               obj_modname.action = self.request.query_params.get("Action")
               obj_modname.type = self.request.query_params.get("Type")
               obj_modname.jsonData = json.dumps(jsondata.get('Params'))
               dataw = decry_data(jsondata.get('Classification')['Update_By'])
               obj_modname.dataw = json.dumps({'Update_By':dataw})
               common.main_fun1(request.read(), path)
               log_data = [{"ATMA_BEFORE_atma_profileproduct_setapi": jsondata}]
               common.logger.error(log_data)
               out_message = obj_modname.Set_Partnerproduct()
               log_data = [{"ATMA_AFTER_atma_profileproduct_setapi": len(out_message)}]
               common.logger.error(log_data)
               if out_message[0] == "SUCCESSFULLY INSERTED":
                   return Response({"MESSAGE": "SUCCESSFULLY INSERTED"})
               else:
                   return Response({"MESSAGE": out_message})
           elif self.request.query_params.get("Group") == "Partner Product" and self.request.query_params.get("Action") == "Atma_Product_Insert":
               path = self.request.stream.path
               jsondata = json.loads(request.body.decode('utf-8'))
               obj_modname =  mATMA.ATMA_model()
               obj_modname.action = self.request.query_params.get("Action")
               obj_modname.type = self.request.query_params.get("Type")
               obj_modname.jsonData = json.dumps(jsondata.get('Params'))
               obj_modname.dataw = decrypt_data(jsondata.get('Classification'))
               common.main_fun1(request.read(), path)
               out_message = obj_modname.Set_Partnerproduct()
               if out_message[0] == "SUCCESSFULLY INSERTED":
                   return Response({"MESSAGE": "SUCCESSFULLY INSERTED"})
               else:
                   return Response({"MESSAGE": out_message})
       except Exception as e:
           common.logger.error(e)
           return Response({"MESSAGE": "ERROR", "DATA": str(e)})

class Partnerdeactivateapi_Set(APIView):
   def post(self, request):
       try:
           if self.request.query_params.get("Group") == "Partner Inactive":
               path = self.request.stream.path #not in use
               jsondata = json.loads(request.body.decode('utf-8'))
               obj_modname = mATMA.ATMA_model()
               obj_modname.action = self.request.query_params.get("Action")
               obj_modname.type = self.request.query_params.get("Type")
               obj_modname.jsonData = json.dumps(jsondata.get('Params'))
               obj_modname.dataw = decrypt_data(jsondata.get('Classification'))
               common.main_fun1(request.read(), path)
               out_message = obj_modname.Set_Partnerdeactivate()
               if out_message[0] == "SUCCESSFULLY INSERTED":
                   return Response({"MESSAGE": "SUCCESSFULLY INSERTED"})
               else:
                   return Response({"MESSAGE": out_message})
       except Exception as e:
           common.logger.error(e)
           return Response({"MESSAGE": "ERROR" + str(e), "DATA": str(e)})


class approval_stagesapi(APIView):
    def post(self, request):
        try:
            if self.request.query_params.get("Group") == "RM_To_VMU_Update":
                # path = self.request.stream.path #pending
                jsondata = json.loads(request.body.decode('utf-8'))
                obj_prodcat = mATMA.ATMA_model()
                obj_prodcat.Group = self.request.query_params.get("Group")
                obj_prodcat.action = self.request.query_params.get("Action")
                obj_prodcat.jsonData = json.dumps(jsondata.get('Params'))
                obj_prodcat.dataw = decrypt_data(jsondata.get('Classification'))
                # common.main_fun1(request.read(), path)
                out_message = obj_prodcat.update_aproval_stagesdetails()
                if out_message[0] == "SUCCESSFULLY UPDATED":
                    return Response({"SUCCESS"})

                else:
                    return Response(out_message)
            if self.request.query_params.get("Group") == "APPROVED_GROUP":
                # path = self.request.stream.path #pending
                jsondata = json.loads(request.body.decode('utf-8'))
                obj_prodcat = mATMA.ATMA_model()
                obj_prodcat.Group = self.request.query_params.get("Group")
                obj_prodcat.action = self.request.query_params.get("Action")
                obj_prodcat.jsonData = json.dumps(jsondata.get('Params'))
                obj_prodcat.dataw = decrypt_data(jsondata.get('Classification'))
                # common.main_fun1(request.read(), path)
                out_message = obj_prodcat.update_headaproval_stagesdetails()
                if out_message[0] == "SUCCESSFULLY UPDATED":
                    return Response({"SUCCESS"})

                else:
                    return Response(out_message)
        except Exception as e:
            common.logger.error(e)
            return Response({"MESSAGE": "ERROR" + str(e), "DATA": str(e)})

class Partnerapproval(APIView):
  def post(self,request):
      try:
          if self.request.query_params.get("Group") == "Partner Activate":
              path = self.request.stream.path
              jsondata = json.loads(request.body.decode('utf-8'))
              object_query = mATMA.ATMA_model()
              object_query.type = self.request.query_params.get("Type")
              object_query.json_classification = decrypt_data(jsondata.get('Params').get('Classification'))
              object_query.jsonData = json.dumps(jsondata.get('Params').get('Filter'))
              common.main_fun1(request.read(), path)
              ld_out_message = object_query.get_partapproval()
              if ld_out_message.get("MESSAGE") == 'FOUND':
                  ld_dict = {"DATA": json.loads(ld_out_message.get("DATA").to_json(orient='records')),
                             "MESSAGE": 'FOUND'}
              elif ld_out_message.get("MESSAGE") == 'NOT_FOUND':
                  ld_dict = {"MESSAGE": 'NOT_FOUND'}
              else:
                  ld_dict = {"MESSAGE": 'ERROR_OCCURED.' + ld_out_message.get("MESSAGE")}
              return Response(ld_dict)
      except Exception as e:
          common.logger.error(e)
          return Response({"MESSAGE": "ERROR_OCCURED", "DATA": str(e)})

class Partnerdisapproval(APIView):
  def post(self,request):
      try:
          if self.request.query_params.get("Group") == "Partner Inactivate":
              path = self.request.stream.path
              jsondata = json.loads(request.body.decode('utf-8'))
              object_query = mATMA.ATMA_model()
              object_query.type = self.request.query_params.get("Type")
              object_query.json_classification = decrypt_data(jsondata.get('Params').get('Classification'))
              object_query.jsonData = json.dumps(jsondata.get('Params').get('Filter'))
              common.main_fun1(request.read(), path)
              ld_out_message = object_query.get_partdisapproval()
              if ld_out_message.get("MESSAGE") == 'FOUND':
                  ld_dict = {"DATA": json.loads(ld_out_message.get("DATA").to_json(orient='records')),
                             "MESSAGE": 'FOUND'}
              elif ld_out_message.get("MESSAGE") == 'NOT_FOUND':
                  ld_dict = {"MESSAGE": 'NOT_FOUND'}
              else:
                  ld_dict = {"MESSAGE": 'ERROR_OCCURED.' + ld_out_message.get("MESSAGE")}
              return Response(ld_dict)
      except Exception as e:
          common.logger.error(e)
          return Response({"MESSAGE": "ERROR_OCCURED", "DATA": str(e)})


class approval_paartnergetapi(APIView):
    def post(self, request):
        try:
            if self.request.query_params.get("Group") == "Partner_Approval_Get":
                # path = self.request.stream.path #not in use pending
                jsondata = json.loads(request.body.decode('utf-8'))
                object_query = mATMA.ATMA_model()
                object_query.type = self.request.query_params.get("Type")
                object_query.json_classification = json.dumps(jsondata.get('Params'))
                object_query.jsonData = decrypt_data(jsondata.get('Classification'))
                # common.main_fun1(request.read(), path)

                log_data = [{"ATMA_BEFORE_atma_ApprovedPartner_Get_+Partner_Approval_Get": jsondata}]
                common.logger.error(log_data)

                ld_out_message = object_query.get_approvalpartner()
                log_data = [{"ATMA_AFTER_atma_ApprovedPartner_Get_+Partner_Approval_Get": len(ld_out_message)}]
                common.logger.error(log_data)

                if ld_out_message.get("MESSAGE") == 'FOUND':
                    ld_dict = {"DATA": json.loads(ld_out_message.get("DATA").to_json(orient='records')),
                               "MESSAGE": 'FOUND'}
                elif ld_out_message.get("MESSAGE") == 'NOT_FOUND':
                    ld_dict = {"MESSAGE": 'NOT_FOUND'}
                else:
                    ld_dict = {"MESSAGE": 'ERROR_OCCURED.' + ld_out_message.get("MESSAGE")}
                return Response(ld_dict)

            if self.request.query_params.get("Group") == "Partner_ChangeRequest":
                # path = self.request.stream.path # pending
                jsondata = json.loads(request.body.decode('utf-8'))
                obj_prodcat = mATMA.ATMA_model()
                obj_prodcat.Group = self.request.query_params.get("Group")
                obj_prodcat.action = self.request.query_params.get("Action")
                obj_prodcat.jsonData = json.dumps(jsondata.get('Params'))
                obj_prodcat.dataw = decrypt_data(jsondata.get('Classification'))
                # common.main_fun1(request.read(), path)
                log_data = [{"ATMA_BEFORE_atma_ApprovedPartner_Get_+Partner_ChangeRequest": jsondata}]
                common.logger.error(log_data)
                out_message = obj_prodcat.updateapprovalrequest()
                log_data = [{"ATMA_AFTER_atma_ApprovedPartner_Get_+Partner_ChangeRequest": len(out_message)}]
                common.logger.error(log_data)
                if out_message[0] == "SUCCESS":
                    return Response({"SUCCESS"})

                else:
                    return Response(out_message)

            if self.request.query_params.get("Group") == "APPROVER_TO_REQUEST":
                # path = self.request.stream.path #not in use
                jsondata = json.loads(request.body.decode('utf-8'))
                obj_prodcat = mATMA.ATMA_model()
                obj_prodcat.action = self.request.query_params.get("Action")
                obj_prodcat.type = self.request.query_params.get("Type")
                obj_prodcat.jsonData = json.dumps(jsondata.get('Params').get('Filter'))
                obj_prodcat.dataw = decrypt_data(jsondata.get('Params').get('Classification'))
                # common.main_fun1(request.read(), path)
                log_data = [{"ATMA_BEFORE_atma_ApprovedPartner_Get_+APPROVER_TO_REQUEST": jsondata}]
                common.logger.error(log_data)
                out_message = obj_prodcat.change_request_page()
                log_data = [{"ATMA_AFTER_atma_ApprovedPartner_Get_+APPROVER_TO_REQUEST": len(out_message)}]
                common.logger.error(log_data)
                out_message1 = common.outputReturn(out_message, 1)
                out_message2 = common.outputReturn(out_message, 0)
                if out_message1 == "SUCCESS":
                    return Response({"MESSAGE": "SUCCESS", "DATA": out_message2})

                else:
                    return Response({out_message1})

            if self.request.query_params.get("Group") == "VIEW_TO_CANCEL":
                path = self.request.stream.path
                jsondata = json.loads(request.body.decode('utf-8'))
                obj_prodcat = mATMA.ATMA_model()
                obj_prodcat.action = self.request.query_params.get("Action")
                obj_prodcat.type = self.request.query_params.get("Type")
                obj_prodcat.jsonData = json.dumps(jsondata.get('Params').get('Filter'))
                obj_prodcat.dataw = json.dumps(jsondata.get('Params').get('Classification'))
                common.main_fun1(request.read(), path)
                log_data = [{"ATMA_BEFORE_atma_ApprovedPartner_Get_+VIEW_TO_CANCEL": jsondata}]
                common.logger.error(log_data)
                out_message = obj_prodcat.change_request_page()
                log_data = [{"ATMA_AFTER_atma_ApprovedPartner_Get_+VIEW_TO_CANCEL": len(out_message)}]
                common.logger.error(log_data)
                out_message1 = common.outputReturn(out_message, 1)
                out_message2 = common.outputReturn(out_message, 0)
                if out_message1 == "SUCCESS":
                    return Response({"MESSAGE": "SUCCESS", "DATA": out_message2})

                else:
                    return Response({out_message1})
        except Exception as e:
            common.logger.error(e)
            return Response({"MESSAGE": "ERROR_OCCURED", "DATA": str(e)})

class Update_changerequest_API(APIView):
    def post(self, request):
        try:
            if self.request.query_params.get("Group") == "Activation_Request":
                path = self.request.stream.path
                jsondata = json.loads(request.body.decode('utf-8'))
                obj_prodcat = mATMA.ATMA_model()
                obj_prodcat.Group = self.request.query_params.get("Group")
                obj_prodcat.action = self.request.query_params.get("Action")
                obj_prodcat.jsonData = json.dumps(jsondata.get('Params').get('Filter'))
                obj_prodcat.dataw = decrypt_data(jsondata.get('Params').get('Classification'))
                common.main_fun1(request.read(), path)
                log_data = [{"ATMA_BEFORE_Bankbranch_setdetails_+Activation_Request": jsondata}]
                common.logger.error(log_data)
                out_message = obj_prodcat.activation_request()
                log_data = [{"ATMA_AFTER_Bankbranch_setdetails_+Activation_Request": len(out_message)}]
                common.logger.error(log_data)
                if out_message[0] == "SUCCESSFULLY UPDATED":
                    return Response({"SUCCESS"})

                else:
                    return Response(out_message)
            if self.request.query_params.get("Group") == "BanckBranch_Set":
                path = self.request.stream.path
                jsondata = json.loads(request.body.decode('utf-8'))
                obj_prodcat = mATMA.ATMA_model()
                obj_prodcat.Group = self.request.query_params.get("Group")
                obj_prodcat.action = self.request.query_params.get("Action")
                obj_prodcat.type = self.request.query_params.get("type")
                obj_prodcat.subtype = self.request.query_params.get("subtype")
                obj_prodcat.create_by = decry_data(self.request.query_params.get("Create_by"))
                obj_prodcat.filter_json = json.dumps(jsondata.get('Params').get('Filter'))
                obj_prodcat.json_classification = decrypt_data(jsondata.get('Params').get('Classification'))
                # common.main_fun1(request.read(), path) commented beacuse for core testing team requirement
                log_data = [{"ATMA_BEFORE_Bankbranch_setdetails_+BanckBranch_Set": jsondata}]
                common.logger.error(log_data)
                out_message = obj_prodcat.setbankbranch()
                log_data = [{"ATMA_AFTER_Bankbranch_setdetails_+BanckBranch_Set": len(out_message)}]
                common.logger.error(log_data)
                if out_message[0] == "SUCCESS":
                    return Response({"SUCCESS"})

                else:
                    return Response(out_message)
            if self.request.query_params.get("Group") == "Get_bankbranchdetails":
                # path = self.request.stream.path #not in use
                jsondata = json.loads(request.body.decode('utf-8'))
                object_query = mATMA.ATMA_model()
                object_query.type = self.request.query_params.get("type")
                object_query.action = self.request.query_params.get("Action")
                object_query.json_classification = decrypt_data(jsondata.get('Params').get('Classification'))
                object_query.jsonData = json.dumps(jsondata.get('Params').get('Filter'))
                # common.main_fun1(request.read(), path)
                log_data = [{"ATMA_BEFORE_Bankbranch_setdetails_+Get_bankbranchdetails": jsondata}]
                common.logger.error(log_data)
                ld_out_message = object_query.get_bankbranchdtl()
                log_data = [{"ATMA_AFTER_Bankbranch_setdetails_+Get_bankbranchdetails": len(ld_out_message)}]
                common.logger.error(log_data)
                if ld_out_message.get("MESSAGE") == 'FOUND':
                    ld_dict = {"DATA": json.loads(ld_out_message.get("DATA").to_json(orient='records')),
                               "MESSAGE": 'FOUND'}
                elif ld_out_message.get("MESSAGE") == 'NOT_FOUND':
                    ld_dict = {"MESSAGE": 'NOT_FOUND'}
                else:
                    ld_dict = {"MESSAGE": 'ERROR_OCCURED.' + ld_out_message.get("MESSAGE")}
                return Response(ld_dict)

            if self.request.query_params.get("Group") == "updatebankbranch":
                # path = self.request.stream.path # not in use
                jsondata = json.loads(request.body.decode('utf-8'))
                obj_prodcat = mATMA.ATMA_model()
                obj_prodcat.Group = self.request.query_params.get("Group")
                obj_prodcat.action = self.request.query_params.get("Action")
                obj_prodcat.type = self.request.query_params.get("type")
                obj_prodcat.subtype = self.request.query_params.get("subtype")
                obj_prodcat.create_by = self.request.query_params.get("Create_by")
                obj_prodcat.filter_json = json.dumps(jsondata.get('Params').get('Filter'))
                obj_prodcat.json_classification = decrypt_data(jsondata.get('Params').get('Classification'))
                # common.main_fun1(request.read(), path)
                log_data = [{"ATMA_BEFORE_Bankbranch_setdetails_+updatebankbranch": jsondata}]
                common.logger.error(log_data)
                out_message = obj_prodcat.updatebankbranch()
                log_data = [{"ATMA_AFTER_Bankbranch_setdetails_+updatebankbranch": len(out_message)}]
                common.logger.error(log_data)
                if out_message[0] == "SUCCESS":
                    return Response({"SUCCESS"})

                else:
                    return Response(out_message)

            if self.request.query_params.get("Group") == "updatebranchmaster":
                # path = self.request.stream.path #not in use
                jsondata = json.loads(request.body.decode('utf-8'))
                obj_prodcat = mATMA.ATMA_model()
                obj_prodcat.Group = self.request.query_params.get("Group")
                obj_prodcat.action = self.request.query_params.get("Action")
                obj_prodcat.type = self.request.query_params.get("type")
                obj_prodcat.subtype = self.request.query_params.get("subtype")
                obj_prodcat.create_by = self.request.query_params.get("Create_by")
                obj_prodcat.filter_json = json.dumps(jsondata.get('Params').get('Filter'))
                obj_prodcat.json_classification = decrypt_data(jsondata.get('Params').get('Classification'))
                # common.main_fun1(request.read(), path)
                log_data = [{"ATMA_BEFORE_Bankbranch_setdetails_+updatebranchmaster": jsondata}]
                common.logger.error(log_data)
                out_message = obj_prodcat.updatebranchmaster()
                log_data = [{"ATMA_AFTER_Bankbranch_setdetails_+updatebranchmaster": len(out_message)}]
                common.logger.error(log_data)
                if out_message[0] == "SUCCESS":
                    return Response({"SUCCESS"})

                else:
                    return Response(out_message)

            if self.request.query_params.get("Group") == "Active_Inactive":
                # path = self.request.stream.path #not inuse
                jsondata = json.loads(request.body.decode('utf-8'))
                obj_prodcat = mATMA.ATMA_model()
                obj_prodcat.Group = self.request.query_params.get("Group")
                obj_prodcat.action = self.request.query_params.get("Action")
                obj_prodcat.type = self.request.query_params.get("type")
                obj_prodcat.subtype = self.request.query_params.get("subtype")
                obj_prodcat.create_by = self.request.query_params.get("Create_by")
                obj_prodcat.filter_json = json.dumps(jsondata.get('Params').get('Filter'))
                obj_prodcat.json_classification = decrypt_data(jsondata.get('Params').get('Classification'))
                # common.main_fun1(request.read(), path)
                log_data = [{"ATMA_BEFORE_Bankbranch_setdetails_+Active_Inactive": jsondata}]
                common.logger.error(log_data)
                out_message = obj_prodcat.activebankbranch()
                log_data = [{"ATMA_AFTER_Bankbranch_setdetails_+Active_Inactive": len(out_message)}]
                common.logger.error(log_data)
                if out_message[0] == "SUCCESS":
                    return Response({"SUCCESS"})

                else:
                    return Response(out_message)
            if self.request.query_params.get("Group") == "Get_masterbranchdetails":
                # path = self.request.stream.path # not in use
                jsondata = json.loads(request.body.decode('utf-8'))
                object_query = mATMA.ATMA_model()
                object_query.type = self.request.query_params.get("type")
                object_query.action = self.request.query_params.get("Action")
                object_query.json_classification = decrypt_data(jsondata.get('Params').get('Classification'))
                object_query.jsonData = json.dumps(jsondata.get('Params').get('Filter'))
                # common.main_fun1(request.read(), path)
                log_data = [{"ATMA_BEFORE_Bankbranch_setdetails_+Get_masterbranchdetails": jsondata}]
                common.logger.error(log_data)
                ld_out_message = object_query.get_masterbranchdtl()
                log_data = [{"ATMA_AFTER_Bankbranch_setdetails_+Get_masterbranchdetails": len(ld_out_message)}]
                common.logger.error(log_data)
                if ld_out_message.get("MESSAGE") == 'FOUND':
                    ld_dict = {"DATA": json.loads(ld_out_message.get("DATA").to_json(orient='records')),
                               "MESSAGE": 'FOUND'}
                elif ld_out_message.get("MESSAGE") == 'NOT_FOUND':
                    ld_dict = {"MESSAGE": 'NOT_FOUND'}
                else:
                    ld_dict = {"MESSAGE": 'ERROR_OCCURED.' + ld_out_message.get("MESSAGE")}
                return Response(ld_dict)

        except Exception as e:
            common.logger.error(e)
            return Response({"MESSAGE": "ERROR_OCCURED", "DATA": str(e)})

