from django.shortcuts import render
from rest_framework.response import Response
from django.db import connection
import pandas as pd
from django.http import JsonResponse, HttpResponse
import json
from Bigflow.Core.models import decrpt as decry_data
import numpy as np
import requests
import base64
import Bigflow.Core.models as common
from Bigflow.menuClass import utility as utl
import Bigflow.Core.jwt_file as jwt
token = common.token()
ip = common.localip()
from Bigflow.JV.Model import mJV
from Bigflow.Core import views as master_views
import pandas

def JV_Templates(request,template_name):
    template_name = template_name
    if template_name is not '':
        utl.check_authorization(request)
        return render(request, template_name+".html")


def JV_Process_Set(request):
    utl.check_pointaccess(request)
    utl.check_authorization(request)
    if request.method == 'POST':
        jsondata = json.loads(request.body.decode('utf-8'))
        action=jsondata.get('action')
        type=jsondata.get('type')
        entity_gid=int(decry_data(request.session['Entity_gid']))
        create_by = int(decry_data(request.session['Emp_gid']))
        jsondata["classification"] = {"entity_gid": entity_gid,"entity_detailsgid":1}
        datas = json.dumps(jsondata)
        token = jwt.token(request)
        params = {'action': action, 'type': type,'create_by':create_by}
        headers = {"content-type": "application/json", "Authorization": "" + token + ""}
        result = requests.post("" + ip + "/JV_Process_Set_API", params=params, headers=headers, data=datas, verify=False)
        results = result.content.decode("utf-8")
        return JsonResponse((results), safe=False)

def JV_Accounting_Entry_Data(request):
    utl.check_pointaccess(request)
    utl.check_authorization(request)
    if request.method == 'GET':
        try:
            get_values = request.GET
            data = json.dumps(get_values)
            final_data = json.loads(data)
            cr_number = final_data.get("download_cr_number")
            from_date = final_data.get("download_from_date")
            to_date = final_data.get("download_to_date")
            if cr_number == None:
                cr_number = ""
            if from_date == None:
                from_date = ""
            if to_date == None:
                to_date = ""
            jsondata = {'action': 'GET','type': 'JV_ENTRY',
                        'filter': {"entry_refno": cr_number, "fromdate": from_date, "todate": to_date,
                                   "Page_Index": 0, "Page_Size": 100000}}
            action = jsondata.get('action')
            type = jsondata.get('type')
            if (action == "GET" and type == "JV_ENTRY"):
                entity_gid = int(decry_data(request.session['Entity_gid']))
                XLSX_MIME = 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
                response = HttpResponse(content_type=XLSX_MIME)
                response['Content-Disposition'] = 'attachment; filename="Accountin_Entry_Data.xlsx"'
                writer = pd.ExcelWriter(response, engine='xlsxwriter')
                jsondata["classification"] = {"Entity_Gid": entity_gid}
                datas = json.dumps(jsondata)
                params = {'action': action, 'type': type}
                token = jwt.token(request)
                headers = {"content-type": "application/json", "Authorization": "" + token + ""}
                result = requests.post("" + ip + "/JV_Process_Get_API", params=params, headers=headers, data=datas,
                                       verify=False)
                results = result.content.decode("utf-8")
                df=json.loads(results)
                df = pd.DataFrame(df)
                final_df = df[
                    ['entry_refno', 'entry_transactiondate', 'entry_gl', 'gl_name', 'entry_amt', 'entry_type',
                     'branch_name', 'entry_module']]
                final_df.columns = ['ENTRY_REFNO', 'ENTRY_TRANSACTION_DATE', 'ENTRY_GL', 'ENTRY_GL_NAME',
                                    'ENTRY_AMOUNT', 'ENTRY_TYPE', 'BRANCH_NAME', 'ENTRY_MODULE']
                final_df.to_excel(writer, index=False)
                writer.save()
                return response
        except Exception as e:
            return JsonResponse({"MESSAGE": "ERROR_OCCURED", "DATA": str(e)})

