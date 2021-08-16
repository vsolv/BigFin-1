import io
import time
import boto3
import requests
from Bigflow.Master import views as master_views
from django.core.files.storage import default_storage
from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
import json
import Bigflow.Core.models as common
import Bigflow.Core.jwt_file as jwt
from datetime import datetime
from django.conf import settings
from django.core.files.base import ContentFile
from Bigflow.ATMA.model import mATMA
from Bigflow.menuClass import utility as utl
from Bigflow.Core.models import decrpt as decry_data
ip = common.localip()


def ATMA_PartnerSummary(request):
    utl.check_authorization(request)
    return render(request,'ATMA_PartnerSummary.html')

def atma_activitydetails(request):
    utl.check_authorization(request)
    return render(request, 'atma_activitydetails.html')

def atma_activitydetailsview(request):
    utl.check_pointaccess(request)
    return render(request, 'atma_activitydetailsview.html')


def atma_activitydetailsedit(request):
    utl.check_pointaccess(request)
    return render(request, 'atma_activitydetailsedit.html')


def atma_catalogcreation(request):
    utl.check_authorization(request)
    return render(request, "atma_catalogcreation.html")

def AtmaPartnerMaker (request):
    utl.check_authorization(request)
    return render(request, "atma_partnermaker.html")

def atmacatalogset(request):
   utl.check_authorization(request)
   if request.method == 'POST':
       jsondata = json.loads(request.body.decode('utf-8'))
       if (jsondata.get('Group')) == 'Catalog Details':
           grp = jsondata.get('Group')
           action = jsondata.get('Action')
           typ = jsondata.get('Group')
           data = json.dumps(jsondata.get('data'))
           dataw = json.dumps(jsondata.get('data').get('Classification'))
           params = {'Group': "" + grp + "", 'Action': "" + action + "", 'Type': "" + typ + ""}
           token = jwt.token(request)
           headers = {"content-type": "application/json", "Authorization": "" + token + ""}
           datas = json.dumps(jsondata.get('data'))
           resp = requests.post("" + ip + "/atmaCatalog_Setapi", params=params, data=datas, headers=headers, verify=False)
           response = resp.content.decode("utf-8")
           return HttpResponse(response)

       if (jsondata.get('Group')) == 'Catalog_Details_Update':
           grp = jsondata.get('Group')
           action = jsondata.get('Action')
           typ = jsondata.get('Type')
           data = json.dumps(jsondata.get('data').get('Params'))
           dataw = json.dumps(jsondata.get('data').get('Classification'))
           params = {'Group': "" + grp + "", 'Action': "" + action + "", 'Type': "" + typ + ""}
           token = jwt.token(request)
           headers = {"content-type": "application/json", "Authorization": "" + token + ""}
           datas = json.dumps(jsondata.get('data'))
           resp = requests.post("" + ip + "/atmaCatalog_Setapi", params=params, data=datas, headers=headers,
                                verify=False)
           response = resp.content.decode("utf-8")
           return HttpResponse(response)

       if (jsondata.get('Group')) == 'CATALOG_ASSIGN':
           grp = jsondata.get('Group')
           action = jsondata.get('Action')
           typ = jsondata.get('Type')
           data = json.dumps(jsondata.get('data').get('Params'))
           dataw = json.dumps(jsondata.get('data').get('Classification'))
           params = {'Group': "" + grp + "", 'Action': "" + action + "", 'Type': "" + typ + ""}
           token = jwt.token(request)
           headers = {"content-type": "application/json", "Authorization": "" + token + ""}
           datas = json.dumps(jsondata.get('data'))
           resp = requests.post("" + ip + "/atmaCatalog_Setapi", params=params, data=datas, headers=headers,
                                verify=False)
           response = resp.content.decode("utf-8")
           return HttpResponse(response)

def atmacatalog_get(request):
   utl.check_authorization(request)
   if request.method == 'POST':
       jsondata = json.loads(request.body.decode('utf-8'))
       if (jsondata.get('Group')) == 'Catalog_Details':
           grp = jsondata.get('Group')
           typ = jsondata.get('Type')
           data = json.dumps(jsondata.get('data'))
           params = {'Group': "" + grp + "", 'Type': "" + typ + ""}
           token = jwt.token(request)
           headers = {"content-type": "application/json", "Authorization": "" + token + ""}
           datas = json.dumps(jsondata.get('data'))
           resp = requests.post("" + ip + "/atmaCatalog_Getapi", params=params, data=datas, headers=headers, verify=False)
           response = resp.content.decode("utf-8")
           return HttpResponse(response)

       if (jsondata.get('Group')) == 'partner_product':
           grp = jsondata.get('Group')
           typ = jsondata.get('Type')
           data = json.dumps(jsondata.get('data'))
           params = {'Group': "" + grp + "", 'Type': "" + typ + ""}
           token = jwt.token(request)
           headers = {"content-type": "application/json", "Authorization": "" + token + ""}
           datas = json.dumps(jsondata.get('data'))
           resp = requests.post("" + ip + "/atmaCatalog_Getapi", params=params, data=datas, headers=headers, verify=False)
           response = resp.content.decode("utf-8")
           return HttpResponse(response)

def atma_getdata(request):
   utl.check_authorization(request)
   if request.method == 'POST':
       jsondata = json.loads(request.body.decode('utf-8'))
       if (jsondata.get('Params').get('Group')) == 'ATMASUMMARY':
           obj = mATMA.ATMA_model()
           grp = jsondata.get('Params').get('Group')
           action = jsondata.get('Params').get('Action')
           params = {'Group': "" + grp + "", 'Action': "" + action + ""}
           token = jwt.token(request)
           headers = {"content-type": "application/json", "Authorization": "" + token + ""}
           datas = json.dumps(jsondata)
           resp = requests.post("" + ip + "/GET_ATMA_Data", params=params, data=datas, headers=headers, verify=False)
           response = resp.content.decode("utf-8")
           return HttpResponse(response)
       if (jsondata.get('Params').get('Group')) == 'ATMA_APPROVAL_SUMMARY':
           obj = mATMA.ATMA_model()
           grp = jsondata.get('Params').get('Group')
           action = jsondata.get('Params').get('Action')
           params = {'Group': "" + grp + "", 'Action': "" + action + ""}
           token = jwt.token(request)
           headers = {"content-type": "application/json", "Authorization": "" + token + ""}
           datas = json.dumps(jsondata)
           resp = requests.post("" + ip + "/GET_ATMA_Data", params=params, data=datas, headers=headers, verify=False)
           response = resp.content.decode("utf-8")
           return HttpResponse(response)
       if (jsondata.get('Params').get('Group')) == 'QUERYSUMMARY':
           obj = mATMA.ATMA_model()
           grp = jsondata.get('Params').get('Group')
           action = jsondata.get('Params').get('Action')
           params = {'Group': "" + grp + "", 'Action': "" + action + ""}
           token = jwt.token(request)
           headers = {"content-type": "application/json", "Authorization": "" + token + ""}
           datas = json.dumps(jsondata)
           resp = requests.post("" + ip + "/GET_ATMA_Data", params=params, data=datas, headers=headers, verify=False)
           response = resp.content.decode("utf-8")
           return HttpResponse(response)
       if (jsondata.get('Params').get('Group')) == 'ATMAPAYMENTSUMMARY':
           grp = jsondata.get('Params').get('Group')
           action = jsondata.get('Params').get('Action')
           data = json.dumps(jsondata.get('data'))
           params = {'Group': "" + grp + "", 'Action': "" + action + ""}
           token = jwt.token(request)
           headers = {"content-type": "application/json", "Authorization": "" + token + ""}
           datas = json.dumps(jsondata)
           resp = requests.post("" + ip + "/GET_ATMA_Data", params=params, data=datas, headers=headers, verify=False)
           return HttpResponse(resp)

       if (jsondata.get('Params').get('Group')) == 'Transaction_Group':
           grp = jsondata.get('Params').get('Group')
           action = jsondata.get('Params').get('Action')
           data = json.dumps(jsondata.get('data'))
           params = {'Group': "" + grp + "", 'Action': "" + action + ""}
           token = jwt.token(request)
           headers = {"content-type": "application/json", "Authorization": "" + token + ""}
           datas = json.dumps(jsondata)
           resp = requests.post("" + ip + "/GET_ATMA_Data", params=params, data=datas, headers=headers, verify=False)
           return HttpResponse(resp)

def atma_ProductCatSubCat_get(request):
  utl.check_authorization(request)
  if request.method == 'POST':
      jsondata = json.loads(request.body.decode('utf-8'))
      if (jsondata.get('Group')) == 'Activity_Group':
          grp = jsondata.get('Group')
          typ = jsondata.get('Type')
          data = json.dumps(jsondata.get('data'))
          params = {'Group': "" + grp + "", 'Type': "" + typ + ""}
          token = jwt.token(request)
          headers = {"content-type": "application/json", "Authorization": "" + token + ""}
          datas = json.dumps(jsondata.get('data'))
          resp = requests.post("" + ip + "/atma_ProductCatSubCat_getAPI", params=params, data=datas, headers=headers, verify=False)
          response = resp.content.decode("utf-8")
          return HttpResponse(response)

def atma_changerequest_activationupdate(request):
    utl.check_authorization(request)
    if request.method == 'POST':
        jsondata=json.loads(request.body.decode('utf-8'))
        if (jsondata.get('Group')) == 'Activation_Request':
            obj=mATMA.ATMA_model()
            grp = jsondata.get('Group')
            action = jsondata.get('Action')
            params = {'Group': "" + grp + "", 'Action': "" + action + ""}
            token = jwt.token(request)
            headers = {"content-type": "application/json", "Authorization": "" + token + ""}
            datas = json.dumps(jsondata)
            resp = requests.post("" + ip + "/Update_changerequest_API", params=params, data=datas, headers=headers,
                                 verify=False)
            response = resp.content.decode("utf-8")
            return HttpResponse(response)

