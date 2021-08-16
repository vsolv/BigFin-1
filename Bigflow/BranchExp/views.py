from django.shortcuts import render
from django.db import connection
import pandas as pd
from django.http import JsonResponse, HttpResponse
import json
from Bigflow.Core.models import decrpt as decry_data
from Bigflow.BranchExp.model import mBranch as mbranch
import Bigflow.Core.jwt_file as jwt
import json
import numpy as np
import requests
import base64
import Bigflow.Core.models as common
from Bigflow.menuClass import utility as utl
token = common.token()
ip = common.localip()

def Branch_Template(request,template_name):
    template_name = template_name
    if template_name is not '':
        utl.check_authorization(request)
        return render(request, template_name+".html")

def outputReturn(tubledtl, index):
    temp = tubledtl[0].split(',')
    if (len(temp) > 1):
        if (index == 0):
            return int(temp[0])
        else:
            return temp[1]
    else:
        return temp[0]


def test(request):
    utl.check_pointaccess(request)
    utl.check_authorization(request)
    cursor = connection.cursor()
    parameters = ()
    cursor.callproc('apro', parameters)
    columns = [x[0] for x in cursor.description]
    rows = cursor.fetchall()
    rows = list(rows)
    grn_dtl = pd.DataFrame(rows, columns=columns)
    jdata = grn_dtl.to_json(orient='records')
    return JsonResponse(json.loads(jdata), safe=False)

def change_value(request):
    cursor = connection.cursor()
    jsondata = json.loads(request.body.decode('utf-8'))
    id = jsondata.get('id')
    parameters = (id)
    query = """update a_table set column3 = 'APPROVED' where id = %s"""
    cursor.execute(query, parameters)
    return JsonResponse(json.loads(""), safe=False)

def change_value_l(request):
    cursor = connection.cursor()
    jsondata = json.loads(request.body.decode('utf-8'))
    value = jsondata.get('value')
    sup = jsondata.get('status')
    parameters = (value,sup)
    query = """insert into a_table  (colmn1,column_id,column2,column3,suppl) values ('rent',3,'value',%s,%s)"""
    cursor.execute(query, parameters)
    parameters = (sup)
    query = """insert into a_table  (colmn1,column_id,column2,column3,suppl) values ('rent',6,'status','Pending',%s)"""
    cursor.execute(query, parameters)
    return JsonResponse(json.loads(""), safe=False)