def JV_Process_Get(request):
    utl.check_pointaccess(request)
    utl.check_authorization(request)
    if request.method == 'POST':
        try:
            jsondata = json.loads(request.body.decode('utf-8'))
            action=jsondata.get('action')
            type=jsondata.get('type')
            entity_gid = int(decry_data(request.session['Entity_gid']))
            create_by = int(decry_data(request.session['Emp_gid']))
            if(action=="GET" and (type=="JV_HEADER_SUMMARY" or type=="JV_DETAILS" or
                                  type=="FIND_AP_CR_NUMBER" or type=="FIND_JV_CR_NUMBER" or type=="JV_TRANS_GET")):
                jsondata["classification"] = {"Entity_Gid": entity_gid}
                datas = json.dumps(jsondata)
                params = {'action': action, 'type': type,'create_by':create_by}
                token = jwt.token(request)
                headers = {"content-type": "application/json", "Authorization": "" + token + ""}
                result = requests.post("" + ip + "/JV_Process_Get_API", params=params, headers=headers, data=datas, verify=False)
                results = result.content.decode("utf-8")
                return JsonResponse(json.loads(results), safe=False)
        except Exception as e:
            return JsonResponse({"MESSAGE": "ERROR_OCCURED", "DATA": str(e)})
def JV_Upload_Data(request):
    utl.check_pointaccess(request)
    utl.check_authorization(request)
    if request.method == 'POST' and request.FILES['file']:
        try:
            entity_gid = int(decry_data(request.session['Entity_gid']))
            create_by = int(decry_data(request.session['Emp_gid']))
            xl_column_name=[]
            Credit_amount=0;
            Debit_amount=0;
            column_name=["EntryType","Branch","Category","Subcategory","BS","CC","CBSGL",
                         "Description","Amount"]
            excel_data_df = pandas.read_excel(request.FILES['file'])
            filtered_df=excel_data_df.drop(columns=['Description'])
            xl_column_name=list(excel_data_df.columns.values)
            if(column_name==xl_column_name):
                if (filtered_df.isnull().values.any()):
                    return JsonResponse(
                        {"MESSAGE": "ERROR_OCCURED", "DATA": "SOME COLUMN IS NULL VALUES"})
                else:
                    Credit_amount = round(excel_data_df.loc[excel_data_df['EntryType'] == 'C', 'Amount'].sum(),2)
                    Debit_amount = round(excel_data_df.loc[excel_data_df['EntryType'] == 'D', 'Amount'].sum(),2)
                    if (Credit_amount == Debit_amount):
                        jdata = excel_data_df.to_json(orient='records')
                        data=json.loads(jdata)
                        data={"detail":data}
                        token = jwt.token(request)
                        datas = json.dumps({"filter":data, "classification": {"Entity_Gid": entity_gid}})
                        params = {'action': "GET", 'type': "JV_FIND_ALL", 'create_by': create_by}
                        try:
                            headers = {"content-type": "application/json", "Authorization": "" + token + ""}
                            result = requests.post("" + ip + "/JV_Process_Get_API", params=params,
                                                   headers=headers,data=datas, verify=False)
                            results = result.content.decode("utf-8")
                            return JsonResponse(json.loads(results), safe=False)
                        except Exception as e:
                            return JsonResponse({"MESSAGE": "ERROR_OCCURED", "DATA": str(e)})
                    else:
                        return JsonResponse(
                            {"MESSAGE": "ERROR_OCCURED", "DATA": "CREDIT AMOUNT AND DEBIT AMOUNT NOT EQUAL"})
            else:
                return JsonResponse({"MESSAGE": "ERROR_OCCURED","DATA":"COLUMN NOT MATCH"})

        except Exception as e:
            return JsonResponse({"MESSAGE": "ERROR_OCCURED", "DATA": str(e)})

