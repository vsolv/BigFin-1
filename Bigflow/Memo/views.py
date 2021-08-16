import base64
import io
import json
import os
import time
from Bigflow.menuClass import utility as utl
import boto3
from datetime import datetime
from django.conf import settings

from django.shortcuts import render
import Bigflow.Core.models as common
import requests
from django.core.files.storage import default_storage
from django.shortcuts import render
from django.http import JsonResponse, HttpResponse, StreamingHttpResponse
from Bigflow.API import views as commonview
from Bigflow.menuClass import utility as utl
ip = common.localip()
token = common.token()
headers = {"content-type": "application/json", "Authorization": "" + token + ""}
s3 = boto3.resource('s3')
def Memo_Summary(request):
    utl.check_authorization(request)
    utl.check_pointaccess(request)
    return render(request,'Memo_Summary.html')

def Memo_addrequest(request):
    utl.check_authorization(request)
    if request.POST['Group']=="MemoRequest_Group":
        if request.method == 'POST' and request.FILES['file']:
            current_month = datetime.now().strftime('%m')
            current_day = datetime.now().strftime('%d')
            current_year_full = datetime.now().strftime('%Y')
            #save_path = + str(current_year_full) + '/' + str(current_month) + '/' + str(current_day) + '/' + str(request.POST['name'])
            #print(save_path)
            #path = default_storage.save(str(save_path), request.FILES['file'])
            file = str(request.FILES['file'])
            grp = request.POST['Group']
            action=request.POST['Action']
            typ = request.POST['Type']
            subtyp = request.POST['SubType']
            Entity_Gid = request.POST['Entity_Gid']
            Create_By = request.POST['Create_By']
            #File_Names=request.POST['File_Name']
            filename = str(request.FILES['file'])
            millis = int(round(time.time() * 1000))
            s1=str(millis)
            concat_filename = Create_By + "_"+s1+"_"+filename

            data = {"Request_Name": request.POST['Request_Name'],"Memo_Subcategory_Gid": request.POST['Memo_Subcategory_Gid'],

                    "File_Name":concat_filename ,"File_Path": "xcv", "Requesttran_Comments":request.POST['Comments'],
                    "Create_By": request.POST['Create_By'],"Entity_Gid":request.POST['Entity_Gid'],"Request_ion":request.POST['ION'],
                    "Tran_To": request.POST['Tran_to'],"Tran_CC":request.POST['Tran_cc'] ,"Request_Content":request.POST['Request_Content'] ,
            }

            #s3.Object('vysfin-assets-uat',File_Names).upload_file(request.FILES['file'])
            s3 = boto3.resource('s3')
            s3_obj = s3.Object(bucket_name='vysfin-assets-uat', key=concat_filename)
            s3_obj.put(Body=request.FILES['file'])

            s3_client = boto3.client('s3')
            #response = s3_client.upload_file(filename, 'vysfin-assets-uat', request.FILES['file'])
            #s3.Object('vysfin-assets-uat', File_Names).download_file('/home/vsolv/Desktop/'+File_Names)

            datas = json.dumps(data)

            params = {'Group': "" + grp + "", 'Action': "" + action + "", 'Type': "" + typ+ "",'SubType': "" + subtyp+ "",
                      'Entity_Gid': "" + Entity_Gid + "",'Create_By': "" + Create_By + "",}
            headers = {"content-type": "application/json", "Authorization": "" + token + ""}

            resp = requests.post("" + ip + "/Memo_Request_API", params=params, data=datas, headers=headers, verify=False)
            response = resp.content.decode("utf-8")

            return HttpResponse(response)
    if request.POST['Group']=="MemoRequestnofile_Group":

            grp = request.POST['Group']
            action=request.POST['Action']
            typ = request.POST['Type']
            subtyp = request.POST['SubType']
            Entity_Gid = request.POST['Entity_Gid']
            Create_By = request.POST['Create_By']
            Request_Content=request.POST['Request_Content']
            valid_json = Request_Content.replace("'", "'''")
            a=json.dumps(valid_json)

            data = {"Request_Name": request.POST['Request_Name'],"Memo_Subcategory_Gid": request.POST['Memo_Subcategory_Gid'],

                    "Requesttran_Comments":request.POST['Comments'],
                    "Create_By": request.POST['Create_By'],"Entity_Gid":request.POST['Entity_Gid'],"Request_ion":request.POST['ION'],
                    "Tran_To": request.POST['Tran_to'],"Tran_CC":request.POST['Tran_cc'] ,"Request_Content":Request_Content,
            }

            datas = json.dumps(data)

            params = {'Group': "" + grp + "", 'Action': "" + action + "", 'Type': "" + typ+ "",'SubType': "" + subtyp+ "",
                      'Entity_Gid': "" + Entity_Gid + "",'Create_By': "" + Create_By + "",}
            headers = {"content-type": "application/json", "Authorization": "" + token + ""}

            resp = requests.post("" + ip + "/Memo_Request_API", params=params, data=datas, headers=headers, verify=False)
            response = resp.content.decode("utf-8")

            return HttpResponse(response)

    if request.POST['Group']=="MemoRequest_Groupfileupdate":
        if request.method == 'POST' and request.FILES['file']:
            grp = request.POST['Group']
            action=request.POST['Action']
            typ = request.POST['Type']
            subtyp = request.POST['SubType']
            Entity_Gid = request.POST['Entity_Gid']
            Create_By = request.POST['Create_By']
            File_Names = request.POST['File_Name']
            filename = str(request.FILES['file'])
            millis = int(round(time.time() * 1000))
            s1 = str(millis)
            concat_filename = Create_By + "_" + s1 + "_" + filename

            data = {"Request_Name": request.POST['Request_Name'],"Memo_Subcategory_Gid": request.POST['Memo_Subcategory_Gid'],
                    "Approver_Gid": request.POST['Request_Approver_Gid'],"Request_Gid": request.POST['Request_Gid'],
                    "File_Name": concat_filename,"File_Path": "save_path", "Comments":request.POST['Comments'],
                    "Create_By": request.POST['Create_By'],"Entity_Gid":request.POST['Entity_Gid'],"Request_ION":request.POST['ION'],
            }
            s3 = boto3.resource('s3')
            s3_obj = s3.Object(bucket_name='vysfin-assets-uat', key=concat_filename)
            s3_obj.put(Body=request.FILES['file'])
            s3_client = boto3.client('s3')
            datas = json.dumps(data)

            params = {'Group': "" + grp + "", 'Action': "" + action + "", 'Type': "" + typ+ "",'SubType': "" + subtyp+ "",
                      'Entity_Gid': "" + Entity_Gid + "",'Create_By': "" + Create_By + "",}
            headers = {"content-type": "application/json", "Authorization": "" + token + ""}

            resp = requests.post("" + ip + "/Memo_Request_API", params=params, data=datas, headers=headers, verify=False)
            response = resp.content.decode("utf-8")
            return HttpResponse(response)
    if request.POST['Group']=="MemoRequest_Groupnofileupdate":
        if request.method == 'POST':
            grp = request.POST['Group']
            action=request.POST['Action']
            typ = request.POST['Type']
            subtyp = request.POST['SubType']
            Entity_Gid = request.POST['Entity_Gid']
            Create_By = request.POST['Create_By']

            data = {"Request_Name": request.POST['Request_Name'],"Subcategory_Gid": request.POST['Memo_Subcategory_Gid'],
                    "Approver_Gid": request.POST['Request_Approver_Gid'],"Request_Gid": request.POST['Request_Gid'],
                    "File_Name": request.POST['File_Name'], "Comments":request.POST['Comments'],
                    "Create_By": request.POST['Create_By'],"Entity_Gid":request.POST['Entity_Gid'],"Request_ION":request.POST['ION'],
            }

            datas = json.dumps(data)

            params = {'Group': "" + grp + "", 'Action': "" + action + "", 'Type': "" + typ+ "",'SubType': "" + subtyp+ "",
                      'Entity_Gid': "" + Entity_Gid + "",'Create_By': "" + Create_By + "",}
            headers = {"content-type": "application/json", "Authorization": "" + token + ""}

            resp = requests.post("" + ip + "/Memo_Request_API", params=params, data=datas, headers=headers, verify=False)
            response = resp.content.decode("utf-8")
            return HttpResponse(response)


