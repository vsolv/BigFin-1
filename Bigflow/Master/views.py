from django.shortcuts import render
from Bigflow.Master.Model import mMasters
from Bigflow.Transaction.Model import mFET
from datetime import datetime
from django.http import JsonResponse
import Bigflow.Core.jwt_file as jwt
from django.core.files.base import ContentFile
import pandas as pd
import json
import datetime
import time
import boto3
from django.http import HttpResponse
from Bigflow.menuClass import utility as utl
from django.core.files.storage import default_storage
from django.conf import settings
from Bigflow.settings import BASE_DIR

import Bigflow.Core.models as common
from Bigflow.Core.models import Excelfilename
# mail
import requests
from Bigflow.settings import BASE_DIR
from Bigflow.Core.models import decrpt as decry_data
# from Bigflow.API import views as commonview
from django.http import JsonResponse, HttpResponse, StreamingHttpResponse
from Bigflow.settings import S3_BUCKET_NAME
import os.path
from Bigflow.Core.models import MasterRequestObject


ip = common.localip()
token = common.token()


def employeeIndex(request):
    utl.check_authorization(request)
    utl.check_pointaccess(request)
    return render(request, "employee/bigflow_mst_employee.html")
def sales_transaction(request):
    utl.check_authorization(request)
    return render(request, "Customer/Sales_Transaction.html")



def Ccbs_Maker_fun(request):
    utl.check_authorization(request)
    utl.check_pointaccess(request)
    return render(request, "CCBS/Ccbs_Maker.html")


def Ccbs_Approver_fun(request):
    utl.check_authorization(request)
    utl.check_pointaccess(request)
    return render(request, "CCBS/Ccbs_Approver.html")


def Ccbs_Maker_Popup_fun(request):
    # utl.check_authorization(request)
    utl.check_pointaccess(request)
    return render(request, "CCBS/Ccbs_Maker_Popup.html")


def Cat_Subcat_fun(request):
    utl.check_authorization(request)
    utl.check_pointaccess(request)
    return render(request, "CCBS/Cat_Subcat_Summary.html")

def Cat_Subcat_Approver(request):
    utl.check_authorization(request)
    utl.check_pointaccess(request)
    return render(request, "CCBS/Cat_Subcat_Approver.html")

def Cat_Subcat_Popup(request):
    utl.check_authorization(request)
    utl.check_pointaccess(request)
    return render(request, "Customer/customer_file_uload.html")



def Cat_Subcat_Popup(request):
    utl.check_authorization(request)
    utl.check_pointaccess(request)
    return render(request, "CCBS/Cat_Subcat_Add_Summary.html")


def Cc_Bb_Summary(request):
    utl.check_authorization(request)
    utl.check_pointaccess(request)
    return render(request, "CCBS/Cc_Bb_Summary.html")


def Cc_Bb_Popup(request):
    utl.check_authorization(request)
    utl.check_pointaccess(request)
    return render(request, "CCBS/Cc_Bs_Add_Summary.html")

def add_business_segment(request):
    utl.check_authorization(request)
    utl.check_pointaccess(request)
    return render(request, "CCBS/add_business_segment.html")


def employeesummaryIndex(request):
    utl.check_authorization(request)
    utl.check_pointaccess(request)
    return render(request, "employee/bigflow_mst_employee_summary.html")


def employeeadrsIndex(request):
    utl.check_pointaccess(request)
    return render(request, "employee/bigflow_mst_employee_adrs.html")


def employeecntctIndex(request):
    utl.check_pointaccess(request)
    return render(request, "employee/bigflow_mst_employee_cntct.html")


def employeeviewIndex(request):
    utl.check_authorization(request)
    utl.check_pointaccess(request)
    return render(request, "employee/bigflow_mst_employee_view.html")


def empattendanceIndex(request):
    utl.check_authorization(request)
    utl.check_pointaccess(request)
    return render(request, "employee/emp_attendance.html")

def emp_upload(request):
    # utl.check_authorization(request)
    # utl.check_pointaccess(request)
    return render(request, "employee/Employee_Upload.html")

def customerupload(request):
    return render(request,"Customer/customer_upload.html")

def custset(request):
    #utl.check_authorization(request)
    if request.method == 'POST':
     try:
        obj_master = mMasters.Masters()
        excel_file = request.FILES['file'] # geting the excel file from angular
        obj_master.Action=request.POST['Action']
        obj_master.Type=request.POST['Type']
        current_month=datetime.datetime.now().strftime('%m')
        current_day = datetime.datetime.now().strftime('%d')
        current_year_full = datetime.datetime.now().strftime('%Y')
        save_path = str(settings.MEDIA_ROOT) + '/Customer/' + str(current_year_full) + '/' + str(
            current_month) + '/' + str(current_day) + '/' + str(request.POST['name'])
        path = default_storage.save(str(save_path), request.FILES['file'])
        df = pd.read_excel(excel_file)
        df['customer_DOB'] = df['customer_DOB'].dt.strftime('%Y-%m-%d')
        df['customer_WD'] = df['customer_WD'].dt.strftime('%Y-%m-%d')
        data= df.to_dict('records')
        obj_master.filerdata={"HEADER":data,"file_name":str(request.POST['name']),"file_path":path}
        obj_master.filerdata=json.dumps(obj_master.filerdata)
        createby = decry_data(request.session['Emp_gid'])
        entity_gid = decry_data(request.session['Entity_gid'])
        #obj_master.classification=json.dumps({"Entity_Gid": [1], "create_by": [1]})
        obj_master.classification = json.dumps({'Entity_Gid': entity_gid, "create_by": createby})
        obj_cancel_data = obj_master.set_customerset()
        excel_status = "".join(obj_cancel_data)
        excel_status = excel_status.split(',')
        return JsonResponse( excel_status[1], safe=False)
     except Exception as e:
               return JsonResponse({"MESSAGE": "ERROR_OCCURED", "DATA": str(e)})

def custupload(request):
    if request.method == 'POST':
     try:
        obj_master = mMasters.Masters()
        jsondata = json.loads(request.body.decode('utf-8'))
        obj_master.action =jsondata.get('Action')
        obj_master.type =jsondata.get('Type')
        createby = decry_data(request.session['Emp_gid'])
        entity_gid = decry_data(request.session['Entity_gid'])
        obj_master.Classification = json.dumps({'Entity_Gid': entity_gid, "create_by": createby})
        #obj_master.Classification=json.dumps(jsondata.get('data').get('Classification'))
        common.main_fun1(request.read(), request.path)
        obj_cancel_data = obj_master.get_customerupload()
        jdata = obj_cancel_data.to_json(orient='records')
        return JsonResponse(json.loads(jdata), safe=False)
     except Exception as e:
              return JsonResponse({"MESSAGE": "ERROR_OCCURED", "DATA": str(e)})

def customersubmit(request):
    if request.method == 'POST':
     try:
        obj_master = mMasters.Masters()
        jsondata = json.loads(request.body.decode('utf-8'))
        obj_master.action =jsondata.get('Action')
        obj_master.type =jsondata.get('Type')
        obj_master.filerdata = json.dumps(jsondata.get('data').get('FILTER'))
        createby = decry_data(request.session['Emp_gid'])
        entity_gid = decry_data(request.session['Entity_gid'])
        obj_master.Classification = json.dumps({'Entity_Gid': entity_gid, "create_by": createby})
        #common.main_fun1(request.read(), request.path)
        obj_cancel_data = obj_master.get_submit()
        return JsonResponse(json.dumps(obj_cancel_data), safe=False)
     except Exception as e:
           return JsonResponse({"MESSAGE": "ERROR_OCCURED", "DATA": str(e)})

def customerdelete(request):
    if request.method == 'POST':
     try:
        obj_master = mMasters.Masters()
        jsondata = json.loads(request.body.decode('utf-8'))
        obj_master.Action =jsondata.get('Action')
        obj_master.Type =jsondata.get('Type')
        obj_master.filerdata = json.dumps(jsondata.get('data').get('FILTER'))
        createby = decry_data(request.session['Emp_gid'])
        entity_gid = decry_data(request.session['Entity_gid'])
        obj_master.classification = json.dumps({'Entity_Gid': entity_gid, "create_by": createby})
        common.main_fun1(request.read(), request.path)
        obj_cancel_data = obj_master.set_customerset()
        jdata = obj_cancel_data.to_json(orient='records')
        return JsonResponse(json.loads(jdata), safe=False)
     except Exception as e:
        return JsonResponse({"MESSAGE": "ERROR_OCCURED", "DATA": str(e)})




def select_query_screen(request):
    utl.check_authorization(request)
    if request.method == 'POST':
         try:
            objdata = mMasters.Masters()
            jsondata = json.loads(request.body.decode('utf-8'))
            objdata.type = jsondata.get('Type')
            objdata.sub_type = jsondata.get('Subtype')
            objdata.filterdata = json.dumps(jsondata.get('Params').get('FILTER'))
            objdata.classification = json.dumps(jsondata.get('Params').get('classification'))
            if objdata.sub_type == 'Table':
                common.main_fun1(request.read(), request.path)
                obj_cancel_data = objdata.SelectSummary()
                obj_cancel_data.columns=['tabels_data']
                jdata = obj_cancel_data.to_json(orient='records')
                return JsonResponse(jdata, safe=False)
            else:
                common.main_fun1(request.read(), request.path)
                obj_cancel_data = objdata.SelectSummary()
                jdata = obj_cancel_data.to_json(orient='records')
                return JsonResponse({"MESSAGE": "FOUND", "DATA": jdata}, safe=False)
         except Exception as e:
            return JsonResponse({"MESSAGE": "ERROR_OCCURED", "DATA": str(e)})

    else:
        return render(request, "Common/select_query_screen.html")

def emprouteIndex(request):
    utl.check_authorization(request)
    utl.check_pointaccess(request)
    return render(request, "Customer/emp_Route.html")


def emproutedaymapping(request):
    utl.check_authorization(request)
    utl.check_pointaccess(request)
    return render(request, "employee/emp_routedaymapping.html")


def courier_index(request):
    utl.check_authorization(request)
    return render(request, "employee/bigflow_mst_courier.html")

def casequery_temp(request):
    utl.check_authorization(request)
    return render(request, "Customer/customer_casequery.html")

def agency(request):
    return render(request,"Customer/customer_agency.html")

def agencyupload(request):
    if request.method == 'POST':
     try:
        obj_master = mMasters.Masters()
        jsondata = json.loads(request.body.decode('utf-8'))
        obj_master.action ='Agent'
        obj_master.type ='Summary'
        obj_master.Classification=json.dumps(jsondata.get('data').get('Classification'))
        obj_master.ls_Createby=1

        obj_cancel_data = obj_master.get_agencyupload()
        jdata = obj_cancel_data.to_json(orient='records')
        return JsonResponse(json.loads(jdata), safe=False)
     except Exception as e:
         return JsonResponse({"MESSAGE": "ERROR_OCCURED", "DATA": str(e)})

def agencyset(request):

    utl.check_authorization(request)
    if request.method == 'POST':
     try:
        obj_master = mMasters.Masters()
        excel_file = request.FILES['file'] # geting the excel file from angular
        obj_master.Action=request.POST['Action']
        obj_master.Type=request.POST['Type']
        #obj_master.create_by=request.session['Emp_gid']
        df = pd.read_excel(excel_file)
        data= df.to_dict('records')
        obj_master.filerdata=json.dumps({"HEADER":data})
        obj_master.classification=json.dumps({"Entity_Gid": [1], "create_by": [1]})
        obj_cancel_data = obj_master.set_agencyset()
        excel_status = "".join(obj_cancel_data)
        excel_status = excel_status.split(',')
        return JsonResponse( excel_status[1], safe=False)
     except Exception as e:
         return JsonResponse({"MESSAGE": "ERROR_OCCURED", "DATA": str(e)})


def SubAgency(request):
    utl.check_authorization(request)
    if request.method == 'POST':
     try:
       # parameters = (self.action, self.Type, self.FILTER, self.Classification, 1, '')
        obj_master = mMasters.Masters()
        jsondata = json.loads(request.body.decode('utf-8'))
        obj_master.Action = jsondata.get('Action')
        obj_master.Type =jsondata.get('Type')
        obj_master.filerdata=json.dumps(jsondata.get('data').get('FILTER'))
        obj_master.Classification=json.dumps(jsondata.get('data').get('Classification'))
        obj_master.ls_Createby=1
        obj_cancel_data = obj_master.sub_agencyset()
        return JsonResponse(json.dumps(obj_cancel_data), safe=False)
     except Exception as e:
         return JsonResponse({"MESSAGE": "ERROR_OCCURED", "DATA": str(e)})

def deleteagency(request):
        utl.check_authorization(request)
        if request.method == 'POST':
         try:
            obj_master = mMasters.Masters()
            jsondata = json.loads(request.body.decode('utf-8'))
            obj_master.action = 'Delete'
            obj_master.type = ''
            obj_master.FILTER = json.dumps(jsondata.get('data').get('FILTER'))
            obj_master.Classification = json.dumps(jsondata.get('data').get('Classification'))
            obj_master.ls_Createby = 1
            obj_cancel_data = obj_master.del_agencyset()
            return JsonResponse(json.dumps(obj_cancel_data), safe=False)
         except Exception as e:
             return JsonResponse({"MESSAGE": "ERROR_OCCURED", "DATA": str(e)})



def set_empupload(request):
   if request.method == 'POST':
     try:
            obj_master = mMasters.Masters()
            excel_file = request.FILES['file'] # getting the excel file from angular
            obj_master.action=request.POST['Action']
            obj_master.type=request.POST['Type']
            df = pd.read_excel(excel_file)
            data= df.to_dict('records')
            current_month =datetime.datetime.now().strftime('%m')
            current_day = datetime.datetime.now().strftime('%d')
            current_year_full = datetime.datetime.now().strftime('%Y')
            save_path = str(settings.MEDIA_ROOT) + '/EMPLOYEE/' + str(current_year_full)+'/'+str(current_month)+ '/'+str(current_day)+'/'+str(request.POST['name'])
            path = default_storage.save(str(save_path), request.FILES['file'])
            obj_master.filterdata={"HEADER":data,"file_name":str(request.POST['name']),"file_path":path}
            obj_master.filter = json.dumps(obj_master.filterdata)
            createby=decry_data(request.session['Emp_gid'])
            entity_gid=decry_data(request.session['Entity_gid'])
            obj_master.json_classification=json.dumps({"Entity_Gid": entity_gid, "create_by": createby})
            # common.main_fun1(request.read(), request.path)
            obj_emp_data = obj_master.set_emp_upload()
            excel_status = "".join(obj_emp_data)
            excel_status = excel_status.split(',')
            return JsonResponse( excel_status[1], safe=False)
     except Exception as e:
            return JsonResponse({"MESSAGE": "ERROR_OCCURED", "DATA": str(e)})



def get_empupload(request):
    if request.method == 'POST':
     try:
        objdata = mMasters.Masters()
        jsondata = json.loads(request.body.decode('utf-8'))
        objdata.action = jsondata.get('Action')
        objdata.type = jsondata.get('Type')
        createby = decry_data(request.session['Emp_gid'])
        entity_gid = decry_data(request.session['Entity_gid'])
        objdata.json_classification = json.dumps({"Entity_Gid": entity_gid, "create_by": createby})
        common.main_fun1(request.read(), request.path)
        obj_getemp_data = objdata.get_emp_upload()
        jdata = obj_getemp_data.to_json(orient='records')
        return JsonResponse(json.loads(jdata), safe=False)
     except Exception as e:
         return JsonResponse({"MESSAGE": "ERROR_OCCURED", "DATA": str(e)})


def del_empupload(request):
  if request.method == 'POST':
     try:
        objdata = mMasters.Masters()
        jsondata = json.loads(request.body.decode('utf-8'))
        objdata.action = jsondata.get('Action')
        objdata.type = jsondata.get('Type')
        objdata.filter = json.dumps(jsondata.get('data').get('Filter'))
        createby = decry_data(request.session['Emp_gid'])
        entity_gid = decry_data(request.session['Entity_gid'])
        objdata.json_classification = json.dumps({"Entity_Gid": entity_gid, "create_by": createby})
        common.main_fun1(request.read(), request.path)
        obj_delete_data = objdata.set_emp_upload()
        return JsonResponse(obj_delete_data, safe=False)
     except Exception as e:
         return JsonResponse({"MESSAGE": "ERROR_OCCURED", "DATA": str(e)})


def saveemp(request):

    if request.method == 'POST':
     try:
        objdata = mMasters.Masters()
        jsondata = json.loads(request.body.decode('utf-8'))
        objdata.action = jsondata.get('Action')
        objdata.type = jsondata.get('Type')
        objdata.filter = json.dumps(jsondata.get('data').get('Filter'))
        createby = decry_data(request.session['Emp_gid'])
        entity_gid = decry_data(request.session['Entity_gid'])
        objdata.json_classification = json.dumps({"Entity_Gid": entity_gid, "create_by": createby})
        # common.main_fun1(request.read(), request.path)
        obj_save_data = objdata.set_emp_upload()
        return JsonResponse(obj_save_data, safe=False)
     except Exception as e:
         return JsonResponse({"MESSAGE": "ERROR_OCCURED", "DATA": str(e)})


def customerall(request):
     if request.method == 'POST':
            #path = request.path
            obj_master = mMasters.Masters()
            jsondata = json.loads(request.body.decode('utf-8'))
            obj_master.Type = 'CUSTOMER'
            obj_master.Subtype = 'CUSTOMER_ALL'
            obj_master.jsonData = json.dumps(jsondata.get('FILTER'))
            #obj_master.jsonData = json.dumps(jsondata.get('params').get('FILTER'))
            # obj_master.customergroup_gid = request.session['customergroup_gid']
            obj_master.entity_gid = json.dumps({"Entity_Gid":decry_data(request.session['Entity_gid'])})
            common.main_fun1(request.read(), request.path)
            # obj_master.entity_gid = json.dumps({"Entity_Gid":(request.session['Entity_gid'])})
            obj_cancel_data = obj_master.get_customerall()
            jdata = obj_cancel_data.to_json(orient='records')
            return JsonResponse(json.loads(jdata), safe=False)


