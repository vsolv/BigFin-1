
import os

import traceback

# import django.db
from environs import Env
# from rest_framework.views import APIView

env = Env()
env.read_env()
from django.conf import settings
from django.shortcuts import render
import json
from django.http import JsonResponse
from Bigflow.Master.Model import mMasters
from Bigflow.Transaction.Model import mFET
import Bigflow
import datetime
import socket
import Bigflow.Core.models as common
from dateutil.relativedelta import relativedelta
import requests
from Bigflow.Core.models import decrpt as decry_data
from Bigflow.Core import class1
from rest_framework_simplejwt import settings as token_Set
from Bigflow.menuClass import utility as utl
from Bigflow.menuClass import utility
from django.http import HttpResponse
from Bigflow.Core import jwt_file as jwt
# from Bigflow.Core.class1 import login as mCore
from apscheduler.scheduler import Scheduler
# Start the scheduler



sched = Scheduler()
sched.start()
from datetime import date
current_date = date.today()

mMaster = Bigflow.mMasters.Masters()
mcommon = Bigflow.common
mCore = Bigflow.mCore

ip = common.localip()
token = common.token()

def loginIndex(request):
    request.session.flush()
    return render(request, "Shared/bigFlowLogin.html")

def Health_Check(request):
    return HttpResponse('SUCCESS HEALTH CHECK')


def setip_out(request):
    utl.check_pointaccess(request)
    if request.method == 'GET':
        obj_position = mMaster
        decrypt_emp_gid = decry_data(request.session['Emp_gid'])
        jsondatas = json.loads(request.GET['jsonData'])
        jsondatas['employee_gid'] = decrypt_emp_gid
        obj_position.action = request.GET['action']
        obj_position.ipaddress = {'ipaddress': socket.gethostname()}
        obj_position.jsonData= jsondatas
        obj_position.jsonData.update(obj_position.ipaddress)
        obj_position.entity_gid = decry_data(request.session['Entity_gid'])
        obj_position.create_by = decrypt_emp_gid
        df_position = mcommon.outputReturn(obj_position.set_ip(), 0)
        return JsonResponse(df_position, safe=False)


def setip_sys(request):
    utl.check_pointaccess(request)
    if request.method == 'POST':
        obj_position = mMaster
        jsondata = json.loads(request.body.decode('utf-8'))
        decrypt_entity_gid = decry_data(request.session['Entity_gid'])
        decrypt_emp_gid = decry_data(request.session['Emp_gid'])
        jsondatas = jsondata.get('parms').get('jsonData')
        jsondatas['employee_gid'] = decrypt_emp_gid
        obj_position.action = jsondata.get('parms').get('action')
        ipaddress = {'ipaddress': socket.gethostname()}
        obj_position.jsonData = jsondatas
        obj_position.jsonData.update(ipaddress)
        obj_position.entity_gid = decrypt_entity_gid
        obj_position.create_by = decrypt_emp_gid
        df_position = mcommon.outputReturn(obj_position.set_ip(), 0)
        if str(df_position).isdigit():
            request.session['Login_Gid']=df_position
        return JsonResponse(df_position, safe=False)



def check_memo_employee(data):
    ip = common.memoapi_url()
    resp = requests.post("" + ip + "/usrserv/emp_insert", params="", data=data, headers="", verify=False)
    response = json.loads(resp.content)
    resp = response['code']
    if (resp ==  'No Branch'):
        return response
    else:
        return  response


import urllib


def loginpswd(request):
    try:
        utl.check_pointaccess(request)
        common.logger.error([{"LG_loginpwd_MSG": 'Point Access Ok'}])
        if request.method == 'POST':
            jsondata = json.loads(request.body.decode('utf-8'))
            Type = jsondata.get('parms').get('TYPE')
            # request.session.flush()
            if Type == 'LOGIN_AD':
                # Api Call starts
                user_name = jsondata.get('parms').get('username')
                user_password = jsondata.get('parms').get('password')
                datas = jsondata.get('parms')
                # del jsondata['TYPE']
                ADip = common.clientapi()
                headers = {"Content-Type": "application/x-www-form-urlencoded", "APIKey": common.ADToken()}
                resp = requests.post("" + ADip + "/next/v1/mw/internal/login", params="", data=datas, headers=headers,
                                     verify=False)
                response = json.loads(resp.content)
                response_msg = response.get("out_msg")
                dict = json.loads(response_msg)
                msg = dict["ErrorCode"]
                common.logger.error([{"LG_AD_MSG": msg}])
                if msg == '00' or msg == '0':
                    dict.update({'EmployeeCode': user_name})
                    validatewithmemo = check_memo_employee(json.dumps(dict))
                    common.logger.error([{"LG_memo_MSG": validatewithmemo}])
                    if validatewithmemo == 'No Branch':
                        return JsonResponse(json.dumps(validatewithmemo), safe=False)
                    else:
                        obj_login = class1.login()
                        obj_login.type = Type
                        validatewithmemo.update({"Employee_Gid": '0', "Password": class1.converttoascii(user_password)})
                        obj_login.jsondata = json.dumps(validatewithmemo)
                        out_message = obj_login.get_login()
                        if out_message[1][0] == 'SUCCESS':
                            ld_dict = {"DATA": out_message[0][0], "MESSAGE": out_message[1][0]}
                            ld_dict = json.dumps(ld_dict)
                            ld_dict = json.loads(ld_dict)
                            emp_id = ld_dict.get('DATA').get('employee_gid')
                            emp_name = ld_dict.get('DATA').get('employee_name')
                            date = ld_dict.get('DATA').get('date')
                            request.session.flush()
                            out_msg = token_jwt(request, "LOGIN", user_name)
                            two_fa = common.two_factor_authenticate()
                            if two_fa == 'Enabled':
                                x_forwarded_ip = request.META.get('HTTP_X_FORWARDED_FOR')
                                if x_forwarded_ip is None:
                                    user_ip_ = ['0']
                                else:
                                    user_ip_ = [x_forwarded_ip]
                                ip_fr_validate = common.ip_address_validate()
                                envIP_list = ip_fr_validate.split(",")
                                for i in envIP_list:
                                    i = i.replace(" ", "")
                                    for j in user_ip_:
                                        j = j.replace(" ", "")
                                        if i == j:
                                            cond_tion = True
                                            condition_ = '0'
                                            print(cond_tion)
                                            break
                                        if i != j:
                                            cond_tion = False
                                            condition_ = '1'
                                            print(cond_tion)
                                    if cond_tion:
                                        break
                            else:
                                condition_ = '0'
                            if out_msg != 'SUCCESS':
                                return JsonResponse(json.dumps('FAIL'), safe=False)
                            request.session['date'] = date
                            request.session['Emp_gid'] = emp_id
                            request.session['Emp_name'] = emp_name
                            request.session['OTP_Validate'] = condition_
                            request.session['Entity_gid'] = ld_dict.get('DATA').get('entity_gid')
                            request.session['Entity_state_gid'] = 1
                            request.session['Entity_detail_gid'] = 1
                            request.session['Branch_gid'] = ld_dict.get('DATA').get('branch_gid')
                            request.session['branch_code'] = ld_dict.get('DATA').get('branch_code')
                            request.session['employee_mobileno'] = ld_dict.get('DATA').get('employee_mobileno')
                            output = ld_dict.get('DATA')
                            output.update({"OTP_Validate": condition_})
                            output.update({"OTP_Validate_ip": common.server_environ_var()})
                            output.update({"OTP_Validate_ip_": common.two_factor_authenticate()})
                            output.update({"OTP_Validate_ip_1": common.ip_address_validate()})
                            print(output)
                            return JsonResponse(json.dumps(output), safe=False)

                        elif out_message[1][0] == 'FAIL' or 'No Branch':
                            return JsonResponse(json.dumps(out_message[1][0]), safe=False)
                else:
                    common.logger.error([{"LG_else_Fail": msg}])
                    return JsonResponse(json.dumps('FAIL'), safe=False)
                # api Call Ends


            elif Type == 'LOGIN_LOCAL':

                # token_jwt(request,"CHECK")
                obj_location = class1.login()
                obj_location.type = Type
                common.logger.error([{"LG_Local_LoginStart": "Started"}])
                obj_location.jsondata = json.dumps(
                    {"Employee_Gid": '0', "EmployeeCode": jsondata.get('parms').get('username'),
                     "Password": class1.converttoascii(jsondata.get('parms').get('password'))})
                result = obj_location.get_login()
                common.logger.error([{"LG_Local_Login_Over": str(result)[0:10]}])
                if (result[1][0] == 'SUCCESS'):
                    request.session.flush()
                    out_msg = token_jwt(request, "LOGIN", jsondata.get('parms').get('username'))
                    if out_msg != 'SUCCESS':
                        return JsonResponse(json.dumps('FAIL'), safe=False)
                    two_fa = common.two_factor_authenticate()
                    if two_fa == 'Enabled':
                        x_forwarded_ip = request.META.get('HTTP_X_FORWARDED_FOR')
                        if x_forwarded_ip == 'null' or 'None':
                            x_forwarded_ip = '0'
                            user_ip_ = [x_forwarded_ip]
                        else:
                            user_ip_ = [x_forwarded_ip]
                        ip_fr_validate = common.ip_address_validate()
                        envIP_list = ip_fr_validate.split(",")
                        for i in envIP_list:
                            i = i.replace(" ", "")
                            for j in user_ip_:
                                j = j.replace(" ", "")
                                if i == j:
                                    cond_tion = True
                                    condition_ = '0'
                                    print(cond_tion)
                                    break
                                if i != j:
                                    cond_tion = False
                                    condition_ = '1'
                                    print(cond_tion)
                            if cond_tion:
                                break
                    else:
                        condition_ = '0'
                    # user_ip = ['210.18.79.86']
                    request.session['OTP_Validate'] = condition_
                    request.session['date'] = result[0][0].get('date')
                    request.session['Emp_gid'] = result[0][0].get('employee_gid')
                    request.session['Emp_name'] = result[0][0].get('employee_name')
                    request.session['Entity_gid'] = result[0][0].get('entity_gid')
                    request.session['Entity_state_gid'] = 1
                    request.session['Entity_detail_gid'] = 1
                    request.session['Branch_gid'] = result[0][0].get('branch_gid')
                    request.session['branch_code'] = result[0][0].get('branch_code')
                    request.session['employee_mobileno'] = result[0][0].get('employee_mobileno')
                    result[0][0].update({"OTP_Validate":condition_})

                    output = result[0][0]
                    common.logger.error([{"LG_Local_Token_Over": str(output)[0:10]}])
                    return JsonResponse(json.dumps(output), safe=False)
                else:
                    return JsonResponse(json.dumps(result[1][0]), safe=False)
        else:
            return render(request, "Shared/bigFlowLogin.html")


    except Exception as e:
        common.logger.error([{"LG_LocalLoginTryC_End": str(e)}])




