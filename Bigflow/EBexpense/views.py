from decimal import Decimal
from typing import Dict
from django.shortcuts import render
from Bigflow.Master import views as master_views
from django.http import JsonResponse, HttpResponse
from Bigflow.EBexpense.Model import ebmodel
import json
import pandas as pd
import Bigflow.Core.models as common
import requests
from Bigflow.Core.models import decrpt as decry_data
from Bigflow.menuClass import utility as utl
token = common.token()

from apscheduler.scheduler import Scheduler
# Start the scheduler Feb 5
sched = Scheduler()
sched.start()
import datetime

from datetime import date
current_date = date.today()




def electricitysmry(request):
    utl.check_authorization(request)
    return render(request, "Electricitydetails_Summary.html")

def electricity_CO_DO_smry(request):
    utl.check_authorization(request)
    return render(request, "Electricitydetails_CO_DOsummary.html")

def electricity_CO_DO_aprvlsmry(request):
    utl.check_authorization(request)
    return render(request, "Electricitydetails_CO_DO_Approvalsmry.html")


def electricitytxnsmry(request):
    utl.check_authorization(request)
    return render(request, "Electricitydetails_txnsummary.html")

def electricityquerysmry(request):
    utl.check_authorization(request)
    return render(request, "Electricitydetails_querysummary.html")

def electricityapprovalsmry(request):
    utl.check_authorization(request)
    return render(request, "Electricitydetailsapproval_summary.html")

def electricitypaymentquerysmry(request):
    utl.check_authorization(request)
    return render(request, "Electricitypaymentqry_smry.html")


def electricitycreate(request):
    utl.check_authorization(request)
    return render(request, "Electricitydetails_Create.html")

def electricitymastertxnsummary(request):
    utl.check_authorization(request)
    return render(request, "Electricitymaster_to_txnsummary.html")




def set_ebdata(request):
    utl.check_authorization(request)
    utl.check_pointaccess(request)
    if request.method == 'POST':
        obj_sales_fav_pdct = ebmodel.Eb_model()
        jsondata = json.loads(request.body.decode('utf-8'))
        obj_sales_fav_pdct.action = jsondata.get('Action')
        obj_sales_fav_pdct.jsonData = json.dumps(jsondata.get('data'))
        obj_sales_fav_pdct.classification = decrupt_generalData(jsondata.get('classification'))
        df_sales_fav_pdct = obj_sales_fav_pdct.set_ebmasterdata()
        return JsonResponse(df_sales_fav_pdct, safe=False)


def get_eb_smry(request):
    utl.check_authorization(request)
    utl.check_pointaccess(request)
    if request.method == 'POST':
     try:
        objdata = ebmodel.Eb_model()
        jsondata = json.loads(request.body.decode('utf-8'))
        objdata.action = jsondata.get('Action')
        objdata.jsonData = json.dumps(jsondata.get('data'))
        objdata.classification = decrupt_generalData(jsondata.get('classification'))
        obj_getemp_data = objdata.get_eb_summary()
        jdata = obj_getemp_data.to_json(orient='records')
        return JsonResponse(json.loads(jdata), safe=False)
     except Exception as e:
         return JsonResponse({"MESSAGE": "ERROR_OCCURED", "DATA": str(e)})

# def getreport_data(request):
#     if request.method == 'GET':
#      try:
#         objdata = ebmodel.Eb_model()
#         objdata.action = request.GET['action']
#         objdata.jsonData = json.dumps({'ebconsumer_branchgid':request.GET['ebconsumer_branchgid']
#         ,'bill_paymentstatus':request.GET['bill_paymentstatus'],'ebconsumer_no':request.GET['ebconsumer_no'],'ebconsumer_name':request.GET['ebconsumer_name'],
#         'tran_fromdate':request.GET['tran_fromdate'],'tran_todate':request.GET['tran_todate']})
#         objdata.classification = decrupt_generalData({'Entity_Gid':request.GET['Entity_Gid'],'Create_By':request.GET['Create_By']})
#         obj_getemp_data = objdata.get_eb_summary()
#         jdata = obj_getemp_data.to_json(orient='records')
#         return JsonResponse(json.loads(jdata), safe=False)
#      except Exception as e:
#          return JsonResponse({"MESSAGE": "ERROR_OCCURED", "DATA": str(e)})