def soorderdetails(request):
    if request.method == 'POST':
        obj_master = mMasters.Masters()
        jsondata = json.loads(request.body.decode('utf-8'))
        obj_master.action = 'GET'
        obj_master.type = 'SALES_TRANS_GET'
        obj_master.jsonData = json.dumps(jsondata.get('params').get('FILTER'))
        # obj_master.jsonData = json.dumps(jsondata.get('params').get('FILTER'))
        obj_master.entity_gid = json.dumps({"Entity_Gid": decry_data(request.session['Entity_gid'])})
        common.main_fun1(request.read(), request.path)
        obj_cancel_data = obj_master.get_orderdetails()
        jdata = obj_cancel_data.to_json(orient='records')
        return JsonResponse(json.loads(jdata), safe=False)

def custset(request):
    #utl.check_authorization(request)
    if request.method == 'POST':
        obj_master = mMasters.Masters()
        excel_file = request.FILES['file'] # geting the excel file from angular
        obj_master.Action=request.POST['Action']
        obj_master.Type=request.POST['Type']
        df = pd.read_excel(excel_file)
        datas= df.to_dict('records')
        obj_master.filerdata=json.dumps({"HEADER":datas})
        obj_master.classification=json.dumps({"Entity_Gid": [1], "create_by": [1]})
        obj_cancel_data = obj_master.set_customerset()
        excel_status = "".join(obj_cancel_data)
        excel_status = excel_status.split(',')
        return JsonResponse( excel_status[1], safe=False)

def customerupload(request):
    return render(request,"Customer/customer_upload.html")

def saleorder(request):
    if request.method == 'POST':
        obj_master = mMasters.Masters()
        jsondata = json.loads(request.body.decode('utf-8'))
        obj_master.action = 'GET'
        obj_master.type = 'SALES_TRANS_GET'
        obj_master.filter = json.dumps(jsondata.get('params').get('FILTER'))
        obj_master.entity_gid = json.dumps({"Entity_Gid": decry_data(request.session['Entity_gid'])})
        common.main_fun1(request.read(), request.path)
        obj_cancel_data = obj_master.get_saleorderdetails()
        jdata = obj_cancel_data.to_json(orient='records')
        return JsonResponse(json.loads(jdata), safe=False)


def customername(request):
    if request.method == 'POST':
        obj_master = mMasters.Masters()
        jsondata = json.loads(request.body.decode('utf-8'))
        obj_master.action = 'customer'
        obj_master.type = 'cust_group'
        obj_master.jsonData = json.dumps(jsondata.get('FILTER'))
        # obj_master.jsonData = json.dumps(jsondata.get('params').get('FILTER'))
        # obj_master.customergroup_gid = request.session['customergroup_gid']
        obj_master.entity_gid = json.dumps({"Entity_Gid": decry_data(request.session['Entity_gid'])})
        common.main_fun1(request.read(), request.path)
        # obj_master.entity_gid = json.dumps({"Entity_Gid":(request.session['Entity_gid'])})
        obj_cancel_data = obj_master.get_customername()
        jdata = obj_cancel_data.to_json(orient='records')
        return JsonResponse(json.loads(jdata), safe=False)


def customergroupname(request):
    if request.method == 'POST':
        obj_master = mMasters.Masters()
        jsondata = json.loads(request.body.decode('utf-8'))
        obj_master.action = 'dropdown'
        obj_master.type = 'cust_groupnames'
        obj_master.jsonData = json.dumps(jsondata.get('FILTER'))
        # obj_master.jsonData = json.dumps(jsondata.get('params').get('FILTER'))
        # obj_master.customergroup_gid = request.session['customergroup_gid']
        obj_master.entity_gid = json.dumps({"Entity_Gid": decry_data(request.session['Entity_gid'])})
        common.main_fun1(request.read(), request.path)
        # obj_master.entity_gid = json.dumps({"Entity_Gid":(request.session['Entity_gid'])})
        obj_cancel_data = obj_master.get_customergroup()
        jdata = obj_cancel_data.to_json(orient='records')
        return JsonResponse(json.loads(jdata), safe=False)


def casequerys(request):
    if request.method == 'POST':

        #path = request.path
        obj_master = mMasters.Masters()
        jsondata = json.loads(request.body.decode('utf-8'))
        obj_master.action ='CaseQueryScreen'
        obj_master.Type ='Details'
        obj_master.jsonData = json.dumps(jsondata.get('params').get('FILTER'))
        #obj_master.jsonData = json.dumps(jsondata.get('params').get('FILTER'))
        # obj_master.customergroup_gid = request.session['customergroup_gid']
        obj_master.entity_gid = json.dumps({"Entity_Gid":decry_data(request.session['Entity_gid'])})
        #obj_master.entity_gid = json.dumps({"Entity_Gid":(request.session['Entity_gid'])})
        common.main_fun1(request.read(), request.path)
        obj_cancel_data = obj_master.get_casequery()
        jdata = obj_cancel_data.to_json(orient='records')
        return JsonResponse(json.loads(jdata), safe=False)
def casequery(request):
        if request.method == 'POST':
            #path =request.path
            obj_master = mMasters.Masters()
            jsondata = json.loads(request.body.decode('utf-8'))
            obj_master.action = 'Cheque'
            obj_master.Type = 'BounceHistory'
            obj_master.jsonData = json.dumps(jsondata.get('params').get('FILTER'))
            # obj_master.jsonData = json.dumps(jsondata.get('params').get('FILTER'))
            # obj_master.customergroup_gid = request.session['customergroup_gid']
            obj_master.entity_gid = json.dumps({"Entity_Gid":decry_data(request.session['Entity_gid'])})
            common.main_fun1(request.read(), request.path)
            #obj_master.entity_gid = json.dumps({"Entity_Gid": (request.session['Entity_gid'])})
            obj_cancel_data = obj_master.get_casequery()
            jdata = obj_cancel_data.to_json(orient='records')
            return JsonResponse(json.loads(jdata), safe=False)
def followup(request):
        if request.method == 'POST':
            #path =request.path
            obj_master = mMasters.Masters()
            jsondata = json.loads(request.body.decode('utf-8'))
            obj_master.action = 'Display'
            obj_master.Type = 'FollowUpDetails'
            obj_master.jsonData = json.dumps(jsondata.get('params').get('FILTER'))
            # obj_master.jsonData = json.dumps(jsondata.get('params').get('FILTER'))
            # obj_master.customergroup_gid = request.session['customergroup_gid']
            obj_master.entity_gid = json.dumps({"Entity_Gid":decry_data(request.session['Entity_gid'])})
            #obj_master.entity_gid = json.dumps({"Entity_Gid": (request.session['Entity_gid'])})
            common.main_fun1(request.read(), request.path)
            obj_cancel_data = obj_master.get_casequery()
            jdata = obj_cancel_data.to_json(orient='records')
            return JsonResponse(json.loads(jdata), safe=False)
def outstanding(request):
    if request.method == 'POST':
        #path =request.path
        obj_master = mMasters.Masters()
        jsondata = json.loads(request.body.decode('utf-8'))
        obj_master.action = 'Report'
        obj_master.Type = 'Outstanding'
        obj_master.jsonData = json.dumps(jsondata.get('params').get('FILTER'))
        # obj_master.jsonData = json.dumps(jsondata.get('params').get('FILTER'))
        # obj_master.customergroup_gid = request.session['customergroup_gid']
        obj_master.entity_gid = json.dumps({"Entity_Gid":decry_data(request.session['Entity_gid'])})
        #obj_master.entity_gid = json.dumps({"Entity_Gid": (request.session['Entity_gid'])})
        common.main_fun1(request.read(), request.path)
        obj_cancel_data = obj_master.get_casequery()
        jdata = obj_cancel_data.to_json(orient='records')
        return JsonResponse(json.loads(jdata), safe=False)




def executivemapping_index(request):
    utl.check_authorization(request)
    utl.check_pointaccess(request)
    return render(request, "employee/bigflow_mst_executivemapping.html")


def city(request):
    utl.check_authorization(request)
    utl.check_pointaccess(request)
    return render(request, "City/bigflow_mst_city.html")


# Supplier create
def supplierIndex(request):
    utl.check_authorization(request)
    return render(request, "Supplier/Supplier_Create.html")


def supplierSumryIndex(request):
    utl.check_authorization(request)
    return render(request, "Supplier/Supplier_Smry.html")


def Product_Add_Popup(request):
    # utl.check_authorization(request)
    utl.check_pointaccess(request)
    return render(request, "Product/Product_Add_popup.html")


def Product_Add_Popupcarton(request):
    utl.check_authorization(request)
    utl.check_pointaccess(request)
    return render(request, "Product/Product_Add_Popupcarton.html")


def Product_Type_Popup(request):
    # utl.check_authorization(request)
    utl.check_pointaccess(request)
    return render(request, "Product/Product_Type_popup.html")

#Hsn Code
def mst_hsn(request):
    utl.check_authorization(request)
    return render(request,"Product/mst_hsn.html")

#Tax Code
def mst_tax(request):
    utl.check_authorization(request)
    return render(request,"Tax/mst_tax.html")

#master state distric city
def mst_state_dist_city(request):
    utl.check_authorization(request)
    return render(request,"Common/mst_state_dist_city.html")

def hsn_data(request):
    utl.check_authorization(request)
    utl.check_pointaccess(request)
    if request.method == 'POST':
        try:
            token = jwt.token(request)
            jsondata = json.loads(request.body.decode('utf-8'))
            if (jsondata.get('params').get('Group')) == 'GET_HSN_DATA':
                entity = request.session['Entity_gid']
                drop_b = {
                    "Table_name":"gal_mst_thsn",
                    "Column_1":"hsn_code,hsn_description,hsn_cgstrate,hsn_sgstrate,hsn_igstrate",
                    "Column_2":"",
                    "Where_Common":"hsn",
                    "Where_Primary":"",
                    "Primary_Value":"",
                    "Order_by":"gid"
                }
                response = alltable(drop_b, entity,token)
                return HttpResponse(response)
            elif (jsondata.get('params').get('Group')) == 'GET_TAX_DATA':
                entity = request.session['Entity_gid']
                drop_b = {
                    "Table_name": "gal_mst_ttaxrate",
                    "Column_1": "taxrate_gid,taxrate_code,taxrate_name,taxrate_rate",
                    "Column_2": "",
                    "Where_Common": "taxrate",
                    "Where_Primary": "",
                    "Primary_Value": "",
                    "Order_by": "gid"
                }
                response = alltable(drop_b, entity,token)
                return HttpResponse(response)
            elif (jsondata.get('params').get('Group')) == 'GET_CATEGORY_OD_OR_ID':
                entity = request.session['Entity_gid']
                drop_b = {
                    "Table_name": "gal_mst_tmetadata",
                    "Column_1": "metadata_value,metadata_gid",
                    "Column_2": "",
                    "Where_Common": "metadata",
                    "Where_Primary": "columnname",
                    "Primary_Value": "category_isodit",
                    "Order_by": "columnname"
                }
                response = alltable(drop_b, entity,token)
                return HttpResponse(response)

            elif (jsondata.get('params').get('Group')) == 'SET_HSN_DATA':
                act = jsondata.get('params').get('Action')
                grp = jsondata.get('params').get('Group')
                typ = jsondata.get('params').get('Type')
                sub = jsondata.get('params').get('Sub_Type')
                emp = request.session['Emp_gid']
                params = {"Action": act, "Group": grp, "Type": typ, "Sub_Type": sub,
                          "Employee_Gid": emp}
                token = jwt.token(request)
                headers = {"content-type": "application/json", "Authorization": "" + token + ""}
                classify = {
                    "CLASSIFICATION": {
                        "Entity_Gid": request.session['Entity_gid']
                    }}
                jsondata['params']['json']['Params'].update(classify)
                datas = json.dumps(jsondata.get('params').get('json'))
                resp = requests.post("" + ip + "/HSN_MASTER", params=params, data=datas, headers=headers,
                                     verify=False)
                response = resp.content.decode("utf-8")
                return HttpResponse(response)
            elif (jsondata.get('params').get('Group')) == 'GET_HSN_DETAILS':
                act = jsondata.get('params').get('Action')
                grp = jsondata.get('params').get('Group')
                typ = jsondata.get('params').get('Type')
                sub = jsondata.get('params').get('Sub_Type')
                entity_gid = int(decry_data(request.session['Entity_gid']))
                headers = {"content-type": "application/json", "Authorization": "" + token + ""}
                datas = json.dumps({"Params":{"DETAILS": {}, "CLASSIFICATION": {"Entity_Gid": entity_gid}}})
                params = {'Action': act, 'Type': typ,'Group':grp}
                result = requests.post("" + ip + "/HSN_MASTER", params=params, data=datas, headers=headers,
                                     verify=False)
                results = result.content.decode("utf-8")
                return JsonResponse(json.loads(results), safe=False)
        except Exception as e:
            return JsonResponse({"MESSAGE": "ERROR_OCCURED", "DATA": str(e)})

def alltable(table_data,entity,token):
    drop_tables = {"data": table_data}
    action = ''
    entity_gid = entity
    params = {'Action': action, 'Entity_Gid': entity_gid}
    headers = {"content-type": "application/json", "Authorization": "" + token + ""}
    datas = json.dumps(drop_tables.get('data'))
    resp = requests.post("" + ip + "/All_Tables_Values_Get", params=params, data=datas, headers=headers,
                         verify=False)
    response_data = resp.content.decode("utf-8")
    return response_data
#set_mst_State-Distric-City-Pincode
def set_mst_SDCP(request):
    utl.check_authorization(request)
    if request.method == 'POST':
        jsondata = json.loads(request.body.decode('utf-8'))
        Action = jsondata.get('Action')
        Type = jsondata.get('Type')
        classify = {
            "CLASSIFICATION": {
                "Entity_Gid": request.session['Entity_gid']
            }}
        jsondata['data']['params'].update(classify)
        datas = json.dumps(jsondata.get('data').get('params'))
        Emp_gid = request.session['Emp_gid']
        Entity_gid = request.session['Entity_gid']
        param = {'Action': Action, 'Entity_gid': Entity_gid,'Type': Type, 'Emp_gid': Emp_gid}
        token = jwt.token(request)
        headers = {"content-type": "application/json", "Authorization": "" + token + ""}
        result = requests.post("" + ip + "/Master_State_Details", params=param, headers=headers, data=datas,
                               verify=False)
        result = result.content.decode("utf-8")
        if (jsondata.get('Type') == 'State_Insert'):
            data = jsondata.get('data').get('params').get('filter')
            data = {'name': data['State_name'], 'country_id': data['State_country_gid'],'Entity_Gid': Entity_gid,'create_by':Emp_gid}
            mrobject = MasterRequestObject('STATE', data, 'POST')
        if (jsondata.get('Type') == 'District_Insert'):
            data = jsondata.get('data').get('params').get('filter')
            data = {'name': data['district_name'], 'state_id': data['district_state_gid'],'Entity_Gid': Entity_gid,'create_by':Emp_gid}
            mrobject = MasterRequestObject('DISTRICT', data, 'POST')
        elif (jsondata.get('Type') == None):
            data = jsondata.get('data').get('params')
            city_data = {'name': data['city_name'], 'state_id': data['state_gid'],'Entity_Gid': Entity_gid,'create_by':Emp_gid}
            mrobject = MasterRequestObject('CITY', city_data, 'POST')
            city_data['district_id'] = data['district_gid']
            city_data['no'] = data['pincode_no']
            city_data['Entity_Gid']=Entity_gid
            city_data['create_by']=Emp_gid
            data = mrobject.param_data
            city_data['city_id'] = json.loads(data.text).get('id')
            pincode_mrobject = MasterRequestObject('PINCODE', city_data, 'POST')

        return JsonResponse(json.loads(result), safe=False)

def tax_data(request):
    utl.check_authorization(request)
    if request.method == 'POST':
        token = jwt.token(request)
        jsondata = json.loads(request.body.decode('utf-8'))
        if (jsondata.get('params').get('Groups')) == 'GET_TAX':
            entity = request.session['Entity_gid']
            drop_b = {
                "Table_name":"gal_mst_ttax",
                "Column_1":"tax_gid,tax_code,tax_name,tax_recivable,tax_payable,tax_glno",
                "Column_2":"",
                "Where_Common":"tax",
                "Where_Primary":"",
                "Primary_Value":"",
                "Order_by":"gid"
            }
            response = alltable(drop_b, entity,token)
            res = json.dumps(response)
            res = str(res)
            return HttpResponse(res)
        elif (jsondata.get('params').get('Groups')) == 'GET_SUB_TAX':
            entity = request.session['Entity_gid']
            tax_gid = jsondata.get('params').get('Tax_Gid')
            drop_b = {
                "Table_name": "gal_mst_tsubtax",
                "Column_1": "subtax_code,subtax_gid,subtax_name,subtax_glno,subtax_tax_gid",
                "Column_2": "",
                "Where_Common": "subtax",
                "Where_Primary": "tax_gid",
                "Primary_Value": tax_gid,
                "Order_by": "gid"
            }
            response = alltable(drop_b, entity,token)
            res = json.dumps(response)
            res = str(res)
            return HttpResponse(res)
        elif (jsondata.get('params').get('Groups')) == 'GET_TAX_RATE':
            entity = request.session['Entity_gid']
            subtax_gid = jsondata.get('params').get('SubTax_Gid')
            drop_b = {
                "Table_name": "gal_mst_ttaxrate",
                "Column_1": "taxrate_subtax_gid,taxrate_code,taxrate_name,taxrate_rate,taxrate_gid",
                "Column_2": "",
                "Where_Common": "taxrate",
                "Where_Primary": "subtax_gid",
                "Primary_Value":subtax_gid ,
                "Order_by": "gid"
            }
            response = alltable(drop_b, entity,token)
            res = json.dumps(response)
            res = str(res)
            return HttpResponse(res)
        elif (jsondata.get('params').get('Groups')) == 'TAX_DATA':
            act = jsondata.get('params').get('Action')
            grp = jsondata.get('params').get('Group')
            typ = jsondata.get('params').get('Type')
            sub = jsondata.get('params').get('Sub_Type')
            emp = request.session['Emp_gid']
            params = {"Action": act, "Group": grp, "Type": typ, "Sub_Type": sub,
                      "Employee_Gid": emp}
            headers = {"content-type": "application/json", "Authorization": "" + token + ""}
            classify = {
                "CLASSIFICATION": {
                    "Entity_Gid": request.session['Entity_gid']
                }}
            jsondata['params']['json']['Params'].update(classify)
            datas = json.dumps(jsondata.get('params').get('json'))
            resp = requests.post("" + ip + "/TAX_MASTER", params=params, data=datas, headers=headers,
                                 verify=False)
            response = resp.content.decode("utf-8")
            return HttpResponse(response)

