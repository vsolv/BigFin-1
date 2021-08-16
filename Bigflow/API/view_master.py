import datetime
import logging
import traceback

from rest_framework.views import APIView
from rest_framework.response import Response
import json
from Bigflow.Master.Model import mMasters
from Bigflow.AP.model import mAP
from Bigflow.Transaction.Model import mFET
from Bigflow.Core.models import decrpt as decry_data
import Bigflow.Core.models as common
from Bigflow.Core.models import MasterRequestObject
from Bigflow.Core.models import get_data_from_id as gdfi
class Product_API(APIView):
    def post(self, request):
        try:
            if self.request.query_params.get("Group") == "PRODUCT_GET":
                obj_product = mFET.FET_model()
                obj_product.type = self.request.query_params.get("Type")
                obj_product.sub_type = self.request.query_params.get("Subtype")
                obj_product.name = ''
                obj_product.limit = '100'

                out_message = obj_product.get_product()
                if len(out_message) > 0:
                    return Response({"MESSAGE": "FOUND", "DATA": json.loads(out_message)})

        except Exception as e:
            return Response({"MESSAGE": "ERROR_OCCURED", "DATA": str(e)})


class Campaign_API(APIView):
    def post(self, request):
        try:
            if self.request.query_params.get("Group") == "CAMPAIGN_GET":
                obj_campaign = mMasters.Masters()
                jsondata = json.loads(request.body.decode('utf-8'))
                obj_campaign.type = self.request.query_params.get("Type")
                obj_campaign.sub_type = self.request.query_params.get("Subtype")
                obj_campaign.jsonData = json.dumps(jsondata.get('Parms').get('Filter'))
                obj_campaign.json_classification = jsondata.get('Parms').get('Classification')

                obj_campaign.json_classification['Entity_Gid'] = [1]
                obj_campaign.json_classification = json.dumps(jsondata.get('Parms').get('Classification'))

                df_outmessage = obj_campaign.get_campaign()

                if df_outmessage.empty == False:
                    json_data = json.loads(df_outmessage.to_json(orient='records'))
                    return Response({"MESSAGE": "FOUND", "DATA": json_data})
                else:
                    return Response({"MESSAGE": "NOT_FOUND"})

        except Exception as e:
            return Response({"MESSAGE": "ERROR_OCCURED", "DATA": str(e)})