def Memo_request_Get(request):
   utl.check_authorization(request)
   if request.method == 'POST':
       jsondata = json.loads(request.body.decode('utf-8'))
       if (jsondata.get('Params').get('Group')) == 'Memoget_Grp':
           grp = jsondata.get('Params').get('Group')
           typ = jsondata.get('Params').get('Type')
           typ1 = json.dumps(jsondata.get('Params').get('Create_By'))
           typ3 = json.dumps(jsondata.get('Params').get('Entity_gid'))
           typ2 = jsondata.get('Params').get('Action')
           data = json.dumps(jsondata.get('Params'))
           params = {'Group': "" + grp + "", 'Type': "" + typ + "", 'Create_By': "" + typ1 + "",
                     'Action': "" + typ2 + "", 'Entity_Gid': "" + typ3 + ""}
           headers = {"content-type": "application/json", "Authorization": "" + token + ""}
           datas = json.dumps(jsondata.get('Params'))
           resp = requests.post("" + ip + "/Memo_Request_GetAPI", params=params, data=datas, headers=headers,
                                verify=False)

           response = resp.content.decode("utf-8")
           return HttpResponse(response)
       if (jsondata.get('Params').get('Group'))=='Active_Inactive':
           Group=jsondata.get('Params').get('Group')
           Action=jsondata.get('Params').get('Action')
           Type=jsondata.get('Params').get('Type')
           Subtype=jsondata.get('Params').get('SubType')
           Create_by=str(jsondata.get('Params').get('Create_by'))
           data=json.dumps(jsondata.get('Params'))
           params = {'Group': "" + Group + "", 'Type': "" + Type + "", 'Create_By': "" + Create_by + "",
                     'Action': "" + Action + "", 'Subtype': "" + Subtype + ""}
           headers = {"content-type": "application/json", "Authorization": "" + token + ""}
           resp = requests.post("" + ip + "/Memo_Approvel_SetAPI", params=params, data=data, headers=headers,
                                verify=False)
           response = resp.content.decode("utf-8")
           return HttpResponse(response)
       if (jsondata.get('Params').get('Group'))=='Memotransation_Grp':
           Group=jsondata.get('Params').get('Group')
           Action=jsondata.get('Params').get('Action')
           Type=jsondata.get('Params').get('Type')
           Subtype=jsondata.get('Params').get('SubType')
           Create_by=str(jsondata.get('Params').get('Create_by'))
           data=json.dumps(jsondata.get('Params'))
           params = {'Group': "" + Group + "", 'Type': "" + Type + "",
                     'Action': "" + Action + ""}
           headers = {"content-type": "application/json", "Authorization": "" + token + ""}
           resp = requests.post("" + ip + "/Memo_Request_GetAPI", params=params, data=data, headers=headers,
                                verify=False)
           response = resp.content.decode("utf-8")
           return HttpResponse(response)
       if (jsondata.get('Params').get('Group'))=='Memotransationset_Grp':
           Group=jsondata.get('Params').get('Group')
           Action=jsondata.get('Params').get('Action')
           Type=jsondata.get('Params').get('Type')
           Subtype=jsondata.get('Params').get('SubType')
           Create_by=str(jsondata.get('Params').get('Create_By'))
           data=json.dumps(jsondata.get('Params'))
           params = {'Group': "" + Group + "", 'Type': "" + Type + "", 'Create_By': "" + Create_by + "",
                     'Action': "" + Action + "", 'Subtype': "" + Subtype + ""}
           headers = {"content-type": "application/json", "Authorization": "" + token + ""}
           resp = requests.post("" + ip + "/Memo_Approvel_SetAPI", params=params, data=data, headers=headers,
                                verify=False)
           response = resp.content.decode("utf-8")
           return HttpResponse(response)

