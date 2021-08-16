from django.shortcuts import render
from Bigflow.Proofing.Model import mproofing
from django.http import JsonResponse
import json
from django.core.files.storage import default_storage
from django.http import HttpResponse
import pandas as pd
from django.conf import settings
from datetime import datetime
import Bigflow.Core.models as common
from django.core.files.base import ContentFile
import requests
import Bigflow.Core.jwt_file as jwt

ip = common.localip()
token = common.token()

# Create your views here.

def mainmaster(request):
    return render(request, "mainmaster.html")

def fileuploadmaster(request):
    return render(request, "Int_mst_fileupload.html")

def Entry_Get(request):
    try:
        if request.method == 'POST':
            obj_entry_get = mproofing.Proofing_model()
            jsondata = json.loads(request.body.decode('utf-8'))
            if jsondata.get('Group') == 'INTEGRITY_SUMMARY':
                obj_entry_get.group = jsondata.get('Group')
                obj_entry_get.Type = jsondata.get('Type')
                obj_entry_get.sub_type = jsondata.get('Sub_Type')
                obj_entry_get.filter_json = '{}'
                params = {'Group': "" + obj_entry_get.group + "", 'Type': "" + obj_entry_get.Type + "", 'Sub_Type': "" + obj_entry_get.sub_type + ""}
                headers = {"content-type": "application/json", "Authorization": "" + token + ""}
                datas = json.dumps(jsondata.get('data'))
                resp = requests.post("" + ip + "/integrity_upload", params=params, data=datas, headers=headers, verify=False)
                response = resp.content.decode("utf-8")
                return HttpResponse(response)
            elif jsondata.get('Group') == 'INTEGRITY_PUSHDATA':
                params = {'Group': "" + jsondata.get('Group') + "", 'Type': "" +jsondata.get('Type')+ "",
                          'Action': "" + jsondata.get('Action') + "",'Employee_Gid':request.session['Emp_gid']}
                headers = {"content-type": "application/json", "Authorization": "" + token + ""}
                datas = json.dumps(jsondata.get('data'))
                resp = requests.post("" + ip + "/integrity_upload", params=params, data=datas, headers=headers,
                                     verify=False)
                response = resp.content.decode("utf-8")
                return HttpResponse(response)
    except Exception as e:
        return JsonResponse(e, safe=False)


def excelgen1(request):
    if request.method == 'POST':
        try:
            if request.POST['Group'] == 'INTEGRITY_UPLOAD':
                current_month = datetime.now().strftime('%m')
                current_day = datetime.now().strftime('%d')
                current_year_full = datetime.now().strftime('%Y')
                save_path = str(settings.MEDIA_ROOT)+ '/INTEGRITY/'+str(current_year_full)+'/'+str(current_month)+'/'+str(current_day)+'/'+str(request.POST['name'])
                path = default_storage.save(str(save_path), request.FILES['file'])
                obj = mproofing.Proofing_model()
                obj.group = request.POST['Group']
                obj.action = request.POST['Action']
                obj.type = request.POST['Type']
                obj.empgid = request.POST['Employee_Gid']
                obj.filepath = path
                obj.name = request.POST['name']
                obj.employee_gid = json.dumps(request.session['Emp_gid'])
                obj.create_by = json.dumps(request.session['Emp_gid'])
                df = pd.read_excel(request.FILES['file'],skiprows=[0])
                gl_number = df['GL NUMBER'].astype(str)
                date = pd.to_datetime(df['DATE'], format='%Y%m%d')
                date = date.apply(lambda x: x.strftime('%Y-%m-%d'))
                desc = df['DESCRIPTION']
                inv_num = df['INVOICE NUMBER'].astype(str)
                amnt = df['AMOUNT'].astype(str)
                df = pd.DataFrame({'GL_NUMBER': gl_number, 'DATE': date, 'DESCRIPTION': desc, 'INVOICE_NUMBER': inv_num,
                     'AMOUNT': amnt})
                ff = df.to_dict('records')
                sd = {"params": {"DATA":{"exceldump_templateheadergid":request.POST['templ'],"exceldump_error":"1","exceldump_status":"1","INTRA":ff},
                                 "FILE": {
                    "FILE": {"File_Gid": "0", "File_Name": obj.name , "File_Path": obj.filepath}},
                                 "CLASSIFICATION": {"Entity_Gid": [request.session['Entity_gid']]}}}
                datas = json.dumps(sd)
                resp = requests.post(
                    "" + ip + "/integrity_upload?Group=" + obj.group + "&Action=" + obj.action + "&Type=" + obj.type + "&Employee_Gid=" + obj.employee_gid + "",
                    data=datas,
                    headers={"content-type": "application/json",
                             "Authorization": "Token 7111797114100105971106449505132"
                             }, verify=False)
                response = resp.content.decode("utf-8")
                return HttpResponse(response)
        except Exception as e:
            return JsonResponse(e, safe=False)


