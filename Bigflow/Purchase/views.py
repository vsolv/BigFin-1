import os
from decimal import Decimal
from typing import Dict

from django.core.files.storage import default_storage
from django.shortcuts import render
from Bigflow.API import views as commonview
from Bigflow import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import get_template
from django.template import Context
from Bigflow.Purchase.Model import mPurchase
from Bigflow.AP.model import mAP
from django.http import JsonResponse, HttpResponse, Http404
import json
import base64
import ast
import datetime
import time
from Bigflow.settings import BASE_DIR
import boto3
from dateutil import tz
# from dateutil.relativedsourceelta import relativedelta
import pandas as pd
import Bigflow.Core.models as common
import requests
from Bigflow.Report.Model import mStock
from PyPDF2 import PdfFileWriter, PdfFileReader
import Bigflow.Core.jwt_file as jwt
from Bigflow.API import view_purchase
import io
import re
from reportlab.pdfgen import canvas
from rest_framework.response import Response
from reportlab.lib.pagesizes import landscape, letter
from reportlab.lib.pagesizes import A4
from Bigflow.settings import BASE_DIR
from Bigflow.menuClass import utility as utl
from Bigflow.Core.models import decrpt as decry_data
token = common.token()


ip = common.localip()
headers = {"content-type": "application/json", "Authorization": "" + common.token() + ""}


def open_po(request):
    utl.check_authorization(request)
    return render(request, "open_po.html")

def purchase_Report(request):
    return render(request, "Purchase_Advanced_Report.html")

def prheader_ccbs(request):
    utl.check_pointaccess(request)
    return render(request, "pur_prheader_ccbs_popup.html")

def po_delievery_popup(request):
    utl.check_pointaccess(request)
    utl.check_authorization(request)
    return render(request, "po_delievery_popup.html")

def delmat(request):
    utl.check_authorization(request)
    return render(request, "pur_delmatscreen.html")

def adddelmat(request):
    utl.check_pointaccess(request)
    return render(request, "pur_Adddelmat.html")


def poamendsmry(request):
    # utl.check_authorization(request)
    return render(request, "pur_Poamendmentsmry.html")

def poedit_amend(request):
    utl.check_authorization(request)
    return render(request, "pur_PoEdit_amend.html")


def purchasesmry(request):
    utl.check_authorization(request)
    return render(request, "pur_PurchaseSummary.html")

def expense_line_summary(request):
    utl.check_authorization(request)
    return render(request, "expense_line_summary.html")

def expense_line_maker(request):
    utl.check_authorization(request)
    return render(request, "expense_line_maker.html")

def purchasecrte(request):
    utl.check_authorization(request)
    return render(request, "pur_PurchaseCreate.html")


def vendorselection(request):
    utl.check_authorization(request)
    return render(request, "pur_vendorselection.html")
# def purchase(request):
#     utl.check_authorization(request)
#     return render(request, "purchasert.html")


def approvalsmry(request):
    utl.check_authorization(request)
    return render(request, "pur_ApprovalSummary.html")

def codegenerationviews(request):
    utl.check_pointaccess(request)
    #code generation
    code='CMD0001'
    # approvalview(request,code)
    return HttpResponse(code)


def approvalview(request):
    utl.check_pointaccess(request)
    if request.method == 'POST':
        path=request.path
        jsondata = json.loads(request.body.decode('utf-8'))
        jsondata['params']['employee_gid'] = decry_data(request.session['Emp_gid'])
        objdata = mPurchase.Purchase_model()
        objdata.commodity_gid= json.dumps(jsondata.get('params'))
        objdata.action= jsondata.get('action')
        objdata.type= jsondata.get('type')
        objdata.limitamut=0
        value = decry_data(request.session['Entity_gid'])
        objdata.entity_gid  = json.dumps({"Entity_Gid": value})
        common.main_fun1(request.read(), path)
        delmatlimit = objdata.delmatlimit()
        jdata = delmatlimit.to_json(orient='records')
        return JsonResponse(jdata, safe=False)
    else:
        utl.check_authorization(request)
        return render(request, "pur_ApprovalView.html")

def tranapproval(request):
    utl.check_pointaccess(request)
    if request.method == 'POST':
        jsondata = json.loads(request.body.decode('utf-8'))
        path=request.path
        objdata = mPurchase.Purchase_model()
        objdata.data = json.dumps(jsondata)
        objdata.action = 'INSERT_PR'
        objdata.ref_gid =jsondata.get('li_ref_gid')
        objdata.totype = jsondata.get('lc_totype')
        objdata.reftable = jsondata.get('li_reftable_gid')
        objdata.status = jsondata.get('ls_status')
        objdata.to = jsondata.get('li_tto')
        objdata.remark = jsondata.get('ls_remarks')
        objdata.Employee_gid = decry_data(request.session['Emp_gid'])
        objdata.entity_gid = decry_data(request.session['Entity_gid'])
        common.main_fun1(request.read(), path)
        tran = objdata.set_trans()
        return JsonResponse(tran, safe=False)


def po_ammentsummry(request):
    utl.check_authorization(request)
    return render(request, "pur_poadmentsummary.html")

def po_headerget_view(request):
    utl.check_pointaccess(request)
    if request.method == 'POST':
        jsondata = json.loads(request.body.decode('utf-8'))
        objdata = mPurchase.Purchase_model()
        objdata.type=jsondata.get('Type')
        objdata.filter_json = json.dumps(jsondata.get('data').get('Params').get('FILTER'))
        objdata.classification_json = json.dumps(jsondata.get('data').get('Params').get('CLASSIFICATION'))
        objdata.create_by = decry_data(request.session['Emp_gid'])
        obj_cancel_data = objdata.getPoheader_details()
        jdata = obj_cancel_data.to_json(orient='records')
        return JsonResponse(json.loads(jdata), safe=False)


def prfinalapproval(request):
    utl.check_authorization(request)
    utl.check_pointaccess(request)
    return render(request, "pur_Finalapproval.html")


def po_ammentcreate(request):
    utl.check_authorization(request)
    return render(request, "pur_poadmentcreate.html")


def po_ammentapprovalcreate(request):
    utl.check_authorization(request)
    return render(request, "pur_poadmentapprovalcreate.html")


def po_ammentapprovalsummry(request):
    utl.check_authorization(request)
    return render(request, "pur_poadmentapprovalsummary.html")

def getfinalapproval(request):
    utl.check_pointaccess(request)
    if request.method == 'GET':
        objdata = mPurchase.Purchase_model()
        obj_cancel_data = objdata.getfinalapprovalget()
        obj_cancel_data['ccbs_details'] = obj_cancel_data['ccbs_details'].apply(json.loads)
        jdata = obj_cancel_data.to_json(orient='records')
        return JsonResponse(json.loads(jdata), safe=False)



#insert pr ccbs data
def saveccbs1(request):
    utl.check_pointaccess(request)
    if request.method == 'POST':
        objdata = mPurchase.Purchase_model()
        jsondata = json.loads(request.body.decode('utf-8'))
        objdata.action =jsondata.get('Action')
        objdata.type =jsondata.get('Type')
        objdata.prdetailsgid =jsondata.get('prdetailsgid')
        objdata.prheaderddl =json.dumps(jsondata.get('PR_Header'))
        prproductddl =jsondata.get('PR_Products')
        objdata.productsddl=json.dumps(prproductddl)
        objdata1 = decry_data(request.session['Entity_gid'])
        objdata.emp = decry_data(request.session['Emp_gid'])
        objdata.draft=json.dumps({"Entity_Gid":[objdata1]})
        objdata.classification_json=json.dumps({"Entity_Gid":[objdata1]})
        obj_data = objdata.insertprccbs()
        return HttpResponse(obj_data)
        # return JsonResponse(jdata, safe=False)

# def po_querystring(request):
#     utl.check_authorization(request)
#     return render(request, "pur_querystring.html")
#Delmat Save
def delmatsavedatas(request):
    utl.check_pointaccess(request)
    if request.method == 'POST':
        jsondata = json.loads(request.body.decode('utf-8'))
        array=jsondata.get('data').get('array')
        crtby = request.session['Emp_gid']
        enty=json.dumps({"entity_gid":request.session['Entity_gid']})
        params = {'Action': jsondata.get("Action"), 'Type': jsondata.get("Type"),
                  'Entity_Gid': "" + enty + "",'Employee_Gid':""+ str(crtby) +"" }
        datas = json.dumps(array)
        token = jwt.token(request)
        headers = {"content-type": "application/json", "Authorization": "" + token + ""}
        resp = requests.post("" + ip + "/Delmat_set", params=params, data=datas, headers=headers, verify=False)
        response = resp.content.decode("utf-8")
        return HttpResponse(response)
#delmatapproval
def delmatapproval(request):
    utl.check_pointaccess(request)
    return render(request, "pur_delmatapproval.html")

#delmatapprovalsmry
def delmatapprovalsmry(request):
    utl.check_authorization(request)
    return render(request, "pur_delmatapprovalsmry.html")


#Delmat Get
def delmatget(request):
      utl.check_pointaccess(request)
      if request.method == 'POST':
        jsondata = json.loads(request.body.decode('utf-8'))
        e = request.session['Entity_gid']
        enty=json.dumps({"entity_gid":e})
        #action='get'
        params = {'Action': "" + jsondata.get('Action') + "",
                  'Entity_Gid': "" + enty + ""}
        token = jwt.token(request)
        headers = {"content-type": "application/json", "Authorization": "" + token + ""}
        resp = requests.post("" + ip + "/Delmat_set", params=params,headers=headers, verify=False)
        response = resp.content.decode("utf-8")
        return HttpResponse(response)
#Delmat Update
def delmatupdate(request):
    utl.check_pointaccess(request)
    if request.method == 'POST':
        jsondata = json.loads(request.body.decode('utf-8'))
        crtby = request.session['Emp_gid']
        value = request.session['Entity_gid']
        enty=json.dumps({"entity_gid":value})
        action='update'
        type='pr_update'
        params = {'Action': "" + action + "", 'Type': "" + type + "",
                  'Entity_Gid': "" + enty + "",'Employee_Gid':""+ str(crtby) +"" }
        # headers = {"content-type": "application/json", "Authorization": "" + token + ""}
        datas = json.dumps(jsondata)
        token = jwt.token(request)
        headers = {"content-type": "application/json", "Authorization": "" + token + ""}
        resp = requests.post("" + ip + "/Delmat_set", params=params, data=datas, headers=headers, verify=False)
        response = resp.content.decode("utf-8")
        return HttpResponse(response)





#All table value for ccbs
def alltable(request):
    utl.check_pointaccess(request)
    if request.method == 'POST':
        jsondata = json.loads(request.body.decode('utf-8'))
        # value = request.session['Entity_gid']
        obj = mPurchase.Purchase_model()
        obj.actn = ''
        obj.entity_gid = json.dumps(request.session['Entity_gid'])
        params = {'Action': "" + obj.actn + "", 'Entity_Gid': "" + obj.entity_gid + ""}
        token = jwt.token(request)
        headers = {"content-type": "application/json", "Authorization": "" + token + ""}
        datas = json.dumps(jsondata)
        resp = requests.post("" + ip + "/All_Tables_Values_Get", params=params, data=datas, headers=headers,
                             verify=False)
        response = resp.content.decode("utf-8")
        return JsonResponse(response, safe=False)





def setpoterms(request):
    utl.check_pointaccess(request)
    if request.method == 'POST':
        jsondata = json.loads(request.body.decode('utf-8'))
        create_by = request.session['Emp_gid']
        params = {'Action': jsondata.get("Action"), 'Type': jsondata.get("Type"),"create_by":create_by}
        token = jwt.token(request)
        headers = {"content-type": "application/json", "Authorization": "" + token + ""}
        datas = json.dumps(jsondata.get("DETAIL"))
        resp = requests.post("" + ip + "/Set_Poterms", params=params, data=datas, headers=headers, verify=False)
        response = resp.content.decode("utf-8")
        return HttpResponse(response)

def getreportdata(request):
    # utl.check_pointaccess(request)
    if request.method == 'POST':
        jsondata = json.loads(request.body.decode('utf-8'))
        params = {'Action': jsondata.get("Action")}
        token = jwt.token(request)
        headers = {"content-type": "application/json", "Authorization": "" + token + ""}
        datas = json.dumps(jsondata.get("data"))
        resp = requests.post("" + ip + "/Get_allreport", params=params, data=datas, headers=headers, verify=False)
        response = resp.content.decode("utf-8")
        return HttpResponse(response)



def reftable(request):
    utl.check_authorization(request)
    if request.method == 'POST':
        objdata = mPurchase.Purchase_model()
        jsondata = json.loads(request.body.decode('utf-8'))
        objdata.datas = json.dumps(jsondata)
        objdata.entity_gid = decry_data(request.session['Entity_gid'])
        obj_cancel_data = objdata.Reftable_Get()
        jdata = obj_cancel_data.to_json(orient='records')
        return JsonResponse(jdata, safe=False)

def pending_posummary(request):
     utl.check_authorization(request)
     if request.method == 'POST':
         objdata = mPurchase.Purchase_model()
         jsondata = json.loads(request.body.decode('utf-8'))
         objdata.Type = jsondata.get('Type')
         objdata.SubType = jsondata.get('SubType')
         objdata.darta = jsondata.get('darta')
         objdata.entity_gid = decry_data(request.session['Entity_gid'])
         obj_cancel_data = objdata.pending_posummary()
         jdata = obj_cancel_data.to_json(orient='records')
         return JsonResponse(jdata, safe=False)