def atma_getdirectordata(request):
    utl.check_authorization(request)
    if request.method == 'POST':
        jsondata = json.loads(request.body.decode('utf-8'))
        if (jsondata.get('Params').get('Group')) == 'ATMASUMMARY':
            obj = mATMA.ATMA_model()
            grp = jsondata.get('Params').get('Group')
            action = jsondata.get('Params').get('Action')
            params = {'Group': "" + grp + "", 'Action': "" + action + ""}
            token = jwt.token(request)
            headers = {"content-type": "application/json", "Authorization": "" + token + ""}
            datas = json.dumps(jsondata)
            resp = requests.post("" + ip + "/GET_ATMA_Directors_Data", params=params, data=datas, headers=headers, verify=False)
            response = resp.content.decode("utf-8")
            return HttpResponse(response)

def atma_viewdata(request):
    utl.check_pointaccess(request)
    return render(request,'ATMA_viewdata.html')

def atma_partneradd(request):
    utl.check_authorization(request)
    return render(request,'ATMA_Partneradd.html')

def atma_activityaddIndex(request):
    utl.check_pointaccess(request)
    return render(request, "ATMA_Activity.html")
def create_activity_details(request):
    utl.check_pointaccess(request)
    return render(request, "create_activity_details.html")

def atma_ActivitydetailsIndex(request):
    utl.check_authorization(request)
    return render(request, "atma_activitydetails.html")

def create_catalog_details(request):
    utl.check_pointaccess(request)
    return render(request, "create_catalog_details.html")
def Partner_Address(request):
    utl.check_pointaccess(request)
    return render(request, "Partner_Address.html")
def Partner_Contact(request):
    utl.check_pointaccess(request)
    return render(request, "Partner_Contact.html")

def Query_Page(request):
    utl.check_authorization(request)
    return render(request, "Query_Page.html")
def Renewal_Page(request):
    utl.check_authorization(request)
    return render(request, "Renewal_Page.html")

def atma_activitydetailsset(request):
   utl.check_authorization(request)
   if request.method == 'POST':
       jsondata = json.loads(request.body.decode('utf-8'))
       if (jsondata.get('Group')) == 'Activity_Details':
           grp = jsondata.get('Group')
           action=jsondata.get('Action')
           typ = jsondata.get('Type')
           data = json.dumps(jsondata.get('data').get('Params'))
           dataw = json.dumps(jsondata.get('data').get('Classification'))
           params = {'Group': "" + grp + "", 'Action': "" + action + "", 'Type': "" + typ+ ""}
           token = jwt.token(request)
           headers = {"content-type": "application/json", "Authorization": "" + token + ""}
           datas = json.dumps(jsondata.get('data'))
           resp = requests.post("" + ip + "/atma_Activitydetails_Set", params=params, data=datas, headers=headers, verify=False)
           response = resp.content.decode("utf-8")
           return HttpResponse(response)

       if (jsondata.get('Group')) == 'Activity_Details_Update':
           grp = jsondata.get('Group')
           action=jsondata.get('Action')
           typ = jsondata.get('Type')
           data = json.dumps(jsondata.get('data').get('Params'))
           dataw = json.dumps(jsondata.get('data').get('Classification'))
           params = {'Group': "" + grp + "", 'Action': "" + action + "", 'Type': "" + typ+ ""}
           token = jwt.token(request)
           headers = {"content-type": "application/json", "Authorization": "" + token + ""}
           datas = json.dumps(jsondata.get('data'))
           resp = requests.post("" + ip + "/atma_Activitydetails_Set", params=params, data=datas, headers=headers, verify=False)
           response = resp.content.decode("utf-8")
           return HttpResponse(response)

def atma_activitydetailsget(request):
   utl.check_authorization(request)
   if request.method == 'POST':
       jsondata = json.loads(request.body.decode('utf-8'))
       if (jsondata.get('Group')) == 'Activity_Details':
           grp = jsondata.get('Group')
           typ = jsondata.get('Type')
           data = json.dumps(jsondata.get('data'))
           params = {'Group': "" + grp + "", 'Type': "" + typ + ""}
           token = jwt.token(request)
           headers = {"content-type": "application/json", "Authorization": "" + token + ""}
           datas = json.dumps(jsondata.get('data'))
           resp = requests.post("" + ip + "/atma_Activitydetails_Get", params=params, data=datas, headers=headers, verify=False)
           response = resp.content.decode("utf-8")
           return HttpResponse(response)

def atmaPartnerPayment_Set(request):
   utl.check_authorization(request)
   if request.method == 'POST':
       jsondata = json.loads(request.body.decode('utf-8'))
       if (jsondata.get('Group')) == 'Header Details':
           grp = jsondata.get('Group')
           action = jsondata.get('Action')
           typ = jsondata.get('Group')
           data = json.dumps(jsondata.get('data'))
           params = {'Group': "" + grp + "", 'Action': "" + action + "", 'Type': "" + typ + ""}
           token = jwt.token(request)
           headers = {"content-type": "application/json", "Authorization": "" + token + ""}

           datas = json.dumps(jsondata.get('data'))
           resp = requests.post("" + ip + "/atmaPartnerPayment_Setapi", params=params, data=datas, headers=headers, verify=False)
           response = resp.content.decode("utf-8")
           return HttpResponse(response)

       if (jsondata.get('Params').get('Group')) == 'PAYMODESUMMARY':
           grp = jsondata.get('Params').get('Group')
           action = jsondata.get('Params').get('Action')
           data = json.dumps(jsondata.get('data'))
           params = {'Group': "" + grp + "", 'Action': "" + action + ""}
           token = jwt.token(request)
           headers = {"content-type": "application/json", "Authorization": "" + token + ""}
           datas = json.dumps(jsondata)
           resp = requests.post("" + ip + "/atmaPartnerPayment_Setapi", params=params, data=datas, headers=headers, verify=False)
           return HttpResponse(resp)

       elif (jsondata.get('Params').get('Group')) == 'MoveToRM':
           group=jsondata.get('Params').get('Group')
           action=jsondata.get('Params').get('Action')
           data=json.dumps(jsondata.get('data'))
           params = {'Group':"" + group + "", 'Action':"" + action + ""}
           token = jwt.token(request)
           headers = {"content-type": "application/json", "Authorization":"" + token + ""}
           datas=json.dumps(jsondata)
           resp = requests.post("" + ip + "/atmaPartnerPayment_Setapi", params=params, data=datas, headers=headers, verify=False)
           return HttpResponse(resp)
       elif (jsondata.get('Params').get('Group')) == 'UPDATEPAYMODESUMMARY':
           grp = jsondata.get('Params').get('Group')
           action = jsondata.get('Params').get('Action')
           data = json.dumps(jsondata.get('data'))
           params = {'Group': "" + grp + "", 'Action': "" + action + ""}
           token = jwt.token(request)
           headers = {"content-type": "application/json", "Authorization": "" + token + ""}
           datas = json.dumps(jsondata)
           resp = requests.post("" + ip + "/atmaPartnerPayment_Setapi", params=params, data=datas, headers=headers, verify=False)
           return HttpResponse(resp)


def atma_addpayment(request):
    utl.check_pointaccess(request)
    return render(request,"Atma_AddPayment.html")

def atma_paymentdetails(request):
    utl.check_pointaccess(request)
    return render(request,'atma_paymentdetails.html')

def atma_attachmentdetails(request):
    utl.check_pointaccess(request)
    return render(request,'atma_attachmentdetails.html')

def atma_branchdetailsdropdown(request):
    utl.check_authorization(request)
    utl.check_pointaccess(request)
    if request.method == 'POST':
        report_data = mATMA.ATMA_model()
        jsondata = json.loads(request.body.decode('utf-8'))
        report_data.type = jsondata.get('Params').get('Type')
        report_data.gid = jsondata.get('Params').get('bank_gid')
        report_data.finaldata = json.dumps({'branch_gid': report_data.gid})
        report_data.emptyjson = json.dumps({})
        module_name = report_data.bankbranch_module()
        jdata = module_name.to_json(orient='records')
        return HttpResponse(jdata)



def atma_docgroupset(request):
   utl.check_authorization(request)
   if request.method == 'POST':
       jsondata = json.loads(request.body.decode('utf-8'))
       if (jsondata.get('Group')) == 'Document_Group':
           grp = jsondata.get('Group')
           action=jsondata.get('Action')
           typ = jsondata.get('Type')
           data = json.dumps(jsondata.get('data'))
           params = {'Group': "" + grp + "", 'Action': "" + action + "", 'Type': "" + typ+ ""}
           token = jwt.token(request)
           headers = {"content-type": "application/json", "Authorization": "" + token + ""}
           datas = json.dumps(jsondata.get('data'))
           resp = requests.post("" + ip + "/atmaapi_Docgroup_Set", params=params, data=datas, headers=headers, verify=False)
           response = resp.content.decode("utf-8")
           return HttpResponse(response)