def ebconsumerdatavalidate(request):
    utl.check_authorization(request)
    utl.check_pointaccess(request)
    if request.method == 'POST':
     try:
        jsondata = json.loads(request.body.decode('utf-8'))
        jsonData = json.dumps(jsondata.get('data'))
        generated_token_data = master_views.master_sync_("GET", "get_data", 1)
        new_token = generated_token_data.get("DATA")[0].get("clienttoken_name")
        headers = {"content-type": "application/json", "Authorization": "Bearer " + new_token + ""}
        ip = common.clientapi()
        resp = requests.post("" + ip + "/next/v1/mw/tneb/fetch", params='', data=jsonData, headers=headers,
                             verify=False)
        if (resp.status_code == 200):
            response = json.loads(resp.content)
            response_msg = json.dumps(response.get("out_msg"))
            return JsonResponse(json.loads(response_msg), safe=False)
        else:
            return JsonResponse({"MESSAGE": "ERROR_OCCURED", "DATA": str('error on API')})
     except Exception as e:
         return JsonResponse({"MESSAGE": "ERROR_OCCURED", "DATA": str(e)})


def ebconsumerpayment(request):
    utl.check_authorization(request)
    utl.check_pointaccess(request)
    if request.method == 'POST':
     try:
        jsondata = json.loads(request.body.decode('utf-8'))
        obj_sales_fav_pdct = ebmodel.Eb_model()
        if jsondata.get('Action') == 'Payment':
            jsonData = json.dumps(jsondata.get('data'))
            log_data = [{"Before_TNEBAPI_PAY_CALL": jsonData}]
            common.logger.error(log_data)
            generated_token_data = master_views.master_sync_("GET", "get_data", 1)
            new_token = generated_token_data.get("DATA")[0].get("clienttoken_name")
            headers = {"content-type": "application/json", "Authorization": "Bearer " + new_token + ""}
            ip = common.clientapi()
            resp = requests.post("" + ip + "/next/v1/mw/tneb/pay", params='', data=jsonData, headers=headers,
                                 verify=False)
            if (resp.status_code == 200):
                response = json.loads(resp.content)
                log_data = [{"After_TNEBAPI_PAY_CALL": response}]
                common.logger.error(log_data)
                response_msg = response.get("out_msg")
                if response_msg["ErrorCode"] == "00":
                    obj_sales_fav_pdct.action = jsondata.get('Action')
                    dbjson = jsondata.get('datas')
                    dbjson.update({"bill_refno":response_msg["ReferenceNumber"]})
                    obj_sales_fav_pdct.jsonData = json.dumps(dbjson)
                    obj_sales_fav_pdct.classification = decrupt_generalData(jsondata.get('classification'))
                    df_sales_fav_pdct = obj_sales_fav_pdct.payment_ebmaster()
                    return JsonResponse(df_sales_fav_pdct, safe=False)
                else:
                    return JsonResponse({"MESSAGE":response_msg["ErrorDescription"] , "DATA": str(response_msg["ErrorDescription"])})
            else:
                return JsonResponse({"MESSAGE": "ERROR_OCCURED", "DATA": str('error on API')})
        elif jsondata.get('Action') == 'Caution_Update' or jsondata.get('Action') == 'Manual_Rejected':
            obj_sales_fav_pdct.action = jsondata.get('Action')
            obj_sales_fav_pdct.jsonData = json.dumps(jsondata.get('datas'))
            obj_sales_fav_pdct.classification = decrupt_generalData(jsondata.get('classification'))
            df_sales_fav_pdct = obj_sales_fav_pdct.payment_ebmaster()
            return JsonResponse(df_sales_fav_pdct, safe=False)
     except Exception as e:
         return JsonResponse({"MESSAGE": "ERROR_OCCURED", "DATA": str(e)})









