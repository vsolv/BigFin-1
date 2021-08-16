from django.shortcuts import render
from Bigflow.Service.Model import mService
from Bigflow.Master.Model import mMasters
from django.http import JsonResponse
import os
import json
#import simplejson as json
#import requests
import datetime
import pandas as pd
#from PIL import Image
from Bigflow.menuClass import utility as utl
from Bigflow.Core.models import decrpt as decry_data


def Requestexe(request):
    utl.check_authorization(request)
    return render(request, "service_requestExceutive.html")


def branchofficerec_index(request):
    utl.check_authorization(request)
    return render(request, "service_branchreceived.html")


def Producttype(request):
    utl.check_authorization(request)
    utl.check_pointaccess(request)
    if request.method == 'POST':
        producttype= mService.Service_model()
        jsondata = json.loads(request.body.decode('utf-8'))
        producttype.producttype_gid = jsondata.get('params').get('producttype_gid')
        data = producttype.get_producttype()
        jdata = data.to_json(orient='records')
        return JsonResponse(jdata, safe=False)

def Productname(request):
    utl.check_authorization(request)
    utl.check_pointaccess(request)
    if request.method =='POST':
        productname = mService.Service_model()
        jsondata = json.loads(request.body.decode('utf-8'))
        productname.producttype_gid = jsondata.get('params').get('producttype_gid')
        productname.supplier_gid = jsondata.get('params').get('supplier_gid')
        data = productname.get_productname()
        jdata = data.to_json(orient='records')
        return JsonResponse(jdata, safe=False)

def customer_detail(request):
    utl.check_authorization(request)
    utl.check_pointaccess(request)
    if request.method == 'POST':
        obj_customer_ddl =  mService.Service_model()
        jsondata = json.loads(request.body.decode('utf-8'))
        obj_customer_ddl.customer_gid =jsondata.get('params').get('customer_gid')
        obj_customer_ddl.customer_code = jsondata.get('params').get('customer_code')
        obj_customer_ddl.customer_name = jsondata.get('params').get('customer_name')
        obj_customer_ddl.entity_gid = request.session['Entity_gid']
        df_customer_ddl = obj_customer_ddl.get_customer()
        jdata = df_customer_ddl.to_json(orient='records')
        return JsonResponse(json.loads(jdata), safe=False)

def get_mappedcustomer(request):
    utl.check_authorization(request)
    utl.check_pointaccess(request)
    if request.method == 'POST':
        objexe = mMasters.Masters()
        jsondata = json.loads(request.body.decode('utf-8'))
        data=jsondata.get('params').get('Emp_gid');
        if jsondata.get('params').get('Emp_gid') == None:
            objexe.employee_gid = request.session['Emp_gid']
        else:
            objexe.employee_gid = 0
        objexe.action = ''
        objexe.entity_gid = request.session['Entity_gid']
        df_executive = objexe.getexecmapping()
        jdata = df_executive.to_json(orient='records')
        return JsonResponse(json.loads(jdata), safe=False)

def outputSplit(tubledtl,index):
    temp=tubledtl[0].split(',')
    if(len(temp)>1):
        if (index==0):
            return int(temp[0])
        else:
            return temp[1]
    else:
        return  temp[0]

def Service_set(request):
    utl.check_authorization(request)
    utl.check_pointaccess(request)
    if request.method == 'POST':
        service_dtl =  mService.Service_model()
        jsondata = json.loads(request.body.decode('utf-8'))
        service_dtl.action =jsondata.get('params').get('action')
        service_dtl.date = jsondata.get('params').get('date')
        service_dtl.customer_gid = jsondata.get('params').get('customer_gid')
        service_dtl.status = jsondata.get('params').get('status')
        service_dtl.SERVICE_JSON = jsondata.get('params').get('SERVICE_JSON')
        service_dtl.entity_gid = jsondata.get('params').get('entity_gid')
        service_dtl.employee_gid = jsondata.get('params').get('employee_gid')
        Service_out = outputSplit(service_dtl.set_servicedtl(), 1)
        return JsonResponse(Service_out, safe=False)

def Service_summary(request):
    utl.check_authorization(request)
    return render(request, "service_summary.html")