def Get_expense(request):
    utl.check_pointaccess(request)
    utl.check_authorization(request)
    if request.method == 'POST':
        jsondata = json.loads(request.body.decode('utf-8'))
        if (jsondata.get('Group')) == 'EXPENSE_DATA':
            objgrp = jsondata.get('Group')
            objtyp = jsondata.get('Type')
            objsubtyp = jsondata.get('Sub_Type')
            entity_gid = int(decry_data(request.session['Entity_gid']))
            create_by = int(decry_data(request.session['Emp_gid']))
            jsondata["Params"]["CLASSIFICATION"] = {"Entity_Gid": entity_gid, "employee_gid": create_by}
            datas = json.dumps(jsondata)
            params = {'Group': "" + objgrp + "", 'Type': "" + objtyp + "", 'SubType': "" + objsubtyp + ""}
            token = jwt.token(request)
            headers = {"content-type": "application/json", "Authorization": "" + token + ""}
            datas = json.dumps(jsondata)
            resp = requests.post("" + ip + "/Expense_Process", params=params, data=datas, headers=headers,
                                 verify=False)
            response = resp.content.decode("utf-8")
            return HttpResponse(response)
        else:
            action = jsondata.get('params').get('action')
            type = jsondata.get('params').get('type')
            params = {'action':action, 'type': type}
            entity_gid = decry_data(request.session['Entity_gid'])
            jsondata["params"]["classification"] = {"Entity_Gid": entity_gid}
            create_by = int(decry_data(request.session['Emp_gid']))
            jsondata['params']['filter']["employee_gid"]=create_by
            token = jwt.token(request)
            headers = {"content-type": "application/json", "Authorization": "" + token + ""}
            datas = json.dumps(jsondata)
            result = requests.post("" + ip + "/Expense_Process", params=params, data=datas, headers=headers,
                                 verify=False)
            results = result.content.decode("utf-8")
            return JsonResponse(json.loads(results), safe=False)
    if request.method == 'GET':
        try:
            get_values = request.GET
            data = json.dumps(get_values)
            final_data = json.loads(data)
            action = final_data.get("action")
            sub_type = final_data.get("type")

            download_employee_gid = final_data.get("download_employee_gid")
            download_cr_number = final_data.get("download_cr_number")
            status = final_data.get("download_status")
            from_date = final_data.get("download_from_date")
            to_date = final_data.get("download_to_date")
            supplier_gid = final_data.get("download_supplier_gid")
            branch_gid = final_data.get("download_branch_gid")

            entity_gid = int(decry_data(request.session['Entity_gid']))
            employee_gid = int(decry_data(request.session['Emp_gid']))
            if (action == "GET"):
                try:
                    params = {'Type': action,"Group":"EXPENSE_DATA","SubType":sub_type}
                    entity_gid = decry_data(request.session['Entity_gid'])
                    jsondata = {"Params": {'Type': action, "SubType": sub_type,
                                           "FILTER": {"invoiceheader_crno": download_cr_number,
                                                      "employee_gid": download_employee_gid, "fromdate": from_date,
                                                      "todate": to_date, "invoiceheader_branchgid": branch_gid,
                                                      "supplier_gid": supplier_gid, "InvoiceHeader_Status": status},
                                           "CLASSIFICATION": {"Entity_Gid": entity_gid, "employee_gid": employee_gid}}}
                    token = jwt.token(request)
                    datas = json.dumps(jsondata)
                    headers = {"content-type": "application/json", "Authorization": "" + token + ""}
                    result = requests.post("" + ip + "/Expense_Process", params=params, data=datas, headers=headers,
                                           verify=False)
                    results = result.content.decode("utf-8")
                    results_data1=json.loads(results)
                    results_data2=results_data1.get("DATA")
                    df = pd.DataFrame(results_data2)
                    XLSX_MIME = 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
                    response = HttpResponse(content_type=XLSX_MIME)
                    response['Content-Disposition'] = 'attachment; filename="Expense_Report.xlsx"'
                    writer = pd.ExcelWriter(response, engine='xlsxwriter')
                    df_view = df
                    df_view['temp_var'] = ""
                    df_view['S_No'] = range(1, 1 + len(df_view))
                    final_df = df_view[
                        ['S_No','invoiceheader_invoiceno','trandate','invoiceheader_crno',
                         'invoiceheader_invoicedate','branch_code','invoicedetails_item','invoicedetails_desc',
                         'Supplier_code','supplier_branchname','supplier_gstno','supplier_panno',
                         'tcc_name','tbs_name','category_name','subcategory_name','invoiceheader_amount',
                         'invoiceheader_taxableamt', 'invoicedetails_igst', 'invoicedetails_cgst',
                         'invoicedetails_sgst', 'invoicedetails_hsncode','invoiceheader_deductionamount','invoiceheader_roundoff',
                         'employee_name','bankdetails_acno']]

                    final_df.columns = ['S. No','Invoice NO','Transaction Date','CR Number',
                                        'Invoice Date','Branch Code','Item','Description',
                                        'Supplier Code','Supplier Name','Supplier GST Number','Supplier PAN Number',
                                        'Cc','Bs','Category','Sub-category','Invoice Header Amount',
                                        'Invoce Taxable Amount','IGST','CGST',
                                        'SGST','HSNCODE','Deduction','Round-off',
                                        'Maker Name','Bank-accno']
                    final_df.to_excel(writer, index=False)
                    writer.save()
                    return response
                except Exception as e:
                    return JsonResponse({"MESSAGE": "ERROR_OCCURED", "DATA": str(e)})
        except Exception as e:
            return JsonResponse({"MESSAGE": "ERROR_OCCURED", "DATA": str(e)})