def Supplier_Master(request):
    utl.check_authorization(request)
    utl.check_pointaccess(request)
    jsondata = json.loads(request.body.decode('utf-8'))
    if request.method == 'POST':
        if (jsondata.get('Group')) == 'Supplier_Get':
            group = jsondata.get('Group')
            type = jsondata.get('Type')
            subtype = jsondata.get('SubType')
            params = {'Group': "" + group + "", 'Type': "" + type + "",
                      'SubType': "" + subtype + ""}
            datas = json.dumps(jsondata.get('data'))
            token = jwt.token(request)
            headers = {"content-type": "application/json", "Authorization": "" + token + ""}
            resp = requests.post("" + ip + "/Supplier_Mast", params=params, data=datas, headers=headers, verify=False)
            response = resp.content.decode("utf-8")
            return HttpResponse(response)
        elif (jsondata.get('Group')) == 'Supplier_Set' and (jsondata.get('Action')) == 'SUPP_INSERT':
            group = jsondata.get('Group')
            action = jsondata.get('Action')
            params = {'Group': "" + group + "", 'Action': "" + action + ""}
            datas = json.dumps(jsondata.get('key'))
            token = jwt.token(request)
            headers = {"content-type": "application/json", "Authorization": "" + token + ""}
            resp = requests.post("" + ip + "/Supplier_Mast", params=params, data=datas, headers=headers, verify=False)
            response = resp.content.decode("utf-8")
            return HttpResponse(response)
        elif (jsondata.get('Group')) == 'Supplier_Set' and (jsondata.get('Action')) == 'SUPP_UPDATE':
            group = jsondata.get('Group')
            action = jsondata.get('Action')
            params = {'Group': "" + group + "", 'Action': "" + action + ""}
            datas = json.dumps(jsondata.get('value'))
            token = jwt.token(request)
            headers = {"content-type": "application/json", "Authorization": "" + token + ""}
            resp = requests.post("" + ip + "/Supplier_Mast", params=params, data=datas, headers=headers, verify=False)
            response = resp.content.decode("utf-8")
            return HttpResponse(response)
        elif (jsondata.get('Group')) == 'Supplier_Set' and (jsondata.get('Action')) == 'SUPPLIER_GROUP_INSERT':
            group = jsondata.get('Group')
            action = jsondata.get('Action')
            params = {'Group': "" + group + "", 'Action': "" + action + ""}
            datas = json.dumps(jsondata.get('value'))
            token = jwt.token(request)
            headers = {"content-type": "application/json", "Authorization": "" + token + ""}
            resp = requests.post("" + ip + "/Supplier_Mast", params=params, data=datas, headers=headers, verify=False)
            response = resp.content.decode("utf-8")
            return HttpResponse(response)
        elif (jsondata.get('Group')) == 'Supplier_Set' and (jsondata.get('Action')) == 'SUPPLIER_GROUP_UPDATE':
            group = jsondata.get('Group')
            action = jsondata.get('Action')
            params = {'Group': "" + group + "", 'Action': "" + action + ""}
            datas = json.dumps(jsondata.get('value'))
            token = jwt.token(request)
            headers = {"content-type": "application/json", "Authorization": "" + token + ""}
            resp = requests.post("" + ip + "/Supplier_Mast", params=params, data=datas, headers=headers, verify=False)
            response = resp.content.decode("utf-8")
            return HttpResponse(response)

        elif (jsondata.get('Group')) == 'Active_INactive_supplier':
            group = jsondata.get('Group')
            action = jsondata.get('Action')
            params = {'Group': "" + group + "", 'Action': "" + action + ""}
            datas = json.dumps(jsondata.get('data'))
            token = jwt.token(request)
            headers = {"content-type": "application/json", "Authorization": "" + token + ""}
            resp = requests.post("" + ip + "/Supplier_Mast", params=params, data=datas, headers=headers, verify=False)
            response = resp.content.decode("utf-8")
            return HttpResponse(response)


def Supplierproduct_index(request):
    utl.check_authorization(request)
    utl.check_pointaccess(request)
    return render(request, "Supplier/Supplier_Rate.html")


def productorservice(request):
    utl.check_authorization(request)
    if request.method == 'POST':
        jsondata = json.loads(request.body.decode('utf-8'))
        if (jsondata.get('Group')) == 'GET_ALL_PRODUCT':
            grp = jsondata.get('Group')
            typ = jsondata.get('Type')
            sbtyp = jsondata.get('Sub_Type')
            params = {'Group': "" + grp + "", 'Type': "" + typ + "", 'Sub_Type': "" + sbtyp + "",'Entity_Gid':request.session['Entity_gid']}
            token = jwt.token(request)
            headers = {"content-type": "application/json", "Authorization": "" + token + ""}
            datas = json.dumps(jsondata.get('data'))
            resp = requests.post("" + ip + "/All_product_get", params=params, data=datas, headers=headers, verify=False)
            response = resp.content.decode("utf-8")
            return HttpResponse(response)


# All_product_get
def All_product_get(request):
    utl.check_authorization(request)
    utl.check_pointaccess(request)
    if request.method == 'POST':
        jsondata = json.loads(request.body.decode('utf-8'))
        params = {'Group': 'GET_ALL_PRODUCT', 'Type': 'PRODUCT', 'Sub_Type': 'ALL'}
        token = jwt.token(request)
        headers = {"content-type": "application/json", "Authorization": "" + token + ""}
        datas = json.dumps(jsondata)
        resp = requests.post("" + ip + "/All_product_get", params=params, data=datas, headers=headers, verify=False)
        response = resp.content.decode("utf-8")
        return HttpResponse(response)


def ccbs_master(request):
    utl.check_authorization(request)
    if request.method == 'POST':
        jsondata = json.loads(request.body.decode('utf-8'))
        group = jsondata.get('Group')
        type = jsondata.get('Type')
        sub_type = jsondata.get('Sub_type')
        params = {'Group': "" + group + "", 'Type': "" + type + "", 'Sub_type': "" + sub_type + ""}
        #datas = json.dumps(jsondata.get('data'))
        token = jwt.token(request)
        headers = {"content-type": "application/json", "Authorization": "" + token + ""}
        datas = json.dumps(jsondata.get('data'))
        resp = requests.post("" + ip + "/ccbsapi", params=params, data=datas, headers=headers, verify=False)
        #data = {"no": datas['category_no'], "name": datas['category_name'],
                #"glno": datas['category_glno'], "isasset": datas['category_isasset'],
                #"isodit": datas['category_isodit']}
        # print(data)
        #mrobject = MasterRequestObject('AP CAT', data, 'post')
        response = resp.content.decode("utf-8")
        return HttpResponse(response)


def main_category_master(request):
    utl.check_authorization(request)
    if request.method == 'GET':
        obj_master = mMasters.Masters()
        dict_dept = obj_master.get_main_category()
        print(len(dict_dept))
        i = 0;
        res = [];
        while i < len(dict_dept):
            res.append(dict_dept[i].to_json(orient='records'))
            i = i + 1;
        print(res);
        return HttpResponse(json.dumps(res));


def cat_subcat_master(request):
    utl.check_authorization(request)
    if request.method == 'POST':
        jsondata = json.loads(request.body.decode('utf-8'))
        group = jsondata.get('Group')
        type = jsondata.get('Type')
        sub_type = jsondata.get('Sub_type')
        params = {'Group': "" + group + "", 'Type': "" + type + "", 'Sub_type': "" + sub_type + ""}
        datas = json.dumps(jsondata.get('data'))
        temp_data = json.loads(datas)['Params']
        temp_data = temp_data['FILTER']
        token = jwt.token(request)
        headers = {"content-type": "application/json", "Authorization": "" + token + ""}
        datas = json.dumps(jsondata.get('data'))
        resp = requests.post("" + ip + "/ccbsapi", params=params, data=datas, headers=headers, verify=False)
        response = resp.content.decode("utf-8")

        return HttpResponse(response)

def get_bus_seg(request):
    if request.method == 'POST':
        token = jwt.token(request)
        jsondata = json.loads(request.body.decode('utf-8'))
        if (jsondata.get('params').get('Group')) == 'BUS_DATA':
            entity = request.session['Entity_gid']
            drop_b = {
                "Table_name": "ap_mst_tbusinesssegment",
                "Column_1": "businesssegment_gid,businesssegment_no,businesssegment_name,businesssegment_description",
                "Column_2": "",
                "Where_Common": "businesssegment",
                "Where_Primary": "",
                "Primary_Value": "",
                "Order_by": "gid"
            }
            response = alltable(drop_b, entity,token)
            return HttpResponse(response)
        elif (jsondata.get('params').get('Group')) == 'BUS_DATA_GID':
            bus_gid = jsondata.get('params').get('Businesssegment_Gid')
            entity = request.session['Entity_gid']
            drop_b = {
                "Table_name": "ap_mst_tbusinesssegment",
                "Column_1": "businesssegment_gid,businesssegment_no,businesssegment_name,businesssegment_description",
                "Column_2": "",
                "Where_Common": "businesssegment",
                "Where_Primary": "gid",
                "Primary_Value": bus_gid,
                "Order_by": "gid"
            }
            response = alltable(drop_b, entity,token)
            return HttpResponse(response)
        elif(jsondata.get('params').get('Group')) == 'BUS_DATA_SET':
            act = jsondata.get('params').get('Action')
            grp = jsondata.get('params').get('Group')
            typ = jsondata.get('params').get('Type')
            sub = jsondata.get('params').get('Sub_Type')
            emp = request.session['Emp_gid']
            params = {"Action": act, "Group": grp, "Type": typ, "Sub_Type": sub,
                      "Employee_Gid": emp}
            headers = {"content-type": "application/json", "Authorization": "" + token + ""}
            classify = {
                "CLASSIFICATION": {
                    "Entity_Gid": request.session['Entity_gid']
                }}
            jsondata['params']['json']['Params'].update(classify)
            datas = json.dumps(jsondata.get('params').get('json'))
            resp = requests.post("" + ip + "/BUSINESS_SEG", params=params, data=datas, headers=headers,
                                 verify=False)
            response = resp.content.decode("utf-8")
            return HttpResponse(response)

def get_exemapping(request):
    utl.check_pointaccess(request)
    if request.method == 'GET':
        objexe = mMasters.Masters()
        objexe.employee_gid = 0
        objexe.action = ''
        objexe.entity_gid = decry_data(request.session['Entity_gid'])
        df_executive = objexe.getexecmapping()
        jdata = df_executive.to_json(orient='records')
        return JsonResponse(json.loads(jdata), safe=False)


# //suppliercode
def suppcode(request):
    utl.check_authorization(request)
    utl.check_pointaccess(request)
    if request.method == 'POST':
        obj = mMasters.Masters()
        jsondata = json.loads(request.body.decode('utf-8'))
        obj.array = jsondata.get('Action')
        obj_cancel_data = obj.suppliercode()
        jdata = obj_cancel_data[0]
        return JsonResponse(jdata, safe=False)


def department(request):
    utl.check_pointaccess(request)
    if request.method == 'GET':
        obj_master = mMasters.Masters()
        obj_master.table_name = request.GET['table_name']
        obj_master.gid = request.GET['gid']
        obj_master.entity_gid = decry_data(request.session['Entity_gid'])
        dict_dept = obj_master.get_Masters()
        return JsonResponse(json.dumps(dict_dept), safe=False)


def employee_get(request):
    utl.check_authorization(request)
    utl.check_pointaccess(request)
    if request.method == 'GET':
        obj_master = mMasters.Masters()
        obj_master.employee_gid = decry_data(request.session['Emp_gid'])
        obj_master.employee_name = request.GET['emp_name']
        obj_master.cluster_gid = request.GET['li_cluster_gid']
        obj_master.cluster = request.GET['cluster']
        entity = decry_data(request.session['Entity_gid'])
        obj_master.jsonData = json.dumps({"entity_gid": [entity], "client_gid": []})
        df_view = obj_master.get_employee()
        jdata = df_view.to_json(orient='records')
        return JsonResponse(json.loads(jdata), safe=False)


def employee_getexcel(request):
    utl.check_authorization(request)
    utl.check_pointaccess(request)
    if request.method == 'GET':
        obj_master = mMasters.Masters()
        obj_master.employee_gid = 0
        obj_master.employee_name = ''
        obj_master.cluster_gid = 0
        obj_master.cluster = 'ALL'
        entity = decry_data(request.session['Entity_gid'])
        obj_master.jsonData = json.dumps({"entity_gid": [entity], "client_gid": []})
        XLSX_MIME = 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        response = HttpResponse(content_type=XLSX_MIME)
        filename = Excelfilename('Employee Details_')
       # filename = Excelfilename('Outstandingreport Details_')
        response['Content-Disposition'] = 'attachment; filename="{}"'.format(filename)
        # response['Content-Disposition'] = 'attachment; filename="PythonExport.xlsx"'
        writer = pd.ExcelWriter(response, engine='xlsxwriter')
        df_view = obj_master.get_employee()
        df_view.to_excel(writer, 'Sheet1')
        writer.save()
        return response


def execmapping_excel(request):
    utl.check_pointaccess(request)
    if request.method == 'GET':
        obj_master = mMasters.Masters()
        obj_master.employee_gid = 0
        obj_master.employee_name = ''
        obj_master.cluster_gid = 0
        obj_master.cluster = 'ALL'
        obj_master.entity_gid = decry_data(request.session['Entity_gid'])
        XLSX_MIME = 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        response = HttpResponse(content_type=XLSX_MIME)
        filename = Excelfilename('Executive Mapping Details_')
        response['Content-Disposition'] = 'attachment; filename="{}"'.format(filename)
        #response['Content-Disposition'] = 'attachment; filename="execmapping.xlsx"'
        writer = pd.ExcelWriter(response, engine='xlsxwriter')
        df_view = obj_master.getexecmapping()
        df_view.to_excel(writer, 'Sheet1')
        writer.save()
        return response


def departmentIndex(request):
    utl.check_authorization(request)
    utl.check_pointaccess(request)
    return render(request, "employee/bigflow_mst_department.html")


def dept_get(request):
    utl.check_pointaccess(request)
    if request.method == 'GET':
        formm = mMasters.Masters()
        formm.entity_gid = decry_data(request.session['Entity_gid'])
        dict_add = formm.get_department()
        return JsonResponse(json.dumps(dict_add), safe=False)



def departjson(request):
    utl.check_pointaccess(request)
    if request.method == 'POST':
        obj_setdept = mMasters.Masters()
        jsondata = json.loads(request.body.decode('utf-8'))
        obj_setdept.action = jsondata.get('parms').get('action')
        obj_setdept.department_gid = jsondata.get('parms').get('li_dept_gid')
        obj_setdept.department_code = jsondata.get('parms').get('ls_dept_code')
        obj_setdept.department_name = jsondata.get('parms').get('ls_dept_name')
        obj_setdept.entity_gid = decry_data(request.session['Entity_gid'])
        obj_setdept.Employee_gid = decry_data(request.session['Emp_gid'])
        out_message = outputReturn(obj_setdept.set_department(), 0)
        return JsonResponse(out_message, safe=False)


def depteditjson(request):
    utl.check_pointaccess(request)
    if request.method == 'POST':
        jsondata = json.loads(request.body.decode('utf-8'))
        print(jsondata)
        f1 = jsondata.get('parms').get('dept_gid')
        result = mMasters.Masters.get_departedit(f1)
        if (result != ''):
            print(result)
            output = result
            return JsonResponse(json.dumps(output), safe=False)


def deptdeletejson(request):
    utl.check_pointaccess(request)
    if request.method == 'POST':
        jsondata = json.loads(request.body.decode('utf-8'))
        print(jsondata)
        f1 = jsondata.get('parms').get('dept_gid')
        result = mMasters.Masters.get_departdelete(f1)
        if (result != ''):
            print(result)
            output = result
            return JsonResponse(json.dumps(output), safe=False)


def deptactivejson(request):
    utl.check_pointaccess(request)
    if request.method == 'POST':
        jsondata = json.loads(request.body.decode('utf-8'))
        print(jsondata)
        f1 = jsondata.get('parms').get('dept_gid')
        result = mMasters.Masters.get_departactive(f1)
        if (result != ''):
            print(result)
            output = result
            return JsonResponse(json.dumps(output), safe=False)


def deptinactivejson(request):
    utl.check_pointaccess(request)
    if request.method == 'POST':
        jsondata = json.loads(request.body.decode('utf-8'))
        print(jsondata)
        f1 = jsondata.get('parms').get('dept_gid')
        result = mMasters.Masters.get_departinactive(f1)
        if (result != ''):
            print(result)
            output = result
            return JsonResponse(json.dumps(output), safe=False)


def courier_summary_get(request):
    utl.check_pointaccess(request)
    if request.method == 'GET':
        obj_master = mMasters.Masters()
        # obj_master.employee_gid = request.GET['emp_gid']
        obj_master.entity_gid = decry_data(request.session['Entity_gid'])
        df_view = obj_master.get_courier_summary()
        jdata = df_view.to_json(orient='records')
        return JsonResponse(json.loads(jdata), safe=False)


def cluster_get(request):
    utl.check_pointaccess(request)
    if request.method == 'GET':
        obj_masCluster = mMasters.Masters()
        obj_masCluster.action = request.GET['action']
        obj_masCluster.cluster_parent_gid = request.GET['parent_gid']
        obj_masCluster.hierarchy_gid = request.GET['hierarchy_gid']
        entity = decry_data(request.session['Entity_gid'])
        obj_masCluster.jsondata = json.dumps({"entity_gid": [entity], "client_gid": []})
        dict_clust = obj_masCluster.get_cluster()
        jdata = dict_clust.to_json(orient='records')
        return JsonResponse(jdata, safe=False)


def get_custgroup(request):
    utl.check_pointaccess(request)
    if request.method == 'GET':
        obj_master = mMasters.Masters()
        obj_master.table_name = 'customergroup'
        obj_master.entity_gid = decry_data(request.session['Entity_gid'])
        dict_custgrp = obj_master.get_Masters()
        return JsonResponse(json.dumps(dict_custgrp), safe=False)


def get_contctgroup(request):
    utl.check_authorization(request)
    utl.check_pointaccess(request)
    if request.method == 'GET':
        obj_master = mMasters.Masters()
        obj_master.table_name = 'contacttype'
        obj_master.entity_gid = decry_data(request.session['Entity_gid'])

        log_data = [{"ATMA_BEFORE_get_contctgroup":"contacttype" }]
        common.logger.error(log_data)

        dict_custgrp = obj_master.get_Masters()

        log_data = [{"ATMA_AFTER_get_contctgroup": dict_custgrp}]
        common.logger.error(log_data)
        return JsonResponse(json.dumps(dict_custgrp), safe=False)