def decrupt_generalData(lj_data):
    if 'Entity_Gid' in lj_data:
        entitiy_gid = decry_data(lj_data['Entity_Gid'])
        lj_data["Entity_Gid"] = entitiy_gid

    if 'Create_By' in lj_data:
        create_by = decry_data(lj_data['Create_By'])
        lj_data["Create_By"] =create_by
        return json.dumps(lj_data)
    else:
        lj_data = json.dumps(lj_data)
        return lj_data
    return json.dumps(lj_data)
from ast import literal_eval

def master_txn_eb_Data(request):
    utl.check_authorization(request)
    utl.check_pointaccess(request)
    objdata = ebmodel.Eb_model()
    objdata.action = 'Scheduler_Data'
    objdata.jsonData = json.dumps({'ebconsumer_status':'Approved'})
    objdata.classification = json.dumps({"Entity_Gid": 1})
    obj_getemp_data = objdata.get_eb_summary()
    jdata = obj_getemp_data.to_json(orient='records')
    data = literal_eval(jdata)
    for x in data:
        jsonData = json.dumps({"MobileNo": x['ebconsumer_contactno'],"BankCode": "PGMKVB","ConsumerNo": x['ebconsumer_no']})
        log_data = [{"Before_TNEBAPI_CALL": jsonData}]
        common.logger.error(log_data)
        generated_token_data = master_views.master_sync_("GET", "get_data", 1)
        new_token = generated_token_data.get("DATA")[0].get("clienttoken_name")
        headers = {"content-type": "application/json", "Authorization": "Bearer " + new_token + ""}
        ip = common.clientapi()
        resp = requests.post("" + ip + "/next/v1/mw/tneb/fetch", params='', data=jsonData,
                             headers=headers,
                             verify=False)
        if (resp.status_code == 200):
            response = json.loads(resp.content)
            log_data = [{"After_TNEBAPI_CALL": response}]
            common.logger.error(log_data)
            if response["bpms_error_code"] == "00":
                response_msg = response.get("out_msg")
                if response_msg["STATUS"] != '':
                    objdata.action = 'INSERT'
                    response_msg.update({"TRANSDT":datetime.datetime.strptime(str(response_msg['TRANSDT']),'%d-%b-%Y %H:%M:%S').strftime('%Y-%m-%d')})
                    response_msg.update({"bill_ebconsumergid":str(x['ebconsumer_gid'])})
                    if x['ebconsumer_occupancy'] == 'Onsite ATM' or x['ebconsumer_occupancy'] == 'Offsite ATM':
                        Sub_cat_gid = 513
                        Debit_Gl = "446000930"
                    elif x['ebconsumer_occupancy'] == 'Staff Quarters' or x['ebconsumer_occupancy'] == 'Guest House':
                        Sub_cat_gid = 403
                        Debit_Gl = "428000100"
                    else:
                        Sub_cat_gid = 402
                        Debit_Gl = "428000100"
                    response_msg.update({"In_date":response_msg['TRANSDT'],
                                        "bill_contactno":x['ebconsumer_contactno'],
                                        "Channel": "Courier",
                                        "Courier_gid": 42,
                                        "AWB_no": "1",
                                        "No_Of_Packets": 1,
                                        "Inward_From": "",
                                        "Received_by": '0ADMIN',
                                        "Remark": "",
                                        "Header_gid": 0,
                                        "Doc_type": 214,
                                        "packet": "PACKET - 1",
                                        "Status": "NEW",
                                        "Count": "1",
                                        "Remark": "",
                                        "Detail_gid": 0,
                                        "Supplier_gid": 1955,
                                        "Sup_state_gid": 31,
                                        "Is_GST": "N",
                                        "Invoice_Date": response_msg['TRANSDT'],
                                        "Invoice_No": x['ebconsumer_no']+str(datetime.datetime.now().strftime("-%b-%d")),
                                        "Invoice_Tot_Amount": str(response_msg["BILLAMT"]),
                                        "Supplier_GST_No": "",
                                        "Header_Status": "NEW",
                                        "Reprocessed": "",
                                         "Remark": "1",
                                        "Employee_gid": "0ADMIN",
                                        "GROUP": "INWARD",
                                        "branch_gid":x['branch_gid'],
                                        "IS_ECF": "N",
                                        "ECF_NO": "",
                                        "BAR_CODE": "1",
                                        "RMU_CODE": "1",
                                        "Due_Adjustment": "N",
                                        "Advance_incr": " ",
                                        "Is_onward": "N",
                                        "Is_amort": "N",
                                        "Is_captalized": "N",
                                        "Is_rcm": "N",
                                        "invoicetaxamount": str(response_msg["BILLAMT"]),
                                        "Pono": 0,
                                        "Advance_type": 0,
                                        "location": 0,
                                        "Item_Name": "Electricity Charges",
                                        "Description": str(datetime.datetime.now().strftime("%b-%Y")),
                                        "HSN_Code": "1",
                                        "Unit_Price": str(response_msg["BILLAMT"]),
                                        "Quantity": "1",
                                        "Amount": str(response_msg["BILLAMT"]),
                                        "DetailProduct_name": 0,
                                        "DetailProduct_gid": 0,
                                        "Discount": 0,
                                        "IGST": 0,
                                        "CGST": 0,
                                        "SGST": 0,
                                        "Total_Amount": str(response_msg["BILLAMT"]),
                                        "PO_Header_Gid": "0",
                                        "PO_Detail_Gid": "",
                                        "GRN_Header_Gid": "",
                                        "GRN_Detail_Gid": "",
                                        "Invoice_Sno": 1,
                                        "Invoice_Other_Amount": 0,
                                        "_invoicedate": 0,
                                        "Invoice_Details_Gid": "0",
                                        "Category_Gid": 56,
                                        "Sub_Category_Gid": Sub_cat_gid,
                                        "D_GL_No": Debit_Gl,
                                        "Debit_Amount": str(response_msg["BILLAMT"]),
                                        "Debit_Gid": "0",
                                        "Invoice_Sno": 1,
                                        "Deduction_amt": 0,
                                        "cc_id": 167,
                                        "bs_id": 42,
                                        "Debit_percentage": 100,
                                        "Paymode_Gid": 8,
                                        "Paymode_name": "CREDITGL",
                                        "C_GL_No": "1741155000059174",
                                        "Bank_Gid": 2964,
                                        "Ref_No": "1741155000059174",
                                        "Tax_Gid": "",
                                        "Tax_Type": "",
                                        "Tax_Rate": "",
                                        "TDS_Exempt": "N",
                                        "trnbranch": "1603",
                                        "paybranch": 1903,
                                        "Credit_Amount":  str(response_msg["BILLAMT"]),
                                        "Credit_Gid": "0",
                                        "taxable_amt": 0,
                                        "ppx_headergid": 0,
                                        "Is_due": 'false',
                                        "supplier_gid": 1955,
                                        "AP_Status": "CHECKER"
                                         })
                    objdata.jsonData = json.dumps(response_msg)
                    objdata.classification = json.dumps({"Entity_Gid":1,"Create_By":1})
                    df_sales_fav_pdct = objdata.payment_ebmaster()
                    continue
                else:
                    continue
    return