def Set_expense(request):
    utl.check_pointaccess(request)
    utl.check_authorization(request)
    if request.method == 'POST':
        try:
            jsondata = json.loads(request.body.decode('utf-8'))
            if (jsondata.get('Group')) == 'EXPENSE_DATA':
                objgrp = jsondata.get('Group')
                objtyp = jsondata.get('Type')
                objsubtyp = jsondata.get('Action')
                entity_gid = int(decry_data(request.session['Entity_gid']))
                Emp_gid = int(decry_data(request.session['Emp_gid']))
                jsondata["Params"]["CLASSIFICATION"] = {"Entity_Gid": entity_gid, "employee_gid": Emp_gid}
                params = {'Group': "" + objgrp + "", 'Type': "" + objtyp + "", 'Action': "" + objsubtyp + ""}
                token = jwt.token(request)
                headers = {"content-type": "application/json", "Authorization": "" + token + ""}
                datas = json.dumps(jsondata)
                resp = requests.post("" + ip + "/Expense_ProcessSet", params=params, data=datas, headers=headers,
                                     verify=False)
                response = resp.content.decode("utf-8")
                return HttpResponse(response)
        except Exception as e:
            return JsonResponse({"MESSAGE": "ERROR_OCCURED", "DATA": str(e)})


def insertNewBranchDetails(request):
    utl.check_pointaccess(request)
    utl.check_authorization(request)
    if request.method == 'POST':
        jsondata = json.loads(request.body.decode('utf-8'))
        type = jsondata.get('Type')
        sub_type = jsondata.get('Sub_Type')
        params = {'Type': type, 'Sub_Type': sub_type}
        entity_gid = decry_data(request.session['Entity_gid'])
        create_by = decry_data(request.session['Emp_gid'])
        jsondata["data"]["classification"] = {"Entity_Gid": entity_gid,"Create_by":create_by}
        datas = json.dumps(jsondata)
        if (jsondata.get('Type') == 'INSERT'):
            token = jwt.token(request)
            headers = {"content-type": "application/json", "Authorization": "" + token + ""}
            result = requests.post("" + ip + "/Br_Property_Proccess_Set", params=params, headers=headers, data=datas, verify=False)
            results = result.content.decode("utf-8")
            return JsonResponse(json.loads(results), safe=False)
        elif (jsondata.get('Type')) == 'update':
            token = jwt.token(request)
            headers = {"content-type": "application/json", "Authorization": "" + token + ""}
            result = requests.post("" + ip + "/Br_Property_Proccess_Set", params=params, headers=headers, data=datas,verify=False)
            results = result.content.decode("utf-8")
            return JsonResponse(json.loads(results), safe=False)


def brGetPropertyType(request):
    utl.check_pointaccess(request)
    utl.check_authorization(request)
    if request.method == 'POST':
        jsondata = json.loads(request.body.decode('utf-8'))
        if (jsondata.get('Type'))== 'PRODUCT':
            type = jsondata.get('Type')
            datas= json.dumps(jsondata.get('data'))
            entity_gid = decry_data(request.session['Entity_gid'])
            create_by = decry_data(request.session['Emp_gid'])
            params = {'Type': type,'entity_gid':entity_gid}
            token = jwt.token(request)
            headers = {"content-type": "application/json", "Authorization": "" + token + ""}
            result = requests.post("" + ip + "/Br_Property_Proccess_Get", params=params, headers=headers, data=datas,
                                   verify=False)
            results = result.content.decode("utf-8")
            return JsonResponse(json.loads(results), safe=False)