def ServiceDtl_get(request):
    utl.check_authorization(request)
    utl.check_pointaccess(request)
    if request.method == 'POST':
        service_get = mService.Service_model()
        jsondata = json.loads(request.body.decode('utf-8'))
        service_get.from_date = jsondata.get('params').get('from_date')
        service_get.to_date = jsondata.get('params').get('to_date')
        service_get.customer_gid = jsondata.get('params').get('customer_gid')
        service_get.product_gid = jsondata.get('params').get('product_gid')
        service_get.service_gid = jsondata.get('params').get('service_gid')
        service_get.status = jsondata.get('params').get('status')
        if 'only_employee' in jsondata.get('params'):
             service_get.employee_gid =  request.session['Emp_gid']
        else:
            service_get.employee_gid = 0
        service_get.entity_gid = request.session['Entity_gid']
        output = service_get.get_Servicedtl()
        jdata = output.to_json(orient='records')
        return JsonResponse(json.loads(jdata), safe=False)

def ServiceReceived(request):
    utl.check_authorization(request)
    return  render(request,"service_reqreceived.html")

def ServiceDispatch(request):
    utl.check_authorization(request)
    return render(request, "service_dispatch.html")

def Dispatch_Set(request):
    utl.check_authorization(request)
    utl.check_pointaccess(request)
    if request.method == 'POST':
        dispatch_dtl = mService.Service_model()
        jsondata = json.loads(request.body.decode('utf-8'))
        lst = jsondata.get('dispatch_data')
        if lst[0].get('type') == 'SALES_INVOICE':
            for x in lst:
                dispatch_dtl.action = x.get('action')
                dispatch_dtl.type = x.get('type')
                dispatch_dtl.in_out =  x.get('in_out')
                dispatch_dtl.courier_gid = x.get('courier_gid')
                dispatch_dtl.Dispatch_date = x.get('Dispatch_date')
                dispatch_dtl.send_by = x.get('send_by')
                dispatch_dtl.awbno = x.get('awbno')
                dispatch_dtl.dispatch_mode = x.get('dispatch_mode')
                dispatch_dtl.dispatch_type = x.get('dispatch_type')
                dispatch_dtl.packets = x.get('packets')
                dispatch_dtl.weight = x.get('weight')
                dispatch_dtl.dispatch_to = x.get('dispatch_to')
                dispatch_dtl.address = x.get('address')
                dispatch_dtl.city = x.get('city')
                dispatch_dtl.state = x.get('state')
                dispatch_dtl.pincode = x.get('pincode')
                dispatch_dtl.remark = x.get('remark')
                dispatch_dtl.returned = x.get('returned')
                dispatch_dtl.returned_on = x.get('returned_on')
                dispatch_dtl.returned_remark = x.get('returned_remark')
                dispatch_dtl.pod = x.get('pod')
                dispatch_dtl.pod_image = x.get('pod_image')
                dispatch_dtl.isactive = x.get('isactive')
                dispatch_dtl.isremoved = x.get('isremoved')
                dispatch_dtl.dispatch_gid = x.get('dispatch_gid')
                dispatch_dtl.status = x.get('status')
                dispatch_dtl.entity_gid = request.session['Entity_gid']
                dispatch_dtl.SERVICE_JSON = jsondata.get('service_dtl')
                dispatch_dtl.employee_gid = request.session['Emp_gid']
                Service_out = outputSplit(dispatch_dtl.set_Dispatch(), 0)
                return JsonResponse(Service_out, safe=False)
        elif lst[0].get('type') == 'SALES_BULK_COURIER':
            for y in lst:
                dispatch_dtl.action = y.get('action')
                dispatch_dtl.type = y.get('type')
                dispatch_dtl.in_out = ''
                dispatch_dtl.courier_gid = y.get('courier_gid')
                dispatch_dtl.Dispatch_date = ''
                dispatch_dtl.send_by =y.get('Sent_By')
                dispatch_dtl.awbno =0
                dispatch_dtl.dispatch_mode = ''
                dispatch_dtl.dispatch_type = ''
                dispatch_dtl.packets = 0
                dispatch_dtl.weight = 0
                dispatch_dtl.dispatch_to = ''
                dispatch_dtl.address = ''
                dispatch_dtl.city = ''
                dispatch_dtl.state = ''
                dispatch_dtl.pincode =0
                dispatch_dtl.remark = ''
                dispatch_dtl.returned = ''
                dispatch_dtl.returned_on = ''
                dispatch_dtl.returned_remark = ''
                dispatch_dtl.pod = 0
                dispatch_dtl.pod_image = ''
                dispatch_dtl.isactive = y.get('isactive')
                dispatch_dtl.isremoved = y.get('isremoved')
                dispatch_dtl.dispatch_gid =0
                dispatch_dtl.status = y.get('status')
                dispatch_dtl.entity_gid = y.get('entity_gid')
                dispatch_dtl.SERVICE_JSON = jsondata.get('service_dtl')
                dispatch_dtl.employee_gid = request.session['Emp_gid']
                Service_out = outputSplit(dispatch_dtl.set_Dispatch(), 0)
                return JsonResponse(Service_out, safe=False)
        elif lst[0].get('type') == 'DISPATCH_POD_UPDATE':
            for z in lst:
                dispatch_dtl.action = z.get('action')
                dispatch_dtl.type = z.get('type')
                dispatch_dtl.courier_gid = 0
                dispatch_dtl.Dispatch_date = ''
                dispatch_dtl.send_by = 0
                dispatch_dtl.awbno = 0
                dispatch_dtl.dispatch_mode =z.get('dispatch_mode')
                dispatch_dtl.dispatch_type = ''
                dispatch_dtl.packets = 0
                dispatch_dtl.weight = 0
                dispatch_dtl.dispatch_to = ''
                dispatch_dtl.address = ''
                dispatch_dtl.city = ''
                dispatch_dtl.state = ''
                dispatch_dtl.pincode = 0
                dispatch_dtl.remark = ''
                dispatch_dtl.returned = ''
                dispatch_dtl.returned_on = ''
                dispatch_dtl.returned_remark = ''
                dispatch_dtl.pod = z.get('pod')
                dispatch_dtl.pod_image = ''
                dispatch_dtl.isactive = ''
                dispatch_dtl.isremoved = ''
                dispatch_dtl.dispatch_gid =z.get('dispatch_gid')
                dispatch_dtl.status = z.get('status')
                dispatch_dtl.entity_gid = z.get('entity_gid')
                dispatch_dtl.employee_gid = request.session['Emp_gid']
                Service_out = outputSplit(dispatch_dtl.set_PODDispatch(), 0)
                return JsonResponse(Service_out, safe=False)


