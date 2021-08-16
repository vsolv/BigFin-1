from django.shortcuts import render
from rest_framework.response import Response
from django.db import connection
import pandas as pd
from django.http import JsonResponse, HttpResponse
import json
import Bigflow.Core.jwt_file as jwt
from Bigflow.BranchExp.model import mBranch as mbranch
import numpy as np
import requests
import base64
import Bigflow.Core.models as common
from Bigflow.Core.models import decrpt as decry_data
import Bigflow.API.view_sales as view_sales
token = common.token()
ip = common.localip()
from Bigflow.menuClass import utility as utl

def Service_Management_Template(request,template_name):
    template_name = template_name
    if template_name is not '':
        utl.check_authorization(request)
        return render(request, template_name+".html")

# def amc_Maker_Summary(request):
#     return render(request, "SM_AMC_Maker_Summary.html")


def get_Service_Management(request):
    utl.check_pointaccess(request)
    utl.check_authorization(request)
    if request.method == 'POST':
        jsondata = json.loads(request.body.decode('utf-8'))
        type=jsondata.get('params').get('type')
        sub_type=jsondata.get('params').get('sub_type')
        entity_gid = int(decry_data(request.session['Entity_gid']))
        create_by = int(decry_data(request.session['Emp_gid']))
        jsondata["classification"] = {"Entity_Gid": entity_gid,"Emp_gid":create_by}
        datas = json.dumps(jsondata)

        if (type == 'Suppplier' and sub_type=='DROPDOWN'):
            params = {'type': type, 'sub_type': sub_type}
            token = jwt.token(request)
            headers = {"content-type": "application/json", "Authorization": "" + token + ""}
            result = requests.post("" + ip + "/Get_Service_Management_Api", params=params, headers=headers, data=datas, verify=False)
            results = result.content.decode("utf-8")
            return JsonResponse(json.loads(results), safe=False)
        elif (type=="Mode" and sub_type=="Summary"):
            params = {'type': type, 'sub_type': sub_type}
            token = jwt.token(request)
            headers = {"content-type": "application/json", "Authorization": "" + token + ""}
            result = requests.post("" + ip + "/Get_Service_Management_Api", params=params, headers=headers, data=datas,
                                   verify=False)
            results = result.content.decode("utf-8")
            return JsonResponse(json.loads(results), safe=False)
        else:
            params = {'type': type, 'sub_type': sub_type}
            token = jwt.token(request)
            headers = {"content-type": "application/json", "Authorization": "" + token + ""}
            result = requests.post("" + ip + "/Get_Service_Management_Api", params=params, headers=headers, data=datas,
                                   verify=False)
            results = result.content.decode("utf-8")
            return JsonResponse(json.loads(results), safe=False)

def set_Service_Management(request):
    utl.check_pointaccess(request)
    utl.check_authorization(request)
    if request.method == 'POST':
        jsondata = json.loads(request.body.decode('utf-8'))
        jsondata1= json.loads(request.body.decode('utf-8'))
        action=jsondata.get('params').get('action')
        type=jsondata.get('params').get('type')
        entity_gid = int(decry_data(request.session['Entity_gid']))
        create_by = decry_data(request.session['Emp_gid'])
        jsondata["params"]["classification"] = {"Entity_Gid": entity_gid}
        datas = json.dumps(jsondata)
        datas1=json.dumps(jsondata1)

        if (action == 'INSERT' and (type=='INSERT_TICKET_HEADER_DETAIL' or type=="INSERT_ERROR_CATEGORY")):
            if(type=='INSERT_TICKET_HEADER_DETAIL'):
                datas=json.loads(datas)
                datas["params"]["filter"]["TicketHeader_AssignedTo"]=create_by
                datas = json.dumps(datas)
            params = {'action': action, 'type': type,'create_by':create_by}
            token = jwt.token(request)
            headers = {"content-type": "application/json", "Authorization": "" + token + ""}
            result = requests.post("" + ip + "/Set_Service_Management_Api", params=params, headers=headers, data=datas, verify=False)
            results = result.content.decode("utf-8")
            return JsonResponse((results), safe=False)
        elif (action == 'INSERT' and type=='INSERT_FOLLOWUP'):
            params = {'action': action, 'type': type,'create_by':create_by}
            token = jwt.token(request)
            headers = {"content-type": "application/json", "Authorization": "" + token + ""}
            result = requests.post("" + ip + "/Set_Service_Management_Api", params=params, headers=headers, data=datas, verify=False)
            results = result.content.decode("utf-8")
            return JsonResponse((results), safe=False)
        elif (action == 'insert' and type=='PR_DETAILS_INSERT'):
            params = {'action': action, 'type': type,'create_by':create_by,"entity_gid":entity_gid}
            token = jwt.token(request)
            headers = {"content-type": "application/json", "Authorization": "" + token + ""}
            result = requests.post("" + ip + "/Pr_Detail_Set_Api", params=params, headers=headers, data=datas1, verify=False)
            results = result.content.decode("utf-8")
            return HttpResponse(results)

