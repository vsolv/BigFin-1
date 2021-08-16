from django.http import JsonResponse, request
from rest_framework.views import APIView
from rest_framework.views import Response
import json
from Bigflow.API import views as commonview
from Bigflow.FA.model import mFA
from Bigflow.Master.Model import mMasters
import Bigflow.Core.models as common
import Bigflow.Core.jwt_file as jwt
ip = common.localip()
import requests

class FAApi(APIView):
    def post(self, request):
        try:
            if self.request.query_params.get("Group") == "FA_ASSERT_MAKER_SUMMARY":
                # Get The Data And Shown in Assert Maker Summary :: Pending Data.
                path = self.request.stream.path
                jsondata = json.loads(request.body.decode('utf-8'))
                obj_fa = mFA.FaModel()
                obj_fa.type = self.request.query_params.get("Type")
                obj_fa.sub_type = self.request.query_params.get("Sub_Type")
                obj_fa.filter_json = json.dumps(jsondata.get('Params').get('FILTER'))
                obj_fa.json_classification = json.dumps(jsondata.get('Params').get('CLASSIFICATION'))
                common.main_fun1(request.read(),path)
                ld_out_message = obj_fa.get_fa_summary()
                if ld_out_message.get("MESSAGE") == 'FOUND':
                    ld_dict = {"DATA": json.loads(ld_out_message.get("DATA").to_json(orient='records')),
                               "MESSAGE": 'FOUND'}
                elif ld_out_message.get("MESSAGE") == 'NOT_FOUND':
                    ld_dict = {"MESSAGE": 'NOT_FOUND'}
                else:
                    ld_dict = {"MESSAGE": 'ERROR_OCCURED.' + ld_out_message.get("MESSAGE")}
                return Response(ld_dict)
            elif self.request.query_params.get("Group") == "FA_INVOICE_DETAILS":
                # Get The Data And Shown in Invoice Details Summary :: Asset Maker.
                path = self.request.stream.path
                jsondata = json.loads(request.body.decode('utf-8'))
                obj_fa = mFA.FaModel()
                obj_fa.type = self.request.query_params.get("Type")
                obj_fa.sub_type = self.request.query_params.get("Sub_Type")
                obj_fa.filter_json = json.dumps(jsondata.get('Params').get('FILTER'))
                obj_fa.json_classification = json.dumps(jsondata.get('Params').get('CLASSIFICATION'))
                common.main_fun1(request.read(), path)
                ld_out_message = obj_fa.get_fa_summary()
                if ld_out_message.get("MESSAGE") == 'FOUND':
                    ld_dict = {"DATA": json.loads(ld_out_message.get("DATA").to_json(orient='records')),
                               "MESSAGE": 'FOUND'}
                elif ld_out_message.get("MESSAGE") == 'NOT_FOUND':
                    ld_dict = {"MESSAGE": 'NOT_FOUND'}
                else:
                    ld_dict = {"MESSAGE": 'ERROR_OCCURED.' + ld_out_message.get("MESSAGE")}
                return Response(ld_dict)
            elif self.request.query_params.get("Group") == "FA_ASSET_CHECKER_SUMMARY":
                # Get The Data And Shown in Asset Checker Summary. - using Group
                path = self.request.stream.path
                jsondata = json.loads(request.body.decode('utf-8'))

                obj_fa = mFA.FaModel()
                obj_fa.type = self.request.query_params.get("Type")
                obj_fa.sub_type = self.request.query_params.get("Sub_Type")
                obj_fa.filter_json = json.dumps(jsondata.get('Params').get('FILTER'))
                obj_fa.json_classification = json.dumps(jsondata.get('Params').get('CLASSIFICATION'))
                common.main_fun1(request.read(), path)
                ld_out_message = obj_fa.get_fa_summary()
                if ld_out_message.get("MESSAGE") == 'FOUND':
                    ld_dict = {"DATA": json.loads(ld_out_message.get("DATA").to_json(orient='records')),
                               "MESSAGE": 'FOUND'}
                elif ld_out_message.get("MESSAGE") == 'NOT_FOUND':
                    ld_dict = {"MESSAGE": 'NOT_FOUND'}
                else:
                    ld_dict = {"MESSAGE": 'ERROR_OCCURED.' + ld_out_message.get("MESSAGE")}
                return Response(ld_dict)
            elif self.request.query_params.get("Group") == "FA_ASSET_TRAN_SUMMARY":
                # Get The Data And Shown in Asset ALL  Summary. -
                path = self.request.stream.path
                jsondata = json.loads(request.body.decode('utf-8'))
                obj_fa = mFA.FaModel()
                obj_fa.type = self.request.query_params.get("Type")
                obj_fa.sub_type = self.request.query_params.get("Sub_Type")
                obj_fa.filter_json = json.dumps(jsondata.get('Params').get('FILTER'))
                obj_fa.json_classification = json.dumps(jsondata.get('Params').get('CLASSIFICATION'))
                common.main_fun1(request.read(), path)
                ld_out_message = obj_fa.get_fa_summary()
                if ld_out_message.get("MESSAGE") == 'FOUND':
                    ld_dict = {"DATA": json.loads(ld_out_message.get("DATA").to_json(orient='records')),
                               "MESSAGE": 'FOUND'}
                elif ld_out_message.get("MESSAGE") == 'NOT_FOUND':
                    ld_dict = {"MESSAGE": 'NOT_FOUND'}
                else:
                    ld_dict = {"MESSAGE": 'ERROR_OCCURED.' + ld_out_message.get("MESSAGE")}
                return Response(ld_dict)
            elif self.request.query_params.get("Group") == "FA_QUERY_SUMMARY":
                # Get The FA Query Data's
                path = self.request.stream.path
                jsondata = json.loads(request.body.decode('utf-8'))

                obj_fq = mFA.FaModel()
                obj_fq.type = self.request.query_params.get("Type")
                obj_fq.sub_type = self.request.query_params.get("Sub_Type")
                obj_fq.filter_json = json.dumps(jsondata.get('Params').get('FILTER'))
                obj_fq.json_classification = json.dumps(jsondata.get('Params').get('CLASSIFICATION'))
                common.main_fun1(request.read(), path)
                ld_out_message = obj_fq.get_fa_query()
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