def atma_doc_get(request):
   utl.check_authorization(request)
   if request.method == 'POST':
       jsondata = json.loads(request.body.decode('utf-8'))
       if (jsondata.get('Group')) == 'Document_Group':
           grp = jsondata.get('Group')
           typ = jsondata.get('Type')
           data = json.dumps(jsondata.get('data'))
           params = {'Group': "" + grp + "", 'Type': "" + typ + ""}
           token = jwt.token(request)
           headers = {"content-type": "application/json", "Authorization": "" + token + ""}
           datas = json.dumps(jsondata.get('data'))
           resp = requests.post("" + ip + "/atmaAttachment_apiurl", params=params, data=datas, headers=headers, verify=False)
           response = resp.content.decode("utf-8")
           return HttpResponse(response)

def atma_attachmentupload(request):
   utl.check_authorization(request)
   if request.method == 'POST' and request.FILES['file']:

        # current_month = datetime.now().strftime('%m')
        # current_day = datetime.now().strftime('%d')
        # current_year_full = datetime.now().strftime('%Y')
        # save_path = str(settings.MEDIA_ROOT) + '/Atma_Documents/' + str(current_year_full) + '/' + str(current_month) + '/' + str(current_day) + '/' + str(request.POST['name'])
        # print(save_path)
        # path = default_storage.save(str(save_path), request.FILES['file'])
        filename = str(request.FILES['file'])
        millis = int(round(time.time() * 1000))
        s1 = str(millis)
        Create_By= decry_data(request.POST['Create_By'])
        c1 = str(Create_By)
        concat_filename = c1 + "_" + s1 + "_" + filename

        grp = request.POST['Group']
        action=request.POST['Action']
        typ = request.POST['Type']

        data = {"Documents_Partnergid": request.POST['Documents_Partnergid'],"Documents_Docgroupgid": request.POST['Documents_Docgroupgid'],
                "Documents_Period": request.POST['Documents_Period'],"Description": request.POST['Description'],"File_Name": concat_filename,
                                      "File_Path": "save_path", "Entity_Gid":request.POST['Entity_Gid'],"Create_By": request.POST['Create_By']
        }
        s3 = boto3.resource('s3')
        s3_obj = s3.Object(bucket_name=common.s3_bucket_name(), key=concat_filename)
        s3_obj.put(Body=request.FILES['file'])

        s3_client = boto3.client('s3')
        #a=master_views.fileUploadS3(request)

        datas = json.dumps(data)

        params = {'Group': "" + grp + "", 'Action': "" + action + "", 'Type': "" + typ+ ""}
        token = jwt.token(request)
        headers = {"content-type": "application/json", "Authorization": "" + token + ""}

        resp = requests.post("" + ip + "/atma_Docgroup_Setapi", params=params, data=datas, headers=headers, verify=False)
        response = resp.content.decode("utf-8")
        return HttpResponse(response)

def atma_gettaxdetails(request):
    utl.check_authorization(request)
    jsondata = json.loads(request.body.decode('utf-8'))
    if (jsondata.get('Params').get('Group')) == 'GETTAXTYPE':
        obj = mATMA.ATMA_model()
        grp = jsondata.get('Params').get('Group')
        action = jsondata.get('Params').get('Action')
        params = {'Group': "" + grp + "", 'Action': "" + action + ""}
        token = jwt.token(request)
        headers = {"content-type": "application/json", "Authorization": "" + token + ""}
        datas = json.dumps(jsondata)
        resp = requests.post("" + ip + "/Gettaxdetails", params=params, data=datas, headers=headers, verify=False)
        response = resp.content.decode("utf-8")
        return HttpResponse(response)
    elif (jsondata.get('Params').get('Group')) == 'TAXINSERTSUMMARY':
        obj = mATMA.ATMA_model()
        grp = jsondata.get('Params').get('Group')
        action = jsondata.get('Params').get('Action')
        params = {'Group': "" + grp + "", 'Action': "" + action + ""}
        token = jwt.token(request)
        headers = {"content-type": "application/json", "Authorization": "" + token + ""}
        datas = json.dumps(jsondata)
        resp = requests.post("" + ip + "/Gettaxdetails", params=params, data=datas, headers=headers, verify=False)
        response = resp.content.decode("utf-8")
        return HttpResponse(response)
    elif (jsondata.get('Params').get('Group')) == 'ATMATAXSUMMARY':
        obj = mATMA.ATMA_model()
        grp = jsondata.get('Params').get('Group')
        action = jsondata.get('Params').get('Action')
        params = {'Group': "" + grp + "", 'Action': "" + action + ""}
        token = jwt.token(request)
        headers = {"content-type": "application/json", "Authorization": "" + token + ""}
        datas = json.dumps(jsondata)
        resp = requests.post("" + ip + "/Gettaxdetails", params=params, data=datas, headers=headers, verify=False)
        response = resp.content.decode("utf-8")
        return HttpResponse(response)