def validate_otp(request):
    try:
        # utl.check_pointaccess(request)
        # common.logger.error([{"LG_loginpwd_MSG": 'Point Access Ok'}])
        if request.method == 'POST':
            jsondata = json.loads(request.body.decode('utf-8'))
            action = jsondata.get('parms').get('action')
            if action == 'GENERATE_OTP':
                # Api Call starts
                datas =  json.dumps({'mobileNumber':request.session['employee_mobileno']})
                # del jsondata['TYPE']
                ADip = common.clientapi()
                generated_token_data = master_sync_Data_("GET", "get_data", 1)
                new_token = generated_token_data.get("DATA")[0].get("clienttoken_name")
                ip_new = "" + ADip + "/next/v1/mw/generateotp"
                headers = {"content-type": "application/json", "Authorization": "Bearer " + new_token + ""}
                resp = requests.post(ip_new, data=datas, headers=headers,
                                     verify=False)
                a = json.loads(resp.text)
                b = a["ErrorCode"]
                # c=a["out_msg"]["Branch_Name"]
                return JsonResponse({"ERRORCODE":a["ErrorCode"],"Description":a["Description"]},safe=False)
                # api Call Ends
            elif action == 'VERIFY_OTP':
                datas = jsondata.get('parms').get('jsonData')
                datas.update({'mobileNumber':request.session['employee_mobileno']})
                datas = json.dumps(datas)
                ADip = common.clientapi()
                generated_token_data = master_sync_Data_("GET", "get_data", 1)
                new_token = generated_token_data.get("DATA")[0].get("clienttoken_name")
                ip_new = "" + ADip + "/next/v1/mw/validateotp"
                headers = {"content-type": "application/json", "Authorization": "Bearer " + new_token + ""}
                resp = requests.post(ip_new, data=datas, headers=headers,
                                     verify=False)
                a = json.loads(resp.text)
                return JsonResponse({"ERRORCODE":a["ErrorCode"],"Description":a["Description"]},safe=False)
        else:
            return render(request, "Shared/bigFlowLogin.html")
    except Exception as e:
        common.logger.error([{"LG_LocalLoginTryC_End": str(e)}])

import base64