class FA_Asset_Make(APIView):
    def post(self,request):
        try:
            if self.request.query_params.get("Group") == "FA_ASSET_MAKE":
                path = self.request.stream.path
                jsondata = json.loads(request.body.decode('utf-8'))
                #
                obj_fa = mFA.FaModel()
                obj_fa.action = self.request.query_params.get("Action")
                obj_fa.type = self.request.query_params.get("Type")
                obj_fa.sub_type = self.request.query_params.get("Sub_Type")
                obj_fa.employee_gid = self.request.query_params.get("Employee_Gid")
                obj_fa.jsondata = json.dumps(jsondata.get('Params').get('DETAILS'))
                obj_fa.json_file = json.dumps(jsondata.get('Params').get('File'))
                obj_fa.jsonData = json.dumps(jsondata.get('Params').get('CHANGE'))
                obj_fa.jsonData_sec = json.dumps(jsondata.get('Params').get('STATUS'))
                obj_fa.json_classification = json.dumps(jsondata.get('Params').get('CLASSIFICATION'))
                common.main_fun1(request.read(), path)
                ld_out_message = obj_fa.set_fa_make()
                if ld_out_message.get("MESSAGE") == 'SUCCESS':
                    ld_dict = {"MESSAGE": "SUCCESS"}
                elif ld_out_message.get("MESSAGE") == 'FAIL':
                    ld_dict = {"MESSAGE": "FAIL"}
                else:
                    ld_dict = {"MESSAGE": 'ERROR_OCCURED.' + ld_out_message.get("MESSAGE")}
                return Response(ld_dict)
            elif self.request.query_params.get("Group") == "FA_ASSET_CHECKER":
                path = self.request.stream.path
                jsondata = json.loads(request.body.decode('utf-8'))

                obj_fa = mFA.FaModel()
                obj_fa.action = self.request.query_params.get("Action")
                obj_fa.type = self.request.query_params.get("Type")
                obj_fa.sub_type = self.request.query_params.get("Sub_Type")
                obj_fa.employee_gid = self.request.query_params.get("Employee_Gid")
                obj_fa.jsondata = json.dumps(jsondata.get('Params').get('DETAILS'))
                obj_fa.jsonData = json.dumps(jsondata.get('Params').get('CHANGE'))
                obj_fa.jsonData_sec = json.dumps(jsondata.get('Params').get('STATUS'))
                obj_fa.json_classification = json.dumps(jsondata.get('Params').get('CLASSIFICATION'))
                common.main_fun1(request.read(), path)
                ld_out_message = obj_fa.set_fa_make()
                if ld_out_message.get("MESSAGE") == 'SUCCESS':
                    if jsondata.get('Params').get('STATUS').get('Status') == "APPROVED":
                        # ld_dict = Acounting_entry.ac_entry(self,jsondata)
                        ld_dict = {"MESSAGE": "SUCCESS"}
                    else:
                        ld_dict = {"MESSAGE": "SUCCESS"}
                elif ld_out_message.get("MESSAGE") == 'FAIL':
                    ld_dict = {"MESSAGE": "FAIL"}
                else:
                    ld_dict = {"MESSAGE": 'ERROR_OCCURED.' + ld_out_message.get("MESSAGE")}
                return Response(ld_dict)
        except Exception as e:
            common.logger.error(e)
            return Response({"MESSAGE": "ERROR_OCCURED", "DATA": str(e)})