def atma_taxdetailsfileupload(request):
    utl.check_authorization(request)
    if request.POST['Group'] == "TAXINSERTSUMMARYEXEMPTEDYES":
        if request.method == 'POST' and request.FILES['file']:
            # current_month = datetime.now().strftime('%m')
            # current_day = datetime.now().strftime('%d')
            # current_year_full = datetime.now().strftime('%Y')
            # save_path = str(settings.MEDIA_ROOT) + '/Atma_TDSDocuments/' + str(current_year_full) + '/' + str(
            #     current_month) + '/' + str(current_day) + '/' + str(request.POST['name'])
            # print(save_path)
            # path = default_storage.save(str(save_path), request.FILES['file'])
            grp = request.POST['Group']
            action = request.POST['Action']
            Create_By = request.POST['Create_By']
            # File_Names=request.POST['File_Name']
            filename = str(request.FILES['file'])
            millis = int(round(time.time() * 1000))
            s1 = str(millis)
            concat_filename = Create_By + "_" + s1 + "_" + filename
            data = {"Tax_Gid": request.POST['Tax_Gid'],
                    "TaxDetails_Partner_Gid": request.POST['TaxDetails_Partner_Gid'],
                    "TaxDetails_Partnerbranchcode":request.POST['TaxDetails_Partnerbranchcode'],
                    "TaxDetails_Partner_Code": request.POST['TaxDetails_Partner_Code'],
                    "TaxDetails_Partner_Type": request.POST['TaxDetails_Partner_Type'],
                    "TaxDetails_TaxNo": request.POST['TaxDetails_TaxNo'],
                    "TaxSubDetails_TaxRate_Gid": request.POST['TaxSubDetails_TaxRate_Gid'],
                    "TaxSubDetails_ExcemthroSold": request.POST['TaxSubDetails_ExcemthroSold'],
                    "TaxSubDetails_TaxRate": request.POST['TaxSubDetails_TaxRate'],
                    "TaxSubDetails_IsExcempted": request.POST['TaxSubDetails_IsExcempted'],
                    "TaxSubDetails_ExcemTo": request.POST['TaxSubDetails_ExcemTo'],
                    "TaxSubDetails_ExcemFrom": request.POST['TaxSubDetails_ExcemFrom'],
                    "TaxSubDetails_ExcemRate": request.POST['TaxSubDetails_ExcemRate'],
                    "FileName": concat_filename, "FilePath": "save_path",
                    "Create_By": request.POST['Create_By'],"Tds":request.POST['Tds'],
                    "TaxDetails_Is_MSME": request.POST['TaxDetails_Is_MSME']
                    }, {"Entity_Gid": request.session['Entity_gid']}

            s3 = boto3.resource('s3')
            s3_obj = s3.Object(bucket_name=common.s3_bucket_name(), key=concat_filename)
            s3_obj.put(Body=request.FILES['file'])

            s3_client = boto3.client('s3')
            datas = json.dumps(data)
            params = {'Group': "" + grp + "", 'Action': "" + action + ""}
            token = jwt.token(request)
            headers = {"content-type": "application/json", "Authorization": "" + token + ""}
            resp = requests.post("" + ip + "/Gettaxdetails", params=params, data=datas, headers=headers, verify=False)
            response = resp.content.decode("utf-8")
            return HttpResponse(response)
    if request.POST['Group'] == "TAXINSERTSUMMARYEXEMPTEDNO":
        grp = request.POST['Group']
        action = request.POST['Action']
        save_path = ""
        data = {"Tax_Gid": request.POST['Tax_Gid'],
                "TaxDetails_Partner_Gid":request.POST['TaxDetails_Partner_Gid'],
                "TaxDetails_Partnerbranchcode": request.POST['TaxDetails_Partnerbranchcode'],
                "TaxDetails_Partner_Code":request.POST['TaxDetails_Partner_Code'],
                "TaxDetails_Partner_Type":request.POST['TaxDetails_Partner_Type'],
                "TaxDetails_TaxNo": request.POST['TaxDetails_TaxNo'],
                "TaxSubDetails_TaxRate_Gid": request.POST['TaxSubDetails_TaxRate_Gid'],
                "TaxDetails_Is_MSME": request.POST['TaxDetails_Is_MSME'],
                "TaxSubDetails_ExcemthroSold": request.POST['TaxSubDetails_ExcemthroSold'],
                "TaxSubDetails_TaxRate": request.POST['TaxSubDetails_TaxRate'],
                "TaxSubDetails_IsExcempted": request.POST['TaxSubDetails_IsExcempted'],
                "TaxSubDetails_ExcemTo": request.POST['TaxSubDetails_ExcemTo'],
                "TaxSubDetails_ExcemFrom": request.POST['TaxSubDetails_ExcemFrom'],
                "TaxSubDetails_ExcemRate": request.POST['TaxSubDetails_ExcemRate'],
                "FileName": request.POST['FileName'], "FilePath": save_path,
                "Create_By": request.POST['Create_By'],"Tds": request.POST['Tds']
                }, {"Entity_Gid": request.session['Entity_gid']}
        datas = json.dumps(data)
        params = {'Group': "" + grp + "", 'Action': "" + action + ""}
        token = jwt.token(request)
        headers = {"content-type": "application/json", "Authorization": "" + token + ""}
        resp = requests.post("" + ip + "/Gettaxdetails", params=params, data=datas, headers=headers, verify=False)
        response = resp.content.decode("utf-8")
        return HttpResponse(response)
    if request.POST['Group'] == "TAXINSERTSUMMARYEXEMPTEDUPDATENO":
        grp = request.POST['Group']
        action = request.POST['Action']
        data = {"Tax_Gid": request.POST['Tax_Gid'],
            "TaxDetails_Partner_Gid": request.POST['TaxDetails_Partner_Gid'],
            "TaxDetails_Partnerbranchcode": request.POST['TaxDetails_Partnerbranchcode'],
            "TaxDetails_Partner_Code": request.POST['TaxDetails_Partner_Code'],
            "TaxDetails_Partner_Type": request.POST['TaxDetails_Partner_Type'],
            "TaxDetails_Is_MSME": request.POST['TaxDetails_Is_MSME'],
            "TaxDetails_TaxNo": request.POST['TaxDetails_TaxNo'],
            "TaxDetails_Gid": request.POST['TaxDetails_Gid'],
            "TaxSubDetails_TaxRate_Gid": request.POST['TaxSubDetails_TaxRate_Gid'],
            "TaxSubDetails_TaxRate": request.POST['TaxSubDetails_TaxRate'],
            "TaxSubDetails_IsExcempted": request.POST['TaxSubDetails_IsExcempted'],
            }, {"Entity_Gid": request.session['Entity_gid'], "Update_By": request.POST['Create_By']}
        datas = json.dumps(data)
        params = {'Group': "" + grp + "", 'Action': "" + action + ""}
        token = jwt.token(request)
        headers = {"content-type": "application/json", "Authorization": "" + token + ""}
        token = jwt.token(request)
        resp = requests.post("" + ip + "/Gettaxdetails", params=params, data=datas, headers=headers, verify=False)
        response = resp.content.decode("utf-8")
        return HttpResponse(response)
    if request.POST['Group'] == "TAXINSERTSUMMARYEXEMPTEDUPDATEYES":
        if request.method == 'POST' and request.FILES['file']:
            # current_month = datetime.now().strftime('%m')
            # current_day = datetime.now().strftime('%d')
            # current_year_full = datetime.now().strftime('%Y')
            # save_path = str(settings.MEDIA_ROOT) + '/Atma_TDSDocuments/' + str(current_year_full) + '/' + str(
            #     current_month) + '/' + str(current_day) + '/' + str(request.POST['name'])
            # print(save_path)
            # path = default_storage.save(str(save_path), request.FILES['file'])
            Create_By = request.POST['Create_By']
            # File_Names=request.POST['File_Name']
            filename = str(request.FILES['file'])
            millis = int(round(time.time() * 1000))
            s1 = str(millis)
            concat_filename = Create_By + "_" + s1 + "_" + filename

            grp = request.POST['Group']
            action = request.POST['Action']
            data = {"Tax_Gid": request.POST['Tax_Gid'],
                    "TaxDetails_Partner_Gid": request.POST['TaxDetails_Partner_Gid'],
                    "TaxDetails_Partnerbranchcode": request.POST['TaxDetails_Partnerbranchcode'],
                    "TaxDetails_Partner_Code": request.POST['TaxDetails_Partner_Code'],
                    "TaxDetails_Partner_Type": request.POST['TaxDetails_Partner_Type'],
                    "TaxDetails_TaxNo": request.POST['TaxDetails_TaxNo'],
                    "TaxDetails_Gid": request.POST['TaxDetails_Gid'],
                    "TaxDetails_Is_MSME": request.POST['TaxDetails_Is_MSME'],
                    "TaxSubDetails_TaxRate_Gid": request.POST['TaxSubDetails_TaxRate_Gid'],
                    "TaxSubDetails_ExcemthroSold": request.POST['TaxSubDetails_ExcemthroSold'],
                    "TaxSubDetails_TaxRate": request.POST['TaxSubDetails_TaxRate'],
                    "TaxSubDetails_IsExcempted": request.POST['TaxSubDetails_IsExcempted'],
                    "TaxSubDetails_ExcemTo": request.POST['TaxSubDetails_ExcemTo'],
                    "TaxSubDetails_ExcemFrom": request.POST['TaxSubDetails_ExcemFrom'],
                    "TaxSubDetails_ExcemRate": request.POST['TaxSubDetails_ExcemRate'],
                    "File_Name": concat_filename, "FilePath": "save_path"
                    }, {"Entity_Gid": request.session['Entity_gid'], "Update_By": request.POST['Create_By']}

            s3 = boto3.resource('s3')
            s3_obj = s3.Object(bucket_name=common.s3_bucket_name(), key=concat_filename)
            s3_obj.put(Body=request.FILES['file'])
            s3_client = boto3.client('s3')
            datas = json.dumps(data)
            params = {'Group': "" + grp + "", 'Action': "" + action + ""}
            token = jwt.token(request)
            headers = {"content-type": "application/json", "Authorization": "" + token + ""}
            resp = requests.post("" + ip + "/Gettaxdetails", params=params, data=datas, headers=headers, verify=False)
            response = resp.content.decode("utf-8")
            return HttpResponse(response)
    if request.POST['Group'] == "TAXINSERTSUMMARYEXEMPTEDUPDATEYESNOFILE":
        grp = request.POST['Group']
        action = request.POST['Action']
        data = {"Tax_Gid": request.POST['Tax_Gid'],
                "TaxDetails_Partner_Gid": request.POST['TaxDetails_Partner_Gid'],
                "TaxDetails_Partnerbranchcode": request.POST['TaxDetails_Partnerbranchcode'],
                "TaxDetails_Partner_Code": request.POST['TaxDetails_Partner_Code'],
                "TaxDetails_Partner_Type": request.POST['TaxDetails_Partner_Type'],
                "TaxDetails_TaxNo": request.POST['TaxDetails_TaxNo'],
                "TaxDetails_Gid": request.POST['TaxDetails_Gid'],
                "TaxDetails_Is_MSME": request.POST['TaxDetails_Is_MSME'],
                "TaxSubDetails_TaxRate_Gid": request.POST['TaxSubDetails_TaxRate_Gid'],
                "TaxSubDetails_ExcemthroSold": request.POST['TaxSubDetails_ExcemthroSold'],
                "TaxSubDetails_TaxRate": request.POST['TaxSubDetails_TaxRate'],
                "TaxSubDetails_IsExcempted": request.POST['TaxSubDetails_IsExcempted'],
                "TaxSubDetails_ExcemTo": request.POST['TaxSubDetails_ExcemTo'],
                "TaxSubDetails_ExcemFrom": request.POST['TaxSubDetails_ExcemFrom'],
                "TaxSubDetails_ExcemRate": request.POST['TaxSubDetails_ExcemRate'],
                "FilePath": request.POST['FilePath'],
                "File_Name": request.POST['File_Name'],
                }, {"Entity_Gid": request.session['Entity_gid'], "Update_By": request.POST['Create_By']}
        datas = json.dumps(data)
        params = {'Group': "" + grp + "", 'Action': "" + action + ""}
        token = jwt.token(request)
        headers = {"content-type": "application/json", "Authorization": "" + token + ""}
        resp = requests.post("" + ip + "/Gettaxdetails", params=params, data=datas, headers=headers,
                         verify=False)
        response = resp.content.decode("utf-8")
        return HttpResponse(response)
        return HttpResponse
def atma_updateattacment_details(request):
   utl.check_authorization(request)
   if request.POST['Group'] == "Document_Update":
       if request.method == 'POST' and request.FILES['file']:
           current_month = datetime.now().strftime('%m')
           current_day = datetime.now().strftime('%d')
           current_year_full = datetime.now().strftime('%Y')
           save_path = str(settings.MEDIA_ROOT) + '/Atma_Documents/' + str(current_year_full) + '/' + str(
               current_month) + '/' + str(current_day) + '/' + str(request.POST['name'])
           print(save_path)
           path = default_storage.save(str(save_path), request.FILES['file'])
           grp = request.POST['Group']
           action = request.POST['Action']
           typ = request.POST['Type']
           data = {"Documents_Gid": request.POST['Documents_Gid'],
                   "Documents_Docgroupgid": request.POST['Documents_Docgroupgid'],
                  "Description": request.POST['Description'],
                   "File_Name": request.POST['File_Name'],
                   "File_Path":save_path,
                   "Update_By": request.session['Emp_gid'],
                   }
           datas = json.dumps(data)
           params = {'Group': "" + grp + "", 'Action': "" + action + "", 'Type': "" + typ + ""}
           token = jwt.token(request)
           headers = {"content-type": "application/json", "Authorization": "" + token + ""}
           resp = requests.post("" + ip + "/atma_Updateattachment", params=params, data=datas, headers=headers,
                                verify=False)
           response = resp.content.decode("utf-8")
           return HttpResponse(response)
   if request.POST['Group'] == "Document_Updatenofile":
       if request.method == 'POST':

           grp = request.POST['Group']
           action = request.POST['Action']
           typ = request.POST['Type']
           data = {"Documents_Gid": request.POST['Documents_Gid'],
                   "Documents_Docgroupgid": request.POST['Documents_Docgroupgid'],
                  "Description": request.POST['Description'],
                   "File_Name": request.POST['File_Name'],
                   "File_Path": request.POST['File_Path'],
                   "Update_By": request.session['Emp_gid'],
                   }
           datas = json.dumps(data)
           params = {'Group': "" + grp + "", 'Action': "" + action + "", 'Type': "" + typ + ""}
           token = jwt.token(request)
           headers = {"content-type": "application/json", "Authorization": "" + token + ""}
           resp = requests.post("" + ip + "/atma_Updateattachment", params=params, data=datas, headers=headers,
                                verify=False)
           response = resp.content.decode("utf-8")
           return HttpResponse(response)
   return render()

