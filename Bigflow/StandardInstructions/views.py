from django.shortcuts import render
from rest_framework.response import Response
from django.db import connection
import pandas as pd
from django.http import JsonResponse, HttpResponse
import json
from Bigflow.Core.models import decrpt as decry_data
from Bigflow.BranchExp.model import mBranch as mbranch
import numpy as np
import requests
import base64
import Bigflow.Core.models as common
import Bigflow.API.view_sales as view_sales
from Bigflow.menuClass import utility as utl
import Bigflow.Core.jwt_file as jwt
token = common.token()
ip = common.localip()

def StandardInstructions_Templates(request,template_name):
    template_name = template_name
    if template_name is not '':
        utl.check_authorization(request)
        return render(request, template_name+".html")


def Get_All_Table_Metadata_Value(request):
    utl.check_pointaccess(request)
    utl.check_authorization(request)
    if request.method == 'POST':
        jsondata = json.loads(request.body.decode('utf-8'))
        action = jsondata.get('params').get('action')
        type=jsondata.get('params').get('type')
        sub_type = jsondata.get('params').get('sub_type')
        entity_gid = request.session['Entity_gid']
        if action=="Get" and type=="Metadata" and sub_type=="Recuring_Period":
            table_data ={
                        "Table_name":"gal_mst_tmetadata",
                        "Column_1":"metadata_value,metadata_gid",
                        "Column_2":"",
                        "Where_Common":"metadata",
                        "Where_Primary":"columnname",
                        "Primary_Value":"standardinstruction_recurringperiod",
                        "Order_by":"columnname"
                        }
            table ={"data":table_data}
            action ='METADATA'

        params = {'Action':action, 'Entity_Gid': entity_gid}
        token = jwt.token(request)
        headers = {"content-type": "application/json", "Authorization": "" + token + ""}
        datas = json.dumps(table.get('data'))
        resp = requests.post("" + ip + "/All_Tables_Values_Get", params=params, data=datas, headers=headers,
                             verify=False)
        response = resp.content.decode("utf-8")
        return HttpResponse(response)

def Set_SI_Details(request):
    utl.check_pointaccess(request)
    utl.check_authorization(request)
    if request.method == 'POST':
        jsondata = json.loads(request.body.decode('utf-8'))
        action=jsondata.get('params').get('action')
        type=jsondata.get('params').get('type')
        entity_gid=int(decry_data(request.session['Entity_gid']))
        create_by = int(decry_data(request.session['Emp_gid']))
        jsondata["params"]["classification"] = {"Entity_Gid": entity_gid,"Entity_Detail_Gid":1}
        datas = json.dumps(jsondata)
        params = {'action': action, 'type': type,'create_by':create_by}
        token = jwt.token(request)
        headers = {"content-type": "application/json", "Authorization": "" + token + ""}
        result = requests.post("" + ip + "/Set_SI_Details_API", params=params, headers=headers, data=datas, verify=False)
        results = result.content.decode("utf-8")
        return JsonResponse((results), safe=False)

def Get_SI_Details(request):
    utl.check_pointaccess(request)
    utl.check_authorization(request)
    if request.method == 'POST':
        jsondata = json.loads(request.body.decode('utf-8'))
        action=jsondata.get('params').get('action')
        type=jsondata.get('params').get('type')
        entity_gid=int(decry_data(request.session['Entity_gid']))
        create_by = int(decry_data(request.session['Emp_gid']))
        jsondata["params"]["classification"] = {"Entity_Gid": entity_gid}
        datas = json.dumps(jsondata)
        params = {'action': action, 'type': type,'create_by':create_by}
        token = jwt.token(request)
        headers = {"content-type": "application/json", "Authorization": "" + token + ""}
        result = requests.post("" + ip + "/Get_SI_Details_API", params=params, headers=headers, data=datas, verify=False)
        results = result.content.decode("utf-8")
        return JsonResponse(json.loads(results), safe=False)