class FA_Tran(APIView):
    def post(self,request):
        try:
            if self.request.query_params.get("Group") == "FA_ASSET_TRAN":
                path = self.request.stream.path
                jsondata = json.loads(request.body.decode('utf-8'))
                obj_fa = mFA.FaModel()
                obj_fa.action = self.request.query_params.get("Action")
                obj_fa.type = self.request.query_params.get("Type")
                obj_fa.sub_type = self.request.query_params.get("Sub_Type")
                obj_fa.employee_gid = self.request.query_params.get("Employee_Gid")
                obj_fa.jsondata = json.dumps(jsondata.get('Params').get('DETAILS'))
                obj_fa.jsonData = json.dumps(jsondata.get('Params').get('CHANGE'))
                obj_fa.jsonData_sec = json.dumps(jsondata.get('Params').get('STATUS'))
                obj_fa.json_classification = json.dumps(jsondata.get('Params').get('CLASSIFICATION'))
                common.main_fun1(request.read(), path)
                ld_out_message = obj_fa.set_fa_make()
                if ld_out_message.get("MESSAGE") == 'SUCCESS':
                    ld_dict = {"MESSAGE": "SUCCESS"}

                elif ld_out_message.get("MESSAGE") == 'FAIL':
                    ld_dict = {"MESSAGE": "FAIL"}
                else:
                    ld_dict = {"MESSAGE": 'ERROR_OCCURED.' + ld_out_message.get("MESSAGE")}
                return Response(ld_dict)
            elif self.request.query_params.get("Group") == "FA_ASSET_CLEARANCE":
                 ## added Newly - 2020 - FA Cleanace all functions
                path = self.request.stream.path
                jsondata = json.loads(request.body.decode('utf-8'))
                obj_fa = mFA.FaModel()
                obj_fa.action = self.request.query_params.get("Action")
                obj_fa.type = self.request.query_params.get("Type")
                obj_fa.sub_type = self.request.query_params.get("Sub_Type")
                obj_fa.employee_gid = self.request.query_params.get("Employee_Gid")
                obj_fa.jsondata = json.dumps(jsondata.get('Params').get('DETAILS'))
                obj_fa.jsonData = json.dumps(jsondata.get('Params').get('CHANGE'))
                obj_fa.jsonData_sec = json.dumps(jsondata.get('Params').get('STATUS'))
                obj_fa.json_classification = json.dumps(jsondata.get('Params').get('CLASSIFICATION'))
                common.main_fun1(request.read(), path)
                ld_out_message = obj_fa.set_fa_make()
                if ld_out_message.get("MESSAGE") == 'SUCCESS':
                    ld_dict = {"MESSAGE": "SUCCESS"}

                elif ld_out_message.get("MESSAGE") == 'FAIL':
                    ld_dict = {"MESSAGE": "FAIL"}
                else:
                    ld_dict = {"MESSAGE": 'ERROR_OCCURED.' + ld_out_message.get("MESSAGE")}
                return Response(ld_dict)
            elif self.request.query_params.get("Group") == "FA_ASSET_DEPRECIATION":
                path = self.request.stream.path
                jsondata = json.loads(request.body.decode('utf-8'))
                obj_fa = mFA.FaModel()
                obj_fa.action = self.request.query_params.get("Action")
                obj_fa.type = self.request.query_params.get("Type")
                obj_fa.sub_type = self.request.query_params.get("Sub_Type")
                obj_fa.employee_gid = self.request.query_params.get("Employee_Gid")
                obj_fa.jsondata = json.dumps(jsondata.get('Params').get('DEPRECIATION'))
                obj_fa.jsonData = json.dumps(jsondata.get('Params').get('CHANGE'))
                obj_fa.json_classification = json.dumps(jsondata.get('Params').get('CLASSIFICATION'))
                common.main_fun1(request.read(), path)
                ld_out_message = obj_fa.set_fa_depreciation()
                if ld_out_message.get("MESSAGE") == 'SUCCESS':
                    ld_dict = {"MESSAGE": "SUCCESS"}
                elif ld_out_message.get("MESSAGE") == 'FAIL':
                    ld_dict = {"MESSAGE": "FAIL"}
                else:
                    ld_dict = {"MESSAGE": 'ERROR_OCCURED.' + ld_out_message.get("MESSAGE")}
                return Response(ld_dict)
        except Exception as e:
            common.logger.error(e)
            return Response({"MESSAGE": "ERROR_OCCURED", "DATA": str(e)})
