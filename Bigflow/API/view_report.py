from rest_framework.views import APIView
from rest_framework.response import Response
import json
from Bigflow.API import views as commonview
from Bigflow.Report.Model import mControlSheet,magentsummary
from Bigflow.Core.models import decrpt as decry_data
class Control_Sheet(APIView):
    def post(self,request):
        try:
            if self.request.query_params.get("Group") == "INITIAL_SUMMARY":
                # The First Page Summary Data
                jsondata = json.loads(request.body.decode('utf-8'))
                obj_ctrl = mControlSheet.CtrlModel()
                obj_ctrl.group = self.request.query_params.get("Group")
                obj_ctrl.type = self.request.query_params.get("Type")
                obj_ctrl.sub_type = self.request.query_params.get("SubType")
                obj_ctrl.create_by = decry_data(self.request.query_params.get("Employee_Gid"))
                obj_ctrl.jsonData = json.dumps(jsondata.get('Params').get('FILTER'))
                obj_ctrl.json_classification = jsondata.get('Params').get('CLASSIFICATION')
                obj_ctrl.json_classification['Entity_Gid'] =decry_data( obj_ctrl.json_classification['Entity_Gid'])
                obj_ctrl.json_classification = json.dumps(jsondata.get('Params').get('CLASSIFICATION'))
                ld_out_message = obj_ctrl.get_ctrl_summary()
                if ld_out_message.get("MESSAGE") == 'FOUND':
                    ld_dict = {"DATA": json.loads(ld_out_message.get("DATA").to_json(orient='records')),
                               "MESSAGE": "FOUND"}
                elif ld_out_message.get("MESSAGE") == 'NOT_FOUND':
                    ld_dict = {"MESSAGE": ld_out_message.get("MESSAGE")}
                else:
                    ld_dict = {"MESSAGE": 'ERROR_OCCURED.' + ld_out_message.get("MESSAGE")}

                return Response(ld_dict)
            elif self.request.query_params.get("Group") == "CONTROL_SALES":
                #### Upload the Sale Data and save Excel
                jsondata = json.loads(request.body.decode('utf-8'))
                obj_ctrl = mControlSheet.CtrlModel()
                obj_ctrl.action = self.request.query_params.get("Action")
                obj_ctrl.type = self.request.query_params.get("Type")
                obj_ctrl.sub_type = 'TALLY'
                obj_ctrl.create_by = self.request.query_params.get("Create_by")
                obj_ctrl.jsonData = json.dumps(jsondata.get('Params').get('DETAILS'))
                obj_ctrl.json_classification = jsondata.get('Params').get('CLASSIFICATION')
                obj_ctrl.json_classification['Entity_Gid'] = decry_data(obj_ctrl.json_classification['Entity_Gid'])
                obj_ctrl.json_classification = json.dumps(jsondata.get('Params').get('CLASSIFICATION'))
                ###
                # Here To Save The File In a Directory
                obj_ctrl.json_file = json.dumps(jsondata.get('Params').get('File'))
                lst_saved_filepath = commonview.File_Upload(obj_ctrl.json_file, 'CONTROL_SHEETS',obj_ctrl.create_by)
                obj_ctrl.jsondata = json.dumps(lst_saved_filepath)
                ###
                out_msg = obj_ctrl.set_ctrl_dump()
                if out_msg.get("MESSAGE") == 'SUCCESS':
                    ld_dict = {"MESSAGE": "SUCCESS"}
                elif out_msg.get("MESSAGE") == 'PROCESS_DATA':
                    ld_dict = {"MESSAGE":"SUCCESS","DATA":json.loads(out_msg.get("DATA").to_json(orient='records'))}
                elif out_msg.get("MESSAGE") == 'FAIL':
                    ld_dict = {"MESSAGE": out_msg.get("MESSAGE")}
                else:
                    ld_dict = {"MESSAGE": 'ERROR_OCCURED.' + out_msg.get("DATA")}
                return Response(ld_dict)

            elif self.request.query_params.get("Group") == "CONTROL_OUTSTANDING":
                #### Upload the Outstanding Data and save Excel
                jsondata = json.loads(request.body.decode('utf-8'))
                obj_ctrl = mControlSheet.CtrlModel()
                obj_ctrl.action = self.request.query_params.get("Action")
                obj_ctrl.type = self.request.query_params.get("Type")
                obj_ctrl.sub_type = 'TALLY'
                obj_ctrl.create_by = '1'
                obj_ctrl.jsonData = json.dumps(jsondata.get('Params').get('DETAILS'))
                obj_ctrl.json_classification = jsondata.get('Params').get('CLASSIFICATION')
                obj_ctrl.json_classification['Entity_Gid'] = decry_data(obj_ctrl.json_classification['Entity_Gid'])
                obj_ctrl.json_classification = json.dumps(jsondata.get('Params').get('CLASSIFICATION'))
                ###
                # Here To Save The File In a Directory
                obj_ctrl.json_file = json.dumps(jsondata.get('Params').get('File'))
                lst_saved_filepath = commonview.File_Upload(obj_ctrl.json_file, 'CONTROL_SHEETS',obj_ctrl.create_by)
                obj_ctrl.jsondata = json.dumps(lst_saved_filepath)
                ###
                out_msg = obj_ctrl.set_ctrl_dump()
                if out_msg.get("MESSAGE") == 'SUCCESS':
                    ld_dict = {"MESSAGE": "SUCCESS"}
                elif out_msg.get("MESSAGE") == 'PROCESS_DATA':
                    ld_dict = {"MESSAGE":"SUCCESS","DATA":json.loads(out_msg.get("DATA").to_json(orient='records'))}
                elif out_msg.get("MESSAGE") == 'FAIL':
                    ld_dict = {"MESSAGE": out_msg.get("MESSAGE")}
                else:
                    ld_dict = {"MESSAGE": 'ERROR_OCCURED.' + out_msg.get("DATA")}
                return Response(ld_dict)
            elif self.request.query_params.get("Group") == "CONTROL_STOCK":
                #### Upload the Stock [2 - Godown and Tallly Source] Data and save Excel
                jsondata = json.loads(request.body.decode('utf-8'))
                obj_ctrl = mControlSheet.CtrlModel()
                obj_ctrl.action = self.request.query_params.get("Action")
                obj_ctrl.type = self.request.query_params.get("Type")
                obj_ctrl.sub_type = self.request.query_params.get("SubType")
                obj_ctrl.create_by = self.request.query_params.get("Create_by")
                obj_ctrl.jsonData = json.dumps(jsondata.get('Params').get('DETAILS'))
                obj_ctrl.json_classification = jsondata.get('Params').get('CLASSIFICATION')
                obj_ctrl.json_classification['Entity_Gid'] = decry_data(obj_ctrl.json_classification['Entity_Gid'])
                obj_ctrl.json_classification = json.dumps(jsondata.get('Params').get('CLASSIFICATION'))
                ###
                # Here To Save The File In a Directory
                if obj_ctrl.sub_type == 'TALLY':
                    obj_ctrl.json_file = json.dumps(jsondata.get('Params').get('File'))
                    lst_saved_filepath = commonview.File_Upload(obj_ctrl.json_file, 'CONTROL_SHEETS',obj_ctrl.create_by)
                    obj_ctrl.jsondata = json.dumps(lst_saved_filepath)
                else:
                    obj_ctrl.jsondata = '{}'
                ###
                out_msg = obj_ctrl.set_ctrl_dump()
                if out_msg.get("MESSAGE") == 'SUCCESS':
                    ld_dict = {"MESSAGE": "SUCCESS"}
                elif out_msg.get("MESSAGE") == 'PROCESS_DATA':
                    ld_dict = {"MESSAGE":"SUCCESS","DATA":json.loads(out_msg.get("DATA").to_json(orient='records'))}
                elif out_msg.get("MESSAGE") == 'FAIL':
                    ld_dict = {"MESSAGE": out_msg.get("MESSAGE")}
                else:
                    ld_dict = {"MESSAGE": 'ERROR_OCCURED.' + out_msg.get("DATA")}
                return Response(ld_dict)
            elif self.request.query_params.get("Group") == "SALES_COMPARE":
                ### Compare the Sales Data
                jsondata = json.loads(request.body.decode('utf-8'))
                obj_ctrl = mControlSheet.CtrlModel()
                obj_ctrl.group = self.request.query_params.get("Group")
                obj_ctrl.type = self.request.query_params.get("Type")
                obj_ctrl.sub_type = self.request.query_params.get("SubType")
                obj_ctrl.create_by = self.request.query_params.get("Employee_Gid")
                obj_ctrl.jsonData = json.dumps(jsondata.get('Params').get('FILTER'))
                obj_ctrl.json_classification = jsondata.get('Params').get('CLASSIFICATION')
                obj_ctrl.json_classification['Entity_Gid'] = decry_data(obj_ctrl.json_classification['Entity_Gid'])
                obj_ctrl.json_classification = json.dumps(jsondata.get('Params').get('CLASSIFICATION'))
                ld_out_message = obj_ctrl.get_ctrl_summary()
                if ld_out_message.get("MESSAGE") == 'FOUND':
                    ld_dict = {"DATA": json.loads(ld_out_message.get("DATA").to_json(orient='records')),
                               "MESSAGE": "FOUND"}
                elif ld_out_message.get("MESSAGE") == 'NOT_FOUND':
                    ld_dict = {"MESSAGE": ld_out_message.get("MESSAGE")}
                else:
                    ld_dict = {"MESSAGE": 'ERROR_OCCURED.' + ld_out_message.get("MESSAGE")}

                return Response(ld_dict)
            elif self.request.query_params.get("Group") == "STOCK_COMPARE":
                ### Compare the Sales Data
                jsondata = json.loads(request.body.decode('utf-8'))
                obj_ctrl = mControlSheet.CtrlModel()
                obj_ctrl.group = self.request.query_params.get("Group")
                obj_ctrl.type = self.request.query_params.get("Type")
                obj_ctrl.sub_type = self.request.query_params.get("SubType")
                obj_ctrl.create_by = self.request.query_params.get("Employee_Gid")
                obj_ctrl.jsonData = json.dumps(jsondata.get('Params').get('FILTER'))
                obj_ctrl.json_classification = jsondata.get('Params').get('CLASSIFICATION')
                obj_ctrl.json_classification['Entity_Gid'] = decry_data(obj_ctrl.json_classification['Entity_Gid'])
                obj_ctrl.json_classification = json.dumps(jsondata.get('Params').get('CLASSIFICATION'))
                ld_out_message = obj_ctrl.get_ctrl_summary()
                if ld_out_message.get("MESSAGE") == 'FOUND':
                    ld_dict = {"DATA": json.loads(ld_out_message.get("DATA").to_json(orient='records')),
                               "MESSAGE": "FOUND"}
                elif ld_out_message.get("MESSAGE") == 'NOT_FOUND':
                    ld_dict = {"MESSAGE": ld_out_message.get("MESSAGE")}
                else:
                    ld_dict = {"MESSAGE": 'ERROR_OCCURED.' + ld_out_message.get("MESSAGE")}

                return Response(ld_dict)
            elif self.request.query_params.get("Group") == "OUTSTANDING_COMPARE":
                ### Compare the Sales Data
                jsondata = json.loads(request.body.decode('utf-8'))
                obj_ctrl = mControlSheet.CtrlModel()
                obj_ctrl.group = self.request.query_params.get("Group")
                obj_ctrl.type = self.request.query_params.get("Type")
                obj_ctrl.sub_type = self.request.query_params.get("SubType")
                obj_ctrl.create_by = self.request.query_params.get("Employee_Gid")
                obj_ctrl.jsonData = json.dumps(jsondata.get('Params').get('FILTER'))
                obj_ctrl.json_classification = jsondata.get('Params').get('CLASSIFICATION')
                obj_ctrl.json_classification['Entity_Gid'] = decry_data(obj_ctrl.json_classification['Entity_Gid'])
                obj_ctrl.json_classification = json.dumps(jsondata.get('Params').get('CLASSIFICATION'))
                ld_out_message = obj_ctrl.get_ctrl_summary()
                if ld_out_message.get("MESSAGE") == 'FOUND':
                    ld_dict = {"DATA": json.loads(ld_out_message.get("DATA").to_json(orient='records')),
                               "MESSAGE": "FOUND"}
                elif ld_out_message.get("MESSAGE") == 'NOT_FOUND':
                    ld_dict = {"MESSAGE": ld_out_message.get("MESSAGE")}
                else:
                    ld_dict = {"MESSAGE": 'ERROR_OCCURED.' + ld_out_message.get("MESSAGE")}

                return Response(ld_dict)
        except Exception as e:
            return Response({"MESSAGE":"ERROR_OCCURED","DATA":str(e)})