def New_delmat_Get(request):
    utl.check_authorization(request)
    if request.method == 'POST':
        objdata = mPurchase.Purchase_model()
        jsondata = json.loads(request.body.decode('utf-8'))
        objdata.Type = jsondata.get('Type')
        objdata.filter_json = json.dumps(jsondata.get('data').get('Params').get('FILTER'))
        entityid = decry_data(request.session['Entity_gid'])
        objdata.json_classification = json.dumps({'Entity_Gid':entityid})
        objdata.create_by = decry_data(request.session['Emp_gid'])
        obj_cancel_data = objdata.New_delmatget()
        jdata = obj_cancel_data.to_json(orient='records')
        return JsonResponse(json.loads(jdata), safe=False)

def Prdraftdata(request):
    utl.check_authorization(request)
    if request.method == 'POST':
        objdata = mPurchase.Purchase_model()
        jsondata = json.loads(request.body.decode('utf-8'))
        # objdata.Type = jsondata.get('Type')
        objdata.filter_json = json.dumps(jsondata.get('params'))
        # objdata.json_classification = json.dumps(jsondata.get('data').get('Params').get('CLASSIFICATION'))
        # objdata.entity_gid = request.session['Entity_gid']
        objdata.create_by = decry_data(request.session['Emp_gid'])
        obj_data = objdata.getdraftddl()
        jdata = obj_data.to_json(orient='records')
        return JsonResponse(json.loads(jdata), safe=False)





# Export openpo excel
def openpo_getexcel(request):
    utl.check_pointaccess(request)
    if request.method == 'GET':
        obj_master =  mPurchase.Purchase_model()
        obj_master.Type ='SUMMARY'
        obj_master.SubType = 'OPENPO'
        obj_master.darta ={

            'Supplier_Gid':'',
            'Po_No': '',
            'Product_Gid': '',
            'From_Date': '',
            'To_Date':''
        }
        obj_master.entity_gid = decry_data(request.session['Entity_gid'])
        obj_master.jsonData = json.dumps({"entity_gid": [obj_master.entity_gid]})
        XLSX_MIME = 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        response = HttpResponse(content_type=XLSX_MIME)
        response['Content-Disposition'] = 'attachment; filename="Openpo.xlsx"'
        writer = pd.ExcelWriter(response, engine='xlsxwriter')
        df_view = obj_master.pending_posummary()
        final_df = df_view[['poheader_no', 'poheader_date', 'supplier_name', 'product_name', 'total_qty',  'allreceive_qty','rem_qty']]
        final_df.columns= ['PO Number', 'PO Date', 'Supplier Name', 'Product Name', 'Ordered Quantity','Received Quantity','Remaining Quantity']
        #convert proper df type
        final_df[['Received Quantity','Remaining Quantity']]=  final_df[['Received Quantity','Remaining Quantity']].apply(pd.to_numeric)
        final_df=final_df.sort_values(by=['PO Number'])
        final_df.to_excel(writer, index=False)
        writer.save()
        return response



def purchasesmryget(request):
    utl.check_authorization(request)
    if request.method == 'POST':
        jsondata = json.loads(request.body.decode('utf-8'))
        action='get'
        Emp_gid = decry_data(request.session['Emp_gid'])
        jsondata['Params']['FILTER']['prheader_employee_gid']=Emp_gid
        jsondata['Params']['CLASSIFICATION']['Entity_gid']={'entity_gid':request.session['Entity_gid']}
        jsondata['Params']['CLASSIFICATION']['Employee_gid']=request.session['Emp_gid']
        params = {'Action': action}
        datas = json.dumps(jsondata)
        token = jwt.token(request)
        headers = {"content-type": "application/json", "Authorization": "" + token + ""}
        result = requests.post("" + ip + "/PR_Header_DDl", params=params, headers=headers, data=datas, verify=False)
        results = result.content.decode("utf-8")
        return JsonResponse(json.loads(results), safe=False)


import PyPDF2
from django.http import JsonResponse, HttpResponse, StreamingHttpResponse


def common_downloadfile(request):
    utl.check_authorization(request)
    if request.method == 'GET':
        # filename = request.GET['filename']
        # s3 = boto3.resource('s3')

        filename = request.GET['filename']
        file_path = os.path.join(settings.MEDIA_ROOT+'/PRPO/', filename)
        print(file_path)
        if os.path.exists(file_path):
            with open(file_path, 'rb') as fh:
                response = StreamingHttpResponse(fh.read(), content_type='application/octet-stream')
                response['Content-Disposition'] = 'inline; filename=' + os.path.basename(file_path)
                return response
        else:
            raise Http404

        # s3_obj=s3.Object(bucket_name=common.s3_bucket_name(),key=filename)
        # body=s3_obj.get()['Body']
        


def pur_poclosesummary(request):
    utl.check_authorization(request)
    if request.method == 'POST':
        path=request.path
        obj_close_data = mPurchase.Purchase_model()
        jsondata = json.loads(request.body.decode('utf-8'))
        obj_close_data.Employee_gid = decry_data(request.session['Entity_gid'])
        obj_close_data.action = jsondata.get('Action')
        obj_close_data.type = jsondata.get('Type')
        obj_close_data.po_data = json.dumps(jsondata.get('params').get('Filter'))
        obj_close_data.classification_json = jsondata.get('params').get('Classification')
        obj_close_data.classification_json=json.dumps({"Entity_Gid": obj_close_data.Employee_gid })
        common.main_fun1(request.read(), path)
        data = obj_close_data.get_pocolse()
        jdata = data.to_json(orient='records')
        return JsonResponse(jdata, safe=False)



def pur_pocloseappsummary(request):
    utl.check_authorization(request)
    if request.method == 'GET':
        obj_purchase_get = mPurchase.Purchase_model()
        obj_purchase_get.serail_no = ''
        obj_purchase_get.amount = '0.00'
        obj_purchase_get.status = ''
        obj_purchase_get.Employee_gid = '0';
        df_pocloseapp = obj_purchase_get.get_pocloseapproval()
        jdata = df_pocloseapp.to_json(orient='records')
        return JsonResponse(json.loads(jdata), safe=False)


def pur_poreopensummary(request):
    utl.check_authorization(request)
    if request.method == 'GET':
        obj_purchase_get = mPurchase.Purchase_model()
        obj_purchase_get.serail_no = ''
        obj_purchase_get.amount = '0.00'
        obj_purchase_get.status = ''
        obj_purchase_get.Employee_gid = 0
        df_pocloseapp = obj_purchase_get.get_poreopen()
        jdata = df_pocloseapp.to_json(orient='records')
        return JsonResponse(json.loads(jdata), safe=False)


def poclosesmry(request):
    utl.check_authorization(request)
    return render(request, "pur_PoCloseSummary.html")


def poclosecrte(request):
    utl.check_authorization(request)
    return render(request, "pur_PoCloseCreate.html")


def pocancelsmry(request):
    utl.check_authorization(request)
    if request.method == 'POST':
        path=request.path
        obj_cancel_data = mPurchase.Purchase_model()
        jsondata = json.loads(request.body.decode('utf-8'))
        obj_cancel_data.Employee_gid = decry_data(request.session['Entity_gid'])
        obj_cancel_data.action = jsondata.get('Action')
        obj_cancel_data.type = jsondata.get('Type')
        obj_cancel_data.pocancel_data = json.dumps(jsondata.get('params').get('Filter'))
        obj_cancel_data.classification_json = jsondata.get('params').get('Classification')
        obj_cancel_data.classification_json=json.dumps({"Entity_Gid": obj_cancel_data.Employee_gid })
        common.main_fun1(request.read(), path)
        data = obj_cancel_data.get_pocancel()
        jdata = data.to_json(orient='records')
        return JsonResponse(jdata, safe=False)
    else:
        utl.check_authorization(request)
        return render(request, "pur_PoCancelSummary.html")


def pocancelcrte(request):
    utl.check_authorization(request)
    return render(request, "pur_PoCancelCreate.html")


def poreopensmry(request):
    utl.check_authorization(request)
    return render(request, "pur_PoReopenSummary.html")


def poreopencrte(request):
    utl.check_authorization(request)
    utl.check_pointaccess(request)
    return render(request, "pur_PoReopenCreate.html")


def poapprvlclssmry(request):
    utl.check_authorization(request)
    return render(request, "pur_PoApprovalCloseSummary.html")


def poapprvlclscrt(request):
    utl.check_authorization(request)
    return render(request, "pur_PoApprovalCloseCreate.html")


def poapprvlcnclsmry(request):
    utl.check_authorization(request)
    if request.method == 'POST':
        obj_cancel_data = mPurchase.Purchase_model()
        jsondata = json.loads(request.body.decode('utf-8'))
        obj_cancel_data.serail_no = jsondata.get('params').get('serail_no')
        obj_cancel_data.amount = jsondata.get('params').get('amount')
        obj_cancel_data.status = jsondata.get('params').get('status')
        obj_cancel_data.Employee_gid = 0
        data = obj_cancel_data.get_pocancelapproval()
        jdata = data.to_json(orient='records')
        return JsonResponse(jdata, safe=False)
    else:
        utl.check_authorization(request)
        return render(request, "pur_PoApprovalCancelSummary.html")


def poapprvlcnclcrt(request):
    utl.check_authorization(request)
    return render(request, "pur_PoApprovalCancelCreate.html")



#open po edit
def openpo_edit(request):
    utl.check_authorization(request)
    utl.check_pointaccess(request)
    return render(request, "pur_openpo_edit.html")





def grnsmry(request):
    utl.check_authorization(request)
    return render(request, "pur_GrnSummary.html")


def grncreate(request):
    utl.check_authorization(request)
    return render(request, "pur_GrnCreate.html")


def grnaprvlsmry(request):
    utl.check_authorization(request)
    return render(request, "pur_GrnApprovalSummary.html")


def grnaprvlcreate(request):
    utl.check_authorization(request)
    return render(request, "pur_GrnApprovalCreate.html")


def posummary(request):
    utl.check_authorization(request)
    return render(request, "pur_POsummary.html")





def Poheader_detail(request):
    utl.check_authorization(request)
    if request.method == 'POST':
        path=request.path
        jsondata = json.loads(request.body.decode('utf-8'))
        type = jsondata.get("Type")
        if (type == "GET"):
            entity_gid = decry_data(request.session['Entity_gid'])
            purchase_obj = mPurchase.Purchase_model()
            purchase_obj.type = type
            purchase_obj.filter_json = json.dumps(jsondata.get("params").get("Filter"))
            # purchase_obj.filter_json = json.dumps(jsondata.get("params").get("Filter"))
            purchase_obj.classification_json = json.dumps({"entity_gid": entity_gid})
            purchase_obj.create_by = decry_data(request.session['Emp_gid'])
            common.main_fun1(request.read(), path)
            result = purchase_obj.get_poheader()
            jdata = result.to_json(orient='records')
            return JsonResponse(jdata, safe=False)



def Getpostatus(request):
    utl.check_authorization(request)
    if request.method == 'GET':
        obj_status_get = mPurchase.Purchase_model()
        data = obj_status_get.get_postatus()
        jdata = data.to_json(orient='records')
        return JsonResponse(json.loads(jdata), safe=False)


def POApproval_create(request):
    utl.check_authorization(request)
    return render(request, "pur_POapproval_Create.html")


def POApproval_Index(request):
    utl.check_authorization(request)
    return render(request, "pur_POapproval_Index.html")

# why employee gid 0 aswani for below two
def POApproval_detail(request):
    utl.check_authorization(request)
    if request.method == 'POST':
        obj_header_dtl = mPurchase.Purchase_model()
        jsondata = json.loads(request.body.decode('utf-8'))
        obj_header_dtl.serail_no = jsondata.get('params').get('poheader_sno')
        obj_header_dtl.supplier_name = jsondata.get('params').get('poheader_suppliername')
        obj_header_dtl.amount = jsondata.get('params').get('po_amount')
        obj_header_dtl.status = jsondata.get('params').get('po_status')
        obj_header_dtl.Employee_gid = 0
        data = obj_header_dtl.get_poheader()
        jdata = data.to_json(orient='records')
        return JsonResponse(jdata, safe=False)


def Approval_PODetail(request):
    utl.check_authorization(request)
    if request.method == 'POST':
        path=request.path
        obj_podetail = mPurchase.Purchase_model()
        jsondata = json.loads(request.body.decode('utf-8'))
        obj_podetail.podetails_gid = jsondata.get('params').get('podetails_gid')
        obj_podetail.product_name = jsondata.get('params').get('product_name')
        obj_podetail.Employee_gid = 0
        # common.main_fun1(request.read(), path)
        data = obj_podetail.get_podetails()
        jdata = data.to_json(orient='records')
        return JsonResponse(jdata, safe=False)


def PODelivery_detail(request):
    utl.check_authorization(request)
    if request.method == 'POST':
        path=request.path
        obj_delivery = mPurchase.Purchase_model()
        jsondata = json.loads(request.body.decode('utf-8'))
        obj_delivery.podetails_gid = jsondata.get('params').get('podetails_gid')
        common.main_fun1(request.read(), path)
        data = obj_delivery.get_delivery()
        jdata = data.to_json(orient='records')
        return JsonResponse(jdata, safe=False)


def Approval_View_Update(request):
    utl.check_authorization(request)
    if request.method == 'POST':
        path=request.path
        obj_maker = mPurchase.Purchase_model()
        jsondata = json.loads(request.body.decode('utf-8'))
        obj_maker.action = jsondata.get('params').get('action')
        obj_maker.actionsys = jsondata.get('params').get('actionsys')
        obj_maker.poheader_gid = jsondata.get('params').get('poheader_gid')
        # obj_maker.remark = jsondata.get('params').get('remark')
        obj_maker.remark = ' ' if jsondata.get('params').get('remark') == None else jsondata.get('params').get('remark')
        obj_maker.Employee_gid = decry_data(request.session['Emp_gid'])
        obj_maker.entity_gid = decry_data(request.session['Entity_gid'])
        common.main_fun1(request.read(), path)
        data = obj_maker.set_poapprovalviewupdate()
        return JsonResponse(json.dumps(data), safe=False)