class Entity_Details(APIView):
    def post(self,request):
        try:
            if self.request.query_params.get("Group") == "SUMMARY":
                path = self.request.stream.path
                jsondata = json.loads(request.body.decode('utf-8'))
                obj_fa = mFA.FaModel()
                obj_fa.type = self.request.query_params.get("Type")
                obj_fa.sub_type = self.request.query_params.get("Sub_Type")
                obj_fa.filter_json = json.dumps(jsondata.get('params').get('FILTER'))
                obj_fa.json_classification = json.dumps(jsondata.get('params').get('CLASSIFICATION'))
                common.main_fun1(request.read(), path)
                ld_out_message = obj_fa.get_entitybranch()
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



class FA_Location(APIView):
    def post(self,request):
        try:
            if self.request.query_params.get("Group") == "FA_LOCATION_GET":
                path = self.request.stream.path
                jsondata = json.loads(request.body.decode('utf-8'))

                obj_fa = mFA.FaModel()
                obj_fa.type = self.request.query_params.get("Type")
                obj_fa.sub_type = self.request.query_params.get("Sub_Type")
                obj_fa.filter_json = json.dumps(jsondata.get('Params').get('FILTER'))
                obj_fa.json_classification = json.dumps(jsondata.get('Params').get('CLASSIFICATION'))
                common.main_fun1(request.read(), path)
                ld_out_message = obj_fa.get_fa_location()
                if ld_out_message.get("MESSAGE") == 'FOUND':
                    ld_dict = {"DATA": json.loads(ld_out_message.get("DATA").to_json(orient='records')),
                               "MESSAGE": 'FOUND'}
                elif ld_out_message.get("MESSAGE") == 'NOT_FOUND':
                    ld_dict = {"MESSAGE": 'NOT_FOUND'}
                else:
                    ld_dict = {"MESSAGE": 'ERROR_OCCURED.' + ld_out_message.get("MESSAGE")}
                return Response(ld_dict)
            elif self.request.query_params.get("Group") == "FA_LOCATION_SET":
                path = self.request.stream.path
                jsondata = json.loads(request.body.decode('utf-8'))

                obj_fa = mFA.FaModel()
                obj_fa.action = self.request.query_params.get("Action")
                obj_fa.type = self.request.query_params.get("Type")
                obj_fa.sub_type = self.request.query_params.get("Sub_Type")
                obj_fa.employee_gid = self.request.query_params.get("Employee_Gid")
                obj_fa.jsondata = json.dumps(jsondata.get('Params').get('DETAILS'))
                obj_fa.json_classification = json.dumps(jsondata.get('Params').get('CLASSIFICATION'))
                common.main_fun1(request.read(), path)
                ld_out_message = obj_fa.set_fa_location()
                if ld_out_message.get("MESSAGE") == 'SUCCESS':
                    ld_dict = {"MESSAGE": "SUCCESS"}
                elif ld_out_message.get("MESSAGE") == 'FAIL':
                    ld_dict = {"MESSAGE": "FAIL"}
                else:
                    ld_dict = {"MESSAGE": 'ERROR_OCCURED.' + ld_out_message.get("MESSAGE")}
                return Response(ld_dict)
        except Exception as e:
            common.logger.error(e)
            return Response({"MESSAGE": "ERROR_OCCURED", "DATA": str(e)})