class PRPO_Query(APIView):
    def post(self,request):
        try:
            if self.request.query_params.get("Group") == "PRPO_QUERY_SUMMARY":
                jsondata = json.loads(request.body.decode('utf-8'))
                obj_query = mPurchase.PurchaseModel()
                obj_query.group = self.request.query_params.get("Group")
                obj_query.type = self.request.query_params.get("Type")
                obj_query.sub_type = self.request.query_params.get("Sub_Type")
                obj_query.filter_json = json.dumps(jsondata.get('Params').get('FILTER'))
                obj_query.json_classification = json.dumps(jsondata.get('Params').get('CLASSIFICATION'))
                ld_out_message = obj_query.get_prpo_query()
                if ld_out_message.get("MESSAGE") == 'FOUND':
                    ld_dict = {"DATA": json.loads(ld_out_message.get("DATA").to_json(orient='records')),
                               "MESSAGE": "FOUND"}
                elif ld_out_message.get("MESSAGE") == 'NOT_FOUND':
                    ld_dict = {"MESSAGE": ld_out_message.get("MESSAGE")}
                else:
                    ld_dict = {"MESSAGE": 'ERROR_OCCURED.' + ld_out_message.get("MESSAGE")}

                return Response(ld_dict)
        except Exception as e:
            return Response({"MESSAGE":"ERROR_OCCURED","DATA":str(e)})