class CCBS_MASTER(APIView):
    def post(self, request):
        try:
            if self.request.query_params.get("Group") == "CCBS_MASTER":
                obj_campaign = mMasters.Masters()
                jsondata = json.loads(request.body.decode('utf-8'))
                obj_campaign.type = self.request.query_params.get("Type")
                obj_campaign.sub_type = self.request.query_params.get("Sub_type")
                obj_campaign.jsonData = json.dumps(jsondata.get('Params').get('FILTER'))
                clasification = decry_data(jsondata.get('Params').get('CLASSIFICATION')['Entity_Gid'])
                obj_campaign.json_classification = json.dumps({'Entity_Gid':clasification})
                df_outmessage = obj_campaign.get_CCBS_Master()
                if df_outmessage.empty == False:
                    json_data = json.loads(df_outmessage.to_json(orient='records'))
                    return Response({"MESSAGE": "FOUND", "DATA": json_data})
                else:
                    return Response({"MESSAGE": "NOT_FOUND"})

            if self.request.query_params. get("Group") == "SET_CATEGORY_AND_SUBCATEGORY_MASTER":
                obj_campaign = mMasters.Masters()
                jsondata = json.loads(request.body.decode('utf-8'))
                obj_campaign.type = self.request.query_params.get("Type")
                obj_campaign.sub_type = self.request.query_params.get("Sub_type")
                obj_campaign.jsonData = json.dumps(jsondata.get('Params').get('FILTER'))
                clasifiction = decry_data(jsondata.get('Params').get('CLASSIFICATION')['Entity_Gid'])
                create_by = decry_data(jsondata.get('Params').get('CLASSIFICATION')['Create_by'])
                obj_campaign.json_classification = json.dumps({'Entity_Gid':clasifiction,'Create_by':create_by})
                df_outmessage = obj_campaign.set_cat_subcat_Master()
                # print(df_outmessage[0])
                if df_outmessage[0] == "SUCCESS":
                    print(self.request.query_params.get("Sub_type"), self.request.query_params.get("Type"))
                    if (self.request.query_params.get("Sub_type") == 'add_bs' and self.request.query_params.get("Type") == 'INSERT'):
                        data = jsondata['Params']
                        data = data['FILTER']
                        #print(data, type(data))
                        data = {"code":data['tbs_code'],"no": str(data['tbs_no']), "name": data['tbs_name'], "remarks": data['tbs_remarks'],
                                "description": data['tbs_remarks'],'Entity_Gid': jsondata.get('Params').get('CLASSIFICATION')['Entity_Gid'],'create_by':jsondata.get('Params').get('CLASSIFICATION')['Create_by']}
                        #print(data)
                        mrobject = MasterRequestObject('BS', data, 'POST')
                    elif (self.request.query_params.get("Sub_type") == 'add_cc' and self.request.query_params.get(
                            "Type") == 'INSERT'):
                        data = jsondata['Params']
                        data = data['FILTER']
                        #print(data, type(data))
                        data = {"code":data['tcc_code'],"no": str(data['tcc_no']), "name": data['tcc_name'], "remarks": data['tcc_remarks'],
                                "description": data['tcc_remarks'],'Entity_Gid':jsondata.get('Params').get('CLASSIFICATION')['Entity_Gid'],'create_by':jsondata.get('Params').get('CLASSIFICATION')['Create_by']}
                        #print(data)
                        mrobject = MasterRequestObject('CC', data, 'POST')

                    elif (self.request.query_params.get("Sub_type") == 'add_category' and self.request.query_params.get("Type") == 'INSERT'):
                        try:
                            datas = jsondata['Params']
                            datas = datas['FILTER']
                            print(datas)
                            if(datas['category_isasset']=='Y'):
                                datas['category_isasset']=1
                            else:
                                datas['category_isasset'] = 0
                            datas = {"code":datas['category_code'],"no": datas['category_no'], "name": datas['category_name'],
                                    "glno": datas['category_glno'], "isasset": datas['category_isasset'],
                                    "isodit": datas['category_isodit'],"Entity_Gid":jsondata.get('Params').get('CLASSIFICATION')['Entity_Gid'],"create_by":jsondata.get('Params').get('CLASSIFICATION')['Create_by']}
                            #print(datas)
                            mrobject = MasterRequestObject('CATEGORY', datas, 'post')
                        except:
                            #traceback.print_exc()
                            pass
                    elif(self.request.query_params.get("Sub_type") == 'add_subcategory' and self.request.query_params.get("Type") == 'INSERT'):
                            datas = jsondata['Params']['FILTER']
                            # print(datas)
                            try:
                                if (datas['blocked_status'] == 'N'):
                                    datas['blocked_status'] = 0
                                else:
                                    datas['blocked_status'] = 1
                                if (datas['rcm_status'] == 'N'):
                                    datas['rcm_status'] = 0
                                else:
                                    datas['rcm_status'] = 1
                                asst_code=None
                                try:
                                    asst_code=int(datas['subcategory_asst_code'])
                                except:
                                    pass

                                data = {"no": datas['subcategory_no'], "name": datas['subcategory_name'],
                                        "category_id": datas['subcategory_categorygid'][0],
                                        "gstrcm": datas['rcm_status'],
                                        "glno": int(datas['subcategory_glno']),
                                        "expense_id": str(datas['expense_gid']),
                                        "gstblocked": 1,"Entity_Gid":jsondata.get('Params').get('CLASSIFICATION')['Entity_Gid'],"create_by":jsondata.get('Params').get('CLASSIFICATION')['Create_by']}
                                if(asst_code!=None):
                                    data["assetcode"]: int(datas['subcategory_asst_code'])
                                from Bigflow.Core.models import get_data_from_id as gdfi
                                codes=gdfi('APSUBCAT',data)

                                data.pop('category_id')
                                data.pop('expense_id')
                                data['category_code']=codes['category_code']
                                data['expense_code']=codes['expense_code']
                                data['code']=codes['code']
                                mrobject = MasterRequestObject('SUBCATEGORY', data, 'post')
                            except:
                                common.logger.error(str(traceback.print_exc()))
                    return Response({"MESSAGE": "SUCCESS"})
                else:
                    return Response({"MESSAGE": str(df_outmessage[0])})

            if self.request.query_params.get("Group") == "SET_CCBS_MASTER":
                obj_campaign = mMasters.Masters()
                jsondata = json.loads(request.body.decode('utf-8'))
                obj_campaign.type = self.request.query_params.get("Type")
                obj_campaign.sub_type = self.request.query_params.get("Sub_type")
                obj_campaign.jsonData = json.dumps(jsondata.get('Params').get('FILTER'))
                clasifiction = decry_data(jsondata.get('Params').get('CLASSIFICATION')['Entity_Gid'])
                create_by = decry_data(jsondata.get('Params').get('CLASSIFICATION')['Create_by'])
                obj_campaign.json_classification = json.dumps({'Entity_Gid':clasifiction,'Create_by':create_by})
                df_outmessage = obj_campaign.set_CCBS_Master()
                if df_outmessage[0] == "SUCCESS":
                    return Response({"MESSAGE": "SUCCESS"})
                else:
                    return Response({"MESSAGE": str(df_outmessage[0])})

        except Exception as e:
            return Response({"MESSAGE": "ERROR_OCCURED", "DATA": str(e)})


class StatePrice_API(APIView):
    def post(self, request):
        try:
            obj_State = mMasters.Masters()
            jsondata = json.loads(request.body.decode('utf-8'))
            obj_State.type = self.request.query_params.get("Type")
            obj_State.sub_type = self.request.query_params.get("Subtype")
            obj_State.entity = self.request.query_params.get("entity")
            obj_State.create_by = (self.request.query_params.get("Emp_Gid"))
            obj_State.create_by = [decry_data(obj_State.create_by)]
            obj_State.json_classification = jsondata.get('Parms').get('Classification')
            obj_State.json_classification['entity_gid']=[decry_data(obj_State.entity )]
            obj_State.json_filters = json.dumps(jsondata.get('Parms').get('Filter'))
            obj_State.json_classification = json.dumps(jsondata.get('Parms').get('Classification'))
            out_message = obj_State.get_StatePrice()
            if len(out_message) > 0:
                return Response({"MESSAGE": "FOUND", "DATA": out_message})
        except Exception as e:
            return Response({"MESSAGE": "ERROR_OCCURED", "DATA": str(e)})


class All_Tables_Values_Get(APIView):
    def post(self, request):
        try:
            obj_values = mMasters.Masters()
            #path=(self.request.stream.path)
            obj_values.action = ''
            obj_values.jsonData = request.body.decode('utf-8')
            obj_values.entity_gid = '1'
            #common.main_fun1(request.read(), path)
            log_data = [{"BEFORE_ALL_TABLES_VALUES_GET_SP": obj_values.jsonData}]
            common.logger.error(log_data)
            out_message = obj_values.get_alltablevalue()
            log_data = [{"AFTER_ALL_TABLES_VALUES_GET_SP": len(out_message)}]
            common.logger.error(log_data)
            if out_message.empty == False:
                json_data = json.loads(out_message.to_json(orient='records'))
                return Response({"MESSAGE": "FOUND", "DATA": json_data})
            else:
                return Response({"MESSAGE": "NOT_FOUND"})

        except Exception as e:
            return Response({"MESSAGE": "ERROR_OCCURED", "DATA": str(e)})


