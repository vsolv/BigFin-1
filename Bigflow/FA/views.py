from __future__ import unicode_literals
import base64
import datetime
import boto3
import botocore
import pandas as pd
from django.contrib.sites import requests
from django.http import JsonResponse, StreamingHttpResponse
from six import StringIO

from Bigflow.API import view_fa, view_sales, view_master,views
from django.shortcuts import render
from django.http import HttpResponse
import json
import Bigflow.Core.models as common
import Bigflow.Core.jwt_file as jwt
import requests

from Bigflow.menuClass import utility as utl
from Bigflow.FA.model import mFA
from Bigflow.Core.models import decrpt as decry_data
from Bigflow.settings import S3_BUCKET_NAME
ip = common.localip()

# token = common.token()
# Asset Make
def fa_summary(request):
    utl.check_authorization(request)
    return render(request, 'fa_summary.html')
def fa_assetadd(request):
    utl.check_authorization(request)
    return render(request, 'fa_assetadd.html')
def fa_assetchecker(request):
    utl.check_authorization(request)
    return render(request, 'fa_assetchecker.html')

# capitalise date
def fa_capdate_change(request):
    utl.check_authorization(request)
    return render(request, 'fa_capdate_change.html')
def fa_capdate_changeplus(request):
    utl.check_authorization(request)
    return render(request, 'fa_capdate_changeplus.html')
def fa_capdate_checker(request):
    utl.check_authorization(request)
    return render(request, 'fa_capdate_checker.html')

# ParentChild
def fa_asset_parentchild(request):
    utl.check_authorization(request)
    return render(request, 'fa_asset_parentchild.html')
def fa_asset_parentchildcheck(request):
    utl.check_authorization(request)
    return render(request, 'fa_asset_parentchildcheck.html')
def fa_asset_parent_plus(request):
    utl.check_authorization(request)
    return render(request, 'fa_asset_parent_plus.html')

# writeoff checker
def fa_writeoff(request):
    utl.check_authorization(request)
    return render(request, 'fa_writeoff.html')
def fa_writeoffplus(request):
    utl.check_authorization(request)
    return render(request, 'fa_writeoffplus.html')
def fa_writeoff_check(request):
    utl.check_authorization(request)
    return render(request, 'fa_writeoff_check.html')
# impairment
def fa_impairment(request):
    utl.check_authorization(request)
    return render(request, 'fa_impairment.html')
def fa_impairmentplus(request):
    utl.check_authorization(request)
    return render(request, 'fa_impairmentplus.html')
def fa_impairment_check(request):
    utl.check_authorization(request)
    return render(request, 'fa_impairment_check.html')
# Merge
def fa_asset_merge(request):
    utl.check_authorization(request)
    return render(request, 'fa_asset_merge.html')
def fa_asset_merge_plus(request):
    utl.check_authorization(request)
    return render(request, 'fa_asset_merge_plus.html')
def fa_asset_merge_checker(request):
    utl.check_authorization(request)
    return render(request, 'fa_asset_merge_checker.html')
# Split
def fa_asset_split(request):
    utl.check_authorization(request)
    return render(request, 'fa_asset_split.html')
def fa_asset_split_plus(request):
    utl.check_authorization(request)
    return render(request, 'fa_asset_split_plus.html')
def fa_asset_split_checker(request):
    utl.check_authorization(request)
    return render(request, 'fa_asset_split_checker.html')
# catgry
def fa_asset_catgry(request):
    utl.check_authorization(request)
    return render(request, 'fa_asset_catgry.html')
def fa_asset_catgry_plus(request):
    utl.check_authorization(request)
    return render(request, 'fa_asset_catgry_plus.html')
def fa_asset_catgrychecker(request):
    utl.check_authorization(request)
    return render(request, 'fa_asset_catgrychecker.html')
#catgry_master
def fa_asset_catgry_master_plus(request):
    utl.check_authorization(request)
    return render(request, 'fa_asset_catgry_master_plus.html')
def fa_asset_catgry_summary(request):
    utl.check_authorization(request)
    return render(request, 'fa_asset_catgry_master.html')

#fa_asset_salevaluemaker_details
def fa_asset_sale(request):
    utl.check_authorization(request)
    return render(request, 'fa_asset_sale.html')
def fa_asset_saleplus(request):
    utl.check_authorization(request)
    return render(request, 'fa_asset_saleplus.html')
def fa_asset_sale_checker(request):
    utl.check_authorization(request)
    return render(request, 'fa_asset_sale_checker.html')
# reduction
def fa_value_reduction(request):
    utl.check_authorization(request)
    return render(request, 'fa_value_reduction.html')
def fa_value_reduction_plus(request):
    utl.check_authorization(request)
    return render(request, 'fa_value_reduction_plus.html')
def fa_reduction_checker(request):
    utl.check_authorization(request)
    return render(request, 'fa_value_reduction_checker.html')
# transfer
def fa_transfer_maker(request):
    utl.check_authorization(request)
    return render(request, 'fa_transfer_maker.html')
def fa_transferplus(request):
    utl.check_authorization(request)
    return render(request, 'fa_transferplus.html')
def fa_transfer_checker(request):
    utl.check_authorization(request)
    return render(request, 'fa_transfer_checker.html')
#deprisation_calc
def fa_depreciation_calc(request):
    utl.check_authorization(request)
    return render(request, 'fa_depreciation_calc.html')
def fa_posttocbs(request):
    utl.check_authorization(request)
    return render(request, 'fa_posttocbs.html')


#fa_financial_year
def fa_financial_year(request):
    utl.check_authorization(request)
    return render(request, 'fa_financial_year.html')
def fa_financial_year_plus(request):
    utl.check_authorization(request)
    return render(request, 'fa_financial_year_plus.html')
def fa_financial_year_checker(request):
    utl.check_authorization(request)
    return render(request, 'fa_financial_year_checker.html')

# physical Verification
def fa_physic_verify(request):
    utl.check_authorization(request)
    return render(request, 'fa_physic_verify.html')
def fa_physic_verify_plus(request):
    utl.check_authorization(request)
    return render(request, 'fa_physic_verify_plus.html')
def fa_physic_verify_check(request):
    utl.check_authorization(request)
    return render(request, 'fa_physic_verify_check.html')

def fa_cwip_checker(request):
    utl.check_authorization(request)
    return render(request, 'fa_cwip_checker.html')

# Query
def fa_query_summary(request):
    utl.check_authorization(request)
    return  render(request,'fa_asset_query.html')

# Branch Master
def fa_mst_location(request):
    utl.check_authorization(request)
    return  render(request,'fa_mst_location.html')

# Branch Master
def fa_image_popup(request):
    utl.check_pointaccess(request)
    return  render(request,'fa_image_popup.html')

# from Bigflow.settings import BASE_DIR
#
# def FA_Template(request,template_name):
#     template_name = template_name
#     urls_name = []
#     urls_name = url_name.urlpatterns
#     for v in urls_name:
#         url = v.name
#         print(url)
#     html_files = []
#     html_files = os.listdir(BASE_DIR + '/Bigflow' + '/FA/templates')
#     file_name = template_name+".html"
#     for x in html_files:
#         if x == file_name:
#             return render(request, template_name + ".html")
#             break
#     else :
#         for v in urls_name:
#             url = v.name
#             print(url)
#             if url == template_name:
#                 call = template_name + ()
#                 break
#         else:
#             return render(request, "error.html")
#
#     if template_name is not '':
#          return render(request, template_name+".html")


def error_404_view(request):
    utl.check_authorization(request)
    return render(request,'error.html')


