import base64
import json

from django.shortcuts import render
import Bigflow.Core.models as common
import requests
from django.core.files.storage import default_storage
from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from Bigflow.API import views as commonview
from Bigflow.menuClass import utility as utl

import Bigflow.Core.jwt_file as jwt
ip = common.localip()



def PAR_Summary(request):
    utl.check_authorization(request)
    return render(request,'PAR_Summary.html')
def PAR_Add(request):
    utl.check_authorization(request)
    return render(request,'PAR_Add.html')
def PAR_Add_Set(request):
   if request.method == 'POST':
       jsondata = json.loads(request.body.decode('utf-8'))
       if (jsondata.get('Group')) == 'Add_Par':
           grp = jsondata.get('Group')
           typ = jsondata.get('Type')
           typ1 = jsondata.get('Create_By')
           typ2 = jsondata.get('Action')
           data = json.dumps(jsondata.get('data'))
           token = jwt.token(request)
           params = {'Group': "" + grp + "", 'Type': "" + typ + "", 'Create_By': "" + typ1 + "", 'Action': "" + typ2 + ""}
           headers = {"content-type": "application/json", "Authorization": "" + token + ""}
           datas = json.dumps(jsondata.get('data'))
           resp = requests.post("" + ip + "/PARSET_API", params=params, data=datas, headers=headers, verify=False)
           response = resp.content.decode("utf-8")
           return HttpResponse(response)
       if (jsondata.get('Group')) == 'Add_Mep':
           grp = jsondata.get('Group')
           typ = jsondata.get('Type')
           typ1 = jsondata.get('Create_By')
           typ2 = jsondata.get('Action')
           data = json.dumps(jsondata.get('Params'))
           token = jwt.token(request)
           params = {'Group': "" + grp + "", 'Type': "" + typ + "", 'Create_By': "" + typ1 + "", 'Action': "" + typ2 + ""}
           headers = {"content-type": "application/json", "Authorization": "" + token + ""}
           datas = json.dumps(jsondata.get('data'))
           resp = requests.post("" + ip + "/MEPSET_API", params=params, data=datas, headers=headers, verify=False)
           response = resp.content.decode("utf-8")
           return HttpResponse(response)
       if request.method == 'POST':
           jsondata = json.loads(request.body.decode('utf-8'))
           if (jsondata.get('Group')) == 'Add_Update':
               grp = jsondata.get('Group')
               typ = jsondata.get('Type')
               typ1 = jsondata.get('Create_By')
               typ2 = jsondata.get('Action')
               data = json.dumps(jsondata.get('data'))
               params = {'Group': "" + grp + "", 'Type': "" + typ + "", 'Create_By': "" + typ1 + "",
                         'Action': "" + typ2 + ""}
               token = jwt.token(request)
               headers = {"content-type": "application/json", "Authorization": "" + token + ""}
               datas = json.dumps(jsondata.get('data'))
               resp = requests.post("" + ip + "/PARSET_API", params=params, data=datas, headers=headers, verify=False)
               response = resp.content.decode("utf-8")
               return HttpResponse(response)
def Par_Get(request):
   if request.method == 'POST':
       jsondata = json.loads(request.body.decode('utf-8'))
       if (jsondata.get('Params').get('Group')) == 'PAR_GET':
           grp = jsondata.get('Params').get('Group')
           typ = jsondata.get('Params').get('Type')
           typ1 = jsondata.get('Params').get('Create_By')
           typ3 = json.dumps(jsondata.get('Params').get('Entity_gid'))
           typ2 = jsondata.get('Params').get('Action')
           data = json.dumps(jsondata.get('Params'))
           token = jwt.token(request)
           params = {'Group': "" + grp + "", 'Type': "" + typ + "", 'Create_By': "" + typ1 + "", 'Action': "" + typ2 + "", 'Entity_Gid':""+typ3+""}
           headers = {"content-type": "application/json", "Authorization": "" + token + ""}
           datas = json.dumps(jsondata.get('Params'))
           resp = requests.post("" + ip + "/PARGET_API", params=params, data=datas, headers=headers, verify=False)
           response = resp.content.decode("utf-8")
           return HttpResponse(response)
       if (jsondata.get('Params').get('Group')) == 'MEP_GET':
           grp = jsondata.get('Params').get('Group')
           typ = jsondata.get('Params').get('Type')
           typ1 = jsondata.get('Params').get('Create_By')
           typ3 = json.dumps(jsondata.get('Params').get('Entity_gid'))
           typ2 = jsondata.get('Params').get('Action')
           data = json.dumps(jsondata.get('Params'))
           token = jwt.token(request)
           params = {'Group': "" + grp + "", 'Type': "" + typ + "", 'Create_By': "" + typ1 + "", 'Action': "" + typ2 + "", 'Entity_Gid':""+typ3+""}
           headers = {"content-type": "application/json", "Authorization": "" + token + ""}
           datas = json.dumps(jsondata.get('Params'))
           resp = requests.post("" + ip + "/MEPGET_API", params=params, data=datas, headers=headers, verify=False)
           response = resp.content.decode("utf-8")
           return HttpResponse(response)

def Par_Checker(request):
    utl.check_authorization(request)
    return render(request, 'Par_Checker.html')

def Mep_Summary(request):
    utl.check_authorization(request)
    return render(request, 'Mep_Summary.html')

def Mep_Add(request):
    utl.check_authorization(request)
    return render(request, 'Mep_Add.html')

def Mep_Checker(request):
    utl.check_authorization(request)
    return render(request, 'Mep_Checker.html')

def imageconvert_par(request):
    utl.check_pointaccess(request)
    if request.method == 'POST' and request.FILES['file']:
            f = request.FILES['file']
            name = request.POST['name']
            data = base64.b64encode(f.read())
            print(data)
            base = name ,"+",data
            return HttpResponse(base)
            # base = {
            #     'name': name,
            #     'data': data,
            # }
            # return JsonResponse(base)