class All_Product_Get(APIView):
    def post(self, request):
        try:
            if self.request.query_params.get("Group") == "GET_ALL_PRODUCT":
                jsondata = json.loads(request.body.decode('utf-8'))
                obj_allproduct = mMasters.Masters()
                obj_allproduct.type = self.request.query_params.get("Type")
                obj_allproduct.sub_type = self.request.query_params.get("Sub_Type")
                obj_allproduct.jsonData = json.dumps(jsondata.get('Params').get('FILTER'))
                gid = int(decry_data(jsondata.get('Params').get('CLASSIFICATION')['Entity_Gid']))
                obj_allproduct.json_classification = json.dumps({'Entity_Gid':[gid]})
                ld_out_message = obj_allproduct.get_AllProduct()
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

class EmailVerify_API(APIView):
    def post(self,request):
        try:

                obj_email = mMasters.Masters()
                jsondata = json.loads(request.body.decode('utf-8'))
                obj_email.type = self.request.query_params.get("Type")
                obj_email.sub_type = self.request.query_params.get("SubType")
                obj_email.jsonData = json.dumps(jsondata.get('Params'))
                # obj_email.jsonData = 10764
                obj_email.json_classification = json.dumps({'Entity_Gid': [1]})
                ld_out_message = obj_email.set_updateemailverify()
                # return Response(ld_out_message)
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
        #
        #     json_data = json.loads(ld_out_message.to_json(orient='records'))
        #     return Response(json_data)
        #
        # except Exception as e:
        #     return Response({"MESSAGE": "ERROR_OCCURED", "DATA": str(e)})





class Classification_Get(APIView):
    def post(self, request):
        try:
            if self.request.query_params.get("Group") == "BRANCH_SALES":
                jsondata = json.loads(request.body.decode('utf-8'))
                obj_classification = mMasters.Masters()
                obj_classification.type = self.request.query_params.get("Type")
                obj_classification.sub_type = self.request.query_params.get("Sub_Type")
                obj_classification.jsonData = jsondata.get('Params').get('FILTER')

                obj_classification.jsonData['Employee_Gid']=decry_data(obj_classification.jsonData['Employee_Gid'])
                obj_classification.json_classification = jsondata.get('Params').get('CLASSIFICATION')
                obj_classification.entity = self.request.query_params.get("entity")
                obj_classification.json_classification['Entity_Gid'] = decry_data( obj_classification.entity )
                obj_classification.jsonData = json.dumps(jsondata.get('Params').get('FILTER'))
                obj_classification.json_classification = json.dumps(obj_classification.json_classification)
                ld_out_message = obj_classification.get_classification_summary()
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


class ProductCat_type_Set(APIView):
    def post(self, request):
       try:
            if self.request.query_params.get("Group") ==  "Product_Type" or 'Product_Carton_Map' or 'Product_Category':
                jsondata = json.loads(request.body.decode('utf-8'))
                Entity_Gid = decry_data(jsondata['Entity_Gid'])
                Create_By = decry_data(jsondata['Create_By'])
                jsondata['Entity_Gid'] = Entity_Gid
                jsondata['create_by'] = Create_By
                jsondata['Create_By'] = Create_By
                obj_prodcat = mMasters.Masters()
                obj_prodcat.action = self.request.query_params.get("Action")
                obj_prodcat.type = self.request.query_params.get("Type")
                obj_prodcat.jsonData = json.dumps(jsondata)
                out_message = obj_prodcat.Set_Productcat()
                if (out_message[0] == "SUCCESS") or (out_message[0] == "SUCCESSFULLY UPDATED"):
                  return Response({"MESSAGE": "SUCCESS"})
                else:
                  return Response({"MESSAGE": "FAIL", "DATA": str(out_message[0])})

            elif self.request.query_params.get("Group") ==  "Product_Type1" or 'Product_Carton_Map1' or 'insert_data' or 'Product_Category1':
                jsondata = json.loads(request.body.decode('utf-8'))
                create_by = decry_data(jsondata['create_by'])
                jsondata['create_by'] = create_by
                obj_prodcat = mMasters.Masters()
                obj_prodcat.action = self.request.query_params.get("Action")
                obj_prodcat.type = self.request.query_params.get("Type")
                obj_prodcat.jsonData = json.dumps(jsondata)
                out_message = obj_prodcat.Set_Productcat()
                if (out_message[0] == "SUCCESS") or (out_message[0] == "SUCCESSFULLY UPDATED"):
                  return Response({"MESSAGE": "SUCCESS"})
                else:
                  return Response({"MESSAGE": "FAIL", "DATA": str(out_message[0])})

       except Exception as e:
            return Response({"MESSAGE": "ERROR", "DATA": str(e)})