import base64
def token_jwt(request,ref,username):
    try:

        # token_Set.DEFAULTS = {'ACCESS_TOKEN_LIFETIME': datetime.timedelta(minutes=15),
        #                       'SLIDING_TOKEN_LIFETIME': datetime.timedelta(minutes=15)
        #                       }
        if ref == 'LOGIN':

            datenow = str(datetime.datetime.now().strftime("%Y-%m-%d"))
            password = datenow + username[::-1]
            password = class1.converttoascii(password)

            headers = {"content-type": "application/json"}
            params = ''
            datas = json.dumps({"username":username,"password":"abcd","auth_pwd":password,"apitype":"Direct"})
            common.logger.error([{"LG_Tkn_PARAMS_username": username[0:3]}])
            common.logger.error([{"LG_Tkn_PARAMS_pass": password[0:3]}])
            common.logger.error([{"LG_Tkn_PARAMS_ip": ip[0:5]}])

            resp = requests.post("" + ip + "/token", params=params, data=datas, headers=headers,
                                 verify=False)
            common.logger.error([{"LG_Tkn_FullMsg": str(resp)}])
            token_data = json.loads(resp.content.decode("utf-8"))

            # token_data = json.loads(resp.content)   revert back to Original
            common.logger.error([{"LG_Tkn_status": resp.status_code}])
            ### Validations
            if token_data != '' and resp.status_code == 200 :
                access_token = token_data.get("access")
                refresh_token = token_data.get("refresh")
                access_expirytime = access_token.split('.')
                access_expirytime = access_expirytime[1]
                access_expirytime = base64.b64decode(access_expirytime +"==")
                access_expirytime = json.loads(access_expirytime)
                access_expirytime = access_expirytime.get("exp")
                access_expirytime = datetime.datetime.fromtimestamp(access_expirytime).strftime("%H:%M:%S")
                request.session["access_token"] = access_token

                request.session["refresh_token"] = refresh_token
                request.session["access_expirytime"] = access_expirytime
                refresh_expirytime = refresh_token.split('.')
                refresh_expirytime = refresh_expirytime[1]
                refresh_expirytime = base64.b64decode(refresh_expirytime + "==")
                refresh_expirytime = json.loads(refresh_expirytime)
                refresh_expirytime = refresh_expirytime.get("exp")
                refresh_expirytime = datetime.datetime.fromtimestamp(refresh_expirytime).strftime("%m/%d/%Y, %H:%M:%S")
                request.session["refresh_expirytime"] = refresh_expirytime
                common.logger.error([{"LG_Tkn_Success":"Generated"}])
                return 'SUCCESS'
            elif resp.status_code != 200:
                common.logger.error([{"LG_Tkn_status":"FAIL"}])
                return 'FAIL'


        elif ref =='CHECK':
            common.logger.error([{"LG_Check_var_1": str(datetime.datetime.now().strftime("%H:%M:%S"))}])
            common.logger.error([{"LG_Check_var_2": str(request.session["access_expirytime"])}])
            common.logger.error([{"LG_Check_var_3": str(datetime.datetime.now().strftime("%m/%d/%Y, %H:%M:%S"))}])
            common.logger.error([{"LG_Check_var_4": str(request.session["refresh_expirytime"])}])

            from datetime import datetime as datealter
            nowtime = datetime.datetime.now().strftime("%H:%M:%S")
            nowtime = datealter.strptime(nowtime,"%H:%M:%S")
            accessexpirttime = datealter.strptime(request.session["access_expirytime"],"%H:%M:%S")

            if nowtime.time() < accessexpirttime.time():
            # if datetime.datetime.now().strftime("%I:%M:%S") < request.session["access_expirytime"] :
                return request.session["access_token"]
            elif datetime.datetime.now().strftime("%m/%d/%Y, %H:%M:%S") < request.session["refresh_expirytime"]:
                common.logger.error([{"LG_Check_Logins": "BC"}])
                # utl.check_login(request)
                common.logger.error([{"LG_Check_Logins": "AC"}])
                headers = {"content-type": "application/json"}
                params = ''
                datas = json.dumps({"refresh":request.session["refresh_token"] })
                resp = requests.post("" + ip + "/api/token/refresh/", params=params, data=datas, headers=headers,
                                     verify=False)
                token_data = json.loads(resp.content.decode("utf-8"))
                access_token = token_data.get("access")
                access_expirytime = access_token.split('.')
                access_expirytime = access_expirytime[1]
                access_expirytime = base64.b64decode(access_expirytime +"==")
                access_expirytime = json.loads(access_expirytime)
                access_expirytime = access_expirytime.get("exp")
                access_expirytime = datetime.datetime.fromtimestamp(access_expirytime).strftime("%H:%M:%S")
                request.session["access_token"] = access_token
                request.session["access_expirytime"] = access_expirytime
                common.logger.error([{"LG_Check_tkn_checked": "Checked"}])
                return access_token
            else:
                common.logger.error([{"LG_Date_Check_Else": ref}])
                request.session.flush()
                return utility.error_403(request)
    except Exception as e:
        common.logger.error([{"LG_Tkn_Exeption": str(e)}])
        common.logger.error([{"LG_Tkn_Exeption_1": str(datetime.datetime.now().strftime("%H:%M:%S"))}])
        common.logger.error([{"LG_Tkn_Exeption_2": str(request.session["access_expirytime"])}])
        return 'FAIL'


def welcomeIndex(request):
    utl.check_pointaccess(request)
    return render(request, "welcome.html")


def update_personal_index(request):
    utl.check_pointaccess(request)
    return render(request, "update_personal_index.html")


def StateAdd(request):
    utl.check_authorization(request)
    utl.check_pointaccess(request)
    return render(request, "Shared/State_popup.html")

def pdfviewer(request):
    utl.check_authorization(request)
    utl.check_pointaccess(request)
    return render(request, "Shared/pdfviewier.html")

def menuList(request):
    utl.check_authorization(request)
    utl.check_pointaccess(request)
    if request.method == 'GET':
        emp_gid = decry_data(request.session['Emp_gid'])
        result = mCore.menulist(emp_gid)
        if (result[1][0] == 'FOUND'):
            output = result[0]
            return JsonResponse(json.dumps(output), safe=False)
    else:
        request.session.flush()
        return render(request, "Shared/bigFlowLogin.html")

def loaderspinnerIndex(request):
    utl.check_pointaccess(request)
    return render(request, "Shared/loaderSpinner.html")


def customercuecardIndex(request):
    utl.check_authorization(request)
    utl.check_pointaccess(request)
    return render(request, "Sidepanel/customer_cuecard.html")


def customercuecardviewIndex(request):
    utl.check_authorization(request)
    utl.check_pointaccess(request)
    return render(request, "Shared/customer_cuecardview.html")


def customersnapshotIndex(request):
    utl.check_authorization(request)
    utl.check_pointaccess(request)
    return render(request, "Sidepanel/customer_snapshot.html")


def customerentityoutcomeIndex(request):
    utl.check_authorization(request)
    utl.check_pointaccess(request)
    return render(request, "Sidepanel/customer_entityoutcome.html")


def customercreditapproveIndex(request):
    utl.check_authorization(request)
    utl.check_pointaccess(request)
    return render(request, "Sidepanel/customer_creditapprove.html")


def customeractivitytrendIndex(request):
    utl.check_authorization(request)
    utl.check_pointaccess(request)
    return render(request, "Sidepanel/customer_activitytrend.html")


def customersnapstviewIndex(request):
    utl.check_authorization(request)
    utl.check_pointaccess(request)
    return render(request, "Shared/customer_snapshtview.html")


def customerentityviewIndex(request):
    utl.check_authorization(request)
    utl.check_pointaccess(request)
    return render(request, "Shared/customer_entityview.html")


def customeractivitytrendviewIndex(request):
    utl.check_authorization(request)
    utl.check_pointaccess(request)
    return render(request, "Shared/customer_activitytrendview.html")


def customercreditapproveviewIndex(request):
    utl.check_authorization(request)
    utl.check_pointaccess(request)
    return render(request, "Shared/customer_creditapproveview.html")


def commentviewindex(request):
    utl.check_authorization(request)
    utl.check_pointaccess(request)
    return render(request, "Shared/comment.html")


def viewDetailsIndex(request):
    utl.check_authorization(request)
    utl.check_pointaccess(request)
    return render(request, "Shared/viewDetails.html")


def commondispatch(request):
    utl.check_authorization(request)
    utl.check_pointaccess(request)
    return render(request, "Shared/commondispatch.html")