def asset_details(request):
    utl.check_authorization(request)
    if request.method == 'POST':
        jsondata = json.loads(request.body.decode('utf-8'))
        obj = view_fa.FAApi()
        obj.grp = jsondata.get('params').get('Group')
        obj.typ = jsondata.get('params').get('Type')
        obj.sub = jsondata.get('params').get('Sub_Type')
        params = {"Group": obj.grp, "Type": obj.typ, "Sub_Type": obj.sub}
        token = jwt.token(request)
        headers = {"content-type": "application/json", "Authorization": "" + token + ""}
        classify = {
            "CLASSIFICATION":{
                "Entity_Gid" : [decry_data(request.session['Entity_gid'])]
            }}
        jsondata['params']['json']['Params'].update(classify)
        datas = json.dumps(jsondata.get('params').get('json'))
        resp = requests.post("" + ip + "/FA_Summary", params=params, data=datas, headers=headers,
                             verify=False)
        response = resp.content.decode("utf-8")
        return HttpResponse(response)

def drop_data(request):
    utl.check_authorization(request)
    if request.method == 'POST':
        drop_l ={
                "Table_name":"fa_mst_tassetcat",
                "Column_1":"assetcat_gid,assetcat_subcatname",
                "Column_2":"",
                "Where_Common":"assetcat",
                "Where_Primary":"",
                "Primary_Value":"",
                "Order_by":"subcatname"
               }
        drop_table ={"data":drop_l}
        obj = view_sales.SalesOrder_Register()
        obj.actn ='FACAT'
        obj.entity_gid =request.session['Entity_gid']
        params = {'Action':obj.actn, 'Entity_Gid': obj.entity_gid}
        token = jwt.token(request)
        headers = {"content-type": "application/json", "Authorization": "" + token + ""}
        datas = json.dumps(drop_table.get('data'))
        resp = requests.post("" + ip + "/All_Tables_Values_Get", params=params, data=datas, headers=headers,
                             verify=False)
        response = resp.content.decode("utf-8")
        return HttpResponse(response)

def get_entity_branch(request):
    utl.check_authorization(request)
    if request.method == 'POST':
        jsondata = json.loads(request.body.decode('utf-8'))
        obj = view_fa.FA_Location()
        obj.grp = jsondata.get('params').get('Group')
        obj.typ = jsondata.get('params').get('Type')
        obj.sub = jsondata.get('params').get('Sub_Type')
        params = {"Group": obj.grp, "Type": obj.typ, "Sub_Type": obj.sub}
        token = jwt.token(request)
        headers = {"content-type": "application/json", "Authorization": "" + token + ""}
        classify = {
            "CLASSIFICATION": {
                "Entity_Gid": int(decry_data(request.session['Entity_gid']))
            }}
        jsondata['params']['json']['params'].update(classify)
        datas = json.dumps(jsondata.get('params').get('json'))
        resp = requests.post("" + ip + "/ENTITY_DETAILS", params=params, data=datas, headers=headers,
                             verify=False)
        response = resp.content.decode("utf-8")
        return HttpResponse(response)


def get_branch(request):
    utl.check_authorization(request)
    if request.method == 'POST':
        jsondata = json.loads(request.body.decode('utf-8'))
        name = jsondata.get('params').get('Branch_name')
        if(name == None):  name = ""
        limts = jsondata.get('params').get('Limits')
        drop_m = {
            "Table_name": "gal_mst_tbranch",
            "Column_1": "branch_gid,branch_name,branch_code",
            "Column_2": "",
            "Where_Common": "branch",
            "Where_Primary": "",
            "Primary_Value": "",
            "Where_Data": "name",
            "Primary_Data":name,
            "Limits": limts,
            "Order_by": "name"
        }
        drop_table ={"data":drop_m}
        obj = view_master.All_Tables_Values_Get()
        obj.actn = 'FABRANCH'
        obj.entity_gid = request.session['Entity_gid']
        params = {'Action':obj.actn, 'Entity_Gid': obj.entity_gid}
        token = jwt.token(request)
        headers = {"content-type": "application/json", "Authorization": "" + token + ""}
        datas = json.dumps(drop_table.get('data'))
        resp = requests.post("" + ip + "/All_Tables_Values_Get", params=params, data=datas, headers=headers,
                             verify=False)
        response = resp.content.decode("utf-8")
        return HttpResponse(response)
def imageconvert_base64(request):
    if request.method == 'POST' and request.FILES['file']:
            f = request.FILES['file']
            name = request.POST['name']
            data = base64.b64encode(f.read())
            # print(data)
            base = name ,"+",data
            return HttpResponse(base)
            # base = {
            #     'name': name,
            #     'data': data,
            # }
            # return JsonResponse(base)


def save_asset(request):
    utl.check_authorization(request)
    if request.method == 'POST':
        full_json = request.POST['data']
        jsondata = json.loads(full_json)
        asset_data = jsondata.get('params').get('json').get('Params').get('DETAILS').get('ASSET')
        # asset_data = jsondata.get('params').get('json').get('DETAILS').get('ASSET')
        files = []
        if request.FILES:
            file_no = list(request.FILES.keys())
            tmp_refgid =0
            tmp_files = []
            for i in range(0, len(request.FILES)):
                name = file_no[i]
                refgid = name.split("_")[1]
                extension = ".jpg"
                file_data = request.FILES[name].read()
                file_name_new = str(request.session['Emp_gid']) + '_' + str(
                    datetime.datetime.now().strftime("%y%m%d_%H%M%S")) + str(i) + str(extension)
                contents = file_data
                s3 = boto3.resource('s3')
                s3_obj = s3.Object(bucket_name=S3_BUCKET_NAME, key=file_name_new)
                s3_obj.put(Body=contents)

                if len(files) != 0:
                    tmp_files = []
                    if refgid == tmp_refgid:
                        for j in files:
                            if j.get('RefGid') == refgid:
                                file_data = {
                                    "File_path": file_name_new,
                                    "File_name": file_name_new
                                }
                                j['File'].append(file_data)
                                tmp_refgid = refgid

                    elif refgid != tmp_refgid:
                        file_data = {
                            "File_path": file_name_new,
                            "File_name": file_name_new
                        }
                        tmp_files.append(file_data)
                        content = {
                            "RefGid": refgid,
                            "File": tmp_files
                        }
                        files.append(content)
                        tmp_refgid = refgid
                else:
                    tmp_files = []
                    file_data = {
                        "File_path": file_name_new,
                        "File_name": file_name_new
                    }
                    tmp_files.append(file_data)
                    content = {
                        "RefGid": refgid,
                        "File" :tmp_files
                    }
                    files.append(content)
                    tmp_refgid = refgid
            jsondata['params']['json']['Params']['File'] = files
        else:
            jsondata['params']['json']['Params']['File'] = {}
        obj = view_fa.FA_Asset_Make()
        obj.act = jsondata.get('params').get('Action')
        obj.grp = jsondata.get('params').get('Group')
        obj.typ = jsondata.get('params').get('Type')
        obj.sub = jsondata.get('params').get('Sub_Type')
        obj.entity = decry_data(request.session['Emp_gid'])
        params = {"Action": obj.act, "Group": obj.grp, "Type": obj.typ, "Sub_Type": obj.sub, "Employee_Gid": obj.entity}
        token = jwt.token(request)
        headers = {"content-type": "application/json", "Authorization": "" + token + ""}
        classify = {
            "CLASSIFICATION": {
                "Entity_Gid": decry_data(request.session['Entity_gid'])
            }}
        jsondata['params']['json']['Params'].update(classify)
        datas = json.dumps(jsondata.get('params').get('json'))
        resp = requests.post("" + ip + "/FA_MAKER", params=params, data=datas, headers=headers,
                             verify=False)
        response = resp.content.decode("utf-8")
        return HttpResponse(response)