class Supplier_Master(APIView):
    def post(self, request):
        try:
            if self.request.query_params.get("Group") == "Supplier_Get":
                jsondata = json.loads(request.body.decode('utf-8'))
                obj_supplier = mMasters.Masters()
                obj_supplier.type = self.request.query_params.get("Type")
                obj_supplier.sub_type = self.request.query_params.get("SubType")
                obj_supplier.json_supplier = json.dumps(jsondata.get('Params').get('Details'))
                obj_supplier.json_classification = json.dumps(jsondata.get('Params').get('Classification'))
                out_message = obj_supplier.get_Supplier()
                if out_message.get("MESSAGE") == 'FOUND':
                    ld_dict = {"DATA": json.loads(out_message.get("DATA").to_json(orient='records')),
                               "MESSAGE": "FOUND"}

                elif out_message.get("MESSAGE") == 'NOT_FOUND':
                    ld_dict = {"MESSAGE": out_message.get("MESSAGE")}
                else:
                    ld_dict = {"MESSAGE": 'ERROR_OCCURED.' + out_message.get("MESSAGE")}
                return Response(ld_dict)
            if self.request.query_params.get("Group") == "Supplier_Set":
                jsondata = json.loads(request.body.decode('utf-8'))
                obj_supplier = mMasters.Masters()
                obj_supplier.action = self.request.query_params.get("Action")
                obj_supplier.json_supplier = json.dumps(jsondata.get('Params').get('Supplier'))
                obj_supplier.json_address = json.dumps(jsondata.get('Params').get('Address'))
                obj_supplier.json_contact = json.dumps(jsondata.get('Params').get('Contact'))
                obj_supplier.json_clasfication = json.dumps(jsondata.get('Params').get('Classification'))
                out_message = obj_supplier.set_Supplier()
                if out_message[0] == "SUCCESS":
                    return Response({"MESSAGE": "SUCCESS"})
                else:
                    return Response({"MESSAGE": "FAIL", "DATA": str(out_message[0])})
            elif self.request.query_params.get("Group") == "Supplier_Update":
                jsondata = json.loads(request.body.decode('utf-8'))
                obj_supplier = mMasters.Masters()
                obj_supplier.action = self.request.query_params.get("Action")
                obj_supplier.json_supplier = json.dumps(jsondata.get('Params').get('Supplier'))
                obj_supplier.json_address = json.dumps(jsondata.get('Params').get('Address'))
                obj_supplier.json_contact = json.dumps(jsondata.get('Params').get('Contact'))
                obj_supplier.json_clasfication = json.dumps(jsondata.get('Params').get('Classification'))
                out_message = obj_supplier.set_Supplier()
                if out_message[0] == "SUCCESS":
                    return Response({"MESSAGE": "SUCCESS"})
                else:
                    return Response({"MESSAGE": "FAIL", "DATA": str(out_message[0])})
            elif self.request.query_params.get("Group") == "Active_INactive_supplier":
                jsondata = json.loads(request.body.decode('utf-8'))
                obj_supplier = mMasters.Masters()
                obj_supplier.action = self.request.query_params.get("Action")
                obj_supplier.json_supplier = json.dumps(jsondata.get('parms').get('supplier'))
                obj_supplier.json_address ='{}'
                obj_supplier.json_contact ='{}'
                obj_supplier.json_clasfication = json.dumps(jsondata.get('parms').get('classification'))
                out_message = obj_supplier.set_Supplier()
                if out_message[0] == "SUCCESS":
                    return Response({"MESSAGE": "SUCCESS"})
                else:
                    return Response({"MESSAGE": "FAIL", "DATA": str(out_message[0])})




        except Exception as e:
            return Response({"MESSAGE": "ERROR_OCCURED", "DATA": str(e)})


class cluster_Master(APIView):
    def post(self, request):
        try:
            if self.request.query_params.get("Group") == "CLUSTER_EMPMAP_FLAG":
                jsondata = json.loads(request.body.decode('utf-8'))
                obj_cluster = mMasters.Masters()
                obj_cluster.action = self.request.query_params.get("Group")

                obj_cluster.jsondata = json.dumps(jsondata.get('Classification'))

                ldf_cluster = obj_cluster.get_cluster()
                if ldf_cluster.empty == False:
                    return Response({"MESSAGE": "FOUND", "DATA": json.loads(ldf_cluster.to_json(orient='records'))})
                else:
                    return Response({"MESSAGE": "NOT_FOUND"})

        except Exception as e:
            return Response({"MESSAGE": "ERROR_OCCURED", "DATA": str(e)})


class Product_Master(APIView):
    def post(self, request):
        try:
            if self.request.query_params.get("Group") == "Product_Get":
                jsondata = json.loads(request.body.decode('utf-8'))
                obj_product = mMasters.Masters()
                obj_product.type = self.request.query_params.get("Type")
                obj_product.subtype = self.request.query_params.get("SubType")
                entity = json.loads(self.request.query_params.get("Entity_gid"))
                gid = entity['Entity_Gid']
                gid = int(decry_data(gid))
                obj_product.Entity_gid = json.dumps({'Entity_Gid':[gid]})
                obj_product.jsondata = json.dumps(jsondata.get('Filters'))
                out_message = obj_product.getsmry_product()
                if out_message.get("MESSAGE") == 'FOUND':
                    ld_dict = {"DATA": json.loads(out_message.get("DATA").to_json(orient='records')),
                               "MESSAGE": "FOUND"}

                elif out_message.get("MESSAGE") == 'NOT_FOUND':
                    ld_dict = {"MESSAGE": out_message.get("MESSAGE")}
                else:
                    ld_dict = {"MESSAGE": 'ERROR_OCCURED.' + out_message.get("MESSAGE")}
                return Response(ld_dict)
            elif self.request.query_params.get("Group") == "Product_Set":
                jsondata = json.loads(request.body.decode('utf-8'))
                obj_product_set = mMasters.Masters()
                obj_product_set.action = self.request.query_params.get("Action")
                obj_product_set.type = self.request.query_params.get("Type")
                entity_gid = decry_data(jsondata['Entity_Gid'])
                create_by = decry_data(jsondata['Create_By'])
                jsondata['data']['entity_gid'] = entity_gid
                jsondata['data']['create_by'] = create_by
                obj_product_set.jsonData = json.dumps(jsondata.get("data"))
                out_message = obj_product_set.Set_Productcat()
                if out_message[0] == "SUCCESS":
                    return Response({"MESSAGE": "SUCCESS"})
                else:
                    return Response({ "MESSAGE": str(out_message[0])})
        except Exception as e:
            return Response({"MESSAGE": "ERROR_OCCURED", "DATA": str(e)})