class Agaentsmry(APIView):
    def post(self,request):
        try:
            if(request.method=='POST'):

                object_query = magentsummary.control()
                jsondata = json.loads(request.body.decode('utf-8'))
                object_query.action = self.request.query_params.get("Action")
                object_query.type = self.request.query_params.get("Type")
                object_query.enty = json.dumps(jsondata.get('classification'))
                object_query.main = json.dumps(jsondata.get('Main_data'))
                ld_out_message = object_query.Agentsummary_Get()
                if ld_out_message.get("MESSAGE") == 'FOUND':
                    ld_dict = {"DATA": json.loads(ld_out_message.get("DATA").to_json(orient='records')),
                               "MESSAGE": "FOUND"}
                elif ld_out_message.get("MESSAGE") == 'NOT_FOUND':
                    ld_dict = {"MESSAGE": ld_out_message.get("MESSAGE")}
                else:
                    ld_dict = {"MESSAGE": 'ERROR_OCCURED.' + ld_out_message.get("MESSAGE")}

                return Response(ld_dict)
        except Exception as e:
            return Response({"MESSAGE": "ERROR_OCCURED", "DATA": str(e)})





from Bigflow.Report.Model import mastersyncdata


class MasterSync_Data_(APIView):
 def post(self,request):
        try:
            if self.request.query_params.get("Group") == "Master_Sync":
                jsondata = json.loads(request.body.decode('utf-8'))
                obj = mastersyncdata.MasterSyncData()
                obj.group = self.request.query_params.get("Group")
                obj.action = self.request.query_params.get("Action")
                obj.type = self.request.query_params.get("Type")
                obj.main = json.dumps(jsondata.get("params").get("filter"))
                ld_out_message = obj.masterSync_data()
                if ld_out_message.get("MESSAGE") == 'FOUND':
                        ld_dict = {"DATA": json.loads(ld_out_message.get("DATA").to_json(orient='records')),
                               "MESSAGE": "FOUND"}
                elif ld_out_message.get("MESSAGE") == 'NOT_FOUND':
                    ld_dict = {"MESSAGE": ld_out_message.get("MESSAGE")}
                else:
                    ld_dict = {"MESSAGE": 'ERROR_OCCURED.' + ld_out_message.get("MESSAGE")}
                return Response(ld_dict)

            elif self.request.query_params.get("Group") == "Master_Employee":
                jsondata = json.loads(request.body.decode('utf-8'))
                obj = mastersyncdata.MasterSyncData()
                obj.group = self.request.query_params.get("Group")
                obj.action = self.request.query_params.get("Action")
                obj.type = self.request.query_params.get("Type")
                obj.main = json.dumps(jsondata.get("params").get("jsonData"))
                ld_out_message = obj.masterSync_employee_data()
                if ld_out_message.get("MESSAGE") == 'FOUND':
                    ld_dict = {"DATA": json.loads(ld_out_message.get("DATA").to_json(orient='records')),
                               "MESSAGE": "FOUND"}
                elif ld_out_message.get("MESSAGE") == 'NOT_FOUND':
                    ld_dict = {"MESSAGE": ld_out_message.get("MESSAGE")}
                else:
                    ld_dict = {"MESSAGE": 'ERROR_OCCURED.' + ld_out_message.get("MESSAGE")}
                return Response(ld_dict)


            elif self.request.query_params.get("Group") == "Master_Branch":
                jsondata = json.loads(request.body.decode('utf-8'))
                obj = mastersyncdata.MasterSyncData()
                obj.group = self.request.query_params.get("Group")
                obj.action = self.request.query_params.get("Action")
                obj.type = self.request.query_params.get("Type")
                obj.main = json.dumps(jsondata.get("params").get("jsonData"))
                ld_out_message = obj.masterSync_branch_data()
                if ld_out_message.get("MESSAGE") == 'FOUND':
                    ld_dict = {"DATA": json.loads(ld_out_message.get("DATA").to_json(orient='records')),
                               "MESSAGE": "FOUND"}
                elif ld_out_message.get("MESSAGE") == 'NOT_FOUND':
                    ld_dict = {"MESSAGE": ld_out_message.get("MESSAGE")}
                else:
                    ld_dict = {"MESSAGE": 'ERROR_OCCURED.' + ld_out_message.get("MESSAGE")}
                return Response(ld_dict)


            elif self.request.query_params.get("Group") == "Master_GL":
                jsondata = json.loads(request.body.decode('utf-8'))
                obj = mastersyncdata.MasterSyncData()
                obj.group = self.request.query_params.get("Group")
                obj.action = self.request.query_params.get("Action")
                obj.type = self.request.query_params.get("Type")
                obj.main = json.dumps(jsondata.get("params").get("jsonData"))
                ld_out_message = obj.masterSync_gl_data()
                if ld_out_message.get("MESSAGE") == 'FOUND':
                    ld_dict = {"DATA": json.loads(ld_out_message.get("DATA").to_json(orient='records')),
                               "MESSAGE": "FOUND"}
                elif ld_out_message.get("MESSAGE") == 'NOT_FOUND':
                    ld_dict = {"MESSAGE": ld_out_message.get("MESSAGE")}
                else:
                    ld_dict = {"MESSAGE": 'ERROR_OCCURED.' + ld_out_message.get("MESSAGE")}
                return Response(ld_dict)


        except Exception as e:
            return Response({"MESSAGE": "ERROR_OCCURED", "DATA": str(e)})