def sms_File_Upload(request):
    utl.check_pointaccess(request)
    utl.check_authorization(request)
    if request.method == 'POST' or request.FILES['file']:
        dd = base64.b64encode(request.FILES['file'].read())
        file = dd.decode("utf-8")
        name = request.POST['name']
        base = {'name':name,'file':file}
        return JsonResponse(base)

def category_data(request):
    utl.check_pointaccess(request)
    utl.check_authorization(request)
    if request.method == 'POST':
        jsondata = json.loads(request.body.decode('utf-8'))
        action = jsondata.get('params').get('action')
        type=jsondata.get('params').get('type')
        sub_type = jsondata.get('params').get('sub_type')
        entity_gid = request.session['Entity_gid']
        create_by = request.session['Emp_gid']
        if type=="Mode" and sub_type=="Summary":
            table_data ={
                "Table_name":"fa_mst_tassetcat",
                "Column_1":"assetcat_gid,assetcat_subcatname",
                "Column_2":"",
                "Where_Common":"assetcat",
                "Where_Primary":"",
                "Primary_Value":"",
                "Order_by":"subcatname"
               }
            table ={"data":table_data}
            action ='FACAT'
        elif type=="Branch" and sub_type=="Summary":
            table_data = {
                "Table_name": "gal_mst_tbranch",
                "Column_1": "branch_gid,branch_name",
                "Column_2": "",
                "Where_Common": "branch",
                "Where_Primary": "",
                "Primary_Value": "",
                "Order_by": "name"
            }
            table = {"data": table_data}
            action = 'FABRANCH'
        params = {'Action':action, 'Entity_Gid': entity_gid}
        token = jwt.token(request)
        headers = {"content-type": "application/json", "Authorization": "" + token + ""}
        table_values=table.get('data')
        datas = json.dumps(table.get('data'))
        resp = requests.post("" + ip + "/All_Tables_Values_Get", params=params, data=datas, headers=headers,
                             verify=False)
        response = resp.content.decode("utf-8")
        return HttpResponse(response)

def Get_All_Table_Metadata(request):
    utl.check_pointaccess(request)
    utl.check_authorization(request)
    if request.method == 'POST':
        jsondata = json.loads(request.body.decode('utf-8'))
        action = jsondata.get('params').get('action')
        type=jsondata.get('params').get('type')
        sub_type = jsondata.get('params').get('sub_type')
        entity_gid = int(decry_data(request.session['Entity_gid']))
        create_by = int(decry_data(request.session['Emp_gid']))
        if action=="Get" and type=="Metadata" and sub_type=="Service_Period":
            table_data ={
                        "Table_name":"gal_mst_tmetadata",
                        "Column_1":"metadata_value",
                        "Column_2":"",
                        "Where_Common":"metadata",
                        "Where_Primary":"columnname",
                        "Primary_Value":"amcheader_serviceperiod",
                        "Order_by":"columnname"
                        }
            table ={"data":table_data}
            action ='METADATA'

        if action == "Get" and type == "Metadata" and sub_type == "BS_DATA":
            table_data = {
                "Table_name": "ap_mst_tbs",
                "Column_1": "tbs_code,tbs_gid,tbs_name",
                "Column_2": "",
                "Where_Common": "tbs",
                "Where_Primary": "",
                "Primary_Value": "",
                "Order_by": "gid"
            }
            table = {"data": table_data}

        if action == "Get" and type == "Metadata" and sub_type == "CC_DATA":
            filter = jsondata.get('params').get('filter')
            bs_gid=filter.get('bs_gid');
            table_data = {
                "Table_name": "ap_mst_tcc",
                "Column_1": "tcc_gid,tcc_code,tcc_name",
                "Column_2": "",
                "Where_Common": "tcc",
                "Where_Primary": "bsgid",
                "Primary_Value": bs_gid,
                "Order_by": "gid"
            }
            table = {"data": table_data}

        if action == "Get" and type == "Metadata" and sub_type == "Pro_Category":
            table_data={"Table_name": "gal_mst_tproductcategory",
                        "Column_1": "productcategory_gid,productcategory_clientgid,productcategory_code,productcategory_name",
                        "Column_2": "", "Where_Common": "productcategory", "Where_Primary": "", "Primary_Value":"", "Order_by": "gid"
                        }
            table = {"data": table_data}

        if action == "Get" and type == "Metadata" and sub_type == "Pro_Category_Type":
            filter = jsondata.get('params').get('filter')
            productcategory_gid = filter.get('productcategory_gid');
            table_data={"Table_name": "gal_mst_tproducttype","Column_1": "producttype_gid,producttype_productcategory_gid,"
                        "producttype_code,producttype_name","Column_2": "", "Where_Common": "producttype",
                        "Where_Primary":"productcategory_gid", "Primary_Value":productcategory_gid, "Order_by": "gid"
                        }
            table = {"data": table_data}

        if action == "Get" and type == "Metadata" and sub_type == "Property_Type":
            table_data={"Table_name": "ap_mst_tproperty","Column_1": "property_gid,property_code,property_name,property_type",
                        "Column_2": "", "Where_Common": "property", "Where_Primary":"", "Primary_Value":"", "Order_by": "gid"
                        }
            table = {"data": table_data}

        if action == "Get" and type == "Metadata" and sub_type == "GET_BRANCH":
            action="";
            table_data={"Table_name": "gal_mst_tbranch","Column_1": "branch_gid,branch_code,branch_name","Column_2": "",
                        "Where_Common": "branch","Where_Primary": "","Primary_Value": "","Order_by": "gid"}
            table = {"data": table_data}

        params = {'Action':action, 'Entity_Gid': entity_gid}
        token = jwt.token(request)
        headers = {"content-type": "application/json", "Authorization": "" + token + ""}
        datas = json.dumps(table.get('data'))
        resp = requests.post("" + ip + "/All_Tables_Values_Get_Metadata", params=params, data=datas, headers=headers,
                             verify=False)
        response = resp.content.decode("utf-8")
        return HttpResponse(response)