def master_txn_eb_Data_scheduler():
    objdata = ebmodel.Eb_model()
    objdata.action = 'Scheduler_Data'
    objdata.jsonData = json.dumps({'ebconsumer_status':'Approved'})
    objdata.classification = json.dumps({"Entity_Gid": 1})
    obj_getemp_data = objdata.get_eb_summary()
    jdata = obj_getemp_data.to_json(orient='records')
    data = literal_eval(jdata)
    for x in data:
        jsonData = json.dumps({"MobileNo": x['ebconsumer_contactno'],"BankCode": "PGMKVB","ConsumerNo": x['ebconsumer_no']})
        log_data = [{"Before_TNEBAPI_CALL": jsonData}]
        common.logger.error(log_data)
        generated_token_data = master_views.master_sync_("GET", "get_data", 1)
        new_token = generated_token_data.get("DATA")[0].get("clienttoken_name")
        headers = {"content-type": "application/json", "Authorization": "Bearer " + new_token + ""}
        ip = common.clientapi()
        resp = requests.post("" + ip + "/next/v1/mw/tneb/fetch", params='', data=jsonData,
                             headers=headers,
                             verify=False)
        if (resp.status_code == 200):
            response = json.loads(resp.content)
            log_data = [{"After_TNEBAPI_CALL": response}]
            common.logger.error(log_data)
            if response["bpms_error_code"] == "00":
                response_msg = response.get("out_msg")
                if response_msg["STATUS"] != '':
                    objdata.action = 'INSERT'
                    response_msg.update({"TRANSDT":datetime.datetime.strptime(str(response_msg['TRANSDT']),'%d-%b-%Y %H:%M:%S').strftime('%Y-%m-%d')})
                    response_msg.update({"bill_ebconsumergid":str(x['ebconsumer_gid'])})
                    if x['ebconsumer_occupancy'] == 'Onsite ATM' or x['ebconsumer_occupancy'] == 'Offsite ATM':
                        Sub_cat_gid = 513
                        Debit_Gl = "446000930"
                    elif x['ebconsumer_occupancy'] == 'Staff Quarters' or x['ebconsumer_occupancy'] == 'Guest House':
                        Sub_cat_gid = 403
                        Debit_Gl = "428000100"
                    else:
                        Sub_cat_gid = 402
                        Debit_Gl = "428000100"
                    response_msg.update({"In_date":response_msg['TRANSDT'],
                                        "bill_contactno":x['ebconsumer_contactno'],
                                        "Channel": "Courier",
                                        "Courier_gid": 42,
                                        "AWB_no": "1",
                                        "No_Of_Packets": 1,
                                        "Inward_From": "",
                                        "Received_by": '0ADMIN',
                                        "Remark": "",
                                        "Header_gid": 0,
                                        "Doc_type": 214,
                                        "packet": "PACKET - 1",
                                        "Status": "NEW",
                                        "Count": "1",
                                        "Remark": "",
                                        "Detail_gid": 0,
                                        "Supplier_gid": 1955,
                                        "Sup_state_gid": 31,
                                        "Is_GST": "N",
                                        "Invoice_Date": response_msg['TRANSDT'],
                                        "Invoice_No": x['ebconsumer_no']+str(datetime.datetime.now().strftime("-%b-%d")),
                                        "Invoice_Tot_Amount": str(response_msg["BILLAMT"]),
                                        "Supplier_GST_No": "",
                                        "Header_Status": "NEW",
                                        "Reprocessed": "",
                                         "Remark": "1",
                                        "Employee_gid": "0ADMIN",
                                        "GROUP": "INWARD",
                                        "branch_gid":x['branch_gid'],
                                        "IS_ECF": "N",
                                        "ECF_NO": "",
                                        "BAR_CODE": "1",
                                        "RMU_CODE": "1",
                                        "Due_Adjustment": "N",
                                        "Advance_incr": " ",
                                        "Is_onward": "N",
                                        "Is_amort": "N",
                                        "Is_captalized": "N",
                                        "Is_rcm": "N",
                                        "invoicetaxamount": str(response_msg["BILLAMT"]),
                                        "Pono": 0,
                                        "Advance_type": 0,
                                        "location": 0,
                                        "Item_Name": "Electricity Charges",
                                        "Description": str(datetime.datetime.now().strftime("%b-%Y")),
                                        "HSN_Code": "1",
                                        "Unit_Price": str(response_msg["BILLAMT"]),
                                        "Quantity": "1",
                                        "Amount": str(response_msg["BILLAMT"]),
                                        "DetailProduct_name": 0,
                                        "DetailProduct_gid": 0,
                                        "Discount": 0,
                                        "IGST": 0,
                                        "CGST": 0,
                                        "SGST": 0,
                                        "Total_Amount": str(response_msg["BILLAMT"]),
                                        "PO_Header_Gid": "0",
                                        "PO_Detail_Gid": "",
                                        "GRN_Header_Gid": "",
                                        "GRN_Detail_Gid": "",
                                        "Invoice_Sno": 1,
                                        "Invoice_Other_Amount": 0,
                                        "_invoicedate": 0,
                                        "Invoice_Details_Gid": "0",
                                        "Category_Gid": 56,
                                        "Sub_Category_Gid": Sub_cat_gid,
                                        "D_GL_No": Debit_Gl,
                                        "Debit_Amount": str(response_msg["BILLAMT"]),
                                        "Debit_Gid": "0",
                                        "Invoice_Sno": 1,
                                        "Deduction_amt": 0,
                                        "cc_id": 167,
                                        "bs_id": 42,
                                        "Debit_percentage": 100,
                                        "Paymode_Gid": 8,
                                        "Paymode_name": "CREDITGL",
                                        "C_GL_No": "1741155000059174",
                                        "Bank_Gid": 2964,
                                        "Ref_No": "1741155000059174",
                                        "Tax_Gid": "",
                                        "Tax_Type": "",
                                        "Tax_Rate": "",
                                        "TDS_Exempt": "N",
                                        "trnbranch": "1603",
                                        "paybranch": 1903,
                                        "Credit_Amount":  str(response_msg["BILLAMT"]),
                                        "Credit_Gid": "0",
                                        "taxable_amt": 0,
                                        "ppx_headergid": 0,
                                        "Is_due": 'false',
                                        "supplier_gid": 1955,
                                        "AP_Status": "CHECKER"
                                         })
                    objdata.jsonData = json.dumps(response_msg)
                    objdata.classification = json.dumps({"Entity_Gid":1,"Create_By":1})
                    df_sales_fav_pdct = objdata.payment_ebmaster()
                    continue
                else:
                    continue
    return