# commented by Ramesh,viki  May 10 - 2020 - VAPT - no template
# def atma_taxviewpage(request):
#     utl.check_authorization(request)
#     return render(request,'atma_taxviewpage.html')

def atma_tax_details(request):
    utl.check_pointaccess(request)
    return render(request,'atma_tax_details.html')

def atma_ProductCatSubCat_get(request):
  utl.check_authorization(request)
  if request.method == 'POST':
      jsondata = json.loads(request.body.decode('utf-8'))
      if (jsondata.get('Group')) == 'Activity_Group':
          grp = jsondata.get('Group')
          typ = jsondata.get('Type')
          data = json.dumps(jsondata.get('data'))
          params = {'Group': "" + grp + "", 'Type': "" + typ + ""}
          token = jwt.token(request)
          headers = {"content-type": "application/json", "Authorization": "" + token + ""}
          datas = json.dumps(jsondata.get('data'))
          resp = requests.post("" + ip + "/atma_ProductCatSubCat_getAPI", params=params, data=datas, headers=headers, verify=False)
          response = resp.content.decode("utf-8")
          return HttpResponse(response)


def atma_activity_get(request):
  utl.check_authorization(request)
  if request.method == 'POST':
      jsondata = json.loads(request.body.decode('utf-8'))
      if (jsondata.get('Group')) == 'Activity_Group':
          grp = jsondata.get('Group')
          typ = jsondata.get('Type')
          data = json.dumps(jsondata.get('data'))
          params = {'Group': "" + grp + "", 'Type': "" + typ + ""}
          token = jwt.token(request)
          headers = {"content-type": "application/json", "Authorization": "" + token + ""}
          datas = json.dumps(jsondata.get('data'))
          resp = requests.post("" + ip + "/atma_Activityget", params=params, data=datas, headers=headers, verify=False)
          response = resp.content.decode("utf-8")
          return HttpResponse(response)

def atma_activityaddedit(request):
  utl.check_authorization(request)
  if request.method == 'POST':
      jsondata = json.loads(request.body.decode('utf-8'))
      if (jsondata.get('Group')) == 'Activity_ADD':
          grp = jsondata.get('Group')
          action=jsondata.get('Action')
          typ = jsondata.get('Type')
          data = json.dumps(jsondata.get('data').get('Params'))
          dataw = json.dumps(jsondata.get('data').get('Classification'))
          params = {'Group': "" + grp + "", 'Action': "" + action + "", 'Type': "" + typ+ ""}
          token = jwt.token(request)
          headers = {"content-type": "application/json", "Authorization": "" + token + ""}
          datas = json.dumps(jsondata.get('data'))
          resp = requests.post("" + ip + "/atma_ActivitySet_APIurl", params=params, data=datas, headers=headers, verify=False)
          response = resp.content.decode("utf-8")
          return HttpResponse(response)
      if (jsondata.get('Group')) == 'Activity_UPDATE':
          grp = jsondata.get('Group')
          action = jsondata.get('Action')
          typ = jsondata.get('Type')
          data = json.dumps(jsondata.get('data').get('Params'))
          dataw = json.dumps(jsondata.get('data').get('Classification'))
          params = {'Group': "" + grp + "", 'Action': "" + action + "", 'Type': "" + typ + ""}
          token = jwt.token(request)
          headers = {"content-type": "application/json", "Authorization": "" + token + ""}
          datas = json.dumps(jsondata.get('data'))
          resp = requests.post("" + ip + "/atma_ActivitySet_APIurl", params=params, data=datas, headers=headers, verify=False)
          response = resp.content.decode("utf-8")
          return HttpResponse(response)

# Start Profile page...
def atma_profilepage(request):
    utl.check_pointaccess(request)
    return render(request,'atma_profilepage.html')
def atma_Productdetails(request):
    utl.check_pointaccess(request)
    return render(request,'atma_Productdetails.html')

def atma_Branchdetails(request):
    utl.check_pointaccess(request)
    return render(request,'atma_Branchdetails.html')

def atma_Clientdetails(request):
    utl.check_pointaccess(request)
    return render(request,'atma_Clientdetails.html')

def atma_Contractdetails(request):
    utl.check_pointaccess(request)
    return render(request,'atma_Contractdetails.html')

def atma_SetClientdetails(request):
    utl.check_authorization(request)
    if request.method == 'POST':
        jsondata = json.loads(request.body.decode('utf-8'))
        if (jsondata.get('Group')) == 'ClientDetails_ADD':
            grp = jsondata.get('Group')
            action = jsondata.get('Action')
            typ = jsondata.get('Type')
            data = json.dumps(jsondata.get('data').get('Params'))
            dataw = json.dumps(jsondata.get('data').get('Classification'))
            token = jwt.token(request)
            params = {'Group': "" + grp + "", 'Action': "" + action + "", 'Type': "" + typ + ""}
            headers = {"content-type": "application/json", "Authorization": "" + token + ""}
            datas = json.dumps(jsondata.get('data'))
            resp = requests.post("" + ip + "/atma_clientdetails_api", params=params, data=datas, headers=headers,
                                 verify=False)
            response = resp.content.decode("utf-8")
            return HttpResponse(response)
        if (jsondata.get('Group')) == 'ClientDetails_GET':
            grp = jsondata.get('Group')
            action = jsondata.get('Action')
            typ = jsondata.get('Type')
            data = json.dumps(jsondata.get('data').get('Params'))
            dataw = json.dumps(jsondata.get('data').get('Classification'))
            params = {'Group': "" + grp + "", 'Action': "" + action + "", 'Type': "" + typ + ""}
            token = jwt.token(request)
            headers = {"content-type": "application/json", "Authorization": "" + token + ""}
            datas = json.dumps(jsondata.get('data'))
            resp = requests.post("" + ip + "/atma_clientdetails_api", params=params, data=datas, headers=headers,
                                 verify=False)
            response = resp.content.decode("utf-8")
            return HttpResponse(response)
        if (jsondata.get('Group')) == 'ClientDetails_Update':
            grp = jsondata.get('Group')
            action = jsondata.get('Action')
            typ = jsondata.get('Type')
            data = json.dumps(jsondata.get('data').get('Params'))
            dataw = json.dumps(jsondata.get('data').get('Classification'))
            token = jwt.token(request)
            params = {'Group': "" + grp + "", 'Action': "" + action + "", 'Type': "" + typ + ""}
            headers = {"content-type": "application/json", "Authorization": "" + token + ""}
            datas = json.dumps(jsondata.get('data'))
            resp = requests.post("" + ip + "/atma_clientdetails_api", params=params, data=datas, headers=headers,
                                 verify=False)
            response = resp.content.decode("utf-8")
            return HttpResponse(response)

def atma_SetContractdetails(request):
    utl.check_authorization(request)
    if request.method == 'POST':
        jsondata = json.loads(request.body.decode('utf-8'))
        if (jsondata.get('Group')) == 'ContractDetails_SET':
            grp = jsondata.get('Group')
            action = jsondata.get('Action')
            typ = jsondata.get('Type')
            data =jsondata.get('data')
            common.main_fun(data)
            dataw = json.dumps(jsondata.get('data').get('Classification'))
            params = {'Group': "" + grp + "", 'Action': "" + action + "", 'Type': "" + typ + ""}
            token = jwt.token(request)
            headers = {"content-type": "application/json", "Authorization": "" + token + ""}
            datas = json.dumps(jsondata.get('data'))
            resp = requests.post("" + ip + "/atma_contractdetails_api", params=params, data=datas, headers=headers,
                                 verify=False)
            response = resp.content.decode("utf-8")
            return HttpResponse(response)
        if (jsondata.get('Group')) == 'ContractDetails_GET':
            grp = jsondata.get('Group')
            action = jsondata.get('Action')
            typ = jsondata.get('Type')
            data = json.dumps(jsondata.get('data').get('Params'))
            dataw = json.dumps(jsondata.get('data').get('Classification'))
            params = {'Group': "" + grp + "", 'Action': "" + action + "", 'Type': "" + typ + ""}
            token = jwt.token(request)
            headers = {"content-type": "application/json", "Authorization": "" + token + ""}
            datas = json.dumps(jsondata.get('data'))
            resp = requests.post("" + ip + "/atma_contractdetails_api", params=params, data=datas, headers=headers,
                                 verify=False)
            response = resp.content.decode("utf-8")
            return HttpResponse(response)

        if (jsondata.get('Group')) == 'ContractDetails_Update':
            grp = jsondata.get('Group')
            action = jsondata.get('Action')
            typ = jsondata.get('Type')
            data = json.dumps(jsondata.get('data').get('Params'))
            dataw = json.dumps(jsondata.get('data').get('Classification'))
            params = {'Group': "" + grp + "", 'Action': "" + action + "", 'Type': "" + typ + ""}
            token = jwt.token(request)
            headers = {"content-type": "application/json", "Authorization": "" + token + ""}
            datas = json.dumps(jsondata.get('data'))
            resp = requests.post("" + ip + "/atma_contractdetails_api", params=params, data=datas, headers=headers,
                                 verify=False)
            response = resp.content.decode("utf-8")
            return HttpResponse(response)