class PPR_Data_Get(APIView):
    def post(self, request):
        try:
            if self.request.query_params.get("Group") == "PPR_Data":
                jsondata = json.loads(request.body.decode('utf-8'))
                obj_prodcat = magentsummary.control()
                obj_prodcat.action = self.request.query_params.get("Action")
                obj_prodcat.type = self.request.query_params.get("Type")
                obj_prodcat.jsonData = json.dumps(jsondata.get('Params'))
                obj_prodcat.dataw = json.dumps(
                    {"Entity_Gid": decry_data(json.loads(json.dumps(jsondata.get('Classification')))["Entity_Gid"]),
                     "Create_By": decry_data(json.loads(json.dumps(jsondata.get('Classification')))["Create_By"])})
                out_message = obj_prodcat.sp_PPR_Data_Get_frm_gen()
                if out_message["MESSAGE"] == "FOUND":
                    return Response({"DATA": out_message["DATA"]})
                else:
                    return Response({"MESSAGE": out_message})
        except Exception as e:
            return Response({"MESSAGE": "ERROR", "DATA": str(e)})


class PPR_Data_Set(APIView):
    def post(self, request):
        try:
            if self.request.query_params.get("Group") == "PPR_SET":
                jsondata = json.loads(request.body.decode('utf-8'))
                obj_prodcat = magentsummary.control()
                obj_prodcat.action = self.request.query_params.get("Action")
                # obj_prodcat.type = self.request.query_params.get("Type")
                obj_prodcat.jsonData = json.dumps(jsondata.get('Params'))

                if "Local" in request.query_params:
                    obj_prodcat.dataw = json.dumps(jsondata.get('Classification'))
                else:
                    obj_prodcat.dataw = json.dumps(
                        {"Entity_Gid": decry_data(json.loads(json.dumps(jsondata.get('Classification')))["Entity_Gid"]),
                         "Create_By": decry_data(json.loads(json.dumps(jsondata.get('Classification')))["Create_By"])})
                out_message = obj_prodcat.sp_PPR_Data_Set_frm_gen()
                return Response({"MESSAGE": out_message["MESSAGE"]})
        except Exception as e:
            return Response({"MESSAGE": "ERROR", "DATA": str(e)})