def get_employeeddl(request):
    utl.check_pointaccess(request)
    if request.method == 'GET':
        obj_master = mMasters.Masters()
        obj_master.table_name = 'employee'
        obj_master.entity_gid = decry_data(request.session['Entity_gid'])
        dict_custgrp = obj_master.get_Masters()
        return JsonResponse(json.dumps(dict_custgrp), safe=False)


def Customer_Index(request):
    utl.check_authorization(request)
    utl.check_pointaccess(request)
    return render(request, "Customer/bigflow_mst_customer.html")


def customergrp_get(request):
    utl.check_pointaccess(request)
    if request.method == 'GET':
        custgrp = mMasters.Masters()
        custgrp.custgrp_gid = request.GET['custgrp_gid']
        custgrp.entity_gid = decry_data(request.session['Entity_gid'])
        cust = custgrp.get_custgrp()
        jdata = cust.to_json(orient='records')
        return JsonResponse(jdata, safe=False)


def emp_customer_map_set(request):
    utl.check_pointaccess(request)
    if request.method == 'POST':
        obj_emp_cust_map = mMasters.Masters()
        jsondata = json.loads(request.body.decode('utf-8'))
        obj_emp_cust_map.Employee_gid = jsondata.get('parms').get('emp_gid')
        insertjson = jsondata.get('parms').get('emp_gid')
        out_message = obj_emp_cust_map


def customer_get(request):
    utl.check_pointaccess(request)
    if request.method == 'GET':
        obj_master = mMasters.Masters()
        # obj_master.customer_gid = 335
        obj_master.jsonData = request.GET['jsonData']
        obj_master.entity_gid = decry_data(request.session['Entity_gid'])
        customer = obj_master.get_customer()
        jdata = customer.to_json(orient='records')
        return JsonResponse(jdata, safe=False)


def customer_getexcel(request):
    utl.check_pointaccess(request)
    if request.method == 'GET':
        obj_master = mMasters.Masters()
        obj_master.jsonData = '{}'
        obj_master.entity_gid = decry_data(request.session['Entity_gid'])
        XLSX_MIME = 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        response = HttpResponse(content_type=XLSX_MIME)
        filename = Excelfilename('Customer Details_')
        response['Content-Disposition'] = 'attachment; filename="{}"'.format(filename)

        #response['Content-Disposition'] = 'attachment; filename="PythonExpor.xlsx"'
        writer = pd.ExcelWriter(response, engine='xlsxwriter')
        df_view = obj_master.get_customer()
        df_view.to_excel(writer, 'Sheet1')
        writer.save()
        return response


def custpin_excel(request):
    utl.check_pointaccess(request)
    if request.method == 'GET':
        obj_master = mMasters.Masters()
        customer = obj_master.get_pincust()
        jdata = customer.to_json(orient='records')
        return JsonResponse(jdata, safe=False)


def customeredt_get(request):
    utl.check_pointaccess(request)
    if request.method == 'GET':
        custedt = mMasters.Masters()
        custedt.customer_gid = request.GET['cust_gid']
        custedt.entity_gid = decry_data(request.session['Entity_gid'])
        customer = custedt.get_customer()
        jdata = customer.to_json(orient='records')
        return JsonResponse(jdata, safe=False)


def customercreateIndex(request):
    utl.check_authorization(request)
    utl.check_pointaccess(request)
    return render(request, "Customer/bigflow_mst_customercreate.html")


def locationddl(request):
    utl.check_authorization(request)
    utl.check_pointaccess(request)
    if request.method == 'GET':
        dict_loct = mMasters.Masters()
        dict_loct.entity_gid = decry_data(request.session['Entity_gid'])
        locti = dict_loct.get_Location()
        jdata = locti.to_json(orient='records')
        return JsonResponse(jdata, safe=False)


def stateddl(request):
    utl.check_authorization(request)
    utl.check_pointaccess(request)
    if request.method == 'GET':
        statdddl = mMasters.Masters()
        statdddl.table_name = 'state'
        statdddl.entity_gid = decry_data(request.session['Entity_gid'])
        statdddl.gid = 0
        log_data = [{"BEFORE_stateddl": "STATE"}]
        common.logger.error(log_data)
        state = statdddl.get_ddl()
        log_data = [{"AFTER_stateddl": len(state)}]
        common.logger.error(log_data)
        jdata = state.to_json(orient='records')
        return JsonResponse(jdata, safe=False)


def empddl(request):
    utl.check_pointaccess(request)
    if request.method == 'GET':
        employee = mMasters.Masters()
        employee.table_name = 'employee'
        employee.entity_gid = decry_data(request.session['Entity_gid'])
        employee.gid = 0
        employname = employee.get_ddl()
        jdata = employname.to_json(orient='records')
        return JsonResponse(jdata, safe=False)


def districtddl(request):
    utl.check_authorization(request)
    utl.check_pointaccess(request)
    if request.method == 'GET':
        distddl = mMasters.Masters()
        distddl.state_gid = request.GET['state_gid']
        distddl.entity_gid = decry_data(request.session['Entity_gid'])

        log_data = [{"BEFORE_districtddl": distddl.state_gid}]
        common.logger.error(log_data)
        district = distddl.get_district()
        log_data = [{"AFTER_districtddl": len(district)}]
        common.logger.error(log_data)
        jdata = district.to_json(orient='records')
        return JsonResponse(jdata, safe=False)


def allpinget(request):
    utl.check_authorization(request)
    utl.check_pointaccess(request)
    if request.method == 'GET':
        obj_pin = mMasters.Masters()
        obj_pin.pincode_no = request.GET['pincode']
        obj_pin.entity_gid = decry_data(request.session['Entity_gid'])
        log_data = [{"BEFORE_allpinget": obj_pin.pincode_no}]
        common.logger.error(log_data)

        district = obj_pin.get_pincode()

        log_data = [{"AFTER_allpinget": district}]
        common.logger.error(log_data)
        jdata = district.to_json(orient='records')
        return JsonResponse(jdata, safe=False)


def cityddl(request):
    utl.check_authorization(request)
    utl.check_pointaccess(request)
    if request.method == 'GET':
        ctyddl = mMasters.Masters()
        ctyddl.district_gid = request.GET['district_gid']
        ctyddl.entity_gid = decry_data(request.session['Entity_gid'])
        log_data = [{"BEFORE_cityddl": ctyddl.district_gid }]
        common.logger.error(log_data)
        city = ctyddl.get_city()
        log_data = [{"AFTER_cityddl":len(city)}]
        common.logger.error(log_data)
        jdata = city.to_json(orient='records')
        return JsonResponse(jdata, safe=False)


def pincode(request):
    utl.check_authorization(request)
    utl.check_pointaccess(request)
    if request.method == 'GET':
        pincd = mMasters.Masters()
        pincd.city_gid = request.GET['city_gid']
        pincd.entity_gid = decry_data(request.session['Entity_gid'])

        log_data = [{"BEFORE_pincode": pincd.city_gid}]
        common.logger.error(log_data)

        pincode = pincd.get_pincode()

        log_data = [{"AFTER_pincode": pincode}]
        common.logger.error(log_data)
        jdata = pincode.to_json(orient='records')
        return JsonResponse(jdata, safe=False)


def customerset(request):
    utl.check_authorization(request)
    utl.check_pointaccess(request)
    if request.method == 'POST':
        custset = mMasters.Masters()
        jsondata = json.loads(request.body.decode('utf-8'))
        custset.action = jsondata.get('parms').get('Action')
        custset.create_by = request.session['Emp_gid']
        custset.entity_gid = request.session['Entity_gid']
        if custset.action == 'Insert':
            loct_gid = jsondata.get('parms').get('details').get('Location')
            if (loct_gid == None):
                custset.pincode_gid = jsondata.get('parms').get('details').get('pincodegid')
                custset.location_name = jsondata.get('parms').get('details').get('loccity')
                custset.cluster_gid = jsondata.get('parms').get('details').get('cluster')
                custset.location_code = '500'
                loc_gid = outputReturn(custset.set_Location(), 0)
            else:
                loc_gid = jsondata.get('parms').get('details').get('Location')
            if (loc_gid > 0):
                custset.location_gid = loc_gid
                custset.add_refcode = 'CUST'
                custset.address1 = jsondata.get('parms').get('details').get('Address1')
                custset.address2 = jsondata.get('parms').get('details').get('Address2')
                custset.address3 = jsondata.get('parms').get('details').get('Address3')
                custset.pincode_no = jsondata.get('parms').get('details').get('pincode')
                custset.state_gid = jsondata.get('parms').get('details').get('state')
                custset.district_gid = jsondata.get('parms').get('details').get('district')
                custset.city_gid = jsondata.get('parms').get('details').get('city')
                address_gid = outputReturn(custset.set_address(), 0)
                if (address_gid > 0):
                    custset.address_gid = address_gid
                    custset.custgrp_gid = jsondata.get('parms').get('details').get('custgrp_gid')
                    custset.customer_name = jsondata.get('parms').get('details').get('cust_name')
                    custset.customer_code = jsondata.get('parms').get('details').get('cust_code')
                    custset.cust_type = jsondata.get('parms').get('details').get('cust_type')
                    custset.custcate_gid = jsondata.get('parms').get('details').get('custcate_gid')
                    custset.constitution_gid = jsondata.get('parms').get('details').get('custconstitut_gid')
                    custset.salemode_gid = jsondata.get('parms').get('details').get('custsalemode_gid')
                    custset.size_gid = jsondata.get('parms').get('details').get('custsize_gid')
                    custset.landmark = jsondata.get('parms').get('details').get('LNDMRK')
                    custset.cust_billingname = jsondata.get('parms').get('details').get('BILLINGANME')
                    custset.cust_subtype = jsondata.get('parms').get('details').get('cust_subtype')
                    result = outputReturn(custset.set_customer(), 0)
                    if (result > 0):
                        custset.contact_gid = result
                        custset.cont_refcode = 'CUST'
                        custset.cont_refgid = result
                        custset.contacttype_gid = jsondata.get('parms').get('details').get('ContactType')
                        custset.conper1 = jsondata.get('parms').get('details').get('Personname')
                        custset.designation_gid = jsondata.get('parms').get('details').get('Designation')
                        custset.landline_no = jsondata.get('parms').get('details').get('Landline1')
                        custset.landline_no1 = jsondata.get('parms').get('details').get('Landline2')
                        custset.mobile_no = jsondata.get('parms').get('details').get('Mobilenum')
                        custset.mobile_no1 = jsondata.get('parms').get('details').get('Mobilenum2')
                        custset.email = jsondata.get('parms').get('details').get('Emailid')
                        if (jsondata.get('parms').get('details').get('BirthDate') != ''):
                            custset.cont_dob = common.convertDate(
                                jsondata.get('parms').get('details').get('BirthDate'))
                        else:
                            custset.cont_dob = ''
                        if (jsondata.get('parms').get('details').get('Wedingday') != ''):
                            custset.wedding_day = common.convertDate(
                                jsondata.get('parms').get('details').get('Wedingday'))
                        else:
                            custset.wedding_day = ''
                        resultc = outputReturn(custset.set_contact(), 0)
                        gstno = jsondata.get('parms').get('details').get('GSTNO')
                        if (gstno == '' or gstno == None):
                            courier = jsondata.get('parms').get('details').get('COURIER')
                            if (courier == '' or courier == None):
                                return JsonResponse(result, safe=False)
                            else:
                                custset.jsondata = '{}'
                                custset.cust_courier_gid = jsondata.get('parms').get('details').get('cust_courier_gid')
                                custset.customer_gid = result
                                custset.courier_gid = jsondata.get('parms').get('details').get('COURIER')
                                custset.remark = ''
                                custset.from_date = jsondata.get('parms').get('details').get('COURIER_fromdate')
                                custset.to_date = jsondata.get('parms').get('details').get('COURIER_todate')
                                resultcou = outputReturn(custset.set_courierdetails(), 0)
                                if (resultcou > 0):
                                    return JsonResponse(resultcou, safe=False)
                                else:
                                    return JsonResponse('Courier Not Inserted', safe=False)
                        else:
                            custset.gstno = gstno
                            custset.tax_code = 'GST'
                            custset.subtax_name = 'CGST'
                            custset.ref_name = 'CUST_GST'
                            custset.tax_type = 'C'
                            custset.reftbl_code = jsondata.get('parms').get('details').get('cust_code')
                            result1 = outputReturn(custset.set_taxdetails(), 0)
                            if (result1 > 0):
                                courier = jsondata.get('parms').get('details').get('COURIER')
                                if (courier == '' or courier == None):
                                    return JsonResponse(result1, safe=False)
                                else:
                                    custset.jsondata = '{}'
                                    custset.cust_courier_gid = jsondata.get('parms').get('details').get(
                                        'cust_courier_gid')
                                    custset.customer_gid = result
                                    custset.courier_gid = jsondata.get('parms').get('details').get('COURIER')
                                    custset.remark = ''
                                    custset.from_date = jsondata.get('parms').get('details').get('COURIER_fromdate')
                                    custset.to_date = jsondata.get('parms').get('details').get('COURIER_todate')
                                    resultcou = outputReturn(custset.set_courierdetails(), 0)
                                    if (resultcou > 0):
                                        return JsonResponse(resultcou, safe=False)
                                    else:
                                        return JsonResponse('Courier Not Inserted', safe=False)
                            else:
                                return JsonResponse('GST Not Inserted', safe=False)


                    else:
                        return JsonResponse('Customer Not Inserted', safe=False)
                else:
                    return JsonResponse('Address Not Inserted', safe=False)
            else:
                return JsonResponse('Location Not Inserted', safe=False)
        else:
            custset.location_gid = jsondata.get('parms').get('details').get('Location')
            custset.pincode_gid = jsondata.get('parms').get('details').get('pincodegid')
            custset.location_name = jsondata.get('parms').get('details').get('loccity')
            custset.cluster_gid = jsondata.get('parms').get('details').get('cluster')
            custset.location_code = '500'
            loc_result = outputReturn(custset.set_Location(), 0)
            if (loc_result == 'SUCCESS'):
                custset.add_refcode = 'CUST'
                custset.address1 = jsondata.get('parms').get('details').get('Address1')
                custset.address2 = jsondata.get('parms').get('details').get('Address2')
                custset.address3 = jsondata.get('parms').get('details').get('Address3')
                custset.pincode_no = jsondata.get('parms').get('details').get('pincode')
                custset.state_gid = jsondata.get('parms').get('details').get('state')
                custset.district_gid = jsondata.get('parms').get('details').get('district')
                custset.city_gid = jsondata.get('parms').get('details').get('city')
                address_gid = jsondata.get('parms').get('details').get('Address_gid')
                if (address_gid > 0):
                    custset.action = 'Update'
                    custset.address_gid = address_gid
                    add_result = outputReturn(custset.set_address(), 0)
                else:
                    custset.action = 'Insert'
                    outmsg = outputReturn(custset.set_address(), 0)
                    if (outmsg > 0):
                        address_gid = outmsg
                        add_result = 'SUCCESS'
                if (add_result == 'SUCCESS'):
                    custset.action = 'Update'
                    custset.custgrp_gid = jsondata.get('parms').get('details').get('custgrp_gid')
                    custset.customer_name = jsondata.get('parms').get('details').get('cust_name')
                    custset.customer_code = jsondata.get('parms').get('details').get('cust_code')
                    custset.cust_type = jsondata.get('parms').get('details').get('cust_type')
                    custset.cust_subtype = jsondata.get('parms').get('details').get('cust_subtype')
                    custset.custcate_gid = jsondata.get('parms').get('details').get('custcate_gid')
                    custset.constitution_gid = jsondata.get('parms').get('details').get('custconstitut_gid')
                    custset.salemode_gid = jsondata.get('parms').get('details').get('custsalemode_gid')
                    custset.size_gid = jsondata.get('parms').get('details').get('custsize_gid')
                    custset.landmark = jsondata.get('parms').get('details').get('LNDMRK')
                    custset.cust_billingname = jsondata.get('parms').get('details').get('BILLINGANME')
                    custset.address_gid = address_gid
                    custset.customer_gid = jsondata.get('parms').get('details').get('cust_gid')
                    result = outputReturn(custset.set_customer(), 0)
                    if (result == 'SUCCESS'):
                        custset.cont_refcode = 'CUST'
                        custset.cont_refgid = jsondata.get('parms').get('details').get('cust_gid')
                        custset.contacttype_gid = jsondata.get('parms').get('details').get('ContactType')
                        custset.conper1 = jsondata.get('parms').get('details').get('Personname')
                        custset.designation_gid = jsondata.get('parms').get('details').get('Designation')
                        custset.landline_no = jsondata.get('parms').get('details').get('Landline1')
                        custset.landline_no1 = jsondata.get('parms').get('details').get('Landline2')
                        custset.mobile_no = jsondata.get('parms').get('details').get('Mobilenum')
                        custset.mobile_no1 = jsondata.get('parms').get('details').get('Mobilenum2')
                        custset.email = jsondata.get('parms').get('details').get('Emailid')
                        if (jsondata.get('parms').get('details').get('BirthDate') != ''):
                            custset.cont_dob = common.convertDate(
                                jsondata.get('parms').get('details').get('BirthDate'))
                        else:
                            custset.cont_dob = ''
                        if (jsondata.get('parms').get('details').get('Wedingday') != ''):
                            custset.wedding_day = common.convertDate(
                                jsondata.get('parms').get('details').get('Wedingday'))
                        else:
                            custset.wedding_day = ''
                        contact_gid = jsondata.get('parms').get('details').get('contact_gid')
                        if (contact_gid != 0 and contact_gid != None):
                            custset.contact_gid = contact_gid
                            custset.action = 'Update'
                            out_message = outputReturn(custset.set_contact(), 0)
                        else:
                            custset.action = 'Insert'
                            outmsg1 = outputReturn(custset.set_contact(), 0)
                            if (outmsg1 > 0):
                                out_message = 'SUCCESS'
                        if (out_message == 'SUCCESS'):
                            GSTno = jsondata.get('parms').get('details').get('GSTNO')
                            GSTgid = jsondata.get('parms').get('details').get('GSTNO_gid')
                            if (GSTno != 0 and GSTno != None and GSTno != '' and out_message != 0):
                                if (GSTgid == 0 or GSTgid == None):
                                    custset.action = 'Insert'
                                    custset.gstno = jsondata.get('parms').get('details').get('GSTNO')
                                    custset.tax_code = 'GST'
                                    custset.subtax_name = 'CGST'
                                    custset.ref_name = 'CUST_GST'
                                    custset.tax_type = 'C'
                                    custset.reftbl_code = jsondata.get('parms').get('details').get('cust_code')
                                    result1 = outputReturn(custset.set_taxdetails(), 0)
                                    if (result1 > 0):
                                        courier = jsondata.get('parms').get('details').get('COURIER')
                                        cust_courier_gid = jsondata.get('parms').get('details').get('cust_courier_gid')
                                        if (cust_courier_gid == 0 or cust_courier_gid == None):
                                            custset.action = 'Insert'
                                            custset.jsondata = '{}'
                                            custset.cust_courier_gid = jsondata.get('parms').get('details').get(
                                                'cust_courier_gid')
                                            custset.customer_gid = result
                                            custset.courier_gid = jsondata.get('parms').get('details').get('COURIER')
                                            custset.remark = ''
                                            custset.from_date = jsondata.get('parms').get('details').get(
                                                'COURIER_fromdate')
                                            custset.to_date = jsondata.get('parms').get('details').get('COURIER_todate')
                                            resultcou = outputReturn(custset.set_courierdetails(), 0)
                                            if (resultcou > 0):
                                                return JsonResponse(resultcou, safe=False)
                                            else:
                                                return JsonResponse('Courier Not Inserted', safe=False)
                                        else:
                                            custset.action = 'Update'
                                            custset.jsondata = '{}'
                                            custset.courier_gid = jsondata.get('parms').get('details').get('COURIER')
                                            result1 = outputReturn(custset.set_courierdetails(), 0)
                                            if (result1 == 'SUCCESS'):
                                                return JsonResponse(result, safe=False)
                                            else:
                                                return JsonResponse('Courier Not Updated', safe=False)

                                    else:
                                        return JsonResponse('GST Not Inserted', safe=False)
                                else:
                                    custset.action = 'Update'
                                    custset.gstno = jsondata.get('parms').get('details').get('GSTNO')
                                    custset.taxdtl_gid = GSTgid
                                    result1 = outputReturn(custset.set_taxdetails(), 0)
                                    if (result1 == 'SUCCESS'):
                                        courier = jsondata.get('parms').get('details').get('COURIER')
                                        cust_courier_gid = jsondata.get('parms').get('details').get('cust_courier_gid')
                                        if (cust_courier_gid == 0 or cust_courier_gid == None):
                                            custset.action = 'Insert'
                                            custset.jsondata = '{}'
                                            # custset.cust_courier_gid = jsondata.get('parms').get('details').get('cust_courier_gid') to custset.cust_courier_gid =0 by sakthivel
                                            custset.cust_courier_gid = 0
                                            custset.courier_gid = jsondata.get('parms').get('details').get('COURIER')
                                            custset.remark = ''
                                            custset.from_date = jsondata.get('parms').get('details').get(
                                                'COURIER_fromdate')
                                            custset.to_date = jsondata.get('parms').get('details').get('COURIER_todate')
                                            courier_update = custset.set_courierdetails()
                                            resultcou = outputReturn(courier_update, 0)
                                            resultcou1 = outputReturn(courier_update, 1)
                                            if (resultcou > 0):
                                                return JsonResponse(resultcou1, safe=False)
                                            else:
                                                return JsonResponse('Courier Not Inserted', safe=False)
                                        else:
                                            custset.action = 'Update'
                                            custset.jsondata = '{}'
                                            # courier_gid to cust_courier_gid by sakthivel
                                            custset.cust_courier_gid = jsondata.get('parms').get('details').get(
                                                'cust_courier_gid')
                                            custset.courier_gid = jsondata.get('parms').get('details').get('COURIER')
                                            result1 = outputReturn(custset.set_courierdetails(), 0)
                                            if (result1 == 'SUCCESS'):
                                                return JsonResponse(result, safe=False)
                                            else:
                                                return JsonResponse('Courier Not Updated', safe=False)
                                    else:
                                        return JsonResponse('GST Not Updated', safe=False)
                            else:
                                courier = jsondata.get('parms').get('details').get('COURIER')
                                cust_courier_gid = jsondata.get('parms').get('details').get('cust_courier_gid')
                                if (cust_courier_gid == 0 or cust_courier_gid == None):
                                    custset.action = 'Insert'
                                    custset.jsondata = '{}'
                                    custset.courier_gid = jsondata.get('parms').get('details').get('COURIER')
                                    custset.cust_courier_gid = jsondata.get('parms').get('details').get(
                                        'cust_courier_gid')
                                    custset.customer_gid = result
                                    custset.remark = ''
                                    custset.from_date = jsondata.get('parms').get('details').get('COURIER_fromdate')
                                    custset.to_date = jsondata.get('parms').get('details').get('COURIER_todate')
                                    resultcou = outputReturn(custset.set_courierdetails(), 0)
                                    if (resultcou > 0):
                                        return JsonResponse(resultcou, safe=False)
                                    else:
                                        return JsonResponse('Courier Not Inserted', safe=False)
                                else:
                                    custset.action = 'Update'
                                    custset.jsondata = '{}'
                                    custset.courier_gid = jsondata.get('parms').get('details').get('COURIER')
                                    custset.cust_courier_gid = jsondata.get('parms').get('details').get(
                                        'cust_courier_gid')
                                    result1 = outputReturn(custset.set_courierdetails(), 0)
                                    if (result1 == 'SUCCESS'):
                                        return JsonResponse(result, safe=False)
                                    else:
                                        return JsonResponse('Courier Not Updated', safe=False)

                        else:
                            return JsonResponse('Contact Not Updated', safe=False)
                    else:
                        return JsonResponse('Customer Not Updated', safe=False)
                else:
                    return JsonResponse('Address Not Updated', safe=False)
            else:
                return JsonResponse('Location Not Updated', safe=False)