sched.add_cron_job(master_txn_eb_Data_scheduler, hour=0, minute=10)

def eb_status_insert(request):
    utl.check_authorization(request)
    utl.check_pointaccess(request)
    jsondata = json.loads(request.body.decode('utf-8'))
    objdata = ebmodel.Eb_model()
    objdata.action = 'Scheduler_Data'
    objdata.jsonData = json.dumps({'ebconsumer_status':'Approved'})
    objdata.classification = json.dumps({"Entity_Gid": 1})
    obj_getemp_data = objdata.get_eb_summary()
    jdata = obj_getemp_data.to_json(orient='records')
    data = literal_eval(jdata)
    for x in data:
        jsonData = json.dumps({"MobileNo": "913465798549","BankCode": "PGMKVB","ConsumerNo": x['ebconsumer_no']})
        generated_token_data = master_views.master_sync_("GET", "get_data", 1)
        new_token = generated_token_data.get("DATA")[0].get("clienttoken_name")
        headers = {"content-type": "application/json", "Authorization": "Bearer " + new_token + ""}
        ip = common.clientapi()
        resp = requests.post("" + ip + "/next/v1/mw/tneb/fetch", params='', data=jsonData,
                             headers=headers,
                             verify=False)
        if (resp.status_code == 200):
            response = json.loads(resp.content)
            if response["bpms_error_code"] == "00":
                response_msg = response.get("out_msg")
                if response_msg["STATUS"] != '':
                    objdata.action = jsondata.get('Action')
                    response_msg.update({"TRANSDT":datetime.datetime.strptime(str(response_msg['TRANSDT']),'%d-%b-%Y %H:%M:%S').strftime('%Y-%m-%d')})
                    response_msg.update({"consumerstatus_consumergid":str(x['ebconsumer_gid']),"consumerstatus_consumerno":str(x['ebconsumer_no']),"consumerstatus_status":response_msg["STATUS"]})
                    objdata.jsonData = json.dumps(response_msg)
                    objdata.classification = json.dumps({"Entity_Gid":1,"Create_By":1})
                    df_sales_fav_pdct = objdata.payment_ebmaster()
                    continue
    return JsonResponse(df_sales_fav_pdct, safe=False)