def Approval_Update(request):
    utl.check_authorization(request)
    if request.method == 'POST':
        path=request.path
        obj_maker = mPurchase.Purchase_model()
        jsondata = json.loads(request.body.decode('utf-8'))
        obj_maker.action = jsondata.get('params').get('action')
        obj_maker.poheader_gid = jsondata.get('params').get('poheader_gid')
        obj_maker.remark = ' ' if jsondata.get('params').get('remark') == None else jsondata.get('params').get('remark')
        obj_maker.entity_gid = decry_data(request.session['Entity_gid'])
        obj_maker.Employee_gid = decry_data(request.session['Emp_gid'])
        common.main_fun1(request.read(), path)
        data = obj_maker.set_poapprovalupdate()[0].split(',')
        return JsonResponse(json.dumps(data[1]), safe=False)

def Prapproval_get(request):
   utl.check_authorization(request)
   if request.method == 'POST':
       path=request.path
       obj_prapproval = mPurchase.Purchase_model()
       jdata = json.loads(request.body.decode('utf-8'))
       obj_prapproval.empcode = jdata.get('employee_code')
       obj_prapproval.action = jdata.get('Action')
       obj_prapproval.type = jdata.get('Type')
       obj_prapproval.filter = json.dumps(jdata.get('filter'))
       Entity_Gid=decry_data(request.session['Entity_gid'])
       obj_prapproval.enty = json.dumps({'Entity_Gid':Entity_Gid })
       common.main_fun1(request.read(), path)
       df_prapproval = obj_prapproval.get_prapproval()
       jdata = df_prapproval.to_json(orient='records')
       return JsonResponse(json.loads(jdata), safe=False)


def pr_po_delete(request):
    utl.check_authorization(request)
    if request.method == 'POST':
        obj_prapproval = mPurchase.Purchase_model()
        jsondata = json.loads(request.body.decode('utf-8'))
        obj_prapproval.action = jsondata.get('action')
        obj_prapproval.data = json.dumps(jsondata.get('data'))
        value = decry_data(request.session['Entity_gid'])
        obj_prapproval.enty = json.dumps({"entity_gid": value})
        emp_gid = decry_data(request.session['Emp_gid'])
        obj_prapproval.Employee_gid = json.dumps(emp_gid)
        tran = obj_prapproval.pr_po_delete()
        # jdata = tran.to_json(orient='records')
        return JsonResponse(json.dumps(tran), safe=False)



def Prdetail_get(request):
    utl.check_authorization(request)
    if request.method == 'POST':
        obj_prapproval = mPurchase.Purchase_model()
        path=request.path
        jsondata = json.loads(request.body.decode('utf-8'))
        obj_prapproval.prheader_gid = jsondata.get('params').get('prheader_gid')
        obj_prapproval.product_name = jsondata.get('params').get('product_name')
        obj_prapproval.action = jsondata.get('params').get('action')
        obj_prapproval.Employee_gid = decry_data(request.session['Emp_gid'])
        obj_prapproval.entity_gid = decry_data(request.session['Entity_gid'])
        common.main_fun1(request.read(), path)
        df_prdetails = obj_prapproval.get_prdetails()
        jdata = df_prdetails.to_json(orient='records')
        return JsonResponse(json.loads(jdata), safe=False)


def Dropdown_details(request):
    utl.check_authorization(request)
    if request.method == 'POST':
        dropdown = mPurchase.Purchase_model()
        jsondata = json.loads(request.body.decode('utf-8'))
       
        dropdown.tablename = jsondata.get('params').get('tablename')
        dropdown.gid = jsondata.get('params').get('gid')
        dropdown.name = jsondata.get('params').get('name')
        dropdown.entity_gid = decry_data(request.session['Entity_gid'])
        data = dropdown.get_dropdown_details()
        jdata = data.to_json(orient='records')
        return JsonResponse(jdata, safe=False)


def product_name(request):
    utl.check_authorization(request)
    if request.method == 'POST':
        productname = mPurchase.Purchase_model()
        jsondata = json.loads(request.body.decode('utf-8'))
        productname.action = 'Date_wise'
        productname.date = common.convertdbDate(request.session['date'])
        productname.supplier_gid = jsondata.get('params').get('supplier_gid')
        productname.product_gid = jsondata.get('params').get('product_gid')
        productname.char_active = jsondata.get('params').get('char_active')
        data = productname.get_productnames()
        data['stategid'] = request.session['Entity_state_gid']
        jdata = data.to_json(orient='records')
        return JsonResponse(jdata, safe=False)


def POQtyList(request):
    utl.check_pointaccess(request)
    if request.method == 'POST':
        polist = mPurchase.Purchase_model()
        jsondata = json.loads(request.body.decode('utf-8'))
        polist.action = jsondata.get('params').get('action')
        polist.supplier_gid = jsondata.get('params').get('supplier_gid')
        polist.product_gid = jsondata.get('params').get('product_gid')
        polist.product_name = jsondata.get('params').get('product_name')
        polist.serail_no = jsondata.get('params').get('serial_no')
        data = polist.get_poqty()
        data = data[data['req_qty'] > 0]
        jdata = data.to_json(orient='records')
        return JsonResponse(jdata, safe=False)


def supplier_details(request):
    utl.check_authorization(request)
    if request.method == 'POST':
        suplierdetails = mPurchase.Purchase_model()
        jsondata = json.loads(request.body.decode('utf-8'))
        path=request.path
        suplierdetails.action = jsondata.get('params').get('action')
        suplierdetails.type = jsondata.get('params').get('type')
        suplierdetails.vendor = jsondata.get('params').get('product_gid')
        common.main_fun1(request.read(), path)
        data = suplierdetails.get_supplier()
        data['stategid'] = request.session['Entity_state_gid']
        jdata = data.to_json(orient='records')
        return JsonResponse(jdata, safe=False)


def poreject(request):
    utl.check_authorization(request)
    if request.method == 'POST':
        path=request.path
        obj_maker = mPurchase.Purchase_model()
        jsondata = json.loads(request.body.decode('utf-8'))
        obj_maker.Type = jsondata.get('Type')
        obj_maker.actionsys = jsondata.get('Sub_Type')
        obj_maker.lj_filters = jsondata.get('data').get('Params').get('FILTER')
        obj_maker.lj_filters['li_tto']=decry_data(request.session['Emp_gid'])
        obj_maker.lj_filters = json.dumps(jsondata.get('data').get('Params').get('FILTER'))
        obj_maker.lj_classification = jsondata.get('data').get('Params').get('CLASSIFICATION')
        obj_maker.lj_classification['Entity_Gid']=decry_data(request.session['Entity_gid'])
        obj_maker.lj_classification['Create_by']=decry_data(request.session['Emp_gid'])
        obj_maker.lj_classification = json.dumps(jsondata.get('data').get('Params').get('CLASSIFICATION'))
        common.main_fun1(request.read(), path)
        data = obj_maker.set_poreject()
        return JsonResponse(json.dumps(data), safe=False)


def Poapproval_get(request):
   utl.check_authorization(request)
   if request.method == 'GET':
       obj_prapproval = mPurchase.Purchase_model()
       obj_prapproval.serial_no = ''
       obj_prapproval.status = ''
       obj_prapproval.login_gid = decry_data(request.session['Emp_gid'])
       df_prapproval = obj_prapproval.gett_poapproval()
       jdata = df_prapproval.to_json(orient='records')
       return JsonResponse(json.loads(jdata), safe=False)


def deliverydetail(request):
    utl.check_authorization(request)
    if request.method == 'POST':
        delivery = mPurchase.Purchase_model()
        jsondata = json.loads(request.body.decode('utf-8'))
        delivery.serail_no = jsondata.get('params').get('serail_no')
        data = delivery.get_podelivery()
        jdata = data.to_json(orient='records')
        return JsonResponse(json.loads(jdata), safe=False)


def Prapproval_set(request):
    utl.check_authorization(request)
    if request.method == 'POST':
        path=request.path
        obj_prapproval = mPurchase.Purchase_model()
        jsondata = json.loads(request.body.decode('utf-8'))
        obj_prapproval.action = jsondata.get('params').get('status_pr')
        obj_prapproval.prheader_gid = jsondata.get('params').get('prheader')
        obj_prapproval.empname = jsondata.get('params').get('empname')
        if jsondata.get('params').get('lsremaks') == None :
            obj_prapproval.remark = ' '
        else:
            obj_prapproval.remark = jsondata.get('params').get( 'lsremaks')
        obj_prapproval.Employee_gid = decry_data(request.session['Emp_gid'])
        obj_prapproval.entity_gid = decry_data(request.session['Entity_gid'])
        common.main_fun1(request.read(), path)
        data = obj_prapproval.set_prapproval()
        return JsonResponse(json.dumps(data), safe=False)

def Poapproval_set(request):
    utl.check_authorization(request)
    if request.method == 'POST':
        path=request.path
        obj_prapproval = mPurchase.Purchase_model()
        jsondata = json.loads(request.body.decode('utf-8'))
       
        obj_prapproval.action = jsondata.get('params').get('status_pr')
        obj_prapproval.poheader_gid = jsondata.get('params').get('poheader')
        obj_prapproval.empname = jsondata.get('params').get('empname')
        obj_prapproval.lsremaks = jsondata.get('params').get('lsremaks')
        obj_prapproval.Employee_gid = decry_data(request.session['Emp_gid'])
        obj_prapproval.entity_gid = decry_data(request.session['Entity_gid'])
        common.main_fun1(request.read(), path)
        data = obj_prapproval.set_poapproval()
        return JsonResponse(json.dumps(data), safe=False)





# def Prdelete_Set(request):
#     utl.check_authorization(request)
#     if request.method == 'POST':
#         obj_prdata = mPurchase.Purchase_model()
#         jsondata = json.loads(request.body.decode('utf-8'))
#         obj_prdata.prdetail_gid = jsondata.get('params').get('prdetail_gid')
#         obj_prdata.Employee_gid = request.session['Emp_gid']
#         data = obj_prdata.set_prdelete()
#         return JsonResponse(json.dumps(data), safe=False)