class Hsn_Master(APIView):
    def post(self, request):
        try:
            if self.request.query_params.get("Group") == "SET_HSN_DATA":
                jsondata = json.loads(request.body.decode('utf-8'))
                obj_hsn = mMasters.Masters()
                obj_hsn.action = self.request.query_params.get("Action")
                obj_hsn.type = self.request.query_params.get("Type")
                obj_hsn.sub_type = self.request.query_params.get("Sub_Type")
                obj_hsn.employee_gid = decry_data(self.request.query_params.get("Employee_Gid"))
                obj_hsn.jsondata = json.dumps(jsondata.get('Params').get('DETAILS'))
                json_classification = jsondata.get('Params').get('CLASSIFICATION')
                entity = decry_data(json_classification['Entity_Gid'])
                obj_hsn.json_classification = json.dumps({'Entity_Gid': entity})
                ld_out_message = obj_hsn.set_hsn()
                if ld_out_message.get("MESSAGE") == 'SUCCESS':
                    ld_dict = {"MESSAGE": "SUCCESS"}
                elif ld_out_message.get("MESSAGE") == 'FAIL':
                    ld_dict = {"MESSAGE": "FAIL"}
                else:
                    ld_dict = {"MESSAGE": 'ERROR_OCCURED.' + ld_out_message.get("MESSAGE")}
                if(ld_dict['MESSAGE']=="SUCCESS"):
                    try:
                        # print(jsondata)
                        data=jsondata['Params']['DETAILS']
                        from Bigflow.Core.models import get_data_from_id as gdfi
                        codes=gdfi('HSN',data)
                        hsn_data={'code':data['HSN_Code'],'description':data['HSN_Desc'],
                                  'cgstrate':codes['cgstrate'],'igstrate':codes['igstrate'],
                                  'sgstrate':codes['sgstrate'],'cgstrate_code':codes['cgstrate_code'],
                                  'sgstrate_code':codes['sgstrate_code'],'igstrate_code':codes['igstrate_code'],
                                  'Entity_Gid':json_classification['Entity_Gid'],'create_by':self.request.query_params.get("Employee_Gid")}
                        # print(hsn_data)
                        mrobject=MasterRequestObject('HSN',hsn_data,'POST')
                    except:
                        common.logger.error(traceback.print_exc())


                return Response(ld_dict)
            elif self.request.query_params.get("Group") == "GET_HSN_DETAILS":
                jsondata = json.loads(request.body.decode('utf-8'))
                obj_hsn = mMasters.Masters()
                obj_hsn.action = self.request.query_params.get("Action")
                obj_hsn.type = self.request.query_params.get("Type")
                obj_hsn.filter_json = json.dumps(jsondata.get('Params').get('DETAILS'))
                obj_hsn.json_classification = jsondata.get('Params').get('CLASSIFICATION')
                #obj_emp.json_classification['Entity_Gid'] =int(decry_data(obj_emp.json_classification['Entity_Gid'] ))
                obj_hsn.json_classification = json.dumps(jsondata.get('Params').get('CLASSIFICATION'))
                out_message = obj_hsn.get_hsn_data()
                json_data = json.loads(out_message.to_json(orient='records'))
                return Response(json_data)

        except Exception as e:
            return Response({"MESSAGE": "ERROR_OCCURED", "DATA": str(e)})