#     location details
def branch_details(request):
    utl.check_authorization(request)
    if request.method == 'POST':
        jsondata = json.loads(request.body.decode('utf-8'))
        obj = view_fa.FA_Location()
        obj.grp = jsondata.get('params').get('Group')
        obj.typ = jsondata.get('params').get('Type')
        obj.sub = jsondata.get('params').get('Sub_Type')
        params = {"Group": obj.grp, "Type": obj.typ, "Sub_Type": obj.sub}
        token = jwt.token(request)
        headers = {"content-type": "application/json", "Authorization": "" + token + ""}
        classify = {
            "CLASSIFICATION": {
                "Entity_Gid": decry_data(request.session['Entity_gid'])
            }}
        jsondata['params']['json']['Params'].update(classify)
        datas = json.dumps(jsondata.get('params').get('json'))
        resp = requests.post("" + ip + "/FA_LOCATION", params=params, data=datas, headers=headers,
                             verify=False)
        response = resp.content.decode("utf-8")
        return HttpResponse(response)

def save_location(request):
    utl.check_authorization(request)
    if request.method == 'POST':
        jsondata = json.loads(request.body.decode('utf-8'))
        obj = view_fa.FA_Location()
        obj.act = jsondata.get('params').get('Action')
        obj.grp = jsondata.get('params').get('Group')
        obj.typ = jsondata.get('params').get('Type')
        obj.sub = jsondata.get('params').get('Sub_Type')
        obj.entity = decry_data(request.session['Emp_gid'])
        params = {"Action": obj.act, "Group": obj.grp, "Type": obj.typ, "Sub_Type": obj.sub,"Employee_Gid" :obj.entity}
        token = jwt.token(request)
        headers = {"content-type": "application/json", "Authorization": "" + token + ""}
        classify = {
            "CLASSIFICATION": {
                "Entity_Gid": decry_data(request.session['Entity_gid'])
            }}
        jsondata['params']['json']['Params'].update(classify)
        datas = json.dumps(jsondata.get('params').get('json'))
        resp = requests.post("" + ip + "/FA_LOCATION", params=params, data=datas, headers=headers,
                             verify=False)
        response = resp.content.decode("utf-8")
        return HttpResponse(response)

def writeoff_summary(request):
    utl.check_authorization(request)
    if request.method == 'POST':
        jsondata = json.loads(request.body.decode('utf-8'))
        obj = view_fa.FA_Asset_Make()
        sub_type = jsondata.get('params').get('Sub_Type')
        type = jsondata.get('params').get('Type')
        if type == 'ASSET_SALE' and sub_type == 'CHECKER':
            obj.act = jsondata.get('params').get('Action')
            obj.grp = jsondata.get('params').get('Group')
            obj.typ = jsondata.get('params').get('Type')
            obj.sub = jsondata.get('params').get('Sub_Type')
            obj.entity = decry_data(request.session['Emp_gid'])
            params = {"Action": obj.act, "Group": obj.grp, "Type": obj.typ, "Sub_Type": obj.sub,
                      "Employee_Gid": obj.entity}
            token = jwt.token(request)
            headers = {"content-type": "application/json", "Authorization": "" + token + ""}
            jsondata['params']['json']['Params']['DETAILS']['ASSET']['State_Billing_From_Gid'] = request.session['Entity_state_gid']
            classify = {
                "CLASSIFICATION": {
                    "Entity_Gid": decry_data(request.session['Entity_gid']),
                    "Entity_Details_Gid" : request.session['Entity_detail_gid']
                }}
            jsondata['params']['json']['Params'].update(classify)
            datas = json.dumps(jsondata.get('params').get('json'))
            resp = requests.post("" + ip + "/FA_TRAN", params=params, data=datas, headers=headers,
                                 verify=False)
            response = resp.content.decode("utf-8")

            # AE on Sale Off Approve
            datas = json.loads(datas)
            ls_status = datas.get('Params').get('STATUS').get('Status')
            if (obj.typ == "ASSET_SALE") and obj.sub == "CHECKER" and ls_status == "APPROVED":
                out_msg = json.loads(response)
                if out_msg.get("MESSAGE") == "SUCCESS":
                    datas = json.dumps(datas)
                    client_msg = ac_entry(request, datas,'FA_SALE')
                    if client_msg != 'SUCCESS':
                        JsonResponse({"MESSAGE": "FAIL", "DATA": str(client_msg)})

            return HttpResponse(response)
        else:
            obj.act = jsondata.get('params').get('Action')
            obj.grp = jsondata.get('params').get('Group')
            obj.typ = jsondata.get('params').get('Type')
            obj.sub = jsondata.get('params').get('Sub_Type')
            obj.entity = decry_data(request.session['Emp_gid'])
            params = { "Action":obj.act, "Group": obj.grp, "Type": obj.typ, "Sub_Type": obj.sub,"Employee_Gid" :obj.entity }
            token = jwt.token(request)
            headers = {"content-type": "application/json", "Authorization": "" + token + ""}
            classify = {
                "CLASSIFICATION": {
                    "Entity_Gid": decry_data(request.session['Entity_gid'])
                }}
            jsondata['params']['json']['Params'].update(classify)
            datas = json.dumps(jsondata.get('params').get('json'))
            resp = requests.post("" + ip + "/FA_TRAN", params=params, data=datas, headers=headers,
                                 verify=False)
            response = resp.content.decode("utf-8")
            # AE on Write Off Approve
            # datas = json.loads(datas)
            # ls_status = datas.get('Params').get('STATUS').get('Status')
            # if (obj.typ == "ASSET_WRITEOFF" or obj.typ == 'ASSET_IMPAIRMENT' ) and obj.sub == "CHECKER" and ls_status == "APPROVED" :
            #     out_msg = json.loads(response)
            #     if out_msg.get("MESSAGE") == "SUCCESS":
            #         datas = json.dumps(datas)
            #         client_msg = ac_entry(request, datas)
            #         if client_msg != 'SUCCESS':
            #             JsonResponse({"MESSAGE": "FAIL", "DATA": str(client_msg)})
            return HttpResponse(response)

def asset_checker(request):
    utl.check_authorization(request)
    if request.method == 'POST':
        jsondata = json.loads(request.body.decode('utf-8'))
        obj = view_fa.FA_Asset_Make()
        obj.act = jsondata.get('params').get('Action')
        obj.grp = jsondata.get('params').get('Group')
        obj.typ = jsondata.get('params').get('Type')
        obj.sub = jsondata.get('params').get('Sub_Type')
        status = jsondata.get('params').get('json').get('Params').get('STATUS').get('Status')
        obj.entity = decry_data(request.session['Emp_gid'])
        params = { "Action":obj.act, "Group": obj.grp, "Type": obj.typ, "Sub_Type": obj.sub,"Employee_Gid" :obj.entity }
        token = jwt.token(request)
        headers = {"content-type": "application/json", "Authorization": "" + token + ""}
        classify = {
            "CLASSIFICATION": {
                "Entity_Gid": decry_data(request.session['Entity_gid'])
            }}
        jsondata['params']['json']['Params'].update(classify)
        datas = json.dumps(jsondata.get('params').get('json'))
        resp = requests.post("" + ip + "/FA_MAKER", params=params, data=datas, headers=headers,
                             verify=False)
        response = resp.content.decode("utf-8")
         # Check for Reject too
        if obj.grp == "FA_ASSET_CHECKER" and status != "REJECTED":
            common.logger.error([{"FA_AstChecker_WisefinData": datas}])
            out_msg = json.loads(response)
            common.logger.error([{"FA_AstChecker_WisefinMsg": out_msg}])
            if out_msg.get("MESSAGE") == "SUCCESS":
                common.logger.error([{"FA_AstChecker_AC_EntryCalling": 1}])
                client_msg = ac_entry(request,datas,'FA_MAKE')
                common.logger.error([{"FA_AstChecker_AC_EntryCalled": client_msg}])
                if client_msg.get("MESSAGE") != 'SUCCESS':
                    # Update The asset Detail entry failed
                    obj_ae = mFA.FaModel()
                    obj_ae.action = "UPDATE"
                    obj_ae.type = "ASSET_ENTRY"
                    obj_ae.sub_type = "UPDATE"
                    obj_ae.jsondata = json.dumps(jsondata.get('params').get('json').get('Params').get('DETAILS'))
                    obj_ae.jsonData = "{}"
                    obj_ae.json_file = "{}"
                    obj_ae.jsonData_sec = "{}"
                    obj_ae.json_classification = json.dumps({"Entity_Gid": [decry_data(request.session['Entity_gid'])]})
                    obj_ae.employee_gid = decry_data(request.session['Emp_gid'])
                    outs = obj_ae.set_fa_make()
                    common.logger.error([{"FA_AstChecker_WisefinUpdate": outs}])
                    return JsonResponse({"MESSAGE": "FAIL", "DATA":"Error On CBS Posting."})
                elif client_msg.get("MESSAGE") == 'SUCCESS':
                    common.logger.error([{"FA_AstChecker_API_Success": "Closed"}])
                    return JsonResponse({"MESSAGE": "SUCCESS", "DATA": "SUCCESS"})
                else:
                    common.logger.error([{"FA_AstChecker_AcEntry_Error_Else": "ELSE"}])
                    return JsonResponse({"MESSAGE": "FAIL", "DATA": "FAIL"})

        return HttpResponse(response)