def Memo_ApprovalSummary(request):
    utl.check_authorization(request)
    utl.check_pointaccess(request)
    return render(request,'Memo_ApprovalSummary.html')

def Memo_Approve(request):
    utl.check_authorization(request)
    utl.check_pointaccess(request)
    return render(request,'Memo_Approve.html')

def Memo_Approve_Set(request):
        utl.check_authorization(request)
        if request.POST['Group']=="MemoApprovelset_Group":
            if request.method == 'POST' and request.FILES['file']:
                current_month = datetime.now().strftime('%m')
                current_day = datetime.now().strftime('%d')
                current_year_full = datetime.now().strftime('%Y')
                save_path = str(settings.MEDIA_ROOT) + '/Memo_Documents/' + str(current_year_full) + '/' + str(current_month) + '/' + str(current_day) + '/' + str(request.POST['name'])
                #print(save_path)
                path = default_storage.save(str(save_path), request.FILES['file'])

                grp = request.POST['Group']
                action=request.POST['Action']
                typ = request.POST['Type']
                subtyp = request.POST['SubType']
                Entity_Gid = request.POST['Entity_Gid']
                Create_By = request.POST['Create_By']
                status_request = request.POST['status_request']
                File_Names = request.POST['File_Name']

                data = {"Request_Gid": request.POST['Request_Gid'],"Comments": request.POST['Comments'],

                "File_Name": request.POST['File_Name'],"File_Path": save_path,
                }
                s3.Object('vysfin-assets-uat', File_Names).upload_file(save_path)
                datas = json.dumps(data)

                params = {'Group': "" + grp + "", 'Action': "" + action + "", 'Type': "" + typ+ "",'SubType': "" + subtyp+ "",
                  'Entity_Gid': "" + Entity_Gid + "",'Create_By': "" + Create_By + "",'status_request': "" + status_request + "",}
                headers = {"content-type": "application/json", "Authorization": "" + token + ""}

                resp = requests.post("" + ip + "/Memo_Approvel_SetAPI", params=params, data=datas, headers=headers, verify=False)
                response = resp.content.decode("utf-8")
            return HttpResponse(response)
        if request.POST['Group']=="MemoApprovelsetnofile_Group":


                grp = request.POST['Group']
                action=request.POST['Action']
                typ = request.POST['Type']
                subtyp = request.POST['SubType']
                Entity_Gid = request.POST['Entity_Gid']
                Create_By = request.POST['Create_By']
                status_request = request.POST['status_request']
                data = {"Request_Gid": request.POST['Request_Gid'],"Comments": request.POST['Comments'],
                }

                datas = json.dumps(data)

                params = {'Group': "" + grp + "", 'Action': "" + action + "", 'Type': "" + typ+ "",'SubType': "" + subtyp+ "",
                  'Entity_Gid': "" + Entity_Gid + "",'Create_By': "" + Create_By + "",'status_request': "" + status_request + "",}
                headers = {"content-type": "application/json", "Authorization": "" + token + ""}

                resp = requests.post("" + ip + "/Memo_Approvel_SetAPI", params=params, data=datas, headers=headers, verify=False)
                response = resp.content.decode("utf-8")
                return HttpResponse(response)