class Tax_Master(APIView):
    def post(self, request):
        try:
            if self.request.query_params.get("Group") == "SET_TAX_DATA":
                jsondata = json.loads(request.body.decode('utf-8'))
                obj_tax = mMasters.Masters()
                obj_tax.action = self.request.query_params.get("Action")
                obj_tax.type = self.request.query_params.get("Type")
                obj_tax.sub_type = self.request.query_params.get("Sub_Type")
                obj_tax.employee_gid =decry_data(self.request.query_params.get("Employee_Gid"))
                create_by=decry_data(self.request.query_params.get("Employee_Gid"))
                obj_tax.jsondata = json.dumps(jsondata.get('Params').get('DETAILS'))
                json_classification = jsondata.get('Params').get('CLASSIFICATION')
                entity = decry_data(json_classification['Entity_Gid'])
                obj_tax.json_classification = json.dumps({'Entity_Gid': entity})
                ld_out_message = obj_tax.set_tax_data()
                if ld_out_message.get("MESSAGE") == 'SUCCESS':
                    ld_dict = {"MESSAGE": "SUCCESS"}
                elif ld_out_message.get("MESSAGE") == 'FAIL':
                    ld_dict = {"MESSAGE": "FAIL"}
                else:
                    ld_dict = {"MESSAGE": 'ERROR_OCCURED.' + ld_out_message.get("MESSAGE")}

                if (ld_dict['MESSAGE'] == 'SUCCESS'):
                    try:
                        if (self.request.query_params.get("Sub_Type") == 'ISACTIVE'):
                            print(jsondata)
                            from Bigflow.Core.models import get_data_from_id as gdfi
                            codes=gdfi('TAXACT',jsondata.get('Params')['DETAILS'])
                            taxact=jsondata.get('Params')['DETAILS']['ISACTIVE']
                            data={'tax_code':codes['tax_code'],'isactive':jsondata.get('Params')['DETAILS']['ISACTIVE'],'Entity_Gid':json_classification['Entity_Gid'],'create_by':self.request.query_params.get("Employee_Gid")}
                            mrobject=MasterRequestObject('TAXACT',data,'POST')
                        if (self.request.query_params.get("Sub_Type") == 'TAX_NAME'):
                            # print(jsondata)
                            data = jsondata['Params']
                            data = data['DETAILS']

                            if (data['Is_Receivable'] == 'Y'):
                                data['Is_Receivable'] = True
                            else:
                                data['Is_Receivable'] = False
                            if (data['Is_Payable'] == 'Y'):
                                data['Is_Payable'] = True
                            else:
                                data['Is_Payable'] = False
                            #print(data)
                            from Bigflow.Core.models import get_data_from_id
                            mst_data={}
                            mst_data['Tax_Name']=data['Tax_Name']
                            codes=get_data_from_id('TAX',mst_data)
                            data = {"code":codes['code'],"name": data['Tax_Name'], "receivable": data['Is_Receivable'],
                                    "payable": data['Is_Payable'], "glno": data['GL_No'],'Entity_Gid':json_classification['Entity_Gid'],'create_by':self.request.query_params.get("Employee_Gid")}
                            mrobject = MasterRequestObject('TAX', data, 'POST')
                    except:
                        common.logger.error(str(traceback.print_exc()))
                # print(self.request.query_params.get("Sub_Type"))
                if (ld_dict['MESSAGE'] == 'SUCCESS'):
                    try:
                        if (self.request.query_params.get("Sub_Type") == 'SUBTAX_NAME'):
                            data = jsondata['Params']
                            data = data['DETAILS']
                            from Bigflow.Core.models import get_data_from_id as gdfi
                            print(data)
                            codes=gdfi('SUBTAX',data)
                            common.logger.error(codes)
                            data = {"code":codes['code'],"tax_code": codes['tax_code'], "name": data['SubTax_Name'],
                                    "remarks": data['SubTax_Remarks'], "glno": data['GL_No'],'Entity_Gid':json_classification['Entity_Gid'],'create_by':self.request.query_params.get("Employee_Gid")}

                            #print(data)
                            mrobject = MasterRequestObject('SUB TAX', data, 'POST')
                    except:
                        traceback.print_exc()
                if (ld_dict['MESSAGE'] == 'SUCCESS'):
                    try:
                        if (self.request.query_params.get("Sub_Type") == 'TAX_RATE_NAME'):
                            # print(jsondata)
                            data = jsondata['Params']
                            print(data)
                            data=data['DETAILS']
                            data = {"subtax_id": str(data['SubTax_Gid']), "name": data['Tax_Rate_Name'],
                                    "rate": float(data['Tax_Rate']),'Entity_Gid':json_classification['Entity_Gid'],'create_by':self.request.query_params.get("Employee_Gid")}
                            from Bigflow.Core.models import get_data_from_id as gdfi
                            codes=gdfi('TAXRATE',data)
                            print(codes)
                            data={"subtax_code":codes['subtax_code'],"code":codes['code'],"name":data['name'],"rate":data["rate"],"Entity_Gid":data["Entity_Gid"],'create_by':self.request.query_params.get("Employee_Gid")}
                            print(data)
                            mrobject = MasterRequestObject('TAX RATE', data, 'POST')
                    except:
                        traceback.print_exc()
                return Response(ld_dict)
            elif self.request.query_params.get("Group") == "GET_TAX_DATA":
                jsondata = json.loads(request.body.decode('utf-8'))
                obj_tax = mMasters.Masters()
                obj_tax.type = self.request.query_params.get("Type")
                obj_tax.sub_type = self.request.query_params.get("Sub_Type")
                obj_tax.filter_json = json.dumps(jsondata.get('Params').get('FILTER'))
                json_classification = jsondata.get('Params').get('CLASSIFICATION')
                entity = decry_data(json_classification['Entity_Gid'])
                obj_tax.json_classification = json.dumps({'Entity_Gid': entity})
                out_message = obj_tax.get_tax_data()
                if out_message.get("MESSAGE") == 'FOUND':
                    ld_dict = {"DATA": json.loads(out_message.get("DATA").to_json(orient='records')),
                               "MESSAGE": "FOUND"}
                elif out_message.get("MESSAGE") == 'NOT_FOUND':
                    ld_dict = {"MESSAGE": out_message.get("MESSAGE")}
                else:
                    ld_dict = {"MESSAGE": 'ERROR_OCCURED.' + out_message.get("MESSAGE")}
                return Response(ld_dict)
        except Exception as e:
            return Response({"MESSAGE": "ERROR_OCCURED", "DATA": str(e)})

class Business_Segment(APIView):
    def post(self, request):
        try:
            if self.request.query_params.get("Group") == "BUS_DATA_SET":
                jsondata = json.loads(request.body.decode('utf-8'))
                obj_tax = mMasters.Masters()
                obj_tax.action = self.request.query_params.get("Action")
                obj_tax.type = self.request.query_params.get("Type")
                obj_tax.sub_type = self.request.query_params.get("Sub_Type")
                obj_tax.employee_gid = decry_data(self.request.query_params.get("Employee_Gid"))
                obj_tax.jsondata = json.dumps(jsondata.get('Params').get('DETAILS'))
                clasification  = decry_data(jsondata.get('Params').get('CLASSIFICATION')['Entity_Gid'])
                obj_tax.json_classification = json.dumps({'Entity_Gid':clasification})
                ld_out_message = obj_tax.set_businesssegment_data()
                if ld_out_message.get("MESSAGE") == 'SUCCESS':
                    ld_dict = {"MESSAGE": "SUCCESS"}
                elif ld_out_message.get("MESSAGE") == 'FAIL':
                    ld_dict = {"MESSAGE": "FAIL"}
                else:
                    ld_dict = {"MESSAGE": 'ERROR_OCCURED.' + ld_out_message.get("MESSAGE")}
                return Response(ld_dict)
        except Exception as e:
            return Response({"MESSAGE": "ERROR_OCCURED", "DATA": str(e)})