def outputReturn(tubledtl, index):
    temp = tubledtl[0].split(',')
    if (len(temp) > 1):
        if (index == 0):
            return int(temp[0])
        else:
            return temp[1]
    else:
        return temp[0]


def locationget(request):
    utl.check_authorization(request)
    utl.check_pointaccess(request)
    if request.method == 'GET':
        loct = mMasters.Masters()
        loct.location_gid = request.GET['location_gid']
        loct.entity_gid = decry_data(request.session['Entity_gid'])
        dict_loct = loct.get_Location()
        jdata = dict_loct.to_json(orient='records')
        return JsonResponse(jdata, safe=False)


def addressget(request):
    utl.check_authorization(request)
    utl.check_pointaccess(request)
    if request.method == 'GET':
        add = mMasters.Masters()
        add.address_gid = request.GET['add_gid']
        add.entity_gid = decry_data(request.session['Entity_gid'])
        dict_add = add.get_address()
        jdata = dict_add.to_json(orient='records')
        return JsonResponse(jdata, safe=False)


def customerdel(request):
    utl.check_pointaccess(request)
    if request.method == 'POST':
        cust_del = mMasters.Masters()
        jsondata = json.loads(request.body.decode('utf-8'))
        cust_del.customer_gid = jsondata.get('params').get('cust_gid')
        cust_del.action = jsondata.get('params').get('Action')
        del_res = outputReturn(cust_del.set_customer(), 0)
        return JsonResponse(del_res, safe=False)


def getMappedLocation(request):
    utl.check_pointaccess(request)
    if request.method == 'GET':
        obj_mapped_customer = mFET.FET_model()
        obj_mapped_customer.Employee_gid = request.GET['emp_gid']
        obj_mapped_customer.entity_gid = decry_data(request.session['Entity_gid'])
        df_mapped_customer = obj_mapped_customer.get_mapped_customer()
        df_mappedLocation = (df_mapped_customer[['location_gid', 'location_name']]) \
            .groupby(['location_gid', 'location_name']).size().reset_index();
        return JsonResponse(json.loads(df_mappedLocation.to_json(orient='records')), safe=False)


def setRouteDtl(request):
    utl.check_pointaccess(request)
    if request.method == 'POST':
        obj_setroute = mMasters.Masters()
        jsondata = json.loads(request.body.decode('utf-8')).get('parms')
        obj_setroute.action = jsondata.get('action')
        obj_setroute.json_employee_gid = json.dumps(jsondata.get('emp_gid'))
        obj_setroute.routeHead_gid = jsondata.get('routeHead_gid')
        obj_setroute.route_code = jsondata.get('route_code')
        obj_setroute.route_name = jsondata.get('route_name')
        obj_setroute.remark = jsondata.get('remark')
        obj_setroute.jsonData = json.dumps(jsondata.get('location_dtl'))
        obj_setroute.create_by = decry_data(request.session['Emp_gid'])
        obj_setroute.entity_gid = decry_data(request.session['Entity_gid'])
        out_message = outputReturn(obj_setroute.setRouteDtl(), 1)
        return JsonResponse(out_message, safe=False)


def getRouteDtl(request):
    utl.check_pointaccess(request)
    if request.method == 'GET':
        obj_getRouteDtl = mMasters.Masters()
        obj_getRouteDtl.action = request.GET['action']
        obj_getRouteDtl.routeHead_gid = request.GET['routeHead_gid']
        obj_getRouteDtl.route_code = request.GET['route_code']
        obj_getRouteDtl.route_name = request.GET['route_name']
        obj_getRouteDtl.json_employee_gid = request.GET['emp_gid']
        obj_getRouteDtl.entity_gid = decry_data(request.session['Entity_gid'])
        df_getRoute = obj_getRouteDtl.getRouteDtl()
        if request.GET['action'] == 'HEADER_DETAILS':
            df_getRoute = (
                df_getRoute[
                    ['routeheader_gid', 'routeheader_code', 'routeheader_name', 'routeheader_remarks']]).groupby(
                ['routeheader_gid', 'routeheader_code', 'routeheader_name',
                 'routeheader_remarks']).size().reset_index();
        elif request.GET['action'] == 'ROUTE_EMPLOYEE' or request.GET['action'] == 'ROUTE_LOCATION':
            df_getRoute['status'] = df_getRoute['status'].astype(bool)
            if obj_getRouteDtl.routeHead_gid == '0':
                df_getRoute = df_getRoute.drop('status', axis=1)
        return JsonResponse(json.loads(df_getRoute.to_json(orient='records')), safe=False)


def gettownn(request):
    utl.check_pointaccess(request)
    if request.method == 'GET':
        obj_custcate = mMasters.Masters()
        obj_custcate.action = request.GET['action']
        obj_custcate.routeHead_gid = request.GET['routeHead_gid']
        obj_custcate.entity_gid = decry_data(request.session['Entity_gid'])
        dict_custgrp = obj_custcate.getRouteDtl()
        return JsonResponse(json.loads(dict_custgrp.to_json(orient='records')), safe=False)


def getrout(request):
    utl.check_pointaccess(request)
    if request.method == 'GET':
        obj_custcate = mMasters.Masters()
        obj_custcate.action = request.GET['action']
        obj_custcate.json_cluster_gid = request.GET['cluster_gid']
        obj_custcate.entity_gid = decry_data(request.session['Entity_gid'])
        dict_custgrp = obj_custcate.getRouteDtl()
        return JsonResponse(json.loads(dict_custgrp.to_json(orient='records')), safe=False)


def CustomerTerritoryIndex(request):
    utl.check_authorization(request)
    utl.check_pointaccess(request)
    return render(request, "Customer/customer_territory.html")


def getClusterDtl(request):
    utl.check_pointaccess(request)
    if request.method == 'GET':
        obj_clusterDtl = mMasters.Masters()
        obj_clusterDtl.action = 'ALL'
        obj_clusterDtl.cluster_parent_gid = 0
        obj_clusterDtl.hierarchy_gid = 0
        entity = decry_data(request.session['Entity_gid'])
        obj_clusterDtl.jsondata = json.dumps({"entity_gid": [entity], "client_gid": []})
        df_cluster = obj_clusterDtl.get_cluster()
        obj_clusterDtl.action = 'R'
        obj_clusterDtl.entity_gid = entity
        df_hierarchy = obj_clusterDtl.getHierarchy()
        test = []
        for x, hier in df_hierarchy.iterrows():
            re = df_cluster[df_cluster['cluster_hierarchygid'] == hier['hierarchy_gid']]
            test.append(re)
        df_hierarchy['clustlist'] = test
        jdata = df_hierarchy.to_json(orient='records')
        return JsonResponse(json.loads(jdata), safe=False)


def setCluster(request):
    utl.check_pointaccess(request)
    if request.method == 'POST':
        obj_clstrset = mMasters.Masters()
        jsondata = json.loads(request.body.decode('utf-8'))
        obj_clstrset.action = jsondata.get('parms').get('action')
        obj_clstrset.cluster_gid = jsondata.get('parms').get('li_clus_gid')
        obj_clstrset.cluster_name = jsondata.get('parms').get('ls_clus_name')
        obj_clstrset.cluster_parent_gid = jsondata.get('parms').get('li_parent_gid')
        obj_clstrset.hierarchy_gid = jsondata.get('parms').get('li_hierarchy_gid')
        obj_clstrset.entity_gid = decry_data(request.session['Entity_gid'])
        obj_clstrset.Employee_gid = decry_data(request.session['Emp_gid'])
        out_message = outputReturn(obj_clstrset.setCluster(), 0)
        return JsonResponse(out_message, safe=False)


def sideNavFilterIndex(request):
    utl.check_authorization(request)
    utl.check_pointaccess(request)
    return render(request, "Shared/sideNavFilter.html")


# def dept_get(request):
#     if 'HTTP_REFERER' in request.META:
#         if request.method == 'GET':
#             formm = mMasters.Masters()
#             formm.entity_gid = decry_data(request.session['Entity_gid'])
#             dict_add = formm.get_department()
#             return JsonResponse(json.dumps(dict_add), safe=False)
#     else:
#
#         return render(request, "Shared/error_403.html", {'test': 'noaccess'})

def dept_get(request):
    # utl.check_authorization(request)
    # utl.check_pointaccess(request)
    if request.method == 'GET':
        formm = mMasters.Masters()
        formm.entity_gid = '1'
        dict_add = formm.get_department()
        return JsonResponse(json.dumps(dict_add), safe=False)



def desg_get(request):
    utl.check_authorization(request)
    utl.check_pointaccess(request)
    if request.method == 'GET':
        formm = mMasters.Masters()
        formm.entity_gid = decry_data(request.session['Entity_gid'])

        log_data = [{"BEFORE_desgjson":formm.entity_gid }]
        common.logger.error(log_data)

        dict_add = formm.get_designation()

        log_data = [{"AFTER_desgjson": len(dict_add)}]
        common.logger.error(log_data)
        return JsonResponse(json.dumps(dict_add), safe=False)

# Product
def productdetails(request):
    utl.check_authorization(request)
    return render(request, "Product/Product_details.html")


# def productcreate(request):
#     return render(request, "Product/Product_create.html")

def productadd(request):
    utl.check_authorization(request)
    return render(request, "Product/Product_Add.html")


def productIndex(request):
    utl.check_authorization(request)
    return render(request, "Product/Product_summary.html")


def productcategoryIndex(request):
    utl.check_authorization(request)
    return render(request, "Product/Product_category.html")


def producttypeIndex(request):
    utl.check_authorization(request)
    return render(request, "Product/Product_type.html")


def categoryget(request):
    utl.check_authorization(request)
    utl.check_pointaccess(request)
    if request.method == 'GET':
        form = mMasters.Masters
        jdata = form.get_category(request)
        return JsonResponse(json.dumps(jdata), safe=False)


def typeget(request):
    utl.check_authorization(request)
    utl.check_pointaccess(request)
    if request.method == 'GET':
        types = mMasters.Masters()
        types.prodcat_gid = request.GET['prodcat_gid']
        dict_add = types.getproduct_types()
        jdata = dict_add.to_json(orient='records')
        return JsonResponse(jdata, safe=False)


def get_custcate(request):
    utl.check_pointaccess(request)
    if request.method == 'GET':
        obj_custcate = mMasters.Masters()
        obj_custcate.table_name = 'custcategory'
        obj_custcate.entity_gid = decry_data(request.session['Entity_gid'])
        dict_custgrp = obj_custcate.get_Masters()
        return JsonResponse(json.dumps(dict_custgrp), safe=False)


def get_cluster(request):
    utl.check_pointaccess(request)
    if request.method == 'GET':
        obj_locCluster = mMasters.Masters()
        obj_locCluster.action = request.GET['action']
        entity = decry_data(request.session['Entity_gid'])
        obj_locCluster.jsondata = json.dumps({"entity_gid": [entity], "client_gid": []})
        dict_locclust = obj_locCluster.get_cluster()
        jdata = dict_locclust.to_json(orient='records')
        return JsonResponse(jdata, safe=False)


def get_custdata(request):
    utl.check_pointaccess(request)
    if request.method == 'GET':
        obj_custdata = mMasters.Masters()
        obj_custdata.table_name = request.GET['tablename']
        obj_custdata.column_name = request.GET['columnname']
        obj_custdata.entity_gid = decry_data(request.session['Entity_gid'])
        dict_custdata = obj_custdata.getmetadata()
        jdata = dict_custdata.to_json(orient='records')
        return JsonResponse(jdata, safe=False)


def supplierdetails(request):
    utl.check_pointaccess(request)
    if request.method == 'POST':
        custgrpset = mMasters.Masters()
        jsondata = json.loads(request.body.decode('utf-8'))
        custgrpset.action = jsondata.get('params').get('Action')
        custgrpset.create_by = request.session['Emp_gid']
        custgrpset.entity_gid = request.session['Entity_gid']
        if custgrpset.action == 'SUPP_INSERT':
            custgrpset.action = 'SUPP_INSERT'
            custgrpset.custgrp_gid = jsondata.get('params').get('supplier_details').get('custgrp_gid')
            custgrpset.custgrp_name = jsondata.get('params').get('supplier_details').get('custgrp_name')
            resultsupplier = outputReturn(custgrpset.set_customergroup(), 0)
            if (resultsupplier == 'SUCCESS'):
                return JsonResponse(resultsupplier, safe=False)
            else:
                return JsonResponse('Supplier Not Updated', safe=False)