def customerSales(request):
    utl.check_authorization(request)
    utl.check_pointaccess(request)
    if request.method == 'GET':
        if (request.GET['todate'] != request.GET['fromdate']):
            ddd = (request.GET['todate'])
            today = datetime.datetime.strptime(ddd, "%d/%m/%Y")
            fdate = datetime.date(today.year, today.month, 1)
            # tdate = fdate + relativedelta(months=-11)
            # teee=relativedelta(dt1=fdate,dt2=tdate)
            temp = fdate
            header = []
            for x in range(12):
                data = {'month': temp.month, 'year': temp.year, 'month_year': str(temp.month) + '-' + str(temp.year)}
                temp = temp + relativedelta(months=-1)
                header.append(data)
            # return JsonResponse(header, safe=False)
            mMaster.action = 'customerwisesale'
            mMaster.name = ''
            mMaster.jsonData = '{"customer_gid":' + request.GET['cust_gid'] + ',"fromdate":"' + common.convertDate(
                request.GET['fromdate']) + '","todate":"' + common.convertDate(request.GET['todate']) + '"}'
            df_custsales = mMaster.getcustomersales()
            mMaster.entity_gid = decry_data(request.session['Entity_gid'])
            df_product = (df_custsales[['product_gid', 'product_name']]).groupby(['product_gid', 'product_name']).size().reset_index();
        else:
            today = datetime.date.today()
            fdate = datetime.date(today.year, today.month, 1)
            # tdate = fdate + relativedelta(months=-11)
            # teee=relativedelta(dt1=fdate,dt2=tdate)
            temp = fdate
            header = []
            for x in range(12):
                data = {'month': temp.month, 'year': temp.year, 'month_year': str(temp.month) + '-' + str(temp.year)}
                temp = temp + relativedelta(months=-1)
                header.append(data)
            # return JsonResponse(header, safe=False)
            mMaster.action = 'customerwisesale'
            mMaster.name = ''
            mMaster.jsonData = '{"customer_gid":' + request.GET[
                'cust_gid'] + ',"fromdate":"' + '' + '","todate":"' + '' + '"}'
            mMaster.entity_gid = decry_data(request.session['Entity_gid'])
            df_custsales = mMaster.getcustomersales()
            df_product = (df_custsales[['product_gid', 'product_name']]) \
                .groupby(['product_gid', 'product_name']).size().reset_index();
        sales_details = []
        for x, item in df_product.iterrows():
            details = {'product_gid': item['product_gid'], 'product_name': item['product_name']}
            for y in header:
                month_dtl = {}
                d = df_custsales[
                    (df_custsales['sales_month'] == y['month']) & (df_custsales['sales_year'] == y['year']) & (
                            df_custsales['product_gid'] == item['product_gid']
                    )]
                if d.empty:
                    month_dtl['sales_qty'] = ''
                    month_dtl['sales_amt_wogst'] = ''
                    details[y['month_year']] = month_dtl
                else:
                    month_dtl['sales_qty'] = d['sales_qty'].iloc[0]
                    month_dtl['sales_amt_wogst'] = d['sales_amt_wogst'].iloc[0]
                    details[y['month_year']] = month_dtl
            sales_details.append(details)
        datadetails = {'customer_name': df_custsales['customer_name'].iloc[0],
                       'employee_name': df_custsales['employee_name'].iloc[0], 'sales_details': sales_details,
                       'headers': header}
        return JsonResponse(datadetails, safe=False)


def dp_get(request):
    utl.check_authorization(request)
    utl.check_pointaccess(request)
    if request.method == 'GET':
        if (request.GET['todate'] != request.GET['fromdate']):
            ddd = (request.GET['todate'])
            today = datetime.datetime.strptime(ddd, "%d/%m/%Y")
            fdate = datetime.date(today.year, today.month, 1)
            # tdate = fdate + relativedelta(months=-11)
            # teee=relativedelta(dt1=fdate,dt2=tdate)
            temp = fdate
            header = []
            for x in range(12):
                data = {'month': temp.month, 'year': temp.year, 'month_year': str(temp.month) + '-' + str(temp.year)}
                temp = temp + relativedelta(months=-1)
                header.append(data)
            # return JsonResponse(header, safe=False)
            mMaster.action = 'dpprice'
            mMaster.name = ''
            mMaster.jsonData = '{"customer_gid":' + request.GET['cust_gid'] + ',"fromdate":"' + common.convertDate(
                request.GET['fromdate']) + '","todate":"' + common.convertDate(request.GET['todate']) + '"}'
            mMaster.entity_gid = decry_data(request.session['Entity_gid'])
            df_custdp = mMaster.getcustomersales()
            df_product = (df_custdp[['product_gid', 'product_name']]) \
                .groupby(['product_gid', 'product_name']).size().reset_index();
        else:
            today = datetime.date.today()
            fdate = datetime.date(today.year, today.month, 1)
            temp = fdate
            header = []
            for x in range(12):
                data = {'month': temp.month, 'year': temp.year, 'month_year': str(temp.month) + '-' + str(temp.year)}
                temp = temp + relativedelta(months=-1)
                header.append(data)
            # return JsonResponse(header, safe=False)
            mMaster.action = 'dpprice'
            mMaster.name = ''
            mMaster.jsonData = '{"customer_gid":' + request.GET[
                'cust_gid'] + ',"fromdate":"' + '  ' + '","todate":"' + '' + '"}'
            mMaster.entity_gid = decry_data(request.session['Entity_gid'])
            df_custdp = mMaster.getcustomersales()
            df_product = (df_custdp[['product_gid', 'product_name']]) \
                .groupby(['product_gid', 'product_name']).size().reset_index();
        dp_details = []
        for x, item in df_product.iterrows():
            detail = {'product_gid': item['product_gid'], 'product_name': item['product_name']}
            for y in header:
                month_dtl = {}
                d = df_custdp[
                    (df_custdp['sales_month'] == y['month']) & (df_custdp['sales_year'] == y['year']) & (
                            df_custdp['product_gid'] == item['product_gid']
                    )]
                if d.empty:
                    month_dtl['dpamount'] = ''
                    month_dtl['sales_amt_wgst'] = ''
                    detail[y['month_year']] = month_dtl
                else:
                    month_dtl['dpamount'] = d['dpamount'].iloc[0]
                    month_dtl['sales_amt_wgst'] = d['dpamount'].iloc[0] - d['sales_amt_wogst'].iloc[0]
                    detail[y['month_year']] = month_dtl
            dp_details.append(detail)
        datadetails = {'customer_name': df_custdp['customer_name'].iloc[0],
                       'employee_name': df_custdp['employee_name'].iloc[0], 'dp_details': dp_details,
                       'headers': header}
        return JsonResponse(datadetails, safe=False)


def get_categorygroup(request):
    utl.check_authorization(request)
    utl.check_pointaccess(request)
    if request.method == 'GET':
        obj_cat = mMasters.Masters()
        obj_cat.table_name = 'custcategory'
        obj_cat.entity_gid = decry_data(request.session['Entity_gid'])
        dict_custgrp = obj_cat.get_Masters()
        return JsonResponse(json.dumps(dict_custgrp), safe=False)


def outstnd_get(request):
    utl.check_authorization(request)
    utl.check_pointaccess(request)
    if request.method == 'GET':
        if (request.GET['todate'] != request.GET['fromdate']):
            ddd = (request.GET['todate'])
            today = datetime.datetime.strptime(ddd, "%d/%m/%Y")
            fdate = datetime.date(today.year, today.month, 1)
            # tdate = fdate + relativedelta(months=-11)
            # teee=relativedelta(dt1=fdate,dt2=tdate)
            temp = fdate
            header = []
            for x in range(12):
                data = {'month': temp.month, 'year': temp.year, 'month_year': str(temp.month) + '-' + str(temp.year)}
                temp = temp + relativedelta(months=-1)
                header.append(data)
            # return JsonResponse(header, safe=False)
            mMaster.action = 'outstanding'
            mMaster.name = ''
            mMaster.jsonData = '{"customer_gid":' + request.GET['cust_gid'] + ',"fromdate":"' + common.convertDate(
                request.GET['fromdate']) + '","todate":"' + common.convertDate(request.GET['todate']) + '"}'
            mMaster.entity_gid = decry_data(request.session['Entity_gid'])
            df_custdp = mMaster.getcustomersales()
            df_product = (df_custdp[['customer_gid', 'customer_name']]) \
                .groupby(['customer_gid', 'customer_name']).size().reset_index();
        else:
            today = datetime.date.today()
            fdate = datetime.date(today.year, today.month, 1)
            temp = fdate
            header = []
            for x in range(12):
                data = {'month': temp.month, 'year': temp.year, 'month_year': str(temp.month) + '-' + str(temp.year)}
                temp = temp + relativedelta(months=-1)
                header.append(data)
            mMaster.action = 'outstanding'
            mMaster.name = ''
            mMaster.jsonData = '{"customer_gid":' + request.GET[
                'cust_gid'] + ',"fromdate":"' + '' + '","todate":"' + '' + '"}'
            mMaster.entity_gid =decry_data(request.session['Entity_gid'])
            df_custdp = mMaster.getcustomersales()
            df_product = (df_custdp[['customer_gid', 'customer_name']]) \
                .groupby(['customer_gid', 'customer_name']).size().reset_index();
        os_details = []
        for x, item in df_product.iterrows():
            details = {'customer_gid': item['customer_gid'], 'customer_name': item['customer_name']}
            for y in header:
                month_dtl = {}
                d = df_custdp[
                    (df_custdp['sales_month'] == y['month']) & (df_custdp['sales_year'] == y['year']) & (
                            df_custdp['customer_gid'] == item['customer_gid']
                    )]
                if d.empty:
                    month_dtl['outstanding_amt'] = ''
                    details[y['month_year']] = month_dtl
                else:
                    month_dtl['outstanding_amt'] = d['outstanding_amt'].iloc[0]
                    details[y['month_year']] = month_dtl
                    os_details.append(details)
        datadetails = {'customer_name': df_custdp['customer_name'].iloc[0], 'os_details': os_details,
                       'headers': header}
        return JsonResponse(datadetails, safe=False)