def eb_fetch_validte(request):
    utl.check_authorization(request)
    utl.check_pointaccess(request)
    jsondata = json.loads(request.body.decode('utf-8'))
    jsonData = json.dumps({"MobileNo": jsondata.get('contact_no'),"BankCode": "PGMKVB","ConsumerNo": jsondata.get('consumer_no')})
    generated_token_data = master_views.master_sync_("GET", "get_data", 1)
    new_token = generated_token_data.get("DATA")[0].get("clienttoken_name")
    headers = {"content-type": "application/json", "Authorization": "Bearer " + new_token + ""}
    ip = common.clientapi()
    resp = requests.post("" + ip + "/next/v1/mw/tneb/fetch", params='', data=jsonData,
                         headers=headers,
                         verify=False)
    if (resp.status_code == 200):
        response = json.loads(resp.content)
        if response["bpms_error_code"] == "00":
            response_msg = response.get("out_msg")
            if response_msg["STATUS"] == 'K':
                return JsonResponse({"MESSAGE": "SUCCESS", "DATA": response_msg["STATUS"]})
            else:
                return JsonResponse({"MESSAGE": "ERROR_OCCURED", "DATA": response_msg["STATUS"]})




def get_view_tble_view(request):
    # utl.check_authorization(request)
    # utl.check_pointaccess(request)
    if request.method == 'POST':
        obj_sales_fav_pdct =  ebmodel.Eb_model()
        jsondata = json.loads(request.body.decode('utf-8'))
        if jsondata.get('Group') == 'COLUMN_FILTER':
            obj_sales_fav_pdct.action = jsondata.get('Action')
            obj_sales_fav_pdct.jsonData = json.dumps(jsondata.get('data'))
            obj_sales_fav_pdct.jsondata = json.dumps(jsondata.get('data_filter'))
            obj_sales_fav_pdct.jsonData_sec = json.dumps(jsondata.get('data_filter_report'))
            obj_sales_fav_pdct.classification = decrupt_generalData(jsondata.get('classification'))
            obj_getemp_data = obj_sales_fav_pdct.get_table_datareport()
            jdata = list(obj_getemp_data.columns)
            jdata = {"data":jdata}
            return JsonResponse(jdata)
        if jsondata.get('Group') != 'COLUMN_FILTER':
            obj_sales_fav_pdct.action = jsondata.get('Action')
            obj_sales_fav_pdct.jsonData = json.dumps(jsondata.get('data'))
            obj_sales_fav_pdct.jsondata = json.dumps(jsondata.get('data_filter'))
            obj_sales_fav_pdct.jsonData_sec = json.dumps(jsondata.get('data_filter_report'))
            obj_sales_fav_pdct.classification = decrupt_generalData(jsondata.get('classification'))
            obj_getemp_data = obj_sales_fav_pdct.get_table_datareport()
            jdata = obj_getemp_data.to_json(orient='records')
            return JsonResponse(json.loads(jdata), safe=False)