def POheader_Set(request):
    utl.check_pointaccess(request)
    if request.method == 'POST':
        obj_prdata = mPurchase.Purchase_model()
        jsondata = json.loads(request.body.decode('utf-8'))
        podetails = jsondata.get('params').get('podetails')
        if podetails == []:
            poheader_gid = '0'
        else:
            poheader_gid = podetails[0].get('poheader_gid')
        if poheader_gid == '':
            obj_prdata.action = jsondata.get('params').get('action')
            obj_prdata.date = datetime.datetime.now().date()
            obj_prdata.supplier_gid = podetails[0].get('supplier_gid')
            obj_prdata.teamandcont_gid = podetails[0].get('teamandcont_gid')
            obj_prdata.amount = jsondata.get('params').get('total_amount')
            obj_prdata.amement_gid = podetails[0].get('amement_gid')
            obj_prdata.vesion_gid = podetails[0].get('vesion_gid')
            obj_prdata.from_date = datetime.datetime.strptime(jsondata.get('params').get('from_date'),
                                                              "%d/%m/%Y").strftime("%Y-%m-%d")
            obj_prdata.to_date = datetime.datetime.strptime(jsondata.get('params').get('to_date'), "%d/%m/%Y").strftime(
                "%Y-%m-%d")
            obj_prdata.Employee_gid = request.session['Emp_gid']
            obj_prdata.status = jsondata.get('params').get('status')
            obj_prdata.entity_gid = request.session['Entity_gid']
            data = obj_prdata.set_poheader()[0].split(',')
            if data != "Error":
                for x in podetails:
                    obj_prdata.poheader_gid = data[0]
                    obj_prdata.product_gid = x.get('product_gid')
                    obj_prdata.product_qty = x.get('podetails_qty')
                    obj_prdata.umo_gid = x.get('podetails_uom')
                    obj_prdata.per_unitamt = x.get('podetails_unitprice')
                    obj_prdata.amount = x.get('podetails_amount')
                    obj_prdata.taxamt = x.get('podetails_taxamount')
                    obj_prdata.netamount = x.get('podetails_totalamount')
                    obj_prdata.entity_gid = request.session['Entity_gid']
                    obj_prdata.Employee_gid = request.session['Emp_gid']
                    data1 = obj_prdata.set_podetails()[0].split(',')
                    dataout1 = data1[1].split(',')
                    prdtlgid = 0
                    prptgid = 0
                    if data1 != "Error":
                        if x.get('godown') != None:
                            for y in x.get('godown'):
                                if y.get('godown_incharge') != "":
                                    obj_prdata.action = 'Insert'
                                    obj_prdata.poheader_gid = data[0]
                                    obj_prdata.podetails_gid = data1[0]
                                    obj_prdata.product_gid = x.get('product_gid')
                                    obj_prdata.product_qty = y.get('godown_qty')
                                    obj_prdata.godown_gid = y.get('godown_gid')
                                    obj_prdata.entity_gid = request.session['Entity_gid']
                                    obj_prdata.Employee_gid = request.session['Emp_gid']
                                    obj_prdata.delivery_gid = 0
                                    data2 = obj_prdata.set_podelivery()[0].split(',')
                        if x.get('prpopty') != None:
                            for z in x.get('prpopty'):

                                prdtlgid = z.get("prdetail_gid")
                                if prdtlgid == 0 or prdtlgid == None:
                                    prdtlgid = z.get("prdetails_gid")
                                    prptgid = z.get("pr_qty")
                                if prptgid == 0 or prptgid == None:
                                    prptgid = z.get("qty")
                                obj_prdata.action = 'Insert'
                                obj_prdata.poheader_gid = data[0]
                                obj_prdata.podetails_gid = data1[0]
                                obj_prdata.prdetail_gid = prdtlgid
                                obj_prdata.product_qty = prptgid
                                obj_prdata.entity_gid = request.session['Entity_gid']
                                obj_prdata.Employee_gid = request.session['Emp_gid']
                                obj_prdata.prpo_gid = z.get("prpo_gid")
                                data3 = obj_prdata.set_prpoqty()[0].split(',')

                # if obj_prdata.status == "Pending for Approval":
                #     if dataout1 == "SUCCESS":
                #         obj_prdata.action = 'Insert'
                #         obj_prdata.ref_gid = 1
                #         obj_prdata.reftable = obj_prdata.prheader_gid
                #         obj_prdata.status = 'Pending for Approval'
                #         obj_prdata.totype = 'I'
                #         obj_prdata.to = 2
                #         obj_prdata.remark = ''
                #         tran = obj_prdata.set_trans()[0].split(',')
                return JsonResponse(json.dumps(dataout1), safe=False)
            else:
                return JsonResponse(json.dumps(data), safe=False)
        else:
            if poheader_gid != '0':
                obj_prdata.action = jsondata.get('params').get('action')
                obj_prdata.poheader_gid = poheader_gid
                obj_prdata.amount = jsondata.get('params').get('total_amount')
                podelete = jsondata.get('params').get('podelete')
                obj_prdata.from_date = datetime.datetime.strptime(jsondata.get('params').get('from_date'),
                                                                  "%d/%m/%Y").strftime("%Y-%m-%d")
                obj_prdata.to_date = datetime.datetime.strptime(jsondata.get('params').get('to_date'),
                                                                "%d/%m/%Y").strftime(
                    "%Y-%m-%d")

                obj_prdata.teamandcont_gid = podetails[0].get('teamandcont_gid')
                obj_prdata.entity_gid = request.session['Entity_gid']
                obj_prdata.create_by = request.session['Emp_gid']
                data = obj_prdata.set_poheaderupdate()[0].split(',')
                if data != "Error":
                    for x in podetails:
                        prdtlgid = 0
                        if x.get('podetail_gid') == "":
                            obj_prdata.poheader_gid = data[0]
                            obj_prdata.product_gid = x.get('product_gid')
                            obj_prdata.product_qty = x.get('podetails_qty')
                            obj_prdata.umo_gid = x.get('podetails_uom')
                            obj_prdata.per_unitamt = x.get('podetails_unitprice')
                            obj_prdata.amount = x.get('podetails_amount')
                            obj_prdata.taxamt = x.get('podetails_taxamount')
                            obj_prdata.netamount = x.get('podetails_totalamount')
                            obj_prdata.entity_gid = request.session['Entity_gid']
                            obj_prdata.Employee_gid = request.session['Emp_gid']
                            data1 = obj_prdata.set_podetails()

                            prptgid = 0
                            if data1 != "Error":
                                for y in x.get('godown'):
                                    if y.get('godown_deivery_gid') == 0:
                                        obj_prdata.action = 'Insert'
                                        obj_prdata.poheader_gid = data[0]
                                        obj_prdata.podetails_gid = data1[0]
                                        obj_prdata.product_gid = x.get('product_gid')
                                        obj_prdata.product_qty = y.get('godown_qty')
                                        obj_prdata.godown_gid = y.get('godown_gid')
                                        obj_prdata.entity_gid = request.session['Entity_gid']
                                        obj_prdata.Employee_gid = request.session['Emp_gid']
                                        obj_prdata.delivery_gid = y.get('godown_deivery_gid')
                                        data2 = obj_prdata.set_podelivery()[0].split(',')
                                    else:
                                        obj_prdata.action = 'Update'
                                        obj_prdata.poheader_gid = data[0]
                                        obj_prdata.podetails_gid = data1[0]
                                        obj_prdata.product_gid = x.get('product_gid')
                                        obj_prdata.product_qty = y.get('godown_qty')
                                        obj_prdata.godown_gid = y.get('godown_Gid')
                                        obj_prdata.entity_gid = request.session['Entity_gid']
                                        obj_prdata.Employee_gid = request.session['Emp_gid']
                                        obj_prdata.delivery_gid = y.get('godown_deivery_gid')
                                        data3 = obj_prdata.set_podelivery()[0].split(',')
                                for z in x.get('prpopty'):
                                    prdtlgid = z.get("prdetail_gid")
                                    if prdtlgid == 0 or prdtlgid == None:
                                        prdtlgid = z.get("prdetails_gid")
                                        prptgid = z.get("pr_qty")
                                    if prptgid == 0 or prptgid == None:
                                        prptgid = z.get("qty")

                                        obj_prdata.action = 'Insert'
                                        obj_prdata.poheader_gid = data[0]
                                        obj_prdata.podetails_gid = data1[0]
                                        obj_prdata.prdetail_gid = z.get('prdetail_gid')
                                        obj_prdata.product_qty = prptgid
                                        obj_prdata.entity_gid = request.session['Entity_gid']
                                        obj_prdata.Employee_gid = request.session['Emp_gid']
                                        obj_prdata.prpo_gid = z.get('prpo_gid')
                                        data4 = obj_prdata.set_prpoqty()[0].split(',')
                                    else:
                                        obj_prdata.action = 'Update'
                                        obj_prdata.poheader_gid = data[0]
                                        obj_prdata.podetails_gid = data1[0]
                                        obj_prdata.prdetail_gid = z.get('prdetail_gid')
                                        obj_prdata.product_qty = z.get('pr_qty')
                                        obj_prdata.entity_gid = request.session['Entity_gid']
                                        obj_prdata.Employee_gid = request.session['Emp_gid']
                                        obj_prdata.prpo_gid = z.get('prpo_gid')
                                        data5 = obj_prdata.set_prpoqty()[0].split(',')
                        else:
                            prdtlgid = 0
                            prdtlgid = x.get('podetails_gid')
                            if prdtlgid == 0 or prdtlgid == None:
                                prdtlgid = x.get("podetail_gid")
                            obj_prdata.podetails_gid = prdtlgid
                            obj_prdata.product_gid = x.get('product_gid')
                            obj_prdata.product_qty = x.get('podetails_qty')
                            obj_prdata.per_unitamt = x.get('podetails_unitprice')
                            obj_prdata.amount = x.get('podetails_amount')
                            obj_prdata.taxamt = x.get('podetails_taxamount')
                            obj_prdata.netamount = x.get('podetails_totalamount')
                            obj_prdata.Employee_gid = request.session['Emp_gid']
                            data1 = outputSplit(obj_prdata.set_podetailupdate(), 1)

                            prptgid = 0
                            if data1 != "Error":
                                if x.get('godown') != None:
                                    for y in x.get('godown'):
                                        if y.get('godown_deivery_gid') == 0:
                                            obj_prdata.action = 'Insert'
                                            obj_prdata.poheader_gid = obj_prdata.poheader_gid
                                            obj_prdata.podetails_gid = prdtlgid
                                            obj_prdata.product_gid = x.get('product_gid')
                                            obj_prdata.product_qty = y.get('godown_qty')
                                            obj_prdata.godown_gid = y.get('godown_gid')
                                            obj_prdata.entity_gid = request.session['Entity_gid']
                                            obj_prdata.Employee_gid = request.session['Emp_gid']
                                            obj_prdata.delivery_gid = y.get('godown_deivery_gid')
                                            data2 = obj_prdata.set_podelivery()[0].split(',')
                                        else:
                                            obj_prdata.action = 'Update'
                                            obj_prdata.poheader_gid = obj_prdata.poheader_gid
                                            obj_prdata.podetails_gid = obj_prdata.podetails_gid
                                            obj_prdata.product_gid = x.get('product_gid')
                                            obj_prdata.product_qty = y.get('godown_qty')
                                            obj_prdata.godown_gid = y.get('godown_gid')
                                            obj_prdata.entity_gid = request.session['Entity_gid']
                                            obj_prdata.Employee_gid = request.session['Emp_gid']
                                            obj_prdata.delivery_gid = y.get('godown_deivery_gid')
                                            data3 = obj_prdata.set_podelivery()[0].split(',')

                                if x.get('prpopty') != None:
                                    for z in x.get('prpopty'):
                                        if prdtlgid == 0 or prdtlgid == None:
                                            prdtlgid = z.get("prdetails_gid")
                                            prptgid = z.get("pr_qty")
                                        if prptgid == 0 or prptgid == None:
                                            prptgid = z.get("qty")

                                            obj_prdata.action = 'Insert'
                                            obj_prdata.poheader_gid = obj_prdata.poheader_gid
                                            obj_prdata.podetails_gid = obj_prdata.podetails_gid
                                            obj_prdata.prdetail_gid = z.get('prdetail_gid')
                                            obj_prdata.product_qty = prptgid
                                            obj_prdata.entity_gid = request.session['Entity_gid']
                                            obj_prdata.Employee_gid = request.session['Emp_gid']
                                            obj_prdata.prpo_gid = z.get('prpo_gid')
                                            data4 = obj_prdata.set_prpoqty()[0].split(',')
                                        else:
                                            obj_prdata.action = 'Update'
                                            obj_prdata.poheader_gid = obj_prdata.poheader_gid
                                            obj_prdata.podetails_gid = obj_prdata.podetails_gid
                                            obj_prdata.prdetail_gid = z.get('prdetail_gid')
                                            obj_prdata.product_qty = z.get('pr_qty')
                                            obj_prdata.entity_gid = request.session['Entity_gid']
                                            obj_prdata.Employee_gid = request.session['Emp_gid']
                                            obj_prdata.prpo_gid = z.get('prpo_gid')
                                            data5 = obj_prdata.set_prpoqty()[0].split(',')
                    if data1 == "SUCCESS":
                        for podel in podelete:
                            obj_prdata.podetails_gid = podel
                            obj_prdata.Employee_gid = request.session['Emp_gid']
                            obj_prdata.entity_gid = request.session['Entity_gid']
                            datapodel = obj_prdata.set_podetele()[0].split(',')

                        podeliverydelete = jsondata.get('params').get('podeliverydelete')

                        if podeliverydelete != None:
                            for podeliverydel in podeliverydelete:
                                obj_prdata.action = 'Delete'
                                obj_prdata.poheader_gid = 0
                                obj_prdata.podetails_gid = 0
                                obj_prdata.product_gid = 0
                                obj_prdata.product_qty = 0
                                obj_prdata.godown_gid = 0
                                obj_prdata.entity_gid = request.session['Entity_gid']
                                obj_prdata.Employee_gid = request.session['Emp_gid']
                                obj_prdata.delivery_gid = podeliverydel
                                data3 = obj_prdata.set_podelivery()[0].split(',')

                    if obj_prdata.status == "Pending for Approval":
                        if data1 == "SUCCESS":
                            obj_prdata.action = 'Insert'
                            obj_prdata.ref_gid = 1
                            obj_prdata.reftable = obj_prdata.prheader_gid
                            obj_prdata.status = 'Pending for Approval'
                            obj_prdata.totype = 'I'
                            obj_prdata.to = 2
                            obj_prdata.remark = ''
                            tran = obj_prdata.set_trans()[0].split(',')

                    return JsonResponse(data1, safe=False)
                else:
                    return JsonResponse(data, safe=False)
            else:
                podelete = jsondata.get('params').get('podelete')
                for podel in podelete:
                    obj_prdata.podetails_gid = podel
                    obj_prdata.Employee_gid = request.session['Emp_gid']
                    obj_prdata.entity_gid = request.session['Entity_gid']
                    datapodel = obj_prdata.set_podetele()[0].split(',')

                podeliverydelete = jsondata.get('params').get('podeliverydelete')

                if podeliverydelete != None:
                    for podeliverydel in podeliverydelete:
                        obj_prdata.action = 'Delete'
                        obj_prdata.poheader_gid = 0
                        obj_prdata.podetails_gid = 0
                        obj_prdata.product_gid = 0
                        obj_prdata.product_qty = 0
                        obj_prdata.godown_gid = 0
                        obj_prdata.entity_gid = request.session['Entity_gid']
                        obj_prdata.Employee_gid = request.session['Emp_gid']
                        obj_prdata.delivery_gid = podeliverydel
                        data3 = obj_prdata.set_podelivery()[0].split(',')


                return JsonResponse(datapodel, safe=False)


def outputSplit(tubledtl, index):
    temp = tubledtl[0].split(',')
    if (len(temp) > 1):
        if (index == 0):
            return int(temp[0])
        else:
            return temp[1]
    else:
        return temp[0]


def Getprstatus(request):
    utl.check_authorization(request)
    if request.method == 'GET':
        obj_status_get = mPurchase.Purchase_model()
        data = obj_status_get.get_prstatus()
        jdata = data.to_json(orient='records')
        return JsonResponse(json.loads(jdata), safe=False)


def getpoadmentment(request):
    utl.check_authorization(request)
    if request.method == 'GET':
        obj_adment = mPurchase.Purchase_model()
        data = obj_adment.get_poadment()
        jdata = data.to_json(orient='records')
        return JsonResponse(json.loads(jdata), safe=False)


def getpoadmentmentapp(request):
    utl.check_authorization(request)
    if request.method == 'GET':
        obj_adment = mPurchase.Purchase_model()
        data = obj_adment.get_poadmentapproval()
        jdata = data.to_json(orient='records')
        return JsonResponse(json.loads(jdata), safe=False)


def get_grnheadersumry(request):
    utl.check_authorization(request)
    if request.method == 'POST':
        path=request.path
        obj_grnheader = mPurchase.Purchase_model()
        jsondata = json.loads(request.body.decode('utf-8'))
        obj_grnheader.type = jsondata.get('Params').get('type')
        obj_grnheader.action = jsondata.get('Params').get('Action')
        filter = jsondata.get('Params').get('filter')
        obj_grnheader.filter = json.dumps(filter)
        classification = jsondata.get('Params').get('classification')
        obj_grnheader.classification = json.dumps(classification)
        common.main_fun1(request.read(), path)
        data = obj_grnheader.get_grnheader()
        jdata = data.to_json(orient='records')
        return JsonResponse(json.loads(jdata), safe=False)