class Courier_Master(APIView):
    def post(self, request):
        try:
            if self.request.query_params.get("Group") == "SET_COURIER_DATA":
                jsondata = json.loads(request.body.decode('utf-8'))
                obj_courier = mMasters.Masters()
                obj_courier.action = self.request.query_params.get("Action")
                obj_courier.type = self.request.query_params.get("Type")
                obj_courier.sub_type = self.request.query_params.get("Sub_Type")
                obj_courier.employee_gid = decry_data(self.request.query_params.get("Employee_Gid"))
                obj_courier.jsondata = json.dumps(jsondata.get('Params').get('DETAILS'))
                json_classification = decry_data(jsondata.get('Params').get('CLASSIFICATION')['Entity_Gid'])
                obj_courier.json_classification = json.dumps({'Entity_Gid':json_classification})
                ld_out_message = obj_courier.set_courier()
                if ld_out_message.get("MESSAGE") == 'SUCCESS':
                    ld_dict = {"MESSAGE": "SUCCESS"}
                elif ld_out_message.get("MESSAGE") == 'FAIL':
                    ld_dict = {"MESSAGE": "FAIL"}
                else:
                    ld_dict = {"MESSAGE": 'ERROR_OCCURED.' + ld_out_message.get("MESSAGE")}
                return Response(ld_dict)
            elif self.request.query_params.get("Group") == "GET_COURIER_DATA":
                jsondata = json.loads(request.body.decode('utf-8'))
                obj_courier = mMasters.Masters()
                obj_courier.type = self.request.query_params.get("Type")
                obj_courier.sub_type = self.request.query_params.get("Sub_Type")
                obj_courier.filter_json = json.dumps(jsondata.get('Params').get('FILTER'))
                json_classification = decry_data(jsondata.get('Params').get('CLASSIFICATION')['Entity_Gid'])
                obj_courier.json_classification = json.dumps({'Entity_Gid':json_classification})
                out_message = obj_courier.get_courier_data()
                if out_message.get("MESSAGE") == 'FOUND':
                    ld_dict = {"DATA": json.loads(out_message.get("DATA").to_json(orient='records')),
                               "MESSAGE": "FOUND"}
                elif out_message.get("MESSAGE") == 'NOT_FOUND':
                    ld_dict = {"MESSAGE": out_message.get("MESSAGE")}
                else:
                    ld_dict = {"MESSAGE": 'ERROR_OCCURED.' + out_message.get("MESSAGE")}
                return Response(ld_dict)
        except Exception as e:
            return Response({"MESSAGE": "ERROR_OCCURED", "DATA": str(e)})


class Master_Data(APIView):
    def post(self, request):
        try:
            if self.request.query_params.get("Group") == "GET_EMP_DATA":
                jsondata = json.loads(request.body.decode('utf-8'))
                obj_emp = mMasters.Masters()
                obj_emp.type = self.request.query_params.get("Type")
                obj_emp.sub_type = self.request.query_params.get("Sub_Type")
                obj_emp.limit = self.request.query_params.get("Limit")
                obj_emp.filter_json = json.dumps(jsondata.get('Params').get('FILTER'))
                obj_emp.json_classification =jsondata.get('Params').get('CLASSIFICATION')
               # obj_emp.json_classification['Entity_Gid'] =int(decry_data(obj_emp.json_classification['Entity_Gid'] ))

                obj_emp.json_classification = json.dumps(jsondata.get('Params').get('CLASSIFICATION'))
                out_message = obj_emp.get_master_data()
                if out_message.get("MESSAGE") == 'FOUND':
                    ld_dict = {"DATA": json.loads(out_message.get("DATA").to_json(orient='records')),
                               "MESSAGE": "FOUND"}
                elif out_message.get("MESSAGE") == 'NOT_FOUND':
                    ld_dict = {"MESSAGE": out_message.get("MESSAGE")}
                else:
                    ld_dict = {"MESSAGE": 'ERROR_OCCURED.' + out_message.get("MESSAGE")}
                return Response(ld_dict)
        except Exception as e:
            return Response({"MESSAGE": "ERROR_OCCURED", "DATA": str(e)})
 ### Get te emp data for ORM Module
class MasterSyncORM(APIView):
    def post(self,request):
        try:
            if self.request.query_params.get("Type") == "EMPLOYEE_SUMMARY" or self.request.query_params.get("Type") == 'EMPLOYEE_UPDATE' \
                    or self.request.query_params.get("Type") == "DEPT_SUMMARY" or self.request.query_params.get("Type") == "DEPT_UPDATE" :
                path = self.request.stream.path
                jsondata = json.loads(request.body.decode('utf-8'))
                obj_emp = mMasters.Masters()
                obj_emp.type = self.request.query_params.get("Type")
                obj_emp.filter_json = json.dumps(jsondata)
                common.main_fun1(request.read(), path)
                out_message = obj_emp.get_masterdataorm()
                if out_message.get("MESSAGE") == 'FOUND':
                    ld_dict = {"DATA": json.loads(out_message.get("DATA").to_json(orient='records')),
                               "MESSAGE": "FOUND"}
                elif out_message.get("MESSAGE") == 'NOT_FOUND':
                    ld_dict = {"MESSAGE": out_message.get("MESSAGE")}
                else:
                    ld_dict = {"MESSAGE": 'ERROR_OCCURED.' + out_message.get("MESSAGE")}
                return Response(ld_dict)
        except Exception as e:
            common.logger.error(e)
            return Response({"MESSAGE": "ERROR_OCCURED", "DATA": str(e)})



class new_data_insert(APIView):
    def post(self,request):
        try:
            if self.request.query_params.get("Group") == "GENERIC_API_AP":
                jsondata = json.loads(request.body.decode('utf-8'))
                obj_prodcat = mMasters.Masters()
                obj_prodcat.action = self.request.query_params.get("Action")
                obj_prodcat.type = self.request.query_params.get("Type")
                obj_prodcat.jsonData = json.dumps(jsondata.get('Params'))
                obj_prodcat.json_classification = json.dumps(jsondata.get('Classification'))
                log_data = [{"BEFORE_newAPIfromMEMO": jsondata}]
                common.logger.error(log_data)
                out_message = obj_prodcat.new_insert_frm_MS()
                log_data = [{"AFTER_newAPIfromMEMO": out_message}]
                common.logger.error(log_data)
                if out_message == "SUCCESSFULLY INSERTED":
                    return Response({"MESSAGE": "SUCCESSFULLY INSERTED"})
                else:
                    return Response({"MESSAGE": out_message})
        except Exception as e:
            common.logger.error(e)
            return Response({"MESSAGE": "ERROR", "DATA": str(e)})