def convertDate(stringDate):
    return datetime.datetime.strptime(stringDate, "%d/%m/%Y").strftime("%Y-%m-%d")


def payred_get(request):
    utl.check_authorization(request)
    utl.check_pointaccess(request)
    if request.method == 'GET':
        if (request.GET['todate'] != request.GET['fromdate']):
            ddd = (request.GET['todate'])
            today = datetime.datetime.strptime(ddd, "%d/%m/%Y")
            fdate = datetime.date(today.year, today.month, 1)
            temp = fdate
            header = []
            for x in range(12):
                data = {'month': temp.month, 'year': temp.year, 'month_year': str(temp.month) + '-' + str(temp.year)}
                temp = temp + relativedelta(months=-1)
                header.append(data)
            mMaster.action = 'payableamount'
            mMaster.name = ''
            mMaster.jsonData = '{"customer_gid":' + request.GET['cust_gid'] + ',"fromdate":"' + common.convertDate(
                request.GET['fromdate']) + '","todate":"' + common.convertDate(request.GET['todate']) + '"}'
            mMaster.entity_gid = decry_data(request.session['Entity_gid'])
            df_custdp = mMaster.getcustomersales()
            df_product = (df_custdp[['customer_gid', 'customer_name']]) \
                .groupby(['customer_gid', 'customer_name']).size().reset_index();
        else:
            today = datetime.date.today()
            fdate = datetime.date(today.year, today.month, 1)
            temp = fdate
            header = []
            for x in range(12):
                data = {'month': temp.month, 'year': temp.year, 'month_year': str(temp.month) + '-' + str(temp.year)}
                temp = temp + relativedelta(months=-1)
                header.append(data)
            mMaster.action = 'payableamount'
            mMaster.name = ''
            mMaster.jsonData = '{"customer_gid":' + request.GET[
                'cust_gid'] + ',"fromdate":"' + '' + '","todate":"' + '' + '"}'
            mMaster.entity_gid = decry_data(request.session['Entity_gid'])
            df_custdp = mMaster.getcustomersales()
            df_product = (df_custdp[['customer_gid', 'customer_name']]) \
                .groupby(['customer_gid', 'customer_name']).size().reset_index();
        PayRec_details = []
        for x, item in df_product.iterrows():
            details = {'customer_gid': item['customer_gid'], 'customer_name': item['customer_name']}
            for y in header:
                month_dtl = {}
                d = df_custdp[
                    (df_custdp['sales_month'] == y['month']) & (df_custdp['sales_year'] == y['year']) & (
                            df_custdp['customer_gid'] == item['customer_gid']
                    )]
                if d.empty:
                    month_dtl['payableamt'] = ''
                    details[y['month_year']] = month_dtl
                else:
                    month_dtl['payableamt'] = d['payableamt'].iloc[0]
                    details[y['month_year']] = month_dtl
            PayRec_details.append(details)
        datadetails = {'customer_name': df_custdp['customer_name'].iloc[0], 'PayRec_details': PayRec_details,
                       'headers': header}
        return JsonResponse(datadetails, safe=False)


def getentityget(request):
    utl.check_authorization(request)
    utl.check_pointaccess(request)
    if request.method == 'GET':
        today = datetime.date.today()
        f_date = datetime.date(today.year, 1, 1)
        t_date = f_date + relativedelta(months=11)
        if (request.GET['todate'] != request.GET['fromdate']):
            d = common.convertDateTime(request.GET['fromdate'])
            t = common.convertDateTime(request.GET['todate'])
            f_date = datetime.date(d.year, 1, 1)
            t_date = datetime.date(t.year, 12, 31)
        year_dif = (t_date.year - f_date.year) + 1
        detail_list = []
        mMaster.action = 'ALL'
        mMaster.type = ""
        mMaster.jsonData = '{"customer_gid":' + request.GET[
            'cust_gid'] + ',"fromdate":"' + str(f_date) + '","todate":"' + str(t_date) + '"}'
        mMaster.entity_gid = decry_data(request.session['Entity_gid'])
        df_custdp = mMaster.getentity()
        temp = f_date
        for x in range(0, year_dif):
            detail = {}
            detail = {'Year': temp.year}
            highestval = 0
            highestcol = 0
            highestout = 0
            for x in range(12):
                month_dtl = {}
                # for sales
                sale = df_custdp[0][
                    (df_custdp[0]['sales_month'] == temp.month) & (df_custdp[0]['sales_year'] == temp.year)]
                if sale.empty:
                    month_dtl['sales_amt_wogst'] = ''
                else:
                    month_dtl['sales_amt_wogst'] = (sale['sales_amt_wogst'].iloc[0])
                    if highestval < month_dtl['sales_amt_wogst']:
                        highestval = month_dtl['sales_amt_wogst']
                # for collection
                collection = df_custdp[1][
                    (df_custdp[1]['sales_month'] == temp.month) & (df_custdp[1]['sales_year'] == temp.year)]
                if collection.empty:
                    month_dtl['payableamt'] = ''
                else:
                    month_dtl['payableamt'] = (collection['payableamt'].iloc[0])
                    if highestcol < month_dtl['payableamt']:
                        highestcol = month_dtl['payableamt']
                # for outstanding
                outstanding = df_custdp[2][
                    (df_custdp[2]['sales_month'] == temp.month) & (df_custdp[2]['sales_year'] == temp.year)]
                if outstanding.empty:
                    month_dtl['outstanding_amt'] = ''
                else:
                    month_dtl['outstanding_amt'] = (outstanding['outstanding_amt'].iloc[0])
                    if highestout < (outstanding['outstanding_amt'].iloc[0]):
                        highestout = (outstanding['outstanding_amt'].iloc[0])
                detail[temp.month] = month_dtl
                temp = temp + relativedelta(months=1)
            detail['highestval'] = {'highestval': highestval}
            detail['highestcol'] = {'highestcol': highestcol}
            detail['highestout'] = {'highestout': highestout}
            detail_list.append(detail)
    return JsonResponse(detail_list, safe=False)


def getapprove(request):
    utl.check_authorization(request)
    utl.check_pointaccess(request)
    if request.method == 'GET':
        objenti = mFET.FET_model()
        objenti.action = 'OutstandingCustomer'
        objenti.customer_gid = request.GET['cust_gid']
        objenti.limit = 30
        result_ent = objenti.get_FEToutstanding_fet()
        jdata = result_ent.to_json(orient='records')
        return JsonResponse(jdata, safe=False)