def get_grndetails(request):
    utl.check_authorization(request)
    if request.method == 'POST':
        obj_grnheader = mPurchase.Purchase_model()
        jsondata = json.loads(request.body.decode('utf-8'))
        obj_grnheader.grnheader_gid = jsondata.get('params').get('grnheader_gid')
        obj_grnheader.supplier_gid = jsondata.get('params').get('grnheader_supplier_gid')
        data = obj_grnheader.get_grndetails()
        jdata = data.to_json(orient='records')
        return JsonResponse(json.loads(jdata), safe=False)


def set_grnheader(request):
    utl.check_authorization(request)
    if request.method == 'POST':
        obj_grnheader = mPurchase.Purchase_model()
        obj_grnheader.grnheader_gid = ""
        obj_grnheader.supplier_gid = ""
        data = obj_grnheader.get_grndetails()
        jdata = data.to_json(orient='records')
        return JsonResponse(json.loads(jdata), safe=False)


def set_grndetails(request):
    utl.check_authorization(request)
    if request.method == 'POST':
        obj_grnheader = mPurchase.Purchase_model()
        obj_grnheader.grnheader_gid = ""
        obj_grnheader.supplier_gid = ""
        data = obj_grnheader.set_grndetails()
        jdata = data.to_json(orient='records')
        return JsonResponse(json.loads(jdata), safe=False)


def set_grnapproval(request):
    utl.check_authorization(request)
    if request.method == 'POST':
        path=request.path
        obj_maker = mPurchase.Purchase_model()
        jsondata = json.loads(request.body.decode('utf-8'))
        obj_maker.action = jsondata.get('params').get('action')
        obj_maker.grnheader_gid = jsondata.get('params').get('grnheader_gid')

        obj_maker.remark = ' ' if jsondata.get('params').get('remarks') == None else jsondata.get('params').get(
            'remarks')

        obj_maker.Employee_gid = decry_data(request.session['Emp_gid'])
        obj_maker.entity_gid = decry_data(request.session['Entity_gid'])
        common.main_fun1(request.read(), path)
        data = obj_maker.set_grnapproval()
        return JsonResponse(json.dumps(data), safe=False)


def get_grnapprovalget(request):
    utl.check_authorization(request)
    if request.method == 'GET':
        obj_grnheader = mPurchase.Purchase_model()
        obj_grnheader.grnheader_gid = 0
        obj_grnheader.supplier_gid = 0
        data = obj_grnheader.get_grnapprovalset()
        jdata = data.to_json(orient='records')
        return JsonResponse(json.loads(jdata), safe=False)


def get_querystring(request):
    utl.check_authorization(request)
    if request.method == 'GET':
        obj_grnheader = mPurchase.Purchase_model()
        obj_grnheader.poheader_gid = 0
        obj_grnheader.podetail_gid = 0
        obj_grnheader.entity_gid = request.session['Entity_gid']
        data = obj_grnheader.get_querystring()
        jdata = data.to_json(orient='records')
        return JsonResponse(json.loads(jdata), safe=False)


def get_grnpoheaderdetails(request):
    utl.check_authorization(request)
    if request.method == "POST":
        obj_grnpo = mPurchase.Purchase_model()
        jsondata = json.loads(request.body.decode('utf-8'))
        obj_grnpo.grnheader_gid = jsondata.get('params').get('grnheader_gid')
        obj_grnpo.supplier_gid = jsondata.get('params').get('supplier_gid')
        data = obj_grnpo.get_pogrndetails()
        jdata = data.to_json(orient='records')
        return JsonResponse(json.loads(jdata), safe=False)
 #commodity
def commodity(request):
    utl.check_authorization(request)
    return render(request, "pur_commodity.html")
#Commodity Add
def commodityadd(request):
    utl.check_pointaccess(request)
    return render(request, "pur_AddCommodity.html")




#commo_product
def commo_product(request):
    utl.check_authorization(request)
    if request.method == 'POST':
        obj_producategory_ddl = mPurchase.Purchase_model()
        jsondata = json.loads(request.body.decode('utf-8'))
        obj_producategory_ddl.value = jsondata.get('Action')
        obj_producategory_ddl.value1 = json.dumps(jsondata.get('data').get('Params').get('FILTER'))
        Employee_gid = decry_data(request.session['Emp_gid'])
        entity_gid = decry_data(request.session['Entity_gid'])
        obj_producategory_ddl.value2 = json.dumps({'Entity_Gid': entity_gid, 'Create_By': Employee_gid})
        df_customer_ddl = obj_producategory_ddl.commo_productmap()
        return JsonResponse(json.dumps(df_customer_ddl), safe=False)


 #commodity
def commoditydropdown(request):
    utl.check_authorization(request)
    if request.method == 'POST':
        jsondata = json.loads(request.body.decode('utf-8'))
        obj_commodity = mPurchase.Purchase_model()
        obj_commodity.action = jsondata.get('Action')
        obj_commodity.type = jsondata.get('Type')
        Entity_gid = decry_data(request.session['Entity_gid'])
        jsondata['Params']['CLASSIFICATION']['Entity_Gid'] = Entity_gid
        obj_commodity.classification_json = json.dumps(jsondata.get('Params').get('CLASSIFICATION'))
        obj_commodity.jsondata = json.dumps(jsondata.get('Params').get('FILTER'))
        df = obj_commodity.get_commodity_master()
        jdata = df.to_json(orient='records')
        return JsonResponse(json.loads(jdata), safe=False)



# # supplier dropdown
# def supplier_dropdown(request):
#     utl.check_authorization(request)
#     if request.method == 'POST':
#         obj_producategory_ddl = mPurchase.Purchase_model()
#         jsondata = json.loads(request.body.decode('utf-8'))
#         obj_producategory_ddl.action = jsondata.get('Action')
#         obj_producategory_ddl.json_data = json.dumps(jsondata.get('data').get('Params').get('FILTER'))
#         obj_producategory_ddl.entity_gid =request.session['Entity_gid']
#         df_customer_ddl = obj_producategory_ddl.supplier_drop()
#         jdata = df_customer_ddl.to_json(orient='records')
#         return JsonResponse(json.loads(jdata), safe=False)

# # prbased ccbs
# def prdetails_ccbs(request):
#     utl.check_authorization(request)
#     if request.method == 'POST':
#         obj_producategory_ddl = mPurchase.Purchase_model()
#         jsondata = json.loads(request.body.decode('utf-8'))
#         obj_producategory_ddl.Type = jsondata.get('Type')
#         obj_producategory_ddl.Sub_type = jsondata.get('Sub_type')
#         obj_producategory_ddl.json_data = json.dumps(jsondata.get('data').get('Params').get('FILTER'))
#         obj_producategory_ddl.json_classification = json.dumps(jsondata.get('data').get('Params').get('CLASSIFICATION'))
#         obj_producategory_ddl.create_by =request.session['Emp_gid']
#         df_customer_ddl = obj_producategory_ddl.prccbs_details()
#         jdata = df_customer_ddl.to_json(orient='records')
#         return JsonResponse(json.loads(jdata), safe=False)

#commodity save
def commosave(request):
    utl.check_authorization(request)
    if request.method == 'POST':
        obj_producategory_ddl = mPurchase.Purchase_model()
        jsondata = json.loads(request.body.decode('utf-8'))
        obj_producategory_ddl.value = jsondata.get('Action')
        obj_producategory_ddl.value1 = json.dumps(jsondata.get('data').get('Params').get('FILTER'))
        Employee_gid = decry_data(request.session['Emp_gid'])
        entity_gid = decry_data(request.session['Entity_gid'])
        obj_producategory_ddl.value2 = json.dumps({'Entity_Gid':entity_gid,'Create_By':Employee_gid})
        df_customer_ddl = obj_producategory_ddl.dimdimmod()
        return JsonResponse(json.dumps(df_customer_ddl), safe=False)


def activeInactiveget(request):
    if request.method == 'POST':
        obj_producategory_ddl = mPurchase.Purchase_model()
        jsondata = json.loads(request.body.decode('utf-8'))
        obj_producategory_ddl.action = jsondata.get('Action')
        obj_producategory_ddl.jsonData = json.dumps(jsondata.get('data'))
        obj_producategory_ddl.entity_gid = decry_data(request.session['Entity_gid'])
        df_customer_ddl = obj_producategory_ddl.get_allactive_Inactivedata()
        json_data = json.loads(df_customer_ddl.to_json(orient='records'))
        return JsonResponse({"MESSAGE": "FOUND", "DATA": json_data})


#PRcat and subcategory
def pr_productcategory(request):
    utl.check_authorization(request)
    if request.method == 'POST':
        obj_producategory_ddl = mPurchase.Purchase_model()
        jsondata =json.loads(request.body.decode('utf-8'))
        path=request.path
        obj_producategory_ddl.type=jsondata.get('Type')
        obj_producategory_ddl.action=jsondata.get('Action')
        obj_producategory_ddl.data=json.dumps(jsondata.get('main_data'))
        obj_producategory_ddl.classification_json=json.dumps(jsondata.get('classification'))
        common.main_fun1(request.read(), path)
        df_customer_ddl = obj_producategory_ddl.get_pr_productcategory()
        jdata = df_customer_ddl.to_json(orient='records')
        return JsonResponse(json.loads(jdata), safe=False)


#PR product
def pr_product(request):
    utl.check_authorization(request)
    if request.method == 'POST':
        obj_producategory_ddl = mPurchase.Purchase_model()
        jsondata = json.loads(request.body.decode('utf-8'))
        obj_producategory_ddl.producttype_gid = str(jsondata)
        df_customer_ddl = obj_producategory_ddl.get_pr_productname()
        jdata = df_customer_ddl.to_json(orient='records')
        return JsonResponse(json.loads(jdata), safe=False)

#PR Commodity data get
def commodity_pdata(request):
    utl.check_authorization(request)
    if request.method == 'POST':
        obj_producategory_ddl = mPurchase.Purchase_model()
        path=request.path
        jsondata = json.loads(request.body.decode('utf-8'))
        obj_producategory_ddl.action = jsondata.get('Action')
        obj_producategory_ddl.pgid = json.dumps(jsondata.get('data'))
        # obj_producategory_ddl.engid = json.dumps(jsondata.get('endata'))
        value = decry_data(request.session['Entity_gid'])
        obj_producategory_ddl.engid = json.dumps({"Entity_Gid": value})
        common.main_fun1(request.read(), path)
        df_customer_ddl = obj_producategory_ddl.Commodity_product_data()
        jdata = df_customer_ddl.to_json(orient='records')
        return JsonResponse(json.loads(jdata), safe=False)


def render_to_pdf(template_src, context_dict):
    template = get_template(template_src)
    html = template.render(context_dict)
    result = BytesIO()
    pdf = pisa.pisaDocument(BytesIO(html.encode("cp1252")), result)
    if not pdf.err:
        return HttpResponse(result.getvalue(), content_type='application/pdf')
    return None


#generateddl

def generateddl(request):
    utl.check_authorization(request)
    if request.method == 'POST':
        path=request.path
        obj_producategory_ddl = mPurchase.Purchase_model()
        jsondata = json.loads(request.body.decode('utf-8'))
        obj_producategory_ddl.action = 'GET'
        obj_producategory_ddl.sub_type = 'PO_CONTACT_DETAIL'
        obj_producategory_ddl.jdata = json.dumps(jsondata)
        Entity_gid=decry_data(request.session['Entity_gid'])
        obj_producategory_ddl.entity_gid = json.dumps({'Entity_Gid':Entity_gid})
        common.main_fun1(request.read(), path)
        df_customer_ddl = obj_producategory_ddl.get_generatepoddl()
        df_customer_ddl['ip']=ip
        jdata = df_customer_ddl.to_json(orient='records')
        return JsonResponse(json.loads(jdata), safe=False)



def generateddl_download(request):
    if request.method == 'POST':
        obj_producategory_ddl = mPurchase.Purchase_model()
        jsondata = json.loads(request.body.decode('utf-8'))
        obj_producategory_ddl.action = 'GET'
        obj_producategory_ddl.sub_type = 'PO_CONTACT_DETAIL'
        obj_producategory_ddl.jdata = json.dumps(jsondata)
        Entity_gid=decry_data(request.session['Entity_gid'])
        obj_producategory_ddl.entity_gid = json.dumps({'Entity_Gid':Entity_gid})
        df_customer_ddl = obj_producategory_ddl.get_generatepoddl()
        df_customer_ddl['ip']=ip
        jdata = df_customer_ddl.to_json(orient='records')
        data = json.loads(jdata)
        v = data[0]
        a = v['poheader_amount']
        v['poheader_amount'] = "{0:.2f}".format(a)
        de = {}
        v['product_detail'] = json.loads(v['product_detail'])
        for e in v["product_detail"]:
            r = e['podetails_unitprice']
            r1 = e['podetails_totalamount']
            e['podetails_unitprice'] = "{0:.2f}".format(r)
            e['podetails_totalamount'] = "{0:.2f}".format(r1)
            de['address_1'] = e['address_1']
            de['address_2'] = e['address_2']
            de['address_3'] = e['address_3']
            de['address_pincode'] = e['address_pincode']
            de['branch_metadatavalue'] = e['branch_metadatavalue']
            for i in range(len(v["product_detail"])):
                v["product_detail"][i]["address"] = [de]

        v['productdetails'] = json.loads(v['productdetails'])

        v['potermstemplatedes'] = json.loads(v['potermstemplatedes'])
        response = v
        ary=[]
        for json_dict in response.get('productdetails'):
            for key, value in json_dict.items():
                ary.append({"keydata": key, "valuedata": value})
        response['productdetails'] = ary
        pdf = render_to_pdf(BASE_DIR + '/Bigflow/Purchase/templates/PO.html', response)
        pdf2 = pdf
        return pdf2