def brGetPropertyDetails(request):
    utl.check_pointaccess(request)
    utl.check_authorization(request)
    if request.method=='POST':
        jsondata=json.loads(request.body.decode('utf-8'))
        Type = jsondata.get('Type')
        Sub_Type = jsondata.get('Sub_Type')
        entity_gid = decry_data(request.session['Entity_gid'])
        create_by = decry_data(request.session['Emp_gid'])
        jsondata["data"]["classification"] = {"Entity_Gid": entity_gid, "Create_by": create_by}
        datas = json.dumps(jsondata)
        if(jsondata.get('Type'))=='PROPERTY':
            params = {'Type': Type, 'Sub_Type': Sub_Type}
            token = jwt.token(request)
            headers = {"content-type": "application/json", "Authorization": "" + token + ""}
            result = requests.post("" + ip + "/Br_Property_Proccess_Get", params=params,headers=headers,data=datas,verify=False)
            results = result.content.decode("utf-8")
            return JsonResponse(json.loads(results), safe=False)
        elif((jsondata.get("Type")=="GET") and (jsondata.get("Sub_Type")=="PROPERTY_BRANCH_MAPPING")):
            params = {'Type': Type, 'Sub_Type': Sub_Type}
            token = jwt.token(request)
            headers = {"content-type": "application/json", "Authorization": "" + token + ""}
            result = requests.post("" + ip + "/Br_Property_Proccess_Get", params=params, headers=headers, data=datas, verify=False)
            results = result.content.decode("utf-8")
            return JsonResponse(json.loads(results), safe=False)
        elif (jsondata.get('Type'))== 'PRODUCT':
            params = {'Type': Type,'entity_gid':entity_gid}
            new_filter=json.loads(datas)
            del new_filter["data"]["classification"]
            datas=json.dumps(new_filter)
            token = jwt.token(request)
            headers = {"content-type": "application/json", "Authorization": "" + token + ""}
            result = requests.post("" + ip + "/Br_Property_Proccess_Get", params=params, headers=headers, data=datas, verify=False)
            results = result.content.decode("utf-8")
            return JsonResponse(json.loads(results), safe=False)

def get_category_subcategory(request):
    utl.check_pointaccess(request)
    utl.check_authorization(request)
    if request.method == 'POST':
        jsondata = json.loads(request.body.decode('utf-8'))
        group = jsondata.get('Group')
        type = jsondata.get('Type')
        sub_type = jsondata.get('Sub_type')
        entity_gid = decry_data(request.session['Entity_gid'])
        create_by = decry_data(request.session['Emp_gid'])
        jsondata["data"]["Params"]["CLASSIFICATION"] = {"Entity_Gid": entity_gid}
        params = {'Group': "" + group + "", 'Type': "" + type + "", 'Sub_type': "" + sub_type + ""}
        token = jwt.token(request)
        headers = {"content-type": "application/json", "Authorization": "" + token + ""}
        datas = json.dumps(jsondata.get('data'))
        resp = requests.post("" + ip + "/ccbsapi", params=params, data=datas, headers=headers, verify=False)
        response = resp.content.decode("utf-8")
        return HttpResponse(response)

def get_branch(request):
    utl.check_pointaccess(request)
    utl.check_authorization(request)
    if request.method == 'POST':
        drop_m = {
            "Table_name": "gal_mst_tbranch",
            "Column_1": "branch_gid,branch_name,branch_code",
            "Column_2": "",
            "Where_Common": "branch",
            "Where_Primary": "",
            "Primary_Value": "",
            "Order_by": "name"
        }
        drop_table ={"data":drop_m}
        actn = 'FABRANCH'
        entity_gid = request.session['Entity_gid']
        params = {'Action':actn, 'Entity_Gid': entity_gid}
        token = jwt.token(request)
        headers = {"content-type": "application/json", "Authorization": "" + token + ""}
        datas = json.dumps(drop_table.get('data'))
        resp = requests.post("" + ip + "/All_Tables_Values_Get", params=params, data=datas, headers=headers,
                             verify=False)
        response = resp.content.decode("utf-8")
        return HttpResponse(response)

def task_number_one(request):
    utl.check_pointaccess(request)
    utl.check_authorization(request)
    cursor = connection.cursor()
    parameters = ('COLUMN', 'ECF_INSERT', '{}', 'Y',
 '{"Entity_Gid": ['+str(request.session['Entity_gid'])+']}', decry_data(request.session['Emp_gid']),  '')
    cursor.callproc('sp_APExpense_Set', parameters)
    cursor.execute('select @_sp_APExpense_Set_6')
    sp_out_message = cursor.fetchone()
    return HttpResponse(sp_out_message)