def Memo_Masters(request):
    utl.check_authorization(request)
    utl.check_pointaccess(request)
    return render(request,'Memo_Masters.html')



def Memo_downloadfile(request):
    utl.check_authorization(request)
    utl.check_pointaccess(request)
    if request.method == 'GET':
        filename = request.GET['filename']
        s3 = boto3.resource('s3')
        s3_obj=s3.Object(bucket_name='vysfin-assets-uat',key=filename)
        body=s3_obj.get()['Body']
        response = StreamingHttpResponse(body, content_type='application/octet-stream')
        response['Content-Disposition'] = 'inline; filename="{}"'.format(filename)
        return response

def Memo_Categoryadd(request):
    utl.check_authorization(request)
    jsondata = json.loads(request.body.decode('utf-8'))
    if (jsondata.get('Params').get('Group')) == 'Category_Grp':
        Group = jsondata.get('Params').get('Group')
        Action = jsondata.get('Params').get('Action')
        Type = jsondata.get('Params').get('Type')
        Subtype = jsondata.get('Params').get('SubType')
        Create_by = str(jsondata.get('Params').get('Create_by'))
        data = json.dumps(jsondata.get('Params'))
        params = {'Group': "" + Group + "", 'Type': "" + Type + "", 'Create_By': "" + Create_by + "",
                  'Action': "" + Action + "", 'Subtype': "" + Subtype + ""}
        headers = {"content-type": "application/json", "Authorization": "" + token + ""}
        resp = requests.post("" + ip + "/Memo_Master_SetAPI", params=params, data=data, headers=headers,
                             verify=False)
        response = resp.content.decode("utf-8")
        return HttpResponse(response)
    if (jsondata.get('Params').get('Group')) == 'Memocategeory_Grp':
        grp = jsondata.get('Params').get('Group')
        typ = jsondata.get('Params').get('Type')
        typ1 = json.dumps(jsondata.get('Params').get('Create_By'))
        typ3 = json.dumps(jsondata.get('Params').get('Entity_gid'))
        typ2 = jsondata.get('Params').get('Action')
        data = json.dumps(jsondata.get('Params'))
        params = {'Group': "" + grp + "", 'Type': "" + typ + "", 'Create_By': "" + typ1 + "", 'Action': "" + typ2 + "",
                  'Entity_Gid': "" + typ3 + ""}
        headers = {"content-type": "application/json", "Authorization": "" + token + ""}
        datas = json.dumps(jsondata.get('Params'))
        resp = requests.post("" + ip + "/Memo_Master_GetAPI", params=params, data=datas, headers=headers, verify=False)
        response = resp.content.decode("utf-8")
        return HttpResponse(response)
    if (jsondata.get('Params').get('Group')) == 'Memosubcategeory_Grp':
        grp = jsondata.get('Params').get('Group')
        typ = jsondata.get('Params').get('Type')
        typ1 = json.dumps(jsondata.get('Params').get('Create_By'))
        typ3 = json.dumps(jsondata.get('Params').get('Entity_gid'))
        typ2 = jsondata.get('Params').get('Action')
        data = json.dumps(jsondata.get('Params'))
        params = {'Group': "" + grp + "", 'Type': "" + typ + "", 'Create_By': "" + typ1 + "", 'Action': "" + typ2 + "",
                  'Entity_Gid': "" + typ3 + ""}
        headers = {"content-type": "application/json", "Authorization": "" + token + ""}
        datas = json.dumps(jsondata.get('Params'))
        resp = requests.post("" + ip + "/Memo_Master_GetAPI", params=params, data=datas, headers=headers, verify=False)
        response = resp.content.decode("utf-8")
        return HttpResponse(response)
    if (jsondata.get('Params').get('Group')) == 'SubCategory_Grp':
        Group = jsondata.get('Params').get('Group')
        Action = jsondata.get('Params').get('Action')
        Type = jsondata.get('Params').get('Type')
        Subtype = jsondata.get('Params').get('SubType')
        Create_by = str(jsondata.get('Params').get('Create_by'))
        data = json.dumps(jsondata.get('Params'))
        params = {'Group': "" + Group + "", 'Type': "" + Type + "", 'Create_By': "" + Create_by + "",
                  'Action': "" + Action + "", 'Subtype': "" + Subtype + ""}
        headers = {"content-type": "application/json", "Authorization": "" + token + ""}
        resp = requests.post("" + ip + "/Memo_Master_SetAPI", params=params, data=data, headers=headers,
                             verify=False)
        response = resp.content.decode("utf-8")
        return HttpResponse(response)
    if (jsondata.get('Params').get('Group')) == 'UpdateCategory_Grp':
        Group = jsondata.get('Params').get('Group')
        Action = jsondata.get('Params').get('Action')
        Type = jsondata.get('Params').get('Type')
        Subtype = jsondata.get('Params').get('SubType')
        Create_by = str(jsondata.get('Params').get('Create_by'))
        data = json.dumps(jsondata.get('Params'))
        params = {'Group': "" + Group + "", 'Type': "" + Type + "", 'Create_By': "" + Create_by + "",
                  'Action': "" + Action + "", 'Subtype': "" + Subtype + ""}
        headers = {"content-type": "application/json", "Authorization": "" + token + ""}
        resp = requests.post("" + ip + "/Memo_Master_SetAPI", params=params, data=data, headers=headers,
                             verify=False)
        response = resp.content.decode("utf-8")
        return HttpResponse(response)
    if (jsondata.get('Params').get('Group')) == 'Active_Inactive':
        Group = jsondata.get('Params').get('Group')
        Action = jsondata.get('Params').get('Action')
        Type = jsondata.get('Params').get('Type')
        Subtype = jsondata.get('Params').get('SubType')
        Create_by = str(jsondata.get('Params').get('Create_by'))
        data = json.dumps(jsondata.get('Params'))
        params = {'Group': "" + Group + "", 'Type': "" + Type + "", 'Create_By': "" + Create_by + "",
                  'Action': "" + Action + "", 'Subtype': "" + Subtype + ""}
        headers = {"content-type": "application/json", "Authorization": "" + token + ""}
        resp = requests.post("" + ip + "/Memo_Master_SetAPI", params=params, data=data, headers=headers,
                             verify=False)
        response = resp.content.decode("utf-8")
        return HttpResponse(response)
    if (jsondata.get('Params').get('Group')) == 'subActive_Inactive':
        Group = jsondata.get('Params').get('Group')
        Action = jsondata.get('Params').get('Action')
        Type = jsondata.get('Params').get('Type')
        Subtype = jsondata.get('Params').get('SubType')
        Create_by = str(jsondata.get('Params').get('Create_by'))
        data = json.dumps(jsondata.get('Params'))
        params = {'Group': "" + Group + "", 'Type': "" + Type + "", 'Create_By': "" + Create_by + "",
                  'Action': "" + Action + "", 'Subtype': "" + Subtype + ""}
        headers = {"content-type": "application/json", "Authorization": "" + token + ""}
        resp = requests.post("" + ip + "/Memo_Master_SetAPI", params=params, data=data, headers=headers,
                             verify=False)
        response = resp.content.decode("utf-8")
        return HttpResponse(response)
    if (jsondata.get('Params').get('Group')) == 'UpdatesubCategory_Grp':
        Group = jsondata.get('Params').get('Group')
        Action = jsondata.get('Params').get('Action')
        Type = jsondata.get('Params').get('Type')
        Subtype = jsondata.get('Params').get('SubType')
        Create_by = str(jsondata.get('Params').get('Create_by'))
        data = json.dumps(jsondata.get('Params'))
        params = {'Group': "" + Group + "", 'Type': "" + Type + "", 'Create_By': "" + Create_by + "",
                  'Action': "" + Action + "", 'Subtype': "" + Subtype + ""}
        headers = {"content-type": "application/json", "Authorization": "" + token + ""}
        resp = requests.post("" + ip + "/Memo_Master_SetAPI", params=params, data=data, headers=headers,
                             verify=False)
        response = resp.content.decode("utf-8")
        return HttpResponse(response)


def Memo_SubCategory(request):
    utl.check_authorization(request)
    utl.check_pointaccess(request)
    return render(request, 'Memo_SubCategory.html')

def Memo_Create(request):
    utl.check_authorization(request)
    utl.check_pointaccess(request)
    return render(request, 'Memo_Create.html')