def ac_entry(request,jsondata,ref_name):
    utl.check_authorization(request)
    try:
        obj_fa = mFA.FaModel()
        obj_fa.action = "GET"
        obj_fa.type = "ASSET_ENTRY"
        obj_fa.sub_type = "CD_DETAILS"
        # ref_no = jsondata.get('params').get('status_json').get('ref_no')
        jsondata = json.loads(jsondata)
        asst_grpid = jsondata.get('Params').get('Asst_Grp_ID')
        if asst_grpid == 'null' or asst_grpid is None:
            asst_grpid = ''
        asst_main_gids = []
        if jsondata.get('Params').get('DETAILS') is not None:
            asst_main_gids = jsondata.get('Params').get('DETAILS').get('ASSET').get('Asset_Main_Gid')

        if asst_main_gids == 'null' or asst_main_gids is None:
            asst_main_gids = []
        obj_fa.filter_json = json.dumps({"Entry_Module": "FA","Ref_Name":ref_name,"Asst_GrpID":asst_grpid,"Asst_Main_Gids_AE":asst_main_gids})
        obj_fa.json_classification = json.dumps(jsondata.get('Params').get('CLASSIFICATION'))
        datas = obj_fa.get_fa_summary()
        if datas.get("MESSAGE") == 'NOT_FOUND':
            return {"MESSAGE": "FAIL", "DATA": 'Error On Entry Data'}
        elif datas.get("MESSAGE") != 'FOUND':
            return {"MESSAGE": "FAIL", "DATA": 'Error On Entry Data,No Data'}
         ### To DO Validate The Message found
        df_ae = datas.get("DATA")
        common.logger.error([{"FA_CBS_BeforeLoop": 'Loop Start'}])
        for index,row in df_ae.iterrows():
            Fund_Transfer_Dtls_data = row['entry_detail']
            Fund_Transfer_Dtls_data = json.loads(Fund_Transfer_Dtls_data)
            # CBSDATE = Fund_Transfer_Dtls_data.get("Fund_Transfer_Dtls")[0].get("CBSDATE")
            CBSDATE = str(common.get_server_date("GET_CBSDATE")[0])
            meta_branch_code = Fund_Transfer_Dtls_data.get("Fund_Transfer_Dtls")[0].get("Meta_Brn_Code")
            if (meta_branch_code == None or meta_branch_code == ''):
                meta_branch_code = Fund_Transfer_Dtls_data.get("Fund_Transfer_Dtls")[0].get("Brn_Code")
            data = {"Src_Channel": "EMS", "ApplicationId": row['entry_refno'], "TransactionBranch": meta_branch_code,
                    "Txn_Date": CBSDATE, "productType": "DP",
                    "Fund_Transfer_Dtls": Fund_Transfer_Dtls_data.get("Fund_Transfer_Dtls")}
            data = json.dumps({"Params": {"classification": {"Emp_gid": obj_fa.employee_gid}, "filter": data}})
            params = {'Action': "SET", 'Type': "AMOUNT_TRANSFER"}
            token = jwt.token(request)
            headers = {"content-type": "application/json", "Authorization": "" + token + ""}
            common.logger.error([{"FA_WseFin_ApiCall_Before": 'API Called'}])
            result = requests.post("" + ip + "/AP_Bank_API", params=params, headers=headers, data=data,
                                   verify=False)
            results = result.content.decode("utf-8")
            results = json.loads(results)
            common.logger.error([{"FA_WseFin_ApiCall_After": 'API Called'}])
            if (results.get("MESSAGE") == "SUCCESS"):
                try:
                    obj_fa.action = "UPDATE"
                    obj_fa.type = "ENTRY"
                    obj_fa.sub_type = "UPDATE"
                    obj_fa.jsondata = json.dumps(Fund_Transfer_Dtls_data.get("Fund_Transfer_Dtls"))
                    obj_fa.jsonData = json.dumps({"CBS_Ref_No":results.get("CBSREF_NO")})
                    obj_fa.json_file = "{}"
                    obj_fa.jsonData_sec = "{}"
                    obj_fa.json_classification = json.dumps({"Entity_Gid" : [decry_data(request.session['Entity_gid'])]})
                    obj_fa.employee_gid = decry_data(request.session['Emp_gid'])
                    outs = obj_fa.set_fa_make()

                    if outs.get("MESSAGE") != "SUCCESS":
                        common.logger.error([{"FA_WseFin_ApiCall_After_error": 'Fail on Entry Set'}])
                        return JsonResponse({"MESSAGE": "FAIL", "DATA": outs})

                except Exception as e:
                    common.logger.error([{"FA_WseFin_ApiCall_After_exception": str(e)}])
                    return JsonResponse({"MESSAGE": "FAIL", "DATA": str(e)})
            else:
             common.logger.error([{"FA_WseFin_ApiCall_After_else": str(results)}])
             return JsonResponse({"MESSAGE": "FAIL", "DATA": results})

        return ({"MESSAGE": "SUCCESS"})

    except Exception as e:
        common.logger.error([{"FA_WseFin_ApiCall_OverallException": str(e)}])
        return JsonResponse({"MESSAGE": "FAIL", "DATA": str(e)})


 #_asset_category
def fa_category(request):
    utl.check_authorization(request)
    if request.method == 'POST':
        jsondata = json.loads(request.body.decode('utf-8'))
        obj = view_fa.FA_Category()
        obj.grp = jsondata.get('Group')
        obj.typ = jsondata.get('Type')
        obj.sub = jsondata.get('Sub_Type')
        obj.act = jsondata.get('Action')
        obj.emp_gid = decry_data(request.session['Emp_gid'])
        params = {"Group": obj.grp, "Type": obj.typ, "Sub_Type": obj.sub, "Action": obj.act,
                  "Employee_Gid": obj.emp_gid}
        token = jwt.token(request)
        headers = {"content-type": "application/json", "Authorization": "" + token + ""}
        classify = {
            "CLASSIFICATION": {
                "Entity_Gid": decry_data(request.session['Entity_gid'])
            }}
        jsondata['json']['Params'].update(classify)
        datas = json.dumps(jsondata.get('json'))
        resp = requests.post("" + ip + "/FA_CATEGORY", params=params, data=datas, headers=headers,
                             verify=False)
        response = resp.content.decode("utf-8")
        return HttpResponse(response)

