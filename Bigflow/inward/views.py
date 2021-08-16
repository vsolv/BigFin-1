from django.shortcuts import render
from Bigflow.inward.model import mInvoice
from django.http import JsonResponse
import json
import requests
from django.http import HttpResponse
import datetime
import pandas as pd
import Bigflow.Core.models as common
from Bigflow.Core.models import decrpt as decry_data
import Bigflow.Core.jwt_file as jwt
from Bigflow.menuClass import utility as utl
ip = common.localip()
token = common.token()

def inward_summary(request):
    utl.check_authorization(request)
    return render(request, "inw_inwardsummary.html");

def setinwarddetails(request):
    utl.check_authorization(request)
    return render(request, "inw_trn_inwardcreate.html");


def inward_create(request):
    utl.check_pointaccess(request)
    utl.check_authorization(request)
    if request.method == 'POST':
        try:
            path = request.path
            inward_hdl =  mInvoice.inward_model()
            jsondata = json.loads(request.body.decode('utf-8'))
            inward_hdl.action = jsondata.get('params').get('Action')
            inward_hdl.type = jsondata.get('params').get('Type')
            inward_hdl.inwardheader_json = jsondata.get('params').get('lj_header')
            if (len( inward_hdl.inwardheader_json) != 0):
                     inward_hdl.inwardheader_json["HEADER"][0]["Received_by"] = int(decry_data(request.session['Emp_gid']))
            inward_hdl.inwarddetail_json = jsondata.get('params').get('lj_details')
            inward_hdl.entity_gid = int(decry_data(request.session['Entity_gid']))
            inward_hdl.employee_gid = int(decry_data(request.session['Emp_gid']))
            common.main_fun1(request.read(), path)
            inward_header = outputSplit(inward_hdl.set_inward(), 1)
            return JsonResponse(inward_header, safe=False)
        except Exception as e:
            return JsonResponse({"MESSAGE": "ERROR_OCCURED", "DATA": str(e)})

def outputSplit(tubledtl,index):
    temp=tubledtl[0].split(',')
    if(len(temp)>1):
        if (index==0):
            return int(temp[0])
        else:
            return temp[1]
    else:
        return  temp[0]

def get_inwardsummary(request):
    utl.check_pointaccess(request)
    utl.check_authorization(request)
    if request.method == 'POST':
        try:
            path = request.path
            obj_inwardheader = mInvoice.inward_model()
            jsondata = json.loads(request.body.decode('utf-8'))
            obj_inwardheader.action = jsondata.get('params').get('Action')
            obj_inwardheader.type = jsondata.get('params').get('Type')
            obj_inwardheader.inwardheader_json = jsondata.get('params').get('lj_filters')
            obj_inwardheader.entity_gid = decry_data(request.session['Entity_gid'])
            common.main_fun1(request.read(), path)
            df_preschedule = obj_inwardheader.get_inward()
            jdata = df_preschedule.to_json(orient='records')
            return JsonResponse(json.loads(jdata), safe=False)
        except Exception as e:
            return JsonResponse({"MESSAGE": "ERROR_OCCURED", "DATA": str(e)})

def get_inwardsummary_details(request):
    utl.check_pointaccess(request)
    utl.check_authorization(request)
    if request.method == 'POST':
        try:
            path = request.path
            obj_inwardheader = mInvoice.inward_model()
            jsondata = json.loads(request.body.decode('utf-8'))
            obj_inwardheader.action = jsondata.get('params').get('Action')
            obj_inwardheader.type = jsondata.get('params').get('Type')
            obj_inwardheader.inwardheader_json = jsondata.get('params').get('lj_filters')
            obj_inwardheader.entity_gid = int(decry_data(request.session['Entity_gid']))
            common.main_fun1(request.read(), path)
            df_preschedule = obj_inwardheader.get_inward_details()
            jdata = df_preschedule.to_json(orient='records')
            return JsonResponse(json.loads(jdata), safe=False)
        except Exception as e:
            return JsonResponse({"MESSAGE": "ERROR_OCCURED", "DATA": str(e)})

def invoice_crt(request):
    utl.check_authorization(request)
    return render(request,"inw_trn_invoice.html")


def employee_mst_data(request):
    utl.check_pointaccess(request)
    utl.check_authorization(request)
    if request.method == 'POST':
        try:
            path = request.path
            jsondata = json.loads(request.body.decode('utf-8'))
            grp = jsondata.get('params').get('Group')
            limit = jsondata.get('params').get('Limit')
            typ = jsondata.get('params').get('Type')
            sub = jsondata.get('params').get('Sub_Type')
            params = {"Group": grp, "Type": typ, "Sub_Type": sub, "Limit": limit}
            token = jwt.token(request)
            headers = {"content-type": "application/json", "Authorization": "" + token + ""}
            classify = {
                "CLASSIFICATION": {
                    "Entity_Gid": int(decry_data(request.session['Entity_gid']))
                }}
            jsondata['params']['json']['Params'].update(classify)
            datas = json.dumps(jsondata.get('params').get('json'))
            resp = requests.post("" + ip + "/MASTER_DATA", params=params, data=datas, headers=headers,
                                 verify=False)
            response = resp.content.decode("utf-8")
            return HttpResponse(response)
        except Exception as e:
            return JsonResponse({"MESSAGE": "ERROR_OCCURED", "DATA": str(e)})

def Courier_dtl(request):
    utl.check_pointaccess(request)
    utl.check_authorization(request)
    if request.method == 'POST':
        try:
            path = request.path
            Courier_dtl = mInvoice.inward_model()
            jsondata = json.loads(request.body.decode('utf-8'))
            Courier_dtl.courier_gid =jsondata.get('params').get('courier_gid')
            Courier_dtl.courier_name = jsondata.get('params').get('courier_name')
            Courier_dtl.entity_gid = int(decry_data(request.session['Entity_gid']))
            common.main_fun1(request.read(), path)
            data = Courier_dtl.get_courier()
            jdata = data.to_json(orient='records')
            return JsonResponse(json.loads(jdata), safe=False)
        except Exception as e:
            return JsonResponse({"MESSAGE": "ERROR_OCCURED", "DATA": str(e)})