def atma_SetBranchdetails(request):
    utl.check_authorization(request)
    if request.method == 'POST':
        jsondata = json.loads(request.body.decode('utf-8'))
        if (jsondata.get('Group')) == 'BranchDetails_Set':
            grp = jsondata.get('Group')
            action = jsondata.get('Action')
            typ = jsondata.get('Type')
            data = json.dumps(jsondata.get('data').get('Params'))
            dataw = json.dumps(jsondata.get('data').get('Classification'))
            params = {'Group': "" + grp + "", 'Action': "" + action + "", 'Type': "" + typ + ""}
            token = jwt.token(request)
            headers = {"content-type": "application/json", "Authorization": "" + token + ""}
            datas = json.dumps(jsondata.get('data'))
            resp = requests.post("" + ip + "/atma_branchdetails_api", params=params, data=datas, headers=headers,
                                 verify=False)
            response = resp.content.decode("utf-8")
            return HttpResponse(response)

        if (jsondata.get('Group')) == 'BranchDetails_GET':
            grp = jsondata.get('Group')
            action = jsondata.get('Action')
            typ = jsondata.get('Type')
            data = json.dumps(jsondata.get('data').get('Params'))
            dataw = json.dumps(jsondata.get('data').get('Classification'))
            params = {'Group': "" + grp + "", 'Action': "" + action + "", 'Type': "" + typ + ""}
            token = jwt.token(request)
            headers = {"content-type": "application/json", "Authorization": "" + token + ""}
            datas = json.dumps(jsondata.get('data'))
            resp = requests.post("" + ip + "/atma_branchdetails_api", params=params, data=datas, headers=headers,
                                 verify=False)
            response = resp.content.decode("utf-8")
            return HttpResponse(response)

        if (jsondata.get('Group')) == 'BranchDetails_Update':
            grp = jsondata.get('Group')
            action = jsondata.get('Action')
            typ = jsondata.get('Type')
            data = json.dumps(jsondata.get('data').get('Params'))
            dataw = json.dumps(jsondata.get('data').get('Classification'))
            params = {'Group': "" + grp + "", 'Action': "" + action + "", 'Type': "" + typ + ""}
            token = jwt.token(request)
            headers = {"content-type": "application/json", "Authorization": "" + token + ""}
            datas = json.dumps(jsondata.get('data'))
            resp = requests.post("" + ip + "/atma_branchdetails_api", params=params, data=datas, headers=headers,
                                 verify=False)
            response = resp.content.decode("utf-8")
            return HttpResponse(response)


def atma_BasicProfilDetails(request):
    utl.check_pointaccess(request)
    return render(request,'atma_BasicProfilDetails.html')

def atma_Setbasicprofildedetails(request):
    utl.check_authorization(request)
    if request.method == 'POST':
        jsondata = json.loads(request.body.decode('utf-8'))
        if (jsondata.get('Group')) == 'BasicProfile_Set':
            grp = jsondata.get('Group')
            action = jsondata.get('Action')
            typ = jsondata.get('Type')
            data = jsondata.get('data')
            dataw = json.dumps(jsondata.get('data').get('Classification'))
            params = {'Group': "" + grp + "", 'Action': "" + action + "", 'Type': "" + typ + ""}
            token = jwt.token(request)
            headers = {"content-type": "application/json", "Authorization": "" + token + ""}
            common.main_fun(data)
            datas = json.dumps(jsondata.get('data'))
            resp = requests.post("" + ip + "/atma_basicprofiledetails_api", params=params, data=datas, headers=headers,
                                 verify=False)
            response = resp.content.decode("utf-8")
            return HttpResponse(response)
        if (jsondata.get('Group')) == 'Partnerprofile_Get':
            grp = jsondata.get('Group')
            action = jsondata.get('Action')
            typ = jsondata.get('Type')
            data = json.dumps(jsondata.get('data').get('Params'))
            dataw = json.dumps(jsondata.get('data').get('Classification'))
            params = {'Group': "" + grp + "", 'Action': "" + action + "", 'Type': "" + typ + ""}
            token = jwt.token(request)
            headers = {"content-type": "application/json", "Authorization": "" + token + ""}
            datas = json.dumps(jsondata.get('data'))
            resp = requests.post("" + ip + "/atma_basicprofiledetails_api", params=params, data=datas, headers=headers,
                                 verify=False)
            response = resp.content.decode("utf-8")
            return HttpResponse(response)

def atma_PartnerCheckerPage(request):
    utl.check_authorization(request)
    return render(request,'atma_PartnerCheckerPage.html')

def atma_PartnerCheckerApprovalPage(request):
    utl.check_authorization(request)
    return render(request,'atma_PartnerCheckerApprovalPage.html')

def atma_CheckerDetails(request):
    utl.check_authorization(request)
    if request.method == 'POST':
        jsondata = json.loads(request.body.decode('utf-8'))
        if (jsondata.get('Group')) == 'Checker_Get':
            grp = jsondata.get('Group')
            action = jsondata.get('Action')
            typ = jsondata.get('Type')
            data = json.dumps(jsondata.get('data').get('Params'))
            dataw = json.dumps(jsondata.get('data').get('Classification'))
            params = {'Group': "" + grp + "", 'Action': "" + action + "", 'Type': "" + typ + ""}
            token = jwt.token(request)
            headers = {"content-type": "application/json", "Authorization": "" + token + ""}
            datas = json.dumps(jsondata.get('data'))
            resp = requests.post("" + ip + "/atma_getcheckerdetails_api", params=params, data=datas, headers=headers,
                                 verify=False)
            response = resp.content.decode("utf-8")
            return HttpResponse(response)
        if (jsondata.get('Group')) == 'Checker_Status':
            grp = jsondata.get('Group')
            action = jsondata.get('Action')
            typ = jsondata.get('Type')
            data = json.dumps(jsondata.get('data').get('Params'))
            dataw = json.dumps(jsondata.get('data').get('Classification'))
            token = jwt.token(request)
            params = {'Group': "" + grp + "", 'Action': "" + action + "", 'Type': "" + typ + ""}
            headers = {"content-type": "application/json", "Authorization": "" + token + ""}
            datas = json.dumps(jsondata.get('data'))
            resp = requests.post("" + ip + "/atma_getcheckerdetails_api", params=params, data=datas, headers=headers,
                                 verify=False)
            response = resp.content.decode("utf-8")
            return HttpResponse(response)

def prmakerset(request):
    utl.check_authorization(request)
    if request.method == 'POST':
        jsondata = json.loads(request.body.decode('utf-8'))
        if (jsondata.get('Group')) == 'PRMAKER Details':
            grp = jsondata.get('Group')
            action = jsondata.get('Action')
            typ = jsondata.get('Group')
            data = json.dumps(jsondata.get('data').get('Params'))
            dataw = json.dumps(jsondata.get('data').get('Classification'))
            params = {'Group': "" + grp + "", 'Action': "" + action + "", 'Type': "" + typ + ""}
            token = jwt.token(request)
            headers = {"content-type": "application/json", "Authorization": "" + token + ""}
            datas = json.dumps(jsondata.get('data'))
            resp = requests.post("" + ip + "/Prmaker_Setapi", params=params, data=datas, headers=headers,
                                 verify=False)
            response = resp.content.decode("utf-8")
            return HttpResponse(response)

def prmaker_get(request):
   utl.check_authorization(request)
   if request.method == 'POST':
       jsondata = json.loads(request.body.decode('utf-8'))
       if (jsondata.get('Group')) == 'PRMAKER Details':
           grp = jsondata.get('Group')
           typ = jsondata.get('Type')
           data = json.dumps(jsondata.get('data'))
           params = {'Group': "" + grp + "", 'Type': "" + typ + ""}
           token = jwt.token(request)
           headers = {"content-type": "application/json", "Authorization": "" + token + ""}
           token = jwt.token(request)
           datas = json.dumps(jsondata.get('data'))
           resp = requests.post("" + ip + "/PRMAKERapi", params=params, data=datas, headers=headers, verify=False)
           response = resp.content.decode("utf-8")
           return HttpResponse(response)
       if (jsondata.get('Group')) == 'GetProduct_Details':
           grp = jsondata.get('Group')
           typ = jsondata.get('Action')
           data = json.dumps(jsondata.get('data'))
           params = {'Group': "" + grp + "", 'Action': "" + typ + ""}
           token = jwt.token(request)
           headers = {"content-type": "application/json", "Authorization": "" + token + ""}
           token = jwt.token(request)
           datas = json.dumps(jsondata.get('data'))
           resp = requests.post("" + ip + "/PRMAKERapi", params=params, data=datas, headers=headers, verify=False)
           response = resp.content.decode("utf-8")
           return HttpResponse(response)

def AtmaPartnerDeactivationRequest(request):
    utl.check_authorization(request)
    return render(request, "atma_partnerdeactivation_request.html")

def AtmaPartnerActivationRequest(request):
    utl.check_authorization(request)
    return render(request, "atma_partneractivation_request.html")

def AtmaPartnerTerminationRequest(request):
    utl.check_authorization(request)
    return render(request, "atma_partnertermination_request.html")