def fa_category_get(request):
    utl.check_authorization(request)
    if request.method == 'POST':
        jsondata = json.loads(request.body.decode('utf-8'))
        obj = view_fa.FA_Category()
        obj.grp = jsondata.get('params').get('Group')
        obj.typ = jsondata.get('params').get('Type')
        obj.sub = jsondata.get('params').get('Sub_Type')
        params = {"Group": obj.grp, "Type": obj.typ, "Sub_Type": obj.sub}
        token = jwt.token(request)
        headers = {"content-type": "application/json", "Authorization": "" + token + ""}
        classify = {
            "CLASSIFICATION": {
                "Entity_Gid": decry_data(request.session['Entity_gid'])
            }}
        jsondata['params']['json']['Params'].update(classify)
        datas = json.dumps(jsondata.get('params').get('json'))
        resp = requests.post("" + ip + "/FA_CATEGORY", params=params, data=datas, headers=headers,
                             verify=False)
        response = resp.content.decode("utf-8")
        return HttpResponse(response)
def dep_ratedata(request):
    if request.method == 'POST':
        jsondata = json.loads(request.body.decode('utf-8'))
        entity = request.session['Entity_gid']
        drop_b = {
            "Table_name":"gal_mst_tmetadata",
            "Column_1":"metadata_value",
            "Column_2":"",
            "Where_Common":"metadata",
            "Where_Primary":"columnname",
            "Primary_Value":"assetcat_gid",
            "Order_by":"value"
        }
        response = alltable(request,drop_b, entity)
        return HttpResponse(response)
def glno_data(request):
    if request.method == 'POST':
        jsondata = json.loads(request.body.decode('utf-8'))
        entity = request.session['Entity_gid']
        drop_b = {
            "Table_name":"gal_mst_tgl",
            "Column_1":"gl_no,gl_name",
            "Column_2":"",
            "Where_Common":"gl",
            "Where_Primary":"",
            "Primary_Value":"",
            "Order_by":"no"
        }
        response = alltable(request,drop_b, entity)
        return HttpResponse(response)
def dep_data_get(request):
    if request.method == 'POST':
        jsondata = json.loads(request.body.decode('utf-8'))
        entity = request.session['Entity_gid']
        drop_b = {
            "Table_name": "fa_mst_tdepsettings",
            "Column_1": "depsettings_deptype,depsettings_depgl,depsettings_depreservegl",
            "Column_2": "",
            "Where_Common": "depsettings",
            "Where_Primary": "",
            "Primary_Value": "",
            "Order_by": "deptype"
        }
        response = alltable(request,drop_b, entity)
        return HttpResponse(response)
def drop_branch(request):
    if request.method == 'POST':
        jsondata = json.loads(request.body.decode('utf-8'))
        entity = request.session['Entity_gid']
        drop_b = {
            "Table_name": "ap_mst_tcategory",
            "Column_1": "category_gid,category_name",
            "Column_2": "",
            "Where_Common": "category",
            "Where_Primary": "",
            "Primary_Value": "",
            "Order_by": "name"
        }
        response = alltable(request,drop_b, entity)
        return HttpResponse(response)
def cwip_group_get(request):
    utl.check_authorization(request)
    if request.method == 'POST':
        jsondata = json.loads(request.body.decode('utf-8'))
        entity = request.session['Entity_gid']
        drop_b = {
            "Table_name":"fa_mst_tcwipgroup",
            "Column_1":"cwipgroup_gid,cwipgroup_name,cwipgroup_gl",
            "Column_2":"",
            "Where_Common":"cwipgroup",
            "Where_Primary":"doctype",
            "Primary_Value":jsondata.get("params").get("Doc_type"),
            "Order_by":"gid"
        }
        response = alltable(request,drop_b, entity)
        return HttpResponse(response)

def alltable(request,table_data,entity):
    drop_tables = {"data": table_data}
    obj = view_sales.SalesOrder_Register()
    obj.action = 'Debit'
    obj.entity_gid = entity
    params = {'Action': obj.action, 'Entity_Gid': obj.entity_gid}
    token = jwt.token(request)
    headers = {"content-type": "application/json", "Authorization": "" + token + ""}
    datas = json.dumps(drop_tables.get('data'))
    resp = requests.post("" + ip + "/All_Tables_Values_Get", params=params, data=datas, headers=headers,
                         verify=False)
    response_data = resp.content.decode("utf-8")
    return response_data

def get_state_drop(request):
    utl.check_authorization(request)
    if request.method == 'POST':
        jsondata = json.loads(request.body.decode('utf-8'))
        obj = views.Commondropdown()
        obj.grp = jsondata.get('params').get('Group')
        params = {"Group": obj.grp}
        token = jwt.token(request)
        headers = {"content-type": "application/json", "Authorization": "" + token + ""}
        classify = {
            "CLASSIFICATION": {
                "Entity_gid": decry_data(request.session['Entity_gid'])
            }}
        jsondata['params']['json']['Params'].update(classify)
        datas = json.dumps(jsondata.get('params').get('json'))
        resp = requests.post("" + ip + "/Common_Dropdown", params=params, data=datas, headers=headers,
                             verify=False)
        response = resp.content.decode("utf-8")
        return HttpResponse(response)

def cust_data(request):
    utl.check_authorization(request)
    if request.method == 'POST':
        jsondata = json.loads(request.body.decode('utf-8'))
        entity = request.session['Entity_gid']
        drop_b = {
            "Table_name":"gal_mst_tcustomer",
            "Column_1":"customer_gid,customer_name",
            "Column_2":"",
            "Where_Common":"customer",
            "Where_Primary":"type",
            "Primary_Value":"ADHOC",
            "Order_by":"name"
        }
        response = alltable(request,drop_b,entity)
        return HttpResponse(response)

def data_cc(request):
    utl.check_authorization(request)
    if request.method == 'POST':
        jsondata = json.loads(request.body.decode('utf-8'))
        entity = request.session['Entity_gid']
        bs_gid =jsondata.get('params').get('Bs_gid')
        drop_b = {
            "Table_name":"ap_mst_tcc",
            "Column_1":"tcc_gid as cc_gid,tcc_code as cc_code,tcc_no as cc_no,tcc_name as cc_name",
            "Column_2":"",
            "Where_Common":"tcc",
            "Where_Primary":"bsgid",
            "Primary_Value":bs_gid,
            "Order_by":"no"
        }
        response = alltable(request,drop_b, entity)
        return HttpResponse(response)

def data_bs(request):
    utl.check_authorization(request)
    if request.method == 'POST':
        jsondata = json.loads(request.body.decode('utf-8'))
        entity = request.session['Entity_gid']
        drop_b = {
            "Table_name":"ap_mst_tbs",
            "Column_1":"tbs_gid as bs_gid,tbs_code as bs_code,tbs_no as bs_no,tbs_name as bs_name",
            "Column_2":"",
            "Where_Common":"tbs",
            "Where_Primary":"",
            "Primary_Value":"",
            "Order_by":"no"
        }
        response = alltable(request,drop_b,entity)
        return HttpResponse(response)

def sale_make(request):
    utl.check_authorization(request)
    if request.method == 'POST':
        jsondata = json.loads(request.body.decode('utf-8'))
        obj = view_fa.FA_Sale()
        obj.act = jsondata.get('params').get('Action')
        obj.grp = jsondata.get('params').get('Group')
        obj.typ = jsondata.get('params').get('Type')
        obj.sub = jsondata.get('params').get('Sub_Type')
        obj.entity = decry_data(request.session['Emp_gid'])
        params = {"Action": obj.act, "Group": obj.grp, "Type": obj.typ, "Sub_Type": obj.sub, "Employee_Gid": obj.entity}
        token = jwt.token(request)
        headers = {"content-type": "application/json", "Authorization": "" + token + ""}
        classify = {
            "CLASSIFICATION": {
                "Entity_Gid": decry_data(request.session['Entity_gid'])
            }}
        jsondata['params']['json']['Params'].update(classify)
        datas = json.dumps(jsondata.get('params').get('json'))
        resp = requests.post("" + ip + "/FA_SALE", params=params, data=datas, headers=headers,
                             verify=False)
        response = resp.content.decode("utf-8")
        return HttpResponse(response)

