from rest_framework.views import APIView
from rest_framework.response import Response
import json
from Bigflow.Report.Model import mStock


class StockAPI(APIView):

    def post(self, request):
        try:
            if self.request.query_params.get("Group") == "STOCK_SUMMARY":
                jsondata = json.loads(request.body.decode('utf-8'))
                obj_stock = mStock.StockModel()
                obj_stock.type = self.request.query_params.get("Type")
                obj_stock.sub_type = self.request.query_params.get("Sub_Type")
                obj_stock.from_date = self.request.query_params.get("From_Date")
                obj_stock.to_date = self.request.query_params.get("To_Date")
                obj_stock.product_gid = self.request.query_params.get("Product_Gid")
                obj_stock.supplier_gid = self.request.query_params.get("Supplier_Gid")
                obj_stock.entity_gid = self.request.query_params.get("Entity_Gid")
                obj_stock.jsonData = json.dumps(jsondata.get('Params').get('FILTER'))
                ld_out_message = obj_stock.get_stock()
                if ld_out_message.get("MESSAGE") == 'FOUND':
                    ld_dict = {"DATA": json.loads(ld_out_message.get("DATA").to_json(orient='records')),
                               "MESSAGE": "FOUND"}
                elif ld_out_message.get("MESSAGE") == 'NOT_FOUND':
                    ld_dict = {"MESSAGE": ld_out_message.get("MESSAGE")}
                else:
                    ld_dict = {"MESSAGE": 'ERROR_OCCURED.' + ld_out_message.get("MESSAGE")}

                return Response(ld_dict)

            elif self.request.query_params.get("Group") == "SET_UPDATED_STOCK":
                jsondata = json.loads(request.body.decode('utf-8'))
                obj_stock = mStock.StockModel()
                obj_stock.type = self.request.query_params.get("Type")
                obj_stock.action = self.request.query_params.get("Action")
                obj_stock.create_by = self.request.query_params.get("Create_by")
                obj_stock.json = json.dumps(jsondata.get('Params').get('FILTER'))
                obj_stock.stock_json = json.dumps(jsondata.get('Params').get('STOCK'))
                obj_stock.entity_gid = json.dumps(jsondata.get('Params').get('CLASSIFICATION').get('Entity_Gid'))
                ld_out_message = obj_stock.set_stock()
                if ld_out_message.get("MESSAGE") == 'SUCCESS':
                    ld_dict = {"MESSAGE": "SUCCESS"}
                elif ld_out_message.get("MESSAGE") == 'FAIL':
                    ld_dict = {"MESSAGE": ld_out_message.get("MESSAGE")}
                else:
                    ld_dict = {"MESSAGE": 'ERROR_OCCURED.' + ld_out_message.get("MESSAGE")}
                return Response(ld_dict)
        except Exception as e:
            return Response({"MESSAGE": "ERROR_OCCURED", "DATA": str(e)})