def partdisapproval_get(request):
  utl.check_authorization(request)
  if request.method == 'POST':
      jsondata = json.loads(request.body.decode('utf-8'))
      if (jsondata.get('Group')) == 'Partner Inactivate':
          grp = jsondata.get('Group')
          typ = jsondata.get('Type')
          data = json.dumps(jsondata.get('data'))
          params = {'Group': "" + grp + "", 'Type': "" + typ + ""}
          token = jwt.token(request)
          headers = {"content-type": "application/json", "Authorization": "" + token + ""}
          datas = json.dumps(jsondata.get('data'))
          resp = requests.post("" + ip + "/Partnerdisapproval", params=params, data=datas, headers=headers, verify=False)
          response = resp.content.decode("utf-8")
          return HttpResponse(response)

def atma_profileproduct_get(request):
   utl.check_authorization(request)
   if request.method == 'POST':
       jsondata = json.loads(request.body.decode('utf-8'))
       if (jsondata.get('Group')) == 'Partner Product':
           grp = jsondata.get('Group')
           typ = jsondata.get('Type')
           data = json.dumps(jsondata.get('data'))
           params = {'Group': "" + grp + "", 'Type': "" + typ + ""}
           token = jwt.token(request)
           headers = {"content-type": "application/json", "Authorization": "" + token + ""}
           datas = json.dumps(jsondata.get('data'))
           resp = requests.post("" + ip + "/atma_profileproduct_getapi", params=params, data=datas, headers=headers, verify=False)
           response = resp.content.decode("utf-8")
           return HttpResponse(response)

def atma_profileproduct_set(request):
   utl.check_authorization(request)
   if request.method == 'POST':
       jsondata = json.loads(request.body.decode('utf-8'))
       if (jsondata.get('Group')) == 'Partner Product':
           grp = jsondata.get('Group')
           action=jsondata.get('Action')
           typ = jsondata.get('Type')
           data =jsondata.get('data')
           #common.main_fun(data) set
           dataw = json.dumps(jsondata.get('data').get('Classification'))
           params = {'Group': "" + grp + "", 'Action': "" + action + "", 'Type': "" + typ+ ""}
           token = jwt.token(request)
           headers = {"content-type": "application/json", "Authorization": "" + token + ""}
           datas = json.dumps(jsondata.get('data'))
           resp = requests.post("" + ip + "/atma_profileproduct_setapi", params=params, data=datas, headers=headers, verify=False)
           response = resp.content.decode("utf-8")
           return HttpResponse(response)

def partnerdeactivate_set(request):
   utl.check_authorization(request)
   if request.method == 'POST':
       jsondata = json.loads(request.body.decode('utf-8'))
       if (jsondata.get('Group')) == 'Partner Inactive':
           grp = jsondata.get('Group')
           action=jsondata.get('Action')
           typ = jsondata.get('Type')
           data = json.dumps(jsondata.get('data').get('Params'))
           dataw = json.dumps(jsondata.get('data').get('Classification'))
           params = {'Group': "" + grp + "", 'Action': "" + action + "", 'Type': "" + typ+ ""}
           token = jwt.token(request)
           headers = {"content-type": "application/json", "Authorization": "" + token + ""}
           datas = json.dumps(jsondata.get('data'))
           resp = requests.post("" + ip + "/PartnerdeactivateSet_api", params=params, data=datas, headers=headers, verify=False)
           response = resp.content.decode("utf-8")
           return HttpResponse(response)

def partapproval_get(request):
  utl.check_authorization(request)
  if request.method == 'POST':
      jsondata = json.loads(request.body.decode('utf-8'))
      if (jsondata.get('Group')) == 'Partner Activate':
          grp = jsondata.get('Group')
          typ = jsondata.get('Type')
          data = json.dumps(jsondata.get('data'))
          params = {'Group': "" + grp + "", 'Type': "" + typ + ""}
          token = jwt.token(request)
          headers = {"content-type": "application/json", "Authorization": "" + token + ""}
          datas = json.dumps(jsondata.get('data'))
          resp = requests.post("" + ip + "/Partnerapproval", params=params, data=datas, headers=headers, verify=False)
          response = resp.content.decode("utf-8")
          return HttpResponse(response)

def atma_Approval_Summary_Page(request):
    utl.check_authorization(request)
    return render(request,'atma_Approval_Summary_Page.html')

def atma_Approval_ViewDetails_Page(request):
    utl.check_authorization(request)
    return render(request,'atma_Approval_ViewDetails_Page.html')

def atma_Approval_Taxdetails_Page(request):
    utl.check_pointaccess(request)
    return render(request,'atma_Approval_Taxdetails_Page.html')

def atma_Approval_Paymentdetails_Page(request):
    utl.check_pointaccess(request)
    return render(request,'atma_Approval_Paymentdetails_Page.html')

def atma_Approval_Attachmentdetails_Page(request):
    utl.check_pointaccess(request)
    return render(request,'atma_Approval_Attachmentdetails_Page.html')

def atma_Approval_ProfileBasic_Page(request):
    utl.check_pointaccess(request)
    return render(request,'atma_Approval_ProfileBasic_Page.html')

def atma_Approval_ProfileBranch_Page(request):
    utl.check_pointaccess(request)
    return render(request,'atma_Approval_ProfileBranch_Page.html')

def atma_Approval_ProfileClient_Page(request):
    utl.check_pointaccess(request)
    return render(request,'atma_Approval_ProfileClient_Page.html')

def atma_Approval_ProfileContract_Page(request):
    utl.check_pointaccess(request)
    return render(request,'atma_Approval_ProfileContract_Page.html')

def atma_Approval_ActivityDetails_Page(request):
    utl.check_pointaccess(request)
    return render(request,'atma_Approval_Activity.html')

def atma_Approval_ActivityDetails_Summary(request):
    utl.check_pointaccess(request)
    return render(request,'atma_Approval_ActivityDetails_Summary.html')

def atma_Approval_Catalogcreation(request):
    utl.check_pointaccess(request)
    return render(request,'atma_Approval_Catalogcreation.html')

def atma_Approval_ProfileProduct(request):
    utl.check_pointaccess(request)
    return render(request,'atma_Approval_ProfileProduct.html')

def atma_Approval_Stages(request):
    utl.check_authorization(request)
    if request.method == 'POST':
        jsondata = json.loads(request.body.decode('utf-8'))
        if (jsondata.get('Group')) == 'RM_To_VMU_Update':
            grp = jsondata.get('Group')
            action = jsondata.get('Action')
            typ = jsondata.get('Group')
            data = json.dumps(jsondata.get('data').get('Params'))
            dataw = json.dumps(jsondata.get('data').get('Classification'))
            params = {'Group': "" + grp + "", 'Action': "" + action + "", 'Type': "" + typ + ""}
            token = jwt.token(request)
            headers = {"content-type": "application/json", "Authorization": "" + token + ""}
            datas = json.dumps(jsondata.get('data'))
            resp = requests.post("" + ip + "/approval_stagesapi", params=params, data=datas, headers=headers,
                                 verify=False)
            response = resp.content.decode("utf-8")
            return HttpResponse(response)
        if (jsondata.get('Group')) == 'APPROVED_GROUP':
            grp = jsondata.get('Group')
            action = jsondata.get('Action')
            typ = jsondata.get('Group')
            data = json.dumps(jsondata.get('data').get('Params'))
            dataw = json.dumps(jsondata.get('data').get('Classification'))
            params = {'Group': "" + grp + "", 'Action': "" + action + "", 'Type': "" + typ + ""}
            token = jwt.token(request)
            headers = {"content-type": "application/json", "Authorization": "" + token + ""}
            datas = json.dumps(jsondata.get('data'))
            resp = requests.post("" + ip + "/approval_stagesapi", params=params, data=datas, headers=headers,
                                 verify=False)
            response = resp.content.decode("utf-8")
            return HttpResponse(response)


def atma_Approval_Request_Change(request):
    utl.check_authorization(request)
    return render(request,'atma_ApprovedRequest_Change.html')