def dep_calculation(request):
    utl.check_authorization(request)
    if request.method == 'POST':
        jsondata = json.loads(request.body.decode('utf-8'))
        obj = view_fa.FA_Asset_Make()
        obj.act = jsondata.get('params').get('Action')
        obj.grp = jsondata.get('params').get('Group')
        obj.typ = jsondata.get('params').get('Type')
        obj.sub = jsondata.get('params').get('Sub_Type')
        obj.entity = decry_data(request.session['Emp_gid'])
        params = {"Action": obj.act, "Group": obj.grp, "Type": obj.typ, "Sub_Type": obj.sub, "Employee_Gid": obj.entity}
        token = jwt.token(request)
        headers = {"content-type": "application/json", "Authorization": "" + token + ""}
        classify = {
            "CLASSIFICATION": {
                "Entity_Gid": decry_data(request.session['Entity_gid'])
            }}
        jsondata['params']['json']['Params'].update(classify)
        datas = json.dumps(jsondata.get('params').get('json'))
        resp = requests.post("" + ip + "/FA_DEPRECIATION", params=params, data=datas, headers=headers,
                             verify=False)
        response = resp.content.decode("utf-8")

        # if obj.grp == "FA_ASSET_DEPRECIATIONZZZZZZ" and obj.sub == "REGULARZZZZZZZ" :
        #     out_msg = json.loads(response)
        #     if out_msg.get("MESSAGE") == "SUCCESS":
        #         client_msg = ac_entry(request,datas,'FA_DEPRECIATION')
        #         if client_msg != 'SUCCESS':
        #             JsonResponse({"MESSAGE": "FAIL", "DATA": str(client_msg)})
        return HttpResponse(response)



def fin_year(request):
    utl.check_authorization(request)
    if request.method == 'POST':
        jsondata = json.loads(request.body.decode('utf-8'))
        obj = view_fa.FinYear()
        obj.act = jsondata.get('params').get('Action')
        obj.grp = jsondata.get('params').get('Group')
        obj.typ = jsondata.get('params').get('Type')
        obj.sub = jsondata.get('params').get('Sub_Type')
        obj.entity = decry_data(request.session['Emp_gid'])
        params = {"Action": obj.act, "Group": obj.grp, "Type": obj.typ, "Sub_Type": obj.sub,"Employee_Gid" :obj.entity}
        token = jwt.token(request)
        headers = {"content-type": "application/json", "Authorization": "" + token + ""}
        classify = {
            "CLASSIFICATION": {
                "Entity_Gid": decry_data(request.session['Entity_gid']),
                "Entity_Details_Gid" :request.session['Entity_detail_gid']
            }}
        jsondata['params']['json']['Params'].update(classify)
        datas = json.dumps(jsondata.get('params').get('json'))
        resp = requests.post("" + ip + "/FIN_YEAR", params=params, data=datas, headers=headers,
                             verify=False)
        response = resp.content.decode("utf-8")
        return HttpResponse(response)

def css_main_trail(request):
    # if request.method == 'POST':
    #     jsondata = json.loads(request.body.decode('utf-8'))
    #     grp = jsondata.get('params').get('Group')
    #     if grp == "MAIN_NAV_BAR":
    #         maincontent ={
    #                         "color" : "#333333",
    #                     }
    #         print(json.dumps(maincontent))
    #         resp = {'DATA': maincontent, 'MESSAGE':"FOUND"}
    #         #resp['DATA'] = resp['DATA'].apply(json.loads)
    #         print(resp)
    #         return JsonResponse(resp)
    if request.method == 'POST':
        jsondata = json.loads(request.body.decode('utf-8'))
        obj = view_fa.Sales_Invoice_Process()
        obj.grp = jsondata.get('params').get('Group')
        obj.typ = jsondata.get('params').get('Type')
        obj.sub = jsondata.get('params').get('Sub_Type')
        params = {"Group": obj.grp, "Type": obj.typ, "Sub_Type": obj.sub}
        token = jwt.token(request)
        headers = {"content-type": "application/json", "Authorization": "" + token + ""}
        datas = json.dumps(jsondata.get('params').get('json'))
        resp = requests.post("" + ip + "/THEME_CSS", params=params, data=datas, headers=headers,
                             verify=False)
        response = resp.content.decode("utf-8")
        return HttpResponse(response)

### Below used to Forecast excel
def dpforecast_getexcel(request):
    # utl.check_authorization(request)
    # utl.check_pointaccess(request)
    if request.method == 'GET':

        obj_master = mFA.FaModel()
        obj_master.employee_gid = 0
        obj_master.employee_name = ''
        obj_master.cluster_gid = 0
        obj_master.cluster = 'ALL'
        obj_master.jsonData = json.dumps({"entity_gid": [decry_data(request.session['Entity_gid'])], "client_gid": []})
        # XLSX_MIME = 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        # response = HttpResponse(content_type=XLSX_MIME)
        # response['Content-Disposition'] = 'attachment; filename="FAForecastzz.xlsx"'
        # writer = pd.ExcelWriter(response, engine='xlsxwriter')
        obj_master.type = 'FORCAST'
        obj_master.sub_type = 'EXCEL'
        obj_master.filter_json = '{}'
        obj_master.json_classification = json.dumps({"Entity_Gid": decry_data(request.session['Entity_gid'])})
        common.logger.error([{"FA_Before_Model": 'get_fadepreciation_called'}])
        df_view = obj_master.get_fadepreciation()
        common.logger.error([{"FA_After_Model": 'get_fadepreciation_called'}])
        common.logger.error([{"FA_After_Model_Data": df_view.get("DATA")[0:11]}])
        common.logger.error([{"FA_After_Model_Data": df_view.get("MESSAGE")}])
        if df_view.get("MESSAGE") == 'FOUND':
            df_fa = df_view.get("DATA")
# start
            file_name = str('FAForecast_') + str(request.session['Emp_gid']) + str(
                datetime.datetime.now().strftime("%y%m%d_%H%M%S")) + '.csv'
            request.session['FA_ForeCastFileName'] = file_name
            common.logger.error([{"FA_startWriter_cs": 'file'}])
            csv_buffer = StringIO()
            df_fa.to_csv(csv_buffer)
            common.logger.error([{"FA_After_writer_cs": 'aw'}])
            s3_resource = boto3.resource('s3','ap-south-1')
            common.logger.error([{"FA_Before_S3": 'bs3'}])
            s3_resource.Object(S3_BUCKET_NAME, file_name).put(Body=csv_buffer.getvalue())
            common.logger.error([{"FA_AfterS3": 'as3'}])
            msg = {"DATA": "SUCCESS"}
            return JsonResponse(msg)
