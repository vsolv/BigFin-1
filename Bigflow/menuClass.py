import datetime
import json
import os
import logging
import sys

import boto3
import requests
import Bigflow.Core.models as common
from django import template
from django.http import Http404
from django.shortcuts import render

from Bigflow.Core.models import decrpt as decry_data

from Bigflow.Core import class1, models

from Bigflow.settings import BASE_DIR
from django.core.exceptions import PermissionDenied
register = template.Library()


class utility():
    FCMHeader = {"content-type": "application/json",
                 "Authorization": "key= AAAAg_4O2LM:APA91bEulwoPVA7IqL1nnW1aRim8-4o4-L3BwtHa7gAJN-y9KHZTUPe6MXsT-HbeorZIlGUJmlFWOFKARMIzGL4JbzehiFNHDWdDgJoHd7kUK7uI5vLopVD_aw-LMJc_ZOBS17r1ixQC"
                 }
    FCMServerIP = "https://fcm.googleapis.com/fcm/send"

    @staticmethod
    def check_authorization(request):
        #tew = request.path.split("/")[1]
        try:
            menu = request.path[1:-1]
            obj_check_detail = class1.login()
            if 'Emp_gid' not in request.session:
                return utility.error_403(request)
            obj_check_detail.employee_gid = decry_data(request.session['Emp_gid'])
            obj_check_detail.action = menu
            obj_check_detail.entity_gid = decry_data(request.session['Entity_gid'])
            obj_check_detail.create_by = decry_data(request.session['Emp_gid'])
            out_msg = obj_check_detail.get_url()

            if out_msg != 'FOUND':
                return request
            elif (out_msg == 'NOT_FOUND'):
                # utility.set_error_log('Forbidden',
                #                       ' Forbidden by Employee ID = ' + str(
                #                           request.session['Emp_gid']) + ' - Employee Name = ' +
                #                       request.session['Emp_name'])
                common.logger.error(menu + ' is Forbidden for Emp Id ' + str(
                                          decry_data(request.session['Emp_gid'])) + ' - Employee Name = ' +
                                      request.session['Emp_name'])
                request.session.flush()
                request.session['Emp_name'] = 'dummy'
                return
            else:
                request.session.flush()
                return utility.error_403(request)
        except Exception as e:
            common.logger.error(e)
            raise Http404(str(e))
    # @staticmethod
    # def set_error_log(header, error):
    #     # s3 = boto3.resource('s3')
    #     # s3_obj = s3.Object(bucket_name='vysfin-assets-uat', key='BigflowLog.txt')
    #     # s3_obj.put(Body='Application Logs 1')
    #
    #     s3 = boto3.client('s3')
    #     s3.put_object(Body='Application Log 1',Bucket='vysfin-assets-uat',Key='BigflowLog.txt')
    # #
    #     # logger = logging.getLogger('watchtower-logger')
    #     # logger.error(error)
    #
    #     s3_client = boto3.client('s3')
    #
    #     with open('BigflowLog.txt') as file:
    #         object = file.read()
    #
    #         s3_client.put_object(Body=object, Bucket='vysfin-assets-uat', Key='BigflowLog.txt', ContentType='whatever/something',
    #                              ContentEncoding='whatever-itis', StorageClass='PICK_ONE', ACL='you_choose')

    # @staticmethod
    # def set_error_log(header, error):
    #     serverpath = BASE_DIR + '/Bigflow/Logs/'
    #     if not os.path.exists(serverpath):
    #         os.makedirs(serverpath)
    #     header = header + ' - ' + datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    #     logFile = open(serverpath + utility.get_file_name("bigflowlog") + ".txt", "a")
    #     logFile.write(header + "\n" + error + "\n")
    #     logFile.close()
    #     logFile = open(serverpath + utility.get_file_name("bigflowlog") + ".txt", "r")
    #     print("Output of Readlines after appending")
    #     # print(logFile.readlines())
    #     lines = logFile.readlines()
    #     print (lines)
    #     logFile.close()
    #     raise Http404(lines)

    @staticmethod
    def error_403(request):
        return render(request, "Shared/error_403.html", {'test': 'ponraj'})

    @staticmethod
    def get_file_name(name):
        tem_date = datetime.date.today().strftime("%Y%m%d")
        return name + "" + tem_date

    # data must having title and data (sample data:{title:value,message:value,cust_key:cust_value}
    # sendList is a FCMToken list (sample sentList: [fcmToken1,fcmToken2]
    # This is must implement in Android like Action and get value
    @staticmethod
    def sendNotification(data, sendList):
        data = {"registration_ids": sendList, "data": data}
        responce = requests.post(url=utility.FCMServerIP,
                                 params="",
                                 data=json.dumps(data),
                                 headers=utility.FCMHeader,
                                 verify=False)
        responce = responce.content.decode("utf-8")
        responce = json.loads(responce)
        return responce.get("success")

    # This not handle by Android just flash message
    @staticmethod
    def sendFlashNotification(title, message, sendList):
        data = {"registration_ids": sendList,
                "notification": {"body": message, "title": title}}
        responce = requests.post(url=utility.FCMServerIP,
                                 params="",
                                 data=json.dumps(data),
                                 headers=utility.FCMHeader,
                                 verify=False)
        responce = responce.content.decode("utf-8")
        responce = json.loads(responce)
        return responce.get("success")

    @staticmethod
    def apiHeader():
        return {"content-type": "application/json", "Authorization": "Token 7111797114100105971106449505132"}

    @staticmethod
    def xlsxHeader(workbook):
        head_format = workbook.add_format()
        head_format.set_font_color('#0000FF')
        head_format.set_bold()
        head_format.set_align('center')
        head_format.set_align('vcenter')
        return head_format

    @staticmethod
    def headerFormat(workbook):
        head_format = utility.xlsxHeader(workbook)
        head_format.set_font_size(20)
        return head_format

    @staticmethod
    def subHeaderFormat(workbook):
        head_format = utility.xlsxHeader(workbook)
        head_format.set_font_size(14)
        return head_format

    @staticmethod
    def tableHeader(workbook):
        head_format = utility.xlsxHeader(workbook)
        head_format.set_font_size(11)
        return head_format

    @staticmethod
    def numberFormat(workbook):
        head_format = workbook.add_format({'num_format': '#,##0'})
        return head_format
    @staticmethod
    def check_pointaccess(request):
        try:
            if 'HTTP_REFERER' not in request.META:
                common.logger.error('URL Error')
                request.session.flush()
                raise PermissionDenied
                # sys.exit()
        except Exception as e:
            common.logger.error(e)
            raise PermissionDenied

# @register.tag(name="any_function")
# @register.simple_tag(takes_context=True)
# @register.inclusion_tag('mainLayout.html')
@register.simple_tag(takes_context=True)
def any_function(context):
    request = context['request']
    if (context['request'].session.get('Emp_gid', None) == None):
        return False
    else:
        decrypt_emp_gid= decry_data(request.session['Emp_gid'])
        result = class1.menulist(decrypt_emp_gid, 'N')
        output = []
        if (result[1][0] == 'FOUND'):
            output = list(result[0])
        return output


@register.filter
def filter_parent(menu):
    er = len(menu)
    t = filter(lambda p: p['menu_parent_gid'] == 0, menu)
    r = sorted(t, key=lambda k: k['menu_displayorder'])
    return r


@register.filter
def filter_children(menu_id, menu):
    t = filter(lambda p: p['menu_parent_gid'] == menu_id, menu)
    r = sorted(t, key=lambda k: k['menu_displayorder'])
    return r


@register.filter
def checkLength(menu_id, menu):
    t = filter(lambda p: p['menu_parent_gid'] == menu_id, menu)
    r = sorted(t, key=lambda k: k['menu_displayorder'])
    return len(r)