import boto3
from Bigflow.settings import S3_BUCKET_NAME

import time

def get_view_tble_view_1(request):
    # utl.check_authorization(request)
    # utl.check_pointaccess(request)
    if request.method == 'POST':
        obj_sales_fav_pdct = ebmodel.Eb_model()
        jsondata = json.loads(request.body.decode('utf-8'))
        obj_sales_fav_pdct.action = jsondata.get('Action')
        obj_sales_fav_pdct.jsonData = json.dumps(jsondata.get('data'))
        obj_sales_fav_pdct.jsondata = json.dumps(jsondata.get('data_filter'))
        filter_Data = jsondata.get('data_filter')
        reportemp_reportgid = filter_Data['rep_temp_id']
        obj_sales_fav_pdct.jsonData_sec = json.dumps(jsondata.get('data_filter_report'))
        obj_sales_fav_pdct.classification = decrupt_generalData(jsondata.get('classification'))
        XLSX_MIME = 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        response = HttpResponse(content_type=XLSX_MIME)
        response['Content-Disposition'] = 'attachment; filename="PythonExport.xlsx"'
        writer = pd.ExcelWriter(response, engine='xlsxwriter')
        df_view  = obj_sales_fav_pdct.get_table_datareport()
        only_col = list(df_view.columns)
        final = df_view[only_col]

        millis = int(round(time.time() * 1000))
        filename =  str(millis) + '.xlsx'

        obj_sales_fav_pdct.action = 'REPORT_STORAGE'
        obj_sales_fav_pdct.jsonData = '{"REPORT_FILTER": []}'
        obj_sales_fav_pdct.jsondata = json.dumps(
            {"rep_temp_id": str(reportemp_reportgid), "File_path": filename, "File_status": "PROCESSING"})
        obj_sales_fav_pdct.jsonData_sec = '{"column_list":[]}'
        # clasifiction = json.loads(request.GET['classification'])
        obj_sales_fav_pdct.classification = json.dumps({"Entity_Gid": decry_data(request.session['Entity_gid']), "Create_By": decry_data(request.session['Emp_gid'])})
        df_view = obj_sales_fav_pdct.set_table_report()
        datas = "".join(df_view)
        datas = datas.split(',')
        v= datas[0]
        v1 = datas[1]

        final.to_excel(writer, 'Sheet1')
        writer.save()
        data = response.getvalue()
        s3 = boto3.resource('s3')
        s3_obj = s3.Object(bucket_name=S3_BUCKET_NAME, key=filename)
        s3_obj.put(Body=data)

        obj_sales_fav_pdct.action = 'REPORT_STATUS_UP'
        obj_sales_fav_pdct.jsonData = '{"REPORT_FILTER": []}'
        obj_sales_fav_pdct.jsondata = json.dumps(
            {"rep_trn_id": str(v1), "File_status": "COMPLETED"})
        obj_sales_fav_pdct.jsonData_sec = '{"column_list":[]}'
        obj_sales_fav_pdct.classification = json.dumps({"Entity_Gid": decry_data(request.session['Entity_gid']),
                                                        "Create_By": decry_data(request.session['Emp_gid'])})
        df_view = obj_sales_fav_pdct.set_table_report()
        return JsonResponse(df_view, safe=False)


def set_reportdata(request):
    # utl.check_authorization(request)
    # utl.check_pointaccess(request)
    if request.method == 'POST':
        obj_sales_fav_pdct = ebmodel.Eb_model()
        jsondata = json.loads(request.body.decode('utf-8'))
        obj_sales_fav_pdct.action = jsondata.get('Action')
        obj_sales_fav_pdct.jsonData = json.dumps(jsondata.get('data'))
        obj_sales_fav_pdct.jsondata = json.dumps(jsondata.get('data_filter'))
        obj_sales_fav_pdct.jsonData_sec = json.dumps(jsondata.get('data_filter_report'))
        obj_sales_fav_pdct.classification = decrupt_generalData(jsondata.get('classification'))
        obj_getemp_data = obj_sales_fav_pdct.set_table_report()
        return JsonResponse(obj_getemp_data, safe=False)