def customergroupset(request):
    utl.check_pointaccess(request)
    if request.method == 'POST':
        custgrpset = mMasters.Masters()
        jsondata = json.loads(request.body.decode('utf-8'))
        custgrpset.action = jsondata.get('parms').get('Action')
        custgrpset.create_by = request.session['Emp_gid']
        custgrpset.entity_gid = request.session['Entity_gid']
        if custgrpset.action == 'Insert':
            custgrpset.add_refcode = 'CUSTGROUP'
            custgrpset.address1 = jsondata.get('parms').get('grpdetails').get('Address1')
            custgrpset.address2 = jsondata.get('parms').get('grpdetails').get('Address2')
            custgrpset.address3 = jsondata.get('parms').get('grpdetails').get('Address3')
            custgrpset.pincode_no = jsondata.get('parms').get('grpdetails').get('pincode')
            custgrpset.state_gid = jsondata.get('parms').get('grpdetails').get('state')
            custgrpset.district_gid = jsondata.get('parms').get('grpdetails').get('district')
            custgrpset.city_gid = jsondata.get('parms').get('grpdetails').get('city')
            address_gid = outputReturn(custgrpset.set_address(), 0)
            if (address_gid > 0):
                custgrpset.address_gid = address_gid
                custgrpset.custgrp_name = jsondata.get('parms').get('grpdetails').get('custgrp_name')
                custgrpset.custgrp_code = jsondata.get('parms').get('grpdetails').get('custgrp_code')
                custgrpset.conper1 = jsondata.get('parms').get('grpdetails').get('custgrp_cpname1')
                custgrpset.desig1 = jsondata.get('parms').get('grpdetails').get('custgrp_desig1')
                custgrpset.mobile_no = jsondata.get('parms').get('grpdetails').get('custgrp_mobileno1')
                custgrpset.landline_no = jsondata.get('parms').get('grpdetails').get('custgrp_landline1')
                custgrpset.conper2 = jsondata.get('parms').get('grpdetails').get('custgrp_cpname2')
                custgrpset.desig2 = jsondata.get('parms').get('grpdetails').get('custgrp_desig2')
                custgrpset.mobile_no1 = jsondata.get('parms').get('grpdetails').get('custgrp_mobileno2')
                custgrpset.landline_no1 = jsondata.get('parms').get('grpdetails').get('custgrp_landline2')
                custgrpset.entity_gid = request.session['Entity_gid']
                custgrpset.client_gid = jsondata.get('parms').get('grpdetails').get('grpclient_gid')
                result = outputReturn(custgrpset.set_customergroup(), 0)
                return JsonResponse(result, safe=False)
            else:
                return JsonResponse('Address Not Inserted', safe=False)
        else:
            address_gid = jsondata.get('parms').get('grpdetails').get('Address_gid')
            if (address_gid > 0):
                custgrpset.action = 'Update'
                custgrpset.address_gid = address_gid
                custgrpset.add_refcode = 'CUSTGROUP'
                custgrpset.address1 = jsondata.get('parms').get('grpdetails').get('Address1')
                custgrpset.address2 = jsondata.get('parms').get('grpdetails').get('Address2')
                custgrpset.address3 = jsondata.get('parms').get('grpdetails').get('Address3')
                custgrpset.pincode_no = jsondata.get('parms').get('grpdetails').get('pincode')
                custgrpset.state_gid = jsondata.get('parms').get('grpdetails').get('state')
                custgrpset.district_gid = jsondata.get('parms').get('grpdetails').get('district')
                custgrpset.city_gid = jsondata.get('parms').get('grpdetails').get('city')
                add_result = outputReturn(custgrpset.set_address(), 0)

                custgrpset.custgrp_name = jsondata.get('parms').get('grpdetails').get('custgrp_name')
                custgrpset.custgrp_code = jsondata.get('parms').get('grpdetails').get('custgrp_code')
                custgrpset.conper1 = jsondata.get('parms').get('grpdetails').get('custgrp_cpname1')
                custgrpset.desig1 = jsondata.get('parms').get('grpdetails').get('custgrp_desig1')
                custgrpset.mobile_no = jsondata.get('parms').get('grpdetails').get('custgrp_mobileno1')
                custgrpset.landline_no = jsondata.get('parms').get('grpdetails').get('custgrp_landline1')
                custgrpset.conper2 = jsondata.get('parms').get('grpdetails').get('custgrp_cpname2')
                custgrpset.desig2 = jsondata.get('parms').get('grpdetails').get('custgrp_desig2')
                custgrpset.mobile_no1 = jsondata.get('parms').get('grpdetails').get('custgrp_mobileno2')
                custgrpset.landline_no1 = jsondata.get('parms').get('grpdetails').get('custgrp_landline2')
                custgrpset.client_gid = jsondata.get('parms').get('grpdetails').get('grpclient_gid')
                custgrpset.custgrp_gid = jsondata.get('parms').get('grpdetails').get('custgrp_gid')
                custgrpset.address_gid = address_gid
                resultaddress = outputReturn(custgrpset.set_customergroup(), 0)
                if (resultaddress == 'SUCCESS'):
                    return JsonResponse(resultaddress, safe=False)
                else:
                    return JsonResponse('Customer Group Not Updated', safe=False)

            else:
                custgrpset.action = 'Insert'
                custgrpset.add_refcode = 'CUSTGROUP'
                custgrpset.address1 = jsondata.get('parms').get('grpdetails').get('Address1')
                custgrpset.address2 = jsondata.get('parms').get('grpdetails').get('Address2')
                custgrpset.address3 = jsondata.get('parms').get('grpdetails').get('Address3')
                custgrpset.pincode_no = jsondata.get('parms').get('grpdetails').get('pincode')
                custgrpset.state_gid = jsondata.get('parms').get('grpdetails').get('state')
                custgrpset.district_gid = jsondata.get('parms').get('grpdetails').get('district')
                custgrpset.city_gid = jsondata.get('parms').get('grpdetails').get('city')
                addr = custgrpset.set_address()
                add_result = outputReturn(addr, 1)
                add_gid = outputReturn(addr, 0)
            if (add_result == 'SUCCESS'):
                custgrpset.action = 'update'
                custgrpset.custgrp_name = jsondata.get('parms').get('grpdetails').get('custgrp_name')
                custgrpset.custgrp_code = jsondata.get('parms').get('grpdetails').get('custgrp_code')
                custgrpset.conper1 = jsondata.get('parms').get('grpdetails').get('custgrp_cpname1')
                custgrpset.desig1 = jsondata.get('parms').get('grpdetails').get('custgrp_desig1')
                custgrpset.mobile_no = jsondata.get('parms').get('grpdetails').get('custgrp_mobileno1')
                custgrpset.landline_no = jsondata.get('parms').get('grpdetails').get('custgrp_landline1')
                custgrpset.conper2 = jsondata.get('parms').get('grpdetails').get('custgrp_cpname2')
                custgrpset.desig2 = jsondata.get('parms').get('grpdetails').get('custgrp_desig2')
                custgrpset.mobile_no1 = jsondata.get('parms').get('grpdetails').get('custgrp_mobileno2')
                custgrpset.landline_no1 = jsondata.get('parms').get('grpdetails').get('custgrp_landline2')
                custgrpset.client_gid = jsondata.get('parms').get('grpdetails').get('grpclient_gid')
                custgrpset.custgrp_gid = jsondata.get('parms').get('grpdetails').get('custgrp_gid')
                custgrpset.address_gid = add_gid
                result = outputReturn(custgrpset.set_customergroup(), 0)
                if (result == 'SUCCESS'):
                    return JsonResponse(result, safe=False)
                else:
                    return JsonResponse('Customer Group Not Updated', safe=False)
            else:
                return JsonResponse('Address Not Updated', safe=False)


def exemapping(request):
    utl.check_pointaccess(request)
    if request.method == 'POST':
        obj_exec = mMasters.Masters()
        jsondata = json.loads(request.body.decode('utf-8'))
        obj_exec.action = jsondata.get('parms').get('Action')
        obj_exec.exemapjson = jsondata.get('parms').get('custemp')
        obj_exec.from_date = datetime.datetime.strptime(jsondata.get('parms').get('from_date'), "%d/%m/%Y").strftime(
            "%Y-%m-%d")
        obj_exec.to_date = datetime.datetime.strptime(jsondata.get('parms').get('to_date'), "%d/%m/%Y").strftime(
            "%Y-%m-%d")
        obj_exec.employee_gid = decry_data(request.session['Emp_gid'])
        obj_exec.entity_gid = decry_data(request.session['Entity_gid'])
        result = outputReturn(obj_exec.set_exemapping(), 1)
    return JsonResponse(result, safe=False);


def employeeset(request):
    utl.check_authorization(request)
    utl.check_pointaccess(request)
    if request.method == 'POST':
        addrss = 0
        employ = 0
        obj_sales = mMasters.Masters()
        jsondata = json.loads(request.body.decode('utf-8'))
        # getempdetail = jsondata.get('parms').get('empdetail')
        obj_sales.action = jsondata.get('parms').get('Action')
        obj_sales.create_by = request.session['Emp_gid']
        obj_sales.entity_gid = request.session['Entity_gid']
        if obj_sales.action != '':
            obj_sales.add_refcode = 'EMP'
            obj_sales.address1 = jsondata.get('parms').get('empdetail').get('address1')
            obj_sales.address2 = jsondata.get('parms').get('empdetail').get('address2')
            obj_sales.address3 = jsondata.get('parms').get('empdetail').get('address3')
            obj_sales.pincode_no = jsondata.get('parms').get('empdetail').get('pincode')
            obj_sales.state_gid = jsondata.get('parms').get('empdetail').get('state')
            obj_sales.district_gid = jsondata.get('parms').get('empdetail').get('district')
            obj_sales.city_gid = jsondata.get('parms').get('empdetail').get('city')
            obj_sales.address_gid = jsondata.get('parms').get('empdetail').get('Address_gid')
            obj_sales.create_by = request.session['Emp_gid']
            obj_sales.empdetail = jsondata.get('parms').get('data')
            addres = outputReturn(obj_sales.set_address(), 0)
        if (addres > 0):
            obj_sales.employee_gid = 0
            obj_sales.employee_code = jsondata.get('parms').get('empdetail').get('Employeecode')
            obj_sales.employee_name = jsondata.get('parms').get('empdetail').get('Employeename')
            obj_sales.gender = jsondata.get('parms').get('empdetail').get('Employeegndr')
            obj_sales.emp_dob = jsondata.get('parms').get('empdetail').get('Employeedob')
            obj_sales.emp_doj = jsondata.get('parms').get('empdetail').get('Employeedoj')
            obj_sales.department_gid = jsondata.get('parms').get('empdetail').get('Employeedept')
            obj_sales.designation_gid = jsondata.get('parms').get('empdetail').get('Employeedesgn')
            obj_sales.emp_sup_name = jsondata.get('parms').get('empdetail').get('Employeesprvsr')
            obj_sales.emp_sup_gid = jsondata.get('parms').get('empdetail').get('Employeesprvsrgid')
            obj_sales.address_gid = addres
            obj_sales.hierarchy_gid = jsondata.get('parms').get('empdetail').get('Employeehier')
            obj_sales.branch_gid = jsondata.get('parms').get('empdetail').get('Employeebranch')
            obj_sales.jsonData = json.dumps(jsondata.get('jsondata1').get('jsondata1'))
            obj_sales.emp_mobileno = jsondata.get('parms').get('empdetail').get('Employeemob')
            obj_sales.email = jsondata.get('parms').get('empdetail').get('Employeemail')
            employ = outputReturn(obj_sales.set_employee(), 0)
        if (employ > 0):
            obj_sales.contact_gid = addrss
            obj_sales.cont_refcode = 'EMP'
            obj_sales.cont_refgid = employ
            obj_sales.contacttype_gid = jsondata.get('parms').get('empdetail').get('ContactType')
            obj_sales.conper1 = jsondata.get('parms').get('empdetail').get('Personname')
            obj_sales.designation_gid = jsondata.get('parms').get('empdetail').get('Designation')
            obj_sales.landline_no = jsondata.get('parms').get('empdetail').get('Landline1')
            obj_sales.landline_no1 = jsondata.get('parms').get('empdetail').get('Landline2')
            obj_sales.mobile_no = jsondata.get('parms').get('empdetail').get('Mobilenum')
            obj_sales.mobile_no1 = jsondata.get('parms').get('empdetail').get('Mobilenum2')
            obj_sales.email = jsondata.get('parms').get('empdetail').get('Emailid')
            obj_sales.cont_dob = jsondata.get('parms').get('empdetail').get('BirthDate')
            obj_sales.wedding_day = jsondata.get('parms').get('empdetail').get('Wedingday')
            out_message = outputReturn(obj_sales.set_contact(), 0)
            return JsonResponse(out_message, safe=False)


def empactinact(request):
    utl.check_authorization(request)
    utl.check_pointaccess(request)
    if request.method == 'POST':
        empact = mMasters.Masters()
        jsondata = json.loads(request.body.decode('utf-8'))
        empact.employee_gid = jsondata.get('params').get('Emp_gid')
        empact.entity_gid = decry_data(request.session['Entity_gid'])
        empact.action = jsondata.get('params').get('Action')
        actinact_res = outputReturn(empact.set_employee(), 0)
        return JsonResponse(actinact_res, safe=False)


def employeeupset(request):
    utl.check_authorization(request)
    utl.check_pointaccess(request)
    if request.method == 'POST':
        addrss = 0
        employ = 0
        obj_sales = mMasters.Masters()
        jsondata = json.loads(request.body.decode('utf-8'))
        obj_sales.action = jsondata.get('parms').get('Action')
        obj_sales.create_by = request.session['Emp_gid']
        obj_sales.entity_gid = request.session['Entity_gid']
        if obj_sales.action != '':
            obj_sales.add_refcode = 'EMP'
            obj_sales.address1 = jsondata.get('parms').get('empdetail').get('address1')
            obj_sales.address2 = jsondata.get('parms').get('empdetail').get('address2')
            obj_sales.address3 = jsondata.get('parms').get('empdetail').get('address3')
            obj_sales.pincode_no = jsondata.get('parms').get('empdetail').get('pincode')
            obj_sales.state_gid = jsondata.get('parms').get('empdetail').get('state')
            obj_sales.district_gid = jsondata.get('parms').get('empdetail').get('district')
            obj_sales.city_gid = jsondata.get('parms').get('empdetail').get('city')
            obj_sales.address_gid = jsondata.get('parms').get('empdetail').get('Address_gid')
            obj_sales.create_by = request.session['Emp_gid']
            obj_sales.empdetail = jsondata.get('parms').get('data')
            addres = outputReturn(obj_sales.set_address(), 0)
        if (addres != 0):
            obj_sales.employee_gid = jsondata.get('parms').get('empdetail').get('empl_gid')
            obj_sales.employee_code = jsondata.get('parms').get('empdetail').get('Employeecode')
            obj_sales.employee_name = jsondata.get('parms').get('empdetail').get('Employeename')
            obj_sales.gender = jsondata.get('parms').get('empdetail').get('Employeegndr')
            obj_sales.emp_dob = jsondata.get('parms').get('empdetail').get('Employeedob')
            obj_sales.emp_doj = jsondata.get('parms').get('empdetail').get('Employeedoj')
            obj_sales.department_gid = jsondata.get('parms').get('empdetail').get('Employeedept')
            obj_sales.designation_gid = jsondata.get('parms').get('empdetail').get('Employeedesgn')
            obj_sales.emp_sup_name = jsondata.get('parms').get('empdetail').get('Employeesprvsr')
            obj_sales.emp_sup_gid = jsondata.get('parms').get('empdetail').get('Employeesprvsrgid')
            obj_sales.address_gid = jsondata.get('parms').get('empdetail').get('Address_gid')
            obj_sales.hierarchy_gid = jsondata.get('parms').get('empdetail').get('Employeehier')

            obj_sales.jsonData = json.dumps(jsondata.get('jsondata1').get('jsondata1'))
            obj_sales.emp_mobileno = jsondata.get('parms').get('empdetail').get('Employeemob')
            obj_sales.email = jsondata.get('parms').get('empdetail').get('Employeemail')
            employ = outputReturn(obj_sales.set_employee(), 0)
        if (employ != 0):
            obj_sales.contact_gid = jsondata.get('parms').get('empdetail').get('contact_gid')
            obj_sales.cont_refcode = 'EMP'
            obj_sales.cont_refgid = 1
            obj_sales.contacttype_gid = jsondata.get('parms').get('empdetail').get('ContactType')
            obj_sales.conper1 = jsondata.get('parms').get('empdetail').get('Personname')
            obj_sales.designation_gid = jsondata.get('parms').get('empdetail').get('Designation')
            obj_sales.landline_no = jsondata.get('parms').get('empdetail').get('Landline1')
            obj_sales.landline_no1 = jsondata.get('parms').get('empdetail').get('Landline2')
            obj_sales.mobile_no = jsondata.get('parms').get('empdetail').get('Mobilenum')
            obj_sales.mobile_no1 = jsondata.get('parms').get('empdetail').get('Mobilenum2')
            obj_sales.email = jsondata.get('parms').get('empdetail').get('Emailid')
            obj_sales.cont_dob = jsondata.get('parms').get('empdetail').get('BirthDate')
            obj_sales.wedding_day = jsondata.get('parms').get('empdetail').get('Wedingday')
            out_message = outputReturn(obj_sales.set_contact(), 0)
            return JsonResponse(out_message, safe=False)


def employedit_get(request):
    utl.check_authorization(request)
    utl.check_pointaccess(request)
    if request.method == 'GET':
        custedt = mMasters.Masters()
        custedt.employee_gid = request.GET['empl_gid']
        custedt.cluster = request.GET['cluster']
        entity = decry_data(request.session['Entity_gid'])
        custedt.jsonData = json.dumps({"entity_gid": [entity], "client_gid": []})
        customer = custedt.get_employee()
        jdata = customer.to_json(orient='records')
        return JsonResponse(jdata, safe=False)

def get_emailverify(request):
    if request.method == 'POST':
        jsondata = json.loads(request.body.decode('utf-8'))
        objemail = mMasters.Masters()
        objemail.type = jsondata.get('Type')
        objemail.sub_type = jsondata.get('SubType')
        objemail.jsonData = json.dumps(jsondata.get('data'))
        objemail.json_classification = json.dumps({'Entity_Gid': [1]})
        emaildata = objemail.get_emailverify()
        jdata = emaildata.to_json(orient='records')
        return JsonResponse(json.loads(jdata), safe=False)


def hierarchy(request):
    utl.check_authorization(request)
    utl.check_pointaccess(request)
    if request.method == 'GET':
        types = mMasters.Masters()
        types.action = 'E'
        types.entity_gid = decry_data(request.session['Entity_gid'])
        dict_add = types.getHierarchy()
        jdata = dict_add.to_json(orient='records')
        return JsonResponse(jdata, safe=False)