def getproposed(request):
    utl.check_authorization(request)
    utl.check_pointaccess(request)
    if request.method == 'GET':
        objenti = mMasters.Masters()
        objenti.action = 'proposedbill'
        objenti.type = ""
        objenti.jsonData = ' {"customer_gid": ' + request.GET['cust_gid'] + ',"soheader_gid":' + request.GET[
            'soheader_gid'] + '}'
        objenti.entity_gid = decry_data(request.session['Entity_gid'])
        result_ent = objenti.getcreditapprv()
        jdata = result_ent.to_json(orient='records')
        return JsonResponse(jdata, safe=False)


# def pendingsmry(request):
#     if request.method == 'GET':
#         obj_pendingsmry = mMasters.Masters()
#         obj_pendingsmry.customer_gid = request.GET['cust_gid']
#         df_pendingsmry = obj_pendingsmry.get_pendingsummary_get()
#         return JsonResponse(json.dumps(df_pendingsmry), safe=False)
def pendingsmry(request):
    utl.check_authorization(request)
    utl.check_pointaccess(request)
    if request.method == 'GET':
        obj_pendingsmry = mMasters.Masters()
        obj_pendingsmry.action = 'Pendingsummary'
        obj_pendingsmry.customer_gid = request.GET['cust_gid']
        result_ent = obj_pendingsmry.get_pendingsummary_get()
        jdata = result_ent.to_json(orient='records')
        return JsonResponse(jdata, safe=False)


def snapsales(request):
    utl.check_authorization(request)
    utl.check_pointaccess(request)
    if request.method == 'GET':
        if (request.GET['todate'] != request.GET['fromdate']):
            ddd = (request.GET['todate'])
            today = datetime.datetime.strptime(ddd, "%d/%m/%Y")
            fdate = datetime.date(today.year, today.month, 1)
            # tdate = fdate + relativedelta(months=-11)
            # teee=relativedelta(dt1=fdate,dt2=tdate)
            temp = fdate
            header = []
            for x in range(12):
                data = {'month': temp.month, 'year': temp.year, 'month_year': str(temp.month) + '-' + str(temp.year)}
                temp = temp + relativedelta(months=-1)
                header.append(data)
            # return JsonResponse(header, safe=False)
            mMaster.action = 'customerwisesale'
            mMaster.name = ''
            mMaster.jsonData = '{"customer_gid":' + request.GET['cust_gid'] + ',"fromdate":"' + common.convertDate(
                request.GET['fromdate']) + '","todate":"' + common.convertDate(request.GET['todate']) + '"}'
            mMaster.entity_gid = decry_data(request.session['Entity_gid'])
            df_custsales = mMaster.getcustomersales()
            df_product = (df_custsales[['customer_gid', 'customer_name']]) \
                .groupby(['customer_gid', 'customer_name']).size().reset_index();
        else:
            today = datetime.date.today()
            fdate = datetime.date(today.year, today.month, 1)
            # tdate = fdate + relativedelta(months=-11)
            # teee=relativedelta(dt1=fdate,dt2=tdate)
            temp = fdate
            header = []
            for x in range(12):
                data = {'month': temp.month, 'year': temp.year, 'month_year': str(temp.month) + '-' + str(temp.year)}
                temp = temp + relativedelta(months=-1)
                header.append(data)
            # return JsonResponse(header, safe=False)
            mMaster.action = 'customerwisesale'
            mMaster.name = ''
            mMaster.jsonData = '{"customer_gid":' + request.GET[
                'cust_gid'] + ',"fromdate":"' + '' + '","todate":"' + '' + '"}'
            mMaster.entity_gid = decry_data(request.session['Entity_gid'])
            df_custsales = mMaster.getcustomersales()
            df_product = (df_custsales[['customer_gid', 'customer_name']]) \
                .groupby(['customer_gid', 'customer_name']).size().reset_index();
        sales_details = []
        for x, item in df_product.iterrows():
            details = {'customer_gid': item['customer_gid'], 'customer_name': item['customer_name']}
            for y in header:
                month_dtl = {}
                d = df_custsales[
                    (df_custsales['sales_month'] == y['month']) & (df_custsales['sales_year'] == y['year']) & (
                            df_custsales['customer_gid'] == item['customer_gid']
                    )]
                if d.empty:
                    month_dtl['sales_qty'] = ''
                    month_dtl['sales_amt_wgst'] = ''
                    details[y['month_year']] = month_dtl
                else:
                    month_dtl['sales_qty'] = d['sales_qty'].iloc[0]
                    month_dtl['sales_amt_wgst'] = d['sales_amt_wgst'].iloc[0]
                    details[y['month_year']] = month_dtl
            sales_details.append(details)
        datadetails = {'customer_name': df_custsales['customer_name'].iloc[0],
                       'employee_name': df_custsales['employee_name'].iloc[0], 'sales_details': sales_details,
                       'headers': header}
        return JsonResponse(datadetails, safe=False)


def getactivity(request):
    utl.check_authorization(request)
    utl.check_pointaccess(request)
    if request.method == 'GET':
        ddd = (request.GET['todate'])
        today = datetime.datetime.strptime(ddd, "%Y-%m-%d")
        fdate = datetime.date(today.year, today.month, 1)
        temp = fdate
        header = []
        header_month = []
        for x in range(120):
            data = {'month': temp.month, 'year': temp.year, 'month_year': str(temp.month) + '-' + str(temp.year)}
            temp = temp + relativedelta(months=1)
            header.append(data)
        mMaster.action = 'SALES'
        mMaster.entity_gid =decry_data(request.session['Entity_gid'])
        mMaster.jsonData = '{"customer_gid":' + request.GET['cust_gid'] + '}'
        df_sales = mMaster.getactivitytrend()
        df_product = (df_sales[['Activity_Year']]) \
            .groupby(['Activity_Year']).size().reset_index();
        for x in range(12):
            data = {'month': x + 1}
            header_month.append(data)
    sales_details = []
    for x, item in df_product.iterrows():
        details = {'Activity_Year': str(item['Activity_Year'])}
        for y in header:
            month_dtl = {}
            if item['Activity_Year'] == y['year']:
                d = df_sales[
                    (df_sales['period'] == y['month']) & (df_sales['Activity_Year'] == y['year'])
                    ]
                if d.empty:
                    month_dtl['cuecards_value'] = ''
                    details[y['month']] = month_dtl
                else:
                    month_dtl['cuecards_value'] = d['cuecards_value'].iloc[0]
                    details[y['month']] = month_dtl
        sales_details.append(details)
    datadetails = {'customer_name': df_sales['customer_name'].iloc[0],
                   'sales_details': sales_details,
                   'headers': header,
                   'header_month': header_month}
    return JsonResponse(datadetails, safe=False)


def getactivitycol(request):
    utl.check_authorization(request)
    utl.check_pointaccess(request)
    if request.method == 'GET':
        ddd = (request.GET['todate'])
        today = datetime.datetime.strptime(ddd, "%Y-%m-%d")
        fdate = datetime.date(today.year, today.month, 1)
        temp = fdate
        header = []
        header_month = []
        for x in range(120):
            data = {'month': temp.month, 'year': temp.year, 'month_year': str(temp.month) + '-' + str(temp.year)}
            temp = temp + relativedelta(months=1)
            header.append(data)
        mMaster.action = 'PAYMENT'
        mMaster.entity_gid = decry_data(request.session['Entity_gid'])
        mMaster.jsonData = '{"customer_gid":' + request.GET['cust_gid'] + '}'
        df_sales = mMaster.getactivitytrend()
        df_product = (df_sales[['Activity_Year']]) \
            .groupby(['Activity_Year']).size().reset_index();
        for x in range(12):
            data = {'month': x + 1}
            header_month.append(data)
    collection_details = []
    for x, item in df_product.iterrows():
        details = {'Activity_Year': str(item['Activity_Year'])}
        for y in header:
            month_dtl = {}
            if item['Activity_Year'] == y['year']:
                d = df_sales[
                    (df_sales['period'] == y['month']) & (df_sales['Activity_Year'] == y['year'])
                    ]
                if d.empty:
                    month_dtl['cuecards_value'] = ''
                    details[y['month']] = month_dtl
                else:
                    month_dtl['cuecards_value'] = d['cuecards_value'].iloc[0]
                    details[y['month']] = month_dtl
        collection_details.append(details)
    datadetails = {'customer_name': df_sales['customer_name'].iloc[0],
                   'collection_details': collection_details,
                   'headers': header,
                   'header_month': header_month}
    return JsonResponse(datadetails, safe=False)