class new_ecf_pdf_get(APIView):
    def post(self,request):
        try:
            if self.request.query_params.get("Group") == "ECF_PDF_GET":
                jsondata = json.loads(request.body.decode('utf-8'))
                obj_prodcat = mAP.ap_model()
                obj_prodcat.action = self.request.query_params.get("Action")
                obj_prodcat.type = self.request.query_params.get("Type")
                obj_prodcat.filter = json.dumps(jsondata.get('Params'))
                obj_prodcat.classification = json.dumps(jsondata.get('Classification'))
                log_data = [{"BEFORE_ecf_pdfforMEMO": jsondata}]
                common.logger.error(log_data)
                out_message = obj_prodcat.get_ecf_pdf_data()
                log_data = [{"AFTER_ecf_pdfforMEMO": out_message}]
                common.logger.error(log_data)
                ld_dict = {"DATA": out_message,
                           "MESSAGE": "FOUND"}
                return Response(ld_dict)
        except Exception as e:
            common.logger.error(e)
            return Response({"MESSAGE": "ERROR_OCCURED", "DATA": str(e)})

class new_ecf_data_insert(APIView):
    def post(self, request):
        try:
            if (self.request.query_params.get("Group") == "GENERIC_API_ECF" and self.request.query_params.get("Rems_Edit")) == "1":
                jsondata = json.loads(request.body.decode('utf-8'))
                obj_prodcat = mMasters.Masters()
                obj_prodcat.action = self.request.query_params.get("Action")
                obj_prodcat.type = self.request.query_params.get("Type")
                header_details = jsondata.get('Params').get('HEADER_DETAIL_JSON')
                header_details.update({"Is_Edit": "Y"})
                obj_prodcat.jsonData = json.dumps(header_details)
                obj_prodcat.jsondata = json.dumps(jsondata.get('Params').get('DEBIT_JSON'))
                obj_prodcat.filter_json = json.dumps(jsondata.get('Params').get('CREDIT_JSON'))
                obj_prodcat.json_classification = json.dumps(jsondata.get('Classification'))
                log_data = [{"BEFORE_ECFAPIfromMEMO": jsondata}]
                common.logger.error(log_data)
                out_message = obj_prodcat.new_ecf_insert_frm_MS()
                log_data = [{"AFTER_ECFAPIfromMEMO": out_message}]
                common.logger.error(log_data)
                if out_message[0] == "SUCCESS":
                    return Response({"MESSAGE": "SUCCESSFULLY INSERTED"})
                else:
                    return Response({"MESSAGE": out_message[0]})
            elif(self.request.query_params.get("Group") == "GENERIC_API_ECF" and self.request.query_params.get("Rems_Edit")) == "0":
                jsondata = json.loads(request.body.decode('utf-8'))
                obj_prodcat = mMasters.Masters()
                obj_prodcat.action = self.request.query_params.get("Action")
                obj_prodcat.type = self.request.query_params.get("Type")
                header_detail = jsondata.get('Params').get('HEADER_DETAIL_JSON')
                header_detail.update({"Is_Edit": "N"})
                obj_prodcat.jsonData = json.dumps(header_detail)
                obj_prodcat.jsondata = json.dumps(jsondata.get('Params').get('DEBIT_JSON'))
                obj_prodcat.filter_json = json.dumps(jsondata.get('Params').get('CREDIT_JSON'))
                obj_prodcat.json_classification = json.dumps(jsondata.get('Classification'))
                log_data = [{"BEFORE_ECFAPIfromMEMO": jsondata}]
                common.logger.error(log_data)
                out_message = obj_prodcat.new_ecf_insert_frm_MS()
                log_data = [{"AFTER_ECFAPIfromMEMO": out_message}]
                common.logger.error(log_data)
                if out_message[0] == "SUCCESS":
                    return Response({"MESSAGE": "SUCCESSFULLY INSERTED"})
                else:
                    return Response({"MESSAGE": out_message[0]})
        except Exception as e:
            common.logger.error(e)
            return Response({"MESSAGE": "ERROR", "DATA": str(e)})

class update_pesonal_number(APIView):
    def post(self,request):
        try:
            common.logger.error("UPDATE_NO_JSON:" + str(json.loads(request.body.decode('utf-8'))))
            if self.request.query_params.get("GROUP") == "EMPLOYEE_MOBILENO":
                jsondata = json.loads(request.body.decode('utf-8'))
                common.logger.error("UPDATE_NO_JSON:"+str(jsondata))
                obj_prodcat = mMasters.Masters()
                obj_prodcat.action = self.request.query_params.get("Action")
                obj_prodcat.jsondata = json.dumps(jsondata.get('Params').get('Filter'))
                params=(obj_prodcat.action,obj_prodcat.jsondata,'')
                common.logger.error("SP_PARAMETERS:"+str(params))
                log_data = [{"BEFORE_mob_num": jsondata}]
                common.logger.error(log_data)
                out_message = obj_prodcat.update_personal_info()
                common.logger.error([{"UPDATEMOBILE_SP_OUT":out_message}])
                log_data = [{"AFTER_mob_num": out_message}]
                common.logger.error(log_data)
                ld_dict = {"MESSAGE": out_message}
                return Response(ld_dict)
        except Exception as e:
            common.logger.error(e)
            return Response({"MESSAGE": "ERROR_OCCURED", "DATA": str(e)})