def call_JV_Get(params,datas,token):
    try:
        headers = {"content-type": "application/json", "Authorization": "" + token + ""}
        result = requests.post("" + ip + "/JV_Process_Get_API", params=params, headers=headers,
                               data=datas, verify=False)
        results = result.content.decode("utf-8")
        results_data = json.loads(results)
        return results_data
    except Exception as e:
        return JsonResponse({"MESSAGE": "ERROR_OCCURED", "DATA": str(e)})



def jv_get_all_table_metadata_value(request):
    utl.check_pointaccess(request)
    utl.check_authorization(request)
    if request.method == 'POST':
        jsondata = json.loads(request.body.decode('utf-8'))
        action = jsondata.get('action')
        type=jsondata.get('type')
        sub_type = jsondata.get('sub_type')
        entity_gid = request.session['Entity_gid']
        if action=="Get" and type=="JV_Type":
            table_data ={"Table_name": "gal_mst_tmetadata",
                         "Column_1": "metadata_value,metadata_gid",
                         "Column_2": "", "Where_Common": "metadata",
                         "Where_Primary": "columnname",
                         "Primary_Value": "jventry_type",
                         "Order_by": "columnname"
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

def JV_Session_Set(request):
    utl.check_pointaccess(request)
    utl.check_authorization(request)
    if request.method == 'POST':
        jsondata = json.loads(request.body.decode('utf-8'))
        action = jsondata.get('action')
        type = jsondata.get('type')
        session_key_values=jsondata.get("filter")
        if action == "SET" and type == "JV_DATA":
            for (k, v) in session_key_values.items():
                request.session[k] = v
            return HttpResponse("SUCCESS")

def JV_Session_Get(request):
    utl.check_pointaccess(request)
    utl.check_authorization(request)
    if request.method == 'POST':
        jsondata = json.loads(request.body.decode('utf-8'))
        action = jsondata.get('action')
        type = jsondata.get('type')
        session_keys = jsondata.get("filter")
        data = {}
        if action == "GET" and type == "JV_DATA":
            for (k, v) in session_keys.items():
                data[k] = request.session[k]
                if(k=="Emp_gid"):
                    data[k] = int(decry_data(request.session['Emp_gid']))
        return JsonResponse(data, safe=False)

def JV_Approve(request):
    if request.method == 'POST':
        try:
            jsondata = json.loads(request.body.decode('utf-8'))
            action = jsondata.get('action')
            type = jsondata.get('type')
            entity_gid = int(decry_data(request.session['Entity_gid']))
            create_by = int(decry_data(request.session['Emp_gid']))
            if(action=="UPDATE" and type=="APPROVE"):
                jv_Object = mJV.JV()
                jv_Object.action = "INSERT"
                jv_Object.type = "JV_ENTRY"
                jv_Object.filter = json.dumps(jsondata.get("filter"))
                remark=jsondata.get("filter").get("remark")
                jv_Object.classification = json.dumps({"entity_gid": entity_gid,"entity_detailsgid":1})
                jv_Object.create_by = create_by
                employee_gid = create_by
                JV_Header_Gid=jsondata.get("filter").get("jventry_gid")
                JV_Entry_Type=jsondata.get("filter").get("jventry_type")
                JV_Entry_Ref_Number=jsondata.get("filter").get("jventry_refno")
                JV_Header_Amount=jsondata.get("filter").get("jventry_amount")
                out_put_data = jv_Object.jv_process_set_model()
                out_data = out_put_data.get("MESSAGE")
                result_data = out_data[0]
                if (result_data == "SUCCESS" or result_data=="ALREADY INSERTED"):
                    try:
                        jv_Object.action = "GET"
                        jv_Object.type = "AP_ENTER_DETAIL_GET"
                        CR_NO = jsondata.get('filter').get('JV_CR_Number')
                        jv_Object.filter = json.dumps({"entry_refno": CR_NO, "entry_module": "JV"})
                        jv_Object.classification = json.dumps({"Entity_Gid": entity_gid})
                        datas = jv_Object.get_bank_details()
                        Fund_Transfer_Dtls_data = datas.get("entry_detail")[0]
                        Fund_Transfer_Dtls_data = json.loads(Fund_Transfer_Dtls_data)

                        orginal_data_frame = pd.DataFrame(Fund_Transfer_Dtls_data.get("Fund_Transfer_Dtls"))
                        data_frame = pd.DataFrame(Fund_Transfer_Dtls_data.get("Fund_Transfer_Dtls"))

                        data_frame['Amount'] = data_frame['Amount'].astype(float)
                        Credit_amount = data_frame.loc[data_frame['Cr_Dr_Flag'] == 'C', 'Amount'].sum()
                        Debit_amount = data_frame.loc[data_frame['Cr_Dr_Flag'] == 'D', 'Amount'].sum()
                        Credit_amount = str(round(float(Credit_amount), 2))
                        Debit_amount = str(round(float(Debit_amount), 2))
                        if (Credit_amount == Debit_amount):
                            Unique_Values = data_frame.Entry_refno.unique()
                            Unique_Values_Length = len(Unique_Values)
                            Final_Unique_Values = []
                            for i in range(len(Unique_Values)):
                                Single_Unique_Values = Unique_Values[i]
                                Fetched_values = data_frame[(data_frame['Entry_refno'] == Single_Unique_Values)]
                                Final_send_data = orginal_data_frame[
                                    (orginal_data_frame['Entry_refno'] == Single_Unique_Values)]

                                send_Credit_amount = Fetched_values.loc[
                                    Fetched_values['Cr_Dr_Flag'] == 'C', 'Amount'].sum()
                                send_Debit_amount = Fetched_values.loc[
                                    Fetched_values['Cr_Dr_Flag'] == 'D', 'Amount'].sum()
                                send_Credit_amount = str(round(float(send_Credit_amount), 2))
                                send_Debit_amount = str(round(float(send_Debit_amount), 2))

                                if (send_Credit_amount == send_Debit_amount):

                                    send_data = Final_send_data.to_json(orient='records')
                                    send_data = json.loads(send_data)

                                    branch_code = Fund_Transfer_Dtls_data.get("Fund_Transfer_Dtls")[0].get("Brn_Code")
                                    CBSDATE = ""
                                    NEFT_ACCOUNT_NUMBER = ""
                                    # CBSDATE=Fund_Transfer_Dtls_data.get("Fund_Transfer_Dtls")[0].get("CBSDATE")
                                    try:
                                        # pass
                                        CBSDATE_DATA = str(common.get_server_date("GET_CBSDATE_ACCOUNT_NUMBER")[0])
                                        CBSDATE_DATA_LIST = CBSDATE_DATA.split(",")
                                        NEFT_ACCOUNT_NUMBER = CBSDATE_DATA_LIST[0]
                                        CBSDATE = CBSDATE_DATA_LIST[1]
                                    except Exception as e:
                                        common.logger.error(e)
                                        return JsonResponse(
                                            {"MESSAGE": "ERROR_OCCURED_ON_CBSDATE_AND_ACCOUNT_NUMBER_GET",
                                             "DATA": str(e)})

                                    try:
                                        token_status = 1
                                        generated_token_data = master_views.master_sync_Data_("GET", "get_data",
                                                                                              employee_gid)
                                        log_data = generated_token_data
                                        token = generated_token_data.get("DATA")[0].get("clienttoken_name")
                                        if (token == " " or token == None):
                                            token_status = 0
                                        if token_status == 1:
                                            try:
                                                data = {"Src_Channel": "EMS", "ApplicationId": Single_Unique_Values,
                                                        "TransactionBranch": branch_code, "Txn_Date": CBSDATE,
                                                        "productType": "DP", "Fund_Transfer_Dtls": send_data}
                                                data = json.dumps(data)
                                                log_data = [{"BEFORE_AMOUNT_TRANSFER_API_DATA": data}]
                                                common.logger.error(log_data)

                                                client_api = common.clientapi()
                                                headers = {"Content-Type": "application/json",
                                                           "Authorization": "Bearer " + token}
                                                result = requests.post("" + client_api + "/nbfc/v1/mwr/amount-transfer",
                                                                       headers=headers, data=data, verify=False)
                                                results = result.content.decode("utf-8")
                                                results_data = json.loads(results)
                                                log_data = [{"AFTER_AMOUNT_TRANSFER_API_DATA": results_data}]
                                                common.logger.error(log_data)

                                                ErrorStatus = results_data.get("CbsStatus")[0].get("ErrorMessage")
                                                ErrorCode = results_data.get("CbsStatus")[0].get("ErrorCode")
                                                if (ErrorStatus == "Success" and ErrorCode == '0'):
                                                    CBSReferenceNo = results_data.get("CbsStatus")[0].get(
                                                        "CBSReferenceNo")
                                                    try:
                                                        count_values = i + 1
                                                        Final_status = "ENTRY"
                                                        count_values = i + 1
                                                        Final_status = "ENTRY"
                                                        if (count_values == len(Unique_Values)):
                                                            Final_status = "APPROVED"
                                                        jv_Object.action = "INSERT"
                                                        jv_Object.type = "JV_ENTRY_UPDATE"
                                                        jv_Object.filter = json.dumps({"jventry_gid": JV_Header_Gid,"jvcrno": Single_Unique_Values,"remark":remark,
                                                                                       "jvrefno":CBSReferenceNo,"status_":Final_status,
                                                                                       "jventry_type":JV_Entry_Type,"jventry_refno":JV_Entry_Ref_Number,
                                                                                       "jventry_amount":JV_Header_Amount})
                                                        jv_Object.classification = json.dumps(
                                                            {"entity_gid": entity_gid, "entity_detailsgid": 1})
                                                        jv_Object.create_by = create_by
                                                        out_put_final_data = jv_Object.jv_process_set_model()
                                                        out_data_final = out_put_final_data.get("MESSAGE")
                                                        final_result = out_data_final[0]
                                                        if (final_result == "SUCCESS"):
                                                            Final_Unique_Values.append("SUCCESS")
                                                            if (len(Final_Unique_Values) == len(Unique_Values)):
                                                                return JsonResponse(final_result, safe=False)
                                                        else:
                                                            return JsonResponse(
                                                                {"MESSAGE": "ERROR_OCCURED_ACCOUNTING_ENTRY_SET", "DATA": out_data_final})
                                                    except Exception as e:
                                                        return JsonResponse(
                                                            {"MESSAGE": "ERROR_OCCURED_ON_ACCOUNTING_ENTRY_SET", "DATA": str(e)})
                                                else:
                                                    return JsonResponse(
                                                        {"MESSAGE": "FAILED", "FAILED_STATUS": results_data})
                                            except Exception as e:
                                                return JsonResponse({"MESSAGE": "ERROR_OCCURED_ON_API", "DATA": str(e)})
                                        else:
                                            return JsonResponse({"MESSAGE": "ERROR_OCCURED_ON_TOKEN_GENERATIONS OR INVALID AUTHENTICATONS"})
                                    except Exception as e:
                                        common.logger.error(e)
                                        return JsonResponse({"MESSAGE": "ERROR_OCCURED_TOKEN_GENERATION", "DATA": str(e), "log_data": log_data})
                                else:
                                    return JsonResponse({"MESSAGE": "Credit Amount and Debit Amount Not Equal"})
                        else:
                            return JsonResponse({"MESSAGE": "Credit Amount and Debit Amount Not Equal"})
                    except Exception as e:
                        common.logger.error(e)
                        return JsonResponse({"MESSAGE": "ERROR_OCCURED_ON_ENTRY_DETAILS_GET", "DATA": str(e)})
                elif (result_data == "ALREADY PROCESSED"):
                    return JsonResponse(result_data, safe=False)
                else:
                    return JsonResponse({"MESSAGE": "ERROR_OCCURED_ACCOUNTING_ENTRY_SET", "DATA": out_put_data})
        except Exception as e:
            return JsonResponse({"MESSAGE": "ERROR_OCCURED", "DATA": str(e)})