def setPosition(request):
    utl.check_authorization(request)
    utl.check_pointaccess(request)
    if request.method == 'GET':
        jsondata = json.loads(request.GET['details'])
        obj_position = mCore.login()
        obj_position.action = 'INSERT'
        obj_position.latlong_gid = 0
        obj_position.employee_gid = request.session['Emp_gid']
        obj_position.latitude = jsondata.get('latitude')
        obj_position.longitude = jsondata.get('longitude')
        obj_position.entity_gid = decry_data(request.session['Entity_gid'])
        obj_position.create_by = decry_data(request.session['Emp_gid'])
        df_position = mcommon.outputReturn(obj_position.setposition(), 0)
        return JsonResponse(df_position, safe=False)


def getposition(request):
    utl.check_authorization(request)
    utl.check_pointaccess(request)
    if request.method == 'GET':
        obj_poisionget = mCore.login()
        obj_poisionget.action = request.GET['action']
        obj_poisionget.employee_gid = decry_data(request.session['Emp_gid'])
        obj_poisionget.from_date = mcommon.convertDate(request.GET['date'])
        if request.GET['todate'] == '':
            obj_poisionget.to_date = ''
        else:
            obj_poisionget.to_date = mcommon.convertDate(request.GET['todate'])
        obj_poisionget.entity_gid = decry_data(request.session['Entity_gid'])
        df_position = obj_poisionget.getposition()
        # df_position.rename(columns={'latlong_latitude': 'tesse', 'oldName2': 'newName2'}, inplace=True)
        jdata = df_position.to_json(orient='records')
        return JsonResponse(json.loads(jdata), safe=False)


def getdayroute(request):
    utl.check_authorization(request)
    utl.check_pointaccess(request)
    if request.method == 'GET':
        obj_dayrouteget = mMasters.Masters()
        obj_dayrouteget.action = request.GET['action']
        obj_dayrouteget.employee_gid = request.GET['emp_gid']
        obj_dayrouteget.from_date = request.GET['date']
        if request.GET['todate'] == '':
            obj_dayrouteget.to_date = ''
        else:
            obj_dayrouteget.to_date = request.GET['todate']
        obj_dayrouteget.entity_gid = decry_data(request.session['Entity_gid'])
        df_dayroute = obj_dayrouteget.dayrouteget()
        # df_position.rename(columns={'latlong_latitude': 'tesse', 'oldName2': 'newName2'}, inplace=True)
        jdata = df_dayroute.to_json(orient='records')
        return JsonResponse(json.loads(jdata), safe=False)


def setDayroute(request):
    utl.check_authorization(request)
    utl.check_pointaccess(request)
    if request.method == 'GET':
        jsondata = json.loads(request.GET['day'])
        obj_position = mMasters.Masters()
        obj_position.action = request.GET['action']
        obj_position.jsonData = jsondata
        obj_position.entity_gid = decry_data(request.session['Entity_gid'])
        obj_position.create_by = decry_data(request.session['Emp_gid'])
        df_position = obj_position.dayrouteset()
        return JsonResponse(df_position, safe=False)


def routedaymap(request):
    utl.check_authorization(request)
    utl.check_pointaccess(request)
    if request.method == 'GET':
        objenti = mMasters.Masters()
        objenti.action = 'ROUTE_DAYS'
        objenti.json_employee_gid = ' {"routeemp_gid": ' +decry_data( request.GET['emp_gid']) + '}'
        objenti.entity_gid = decry_data(request.session['Entity_gid'])
        result_ent = objenti.getRouteDtl()
        jdata = result_ent.to_json(orient='records')
        return JsonResponse(jdata, safe=False)


def employedaymap(request):
    utl.check_authorization(request)
    utl.check_pointaccess(request)
    if request.method == 'POST':
        obj_setroute = mMasters.Masters()
        jsondata = json.loads(request.body.decode('utf-8')).get('parms')
        obj_setroute.action = jsondata.get('action')
        obj_setroute.json_employee_gid = json.dumps(jsondata.get('emp_det'))
        obj_setroute.create_by = decry_data(request.session['Emp_gid'])
        obj_setroute.entity_gid =decry_data( request.session['Entity_gid'])
        out_message = mcommon.outputReturn(obj_setroute.setRouteDtl(), 1)
        return JsonResponse(out_message, safe=False)


def collectionperformanceIndex(request):
    utl.check_authorization(request)
    utl.check_pointaccess(request)
    return render(request, "report/collection_performance_monthwise.html")


def getcollectionperformance(request):
    utl.check_authorization(request)
    utl.check_pointaccess(request)
    if request.method == 'GET':
        obj_col_per = mCore.login()
        obj_col_per.action = request.GET['action']
        obj_col_per.type = request.GET['type']
        obj_col_per.from_date = common.convertDate(request.GET['f_date'])
        obj_col_per.to_date = common.convertDate(request.GET['t_date'])
        obj_col_per.customer_gid = request.GET['cust_gid']
        obj_col_per.entity_gid = decry_data(request.session['Entity_gid'])
        out_message = obj_col_per.getcollectionperformance()
        jdata = out_message.to_json(orient='records')
        return JsonResponse(json.loads(jdata), safe=False)


def selectSupplierIndex(request):
    utl.check_authorization(request)
    utl.check_pointaccess(request)
    return render(request, "Shared/select_suppliers.html")


def selectproductIndex(request):
    utl.check_authorization(request)
    utl.check_pointaccess(request)
    return render(request, "Shared/select_product.html")


def selectEmployeeIndex(request):
    utl.check_authorization(request)
    utl.check_pointaccess(request)
    return render(request, "Shared/select_employee.html")


def mastersync_employee_Data(request):
    params = mMasters.Masters()
    params.action = "Insert"
    params.jsonData = json.dumps({'masterscheduler_name': 'EMPLOYEE' + str(current_date.year) + '_' + str(
        current_date.month) + '' + '_' + str(current_date.day) + '',
                                  'masterscheduler_date': datetime.datetime.now().strftime("%Y-%m-%d"),
                                  'masterscheduler_type': 'EMPLOYEE'})
    params.json_classification = json.dumps({'Entity_Gid': 1})
    params.employee_gid = '0ADMIN'  # Hardcoded as per Maruthi instruction for Admin id bcz it runs without human interaction
    datas = params.common_for_scheduler()
    datas = "".join(datas)
    datas = datas.split(',')
    if datas[0] == 'SUCCESS':
        params = {"date": datas[1]}
        ip = common.memoapi_url()
        resp = requests.get("" + ip + "/usrserv/employee_get_sync", params=params, data="", headers="",
                            verify=False)
        data = json.loads(resp.content.decode("utf-8"))
        outmsg = data.get("data")
        outmsg = {"masterscheduler_id": datas[2], "ESM_EMP_Master": outmsg}
        params = mMasters.Masters()
        params.action = "Insert"
        params.type = "EMPLOYEE_SET"
        params.jsonData = json.dumps(outmsg)
        params.employee_gid = '0ADMIN'
        message = params.masterSync_Employee_data()
        if message[0] == 'SUCCESS':
            ld_dict = {"Message": "SUCCESS"}
        elif message[0] == 'FAILED':
            ld_dict = {"Message": "MESSAGE"}
        else:
            ld_dict = {"Message": 'ERROR_OCCURED.' + str(message)}
        return JsonResponse(ld_dict, safe=False)