#commodity_generate_code
def commodity_code_gen(request):
    utl.check_authorization(request)
    if request.method == 'POST':
        obj_producategory_ddl = mPurchase.Purchase_model()
        jsondata = json.loads(request.body.decode('utf-8'))
        obj_producategory_ddl.type = jsondata.get('Type')
        obj_producategory_ddl.sub_type = jsondata.get('Sub_Type')
        obj_producategory_ddl.filter_json = json.dumps(jsondata.get('data').get('Params').get('FILTER'))
        obj_producategory_ddl.classification_json = json.dumps(jsondata.get('data').get('Params').get('CLASSIFICATION'))
        df_customer_ddl = obj_producategory_ddl.codegen_commodity()
        return JsonResponse(df_customer_ddl, safe=False)


def get_grnheader(request):
    utl.check_authorization(request)
    if request.method == 'POST':
        obj_prdata = mPurchase.Purchase_model()
        jsondata = json.loads(request.body.decode('utf-8'))
        grndetails = jsondata.get('params').get('grndetlist')
        grnheader = jsondata.get('params').get('objgrnheader')
        grnheader_gid = grnheader.get('grnheader_gid')
        if grnheader_gid == None:
            obj_prdata.action = grnheader.get('type')
            obj_prdata.date = datetime.datetime.strptime(grnheader.get('grnheader_received'), "%d/%m/%Y").strftime(
                "%Y-%m-%d")
            obj_prdata.dcno = grnheader.get('grnheader_dcno')
            obj_prdata.invoice_no = grnheader.get('grnheader_invno')
            obj_prdata.remark = grnheader.get('grnheader_remarks')
            obj_prdata.Employee_gid = request.session['Emp_gid']
            obj_prdata.entity_gid = request.session['Entity_gid']
            data = obj_prdata.set_grnheader()[0].split(',')
            if data != "Error":
                for x in grndetails:
                    if x.get('is_check') == True:
                        obj_prdata.action = 'insert'
                        obj_prdata.grnheader_gid = data[0]
                        obj_prdata.poheader_gid = x.get('poheader_gid')
                        obj_prdata.podetails_gid = x.get('podetails_gid')
                        obj_prdata.product_qty = x.get('current_qty')
                        obj_prdata.godown_gid = x.get('podelivery_godown_gid')
                        obj_prdata.Employee_gid = request.session['Emp_gid']
                        obj_prdata.entity_gid = request.session['Entity_gid']
                        data1 = obj_prdata.set_grndetails()[0].split(',')
                        dataout1 = data1[1]
                return JsonResponse(json.dumps(dataout1), safe=False)
            else:
                return JsonResponse(json.dumps(data), safe=False)
        else:
            obj_prdata.action = grnheader.get('type')
            obj_prdata.date = datetime.datetime.strptime(grnheader.get('grnheader_received'), "%d/%m/%Y").strftime(
                "%Y-%m-%d")
            obj_prdata.dcno = grnheader.get('grnheader_dcno')
            obj_prdata.grnheader_gid = grnheader_gid
            obj_prdata.invoice_no = grnheader.get('grnheader_invno')
            obj_prdata.remark = grnheader.get('grnheader_remarks')
            obj_prdata.Employee_gid = request.session['Emp_gid']
            obj_prdata.entity_gid = request.session['Entity_gid']
            data = obj_prdata.set_grnheaderupdate()[0].split(',')
            # data = obj_prdata.set_grnheaderupdate()[0].split(',')
            if data != "Error":
                for x in grndetails:
                    if x.get('is_check') == True:
                        if x.get('grninwarddetails_gid') == None:
                            obj_prdata.action = 'insert'
                            obj_prdata.grnheader_gid = grnheader_gid
                            obj_prdata.poheader_gid = x.get('poheader_gid')
                            obj_prdata.podetails_gid = x.get('podetails_gid')
                            obj_prdata.product_qty = x.get('current_qty')
                            obj_prdata.godown_gid = x.get('podelivery_godown_gid')
                            obj_prdata.Employee_gid = request.session['Emp_gid']
                            obj_prdata.entity_gid = request.session['Entity_gid']
                            data1 = obj_prdata.set_grndetails()[0].split(',')
                            dataout1 = data1[1]
                        else:
                            obj_prdata.action = 'update'
                            obj_prdata.grnheader_gid = data[0]
                            obj_prdata.grndetail_gid = x.get('grninwarddetails_gid')
                            obj_prdata.poheader_gid = x.get('poheader_gid')
                            obj_prdata.podetails_gid = x.get('podetails_gid')
                            obj_prdata.product_qty = x.get('current_qty')
                            obj_prdata.godown_gid = x.get('podelivery_godown_gid')
                            obj_prdata.Employee_gid = request.session['Emp_gid']
                            obj_prdata.entity_gid = request.session['Entity_gid']
                            data1 = obj_prdata.set_grndetails()[0].split(',')
                            dataout1 = data1[1]
                return JsonResponse(json.dumps(dataout1), safe=False)
            else:
                return JsonResponse(json.dumps(data), safe=False)


def PurchasePlanningIndex(request):
    utl.check_authorization(request)
    return render(request, "PurchasePlanning.html")


# def pr_supplierIndex(request):
#     utl.check_authorization(request)
#     return render(request, "pr_supplier_allocation.html")



def purchasedata(request):
    utl.check_pointaccess(request)
    if request.method == 'GET':
        fdate = common.convertDateTime(request.GET['fromdate'])
        data_perc = 1
        supplier_capcity = 5000
        capacity = {'sup_count': 1, 'sup_capacity': supplier_capcity}
        obj_salesplanning = mPurchase.Purchase_model()

        f_date = fdate
        t_date = f_date + relativedelta(months=+5)

        obj_salesplanning.type = 'Monthwise'
        obj_salesplanning.prod_type_gid = 1
        df_product = obj_salesplanning.get_producttype()

        obj_salesplanning.product_gid = 0
        obj_salesplanning.from_year = f_date.year
        obj_salesplanning.to_year = t_date.year
        obj_salesplanning.from_month = f_date.month
        obj_salesplanning.to_month = t_date.month
        df_salesplan = obj_salesplanning.get_salesplanningl()

        # obj_salesplanning.type = 'Detailswise'
        # obj_salesplanning.product_gid = 0
        # obj_salesplanning.from_year = f_date.year
        # obj_salesplanning.to_year = t_date.year
        # obj_salesplanning.from_month = f_date.month
        # obj_salesplanning.to_month = t_date.month
        # df_salesplandetail = obj_salesplanning.get_salesplanningl()
        # ds = get_mntsales(request,df_salesplandetail)

        df_podetails = obj_salesplanning.get_purchplanningl()
        productdtl = []
        obj_stock = mStock.StockModel()
        obj_stock.type = 'MonthWise_Stock'
        obj_stock.sub_type = ''
        obj_stock.from_date = ''
        obj_stock.to_date = ''
        obj_stock.product_gid = 1
        obj_stock.supplier_gid = 1
        obj_stock.entity_gid = request.session['Entity_gid']
        obj_stock.jsonData = json.dumps({"date": str(f_date + relativedelta(months=-1))})
        openstock = obj_stock.get_stock()
        df_stock = openstock['DATA']
        for x, item in df_product.iterrows():
            productgid = item['product_gid']
            productname = item['product_displayname']
            suppplieruntiprice = item['supplierproduct_unitprice']

            pdtl = {'product_gid': productgid, 'product_name': productname, 'unit_price': suppplieruntiprice,
                    }
            months = []
            temp_date = f_date
            for y in range(0, 4):
                months.append(temp_date.strftime('%m-%Y'))
                pdtl['targetperc' + str(y + 1)] = data_perc

                # closing stock
                nxt_mnt = temp_date + relativedelta(months=+1)
                pdtl['nxtSalePlanQty' + str(y + 1)] = int(
                    df_salesplan[(df_salesplan['salesplandetails_year'] == nxt_mnt.year) & (
                            df_salesplan['product_gid'] == productgid) & (df_salesplan[
                                                                              'salesplandetails_month'] == nxt_mnt.month)][
                        'salqty'].sum())

                # opening stock
                if (y == 0):
                    #pdtl['openStk' + str(y + 1)] = 200
                    for x, item in df_stock.iterrows():
                        productgid1 = item['product_gid']
                        if productgid == productgid1:
                            pdtl['openStk' + str(y + 1)] = item['stockbalance_cb']
                            break

                # sales as on month (Sales planning)
                pdtl['salePlanQty' + str(y + 1)] = int(
                    df_salesplan[(df_salesplan['salesplandetails_year'] == temp_date.year) & (
                            df_salesplan['product_gid'] == productgid) & (
                                         df_salesplan[
                                             'salesplandetails_month'] == temp_date.month)][
                        'salqty'].sum())
                pdtl['ActualSales' + str(y + 1)] = (df_salesplan[(df_salesplan['salesplandetails_year'] == temp_date.year) &
                                                                 (df_salesplan['product_gid'] == productgid) & (
                                         df_salesplan[
                                             'salesplandetails_month'] == temp_date.month) ]['actual_qty'].sum())
                # yearmnth['purPlanQty'] = float(df_podetails[(df_podetails['po_year'] == temp_date.year) & (
                #         df_podetails['product_gid'] == productgid) & (df_podetails['po_month'] == temp_date.month)][
                #                                    'po_quantity'].sum())

                # pending po
                pdtl['pendingPO' + str(y + 1)] = float(df_podetails[(df_podetails['po_year'] == temp_date.year) & (
                        df_podetails['product_gid'] == productgid) & (df_podetails['po_month'] == temp_date.month)][
                                                           'pending_qty'].sum())
                temp_date = temp_date + relativedelta(months=+1)
            productdtl.append(pdtl)
        data = {'productdtl': productdtl, 'months': months, 'capacity': capacity}
        return JsonResponse(data, safe=False)

def get_mntsales(request):
    if request.method == 'POST':
        obj_mntsales = mPurchase.Purchase_model()
        jsondata = json.loads(request.body.decode('utf-8'))
        obj_mntsales.type = 'Detailswise'
        obj_mntsales.prod_type_gid = 0
        obj_mntsales.product_gid = jsondata.get('Product_Gid')
        dt_value = jsondata.get('Date')
        cur_date = datetime.datetime.now()
        if dt_value == "0":
            year_month0 = datetime.datetime.today() + relativedelta(months=0)
            year = year_month0.strftime("%Y")
            month = year_month0.strftime("%m")
        elif dt_value == "1":
            year_month1 = datetime.datetime.today() + relativedelta(months=1)
            year = year_month1.strftime("%Y")
            month = year_month1.strftime("%m")
        elif dt_value == "2":
            year_month2 = datetime.datetime.today() + relativedelta(months=2)
            year = year_month2.strftime("%Y")
            month = year_month2.strftime("%m")
        elif dt_value == "3":
            year_month3 = datetime.datetime.today() + relativedelta(months=3)
            year = year_month3.strftime("%Y")
            month = year_month3.strftime("%m")
        obj_mntsales.from_month = month
        obj_mntsales.to_month = month
        obj_mntsales.from_year = year
        obj_mntsales.to_year = year
        datas = obj_mntsales.get_salesplanningl()
        ldict = datas.to_json(orient='records')
        data = json.loads(ldict)
    return JsonResponse(data,safe=False)

def get_supCapacity(request):
    utl.check_pointaccess(request)
    if request.method == 'GET':
        prsuplierdetails = mPurchase.Purchase_model()
        prsuplierdetails.action = request.GET['action']
        prsuplierdetails.supplier_gid = request.GET['supplier_gid']
        prsuplierdetails.product_gid = request.GET['product_gid']
        prsuplierdetails.product_name = request.GET['product_name']
        prsuplierdetails.serail_no = request.GET['serial_no']
        df_pro = prsuplierdetails.get_poqty()
        # df_pro = json.loads(jdata.to_json(orient='records'))

        prsuplierdetails.action = 'suppliercapacity'
        prsuplierdetails.type = ''
        prsuplierdetails.vendor = '{}'
        sup_details = prsuplierdetails.get_supplier()
        df_supplier = (sup_details[['supplier_gid', 'supplier_name', 'creditlimit_days', 'sup_capacity']]).groupby(
            ['supplier_gid', 'supplier_name', 'creditlimit_days', 'sup_capacity']).size().reset_index();
        df_sup_pro = (sup_details[['product_gid']]).groupby(
            ['product_gid']).size().reset_index(name='counts');
        result = pd.merge(df_pro, df_sup_pro, how='left', on='product_gid').sort_values(by=['counts']).reset_index(
            drop=True)
        supplierlist = json.loads(df_supplier.to_json(orient='records'))
        sup_cap = {}
        for i, item in df_supplier.iterrows():
            sup_cap[item['supplier_gid']] = item['sup_capacity']

        productList = []

        for x, pro in result.iterrows():
            product = {'product_gid': pro['product_gid'], 'product_name': pro['product_name'],
                       'pr_qty': pro['prdetails_qty']}
            supplier = sup_details[sup_details['product_gid'] == pro['product_gid']].sort_values(by=
                                                                                                 ['unitprice',
                                                                                                  'creditlimit_days'],
                                                                                                 ascending=[1,
                                                                                                            0]).reset_index(
                drop=True)
            prqty = pro['prdetails_qty']
            ttl_sup = supplier['supplier_gid'].count()
            remain = prqty
            total = 0
            pro_fill = False
            for y, sup in supplier.iterrows():
                if not pro_fill:
                    capacity = sup_cap[sup['supplier_gid']]
                    remain = capacity - abs(remain)
                    if remain >= 0:
                        product[sup['supplier_gid']] = capacity - remain
                        sup_cap[sup['supplier_gid']] = remain
                        total = total + capacity - remain
                        pro_fill = True;
                    else:
                        product[sup['supplier_gid']] = capacity
                        sup_cap[sup['supplier_gid']] = 0
                        total = total + capacity
                else:
                    product[sup['supplier_gid']] = 0
                if y + 1 == ttl_sup:
                    product['total'] = total
            productList.append(product)
        data = {'product': productList, 'supplier': supplierlist}
        return JsonResponse(data, safe=False)