# ends
#             import io
#             common.logger.error([{"FA_startWriter_xl": 'file'}])
#             with io.BytesIO() as output:
#                 with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
#                     df_fa.to_excel(writer)
#
#                 common.logger.error([{"FA_After_writer_xl": 'aw'}])
#                 data = output.getvalue()
#
#
#             file_name = str('FAForecast_') + str(request.session['Emp_gid']) + str(datetime.datetime.now().strftime("%y%m%d_%H%M%S")) + '.xlsb'
#             request.session['FA_ForeCastFileName'] = file_name
#
#             common.logger.error([{"FA_Before_S3": 'bs3'}])
#
#             s3 = boto3.resource('s3','ap-south-1')
#             s3_obj = s3.Object(bucket_name=S3_BUCKET_NAME, key=file_name)
#             s3_obj.put(Body=data)
#             common.logger.error([{"FA_AfterS3": 'as3'}])
#             msg = {"DATA": "SUCCESS"}
#             return JsonResponse(msg)
        else:
            msg = {"DATA": "FAIL"}
            common.logger.error([{"FA_AfterS3_else": 'as3'}])
            return JsonResponse(msg)
            # df_fa = df_view.get("DATA")
            # df_fa.to_excel(writer, 'Sheet1')
            # writer.save()
            # return response

def check_file_exists_forecast(request):
    s3 = boto3.resource('s3','ap-south-1')
    common.logger.error([{"FA_Before_FileExists": 'bfe'}])
    try:
        file_name = request.session['FA_ForeCastFileName']
        s3.Object(S3_BUCKET_NAME, file_name).load()
    except botocore.exceptions.ClientError as e:
        if e.response['Error']['Code'] == "404":
            msg = {"DATA": "FAIL"}
            common.logger.error([{"FA_Fileexistserror": '404'}])
            return JsonResponse(msg)
        else:
            msg = {"DATA": "ERROR"}
            common.logger.error([{"FA_filesexistserror_else": 'else'}])
            return JsonResponse(msg)
    else:
        msg = {"DATA": "SUCCESS"}
        common.logger.error([{"FA_AfterFileExists": 'get_fadepreciation_called'}])
        return JsonResponse(msg)

def fa_excel_s3_forecast(request):
    filename = request.session['FA_ForeCastFileName']
    # filename = "FAForecastz1.xlsx"
    common.logger.error([{"FA_Before_FileDownload": 'bfdw'}])
    s3 = boto3.resource('s3','ap-south-1')
    s3_obj = s3.Object(bucket_name=S3_BUCKET_NAME, key=filename)
    body = s3_obj.get()['Body']
    response = StreamingHttpResponse(body, content_type='application/octet-stream')
    response['Content-Disposition'] = 'inline; filename="{}"'.format(filename)
    common.logger.error([{"FA_AfterFileGot": 'AfG'}])
    return response


from apscheduler.scheduler import Scheduler
sched = Scheduler()
sched.start()

# def fa_excel(request):
#     sched.add_cron_job(fa_excel_fun(request), second=30)

def fa_excel(request):
    #### This is prepare data for regular excel
    if request.method == 'GET':
        obj_master = mFA.FaModel()
        obj_master.from_date = request.GET['Dep_Month']
        obj_master.jsonData = json.dumps({"entity_gid": [decry_data(request.session['Entity_gid'])], "client_gid": []})
        XLSX_MIME = 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        response = HttpResponse(content_type=XLSX_MIME)
        response['Content-Disposition'] = 'attachment; filename="FARegular.xlsx"'
        writer = pd.ExcelWriter(response, engine='xlsxwriter')
        obj_master.type = 'REGULAR'
        obj_master.sub_type = 'EXCEL'
        dates = {}
        dates = '{"Dep_Month":"'+str(obj_master.from_date)+'"}'
        obj_master.filter_json = dates
        obj_master.json_classification = json.dumps({"Entity_Gid": decry_data(request.session['Entity_gid'])})
        df_view = obj_master.get_fadepreciation()
        if df_view.get("MESSAGE") == 'FOUND':
            df_fa = df_view.get("DATA")
            df_fa.to_excel(writer, 'Sheet1')
            writer.save()
            data = response.getvalue()
            s3 = boto3.resource('s3')
            s3_obj = s3.Object(bucket_name=S3_BUCKET_NAME, key="FARegular.xlsx")
            s3_obj.put(Body=data)
            msg = {"DATA":"SUCCESS"}
            return JsonResponse(msg)
        else:
            df_fa = df_view.get("DATA")
            df_fa.to_excel(writer, 'Sheet1')
            writer.save()
            return response


def check_file_exists(request):
    s3 = boto3.resource('s3')
    try:
        s3.Object(S3_BUCKET_NAME, 'FARegularz.xlsx').load()
    except botocore.exceptions.ClientError as e:
        if e.response['Error']['Code'] == "404":
            msg = {"DATA": "FAIL"}
            return JsonResponse(msg)
        else:
            msg = {"DATA": "ERROR"}
            return JsonResponse(msg)
    else:
        msg = {"DATA": "SUCCESS"}
        return JsonResponse(msg)


def fa_excel_s3(request):
    filename = "FARegularz.xlsx"
    s3 = boto3.resource('s3')
    s3_obj = s3.Object(bucket_name=S3_BUCKET_NAME, key=filename)
    body = s3_obj.get()['Body']
    response = StreamingHttpResponse(body, content_type='application/octet-stream')
    response['Content-Disposition'] = 'inline; filename="{}"'.format(filename)
    return response


def dpregular_getexcel(request):
    # utl.check_authorization(request)
    # utl.check_pointaccess(request)
    if request.method == 'GET':
        obj_master = mFA.FaModel()
        obj_master.from_date = request.GET['Dep_Month']
        obj_master.jsonData = json.dumps({"entity_gid": [decry_data(request.session['Entity_gid'])], "client_gid": []})
        XLSX_MIME = 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        response = HttpResponse(content_type=XLSX_MIME)
        response['Content-Disposition'] = 'attachment; filename="FARegular.xlsx"'
        writer = pd.ExcelWriter(response, engine='xlsxwriter')
        obj_master.type = 'REGULAR'
        obj_master.sub_type = 'EXCEL'
        dates = {}
        dates = '{"Dep_Month":"'+str(obj_master.from_date)+'"}'
        obj_master.filter_json = dates
        obj_master.json_classification = json.dumps({"Entity_Gid": decry_data(request.session['Entity_gid'])})
        df_view = obj_master.get_fadepreciation()
        if df_view.get("MESSAGE") == 'FOUND':
            df_fa = df_view.get("DATA")
            df_fa.to_excel(writer, 'Sheet1')
            writer.save()
            return response
        else:
            df_fa = df_view.get("DATA")
            df_fa.to_excel(writer, 'Sheet1')
            writer.save()
            return response