class AllTableValues_Get(APIView):
    def post(self, request):
        try:
            if self.request.query_params.get("Group") == "sector":
                jsondata = json.loads(request.body.decode('utf-8'))
                obj_prodcat = magentsummary.control()
                obj_prodcat.jsonData = json.dumps(jsondata.get('Params'))
                obj_prodcat.entity_gid = jsondata.get('Classification')
                out_message = obj_prodcat.sp_AllTableValues_Get_frm_gen()
                if out_message["MESSAGE"] == "FOUND":
                    return Response({"DATA": out_message["DATA"]})
                else:
                    return Response({"MESSAGE": out_message})

            elif self.request.query_params.get("Group") == "bussinessName":
                jsondata = json.loads(request.body.decode('utf-8'))
                obj_prodcat = magentsummary.control()
                obj_prodcat.action = self.request.query_params.get("Action")
                obj_prodcat.type = self.request.query_params.get("Type")
                obj_prodcat.jsonData = json.dumps(jsondata.get('Params'))
                obj_prodcat.dataw = json.dumps(
                    {"Entity_Gid": decry_data(json.loads(json.dumps(jsondata.get('Classification')))["Entity_Gid"]),
                     "Create_By": decry_data(json.loads(json.dumps(jsondata.get('Classification')))["Create_By"])})
                out_message = obj_prodcat.sp_PPR_Data_Get_frm_gen()
                if out_message["MESSAGE"] == "FOUND":
                    return Response({"DATA": out_message["DATA"]})
                else:
                    return Response({"MESSAGE": out_message})


            elif self.request.query_params.get("Group") == "bussinessGid":
                jsondata = json.loads(request.body.decode('utf-8'))
                obj_prodcat = magentsummary.control()
                obj_prodcat.action = self.request.query_params.get("Action")
                obj_prodcat.type = self.request.query_params.get("Type")
                obj_prodcat.jsonData = json.dumps(jsondata.get('Params'))
                obj_prodcat.dataw = json.dumps(
                    {"Entity_Gid": decry_data(json.loads(json.dumps(jsondata.get('Classification')))["Entity_Gid"]),
                     "Create_By": decry_data(json.loads(json.dumps(jsondata.get('Classification')))["Create_By"])})
                out_message = obj_prodcat.sp_PPR_Data_Get_frm_gen()
                if out_message["MESSAGE"] == "FOUND":
                    return Response({"DATA": out_message["DATA"]})
                else:
                    return Response({"MESSAGE": out_message})

            elif self.request.query_params.get("Group") == "bussinessGidname":
                jsondata = json.loads(request.body.decode('utf-8'))
                obj_prodcat = magentsummary.control()
                obj_prodcat.action = self.request.query_params.get("Action")
                obj_prodcat.type = self.request.query_params.get("Type")
                obj_prodcat.jsonData = json.dumps(jsondata.get('Params'))
                obj_prodcat.dataw = json.dumps(
                    {"Entity_Gid": decry_data(json.loads(json.dumps(jsondata.get('Classification')))["Entity_Gid"]),
                     "Create_By": decry_data(json.loads(json.dumps(jsondata.get('Classification')))["Create_By"])})
                out_message = obj_prodcat.sp_PPR_Data_Get_frm_gen()
                if out_message["MESSAGE"] == "FOUND":
                    return Response({"MESSAGE": out_message})
                else:
                    return Response({"MESSAGE": out_message})

        except Exception as e:
            return Response({"MESSAGE": "ERROR", "DATA": str(e)})