def Courier_dtl(request):
    utl.check_authorization(request)
    utl.check_pointaccess(request)
    if request.method == 'POST':
        Courier_dtl =  mService.Service_model()
        jsondata = json.loads(request.body.decode('utf-8'))
        Courier_dtl.courier_gid =jsondata.get('params').get('courier_gid')
        Courier_dtl.courier_name = jsondata.get('params').get('courier_name')
        Courier_dtl.entity_gid = decry_data(request.session['Entity_gid'])
        data = Courier_dtl.get_courier()
        jdata = data.to_json(orient='records')
        return JsonResponse(json.loads(jdata), safe=False)

def ServicePOD(request):
    utl.check_authorization(request)
    return render(request,"service_pod.html")

def ServiceDirect(request):
    utl.check_authorization(request)
    return render(request,"service_requestDirect.html")

def ServiceRepaired(request):
    utl.check_authorization(request)
    return render(request,"service_repair.html")

def Repair_set(request):
    utl.check_authorization(request)
    utl.check_pointaccess(request)
    if request.method == 'POST':
        repair_dtl = mService.Service_model()
        jsondata = json.loads(request.body.decode('utf-8'))
        repair_dtl.action = jsondata.get('params').get('action')
        repair_dtl.SERVICE_JSON = jsondata.get('params').get('service_dtl')
        repair_dtl.entity_gid = request.session['Entity_gid']
        repair_dtl.employee_gid = request.session['Emp_gid']
        Repair_out = outputSplit(repair_dtl.set_Repair(), 1)
        return JsonResponse(Repair_out, safe=False)

def Component_get(request):
    utl.check_authorization(request)
    utl.check_pointaccess(request)
    if request.method == 'POST':
        Component_dtl =  mService.Service_model()
        jsondata = json.loads(request.body.decode('utf-8'))
        Component_dtl.component_gid =jsondata.get('params').get('component_gid')
        Component_dtl.service_gid = jsondata.get('params').get('service_gid')
        Component_dtl.entity_gid = request.session['Entity_gid']
        data = Component_dtl.get_component()
        jdata = data.to_json(orient='records')
        return JsonResponse(json.loads(jdata), safe=False)