def get_allqueue_status(request):
    utl.check_pointaccess(request)
    if request.method == "POST":
        obj_allqueuestatus = mPurchase.Purchase_model()
        jsondata = json.loads(request.body.decode('utf-8'))
       
        obj_allqueuestatus.tablename = jsondata.get('params').get('table_name')
        obj_allqueuestatus.ref_gid = jsondata.get('params').get('gid')
        obj_allqueuestatus.status = jsondata.get('params').get('status')
        obj_allqueuestatus.entity_gid = decry_data(request.session['Entity_gid'])
        out_message = outputReturn(obj_allqueuestatus.get_questatus(), 0)
        return JsonResponse(out_message, safe=False)


def outputReturn(tubledtl, index):
    temp = tubledtl[0].split(',')
    if (len(temp) > 1):
        if (index == 0):
            return int(temp[0])
        else:
            return temp[1]
    else:
        return temp[0]


def set_PRDetails(request):
    utl.check_authorization(request)
    if request.method == "POST":
        jsondata = json.loads(request.body.decode('utf-8'))
        action = jsondata.get('action')
        status = jsondata.get('status')
		#type = jsondata.get('type')
        #header = jsondata.get('prheader')
        prdetails = jsondata.get('prdetails')
        #classification = jsondata.get('classificaton')
        pr_amt=jsondata.get('pr_amt')
        prdelete = jsondata.get('prdelete')
        params = {'Action': "" + action + "", 'Employee_Gid': request.session['Emp_gid'] ,
                  'entity_gid':  request.session['Entity_gid'] }
        datas = {"params": {"status": status, "prdetails": prdetails, "prdelete": prdelete,"pr_amt": pr_amt}}
        token = jwt.token(request)
        headers = {"content-type": "application/json", "Authorization": "" + token + ""}
        resp = requests.post("" + ip + "/PurchaseRequest_Set", params=params, data=json.dumps(datas), headers=headers, verify=False)
        response = resp.content.decode("utf-8")
        return HttpResponse(response)

def get_SalesCount(request):
    utl.check_pointaccess(request)
    if request.method == "POST":
        jsondata = json.loads(request.body.decode('utf-8'))
        obj_sales = mPurchase.Purchase_model()
        obj_sales.type = jsondata.get('type')
        obj_sales.sub_type = jsondata.get('sub_type')
        obj_sales.fliter = jsondata.get('fliter')
        obj_sales.classification = jsondata.get('classification')
        obj_sales.create_by = jsondata.get('create_by')
        datas = obj_sales.get_salescount()
        ldict = datas.to_json(orient='records')
        data = json.loads(ldict)
        return JsonResponse(data, safe=False)


def set_grn(request):
    utl.check_authorization(request)
    if request.method == 'POST':
        path=request.path
        obj_ = mPurchase.Purchase_model()
        jsondata = json.loads(request.body.decode('utf-8'))
        obj_.type =  jsondata.get('params').get('type')
        obj_.action = ''
        obj_.jsonData = json.dumps(jsondata.get('params').get('FILTER'))
        Entity_Gid = int(decry_data(request.session['Entity_gid']))
        obj_.json_classification = json.dumps({"Entity_Gid":[Entity_Gid]})
        #obj_.json_classification["Entity_Gid"][0] = request.session['Entity_gid']
        obj_.employee_gid = decry_data(request.session['Emp_gid'])
        # common.main_fun1(request.read(), path)
        ld_out_message = obj_.set_grn_data()
        out_message = outputReturn(ld_out_message, 0)
        return JsonResponse(out_message, safe=False)

def get_grnprocess_details(request):
    utl.check_authorization(request)
    if request.method == 'POST':
        jsondata = json.loads(request.body.decode('utf-8'))
        if ((jsondata.get('params').get('type') == 'GRN') ):
            type = jsondata.get('params').get('type')
            sub_type = jsondata.get('params').get('subtype')
            filter_json = json.dumps(jsondata.get('params').get('filter'))
            entity_gid = request.session['Entity_gid']
            params = {'type': type,'sub_type':sub_type, 'entity_gid': entity_gid}
            token = jwt.token(request)
            headers = {"content-type": "application/json", "Authorization": "" + token + ""}
            result = requests.post("" + ip + "/Get_Grn_Details", params=params, headers=headers, data=filter_json,verify=False)
            results = result.content.decode("utf-8")
            return JsonResponse(json.loads(results), safe=False)

def grndetailsview(request):
    utl.check_authorization(request)
    return render(request, "pur_GrnDetailsView.html")

def get_grnprocessdetails(request):
    utl.check_pointaccess(request)
    if request.method == "POST":
        obj_grnpo = mPurchase.Purchase_model()
        jsondata = json.loads(request.body.decode('utf-8'))
        obj_grnpo.filter_json = jsondata.get('params').get('filter')
        obj_grnpo.type = jsondata.get('params').get('type')
        obj_grnpo.sub_type = jsondata.get('params').get('subtype')
        data = obj_grnpo.grndetails_get()
        jdata = data.to_json(orient='records')
        return JsonResponse(json.loads(jdata), safe=False)


def set_expense_line(request):
    utl.check_pointaccess(request)
    if request.method == "POST":
        jsondata = json.loads(request.body.decode('utf-8'))
        action = jsondata.get('params').get('action')
        type = jsondata.get('params').get('type')
        entity_gid = request.session['Entity_gid']
        create_by = request.session['Emp_gid']
        jsondata["params"]["classification"] = {"Entity_Gid": entity_gid}
        datas = json.dumps(jsondata)
        params = {'action':action,'type': type,'create_by':create_by}
        token = jwt.token(request)
        headers = {"content-type": "application/json", "Authorization": "" + token + ""}
        result = requests.post("" + ip + "/Expense_Line_API", params=params, headers=headers, data=datas,verify=False)
        results = result.content.decode("utf-8")
        return JsonResponse(json.loads(results), safe=False)

# def tense(request):
#     utl.check_authorization(request)
#     return render(request, "finalapprovaltest.html")


def get_MEP_number(request):
    utl.check_authorization(request)
    utl.check_pointaccess(request)
    if request.method == 'POST':
        jsondata = json.loads(request.body.decode('utf-8'))
        Group = jsondata.get('Params').get('Group')
        type = jsondata.get('Params').get('Type')
        subtype = jsondata.get('Params').get('SubType')
        data = jsondata.get('Params')
        entity_gid = request.session['Entity_gid']
        jsondata["Params"]["CLASSIFICATION"]["Entity_Gid"] = entity_gid
        datas = json.dumps(data)
        params = {'Type': type, 'SubType': subtype,'Group':Group}
        token = jwt.token(request)
        headers = {"content-type": "application/json", "Authorization": "" + token + ""}
        result = requests.post("" + ip + "/Mep_In_PR", params=params, headers=headers, data=datas, verify=False)
        results = result.content.decode("utf-8")
        return JsonResponse(json.loads(results), safe=False)






def Pr_approvalget(request):
    utl.check_authorization(request)
    if request.method == 'POST':
        jsondata = json.loads(request.body.decode('utf-8'))
        type = jsondata.get('Params').get('type')
        action = jsondata.get('Params').get('Action')
        if action=='GRN':
                subtype=jsondata.get('Params').get('Sub_type')
                params = {'Type': type, 'Action': action,"Sub_type":subtype}
        else:
            params = {'Type': type, 'Action': action}
        data = jsondata.get('Params').get('filter')
        jsondata['Params']['CLASSIFICATION'] = {'Entity_Gid': request.session['Entity_gid']}
        datas = json.dumps(jsondata)
        token = jwt.token(request)
        headers = {"content-type": "application/json", "Authorization": "" + token + ""}
        result = requests.post("" + ip + "/PO_HeaderDDl", params=params, headers=headers, data=datas, verify=False)
        results = result.content.decode("utf-8")
        return JsonResponse(json.loads(results), safe=False)


def PO_finalinsert(request):
    utl.check_pointaccess(request)
    try:
        if request.method == 'POST':
            path=request.path
            jsondata = json.loads(request.body.decode('utf-8'))
            obj_ = mPurchase.Purchase_model()
            obj_.type = jsondata.get('Params').get('type')
            obj_.action = jsondata.get('Params').get('Action')
            obj_.sub = jsondata.get('Params').get('Subtype')
            data2 = jsondata.get('Params').get('filter')
            notepad = jsondata.get('Params').get('filter').get('Notepad') #{"filter":{'Notepad':"hello world"}}
            if notepad != "":
                millis = int(round(time.time() * 1000))
                filename = request.session['Emp_gid'] + "_" + str(millis) + '.txt'
                file_path = os.path.join(settings.MEDIA_ROOT + '/PRPO/', filename)

                # s3 = boto3.resource('s3')
                # object = s3.Object(common.s3_bucket_name(), filename)
                # object.put(Body=notepad)
                with open(file_path,'x') as txt_file:
                    txt_file.write(notepad)

            else:
                filename = ""
            obj_.filename = filename
            data2.update({"poheader_notepad": filename})
            obj_.datas = json.dumps(data2)
            data1 = json.dumps(jsondata.get('Params').get('filter').get('Header_img'))
            mail_id = jsondata.get('Params').get('filter').get('Emp_mail')
            poddl = json.dumps(jsondata.get('Params').get('filter').get('File'))
            emp = request.session['Emp_gid']
            base64data = json.loads(data1)
            base64ddl = json.loads(poddl)
            obj_.classification_json= json.dumps({'entity_gid':decry_data(request.session['Entity_gid'])})
            obj_.datas = json.dumps(data2)
            obj_.crtb=decry_data(request.session['Emp_gid'])
            common.main_fun1(request.read(), path)

            if mail_id != '':
                obj_data = obj_.po_insert()[0].split(',')
                inward_dtl = mAP.ap_model()
                inward_dtl.action = "GET"
                inward_dtl.type = "MAIL_TEMPLATE"
                inward_dtl.filter = json.dumps({"template_name": "PO",
                                                "header_gid": obj_data[1], "queryname": "PO MAKER"})
                inward_dtl.classification = json.dumps(
                    {"Entity_Gid": decry_data(request.session['Entity_gid']), "Emp_gid": obj_.crtb})
                templates_data = inward_dtl.get_multiple_email_templates_data()
                Mail_Data = templates_data.get("Mail_Data")[0].get("mailtemplate_body")
                Mail_subject = templates_data.get("Mail_Data")[0].get("mailtemplate_subject")
                Header_Data = templates_data.get("Header_Data")[0]
                for (k, v) in Header_Data.items():
                    value = str(v)
                    key = "{{" + k + "}}"
                    Mail_Data = Mail_Data.replace(key, value);
                cleanr = re.compile('<.*?>')
                body_text = re.sub(cleanr, '', Mail_Data)
                data = sending_mail(body_text, mail_id, Mail_subject)
                return HttpResponse(data)
            if mail_id == '':
                obj_data = obj_.po_insert()[0].split(',')
                return HttpResponse(obj_data[0])
    except Exception as e:
        return JsonResponse({"Message": str(e)})






def imageconvert(request):
    utl.check_authorization(request)
    if request.method == 'POST' and request.FILES['file']:
        filename = str(request.FILES['file'])
        millis = int(round(time.time() * 1000))
        concat_filename = request.session['Emp_gid'] + "_" + str(millis) + "_" + filename
        # current_month = datetime.now().strftime('%m')
        # current_day = datetime.now().strftime('%d')
        # current_year_full = datetime.now().strftime('%Y')
        # filename = str(request.FILES['file'])
        # millis = int(round(time.time() * 1000))
        # s1 = str(millis)
        # Create_By = decry_data(request.POST['Create_By'])
        # c1 = str(Create_By)
        # concat_filename = c1 + "_" + s1 + "_" + filename
        save_path = str(settings.MEDIA_ROOT) + '/PRPO/' + concat_filename
        # print(save_path)
        path = default_storage.save(str(save_path), request.FILES['file'])
        # s3 = boto3.resource('s3')
        # s3_obj = s3.Object(bucket_name=common.s3_bucket_name(), key=concat_filename)
        # s3_obj.put(Body=request.FILES['file'])
        return HttpResponse(concat_filename)




import boto3
from botocore.exceptions import ClientError

def sending_mail(mail_data,mail_id,Mail_subject):
    sendermail = common.senderemail()
    SENDER = "Karur Vysya Bank <"+sendermail+">"
    RECIPIENT = mail_id
    AWS_REGION = "ap-south-1"
    SUBJECT = Mail_subject
    BODY_TEXT = ("")
    BODY_HTML = """<html>
    <head></head>
    <body>
    """+mail_data+"""
    </body>
    </html>
                """
    CHARSET = "UTF-8"
    client = boto3.client('ses', region_name=AWS_REGION)
    try:
        # Provide the contents of the email.
        response = client.send_email(
            Destination={
                'ToAddresses': [
                    RECIPIENT,
                ],
            },
            Message={
                'Body': {
                    'Html': {
                        'Charset': CHARSET,
                        'Data': BODY_HTML,
                    },
                    'Text': {
                        'Charset': CHARSET,
                        'Data': BODY_TEXT,
                    },
                },
                'Subject': {
                    'Charset': CHARSET,
                    'Data': SUBJECT,
                },
            },
            Source=SENDER,
        )
    # Display an error if something goes wrong.
    except ClientError as e:
        return (e.response['Error']['Message'])
    else:
        # print(response['MessageId'])
        return 'SUCCESS'