class PPR_Budget_Get(APIView):
    def post(self, request):
        try:
            if self.request.query_params.get("Group") == "PPR_FIND_ALL":
                jsondata = json.loads(request.body.decode('utf-8'))
                obj_prodcat = magentsummary.control()
                obj_prodcat.action = self.request.query_params.get("Action")
                obj_prodcat.type = self.request.query_params.get("Group")
                obj_prodcat.jsonData = json.dumps(jsondata.get('Params'))
                obj_prodcat.dataw = json.dumps(
                    {"Entity_Gid": decry_data(json.loads(json.dumps(jsondata.get('Classification')))["Entity_Gid"]),
                     "Create_By": decry_data(json.loads(json.dumps(jsondata.get('Classification')))["Create_By"])})
                out_message = obj_prodcat.sp_PPR_Budget_Get_frm_gen()
                if out_message["MESSAGE"] == "FOUND":
                    return Response({"DATA": out_message["DATA"]})
                elif out_message["MESSAGE"] == "Error in Data":
                    return Response({"DATA": out_message["DATA"], "MESSAGE": out_message["MESSAGE"]})
                else:
                    return Response({"MESSAGE": out_message})
            elif self.request.query_params.get("Group") == "SUMMARY":
                jsondata = json.loads(request.body.decode('utf-8'))
                obj_prodcat = magentsummary.control()
                obj_prodcat.action = self.request.query_params.get("Action")
                obj_prodcat.type = self.request.query_params.get("Group")
                obj_prodcat.jsonData = json.dumps(jsondata.get('Params'))
                obj_prodcat.dataw = json.dumps(
                    {"Entity_Gid": decry_data(json.loads(json.dumps(jsondata.get('Classification')))["Entity_Gid"]),
                     "Create_By": decry_data(json.loads(json.dumps(jsondata.get('Classification')))["Create_By"])})
                out_message = obj_prodcat.sp_PPR_Budget_Get_frm_gen()
                if out_message["MESSAGE"] == "FOUND":
                    return Response({"DATA": out_message["DATA"]})
                elif out_message["MESSAGE"] == "Error in Data":
                    return Response({"DATA": out_message["DATA"], "MESSAGE": out_message["MESSAGE"]})
                else:
                    return Response({"MESSAGE": out_message})
            elif self.request.query_params.get("Group") == "FinYear_Fetch" or "Sector_Fetch" or "Business_Fetch" or "Bs_Fetch" or "CC_Fetch" or "Expense_grp":
                jsondata = json.loads(request.body.decode('utf-8'))
                obj_prodcat = magentsummary.control()
                obj_prodcat.action = self.request.query_params.get("Action")
                obj_prodcat.type = self.request.query_params.get("Group")
                obj_prodcat.jsonData = json.dumps(jsondata.get('Params'))
                obj_prodcat.dataw = json.dumps(
                    {"Entity_Gid": decry_data(json.loads(json.dumps(jsondata.get('Classification')))["Entity_Gid"]),
                     "Create_By": decry_data(json.loads(json.dumps(jsondata.get('Classification')))["Create_By"])})
                out_message = obj_prodcat.sp_PPR_Budget_Get_frm_gen()
                if out_message["MESSAGE"] == "FOUND":
                    return Response({"DATA": out_message["DATA"]})
                elif out_message["MESSAGE"] == "Error in Data":
                    return Response({"DATA": out_message["DATA"], "MESSAGE": out_message["MESSAGE"]})
                else:
                    return Response({"MESSAGE": out_message})

        except Exception as e:
            return Response({"MESSAGE": "ERROR", "DATA": str(e)})

class PPR_Budget_Set(APIView):
    def post(self, request):
        try:
            if self.request.query_params.get("Group") == "Budget_Insert":
                jsondata = json.loads(request.body.decode('utf-8'))
                obj_prodcat = magentsummary.control()
                obj_prodcat.action = self.request.query_params.get("Action")
                obj_prodcat.jsonData = json.dumps(jsondata.get('Params'))
                obj_prodcat.dataw = json.dumps(
                    {"Entity_Gid": decry_data(json.loads(json.dumps(jsondata.get('Classification')))["Entity_Gid"]),
                     "Create_By": decry_data(json.loads(json.dumps(jsondata.get('Classification')))["Create_By"])})
                out_message = obj_prodcat.sp_PPR_Budget_Set_frm_gen()
                if out_message["MESSAGE"] == "SUCCESS":
                    return Response({"MESSAGE": out_message["MESSAGE"]})
                else:
                    return Response({"MESSAGE": out_message})
        except Exception as e:
            return Response({"MESSAGE": "ERROR", "DATA": str(e)})