class FA_ClearanceLock(APIView):
    def post(self,request):
        try:
            if self.request.query_params.get("Group") == "FA_CLEARANCE_UPDATE":
                path = self.request.stream.path
                jsondata = json.loads(request.body.decode('utf-8'))

                obj_fa = mFA.FaModel()
                obj_fa.action = self.request.query_params.get("Action")
                obj_fa.type = self.request.query_params.get("Type")
                obj_fa.sub_type = self.request.query_params.get("Sub_Type")
                obj_fa.employee_gid = self.request.query_params.get("Employee_Gid")
                obj_fa.jsondata = json.dumps(jsondata.get('Params').get('DETAILS'))
                obj_fa.json_classification = json.dumps(jsondata.get('Params').get('CLASSIFICATION'))
                # common.main_fun1(request.read(), path)
                ld_out_message = obj_fa.set_faclearence_unlock()
                if ld_out_message.get("MESSAGE") == 'SUCCESS':
                    ld_dict = {"MESSAGE": "SUCCESS"}
                elif ld_out_message.get("MESSAGE") == 'FAIL':
                    ld_dict = {"MESSAGE": "FAIL"}
                else:
                    ld_dict = {"MESSAGE": 'ERROR_OCCURED.' + ld_out_message.get("MESSAGE")}
                return Response(ld_dict)
        except Exception as e:
            common.logger.error(e)
            return Response({"MESSAGE": "ERROR_OCCURED", "DATA": str(e)})

class FA_Category(APIView):
    def post(self, request):
        try:
         if self.request.query_params.get("Group") == "FA_CATEGORY_SET":
            path = self.request.stream.path
            jsondata = json.loads(request.body.decode('utf-8'))

            obj_fa = mFA.FaModel()
            obj_fa.action = self.request.query_params.get("Action")
            obj_fa.type = self.request.query_params.get("Type")
            obj_fa.sub_type = self.request.query_params.get("Sub_Type")
            obj_fa.employee_gid = self.request.query_params.get("Employee_Gid")
            obj_fa.jsondata = json.dumps(jsondata.get('Params').get('DETAILS'))
            obj_fa.json_classification = json.dumps(jsondata.get('Params').get('CLASSIFICATION'))
            common.main_fun1(request.read(), path)
            ld_out_message = obj_fa.set_fa_category()
            if ld_out_message.get("MESSAGE") == 'SUCCESS':
                ld_dict = {"MESSAGE": "SUCCESS"}
            elif ld_out_message.get("MESSAGE") == 'FAIL':
                ld_dict = {"MESSAGE": "FAIL"}
            else:
                ld_dict = {"MESSAGE": 'ERROR_OCCURED.' + ld_out_message.get("MESSAGE")}
            return Response(ld_dict)
         elif self.request.query_params.get("Group") == "FA_ASSET_CATEGORY":
            path = self.request.stream.path
            jsondata = json.loads(request.body.decode('utf-8'))

            obj_fa = mFA.FaModel()
            obj_fa.type = self.request.query_params.get("Type")
            obj_fa.sub_type = self.request.query_params.get("Sub_Type")
            obj_fa.filter_json = json.dumps(jsondata.get('Params').get('FILTER'))
            obj_fa.json_classification = json.dumps(jsondata.get('Params').get('CLASSIFICATION'))
            common.main_fun1(request.read(), path)
            ld_out_message = obj_fa.get_fa_category()
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