def saveccbs(request):
    utl.check_authorization(request)
    try:
        if request.method == 'POST':
            objdata = mPurchase.Purchase_model()
            path=request.path
            jsondata = json.loads(request.body.decode('utf-8'))
            objdata.action =jsondata.get('Action')
            objdata.type =jsondata.get('Type')
            prheaderddl =jsondata.get('PR_Header').get('HEADER')[0]
            notepad = jsondata.get('PR_Header').get('HEADER')[0].get('Notepad')
            if notepad != "":
                millis = int(round(time.time() * 1000))
                filename = request.session['Emp_gid'] + "_" + str(millis) + '.txt'
                file_path = os.path.join(settings.MEDIA_ROOT + '/PRPO/', filename)

                # s3 = boto3.resource('s3')
                # object = s3.Object(common.s3_bucket_name(), filename)
                # object.put(Body=notepad)
                with open(file_path, 'x') as txt_file:
                    txt_file.write(notepad)
            else:
                filename = ""
            prheaderddl.update({"prheader_notepad": filename})
            objdata.prheaderddl = jsondata.get('PR_Header')
            obj=jsondata.get('PR_Header')
            obj2=jsondata.get('PR_Header').get('HEADER')
            mail_id = jsondata.get('PR_Header').get('HEADER')[0]
            mail_id = mail_id['Emp_mail']
            obj2[0]['Emp_gid']=decry_data(request.session['Emp_gid'])
            Header_img =json.dumps(jsondata.get('Header_img'))
            productsddl=jsondata.get('PR_Products').get('DETAIL')
            objdata.file = json.dumps(jsondata.get('File'))
            objdata.emp =decry_data(request.session['Emp_gid'])
            Entity_gid = decry_data(request.session['Entity_gid'])
            objdata.draft=json.dumps({"Entity_Gid":[Entity_gid]})
            objdata.productsddl = json.dumps({'DETAIL':productsddl})
            objdata.classification_json=json.dumps({"Entity_Gid":[Entity_gid]})
            # common.main_fun1(request.read(), path)
            if mail_id != '':
                obj_data = objdata.insertprccbs()[0].split(',')
                inward_dtl = mAP.ap_model()
                inward_dtl.action = "GET"
                inward_dtl.type = "MAIL_TEMPLATE"
                inward_dtl.filter = json.dumps({"template_name": "PR",
                                                "header_gid": obj_data[1], "queryname": "PR MAKER"})
                inward_dtl.classification = json.dumps(
                    {"Entity_Gid": Entity_gid, "Emp_gid": objdata.emp})
                templates_data = inward_dtl.get_multiple_email_templates_data()
                Mail_Data = templates_data.get("Mail_Data")[0].get("mailtemplate_body")
                Mail_subject = templates_data.get("Mail_Data")[0].get("mailtemplate_subject")
                Header_Data = templates_data.get("Header_Data")[0]
                for (k, v) in Header_Data.items():
                    value = str(v)
                    key = "{{" + k + "}}"
                    Mail_Data = Mail_Data.replace(key, value);
                cleanr = re.compile('<.*?>')
                body_text = re.sub(cleanr, '', Mail_Data)
                data = sending_mail(body_text,mail_id,Mail_subject)
                return HttpResponse(data)
            if mail_id == '':
                obj_data = objdata.insertprccbs()[0].split(',')
                return HttpResponse(obj_data[0])
    except Exception as e:
        return JsonResponse({"Message": str(e)})






from io import  BytesIO
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa
from django.template import Context


def down_pdf_po (request):
    utl.check_pointaccess(request)
    data = {
    }
    pdf = render_PO_pdf(BASE_DIR + '/Bigflow/Purchase/templates/PO.html', data)

    return HttpResponse(pdf, content_type="application/pdf")

import unicodedata
def render_PO_pdf(template_src, context_dict):
    template = get_template(template_src)
    context = Context(context_dict)
    html = template.render(context_dict)
    result =  BytesIO()
    # pdf = pisa.pisaDocument(BytesIO(html.encode("ISO-8859-1")), result)
    pdf = pisa.pisaDocument(BytesIO(html.encode("'UTF-8")), result)
    if not pdf.err:
        return HttpResponse(result.getvalue(), content_type='application/pdf')
    return None

def common_viewfile(request):
    utl.check_authorization(request)
    if request.method == 'POST':
        jsondata = json.loads(request.body.decode('utf-8'))
        filename= jsondata.get('Filename')
        s3_client = boto3.client('s3','ap-south-1')
        file_path = settings.MEDIA_ROOT+'/PRPO/'+filename
        return JsonResponse(file_path, safe=False)

def common_read_file(request):
    if request.method == 'POST':
        jsondata = json.loads(request.body.decode('utf-8'))
        s3_client = boto3.client('s3', 'ap-south-1')
        filename = jsondata.get('Filename')
        filepath = settings.MEDIA_ROOT + '/PRPO/' + filename
        with open(filepath,'r') as filedata:
            file_path = {"file_path":filedata.read()}
        return JsonResponse(file_path, safe=False)

# from decouple import config
from django.core.mail import send_mail
from django.conf import settings


def sendmail(request):
    utl.check_authorization(request)
    try:
        main = json.loads(request.body.decode('utf-8'))
        obj = mPurchase.Purchase_model()
        obj.action,obj.type ='submit','INSERT'

        maine = {"poheader_ondelivery":100}
        main.update(maine)
        jsondata=json.dumps(main)
        Entity_gid = decry_data(request.session['Entity_gid'])
        Emp_gid = decry_data(request.session['Emp_gid'])
        main['tran_to'] =Emp_gid
        PR_ddl=Productddl(jsondata,Entity_gid)
        amc = {"podetails_amcvalue":0}
        delivery = {"podetails_deliveryperiod":1}
        for i in PR_ddl:
            i.update(amc)
            i.update(delivery)
        main['podetails'] = PR_ddl
        main['total_amount'] = PR_ddl[0]['total_amount']
        obj.datas = json.dumps(main)
        obj.classification_json =json.dumps({"entity_gid": Entity_gid})
        obj.sub,obj.crtb = 'APPROVAL',Emp_gid
        po_status = obj.po_insert()
        po_status = "".join(po_status)
        po_status = po_status.split(',')
        if po_status[0]=='SUCCESS':
                subject = "KVB-PO"
                D=PODTS(po_status[1],Entity_gid).to_dict('records')
                d=D[0]
                email = d['Contact_email']
                if email == None or email == '':
                    email = 'vsolvstab@gmail.com'

                a = d['poheader_amount']
                d['poheader_amount'] = "{0:.2f}".format(a)

                de = {}
                d['product_detail'] = json.loads(d['product_detail'])
                for e in d["product_detail"]:
                    r = e['podetails_unitprice']
                    r1 = e['podetails_totalamount']
                    e['podetails_unitprice'] = "{0:.2f}".format(r)
                    e['podetails_totalamount'] = "{0:.2f}".format(r1)
                    de['address_1'] = e['address_1']
                    de['address_2'] = e['address_2']
                    de['address_3'] = e['address_3']
                    de['address_pincode'] = e['address_pincode']
                    de['branch_metadatavalue'] = e['branch_metadatavalue']
                    for i in range(len(d["product_detail"])):
                        d["product_detail"][i]["address"] = [de]
                ary = []
                d['potermstemplatedes'] = json.loads(d['potermstemplatedes'])
                d['productdetails'] = json.loads(d['productdetails'])
                for json_dict in d.get('productdetails'):
                    for key, value in json_dict.items():
                        ary.append({"keydata": key, "valuedata": value})
                d['productdetails'] = ary
                htmly = get_template(BASE_DIR + '/Bigflow/Purchase/templates/Email-temp.html')
                html_content = htmly.render(d)
                email_from = settings.EMAIL_HOST_USER
                send_mail(subject,'aa', email_from,recipient_list=[email],html_message=html_content,fail_silently=False )
    except Exception as response:
        return JsonResponse({"Message":str(response)})

    return JsonResponse({"Message":"Mailsent"})


def mailcheck(request):
    try:
        subject = "KVB-PO"
        email = 'vsolvstab@gmail.com'
        htmly = get_template(BASE_DIR + '/Bigflow/Purchase/templates/Email-temp.html')
        html_content = htmly.render({'a':'d'})
        email_from = settings.EMAIL_HOST_USER
        send_mail(subject, 'aa', email_from, recipient_list=[email], html_message=html_content, fail_silently=False)
        return JsonResponse({"Message": "Mailsent"})
    except Exception as response:
        return JsonResponse({"Message": str(response)})






def PODTS(poid,Entity_Gid):
        obj_producategory_ddl = mPurchase.Purchase_model()
        obj_producategory_ddl.action = 'GET'
        obj_producategory_ddl.sub_type = 'PO_CONTACT_DETAIL'
        obj_producategory_ddl.jdata = json.dumps({"poheader_gid": poid})
        obj_producategory_ddl.entity_gid = json.dumps({'Entity_Gid':Entity_Gid})
        df_customer_ddl = obj_producategory_ddl.get_generatepoddl()
        df_customer_ddl['ip']=ip
        return df_customer_ddl


def Productddl(jsondata,Entity_gid):
    obj_producategory_ddl = mPurchase.Purchase_model()
    obj_producategory_ddl.action = 'INSERT_DTS'
    obj_producategory_ddl.sub_type = ''
    obj_producategory_ddl.jdata =jsondata
    obj_producategory_ddl.entity_gid = json.dumps({'entity_gid': Entity_gid})
    df_customer_ddl = obj_producategory_ddl.get_sendmail()
    return df_customer_ddl


def getpoamend(request):
    utl.check_authorization(request)
    if request.method == 'POST':
        jsondata = json.loads(request.body.decode('utf-8'))
        create_by = request.session['Emp_gid']
        params = {'Group':jsondata.get("Group"),'Action': jsondata.get("Action"), 'Type': jsondata.get("Type"),"create_by":create_by}
        token = jwt.token(request)
        headers = {"content-type": "application/json", "Authorization": "" + token + ""}
        datas = json.dumps(jsondata.get("DETAIL"))
        resp = requests.post("" + ip + "/Get_Poamend", params=params, data=datas, headers=headers, verify=False)
        response = resp.content.decode("utf-8")
        return HttpResponse(response)

def employee_search(request):
    utl.check_pointaccess(request)
    if request.method == 'POST':
        try:
            path = request.path
            jsondata = json.loads(request.body.decode('utf-8'))
            grp = jsondata.get('Params').get('Group')
            limit = jsondata.get('Params').get('Limit')
            typ = jsondata.get('Params').get('Type')
            sub = jsondata.get('Params').get('Sub_Type')
            Entity_gid = int(decry_data(request.session['Entity_gid']))
            params = {"Group": grp, "Type": typ, "Sub_Type": sub, "Limit": limit}
            token = jwt.token(request)
            headers = {"content-type": "application/json", "Authorization": "" + token + ""}
            classify = {
                "CLASSIFICATION": {
                    "Entity_Gid": Entity_gid
                }}
            jsondata['Params'].update(classify)
            datas = json.dumps(jsondata)
            resp = requests.post("" + ip + "/MASTER_DATA", params=params, data=datas, headers=headers,
                                 verify=False)
            response = resp.content.decode("utf-8")
            return HttpResponse(response)
        except Exception as e:
            return JsonResponse({"MESSAGE": "ERROR_OCCURED", "DATA": str(e)})
def agentsummary(request):
    utl.check_authorization(request)
    return render(request, "Agent_summary.html")

def get_trandata(request):
    if request.method == 'POST':
        jsondata = json.loads(request.body.decode('utf-8'))
        Group = jsondata.get('Group')
        type = jsondata.get('Type')
        subtype = jsondata.get('SubType')
        data = jsondata.get('DETAIL')
        entity_gid = request.session['Entity_gid']
        jsondata['CLASSIFICATION'] = {'Entity_Gid': request.session['Entity_gid']}
        datas = json.dumps(data)
        params = {'Type': type, 'SubType': subtype,'Group':Group}
        token = jwt.token(request)
        headers = {"content-type": "application/json", "Authorization": "" + token + ""}
        result = requests.post("" + ip + "/Tran_History_Get", params=params, headers=headers, data=datas, verify=False)
        results = result.content.decode("utf-8")
        return JsonResponse(json.loads(results), safe=False)



def mail_CheckIndex(request):
    return render(request, "mail_Check.html")




import boto3
from botocore.exceptions import ClientError
def new_mail_check(request):
    if request.method == 'GET':


        SENDER = "Karur Vysya Bank <wisefin-noreply@kvbmail.com>"
        AWS_REGION = "ap-south-1"
        SUBJECT = 'TESTING MAIL'
        BODY_TEXT = ("")
        BODY_HTML = """<html>
        <head></head>
        <body>
        <p>'Only for Testing Purpose Kindly Ignore'</p>
        </body>
        </html>
                    """
        CHARSET = "UTF-8"
        client = boto3.client('ses', region_name=AWS_REGION)
        try:
            # Provide the contents of the email.
            response = client.send_email(
                Destination={
                    'ToAddresses': [
                        'rvignesh@vsolv.co.in','saravanakumarpr@kvbmail.com','sathya.m@kvbmail.com',
                    ],
                },
                Message={
                    'Body': {
                        'Html': {
                            'Charset': CHARSET,
                            'Data': BODY_HTML,
                        },
                        'Text': {
                            'Charset': CHARSET,
                            'Data': BODY_TEXT,
                        },
                    },
                    'Subject': {
                        'Charset': CHARSET,
                        'Data': SUBJECT,
                    },
                },
                Source=SENDER,
            )
        # Display an error if something goes wrong.
        except ClientError as e:
            log_data = [{"MAIL_CHECK_LOG_IN_EXCEPTION": e.response['Error']['Message']}]
            common.logger.error(log_data)
            return (e.response['Error']['Message'])
        else:
            log_data = [{"MAIL_CHECK_SUCCESS": 'SUCCESS'}]
            common.logger.error(log_data)
            return JsonResponse({"MESSAGE": "SUCCESS"})