def PODDispatch_Set(request):
    utl.check_authorization(request)
    utl.check_pointaccess(request)
    if request.method == 'POST':
        dispatch_dtl = mService.Service_model()
        jsondata = json.loads(request.body.decode('utf-8'))
        lst = jsondata.get('dispatch_data')
        for x in lst:
            dispatch_dtl.action = x.get('action')
            dispatch_dtl.type = x.get('type')
            dispatch_dtl.courier_gid = x.get('courier_gid')
            dispatch_dtl.Dispatch_date = x.get('Dispatch_date')
            dispatch_dtl.send_by = x.get('send_by')
            dispatch_dtl.awbno = x.get('awbno')
            dispatch_dtl.dispatch_mode = x.get('dispatch_mode')
            dispatch_dtl.dispatch_type = x.get('dispatch_type')
            dispatch_dtl.packets = x.get('packets')
            dispatch_dtl.weight = x.get('weight')
            dispatch_dtl.dispatch_to = x.get('dispatch_to')
            dispatch_dtl.address = x.get('address')
            dispatch_dtl.city = x.get('city')
            dispatch_dtl.state = x.get('state')
            dispatch_dtl.pincode = x.get('pincode')
            dispatch_dtl.remark = x.get('remark')
            dispatch_dtl.returned = x.get('returned')
            dispatch_dtl.returned_on = x.get('returned_on')
            dispatch_dtl.returned_remark = x.get('returned_remark')
            dispatch_dtl.pod = x.get('pod')
            dispatch_dtl.pod_image = x.get('pod_image')
            dispatch_dtl.isactive = x.get('isactive')
            dispatch_dtl.isremoved = x.get('isremoved')
            dispatch_dtl.dispatch_gid = x.get('dispatch_gid')
            dispatch_dtl.entity_gid = request.session['Entity_gid']
        dispatch_dtl.employee_gid = request.session['Emp_gid']
        Service_out = outputSplit(dispatch_dtl.set_PODDispatch(), 0)
        return JsonResponse(Service_out, safe=False)

# def uploaddata(request):
#     utl.check_authorization(request)
#     return render(request, "file_upload.html")

def upload_image(request):
    utl.check_authorization(request)
    utl.check_pointaccess(request)
    if request.method == 'POST' and request.FILES['file']:
        try:
          newdoc = mService.Document(docfile=request.FILES['file'])
          form = mService.UploadFileForm(request.POST, request.FILES)
          if form.is_valid():
              Uploaded_name= request.POST['filename']
              request.FILES['file'].name = Uploaded_name
              #filename, file_extension = os.path.splitext(request.FILES['file'].name)
              #request.FILES['file'].name = "new"+file_extension
              newdoc.save()
        except:
          print("error occured")
        return JsonResponse("saved", safe=False)

def employee_get(request):
    utl.check_authorization(request)
    utl.check_pointaccess(request)
    if request.method == 'GET':
        gid = ''
        name = ''
        cluster_gid = '1'
        all_cluster_gid = 'ALL'
        executive = ''
        obj_master = mService.Service_model()
        obj_master.jsonData = json.dumps({"entity_gid": [request.session['Entity_gid']], "client_gid": []})
        emp = obj_master.get_employee()
        emp['emp_gid'] =request.session['Emp_gid']
        jdata = emp.to_json(orient='records')
        return JsonResponse(jdata, safe=False)

def Get_address(request):
    utl.check_authorization(request)
    utl.check_pointaccess(request)
    if request.method == 'POST':
        obj_customer_ddl =  mService.Service_model()
        jsondata = json.loads(request.body.decode('utf-8'))
        obj_customer_ddl.location_gid =jsondata.get('params').get('location_gid')
        obj_customer_ddl.entity_gid = request.session['Entity_gid']
        df_customer_ddl = obj_customer_ddl.Location_Get()
        jdata = df_customer_ddl.to_json(orient='records')
        return JsonResponse(json.loads(jdata), safe=False)

def Get_Dispatch(request):
    utl.check_authorization(request)
    utl.check_pointaccess(request)
    if request.method == 'POST':
        obj_customer_ddl =  mService.Service_model()
        jsondata = json.loads(request.body.decode('utf-8'))
        obj_customer_ddl.action =jsondata.get('params').get('action')
        obj_customer_ddl.entity_gid = request.session['Entity_gid']
        df_customer_ddl = obj_customer_ddl.Dispatch_Get()
        jdata = df_customer_ddl.to_json(orient='records')
        return JsonResponse(json.loads(jdata), safe=False)

def DispatchPOD_set(request):
    utl.check_authorization(request)
    utl.check_pointaccess(request)
    if request.method == 'POST':
        service_dtl =  mService.Service_model()
        jsondata = json.loads(request.body.decode('utf-8'))
        service_dtl.action ='DISPATCH_STATUS'
        service_dtl.dispatch_gid = jsondata.get('dispatch_gid')
        service_dtl.status = 'SERVICE CLOSED'
        service_dtl.SERVICE_JSON = '{}'
        service_dtl.entity_gid = request.session['Entity_gid']
        service_dtl.employee_gid = request.session['Emp_gid']
        Service_out = outputSplit(service_dtl.set_servicedtl(), 0)
        return JsonResponse(Service_out, safe=False)