def atma_ApprovedPartner_Get(request):
    utl.check_authorization(request)
    if request.method == 'POST':
        jsondata = json.loads(request.body.decode('utf-8'))
        if (jsondata.get('Group')) == 'Partner_Approval_Get':
            grp = jsondata.get('Group')
            action = jsondata.get('Action')
            typ = jsondata.get('Group')
            data = json.dumps(jsondata.get('data').get('Params'))
            dataw = json.dumps(jsondata.get('data').get('Classification'))
            params = {'Group': "" + grp + "", 'Action': "" + action + "", 'Type': "" + typ + ""}
            token = jwt.token(request)
            headers = {"content-type": "application/json", "Authorization": "" + token + ""}
            datas = json.dumps(jsondata.get('data'))
            resp = requests.post("" + ip + "/approval_paartnergetapi", params=params, data=datas, headers=headers,
                                 verify=False)
            response = resp.content.decode("utf-8")
            return HttpResponse(response)

        if (jsondata.get('Group')) == 'Partner_ChangeRequest':
            grp = jsondata.get('Group')
            action = jsondata.get('Action')
            typ = jsondata.get('Group')
            data = json.dumps(jsondata.get('data').get('Params'))
            dataw = json.dumps(jsondata.get('data').get('Classification'))
            params = {'Group': "" + grp + "", 'Action': "" + action + "", 'Type': "" + typ + ""}
            token = jwt.token(request)
            headers = {"content-type": "application/json", "Authorization": "" + token + ""}
            datas = json.dumps(jsondata.get('data'))
            resp = requests.post("" + ip + "/approval_paartnergetapi", params=params, data=datas, headers=headers,
                                 verify=False)
            response = resp.content.decode("utf-8")
            return HttpResponse(response)

        elif (jsondata.get('Params').get('Group')) == 'APPROVER_TO_REQUEST':
            group = jsondata.get('Params').get('Group')
            action = jsondata.get('Params').get('Action')
            data = json.dumps(jsondata.get('data'))
            params = {'Group': "" + group + "", 'Action': "" + action + ""}
            token = jwt.token(request)
            headers = {"content-type": "application/json", "Authorization": "" + token + ""}
            datas = json.dumps(jsondata)
            resp = requests.post("" + ip + "/approval_paartnergetapi", params=params, data=datas, headers=headers,
                                 verify=False)
            return HttpResponse(resp)

        elif (jsondata.get('Params').get('Group')) == 'VIEW_TO_CANCEL':
            group = jsondata.get('Params').get('Group')
            action = jsondata.get('Params').get('Action')
            data = json.dumps(jsondata.get('data'))
            params = {'Group': "" + group + "", 'Action': "" + action + ""}
            token = jwt.token(request)
            headers = {"content-type": "application/json", "Authorization": "" + token + ""}
            datas = json.dumps(jsondata)
            resp = requests.post("" + ip + "/approval_paartnergetapi", params=params, data=datas, headers=headers,
                                 verify=False)
            return HttpResponse(resp)

        if (jsondata.get('Params').get('Group')) == 'Checkpan_details':
            group = jsondata.get('Params').get('Checkpan_details')
            pannumber = jsondata.get('Params').get('Pan_number')
            #pannumber = "AAACC1287E"
            generated_token_data = master_views.master_sync_("GET", "get_data", 1)
            new_token = generated_token_data.get("DATA")[0].get("clienttoken_name")

            params = {}
            ip = common.clientapi()
            ip1="" + ip + "/next/v1/mw/pan/"+pannumber
            headers = {"content-type": "application/json", "Authorization": "Bearer " + new_token + ""}
            datas = json.dumps(jsondata)
            resp = requests.get( ip1,  headers=headers,
                                 verify=False)
            value=resp.status_code
            if(value==200):
                return HttpResponse({"SUCCESS"})
            else:
                return HttpResponse({"FAILD"})
        if (jsondata.get('Params').get('Group')) == 'IFSC_GROUP':
            group = jsondata.get('Params').get('Group')
            action = jsondata.get('Params').get('Action')
            datas = json.dumps(jsondata.get("Params").get("Filter"))
            generated_token_data = master_views.master_sync_("GET", "get_data", 1)
            new_token = generated_token_data.get("DATA")[0].get("clienttoken_name")
            ip = common.clientapi()
            ip_new= "" + ip + "/next/v1/mw/ifsc-check"
            headers = {"content-type": "application/json", "Authorization": "Bearer " + new_token + ""}
            resp = requests.post( ip_new , data=datas, headers=headers,
                                 verify=False)
            a=json.loads(resp.text)
            b=a["out_msg"]
            #c=a["out_msg"]["Branch_Name"]

            return JsonResponse(b)

        if (jsondata.get('Params').get('Group')) == 'CheckGst_details':
            #group = jsondata.get('Params').get('Checkpan_details')
            Gstnumber = jsondata.get('Params').get('Gst_number')
            #pannumber = "AAACC1287E"
            generated_token_data = master_views.master_sync_("GET", "get_data", 1)
            new_token = generated_token_data.get("DATA")[0].get("clienttoken_name")
            # if (new_token == " " or new_token == None):
            #     token_status = 0
            #
            # if token_status == 1:
            #     print("next")
            params = {}
            ip = common.clientapi()
            ip1="" + ip + "/next/v1/gst/searchtaxpayer?gstin="+Gstnumber+"&action=TP"
            headers = {"content-type": "application/json", "Authorization": "Bearer " + new_token + ""}
            datas = json.dumps(jsondata)
            resp = requests.get( ip1,  headers=headers, verify=False)

            value=resp.status_code
            if(value==200):
                return HttpResponse({"SUCCESS"})
            else:
                return HttpResponse({"FAILD"})
def atma_changerequest_summarypage(request):
    utl.check_authorization(request)
    return render(request,'atma_changerequest_summarypage.html')

def Query_Page(request):
    utl.check_authorization(request)
    return render(request, "Query_Page.html")

def Bankbranch_Add(request):
    utl.check_authorization(request)
    return render(request, "Bankbranch_Add.html")
def Bankbranch_summary(request):
    utl.check_authorization(request)
    return render(request, "Bankbranch_summary.html")

def Bankbranch_setdetails(request):
    utl.check_authorization(request)
    if request.method == 'POST':
        jsondata = json.loads(request.body.decode('utf-8'))
        if (jsondata.get('Params').get('Group')) == 'BanckBranch_Set':
            group = jsondata.get('Params').get('Group')
            action = jsondata.get('Params').get('Action')
            type = jsondata.get('Params').get('Type')
            subtype = jsondata.get('Params').get('SubType')
            Create_by1 = (jsondata.get('Params').get('Create_by'))
            Create_by = str(Create_by1)
            data = json.dumps(jsondata.get('data'))
            params = {'Group': "" + group + "", 'Action': "" + action + "",'type': "" + type + "",'subtype': "" + subtype + ""
                      ,'Create_by': "" + Create_by + ""}
            token = jwt.token(request)
            headers = {"content-type": "application/json", "Authorization": "" + token + ""}
            datas = json.dumps(jsondata)
            resp = requests.post("" + ip + "/Update_changerequest_API", params=params, data=datas, headers=headers,
                                 verify=False)
            return HttpResponse(resp)

        if (jsondata.get('Params').get('Group')) == 'Get_bankbranchdetails':
            group = jsondata.get('Params').get('Group')
            action = jsondata.get('Params').get('Action')
            type = jsondata.get('Params').get('Type')
            data = json.dumps(jsondata.get('data'))
            params = {'Group': "" + group + "", 'Action': "" + action + "",'type': "" + type + ""}
            token = jwt.token(request)
            headers = {"content-type": "application/json", "Authorization": "" + token + ""}
            datas = json.dumps(jsondata)
            resp = requests.post("" + ip + "/Update_changerequest_API", params=params, data=datas, headers=headers,
                                 verify=False)
            return HttpResponse(resp)
        if (jsondata.get('Params').get('Group')) == 'updatebankbranch':
            group = jsondata.get('Params').get('Group')
            action = jsondata.get('Params').get('Action')
            type = jsondata.get('Params').get('Type')
            subtype = jsondata.get('Params').get('SubType')
            Create_by1 = (jsondata.get('Params').get('Create_by'))
            Create_by = str(Create_by1)
            data = json.dumps(jsondata.get('data'))
            params = {'Group': "" + group + "", 'Action': "" + action + "",'type': "" + type + "",'subtype': "" + subtype + ""
                      ,'Create_by': "" + Create_by + ""}
            token = jwt.token(request)
            headers = {"content-type": "application/json", "Authorization": "" + token + ""}
            datas = json.dumps(jsondata)
            resp = requests.post("" + ip + "/Update_changerequest_API", params=params, data=datas, headers=headers,
                                 verify=False)
            return HttpResponse(resp)

        if (jsondata.get('Params').get('Group')) == 'Active_Inactive':
            group = jsondata.get('Params').get('Group')
            action = jsondata.get('Params').get('Action')
            type = jsondata.get('Params').get('Type')
            subtype = jsondata.get('Params').get('SubType')
            Create_by1 = (jsondata.get('Params').get('Create_by'))
            Create_by = str(Create_by1)
            data = json.dumps(jsondata.get('data'))
            params = {'Group': "" + group + "", 'Action': "" + action + "",'type': "" + type + "",'subtype': "" + subtype + ""
                      ,'Create_by': "" + Create_by + ""}
            token = jwt.token(request)
            headers = {"content-type": "application/json", "Authorization": "" + token + ""}
            datas = json.dumps(jsondata)
            resp = requests.post("" + ip + "/Update_changerequest_API", params=params, data=datas, headers=headers,
                                 verify=False)
            return HttpResponse(resp)
        if (jsondata.get('Params').get('Group')) == 'Get_masterbranchdetails':
            group = jsondata.get('Params').get('Group')
            action = jsondata.get('Params').get('Action')
            type = jsondata.get('Params').get('Type')
            data = json.dumps(jsondata.get('data'))
            params = {'Group': "" + group + "", 'Action': "" + action + "",'type': "" + type + ""}
            token = jwt.token(request)
            headers = {"content-type": "application/json", "Authorization": "" + token + ""}
            datas = json.dumps(jsondata)
            resp = requests.post("" + ip + "/Update_changerequest_API", params=params, data=datas, headers=headers,
                                 verify=False)
            return HttpResponse(resp)

        if (jsondata.get('Params').get('Group')) == 'updatebranchmaster':
            group = jsondata.get('Params').get('Group')
            action = jsondata.get('Params').get('Action')
            type = jsondata.get('Params').get('Type')
            subtype = jsondata.get('Params').get('SubType')
            Create_by1 = (jsondata.get('Params').get('Create_by'))
            Create_by = str(Create_by1)
            data = json.dumps(jsondata.get('data'))
            params = {'Group': "" + group + "", 'Action': "" + action + "",'type': "" + type + "",'subtype': "" + subtype + ""
                      ,'Create_by': "" + Create_by + ""}
            token = jwt.token(request)
            headers = {"content-type": "application/json", "Authorization": "" + token + ""}
            datas = json.dumps(jsondata)
            resp = requests.post("" + ip + "/Update_changerequest_API", params=params, data=datas, headers=headers,
                                 verify=False)
            return HttpResponse(resp)

def BankGL_Summary(request):
    utl.check_authorization(request)
    return render(request, "BankGL_Summary.html")
def BankGL_Edit(request):
    utl.check_authorization(request)
    return render(request, "BankGL_Edit.html")