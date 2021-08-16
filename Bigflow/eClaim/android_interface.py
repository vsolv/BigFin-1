
from rest_framework.response import Response
from rest_framework.utils import json
from Bigflow.eClaim.model import meClaim
import base64

class Android():
    def post_summary(self,request):
        token = request.auth.payload.get('user_id')
        obj_claim = meClaim.eClaim_Model()
        emp_data = {
            "empids": token
        }
        obj_claim.filter_json = json.dumps(emp_data)
        emp_bnk = obj_claim.eClaim_employeebnk_get()
        bank_data = json.loads(emp_bnk.get("DATA").to_json(orient='records'))
        entity_gid = bank_data[0].get('entity_gid')
        filter = {
            "Employee_gid":token,
            "createby":token,
            "Entity_Gid" : entity_gid
        }
        query = request.query_params
        jsondata = json.loads(request.body.decode('utf-8'))
        for key,value in query.items():
            filter[key] = value
        for key,value in jsondata.items():
            filter[key] = value
        return filter

    def get_method(self,request):
        token = request.auth.payload.get('user_id')
        obj_claim = meClaim.eClaim_Model()
        emp_data = {
            "empids": token
        }
        obj_claim.employee_gid = token
        emp_bnk = obj_claim.eClaim_entity_get()
        bank_data = json.loads(emp_bnk.get("DATA").to_json(orient='records'))
        entity_gid = bank_data[0].get('entity_gid')
        filter = {
            "Employee_gid": token,
            "createby": token,
            "Entity_Gid": entity_gid
        }
        query = request.query_params
        for key,value in query.items():
            filter[key] = value
        return filter

    def set_data_dtl(self,request):
        jsondata = json.loads(request.body.decode('utf-8'))
        details = jsondata.get('DETAILS')
        return details

    def set_data_chng(self,request):
        jsondata = json.loads(request.body.decode('utf-8'))
        change = jsondata.get('DATA')
        final = {
            "DATA" : change
        }
        return final

    def gid_check(self,data):
        key = data.keys()
        if 'gid' in key :
            print('s')
        else:
            data['gid'] =0
        return data

    def gid_array_check(self,data):
        content = data.get('DATA')
        for i in content:
            key = i.keys()
            if 'gid' in key :
                print('s')
            else:
                i['gid'] =0
        return data

    def param_conversion(self,data,entity_gid):
        data['Entity_Gid'] = entity_gid
        param = {
            "Params":{
                "FILTER":data
            }
        }
        return param

    def param_conversion2(self,data,entity_gid,emp_gid):
        data['Entity_Gid'] = entity_gid
        data['Employee_gid'] = emp_gid
        data['processedby'] = emp_gid
        data['createby'] = emp_gid
        param = {
            "Params":{
                "DETAILS":data
            }
        }
        return param

    def param_conversion3(self,request,data):
        emp_gid = request.auth.payload.get('user_id')
        obj_claim = meClaim.eClaim_Model()
        emp_data = {
            "empids": emp_gid
        }
        obj_claim.filter_json = json.dumps(emp_data)
        emp_bnk = obj_claim.eClaim_employeebnk_get()
        bank_data = json.loads(emp_bnk.get("DATA").to_json(orient='records'))
        entity_gid = bank_data[0].get('entity_gid')
        data['Entity_Gid'] = entity_gid
        data['Employee_gid'] = emp_gid
        data['processedby'] = emp_gid
        data['createby'] = emp_gid
        return data


    def gid_ccbsarray_check(self, data):
        content = data.get('CCBS')
        for i in content:
            key = i.keys()
            if 'gid' in key:
                print('s')
            else:
                i['gid'] = 0
        return data