sched.add_cron_job(mastersync_employee_Data, hour=2, minute=18)
#Scheduler for Mono_to_micro Master Sync
from Bigflow.Core.models import multisystem_sync_create,get_sync_ip
try:

    if(os.environ['sync_started']=='1'):
        os.environ.pop('sync_started')
        pass
except:
    multisystem_sync_create()
    ip_to_run=''
    try:
        ip_to_run = get_sync_ip()[0]
    except:
        Bigflow.Core.models.logger.error({"MASTERSYNC_API":'SP NOT ADDED'})
    curr_ip=socket.gethostbyname(socket.gethostname())
    os.environ['sync_started'] = '1'
    if(curr_ip==ip_to_run):
        sched.add_interval_job(Bigflow.Core.models.schedule_apiRun,minutes=45)
        Bigflow.Core.models.logger.error('MasterSync Scheduler job created')
    else:
        Bigflow.Core.models.logger.error([{'MASTERSYNC_APICALL':'SCHEDULED WILL RUN IN ALTERNATE SYSTEM'}])
# #Branch Data
def mastersync_branch_Data():
    params = mMasters.Masters()
    params.action = "Insert"
    params.jsonData = json.dumps({'masterscheduler_name': 'BRANCH' + str(current_date.year) + '_' + str(
        current_date.month) + '' + '_' + str(current_date.day) + '',
                                  'masterscheduler_date': datetime.datetime.now().strftime("%Y-%m-%d"),
                                  'masterscheduler_type': 'BRANCH'})
    params.json_classification = json.dumps({'Entity_Gid': 1})
    params.employee_gid = '0ADMIN'
    datas = params.common_for_scheduler()
    datas = "".join(datas)
    datas = datas.split(',')
    if datas[0] == 'SUCCESS':
        params = {"date": datas[1]}
        ip = common.memoapi_url()
        resp = requests.get("" + ip + "/usrserv/branch_get_sync", params=params, data='', headers="",
                            verify=False)
        data = json.loads(resp.content.decode("utf-8"))
        outmsg = data.get("data")
        for x in outmsg:
            if x['contact'] != []:
                landlin = x['contact']
                v = landlin[0]['landline']
                outm1 = v.replace("'", "")
                landlin[0]['landline'] = outm1
            if x['address'] != []:
                val = x['address']
                txt = val[0]['line1']
                txt1 = val[0]['line2']
                txt2 = val[0]['line3']
                outm = txt.replace("/n", "")
                outm = txt.replace("\'", "")
                outm = txt.replace("'", "")
                outm1 = txt1.replace("/n", "")
                outm1 = txt1.replace("\'", "")
                outm1 = txt1.replace("'", "")
                outm2 = txt2.replace("/n", "")
                outm2 = txt2.replace("\'", "")
                outm2 = txt2.replace("'", "")
                val[0]['line1'] = outm
                val[0]['line2'] = outm1
                val[0]['line3'] = outm2
        outmsg = {"masterscheduler_id": datas[2], "ESM_BRANCH_Master": outmsg}
        params = mMasters.Masters()
        params.action = "Insert"
        params.type = "BRANCH_SET"
        params.json_classification = json.dumps({"Entity_Gid": "1"})
        params.jsonData = json.dumps(outmsg)
        params.employee_gid = '0ADMIN'
        message = params.masterSync_BRANCH_SET()
        if message[0] == 'SUCCESS':
            ld_dict = {"Message": "SUCCESS"}
            return
        elif message[0] == 'FAILED':
            ld_dict = {"Message": "MESSAGE"}
            return
        else:
            ld_dict = {"Message": 'ERROR_OCCURED.' + str(message)}
            return
        return



sched.add_cron_job(mastersync_branch_Data, hour=15, minute=30)
# GL data
def mastersync_gl_Data():
    params = mMasters.Masters()
    params.action = "Insert"
    params.jsonData = json.dumps({'masterscheduler_name': 'GL' + str(current_date.year) + '_' + str(
        current_date.month) + '' + '_' + str(current_date.day) + '',
                                  'masterscheduler_date': datetime.datetime.now().strftime("%Y-%m-%d"),
                                  'masterscheduler_type': 'GL'})
    params.json_classification = json.dumps({'Entity_Gid': 1})
    params.employee_gid = '6493'
    datas = params.common_for_scheduler()
    # datas = "".join(datas)
    # datas = datas.split(',')
    if 1 == 1:
        url = common.master_sync()
        employeeGid = '6493'
        # generated_token_data = master_sync_Data_("GET","get_data",employeeGid)
        # bearerToken = generated_token_data.get("DATA")[0].get("clienttoken_name")
        # headers = {"Content-Type": "application/javascript", "Authorization": "Bearer"+" " +bearerToken}
        params = {"date": '1999-12-29'}
        resp = requests.get("http://127.0.0.1:8000/usrserv/gl_list_all", params=params, data="", headers="",
                            verify=False)
        data = json.loads(resp.content.decode("utf-8"))
        outmsg = data.get("data")
        outmsg = {"masterscheduler_id": '122', "ESM_EMP_Master": outmsg}
        params = mMasters.Masters()
        params.action = "Insert"
        params.type = "GL_SET"
        params.jsonData = json.dumps(outmsg)
        params.employee_gid = '6493'
        message = params.masterSync_GL_SET()
        if message[0] == 'SUCCESS':
            ld_dict = {"Message": "SUCCESS"}
        elif message[0] == 'FAILED':
            ld_dict = {"Message": "MESSAGE"}
        else:
            ld_dict = {"Message": 'ERROR_OCCURED.' + str(message)}
        return


# sched.add_cron_job(mastersync_gl_Data, hour=5, minute=40)



def master_sync_Data_(action, type, emp_gid):
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
            obj_.jsonData = json.dumps({"clienttoken_name": access_token, "clienttoken_expiry": token_expires,
                                        "clienttoken_user": "vsolv", "clienttoken_pwd": "12345",
                                        "create_by": emp_gid})
            message = obj_.mastersync_set()
            if message[0] == 'SUCCESS':
                ld_dict = {"DATA": [{'clienttoken_name': access_token}],
                           "MESSAGE": 'SUCCESS'}
                return ld_dict
    except Exception as e:
        return ({"MESSAGE": "ERROR_OCCURED" + str(e)})

import boto3
from botocore.exceptions import ClientError
def sending_mail(mail_data,mail_id,Mail_subject):
    sendermail = common.senderemail()
    SENDER = "Karur Vysya Bank <" + sendermail + ">"
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




def version_get(request):
    token = jwt.token(request)
    headers = {"content-type": "application/json", "Authorization": "" + token + ""}
    params = {"Entity_gid": decry_data(request.session['Entity_gid']),
              "Version_flag": "W",
              "Action": "GET"
              }
    resp = requests.get("" + ip + "/Release_Version_Get", params=params, data={}, headers=headers,
                        verify=False)
    response = resp.content.decode("utf-8")
    data = json.loads(response)
    if data.get('MESSAGE') == "FOUND":
        return JsonResponse(data)
    else :
        return JsonResponse({"MESSAGE":"NOT FOUND","DATA":[{"version_no": ""}]})