class FA_Sale(APIView):
    def post(self,request):
        try:
            if self.request.query_params.get("Group") == "FA_CUST":
                path = self.request.stream.path
                jsondata = json.loads(request.body.decode('utf-8'))

                obj_fa = mFA.FaModel()
                obj_fa.action = self.request.query_params.get("Action")
                obj_fa.type = self.request.query_params.get("Type")
                obj_fa.sub_type = self.request.query_params.get("Sub_Type")
                obj_fa.employee_gid = self.request.query_params.get("Employee_Gid")
                obj_fa.jsondata = json.dumps(jsondata.get('Params').get('DETAILS'))
                obj_fa.json_classification = json.dumps(jsondata.get('Params').get('CLASSIFICATION'))
                common.main_fun1(request.read(), path)
                ld_out_message = obj_fa.set_sales()
                if ld_out_message.get("MESSAGE") == 'SUCCESS':
                    ld_dict = {"MESSAGE": "SUCCESS"}
                elif ld_out_message.get("MESSAGE") == 'FAIL':
                    ld_dict = {"MESSAGE": "FAIL"}
                else:
                    ld_dict = {"MESSAGE": 'ERROR_OCCURED.' + ld_out_message.get("MESSAGE")}
                return Response(ld_dict)
            elif self.request.query_params.get("Group") == "FA_CUST_UNIQ":
                path = self.request.stream.path
                jsondata = json.loads(request.body.decode('utf-8'))

                uniq = mMasters.Masters()
                uniq.action = self.request.query_params.get("Action")
                uniq.type = self.request.query_params.get("Type")
                uniq.json_unique = json.dumps(jsondata.get('Params').get('DETAILS'))
                uniq.entity_gid = json.dumps(jsondata.get('Params').get('CLASSIFICATION').get('Entity_Gid'))
                common.main_fun1(request.read(), path)
                uniqu_code = uniq.get_unique()
                ld_dict = {"DATA": json.loads(uniqu_code.get("Final_Code").to_json(orient='records')),
                               "MESSAGE": 'FOUND'}
                return Response(ld_dict)
        except Exception as e:
            common.logger.error(e)
            return Response({"MESSAGE": "ERROR_OCCURED", "DATA": str(e)})

class FA_Depreciation(APIView):
    def post(self, request):
        try:
            if self.request.query_params.get("Group") == "FA_ASSET_DEPRECIATION":
                path = self.request.stream.path
                jsondata = json.loads(request.body.decode('utf-8'))

                obj_fa = mFA.FaModel()
                obj_fa.action = self.request.query_params.get("Action")
                obj_fa.type = self.request.query_params.get("Type")
                obj_fa.sub_type = self.request.query_params.get("Sub_Type")
                obj_fa.employee_gid = self.request.query_params.get("Employee_Gid")
                obj_fa.jsondata = json.dumps(jsondata.get('Params').get('DEPRECIATION'))
                obj_fa.jsonData = json.dumps(jsondata.get('Params').get('CHANGE'))
                obj_fa.json_classification = json.dumps(jsondata.get('Params').get('CLASSIFICATION'))
                common.main_fun1(request.read(), path)
                ld_out_message = obj_fa.set_fa_depreciation()
                if ld_out_message.get("MESSAGE") == 'SUCCESS':
                    ld_dict = {"MESSAGE": "SUCCESS"}
                elif ld_out_message.get("MESSAGE") == 'FAIL':
                    ld_dict = {"MESSAGE": "FAIL"}
                else:
                    ld_dict = {"MESSAGE": 'ERROR_OCCURED.' + ld_out_message.get("MESSAGE")}
                return Response(ld_dict)
            elif self.request.query_params.get("Group") == "FA_ASSET_DEPRECIATION_GET":
                path = self.request.stream.path
                jsondata = json.loads(request.body.decode('utf-8'))

                dep = mFA.FaModel()
                dep.type = self.request.query_params.get("Type")
                dep.sub_type = self.request.query_params.get("Sub_Type")
                dep.filter_json = json.dumps(jsondata.get('Params').get('FILTER'))
                dep.json_classification = json.dumps(jsondata.get('Params').get('CLASSIFICATION'))
                common.main_fun1(request.read(), path)
                common.logger.error([{"FA_Before_Model_sp": 'get_fadepreciation_called'}])
                dep_data = dep.get_fa_depreciation()
                ld_dict = {"DATA": json.loads(dep_data.get("DATA").to_json(orient='records')),
                               "MESSAGE": 'FOUND'}
                common.logger.error([{"FA_After_Model_sp": 'get_fadepreciation_called'}])
                return Response(ld_dict)
        except Exception as e:
            common.logger.error(e)
            return Response({"MESSAGE": "ERROR_OCCURED", "DATA": str(e)})