def commondata_get(request):
    utl.check_authorization(request)
    if request.method == 'POST':
        jsondata = json.loads(request.body.decode('utf-8'))
        entity = request.session['Entity_gid']
        if jsondata.get('Type') == "AP_Category":
            drop_b = {
                "Table_name":"ap_mst_tcategory",
                "Column_1":"category_gid,category_code,category_no,category_name",
                "Column_2":"",
                "Where_Common":"category",
                "Where_Primary":"",
                "Primary_Value":"",
                "Order_by":"gid"
            }
            response = alltable(request,drop_b, entity)
            return HttpResponse(response)
        elif jsondata.get('Type') == "AP_Category_Astcat":
            drop_b = {
                "Table_name":"ap_mst_tcategory",
                "Column_1":"category_gid,category_code,category_no,category_name",
                "Column_2":"",
                "Where_Common":"category",
                "Where_Primary":"isasset",
                "Primary_Value":'Y',
                "Order_by":"gid"
            }
            response = alltable(request,drop_b, entity)
            return HttpResponse(response)

        elif jsondata.get('Type') == "AP_Subcategory":
            drop_b = {
                "Table_name":"ap_mst_tsubcategory",
                "Column_1":"subcategory_gid,subcategory_glno,subcategory_code,subcategory_no,subcategory_name",
                "Column_2":"",
                "Where_Common":"subcategory",
                "Where_Primary":"categorygid",
                "Primary_Value":jsondata.get('Categorygid'),
                "Order_by":"gid"
            }
            response = alltable(request,drop_b, entity)
            return HttpResponse(response)
        elif jsondata.get('Type') == "Gl_Data":
            drop_b = {
                "Table_name":"gal_mst_tgl",
                "Column_1":"gl_gid,gl_no",
                "Column_2":"",
                "Where_Common":"gl",
                "Where_Primary":"",
                "Primary_Value":"",
                "Order_by":"gid"
            }
        elif jsondata.get('Type') == "Product":
            drop_b = {
                "Table_name": "gal_mst_tproduct",
                "Column_1": "product_gid,product_name",
                "Column_2": "",
                "Where_Common": "product",
                "Where_Primary": "",
                "Primary_Value": "",
                "Order_by": "name"
            }
            response = alltable(request,drop_b, entity)
            return HttpResponse(response)
        elif jsondata.get('Type') == "Asset_Group":
            drop_b = {
                "Table_name": "fa_trn_tassetgroup",
                "Column_1": "assetgroup_gid,assetgroup_no",
                "Column_2": "",
                "Where_Common": "assetgroup",
                "Where_Primary": "",
                "Primary_Value": "",
                "Order_by": "no"
            }
            response = alltable(request,drop_b, entity)
            return HttpResponse(response)
        elif jsondata.get('Type') == "Asset_Id":
            drop_b = {
                "Table_name": "fa_trn_tassetdetails",
                "Column_1": "assetdetails_id,assetdetails_gid,assetdetails_status",
                "Column_2": "",
                "Where_Common": "assetdetails",
                "Where_Primary": "assetgroupid",
                "Primary_Value": jsondata.get('Ast_Grp_Gid'),
                "Order_by": "gid",
                "Search_Column_Name": 'ACTIVE'
            }
            response = alltable(request,drop_b, entity)
            return HttpResponse(response)
        elif jsondata.get('Type') == "Check_Bucket_Capitalized":
            bucket_name = jsondata.get('Bucket_Name')
            drop_b = {
                "Table_name": "fa_trn_tfaclringheader",
                "Column_1": "faclringheader_gid",
                "Column_2": "",
                "Where_Common": "faclringheader",
                "Where_Primary": "groupno",
                "Primary_Value": bucket_name,
                "Order_by": "groupno"
            }
            response = alltable(request, drop_b, entity)
            return HttpResponse(response)
        elif jsondata.get('Type') == "Asst_cat_BUC":
            Ap_SubCat_Gid = jsondata.get('Ap_SubCat_Gid')
            drop_b = {
                "Table_name":"fa_mst_tassetcat",
                "Column_1":"assetcat_gid,assetcat_subcatname",
                "Column_2":"",
                "Where_Common":"assetcat",
                "Where_Primary":"subcategorygid",
                "Primary_Value":Ap_SubCat_Gid,
                "Order_by":"subcatname"
            }
            response = alltable(request, drop_b, entity)
            return HttpResponse(response)

def posttocbs_set(request):
    utl.check_authorization(request)
    if request.method == 'POST':
        jsondata = json.loads(request.body.decode('utf-8'))
        obj = view_fa.FA_Asset_Make()
        sub_type = jsondata.get('params').get('Sub_Type')
        type = jsondata.get('params').get('Type')
        obj.act = jsondata.get('params').get('Action')
        obj.grp = jsondata.get('params').get('Group')
        obj.typ = jsondata.get('params').get('Type')
        obj.sub = jsondata.get('params').get('Sub_Type')
        obj.entity = decry_data(request.session['Emp_gid'])
        params = {"Action": obj.act, "Group": obj.grp, "Type": obj.typ, "Sub_Type": obj.sub, "Employee_Gid": obj.entity}
        token = jwt.token(request)
        headers = {"content-type": "application/json", "Authorization": "" + token + ""}
        classify = {
            "CLASSIFICATION": {
                "Entity_Gid": decry_data(request.session['Entity_gid'])
            }}
        jsondata['params']['json']['Params'].update(classify)
        datas = json.dumps(jsondata.get('params').get('json'))
        resp = requests.post("" + ip + "/FA_TRAN", params=params, data=datas, headers=headers,
                             verify=False)
        response = resp.content.decode("utf-8")
        # AE POST To CBS
        datas = json.loads(datas)
        if obj.typ == "POSTTOCBS":
            out_msg = json.loads(response)
            if out_msg.get("MESSAGE") == "SUCCESS":
                datas = json.dumps(datas)
                client_msg = ac_entry(request, datas,"FA_DEPRECIATION")
                if client_msg != 'SUCCESS':
                    JsonResponse({"MESSAGE": "FAIL", "DATA": str(client_msg)})
        return HttpResponse(response)

def repost_set(request):
    jsondata = json.loads(request.body.decode('utf-8'))
    classify = {
        "CLASSIFICATION": {
            "Entity_Gid": decry_data(request.session['Entity_gid'])
        }}
    jsondata['params']['json']['Params'].update(classify)
    datas = json.dumps(jsondata.get('params').get('json'))
    common.logger.error([{"FA_Repost_Data_BeforeAcentryCall": datas}])
    client_msg = ac_entry(request, datas,"FA_MAKE")
    common.logger.error([{"FA_Repost_acentry_msg": client_msg}])
    if client_msg.get("MESSAGE") == 'SUCCESS':
        try:
            obj_fa = mFA.FaModel()
            obj_fa.action = "UPDATE"
            obj_fa.type = "REPOST_ENTRY"
            obj_fa.sub_type = "AST_STATUS"
            datas = json.loads(datas)
            asst_grpid = datas.get('Params').get('Asst_Grp_ID')
            obj_fa.jsondata = json.dumps({"Asst_GrpID": asst_grpid})
            obj_fa.jsonData = "{}"
            obj_fa.json_file = "{}"
            obj_fa.jsonData_sec = "{}"
            obj_fa.json_classification = json.dumps({"Entity_Gid": [decry_data(request.session['Entity_gid'])]})
            obj_fa.employee_gid = decry_data(request.session['Emp_gid'])
            outs = obj_fa.set_fa_make()
            common.logger.error([{"FA_Repost_Wisefin_Update": outs}])
            return JsonResponse({"MESSAGE": "SUCCESS", "DATA": "SUCCESS"})
        except Exception as e:
            common.logger.error([{"FA_Repost_Wisefin_Exception": str(e)}])
            return JsonResponse({"MESSAGE": "FAIL", "DATA": str(e)})
    if client_msg.get("MESSAGE") != 'SUCCESS':
        common.logger.error([{"FA_Repost_Api_Fail": str(client_msg)}])
        return JsonResponse({"MESSAGE": "FAIL", "DATA": str(client_msg)})
    return JsonResponse({"MESSAGE": "SUCCESS", "DATA":"SUCCESS"})


def generate_saletemplate(request):
    # utl.check_authorization(request)
    if request.method == 'POST':
        jsondata = json.loads(request.body.decode('utf-8'))
        obj = view_fa.FA_Location()
        obj.grp = jsondata.get('params').get('Group')
        obj.typ = jsondata.get('params').get('Type')
        obj.sub = jsondata.get('params').get('Sub_Type')
        params = {"Group": obj.grp, "Type": obj.typ, "Sub_Type": obj.sub}
        token = jwt.token(request)
        headers = {"content-type": "application/json", "Authorization": "" + token + ""}
        classify = {
            "CLASSIFICATION": {
                "Entity_Gid": int(decry_data(request.session['Entity_gid'])),
                "Create_By":decry_data(request.session['Emp_gid'])
            }}
        jsondata['params']['json']['Params'].update(classify)
        datas = json.dumps(jsondata.get('params').get('json'))
        resp = requests.post("" + ip + "/GENERATE_SALE_TEMP", params=params, data=datas, headers=headers,
                             verify=False)
        response = resp.content.decode("utf-8")
        return HttpResponse(response)