def set_AMC_Details(request):
    utl.check_pointaccess(request)
    utl.check_authorization(request)
    if request.method == 'POST':
        jsondata = json.loads(request.body.decode('utf-8'))
        action=jsondata.get('params').get('action')
        type=jsondata.get('params').get('type')
        entity_gid = int(decry_data(request.session['Entity_gid']))
        create_by = int(decry_data(request.session['Emp_gid']))
        jsondata["params"]["classification"] = {"Entity_Gid": entity_gid,"Entity_Detail_Gid":1}
        datas = json.dumps(jsondata)
        params = {'action': action, 'type': type,'create_by':create_by}
        token = jwt.token(request)
        headers = {"content-type": "application/json", "Authorization": "" + token + ""}
        result = requests.post("" + ip + "/Set_AMC_Details_Api", params=params, headers=headers, data=datas, verify=False)
        results = result.content.decode("utf-8")
        return JsonResponse((results), safe=False)

def get_AMC_Details(request):
    utl.check_pointaccess(request)
    utl.check_authorization(request)
    if request.method == 'POST':
        jsondata = json.loads(request.body.decode('utf-8'))
        action=jsondata.get('params').get('action')
        type=jsondata.get('params').get('type')
        entity_gid = int(decry_data(request.session['Entity_gid']))
        create_by = int(decry_data(request.session['Emp_gid']))
        jsondata["params"]["classification"] = {"Entity_Gid": entity_gid,"Entity_Detail_Gid":1}
        datas = json.dumps(jsondata)
        params = {'action': action, 'type': type,'create_by':create_by}
        token = jwt.token(request)
        headers = {"content-type": "application/json", "Authorization": "" + token + ""}
        result = requests.post("" + ip + "/Get_AMC_Details_Api", params=params, headers=headers, data=datas, verify=False)
        results = result.content.decode("utf-8")
        return JsonResponse(json.loads(results), safe=False)

def Get_Employee_Data(request):
        utl.check_pointaccess(request)
        utl.check_authorization(request)
        if request.method == 'GET':
            try:
                table_name = 'employee'
                entity_gid = int(decry_data(request.session['Entity_gid']))
                create_by = int(decry_data(request.session['Emp_gid']))
                gid = 0
                params = {'table_name': table_name, 'entity_gid': entity_gid, 'gid': gid}
                token = jwt.token(request)
                datas = json.dumps({"Entity_Gid":entity_gid})
                headers = {"content-type": "application/json", "Authorization": "" + token + ""}
                result = requests.post("" + ip + "/All_Tables_Values_Get_Data", params=params, headers=headers,data=datas,verify=False)
                results = result.content.decode("utf-8")
                return JsonResponse(json.loads(results), safe=False)
            except Exception as e:
                return JsonResponse({"MESSAGE": "ERROR_OCCURED", "DATA": str(e)})

def Session_Set_SMS_Data(request):
    utl.check_pointaccess(request)
    utl.check_authorization(request)
    if request.method == 'POST':
        jsondata = json.loads(request.body.decode('utf-8'))
        action = jsondata.get('action')
        type = jsondata.get('type')
        session_key_values=jsondata.get("filter")
        if action == "SET":
            for (k, v) in session_key_values.items():
                request.session[k] = v
                print(k,v)
            return HttpResponse("SUCCESS")

def Session_Get_SMS_Data(request):
        utl.check_pointaccess(request)
        utl.check_authorization(request)
        if request.method == 'POST':
            jsondata = json.loads(request.body.decode('utf-8'))
            action = jsondata.get('action')
            type = jsondata.get('type')
            session_keys=jsondata.get("filter")
            data={}
            if action == "GET":
                for (k, v) in session_keys.items():
                    data[k]=request.session[k]
                    print(k,v)
            return JsonResponse(data, safe=False)