class FinYear(APIView):
    def post(self, request):
        try:
         if self.request.query_params.get("Group") == "FIN_YEAR_SET":
            path = self.request.stream.path
            jsondata = json.loads(request.body.decode('utf-8'))

            obj_fa = mFA.FaModel()
            obj_fa.action = self.request.query_params.get("Action")
            obj_fa.type = self.request.query_params.get("Type")
            obj_fa.sub_type = self.request.query_params.get("Sub_Type")
            obj_fa.employee_gid = self.request.query_params.get("Employee_Gid")
            obj_fa.jsondata = json.dumps(jsondata.get('Params').get('DETAILS'))
            obj_fa.json_classification = json.dumps(jsondata.get('Params').get('CLASSIFICATION'))
            common.main_fun1(request.read(), path)
            ld_out_message = obj_fa.set_fin_year()
            if ld_out_message.get("MESSAGE") == 'SUCCESS':
                ld_dict = {"MESSAGE": "SUCCESS"}
            elif ld_out_message.get("MESSAGE") == 'FAIL':
                ld_dict = {"MESSAGE": "FAIL"}
            else:
                ld_dict = {"MESSAGE": 'ERROR_OCCURED.' + ld_out_message.get("MESSAGE")}
            return Response(ld_dict)
         elif self.request.query_params.get("Group") == "FIN_YEAR_GET":
            path = self.request.stream.path
            jsondata = json.loads(request.body.decode('utf-8'))

            obj_fa = mFA.FaModel()
            obj_fa.type = self.request.query_params.get("Type")
            obj_fa.sub_type = self.request.query_params.get("Sub_Type")
            obj_fa.filter_json = json.dumps(jsondata.get('Params').get('FILTER'))
            obj_fa.json_classification = json.dumps(jsondata.get('Params').get('CLASSIFICATION'))
            common.main_fun1(request.read(), path)
            ld_out_message = obj_fa.get_fin_year()
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


class Sales_Invoice_Process(object):
    pass


class Theme_CSS(APIView):
    def post(self, request):
        try:
         if self.request.query_params.get("Group") == "THEME_CSS_SET":
            path = self.request.stream.path
            jsondata = json.loads(request.body.decode('utf-8'))

            obj_fa = mFA.FaModel()
            obj_fa.action = self.request.query_params.get("Action")
            obj_fa.type = self.request.query_params.get("Type")
            obj_fa.sub_type = self.request.query_params.get("Sub_Type")
            obj_fa.employee_gid = self.request.query_params.get("Employee_Gid")
            obj_fa.jsondata = json.dumps(jsondata.get('Params').get('DETAILS'))
            common.main_fun1(request.read(), path)
            ld_out_message = obj_fa.set_theme_css()
            if ld_out_message.get("MESSAGE") == 'SUCCESS':
                ld_dict = {"MESSAGE": "SUCCESS"}
            elif ld_out_message.get("MESSAGE") == 'FAIL':
                ld_dict = {"MESSAGE": "FAIL"}
            else:
                ld_dict = {"MESSAGE": 'ERROR_OCCURED.' + ld_out_message.get("MESSAGE")}
            return Response(ld_dict)
         elif self.request.query_params.get("Group") == "THEME_CSS_GET":
            path = self.request.stream.path
            jsondata = json.loads(request.body.decode('utf-8'))

            obj_fa = mFA.FaModel()
            obj_fa.type = self.request.query_params.get("Type")
            obj_fa.sub_type = self.request.query_params.get("Sub_Type")
            obj_fa.filter_json = json.dumps(jsondata.get('Params').get('FILTER'))
            common.main_fun1(request.read(), path)
            ld_out_message = obj_fa.get_theme_css()
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

class GENERATE_Details(APIView):
    def post(self,request):
        try:
            if self.request.query_params.get("Group") == "SUMMARY":
                path = self.request.stream.path
                jsondata = json.loads(request.body.decode('utf-8'))
                obj_fa = mFA.FaModel()
                obj_fa.type = self.request.query_params.get("Type")
                obj_fa.filter_json = json.dumps(jsondata.get('Params').get('FILTER'))
                obj_fa.json_classification = json.dumps(jsondata.get('Params').get('CLASSIFICATION'))
                # common.main_fun1(request.read(), path)
                ld_out_message = obj_fa.get_sale_generate()
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