def branchview(request):
    utl.check_pointaccess(request)
    if request.method == 'GET':
        types = mMasters.Masters()
        types.action = 'E'
        types.entity_gid = decry_data(request.session['Entity_gid'])
        dict_add = types.getBranch()
        jdata = dict_add.to_json(orient='records')
        return JsonResponse(jdata, safe=False)


def commondropdown(request):
    utl.check_pointaccess(request)
    if request.method == 'GET':
        obj_dropdown = mMasters.Masters()
        obj_dropdown.table_name = request.GET['table_name']
        obj_dropdown.gid = request.GET['search_gid']
        obj_dropdown.name = request.GET['search_name']
        obj_dropdown.entity_gid = decry_data(request.session['Entity_gid'])
        df_dropdown = obj_dropdown.get_ddl()
        jdata = df_dropdown.to_json(orient='records')
        return JsonResponse(jdata, safe=False)


def getroute(request):
    utl.check_pointaccess(request)
    if request.method == 'GET':
        custedt = mMasters.Masters()
        custedt.action = request.GET['action']
        custedt.route_code = request.GET['slice']
        custedt.entity_gid = decry_data(request.session['Entity_gid'])
        customer = custedt.getRouteDtl()
        jdata = customer.to_json(orient='records')
        return JsonResponse(jdata, safe=False)


def texteditor(request):
    utl.check_authorization(request)
    return render(request, "Admin/bigflow_mst_Texteditor.html")


def userreport(request):
    utl.check_authorization(request)
    return render(request, "Common/userreport.html")





def mailtemplate(request):
    utl.check_authorization(request)
    return render(request, "Admin/bigflow_mst_mail-template.html")


def mailtemplatesummary(request):
    utl.check_authorization(request)
    return render(request, "Admin/bigflow_mst_mail-template-smmry.html")


def sendmailTemplate(request):
    utl.check_pointaccess(request)
    if request.method == 'POST':
        jsondata = json.loads(request.body.decode('utf-8'))
        # subject = jsondata.get('params').get('sendjson').get('Subject')  # "Hey {name}".format(name="selva")
        # from_email = 'santhosh@vsolv.co.in'
        # to = jsondata.get('params').get('sendjson').get('To')
        # cc = (jsondata.get('params').get('sendjson').get('Cc'), '')
        #
        # ctx = {
        #     'Mode': 'Despatch Mail',
        #     'InvNo': jsondata.get('params').get('sendjson').get('InvNo'),
        #     'Date': jsondata.get('params').get('sendjson').get('Date')
        # }
        # subject = jsondata.get('params').get('sendjson').get('Subject')  # "Test {name}".format(name=ctx['Mode'])
        # InvNo = ctx['InvNo']
        # Date = ctx['Date']
        # date = datetime.datetime.now().strftime("%Y-%m-%d")
        # #message = f"<p>Invoice Number :<br/></p><p>{InvNo}<br/></p>  <br/><p>Date: {date}</p><br/>"
        # #out = re.sub("<.*?>", "", message)
        # #message1 = out.format(InvNo=ctx['InvNo'])
        # message = get_template('MailTemplate/Despatch.html').render(ctx)
        # msg = EmailMultiAlternatives(subject, message, to=[to], from_email=from_email, cc=cc)
        # str = message + "    " + message1
        # msg.attach_alternative(str, "text/html")
        # result = msg.send()
        # if result != 0:
        #     data = "Success"
        #     obj_mail = mMasters.Masters()
        #     obj_mail.json = {"MailTemplate_Gid": jsondata.get('params').get('sendjson').get('Template_gid'), "Mail_From": from_email, "Mail_To": to, "Mail_Cc": cc,
        #                      "Mail_Subject": subject, "Mail_Body": str, "Mail_Date": date, "Mail_Status": "Delivered"}
        #     obj_mail.Action = "Insert"
        #     obj_mail.classification = {"Entity_Gid": request.session['Entity_gid']}
        #     obj_mail.create_by = request.session['Emp_gid']
        #     out_msg = outputReturn(obj_mail.set_Mail(), 0)
        #     if out_msg != 'SUCCESS':
        #         data = 'Mail Send Not Saved'
        #         return JsonResponse(data, safe=False)
        #     else :
        #         data = 'Success'
        # else:
        #     data = "Fail"
        data = ''
        return JsonResponse(data, safe=False)


def Templatecreation(request):
    utl.check_pointaccess(request)
    if request.method == 'POST':
        jsondata = json.loads(request.body.decode('utf-8'))
        Templatename = jsondata.get('params').get('templatename')
        content = jsondata.get('params').get('tag')
        f = open('Bigflow/Master/templates/MailTemplate/%s.html' % Templatename, 'w')
        f.write(content)
        f.close()
        return JsonResponse("success", safe=False)


def EditTemplate(request):
    utl.check_pointaccess(request)
    if request.method == 'POST':
        jsondata = json.loads(request.body.decode('utf-8'))
        Temp_name = jsondata.get('params').get('mail_templatename')
        fh = open(BASE_DIR + '/Bigflow/Master/templates/MailTemplate/%s.html' % Temp_name)
        html = fh.read()
        return JsonResponse(html, safe=False)


def getquerydata(request):
    utl.check_pointaccess(request)
    if request.method == 'POST':
        jsondata = json.loads(request.body.decode('utf-8'))
        query = mMasters.Masters()
        query.mail_headergid = jsondata.get('params').get('mail_headergid')
        query.mail_headername = jsondata.get('params').get('mail_headername')
        query.mail_detailgid = jsondata.get('params').get('mail_detailgid')
        out = query.mailquery_get()
        if query.mail_headergid == 0:
            query_groupby = (out[['mailqueryheader_gid', 'mailqueryheader_name']]).groupby(
                ['mailqueryheader_gid', 'mailqueryheader_name']).size().reset_index();
        else:
            query_groupby = out
        jdata = query_groupby.to_json(orient='records')
        return JsonResponse(jdata, safe=False)


def MailTemplate_set(request):
    utl.check_pointaccess(request)
    if request.method == 'POST':
        Template = mMasters.Masters()
        jsondata = json.loads(request.body.decode('utf-8'))
        Template.action = jsondata.get('params').get('action')
        Template.type = jsondata.get('params').get('type')
        Template.Template_json = jsondata.get('params').get('Template_json')
        Htmlconversion_data = Template.Template_json.get('TEMPLATEDETAIL')
        Templatename = Htmlconversion_data[0]['template_name']
        content = jsondata.get('params').get('Temphtml')
        Template.entity_gid = decry_data(request.session['Entity_gid'])
        Template.employee_gid = decry_data(request.session['Emp_gid'])
        out = outputReturn(Template.set_MailTemplte(), 1)
        if out == 'SUCCESS':
            f = open('Bigflow/Master/templates/MailTemplate/%s.html' % Templatename, 'w')
            f.write(content)
            f.close()
        return JsonResponse(out, safe=False)


def getTemplatedata(request):
    utl.check_pointaccess(request)
    if request.method == 'POST':
        jsondata = json.loads(request.body.decode('utf-8'))
        Temp = mMasters.Masters()
        Temp.mail_templategid = jsondata.get('params').get('mail_templategid')
        Temp.mail_templatename = jsondata.get('params').get('mail_templatename')
        Temp.mail_templatecode = jsondata.get('params').get('mail_templatecode')
        out = Temp.mailtemplate_get()
        jdata = out.to_json(orient='records')
        return JsonResponse(jdata, safe=False)


def getuniquecode(request):
    utl.check_pointaccess(request)
    if request.method == 'GET':
        uniq = mMasters.Masters()
        uniq.action = request.GET['action']
        uniq.type = request.GET['type']
        uniq.json_unique = request.GET['jsondata']
        uniq.entity_gid = decry_data(request.session['Entity_gid'])
        uniqu_code = uniq.get_unique()
        jdata = uniqu_code.to_json(orient='records')
        return JsonResponse(jdata, safe=False)


def gettaxdetails(request):
    utl.check_pointaccess(request)
    if request.method == 'GET':
        taxdtl = mMasters.Masters()
        taxdtl.type = request.GET['type']
        taxdtl.group = request.GET['group']
        taxdtl.json_unique = request.GET['jsondata']
        taxdtl.entity_gid = decry_data(request.session['Entity_gid'])
        df_taxdetl = taxdtl.get_taxdetails()
        jdata = df_taxdetl.to_json(orient='records')
        return JsonResponse(jdata, safe=False)


def commentset(request):
    utl.check_pointaccess(request)
    if request.method == 'POST':
        cmt_dtl = mMasters.Masters()
        jsondata = json.loads(request.body.decode('utf-8'))
        cmt_dtl.action = jsondata.get('params').get('action')
        cmt_dtl.type = jsondata.get('params').get('type')
        cmt_dtl.jsonData = jsondata.get('params').get('json')
        cmt_dtl.jsonData['Employee_Gid'] = decry_data(request.session['Entity_gid'])
        cmt_dtl.entity_gid = decry_data(request.session['Emp_gid'])
        cmt_dtl.create_by = decry_data(request.session['Emp_gid'])
        out_message = outputReturn(cmt_dtl.set_cmddetails(), 0)
        return JsonResponse(out_message, safe=False)


def commentget(request):
    utl.check_pointaccess(request)
    if request.method == 'POST':
        cmt_dtl = mMasters.Masters()
        jsondata = json.loads(request.body.decode('utf-8'))
        cmt_dtl.action = jsondata.get('params').get('action')
        cmt_dtl.type = jsondata.get('params').get('type')
        cmt_dtl.jsonData = jsondata.get('params').get('json')
        cmt_dtl.entity_gid = decry_data(request.session['Entity_gid'])
        cmt_dtl.create_by = decry_data(request.session['Emp_gid'])
        cmt_data = cmt_dtl.get_cmddetails()
        jdata = cmt_data.to_json(orient='records')
        return JsonResponse(json.loads(jdata), safe=False)


def employee_executive(request):
    utl.check_pointaccess(request)
    if request.method == 'GET':
        obj_dropdown = mMasters.Masters()
        obj_dropdown.action = 'DEBIT'
        json_data = '{"Table_name":"gal_mst_temployee","Column_1":"employee_gid,employee_name,employee_dept_gid","Column_2":"","Where_Common":"employee","Where_Primary":"dept_gid","Primary_Value":"2","Order_by":"name"}'
        obj_dropdown.jsonData = json_data
        obj_dropdown.entity_gid = decry_data(request.session['Entity_gid'])
        df_dropexec = obj_dropdown.get_alltablevalue()
        jdata = df_dropexec.to_json(orient='records')
        return JsonResponse(jdata, safe=False)


def employee_allexecutive(request):
    utl.check_pointaccess(request)
    if request.method == 'GET':
        obj_dropdown = mMasters.Masters()
        obj_dropdown.action = 'DEBIT'
        json_data = '{"Table_name":"gal_mst_temployee","Column_1":"employee_gid,employee_name,employee_dept_gid","Column_2":"","Where_Common":"employee","Where_Primary":"dept_gid","Primary_Value":"","Order_by":"name"}'
        obj_dropdown.jsonData = json_data
        obj_dropdown.entity_gid = decry_data(request.session['Entity_gid'])
        df_dropexec = obj_dropdown.get_alltablevalue()
        jdata = df_dropexec.to_json(orient='records')
        return JsonResponse(jdata, safe=False)


def city_get(request):
    utl.check_pointaccess(request)
    if request.method == 'GET':
        obj_city = mMasters.Masters()
        df_city = obj_city.get_city()
        jdata = df_city.to_json(orient='records')
        return JsonResponse(jdata, safe=False)


def city_set(request):
    utl.check_pointaccess(request)
    if request.method == 'POST':
        cityset = mMasters.Masters()
        jsondata = json.loads(request.body.decode('utf-8'))
        cityset.action = jsondata.get('parms').get('action')
        cityset.jsonData = jsondata.get('parms').get('cityjson')
        cityset.entity_gid = decry_data(request.session['Entity_gid'])
        cityset.create_by = decry_data(request.session['Emp_gid'])
        df_cityset = outputReturn(cityset.set_city(), 0)
        return JsonResponse(df_cityset, safe=False)


def suppplierproductmap_set(request):
    utl.check_authorization(request)
    utl.check_pointaccess(request)
    if request.method == 'POST':
        supplierproductset = mMasters.Masters()
        jsondata = json.loads(request.body.decode('utf-8'))
        supplierproductset.action = jsondata.get('parms').get('action')
        supplierproductset.jsonData = jsondata.get('parms').get('supplierratejson')
        supplierproductset.entity_gid = decry_data(request.session['Entity_gid'])
        supplierproductset.create_by = decry_data(request.session['Emp_gid'])
        df_supplierproductset = outputReturn(supplierproductset.set_supplierproductmap(), 0)
        return JsonResponse(df_supplierproductset, safe=False)


def suppplierproductmap_get(request):
    utl.check_authorization(request)
    utl.check_pointaccess(request)
    if request.method == 'POST':
        productname = mMasters.Masters()
        jsondata = json.loads(request.body.decode('utf-8'))
        productname.action = 'Full_wise'
        productname.supplier_gid = jsondata.get('params').get('supplier_gid')
        productname.product_gid = jsondata.get('params').get('product_gid')
        productname.char_active = jsondata.get('params').get('char_active')
        data = productname.get_productnames()
        jdata = data.to_json(orient='records')
        return JsonResponse(jdata, safe=False)


# Client

def client(request):
    utl.check_authorization(request)
    utl.check_pointaccess(request)
    return render(request, "Client/bigflow_mst_client.html")


def clientcreate(request):
    utl.check_authorization(request)
    return render(request, "Client/bigflow_mst_clientcreate.html")


# client
def client_get(request):
    utl.check_pointaccess(request)
    if request.method == 'GET':
        obj_master = mMasters.Masters()
        client_gid = request.GET['client_gid']
        if (client_gid != ''):
            obj_master.client_gid = request.GET['client_gid']
            obj_master.entity_gid = decry_data(request.session['Entity_gid'])
            customer = obj_master.get_client()
            jdata = customer.to_json(orient='records')
            return JsonResponse(jdata, safe=False)
        else:
            obj_master.entity_gid = decry_data(request.session['Entity_gid'])
            customer = obj_master.get_client()
            jdata = customer.to_json(orient='records')
            return JsonResponse(jdata, safe=False)


def client_set(request):
    utl.check_pointaccess(request)
    if request.method == 'POST':
        clientset = mMasters.Masters()
        jsondata = json.loads(request.body.decode('utf-8'))
        clientset.action = jsondata.get('parms').get('action')
        clientset.jsonData = jsondata.get('parms').get('clientjson')
        clientset.entity_gid = request.session['Entity_gid']
        clientset.create_by = request.session['Emp_gid']
        df_cityset = outputReturn(clientset.set_client(), 0)
        return JsonResponse(df_cityset, safe=False)


def SetCityPincode(request):
    utl.check_authorization(request)
    if request.method == 'POST':
        jsondata = json.loads(request.body.decode('utf-8'))
        if (jsondata.get('Action') == 'Insert' and (jsondata.get('Type') == 'State_Insert')):
            Action = jsondata.get('Action')
            Type = jsondata.get('Type')
            datas = json.dumps(jsondata.get('data').get('params'))
            Emp_gid = request.session['Emp_gid']
            param = {'Action': Action, 'Type': Type, 'Emp_gid': Emp_gid}
            token = jwt.token(request)
            headers = {"content-type": "application/json", "Authorization": "" + token + ""}
            result = requests.post("" + ip + "/Master_State_Details", params=param, headers=headers, data=datas,
                                   verify=False)
            result = result.content.decode("utf-8")
            return JsonResponse(json.loads(result), safe=False)
        elif (jsondata.get('Action') == 'Insert' and (jsondata.get('Type') == 'District_Insert')):
            Action = jsondata.get('Action')
            Type = jsondata.get('Type')
            datas = json.dumps(jsondata.get('data').get('params'))
            Emp_gid = request.session['Emp_gid']
            param = {'Action': Action, 'Type': Type, 'Emp_gid': Emp_gid}
            token = jwt.token(request)
            headers = {"content-type": "application/json", "Authorization": "" + token + ""}
            result = requests.post("" + ip + "/Master_State_Details", params=param, headers=headers, data=datas,
                                   verify=False)
            result = result.content.decode("utf-8")
            return JsonResponse(json.loads(result), safe=False)
        elif (jsondata.get('Action')) == 'insert':
            Action = jsondata.get('Action')
            datas = json.dumps(jsondata.get('data').get('params'))
            Emp_gid = request.session['Emp_gid']
            Entity_gid = request.session['Entity_gid']
            token = jwt.token(request)
            param = {'Action': Action, 'Entity_gid': Entity_gid, 'Emp_gid': Emp_gid}
            headers = {"content-type": "application/json", "Authorization": "" + token + ""}
            result = requests.post("" + ip + "/Master_State_Details", params=param, headers=headers, data=datas,
                                   verify=False)
            result = result.content.decode("utf-8")
            results = json.loads(result)
            results = results[0]
            results = results.split(",")
            results = results[1]
            return JsonResponse(results, safe=False)

def common_summary(request):
    utl.check_authorization(request)
    return render(request, 'Common/common_summary.html')


def view_summary(request):
    utl.check_authorization(request)
    utl.check_pointaccess(request)
    if request.method == 'POST':
        send_category = mMasters.Masters()
        jsondata = json.loads(request.body.decode('utf-8'))
        send_category.action = jsondata.get('Params').get('Type')
        send_category.action1 = jsondata.get('Params').get('Sub_Type')
        send_category.action2 = jsondata.get('Params').get('t_name')
        send_category.action4 = json.dumps({'t_name': send_category.action2})
        send_category.action3 = json.dumps({})
        customer = send_category.get_summary()
        jdata = customer.to_json(orient='records')
        return HttpResponse(jdata)