def get_BranchExp_Meta_Data(request):
    utl.check_pointaccess(request)
    utl.check_authorization(request)
    if request.method == 'POST':
        jsondata = json.loads(request.body.decode('utf-8'))
        action = jsondata.get('action')
        type = jsondata.get('type')
        entity_gid = request.session['Entity_gid']
        create_by = int(decry_data(request.session['Emp_gid']))
        if action == "GET" and type == "Branch_Exp_Commodity_Level":
            table_data = {
                "Table_name": "gal_mst_tmetadata",
                "Column_1": "metadata_value,metadata_gid",
                "Column_2": "",
                "Where_Common": "metadata",
                "Where_Primary": "columnname",
                "Primary_Value": "branchexpense_approvallevel",
                "Order_by": "columnname"
            }
            params = {'Action': action, 'Entity_Gid': entity_gid}
            table = {"data": table_data}
            token = jwt.token(request)
            headers = {"content-type": "application/json", "Authorization": "" + token + ""}
            datas = json.dumps(table.get('data'))
            resp = requests.post("" + ip + "/All_Tables_Values_Get", params=params, data=datas, headers=headers,
                                 verify=False)
            response = resp.content.decode("utf-8")
            return HttpResponse(response)

def Session_Set_Expense_Data(request):
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
            return HttpResponse("SUCCESS")

def Session_Get_Expnese_Data(request):
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
            return JsonResponse(data, safe=False)

def Set_premises(request):
    utl.check_pointaccess(request)
    utl.check_authorization(request)
    if request.method == 'POST':
        jsondata = json.loads(request.body.decode('utf-8'))
        if (jsondata.get('group')) == 'PREMISES':
            try:
                group = jsondata.get('group')
                action = jsondata.get('action')
                type = jsondata.get('type')
                entity_gid = int(decry_data(request.session['Entity_gid']))
                create_by = int(decry_data(request.session['Emp_gid']))
                jsondata["classification"] = {"Entity_Gid": entity_gid, "Create_by": create_by}
                params = {'group':group , 'action': action ,'type':type,'create_by':create_by}
                token = jwt.token(request)
                headers = {"content-type": "application/json", "Authorization": "" + token + ""}
                datas = json.dumps(jsondata)
                resp = requests.post("" + ip + "/Premises_Process_Set", params=params, data=datas, headers=headers,
                                     verify=False)
                response = resp.content.decode("utf-8")
                return HttpResponse(response)

            except Exception as e:
                common.logger.error(e)
                return JsonResponse({"MESSAGE": "ERROR_OCCURED", "DATA": str(e)})

def Get_premises(request):
    utl.check_pointaccess(request)
    utl.check_authorization(request)
    if request.method == 'POST':
        jsondata = json.loads(request.body.decode('utf-8'))
        if (jsondata.get('group')) == 'PREMISES':
            try:
                group = jsondata.get('group')
                action = jsondata.get('action')
                type = jsondata.get('type')
                entity_gid = int(decry_data(request.session['Entity_gid']))
                create_by = int(decry_data(request.session['Emp_gid']))
                jsondata["classification"] = {"Entity_Gid": entity_gid, "Create_by": create_by}
                params = {'group':group , 'action': action ,'type':type,'create_by':create_by}
                token = jwt.token(request)
                headers = {"content-type": "application/json", "Authorization": "" + token + ""}
                datas = json.dumps(jsondata)
                resp = requests.post("" + ip + "/Premises_Process_Get", params=params, data=datas, headers=headers,
                                     verify=False)
                results = resp.content.decode("utf-8")
                return JsonResponse(json.loads(results), safe=False)

            except Exception as e:
                common.logger.error(e)
                return JsonResponse({"MESSAGE": "ERROR_OCCURED", "DATA": str(e)})

import logging
import threading
import time
import subprocess
import sys

# def thread_testing(request):
#     if request.method == 'POST':
#         jsondata = json.loads(request.body.decode('utf-8'))
#         for i in range(50):
#             x = threading.Thread(target=insert_temp(request), args=(1,))
#             pass
# def insert_temp(request):
#     jsondata = json.loads(request.body.decode('utf-8'))
#     exp_process = mbranch.BranchExp_model()
#     exp_process.type = jsondata.get("Type")
#     exp_process.sub_type = jsondata.get("Sub_Type")
#     exp_process.filters = json.dumps(jsondata.get("data").get('params').get("filters"))
#     exp_process.classification = json.dumps({"Entity_Gid": 1, "Create_by": 5})
#     result = exp_process.property_set()
#     # print(result)