def insert_summary(request):
    utl.check_authorization(request)
    utl.check_pointaccess(request)
    if request.method == 'POST':
        insert_data = mMasters.Masters()
        entity_gid = decry_data(request.session['Entity_gid'])
        create_by = decry_data(request.session['Emp_gid'])
        jsondata = json.loads(request.body.decode('utf-8'))
        insert_data.action = jsondata.get('Params').get('Action')
        insert_data.action1 = jsondata.get('Params').get('t_name')
        insert_data.action2 = jsondata.get('Params').get('t_code')
        insert_data.action3 = jsondata.get('Params').get('t_tname')
        insert_data.action4 = jsondata.get('Params').get('entity_gid')
        insert_data.action5 = jsondata.get('Params').get('create_by')
        insert_data.action6 = json.dumps(
            {'t_name': insert_data.action1, 't_code': insert_data.action2, 't_tname': insert_data.action3,
             'entity_gid': entity_gid, 'create_by': create_by})
        df_cityset=insert_data.set_summary()
        print(df_cityset)
        if(df_cityset[0]=='SUCCESS'):
            if (jsondata.get('Params').get('t_name') == 'bank'):
                data = {'name': jsondata.get('Params').get('t_tname'),'Entity_Gid':jsondata.get('Params').get('entity_gid'),'create_by':jsondata.get('Params').get('create_by')}
                # print(data)
                mrobject = MasterRequestObject('BANK', data, 'POST')
            if (jsondata.get('Params').get('t_name') == 'designation'):
                data = {'name': jsondata.get('Params').get('t_tname'),'Entity_Gid':jsondata.get('Params').get('entity_gid'),'create_by':jsondata.get('Params').get('create_by')}
                # print(data)
                mrobject = MasterRequestObject('DESIGNATION', data, 'POST')
            if (jsondata.get('Params').get('t_name') == 'contacttype'):
                data = {'name': jsondata.get('Params').get('t_tname'),'Entity_Gid':jsondata.get('Params').get('entity_gid'),'create_by':jsondata.get('Params').get('create_by')}
                # print(data)
                mrobject = MasterRequestObject('CONTACT TYPE', data, 'POST')
            if (insert_data.action1 == jsondata.get('Params').get('t_name') == 'uom'):
                data = {'name': jsondata.get('Params').get('t_tname'),'Entity_Gid':jsondata.get('Params').get('entity_gid'),'create_by':jsondata.get('Params').get('create_by')}
                mrobject = MasterRequestObject('UOM', data, 'POST')
            if (insert_data.action1 == jsondata.get('Params').get('t_name') == 'paymode'):
                data = {'name': jsondata.get('Params').get('t_tname'),'Entity_Gid':jsondata.get('Params').get('entity_gid'),'create_by':jsondata.get('Params').get('create_by')}
                mrobject = MasterRequestObject('PAYMODE', data, 'POST')
        return JsonResponse(df_cityset, safe=False)


def update_summary(request):
    utl.check_authorization(request)
    utl.check_pointaccess(request)
    if request.method == 'POST':
        update = mMasters.Masters()
        entity_gid = decry_data(request.session['Entity_gid'])
        create_by = decry_data(request.session['Emp_gid'])
        jsondata = json.loads(request.body.decode('utf-8'))
        update.action = jsondata.get('Params').get('Action')
        update.category = jsondata.get('Params').get('t_name')
        update.code = jsondata.get('Params').get('t_code')
        update.name = jsondata.get('Params').get('t_tname')
        update.gid = jsondata.get('Params').get('table_gid')
        update.updateby = int(decry_data(request.session['Emp_gid']))
        update.finaldata = json.dumps({'t_name': update.category, 't_code': update.code, 't_tname': update.name,
                                       'table_gid': update.gid, 'update_by': create_by})
        df_update = outputReturn(update.upsatesummary(), 0)
        return JsonResponse(df_update, safe=False)

def insert_bank_branch(request):
    utl.check_authorization(request)
    utl.check_pointaccess(request)
    if request.method=='POST':
        try:
            jsondata=json.loads(request.body.decode('utf-8'))
            action = jsondata.get('action')
            type = jsondata.get('type')
            entity_gid = decry_data(request.session['Entity_gid'])
            create_by = decry_data(request.session['Emp_gid'])
            master_object = mMasters.Masters()
            if(action=='INSERT' and type=="bankbranch"):
                master_object.action=action
                master_object.type=type
                master_object.filter= json.dumps(jsondata.get('filter'))
                master_object.classification=json.dumps({"Entity_Gid": entity_gid, "Create_by": create_by})
                output = master_object.set_bank_branch()
                data = jsondata.get('filter')
                address = data['ADDRESS'][0]
                address1 = {"line1": address['Address1'], "line2": address['Address2'], "line3": address['Address3'],
                            "pincode_id": int(address['Pincode']), "city_id": address['City_Gid'],
                            "district_id": address['District_Gid'], "state_id": address['State_Gid']}
                api_send_data = {"bank_id": data["bankbranch_bank_gid"], "address_id": address1,
                                 "ifsccode": data["bankbranch_ifsccode"], "microcode": data["bankbranch_microcode"],
                                 "name": data["bankbranch_name"],"Entity_Gid": request.session['Entity_gid'], "create_by": request.session['Emp_gid']}
                mrobject = MasterRequestObject('BANK BRANCH', api_send_data, 'POST')
                return JsonResponse(output, safe=False)
        except Exception as e:
            return JsonResponse({"MESSAGE": "ERROR_OCCURED", "DATA": str(e)})

def insert_paymode_details(request):
    utl.check_authorization(request)
    utl.check_pointaccess(request)
    if request.method=='POST':
        try:
            jsondata=json.loads(request.body.decode('utf-8'))
            action = jsondata.get('action')
            type = jsondata.get('type')
            entity_gid = decry_data(request.session['Entity_gid'])
            create_by = decry_data(request.session['Emp_gid'])
            master_object = mMasters.Masters()
            if(action=='INSERT' and type=="paymode"):
                master_object.action=action
                master_object.type=type
                master_object.filter= json.dumps(jsondata.get('filter'))
                master_object.classification=json.dumps({"Entity_Gid": entity_gid, "Create_by": create_by})
                output = master_object.set_paymode_details()
                return JsonResponse(output, safe=False)
            elif(action=="UPDATE" and type=="active_inactive_paymode_detail"):
                master_object.action=action
                master_object.type=type
                master_object.filter= json.dumps(jsondata.get('filter'))
                master_object.classification=json.dumps({"Entity_Gid": entity_gid, "Create_by": create_by})
                output = master_object.set_paymode_details()
                return JsonResponse(output, safe=False)
        except Exception as e:
            return JsonResponse({"MESSAGE": "ERROR_OCCURED", "DATA": str(e)})

def view_summary_dynamic(request):
    utl.check_authorization(request)
    utl.check_pointaccess(request)
    if request.method == 'POST':
        try:
            send_category = mMasters.Masters()
            jsondata = json.loads(request.body.decode('utf-8'))
            send_category.action = jsondata.get('Params').get('Type')
            send_category.type = jsondata.get('Params').get('Sub_Type')
            send_category.filter = json.dumps(jsondata.get('Params'))
            send_category.json_classification = json.dumps({})
            customer = send_category.get_summary_dynamic()
            jdata = customer.to_json(orient='records')
            return HttpResponse(jdata)
        except Exception as e:
            return JsonResponse({"MESSAGE": "ERROR_OCCURED", "DATA": str(e)})


def mst_courier(request):
    utl.check_authorization(request)
    return render(request, 'Common/mst_courier.html')

def courier_data(request):
    utl.check_authorization(request)
    if request.method == 'POST':
        jsondata = json.loads(request.body.decode('utf-8'))
        if (jsondata.get('params').get('Group')) == 'SET_COURIER_DATA':
            act = jsondata.get('params').get('Action')
            grp = jsondata.get('params').get('Group')
            typ = jsondata.get('params').get('Type')
            sub = jsondata.get('params').get('Sub_Type')
            emp = request.session['Emp_gid']
            params = {"Action": act, "Group": grp, "Type": typ, "Sub_Type": sub,
                      "Employee_Gid": emp}
            token = jwt.token(request)
            headers = {"content-type": "application/json", "Authorization": "" + token + ""}
            classify = {
                "CLASSIFICATION": {
                    "Entity_Gid": request.session['Entity_gid']
                }}
            jsondata['params']['json']['Params'].update(classify)
            datas = json.dumps(jsondata.get('params').get('json'))
            resp = requests.post("" + ip + "/COURIER_MST", params=params, data=datas, headers=headers,
                                 verify=False)
            response = resp.content.decode("utf-8")
            return HttpResponse(response)
        elif (jsondata.get('params').get('Group')) == 'GET_COURIER_DATA':
            grp = jsondata.get('params').get('Group')
            typ = jsondata.get('params').get('Type')
            sub = jsondata.get('params').get('Sub_Type')
            params = {"Group": grp, "Type": typ, "Sub_Type": sub}
            token = jwt.token(request)
            headers = {"content-type": "application/json", "Authorization": "" + token + ""}
            classify = {
                "CLASSIFICATION": {
                    "Entity_Gid": request.session['Entity_gid']
                }}
            jsondata['params']['json']['Params'].update(classify)
            datas = json.dumps(jsondata.get('params').get('json'))
            resp = requests.post("" + ip + "/COURIER_MST", params=params, data=datas, headers=headers,
                                 verify=False)
            response = resp.content.decode("utf-8")
            return HttpResponse(response)

def fileUploadS3(request):
    try:
        utl.check_pointaccess(request)
        if request.method == 'POST' and request.FILES['file']:
            filename = str(request.FILES['file'])
            extension = os.path.splitext(filename)[1]
            filename=''.join(e for e in filename if e.isalnum())
            filename=filename+extension
            millis = int(round(time.time() * 1000))
            Emp_gid = decry_data(request.session['Emp_gid'])
            concat_filename = str(Emp_gid) + "_" + str(millis) + "_" + filename
            s3 = boto3.resource('s3')
            s3_obj = s3.Object(bucket_name=S3_BUCKET_NAME, key=concat_filename)
            s3_obj.put(Body=request.FILES['file'])
            #s3_client = boto3.client('s3')
            #file_path = s3_client.generate_presigned_url('get_object',Params={'Bucket': S3_BUCKET_NAME, 'Key': concat_filename},ExpiresIn=3600)
            return JsonResponse({"file_key":concat_filename,"file_path":"fiile_path","status":"SUCCESS"})
    except Exception as e:
        return JsonResponse({"status":e})







# def master_sync_(request):
#     # timer()
#
#     if request.method == 'POST':
#         try:
#             data = mMasters.Masters()
#             jsondata = json.loads(request.body.decode('utf-8'))
#             data.action = jsondata.get('Action')
#             data.type = jsondata.get('Type')
#             data.clientdata = json.dumps(jsondata.get('clientData'))
#             Emp_gid=request.session['Emp_gid']
#             message = data.mastersync_get_()
#             if message.get("MESSAGE") == 'SUCCESS':
#                 ld_dict = {"DATA": json.loads(message.get("DATA").to_json(orient='records')),
#                            "MESSAGE": 'SUCCESS'}
#                 return JsonResponse(ld_dict)
#
#             elif message.get("MESSAGE") == 'FAILED':
#                 url = common.master_accesstoken()
#                 client_id = 'WPRrSfAoa2EQa3IxSiO6zny7WZVDbrJP'
#                 client_secret = 'HgUTl2g2Cg5O6xdG'
#                 grant_type = 'client_credentials'
#                 response = requests.post(url, auth=(client_id, client_secret),
#                                          data={'grant_type': grant_type, 'client_id': client_id,
#                                                'client_secret': client_secret})
#                 datas = json.loads(response.content.decode("utf-8"))
#                 access_token = datas.get("access_token")
#                 token_expires = datas.get("expires_in")
#                 obj_ = mMasters.Masters()
#                 obj_.type = "insert_data"
#                 obj_.action = "Insert"
#                 obj_.jsonData = json.dumps({"clienttoken_name": access_token,"clienttoken_expiry": token_expires,
#                                             "clienttoken_user": "dinesh", "clienttoken_pwd": "padsswor1", "create_by":Emp_gid })
#                 message = obj_.mastersync_set()
#                 if message[0] == 'SUCCESS':
#                     ld_dict = {"DATA": [{'clienttoken_name':access_token}],
#                                "MESSAGE": 'SUCCESS'}
#                     return JsonResponse(ld_dict)
#         except Exception as e:
#              return JsonResponse({"MESSAGE": "ERROR_OCCURED"})


def master_sync_(action,type,emp_gid):
        try:
            data = mMasters.Masters()
            data.action = action
            data.type = type
            data.clientdata = json.dumps({})
            message = data.mastersync_get_()
            if message.get("MESSAGE") == 'SUCCESS':
                ld_dict = {"DATA": json.loads(message.get("DATA").to_json(orient='records')),
                           "MESSAGE": 'SUCCESS'}
                return ld_dict

            elif message.get("MESSAGE") == 'FAILED':
                url = common.master_accesstoken()
                client_id = common.ADToken()
                client_secret = common.ClientSecret()
                grant_type = 'client_credentials'
                response = requests.post(url, auth=(client_id, client_secret),
                                         data={'grant_type': grant_type, 'client_id': client_id,
                                               'client_secret': client_secret})
                datas = json.loads(response.content.decode("utf-8"))
                access_token = datas.get("access_token")
                token_expires = datas.get("expires_in")
                obj_ = mMasters.Masters()
                obj_.type = "insert_data"
                obj_.action = "Insert"
                obj_.jsonData = json.dumps({"clienttoken_name": access_token,"clienttoken_expiry": token_expires,
                                            "clienttoken_user": "vsolv", "clienttoken_pwd": "12345", "create_by":emp_gid })
                message = obj_.mastersync_set()
                if message[0] == 'SUCCESS':
                    ld_dict = {"DATA": [{'clienttoken_name':access_token}],
                               "MESSAGE": 'SUCCESS'}
                    return ld_dict
        except Exception as e:
             return ({"MESSAGE": "ERROR_OCCURED"})



def common_s3_file_url_generate(request):
    utl.check_pointaccess(request)
    if request.method == 'POST':
        jsondata = json.loads(request.body.decode('utf-8'))
        file_details=jsondata.get("file_data")
        final_url_data=[]
        for i in file_details:
            filename= i.get('file_name')
            s3_client = boto3.client('s3','ap-south-1')
            file_path = s3_client.generate_presigned_url('get_object',
                                                         Params={'Bucket': S3_BUCKET_NAME,
                                                                 'Key': filename},ExpiresIn=900)
            final_url_data.append({"file_name":filename,"file_path":file_path})
        return JsonResponse(final_url_data, safe=False)

def common_s3_file_download(request):
    utl.check_pointaccess(request)
    if request.method == 'GET':
        filename = request.GET['filename']
        s3 = boto3.resource('s3')
        s3_obj=s3.Object(bucket_name=S3_BUCKET_NAME,key=filename)
        body=s3_obj.get()['Body']
        response = StreamingHttpResponse(body, content_type='application/octet-stream')
        response['Content-Disposition'] = 'inline; filename="{}"'.format(filename)
        return response

def prod_specification(request):
    if request.method == 'POST':
        jsondata = json.loads(request.body.decode('utf-8'))
        if jsondata.get('Action') == 'INSERT':
            Action = jsondata.get('Action')
            datas = json.dumps(jsondata.get('data').get('params'))
            param = {'Action': Action}
            token = jwt.token(request)
            headers = {"content-type": "application/json", "Authorization": "" + token + ""}
            result = requests.post("" + ip + "/Product_spec", params=param, headers=headers, data=datas,
                                   verify=False)
            result = result.content.decode("utf-8")
            return JsonResponse(json.loads(result), safe=False)
        elif jsondata.get('Action') == 'productspecification_Get':
            Action = jsondata.get('Action')
            datas = json.dumps(jsondata.get('data').get('params'))
            param = {'Action': Action}
            token = jwt.token(request)
            headers = {"content-type": "application/json", "Authorization": "" + token + ""}
            result = requests.post("" + ip + "/Product_spec", params=param, headers=headers, data=datas,
                                   verify=False)
            result = result.content.decode("utf-8")
            return JsonResponse(json.loads(result), safe=False)

def customer_query_screen(request):
    # utl.check_authorization(request)
    if request.method == 'POST':
        try:
            objdata = mMasters.Masters()
            jsondata = json.loads(request.body.decode('utf-8'))
            objdata.type = jsondata.get('Type')
            objdata.sub_type = jsondata.get('Subtype')
            objdata.filterdata = json.dumps(jsondata.get('Params').get('FILTER'))
            objdata.classification = json.dumps(jsondata.get('Params').get('classification'))
            obj_cancel_data = objdata.CustomerSummary()

            jdata = obj_cancel_data.to_json(orient='records')
            return JsonResponse(jdata, safe=False)
        except Exception as e:
            return JsonResponse({"MESSAGE": "ERROR_OCCURED", "DATA": str(e)})
    else:
        return render(request, "Common/customer_query_screen.html")

def customer_query_screen_update(request):
    # utl.check_authorization(request)
    if request.method == 'POST':
        try:
            objdata = mMasters.Masters()
            jsondata = json.loads(request.body.decode('utf-8'))
            objdata.type = jsondata.get('Type')
            objdata.sub_type = jsondata.get('Subtype')
            objdata.filterdata = json.dumps(jsondata.get('Params').get('FILTER'))
            objdata.classification = json.dumps(jsondata.get('Params').get('classification'))
            objdata.jsondata = 1
            obj_cancel_data = objdata.Customerupdate()
            jdata = obj_cancel_data.to_json(orient='records')
            return JsonResponse(jdata, safe=False)
        except Exception as e:
            return JsonResponse({"MESSAGE": "ERROR_OCCURED", "DATA": str(e)})


def customer_query_screen_id(request):
    # utl.check_authorization(request)
    if request.method == 'POST':
        try:
            objdata = mMasters.Masters()
            jsondata = json.loads(request.body.decode('utf-8'))
            objdata.type = jsondata.get('Type')
            objdata.sub_type = jsondata.get('Subtype')
            objdata.filterdata = json.dumps(jsondata.get('Params').get('FILTER'))
            objdata.classification = json.dumps(jsondata.get('Params').get('classification'))
            obj_cancel_data = objdata.Customerid()

            jdata = obj_cancel_data.to_json(orient='records')
            return JsonResponse(jdata, safe=False)
        except Exception as e:
            return JsonResponse({"MESSAGE": "ERROR_OCCURED", "DATA": str(e)})


def customer_query_screen_dependent(request):
    utl.check_authorization(request)
    if request.method == 'POST':
        try:
            objdata = mMasters.Masters()
            jsondata = json.loads(request.body.decode('utf-8'))
            objdata.type = jsondata.get('Type')
            objdata.sub_type = jsondata.get('Subtype')
            objdata.filterdata = json.dumps(jsondata.get('Params').get('FILTER'))
            objdata.classification = json.dumps(jsondata.get('Params').get('classification'))
            obj_cancel_data = objdata.Customerdependent()
            jdata = obj_cancel_data.to_json(orient='records')
            return JsonResponse(jdata, safe=False)
        except Exception as e:
            return JsonResponse({"MESSAGE": "ERROR_OCCURED", "DATA": str(e)})



