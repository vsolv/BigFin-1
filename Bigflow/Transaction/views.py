# import self
import logging
import traceback

import cv2
from django.shortcuts import render
from requests import request

from Bigflow.Transaction.Model import mFET, mSales
from Bigflow.Master.Model import mMasters
from django.http import JsonResponse
from datetime import date
from django.http import HttpResponse
from Bigflow.Collection.Model import mCollection
import shutil
import base64
from fpdf import FPDF
from io import BytesIO
from PIL import Image
import pyzbar
import numpy as np
# from pyzbar import pyzbar
import os
import tempfile
from pdf2image import convert_from_path
import Bigflow.Core.models as common


imagedatas = list()
decodedata = list()
pdfname = list()
from os import path
from glob import glob
# from pyzbar import pyzbar
# import cv2
import pdf2image
import time
from Bigflow.Core.models import decrpt as decry_data
from Bigflow.Core.models import Excelfilename
from Bigflow.Purchase.Model import mPurchase

from Bigflow.settings import BASE_DIR, MEDIA_URL

# from rest_framework.views import APIView
# from rest_framework.response import Response
# from Bigflow.AP.model import mAP
from django.shortcuts import render
from Bigflow.Transaction.Model import mFET, mSales
from Bigflow.Master.Model import mMasters
from django.http import JsonResponse
from datetime import date
from django.http import HttpResponse
from Bigflow.Collection.Model import mCollection
# from rest_framework.views import APIView
# from rest_framework.response import Response
import Bigflow.Core.jwt_file as jwt
import json
import time
import datetime
import requests
import pandas as pd
from Bigflow.Core import models as common
import time
from Bigflow.menuClass import utility as utl
from Bigflow.Core.models import MasterRequestObject
from Bigflow.Core.models import get_data_from_id
ip = common.localip()
# token = common.token()


# headers = {"content-type": "application/json", "Authorization": "" + token + ""}
today = date.today()
today == date.fromtimestamp(time.time())
ddaate = date(today.year, 4, 1)


def add_schdle(request):
    # utl.check_authorization(request)
    # utl.check_pointaccess(request)
    if request.method == 'POST':
        # token = jwt.token(request)
        obj_add_schedule = mFET.FET_model()
        jsondata = json.loads(request.body.decode('utf-8'))
        if jsondata.get('parms').get('TYPE') == 'SCHEDULE':
            obj_add_schedule.action = 'Insert'
            obj_add_schedule.type = 'SINGLE'
            obj_add_schedule.sechedule_gid = 0
            obj_add_schedule.jsonData_sec = json.dumps(jsondata.get('parms').get('customer_gid'))
            obj_add_schedule.customer_gid = jsondata.get('parms').get('customer_gid')
            obj_add_schedule.followup_reason_gid = 0
            obj_add_schedule.schedule_ref_gid = 0
            obj_add_schedule.sch_remark = 'Direct'
            if jsondata.get('parms').get('emp_gid') != None:
                if jsondata.get('parms').get('emp_gid') != 0:
                    obj_add_schedule.employee_gid = jsondata.get('parms').get('emp_gid')
            else:
                obj_add_schedule.employee_gid = decry_data(request.session['Emp_gid'])
            obj_add_schedule.date = common.convertDate(jsondata.get('parms').get('Date'))
            obj_add_schedule.schedule_type_gid = jsondata.get('parms').get('schedule_type_gid')
            obj_add_schedule.entity_gid = decry_data(request.session['Entity_gid'])
            obj_add_schedule.resechedule_date = ''
            obj_add_schedule.create_by = decry_data(request.session['Emp_gid'])
            # print(request.path)
            # common.main_fun1(request.read(), request.path)
            out_message = obj_add_schedule.set_schedule()
            if (out_message != ''):
                output = out_message
                return JsonResponse(output, safe=False)

        elif jsondata.get('parms').get('TYPE') == 'LEADS':
            obj_add_schedule.customer_name = jsondata.get('parms').get('customer_name')
            obj_add_schedule.address_1 = jsondata.get('parms').get('address')
            obj_add_schedule.mobile_no = jsondata.get('parms').get('mobile_no')
            obj_add_schedule.landline_no = jsondata.get('parms').get('landline_no')


        elif jsondata.get('parms').get('TYPE') == 'RESCHEDULE' or jsondata.get('parms').get('TYPE') == 'Reschedule_all':
            obj_add_schedule.action = jsondata.get('parms').get('TYPE')
            obj_add_schedule.type = 'SINGLE'
            obj_add_schedule.sch_remark = jsondata.get('parms').get('ls_Remarks')
            obj_add_schedule.resechedule_date = convertDate(jsondata.get('parms').get('ls_reschdul_date'))
            obj_add_schedule.sechedule_gid = jsondata.get('parms').get('schedule_gid')
            if jsondata.get('parms').get('schedule_gid') == 0:
                obj_add_schedule.date = common.convertDate(jsondata.get('parms').get('sch_date'))
                obj_add_schedule.jsonData = json.dumps(jsondata.get('parms').get('cust_gid'))
            obj_add_schedule.create_by = decry_data(request.session['Emp_gid'])
            # print(request.path)
            # out_message = outputReturn(obj_add_schedule.set_schedule(), 1)  ### comment- Ramesh - API
            # common.main_fun1(request.read(), request.path)

            out_message = obj_add_schedule.set_schedule()
            return JsonResponse(out_message, safe=False)

        elif jsondata.get('parms').get('TYPE') == 'SCHEDULE_BULK':
            obj_add_schedule.action = 'Insert'
            obj_add_schedule.type = 'SCHEDULE_BULK'
            obj_add_schedule.sechedule_gid = 0
            obj_add_schedule.jsonData_sec = json.dumps(jsondata.get('parms').get('data'))
            obj_add_schedule.followup_reason_gid = 0
            obj_add_schedule.schedule_ref_gid = 0
            obj_add_schedule.sch_remark = 'Direct'
            obj_add_schedule.employee_gid = jsondata.get('parms').get('emp_gid')
            if obj_add_schedule.employee_gid != 0:
                obj_add_schedule.employee_gid = jsondata.get('parms').get('emp_gid')
            obj_add_schedule.date = common.convertDate(jsondata.get('parms').get('Date'))
            obj_add_schedule.entity_gid = decry_data(request.session['Entity_gid'])
            obj_add_schedule.resechedule_date = ''
            obj_add_schedule.create_by = decry_data(request.session['Emp_gid'])
            print(request.path)
            # common.main_fun1(request.read(), request.path)
            out_message = obj_add_schedule.set_schedule()
            if (out_message != ''):
                output = out_message
                return JsonResponse(out_message, safe=False)

        elif jsondata.get('parms').get('TYPE') == 'UPDATE':
            obj_add_schedule.action = 'Update'
            obj_add_schedule.type = 'SINGLE'
            obj_add_schedule.sechedule_gid = jsondata.get('parms').get('schedule_gid')
            obj_add_schedule.customer_gid = jsondata.get('parms').get('cust_gid')
            obj_add_schedule.followup_reason_gid = jsondata.get('parms').get('followupreason_gid')
            obj_add_schedule.schedule_ref_gid = jsondata.get('parms').get('sechedule_ref')
            obj_add_schedule.date = jsondata.get('parms').get('Date')
            obj_add_schedule.schedule_type_gid = jsondata.get('parms').get('schedule_type_gid')
            obj_add_schedule.entity_gid = decry_data(request.session['Entity_gid'])
            obj_add_schedule.sch_remark = jsondata.get('parms').get('ls_Remarks')
            obj_add_schedule.create_by = decry_data(request.session['Emp_gid'])
            obj_add_schedule.man = jsondata.get('parms').get('ls_followup_date')
            if jsondata.get('parms').get('ls_followup_date') != None and jsondata.get('parms').get(
                    'ls_followup_date') != '':
                obj_add_schedule.ls_followup_date = convertDate(jsondata.get('parms').get('ls_followup_date'))
            else:
                obj_add_schedule.ls_followup_date = ''
            # out_message = outputReturn(obj_add_schedule.set_schedule(), 0)  ### Ramesh Comment - API
            # common.main_fun1(request.read(), request.path)
            out_message = obj_add_schedule.set_schedule()
            return JsonResponse(out_message, safe=False)

        elif jsondata.get('parms').get('TYPE') == 'INDATE':

            obj_add_schedule.action = 'Update'
            obj_add_schedule.type = 'SINGLE'
            obj_add_schedule.sechedule_gid = jsondata.get('parms').get('schedule_gid')
            obj_add_schedule.customer_gid = jsondata.get('parms').get('cust_gid')
            obj_add_schedule.followup_reason_gid = jsondata.get('parms').get('followupreason_gid')
            obj_add_schedule.schedule_ref_gid = jsondata.get('parms').get('sechedule_ref')
            obj_add_schedule.date = jsondata.get('parms').get('Date')
            obj_add_schedule.schedule_type_gid = jsondata.get('parms').get('schedule_type_gid')
            obj_add_schedule.entity_gid = decry_data(request.session['Entity_gid'])
            obj_add_schedule.sch_remark = jsondata.get('parms').get('ls_Remarks')
            obj_add_schedule.create_by = decry_data(request.session['Emp_gid'])

            if jsondata.get('parms').get('ls_followup_date') != None:
                obj_add_schedule.ls_followup_date = datetime.datetime.strptime(
                    jsondata.get('parms').get('ls_followup_date'), "%d/%m/%Y").strftime("%Y-%m-%d")
            else:
                obj_add_schedule.ls_followup_date = ''
                # common.main_fun1(request.read(), request.path)
                out_message = obj_add_schedule.set_schedule()
                if (out_message != ''):
                    output = out_message
                    return JsonResponse(json.dumps(output), safe=False)

            obj_add_schedule.resechedule_date = jsondata.get('parms').get('resechedule_date')
            out_message = outputReturn(obj_add_schedule.set_schedule(), 1)
            return JsonResponse(out_message, safe=False)

        elif jsondata.get('parms').get('TYPE') == 'DELETE':
            obj_add_schedule.action = 'Delete'
            obj_add_schedule.type = 'SINGLE'
            obj_add_schedule.sechedule_gid = jsondata.get('parms').get('schedule_gid')
            obj_add_schedule.customer_gid = 0
            obj_add_schedule.followup_reason_gid = 0
            obj_add_schedule.schedule_ref_gid = 0
            obj_add_schedule.date = ''
            obj_add_schedule.schedule_type_gid = 0
            obj_add_schedule.entity_gid = decry_data(request.session['Entity_gid'])
            obj_add_schedule.resechedule_date = ''
            obj_add_schedule.create_by = decry_data(request.session['Emp_gid'])
            # common.main_fun1(request.read(), request.path)
            out_message = obj_add_schedule.set_schedule()
            return JsonResponse(json.dumps(out_message), safe=False)

    else:
        utl.check_authorization(request)
        return render(request, "FET/fet_addschedule.html")


def status_qty(request):
    utl.check_authorization(request)
    utl.check_pointaccess(request)
    if request.method == 'POST':
        # token = jwt.token(request)

        obj_qty = mFET.FET_model()
        jsondata = json.loads(request.body.decode('utf-8'))
        obj_qty.action = 'Insert'
        obj_qty.employee_gid = request.session['Emp_gid']
        obj_qty.customer_gid = jsondata.get('parms').get('custid')
        obj_qty.from_date = common.convertdbDate(request.session['date'])
        obj_qty.to_date = common.convertdbDate(request.session['date'])
        obj_qty.entity_gid = decry_data(request.session['Entity_gid'])
        df_obj_add_schedule = obj_qty.get_qty()
        jdata = df_obj_add_schedule.to_json(orient='records')
        return JsonResponse(json.loads(jdata), safe=False)


def convertDate(stringDate):
    return datetime.datetime.strptime(stringDate, "%d/%m/%Y").strftime("%Y-%m-%d")


def status_get(request):
    utl.check_authorization(request)
    utl.check_pointaccess(request)
    if request.method == 'POST':
        token = jwt.token(request)
        obj_status = mFET.FET_model()
        jsondata = json.loads(request.body.decode('utf-8'))
        obj_status.action = 'Reschedule'
        obj_status.employee_gid = decry_data(request.session['Emp_gid'])
        obj_status.customer_gid = jsondata.get('parms').get('customer_gid')
        obj_status.from_date = common.convertdbDate(request.session['date'])
        obj_status.to_date = common.convertdbDate(request.session['date'])
        obj_status.entity_gid = decry_data(request.session['Entity_gid'])
        df_obj_add_schedule = obj_status.get_schedul()
        jdata = df_obj_add_schedule.to_json(orient='records')
        return JsonResponse(json.loads(jdata), safe=False)


def serviceIndex(request):
    utl.check_authorization(request)
    utl.check_pointaccess(request)
    return render(request, "FET/fet_service.html")


def allsaledetIndex(request):
    utl.check_authorization(request)
    utl.check_pointaccess(request)
    return render(request, "FET/fet_allsaledetails.html")


def pcollectionIndex(request):
    utl.check_authorization(request)
    utl.check_pointaccess(request)
    return render(request, "FET/fet_Collection.html")


def preschdleIndex(request):
    utl.check_authorization(request)
    utl.check_pointaccess(request)
    return render(request, "FET/fet_preschedule.html")


def fetemptracking(request):
    utl.check_authorization(request)
    utl.check_pointaccess(request)
    return render(request, "FET/fet_emptrackdetails.html")


def fetemplogin(request):
    utl.check_authorization(request)
    utl.check_pointaccess(request)
    return render(request, "FET/fet_emplogindetails.html")


def fetsnapshot(request):
    # utl.check_authorization(request)
    utl.check_pointaccess(request)
    return render(request, "FET/fet_FetSnapShot.html")


def pre_schedule_get(request):
    # utl.check_authorization(request)
    # utl.check_pointaccess(request)
    if request.method == 'POST':
        token = jwt.token(request)
        obj_preschedule_get = mFET.FET_model()
        jsondata = json.loads(request.body.decode('utf-8'))
        obj_preschedule_get.action = jsondata.get('parms').get('action')
        if obj_preschedule_get.action == 'reportview':
            obj_preschedule_get.action = jsondata.get('parms').get('action')
            obj_preschedule_get.employee_gid = 0
            obj_preschedule_get.jsondata = json.dumps(jsondata.get('parms').get('jsondata'))
            obj_preschedule_get.date = datetime.datetime.strptime(jsondata.get('parms').get('f_date'),
                                                                  "%d/%m/%Y").strftime("%Y-%m-%d")
            jsonData = {"entity_gid": [decry_data(request.session['Entity_gid'])], "client_gid": []}
            obj_preschedule_get.jsonData = json.dumps(jsonData)
            ld_preschedule = obj_preschedule_get.get_preschedule_fet()
            df_preschedule = ld_preschedule.get("DATA")
            jdata = df_preschedule.to_json(orient='records')
            return JsonResponse(json.loads(jdata), safe=False)
        else:
            obj_preschedule_get.action = jsondata.get('parms').get('action')
            obj_preschedule_get.employee_gid = decry_data(request.session['Emp_gid'])
            obj_preschedule_get.jsondata = json.dumps(jsondata.get('parms').get('jsondata'))
            obj_preschedule_get.date = datetime.datetime.strptime(jsondata.get('parms').get('f_date'),
                                                                  "%d/%m/%Y").strftime("%Y-%m-%d")
            obj_preschedule_get.jsonData = json.dumps({"entity_gid": [decry_data(request.session['Entity_gid'])],
                                                       "client_gid": [1]})
            obj_preschedule_get.create_by = decry_data(request.session['Emp_gid'])
            ld_preschedule = obj_preschedule_get.get_preschedule_fet()
            df_preschedule = ld_preschedule.get("DATA")
            jdata = df_preschedule.to_json(orient='records')
            return JsonResponse(json.loads(jdata), safe=False)
    elif request.method == 'GET':
        obj_preschedule_get = mFET


def pre_schedule_status(request):
    utl.check_authorization(request)
    utl.check_pointaccess(request)
    if request.method == 'GET':
        # token = jwt.token(request)
        obj_preschedule_get = mFET.FET_model()
        obj_preschedule_get.action = request.GET['action']
        obj_preschedule_get.jsondata = request.GET['jsondata']
        df_preschedule = obj_preschedule_get.get_preschedul()
        jdata = df_preschedule.to_json(orient='records')
        return JsonResponse(json.loads(jdata), safe=False)
    elif request.method == 'POST':
        obj_preschedule_get = mFET


def empvsschedule_get(request):
    utl.check_authorization(request)
    utl.check_pointaccess(request)
    if request.method == 'GET':
        token = jwt.token(request)
        data = {}
        obj_empvsschedule = mFET.FET_model()
        if (request.GET['localaction'] == 'noexcel'):
            obj_empvsschedule.action = request.GET['action']
            if request.GET['emp_gid'] == '0':
                data['employee_gid'] = decry_data(request.session['Emp_gid'])
            else:
                data['employee_gid'] = request.GET['emp_gid']
            if (request.GET['f_date'] != ''):
                data['fromdate'] = common.convertDate(request.GET['f_date'])
            if (request.GET['t_date'] != ''):
                data['todate'] = common.convertDate(request.GET['t_date'])
            if (request.GET['fu_f_date'] != ''):
                data['followUp_fromdate'] = common.convertDate(request.GET['fu_f_date'])
            if (request.GET['fu_t_date'] != ''):
                data['followUp_todate'] = common.convertDate(request.GET['fu_t_date'])
            if (request.GET['rs_f_date'] != ''):
                data['reschedule_fromdate'] = common.convertDate(request.GET['rs_f_date'])
            if (request.GET['rs_t_date'] != ''):
                data['reschedule_todate'] = common.convertDate(request.GET['rs_t_date'])
            data['customer_gid'] = request.GET['cus_gid']
            data['scheduletype_gid'] = request.GET['type_gid']
            data['customergroup_gid'] = request.GET['custgrp']
            data['location_gid'] = request.GET['loc_gid']
            data['login_emp_gid'] = request.GET['login_emp_gid']
            obj_empvsschedule.jsonData = json.dumps(data)
            obj_empvsschedule.jsondata = json.dumps(
                {"entity_gid": [decry_data(request.session['Entity_gid'])], "client_gid": [request.GET['Cname']]})
            df_preschedule = obj_empvsschedule.get_empvsSchedule()
            df_preschedule['login_gid'] = (request.session['Emp_gid'])
            jdata = df_preschedule.to_json(orient='records')
            return JsonResponse(json.loads(jdata), safe=False)
        else:
            obj_empvsschedule.action = request.GET['action']
            if request.GET['emp_gid'] == '0':
                data['employee_gid'] = decry_data(request.session['Emp_gid'])
            else:
                data['employee_gid'] = request.GET['emp_gid']
            if (request.GET['f_date'] != ''):
                data['fromdate'] = common.convertDate(request.GET['f_date'])
            if (request.GET['t_date'] != ''):
                data['todate'] = common.convertDate(request.GET['t_date'])
            if (request.GET['fu_f_date'] != ''):
                data['followUp_fromdate'] = common.convertDate(request.GET['fu_f_date'])
            if (request.GET['fu_t_date'] != ''):
                data['followUp_todate'] = common.convertDate(request.GET['fu_t_date'])
            if (request.GET['rs_f_date'] != ''):
                data['reschedule_fromdate'] = common.convertDate(request.GET['rs_f_date'])
            if (request.GET['rs_t_date'] != ''):
                data['reschedule_todate'] = common.convertDate(request.GET['rs_t_date'])
            data['customer_gid'] = request.GET['cus_gid']
            data['scheduletype_gid'] = request.GET['type_gid']
            data['customergroup_gid'] = request.GET['custgrp']
            data['location_gid'] = request.GET['loc_gid']
            data['login_emp_gid'] = request.GET['login_emp_gid']
            obj_empvsschedule.jsonData = json.dumps(data)
            obj_empvsschedule.jsondata = json.dumps(
                {"entity_gid": [decry_data(request.session['Entity_gid'])], "client_gid": [request.GET['Cname']]})
            XLSX_MIME = 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
            response = HttpResponse(content_type=XLSX_MIME)
            filename = Excelfilename('FET Review Details_')
            response['Content-Disposition'] = 'attachment; filename="{}"'.format(filename)
            # response['Content-Disposition'] = 'attachment; filename="FET Review Excel.xlsx"'
            writer = pd.ExcelWriter(response, engine='xlsxwriter')
            df_view = obj_empvsschedule.get_empvsSchedule()
            df_view.index = range(1, len(df_view) + 1)
            df_data = df_view[
                ['employee_name', 'customer_name', 'schdate', 'scheduletype_name', 'schedule_status',
                 'followupreason_name', 'schedule_followup_date', 'schedule_reschedule_date', 'schedulereview_remarks',
                 'schedulereview_reviewstatus']]
            df_data.to_excel(writer, sheet_name='FET Review', index_label='SL NO', startrow=1, startcol=2,
                             freeze_panes=(2, 0),
                             header=['Employee Name', 'Customer Name', 'Date', 'Type', 'Status', 'Complete For',
                                     'Followup Date', 'Re-Schedule Date', 'Status Remark', 'Status'])
            writer.save()
            return response


def followup_reason(request):
    utl.check_authorization(request)
    utl.check_pointaccess(request)
    if request.method == 'GET':
        token = jwt.token(request)
        obj_followup_reason = mFET.FET_model()
        obj_followup_reason.schedule_type_gid = request.GET['schType_gid']
        obj_followup_reason.entity_gid = decry_data(request.session['Entity_gid'])
        df_followup_reason = obj_followup_reason.get_followup_reason_fet()
        jdata = df_followup_reason.to_json(orient='records')
        return JsonResponse(json.loads(jdata), safe=False)


def schedule_type(request):
    utl.check_pointaccess(request)
    if request.method == 'GET':
        # token = jwt.token(request)
        obj_schedule_type = mFET.FET_model()
        obj_schedule_type.entity_gid = decry_data(request.session['Entity_gid'])
        df_schedule_type = obj_schedule_type.get_schedule_type()
        jdata = df_schedule_type.to_json(orient='records')
        return JsonResponse(json.loads(jdata), safe=False)


def reportupdateIndex(request):
    utl.check_authorization(request)
    utl.check_pointaccess(request)
    return render(request, "FET/fet_reportupdate.html")


def schedule_collectionIndex(request):
    utl.check_authorization(request)
    utl.check_pointaccess(request)
    return render(request, "FET/fet_ScheduleCollection.html")


def mapped_customer(request):
    utl.check_authorization(request)
    utl.check_pointaccess(request)
    if request.method == 'GET':
        obj_mapped_customer = mFET.FET_model()
        obj_mapped_customer.action = request.GET['action']
        obj_mapped_customer.employee_gid = decry_data(request.session['Emp_gid'])
        obj_mapped_customer.entity_gid = decry_data(request.session['Entity_gid'])
        df_mapped_customer = obj_mapped_customer.get_mapped_customer()
        jdata = df_mapped_customer.to_json(orient='records')
        return JsonResponse(json.loads(jdata), safe=False)


def emp_mapped_customer(request):
    utl.check_authorization(request)
    utl.check_pointaccess(request)
    if request.method == 'GET':
        obj_empmapped_customer = mFET.FET_model()
        obj_empmapped_customer.action = request.GET['action']
        obj_empmapped_customer.employee_gid = request.GET['emp_gid']
        obj_empmapped_customer.entity_gid = decry_data(request.session['Entity_gid'])
        df_mapped_customer = obj_empmapped_customer.get_mapped_customer()
        jdata = df_mapped_customer.to_json(orient='records')
        return JsonResponse(json.loads(jdata), safe=False)


def customer_ddl(request):
    utl.check_authorization(request)
    utl.check_pointaccess(request)
    if request.method == 'GET':
        obj_customer_ddl = mFET.FET_model()
        obj_customer_ddl.customer_gid = 0
        obj_customer_ddl.jsonData = request.GET['jsonData']
        obj_customer_ddl.entity_gid = decry_data(request.session['Entity_gid'])
        df_customer_ddl = obj_customer_ddl.get_customer()
        jdata = df_customer_ddl.to_json(orient='records')
        return JsonResponse(json.loads(jdata), safe=False)


def productcategory_ddl(request):
    utl.check_authorization(request)
    utl.check_pointaccess(request)
    if request.method == 'GET':
        obj_producategory_ddl = mFET.FET_model()
        obj_producategory_ddl.productcat_gid = 1
        df_customer_ddl = obj_producategory_ddl.get_productcategory()
        jdata = df_customer_ddl.to_json(orient='records')
        return JsonResponse(json.loads(jdata), safe=False)


def producttype_ddl(request):
    utl.check_authorization(request)
    utl.check_pointaccess(request)
    if request.method == 'GET':
        obj_producttype_ddl = mFET.FET_model()
        obj_producttype_ddl.producttype_gid = 1
        df_customer_ddl = obj_producttype_ddl.get_producttype()
        jdata = df_customer_ddl.to_json(orient='records')
        return JsonResponse(json.loads(jdata), safe=False)


def Productjson(request):
    utl.check_authorization(request)
    utl.check_pointaccess(request)
    if request.method == 'GET':
        form = mFET.FET_model()
        form.limit = 200
        form.name = ''
        jdata = form.get_product()
        if request.method == 'GET':
            return JsonResponse(json.dumps(jdata), safe=False)
        else:
            return render(request, "", {'form': jdata})


def TA_detailsIndex(request):
    utl.check_authorization(request)
    utl.check_pointaccess(request)
    return render(request, "FET/fet_TAdetails.html")


def sales_orderIndex(request):
    utl.check_authorization(request)
    utl.check_pointaccess(request)
    return render(request, "FET/fet_salesorder.html")


def sales_fav_product(request):
    utl.check_authorization(request)
    utl.check_pointaccess(request)
    if request.method == 'POST':
        obj_sales_fav_pdct = mFET.FET_model()
        jsondata = json.loads(request.body.decode('utf-8'))
        obj_sales_fav_pdct.customer_gid = jsondata.get('parms').get('custid')
        obj_sales_fav_pdct.product_type = 1
        obj_sales_fav_pdct.entity_gid = decry_data(request.session['Entity_gid'])

        # common.main_fun1(request.read(), request.path)
        df_sales_fav_pdct = obj_sales_fav_pdct.get_sales_fav_product()
        jdata = df_sales_fav_pdct.to_json(orient='records')
        return JsonResponse(json.loads(jdata), safe=False)


def sales_order_set(request):
    # utl.check_authorization(request)
    # utl.check_pointaccess(request)
    if request.method == 'POST':
        obj_sales = mSales.Sales_Model()
        obj_sales.employee_gid = decry_data(request.session['Emp_gid'])
        obj_sales = mSales.Sales_Model()
        jsondata = json.loads(request.body.decode('utf-8'))
        if jsondata.get('parms').get('ACTION') == 'Insert':
            if obj_sales.employee_gid > 0:
                obj_sales.customer_gid = jsondata.get('parms').get('custid')
                obj_sales.create_by = decry_data(request.session['Emp_gid'])
                obj_sales.entity_gid = decry_data(request.session['Entity_gid'])
                obj_sales.So_Header_date = common.convertdbDate(request.session['date'])
                obj_sales.Channel = 'c'
                obj_sales.action = 'Insert'
                obj_sales.sodetails = jsondata.get('parms').get('data')
                setsales_order = outputReturn(obj_sales.set_sales_order(), 0)
                return JsonResponse(setsales_order, safe=False)
            else:
                obj_sales.customer_gid = jsondata.get('parms').get('custid')
                obj_sales.employee_gid = decry_data(request.session['Emp_gid'])
                obj_sales.create_by = decry_data(request.session['Emp_gid'])
                obj_sales.entity_gid = decry_data(request.session['Entity_gid'])
                obj_sales.So_Header_date = common.convertdbDate(request.session['date'])
                obj_sales.Channel = 'c'
                obj_sales.action = 'Insert'
                obj_sales.sodetails = jsondata.get('parms').get('data')
                setsales_order = outputReturn(obj_sales.set_sales_order(), 0)
                return JsonResponse(setsales_order, safe=False)
        elif jsondata.get('parms').get('ACTION') == 'Update':
            obj_sales.customer_gid = jsondata.get('parms').get('custid')
            obj_sales.employee_gid = decry_data(request.session['Emp_gid'])
            obj_sales.create_by = decry_data(request.session['Emp_gid'])
            obj_sales.entity_gid = decry_data(request.session['Entity_gid'])
            # obj_sales.quantity=x.get('quantity')
            obj_sales.So_Header_date = common.convertdbDate(request.session['date'])
            obj_sales.Channel = 'c'
            obj_sales.action = 'Update'
            obj_sales.sodetails = jsondata.get('parms').get('data')
            setsales_order = outputReturn(obj_sales.set_sales_order(), 1)
            # jdata = setsales_order.to_json(orient='records')
            return JsonResponse(setsales_order, safe=False)
        elif jsondata.get('parms').get('ACTION') == 'DIRECTSALE_DELETE':
            obj_sales.customer_gid = jsondata.get('parms').get('custid')
            obj_sales.employee_gid = decry_data(request.session['Emp_gid'])
            obj_sales.create_by = decry_data(request.session['Emp_gid'])
            obj_sales.entity_gid = decry_data(request.session['Entity_gid'])
            obj_sales.soheader_gid = jsondata.get('parms').get('soheader_gid')
            obj_sales.So_Header_date = common.convertdbDate(request.session['date'])
            obj_sales.Channel = 'c'
            obj_sales.action = 'DIRECTSALE_DELETE'
            obj_sales.sodetails = jsondata.get('parms').get('data')
            setsales_order = outputReturn(obj_sales.set_sales_order(), 1)
            return JsonResponse(setsales_order, safe=False)
        elif jsondata.get('parms').get('ACTION') == 'Delete':
            obj_sales.customer_gid = jsondata.get('parms').get('custid')
            obj_sales.employee_gid = decry_data(request.session['Emp_gid'])
            obj_sales.create_by = decry_data(request.session['Emp_gid'])
            obj_sales.entity_gid = decry_data(request.session['Entity_gid'])
            # obj_sales.quantity=x.get('quantity')
            obj_sales.So_Header_date = common.convertdbDate(request.session['date'])
            obj_sales.Channel = 'c'
            obj_sales.action = 'Delete'
            obj_sales.sodetails = jsondata.get('parms').get('data')
            setsales_order = outputReturn(obj_sales.set_sales_order(), 1)
            # jdata = setsales_order.to_json(orient='records')
            return JsonResponse(setsales_order, safe=False)


def outputReturn(tubledtl, index):
    temp = tubledtl[0].split(',')
    if (len(temp) > 1):
        if (index == 0):
            return int(temp[0])
        else:
            return temp[1]
    else:
        return temp[0]


def get_addScheduleDtl(request):
    utl.check_authorization(request)
    utl.check_pointaccess(request)
    schedule = []
    if request.method == 'GET':
        token = jwt.token(request)
        obj_mapped_customer1 = mFET.FET_model()
        obj_mapped_customer1.employee_gid = decry_data(request.session['Emp_gid'])
        obj_mapped_customer1.entity_gid = decry_data(request.session['Entity_gid'])
        df_mapped_customer = obj_mapped_customer1.get_mapped_customer()
        obj_mapped_customer1.action = request.GET['action']
        obj_mapped_customer1.date = datetime.datetime.strptime(request.GET['f_date'], "%d/%m/%Y").strftime("%Y-%m-%d")
        obj_mapped_customer1.create_by = decry_data(request.session['Emp_gid'])
        obj_mapped_customer1.jsonData = json.dumps(
            {"entity_gid": [decry_data(request.session['Entity_gid'])], "client_gid": []})
        df_preschedule = obj_mapped_customer1.get_preschedule()
        df_schedule_type = obj_mapped_customer1.get_schedule_type()
        total_schCount = df_preschedule['schedule_customer_gid'].unique().size
        sch_count = []
        for x, cus in df_mapped_customer.iterrows():
            schlist = []
            for y, sch in df_schedule_type.iterrows():
                sch_type = {'sch_type': sch['scheduletype_name'], 'schType_gid': sch['scheduletype_gid']}
                d = df_preschedule[(df_preschedule['schedule_customer_gid'] == cus['customer_gid'])
                                   & (df_preschedule['schedule_scheduletype_gid'] == sch['scheduletype_gid'])]
                if d.empty:
                    sch_type['sch_gid'] = ''
                    sch_type['sch_status'] = ''
                    sch_type['sch_ischecked'] = False
                else:
                    sch_type['sch_gid'] = d['schedule_gid'].iloc[0]
                    sch_type['sch_status'] = d['schedule_status'].iloc[0]
                    sch_type['sch_ischecked'] = True
                schlist.append(sch_type)
            schedule.append(schlist)
            sch_count.append(total_schCount)
        df_mapped_customer['schedule'] = schedule
        df_mapped_customer['sch_count'] = sch_count
        jdata = df_mapped_customer.to_json(orient='records')
        return JsonResponse(json.loads(jdata), safe=False)


def sales_order_get(request):
    utl.check_authorization(request)
    utl.check_pointaccess(request)
    if request.method == 'POST':
        obj_salesget = mSales.Sales_Model()
        jsondata = json.loads(request.body.decode('utf-8'))
        obj_salesget.action = jsondata.get('action')
        obj_salesget.customer_gid = jsondata.get('custid')
        obj_salesget.employee_gid = decry_data(request.session['Emp_gid'])
        obj_salesget.date = jsondata.get('date')
        obj_salesget.jsonData = json.dumps(
            {"Entity_Gid": [decry_data(request.session['Entity_gid'])], "Client_Gid": [jsondata.get('Client_gid')]})
        obj_salesget.jsondata = '{}'
        obj_salesget.limit = 30
        setsales_order = obj_salesget.get_sales_order()
        jdata = setsales_order.to_json(orient='records')
        return JsonResponse(json.loads(jdata), safe=False)


def serviceFET_set(request):
    utl.check_authorization(request)
    utl.check_pointaccess(request)
    if request.method == 'POST':
        token = jwt.token(request)
        obj_add_service = mFET.FET_model()
        jsondata = json.loads(request.body.decode('utf-8'))
        customer_gid = jsondata.get('parms').get('custid')
        lst_salesdata = jsondata.get('parms').get('data')
        for x in lst_salesdata:
            obj_add_service.employee_gid = decry_data(request.session['Emp_gid'])
            obj_add_service.code = '1'
            obj_add_service.customer_gid = customer_gid
            obj_add_service.date = common.convertdbDate(request.session['date'])
            obj_add_service.product_gid = x.get('product_gid')
            obj_add_service.product_stockcode = x.get('product_stock_code')
            obj_add_service.remark = x.get('remarks')
            out_message = obj_add_service.set_service()
        if (out_message != ''):
            output = out_message
            return JsonResponse(json.dumps(output), safe=False)
        return out_message


def collection_set(request):
    utl.check_authorization(request)
    utl.check_pointaccess(request)
    if request.method == 'POST':
        token = jwt.token(request)
        obj_add_collection = mFET.FET_model()
        jsondata = json.loads(request.body.decode('utf-8'))
        obj_add_collection.action = jsondata.get('action')
        obj_add_collection.leadref_gid = jsondata.get('leadref_gid')
        obj_add_collection.customer_gid = jsondata.get('cust_gid')
        obj_add_collection.employee_gid = decry_data(request.session['Emp_gid'])
        obj_add_collection.mode = jsondata.get('collection_mode')
        obj_add_collection.amount = jsondata.get('collection_amount')
        obj_add_collection.date = jsondata.get('date')
        obj_add_collection.cheque_no = jsondata.get('cheque_no')  # OPtional
        if jsondata.get('collection_mode') == 'Cheque':
            obj_add_collection.jsonData = json.dumps(jsondata.get('cheque_data'))
        obj_add_collection.entity_gid = decry_data(request.session['Entity_gid'])
        out_message = outputReturn(obj_add_collection.set_collection(), 0)
        return JsonResponse(out_message, safe=False)


def outstanding_fet_get(request):
    utl.check_authorization(request)
    utl.check_pointaccess(request)
    if request.method == 'POST':
        token = jwt.token(request)
        obj_outstanding_fet = mFET.FET_model()
        jsondata = json.loads(request.body.decode('utf-8'))
        if jsondata.get('parms').get('ACTION') == 'outstandingemployee':
            obj_outstanding_fet.customer_gid = 0
            obj_outstanding_fet.from_date = ''
            obj_outstanding_fet.to_date = ''
            obj_outstanding_fet.employee_gid = request.session['Emp_gid']
            obj_outstanding_fet.limit = 0
            obj_outstanding_fet.action = 'outstandingemployee'
            obj_outstanding_fet.entity_gid = decry_data(request.session['Entity_gid'])
            df_outstanding_fet = obj_outstanding_fet.get_FEToutstanding_fet()
            jdata = df_outstanding_fet.to_json(orient='records')
            return JsonResponse(json.loads(jdata), safe=False)
        elif jsondata.get('parms').get('ACTION') == 'outstandingcustomer':
            obj_outstanding_fet.customer_gid = jsondata.get('parms').get('customer_gid')
            obj_outstanding_fet.from_date = ''
            obj_outstanding_fet.to_date = ''
            obj_outstanding_fet.employee_gid = decry_data(request.session['Emp_gid'])
            obj_outstanding_fet.limit = 1000
            obj_outstanding_fet.action = 'outstandingcustomer'
            obj_outstanding_fet.entity_gid = decry_data(request.session['Entity_gid'])
            df_outstanding_fet = obj_outstanding_fet.get_FEToutstanding_fet()
            jdata = df_outstanding_fet.to_json(orient='records')
            return JsonResponse(json.loads(jdata), safe=False)
        elif jsondata.get('parms').get('ACTION') == 'OutstandingCustomergroup':
            obj_outstanding_fet.customer_gid = jsondata.get('parms').get('customer_gid')
            obj_outstanding_fet.from_date = ''
            obj_outstanding_fet.to_date = ''
            obj_outstanding_fet.employee_gid = decry_data(request.session['Emp_gid'])
            obj_outstanding_fet.limit = 1000
            obj_outstanding_fet.action = 'OutstandingCustomergroup'
            obj_outstanding_fet.entity_gid = decry_data(request.session['Entity_gid'])
            df_outstanding_fet = obj_outstanding_fet.get_FEToutstanding_fet()
            jdata = df_outstanding_fet.to_json(orient='records')
            return JsonResponse(json.loads(jdata), safe=False)
    elif request.method == 'GET':
        obj_outstanding_fet = mFET.FET_model()
        obj_outstanding_fet.action = request.GET['action']
        obj_outstanding_fet.customer_gid = request.GET['cust_gid']
        obj_outstanding_fet.from_date = common.convertDate(request.GET['f_date']) if request.GET['f_date'] != '' else ''
        obj_outstanding_fet.to_date = common.convertDate(request.GET['t_date']) if request.GET['t_date'] != '' else ''
        obj_outstanding_fet.employee_gid = request.GET['emp_gid']
        obj_outstanding_fet.entity_gid = decry_data(request.session['Entity_gid'])
        obj_outstanding_fet.limit = request.GET['row_limit']
        obj_outstanding_fet.entity_gid = decry_data(request.session['Entity_gid'])
        df_outstanding_fet = obj_outstanding_fet.get_FEToutstanding_fet()
        jdata = df_outstanding_fet.to_json(orient='records')
        return JsonResponse(json.loads(jdata), safe=False)


# Through API Get Outstanding
def getOutstanding(request):
    utl.check_authorization(request)
    utl.check_pointaccess(request)
    if request.method == "POST":
        token = jwt.token(request)
        jsondata = json.loads(request.body.decode('utf-8'))
        data = jsondata.get('data')
        limit = jsondata.get('limit')
        entity_gid = request.session['Entity_gid']
        headers = {"content-type": "application/json",
                   "Authorization": "" + token + ""}
        params = {'ACTION': "Common", 'Entity_gid': entity_gid, "entity": entity_gid,
                  'Limit': "" + str(limit) + ""}
        resp = requests.post("" + ip + "/Customerview_get", params=params, data=json.dumps(data), headers=headers,
                             verify=False)
        response = resp.content.decode("utf-8")
        return HttpResponse(response)


def sales_history_fet_get(request):
    utl.check_authorization(request)
    utl.check_pointaccess(request)
    if request.method == 'POST':
        token = jwt.token(request)
        obj_sales_history = mFET.FET_model()
        jsondata = json.loads(request.body.decode('utf-8'))
        obj_sales_history.customer_gid = jsondata.get('parms').get('customer_gid')
        obj_sales_history.from_date = ''
        obj_sales_history.to_date = ''
        obj_sales_history.limit = 10000
        obj_sales_history.entity_gid = decry_data(request.session['Entity_gid'])
        df_sales_history = obj_sales_history.get_sales_history_fet()
        jdata = df_sales_history.to_json(orient='records')
        return JsonResponse(json.loads(jdata), safe=False)


def collection_history_fet(request):
    utl.check_authorization(request)
    utl.check_pointaccess(request)
    if request.method == 'POST':
        token = jwt.token(request)
        obj_collection_history = mFET.FET_model()
        jsondata = json.loads(request.body.decode('utf-8'))
        obj_collection_history.action = 'Scheduleview'
        obj_collection_history.customer_gid = jsondata.get('parms').get('custid')
        obj_collection_history.employee_gid = decry_data(request.session['Emp_gid'])
        obj_collection_history.from_date = (datetime.date.today() + datetime.timedelta(-6 * 365 / 12)).isoformat()
        obj_collection_history.to_date = common.convertdbDate(request.session['date'])
        df_collection_history = obj_collection_history.get_collection_history_fet()
        jdata = df_collection_history.to_json(orient='records')
        return JsonResponse(json.loads(jdata), safe=False)


def schedule_view_fet_get(request):
    utl.check_authorization(request)
    utl.check_pointaccess(request)
    if request.method == 'POST':
        obj_schedule_view = mFET.FET_model()
        jsondata = json.loads(request.body.decode('utf-8'))
        obj_schedule_view.customer_gid = jsondata.get('parms').get('customer_gid')
        obj_schedule_view.from_date = ''
        obj_schedule_view.to_date = ''
        obj_schedule_view.limit = 30
        obj_schedule_view.entity_gid = decry_data(request.session['Entity_gid'])
        df_schedule_view = obj_schedule_view.get_schedule_view_fet()
        jdata = df_schedule_view.to_json(orient='records')
        return JsonResponse(json.loads(jdata), safe=False)


def leadrequest_set(request):
    utl.check_authorization(request)
    utl.check_pointaccess(request)
    if request.method == 'POST':
        obj_leadsrequest = mFET.FET_model()
        jsondata = json.loads(request.body.decode('utf-8'))
        obj_leadsrequest.action = jsondata.get('parms').get('action')
        obj_leadsrequest.leadref_gid = jsondata.get('parms').get('leadref_gid')
        obj_leadsrequest.customer_name = jsondata.get('parms').get('customer_name')
        obj_leadsrequest.mobile_no = jsondata.get('parms').get('mobile_no')
        obj_leadsrequest.address1 = jsondata.get('parms').get('address')
        obj_leadsrequest.entity_gid = decry_data(request.session['Entity_gid'])
        obj_leadsrequest.employee_gid = decry_data(request.session['Emp_gid'])
        out_message = outputReturn(obj_leadsrequest.set_leadrequest(), 1)
        return JsonResponse(out_message, safe=False)


def leadrequest_approve(request):
    utl.check_authorization(request)
    utl.check_pointaccess(request)
    if request.method == 'POST':
        obj_lead_approve = mFET.FET_model()
        jsondata = json.loads(request.body.decode('utf-8'))
        obj_lead_approve.action = jsondata.get('parms').get('action')
        obj_lead_approve.leadref_gid = jsondata.get('parms').get('leadref_gid')
        obj_lead_approve.status = jsondata.get('parms').get('status')
        obj_lead_approve.reason = jsondata.get('parms').get('reason')
        obj_lead_approve.employee_gid = decry_data(request.session['Emp_gid'])
        out_message = outputReturn(obj_lead_approve.set_leadrequest(), 1)
        return JsonResponse(out_message, safe=False)


def leadrequest_get(request):
    utl.check_authorization(request)
    utl.check_pointaccess(request)
    if request.method == 'GET':
        obj_leadsrequest_get = mFET.FET_model()
        obj_leadsrequest_get.leadref_gid = request.GET['leadref_gid']
        obj_leadsrequest_get.leadref_name = request.GET['leadref_name']
        obj_leadsrequest_get.status = request.GET['leadref_status']
        obj_leadsrequest_get.mobile_no = request.GET['mobile_no']
        obj_leadsrequest_get.entity_gid = decry_data(request.session['Entity_gid'])
        df_lead_view = obj_leadsrequest_get.get_leadrequest()
        jdata = df_lead_view.to_json(orient='records')
        return JsonResponse(json.loads(jdata), safe=False)


def Schedule_reportIndex(request):
    utl.check_authorization(request)
    utl.check_pointaccess(request)
    return render(request, "FET/fet_ScheduleReport.html")


def Schedule_reportget(request):
    utl.check_authorization(request)
    utl.check_pointaccess(request)
    if request.method == 'GET':
        token = jwt.token(request)
        obj_Schdul_det = mFET.FET_model()
        params = json.loads(request.GET['details'])
        obj_Schdul_det.from_date = convertDate(params.get('fdata'))
        obj_Schdul_det.to_date = convertDate(params.get('tdate'))
        obj_Schdul_det.employee_gid = decry_data(request.session['Emp_gid'])
        obj_Schdul_det.customer_gid = params.get('cust_gid')
        obj_Schdul_det.limit = 30
        obj_Schdul_det.entity_gid = decry_data(request.session['Entity_gid'])
        dt_shedul = obj_Schdul_det.get_schedule_view_fet()
        df = pd.DataFrame(dt_shedul)
        df_filtered = df.query('schedule_status == "CLOSED"', inplace=True)
        obj_Schdul_det.date = params.get('resh_date')
        obj_Schdul_det.entity_gid = decry_data(request.session['Entity_gid'])
        dt_salesorder = obj_Schdul_det.get_sales_history_fet()
        obj_Schdul_det.action = 'OutstandingCustomer'
        dtsales = pd.merge(df_filtered, dt_salesorder, how='left', left_on='Schedule_ref_gid',
                           right_on='soheader_gid')
        dtsales["collection_amount"] = 0
        dtsales["Outstanding_amount"] = ''
        for index, row in dtsales.iterrows():
            schedule_type = row['scheduletype_name']
            Schedule_ref_gid = row['Schedule_ref_gid']
            obj_Schdul_det.from_date = ''
            obj_Schdul_det.to_date = row['schedule_date'].date()
            obj_Schdul_det.customer_gid = row['schedule_customer_gid']
            dt_outstanding = obj_Schdul_det.get_outstanding_fet()
            outstand = pd.DataFrame(dt_outstanding)
            dtsales.set_value(index, 'Outstanding_amount', outstand['pending'].sum())
            if (schedule_type == 'COLLECTION'):
                if (pd.notnull(Schedule_ref_gid)):
                    obj_Schdul_det.collectionheader_gid = Schedule_ref_gid
                    obj_Schdul_det.jsondata = json.dumps(
                        {"entity_gid": [decry_data(request.session['Entity_gid'])], "client_gid": []})
                    colln_data = obj_Schdul_det.get_collection_amt()
                    coll = pd.DataFrame(colln_data)
                    dtsales.set_value(index, 'collection_amount', coll['fetcollectionheader_amount'])
        jdata = dtsales.to_json(orient='records')
        return JsonResponse(jdata, safe=False)


def report_collection(request):
    utl.check_authorization(request)
    utl.check_pointaccess(request)
    if request.method == 'POST':
        obj_Schdul_det = mFET.FET_model()
        jsondata = json.loads(request.body.decode('utf-8'))
        obj_Schdul_det.action = jsondata.get('Action')
        obj_Schdul_det.type = jsondata.get('Type')
        obj_Schdul_det.collectionheader_gid = jsondata.get('collectionheader_gid')
        obj_Schdul_det.name = ''
        obj_Schdul_det.date = ''
        obj_Schdul_det.jsonData = jsondata.get('CHEQUE').get('params').get('DATA')
        obj_Schdul_det.jsondata = jsondata.get('CHEQUE').get('params').get('CLASSIFICATION')
        colln_data = obj_Schdul_det.get_collection_amt()
        jdata = colln_data.to_json(orient='records')
        return JsonResponse(jdata, safe=False)


def bank_detail(request):
    utl.check_authorization(request)
    utl.check_pointaccess(request)
    if request.method == 'GET':
        obj_bank_detail = mFET.FET_model()
        obj_bank_detail.entity_gid = request.session['Entity_gid']
        df_bank_view = obj_bank_detail.get_bankdetails()
        jdata = df_bank_view.to_json(orient='records')
        return JsonResponse(json.loads(jdata), safe=False)


def directIndex(request):
    utl.check_authorization(request)
    utl.check_pointaccess(request)
    return render(request, "FET/fet_DirectSale.html")


def directentryIndex(request):
    utl.check_authorization(request)
    utl.check_pointaccess(request)
    return render(request, "FET/fet_DirectEntry.html")


def salecreateIndex(request):
    # utl.check_authorization(request)
    utl.check_pointaccess(request)
    return render(request, "FET/fet_SaleCreate.html")


def collectioncreateIndex(request):
    # utl.check_authorization(request)
    utl.check_pointaccess(request)
    return render(request, "FET/fet_CollectionCreate.html")


def fetapprovalIndex(request):
    utl.check_authorization(request)
    utl.check_pointaccess(request)
    return render(request, "FET/fet_Approval.html")


def fetprospctIndex(request):
    utl.check_authorization(request)
    utl.check_pointaccess(request)
    return render(request, 'FET/fet_Prospect.html')


def searchview(request):
    # utl.check_authorization(request)
    utl.check_pointaccess(request)
    return render(request, "FET/advancesearchview.html")


def getEditSchedule(request):
    utl.check_authorization(request)
    utl.check_pointaccess(request)
    if request.method == 'GET':
        obj_scheduleEdit = mFET.FET_model()
        obj_scheduleEdit.schedule_gid = request.GET['schedule_gid']
        obj_scheduleEdit.entity_gid = decry_data(request.session['Entity_gid'])
        df_scheduledtl = obj_scheduleEdit.get_scheduleEdit()
        jdata = df_scheduledtl.to_json(orient='records')
        return JsonResponse(json.loads(jdata), safe=False)


def getEditdrct(request):
    utl.check_authorization(request)
    utl.check_pointaccess(request)
    if request.method == 'GET':
        obj_scheduleEdit = mFET.FET_model()
        obj_scheduleEdit.action = request.GET['action']
        obj_scheduleEdit.so_header_gid = request.GET['so_header_gid']
        obj_scheduleEdit.entity_gid = decry_data(request.session['Entity_gid'])
        df_scheduledtl = obj_scheduleEdit.get_drctEdit()
        jdata = df_scheduledtl.to_json(orient='records')
        return JsonResponse(json.loads(jdata), safe=False)


def getCustomerFilterlist(request):
    # utl.check_authorization(request)
    # utl.check_pointaccess(request)
    if request.method == 'GET':
        # token = jwt.token(request)
        employee = json.loads(request.GET['emp_gid'])
        routedtl = json.loads(request.GET['route_gid'])
        clusterdtl = json.loads(request.GET['cluster_gid'])
        # employee
        obj_hirEmpList = mFET.FET_model()
        obj_hirEmpList.employee_gid = decry_data(request.session['Emp_gid'])
        obj_hirEmpList.employee_name = ''
        obj_hirEmpList.cluster_gid = 1
        obj_hirEmpList.jsonData = json.dumps(
            {"entity_gid": [decry_data(request.session['Entity_gid'])], "client_gid": [(request.GET['Client_gid'])]})
        df_emp = obj_hirEmpList.getHierarchy_employeeList()
        tee = df_emp[df_emp['employee_gid'] == decry_data(request.session['Emp_gid'])]
        tee1 = tee['employee_supervisor_gid'].tolist()[0]
        emp_tree = getempTree(df_emp, tee1)
        # route
        obj_hirEmpList.action = 'ROUTE_FILTER'
        obj_hirEmpList.route_gid = 0
        obj_hirEmpList.route_name = ''
        obj_hirEmpList.route_code = ''
        if (len(employee) != 0):
            employee = json.loads(request.GET['emp_gid'])
        else:
            employee = df_emp['employee_gid'].tolist()

        obj_hirEmpList.json_employee_gid = json.dumps({'routeemp_gid': employee})
        obj_hirEmpList.entity_gid = decry_data(request.session['Entity_gid'])
        df_route = obj_hirEmpList.getRoute()
        route_tree = getrouteTree(df_route)
        # territory
        obj_clustertree = mMasters.Masters()
        obj_clustertree.action = 'PARENT_ROUTE'
        obj_clustertree.cluster_parent_gid = 0
        obj_clustertree.hierarchy_gid = 0
        obj_clustertree.employee_gid = 0
        obj_clustertree.jsondata = json.dumps(
            {"entity_gid": [decry_data(request.session['Entity_gid'])], "client_gid": []})
        obj_clustertree.jsonData = json.dumps(
            {'FILTER': [{'Employee_gid': employee, 'Cluster_gid': clusterdtl, 'Route_header_gid': routedtl}]})
        df_cluster = obj_clustertree.get_cluster()
        te = getmenutree(df_cluster, 0)
        # customer

        obj_hirEmpList.action = 'ADD_SCHEDULE'
        obj_hirEmpList.jsonData = json.dumps(
            {'FILTER': [{'Employee_gid': employee, 'Cluster_gid': clusterdtl, 'Route_header_gid': routedtl}]})
        obj_hirEmpList.jsondata = json.dumps(
            {"entity_gid": [decry_data(request.session['Entity_gid'])], "client_gid": []})
        df_custall = obj_hirEmpList.getcustomer()
        df_custall['type'] = 'ALL'
        obj_hirEmpList.action = 'ROUTE_MAP'
        today = common.convertdbDate(request.session['date'])
        fdate = datetime.datetime.strptime(request.GET['f_date'], "%d/%m/%Y").strftime("%A")
        obj_hirEmpList.jsonData = json.dumps(
            {'FILTER': [{'Employee_gid': employee, 'Cluster_gid': clusterdtl, 'Route_header_gid': routedtl}],
             'ROUTE_MAP': [{'Employee_gid': employee, 'Day_plan': fdate, 'Schedule_date': today}]})
        obj_hirEmpList.jsondata = json.dumps(
            {"entity_gid": [decry_data(request.session['Entity_gid'])], "client_gid": []})
        df_custroute = obj_hirEmpList.getcustomer()
        df_custroute['type'] = 'ROUTE'
        df_cust = pd.concat([df_custall, df_custroute], ignore_index=True, sort=True)
        tee2 = json.loads(df_cust['customer_gid'].to_json(orient='records'))
        see = set(list(tee2))
        data = {}
        df_size = (df_cust[['customer_size', 'customer_size_gid']]).groupby(
            ['customer_size', 'customer_size_gid']).size().reset_index();
        df_type = (df_cust[['customer_type']]).groupby(['customer_type']).size().reset_index();
        df_category = (df_cust[['custcategory_name', 'customer_category_gid']]).groupby(
            ['custcategory_name', 'customer_category_gid']).size().reset_index();
        df_constitution = (df_cust[['customer_constitution', 'customer_constitution_gid']]).groupby(
            ['customer_constitution', 'customer_constitution_gid']).size().reset_index();
        df_mode = (df_cust[['customer_salemode', 'customer_salemode_gid']]).groupby(
            ['customer_salemode', 'customer_salemode_gid']).size().reset_index();

        obj_hirEmpList.action = request.GET['action']
        obj_hirEmpList.date = convertDate(request.GET['f_date'])

        # obj_hirEmpList.employee_gid=employee
        obj_hirEmpList.create_by = decry_data(request.session['Emp_gid'])
        # OutStanding report-------------------------
        obj_cltn = mCollection.Collection_model()
        obj_cltn.type = 'OUTSTANDING_DUE_DAYS'
        obj_cltn.sub_type = 'DUE_DAYS'
        obj_cltn.filter_json = json.dumps({"customer_gid": list(see)})
        obj_cltn.Classification = json.dumps({"Entity_Gid": [int(decry_data(request.session['Entity_gid']))]})
        df_outstanding = obj_cltn.get_OutstandingCustomer()

        obj_hirEmpList.jsonData = json.dumps(
            {"entity_gid": [decry_data(request.session['Entity_gid'])], "client_gid": []})
        df_preschedule = obj_hirEmpList.get_preschedule()
        df_schedule_type = obj_hirEmpList.get_schedule_type()
        data['employee'] = emp_tree
        data['route'] = route_tree
        data['terrirtory'] = te
        data['size'] = json.loads(df_size.to_json(orient='records'))
        data['type'] = json.loads(df_type.to_json(orient='records'))
        data['categroy'] = json.loads(df_category.to_json(orient='records'))
        data['constitution'] = json.loads(df_constitution.to_json(orient='records'))
        data['mode'] = json.loads(df_mode.to_json(orient='records'))
        data['customer'] = json.loads(
            get_filteredCustomer(df_cust, df_preschedule, df_schedule_type).to_json(orient='records'))
        # Outstanding report-----------------------------
        data['outstanding'] = json.loads(df_outstanding.to_json(orient='records'))
        jdata = data
        return JsonResponse(jdata, safe=False)


def get_filteredCustomer(customerList, scheduleList, scheduleTypeList):
    schedule = []
    df_mapped_customer = customerList
    df_preschedule = scheduleList
    df_schedule_type = scheduleTypeList
    total_schCount = df_preschedule['schedule_customer_gid'].unique().size
    sch_count = []
    orderby = []
    status = []
    nnme = []
    editflag = []
    ordertype = []
    schlistempty = [];
    for y, sch in df_schedule_type.iterrows():
        sch_type = {'sch_type': sch['scheduletype_name'], 'schType_gid': sch['scheduletype_gid'],
                    'schtype_order': sch['scheduletype_order']}
        sch_type['sch_gid'] = ''
        sch_type['sch_status'] = ''
        sch_type['sch_empname'] = ''
        sch_type['sch_edit'] = ''
        sch_type['schtype_order'] = ''
        sch_type['sch_ischecked'] = False
        schlistempty.append(sch_type)

    for x, cus in df_mapped_customer.iterrows():
        schlist = []
        order_by = 1
        status_det = ""
        empnme = ""
        edit = ""
        schorder = ""
        per = df_preschedule[(df_preschedule['schedule_customer_gid'] == cus['customer_gid'])];
        if not per.empty:
            for y, sch in df_schedule_type.iterrows():
                sch_type = {'sch_type': sch['scheduletype_name'], 'schType_gid': sch['scheduletype_gid'],
                            'schtype_order': sch['scheduletype_order']}
                d = df_preschedule[(df_preschedule['schedule_customer_gid'] == cus['customer_gid'])
                                   & (df_preschedule['schedule_scheduletype_gid'] == sch['scheduletype_gid'])]
                if d.empty:
                    sch_type['sch_gid'] = ''
                    sch_type['sch_status'] = ''
                    sch_type['sch_empname'] = ''
                    sch_type['sch_edit'] = ''
                    sch_type['schtype_order'] = ''
                    sch_type['sch_ischecked'] = False
                else:
                    status_det = d['schedule_status'].iloc[0]
                    empnme = d['employee_name'].iloc[0]
                    if d['Is_Edit'].iloc[0] == 'Y':
                        edit = d['IS_FOLLOW_UP_EDIT'].iloc[0]
                    else:
                        edit = d['Is_Edit'].iloc[0]
                    schorder = d['scheduletype_order'].iloc[0]
                    if d['Order_by'].iloc[0] == '0' and order_by == 1:
                        order_by = 0
                    sch_type['sch_gid'] = d['schedule_gid'].iloc[0]
                    sch_type['sch_status'] = d['schedule_status'].iloc[0]
                    sch_type['sch_empname'] = d['employee_name'].iloc[0]
                    if d['Is_Edit'].iloc[0] == 'Y':
                        sch_type['sch_edit'] = d['IS_FOLLOW_UP_EDIT'].iloc[0]
                    else:
                        sch_type['sch_edit'] = d['Is_Edit'].iloc[0]
                    sch_type['schtype_order'] = d['scheduletype_order'].iloc[0]
                    sch_type['sch_ischecked'] = True
                schlist.append(sch_type)
            schedule.append(schlist)
            status.append(status_det)
            nnme.append(empnme)
            editflag.append(edit)
            ordertype.append(schorder)
            orderby.append(order_by)
            sch_count.append(total_schCount)
        else:
            schedule.append(schlistempty)
            status.append(status_det)
            nnme.append(empnme)
            editflag.append(edit)
            ordertype.append(schorder)
            orderby.append(order_by)
            sch_count.append(total_schCount)
    df_mapped_customer['sch_status'] = status
    df_mapped_customer['sch_empname'] = nnme
    df_mapped_customer['schedule'] = schedule
    df_mapped_customer['sch_count'] = sch_count
    df_mapped_customer['sch_edit'] = editflag
    df_mapped_customer['schtype_order'] = ordertype
    df_mapped_customer['Order_by'] = orderby
    return df_mapped_customer.sort_values(['Order_by', 'customer_name'])


def getClusterTree(request):
    utl.check_authorization(request)
    utl.check_pointaccess(request)
    if request.method == 'GET':
        token = jwt.token(request)
        obj_clustertree = mMasters.Masters()
        obj_clustertree.action = 'ALL'
        obj_clustertree.cluster_parent_gid = 0
        obj_clustertree.hierarchy_gid = 0
        obj_clustertree.employee_gid = 0
        obj_clustertree.jsondata = json.dumps(
            {"entity_gid": [decry_data(request.session['Entity_gid'])], "client_gid": []})
        df_cluster = obj_clustertree.get_cluster()
        jdata = df_cluster.to_json(orient='records')
        te = getmenutree(df_cluster, 0)
        return JsonResponse(te, safe=False)


def getmenutree(list, parent_gid):
    # te = getmenutree(df_cluster, 0)
    de = []
    re = list[list['cluster_parent_gid'] == parent_gid]
    for x, main in re.iterrows():
        te = {}
        te['menu_id'] = main['cluster_gid']
        te['menu_name'] = main['cluster_name']
        te['menu_parent'] = main['cluster_parent_gid']
        te['cluster_hierarchygid'] = main['cluster_hierarchygid']
        te['child_list'] = getmenutree(list, main['cluster_gid'])
        de.append(te)
    return de


def getempTree(list, parent_gid):
    de = []
    re = list[list['employee_supervisor_gid'] == parent_gid]
    for x, main in re.iterrows():
        te = {}
        te['emp_gid'] = main['employee_gid']
        te['emp_name'] = main['employee_name']
        te['child_list'] = getempTree(list, main['employee_gid'])
        de.append(te)
    return de


def getrouteTree(list):
    de = []
    ter = (list[['routeheader_name', 'routeheader_gid']]).groupby(
        ['routeheader_name', 'routeheader_gid']).size().reset_index();
    for x, main in ter.iterrows():
        te = {}
        te['route_gid'] = main['routeheader_gid']
        te['route_name'] = main['routeheader_name']
        ter1 = list[list['routeheader_gid'] == main['routeheader_gid']]
        ter2 = (ter1[['cluster_name', 'cluster_gid']]).groupby(
            ['cluster_name', 'cluster_gid']).size().reset_index();
        te['child_list'] = json.loads(ter2.to_json(orient='records'))
        de.append(te)
    return de


def stocktakenIndex(request):
    utl.check_authorization(request)
    utl.check_pointaccess(request)
    return render(request, "FET/fet_stocktaken.html")


def stockget(request):
    # utl.check_authorization(request)
    # utl.check_pointaccess(request)
    if request.method == 'POST':
        token = jwt.token(request)
        obj_stock = mFET.FET_model()
        jsondata = json.loads(request.body.decode('utf-8')).get('parms')
        obj_stock.action = jsondata.get('action')
        obj_stock.employee_gid = decry_data(request.session['Emp_gid'])
        obj_stock.customer_gid = jsondata.get('custid')
        obj_stock.from_date = ddaate.replace(today.year - 3)
        obj_stock.to_date = date.today()
        obj_stock.date = jsondata.get('todaydate')
        obj_stock.type = jsondata.get('type')
        obj_stock.entity_gid = decry_data(request.session['Entity_gid'])
        df_obj_add_schedule = obj_stock.get_stock()
        jdata = df_obj_add_schedule.to_json(orient='records')
        return JsonResponse(json.loads(jdata), safe=False)


def stockeditget(request):
    utl.check_authorization(request)
    utl.check_pointaccess(request)
    if request.method == 'POST':
        token = jwt.token(request)
        obj_stock = mFET.FET_model()
        jsondata = json.loads(request.body.decode('utf-8')).get('parms')
        obj_stock.action = jsondata.get('action')
        obj_stock.employee_gid = decry_data(request.session['Emp_gid'])
        obj_stock.customer_gid = jsondata.get('custid')
        obj_stock.from_date = ddaate.replace(today.year - 3)
        obj_stock.to_date = date.today()
        obj_stock.date = common.convertDate(jsondata.get('todaydate'))
        obj_stock.type = jsondata.get('type')
        obj_stock.entity_gid = decry_data(request.session['Entity_gid'])
        df_obj_add_schedule = obj_stock.get_stock()
        jdata = df_obj_add_schedule.to_json(orient='records')
        return JsonResponse(json.loads(jdata), safe=False)


def stockset(request):
    # utl.check_authorization(request)
    # utl.check_pointaccess(request)
    if request.method == 'POST':
        obj_leadsrequest = mFET.FET_model()
        jsondata = json.loads(request.body.decode('utf-8')).get('parms')
        obj_leadsrequest.action = jsondata.get('action')
        obj_leadsrequest.customer_gid = jsondata.get('custid')
        obj_leadsrequest.date = common.convertDate(jsondata.get('todaydate'))
        obj_leadsrequest.employee_gid = decry_data(request.session['Emp_gid'])
        obj_leadsrequest.entity_gid = decry_data(request.session['Entity_gid'])
        obj_leadsrequest.stckdet = json.dumps(jsondata.get('stckdet'))
        out_message = outputReturn(obj_leadsrequest.set_stock(), 1)
        return JsonResponse(out_message, safe=False)


def emptrackingIndex(request):
    utl.check_authorization(request)
    utl.check_pointaccess(request)
    return render(request, "FET/fet_emp_tracking.html")


def stockcreateIndex(request):
    # utl.check_authorization(request)
    utl.check_pointaccess(request)
    return render(request, "FET/fet_Stockcreate.html")


def schedulereviewIndex(request):
    utl.check_authorization(request)
    utl.check_pointaccess(request)
    return render(request, "FET/fet_review.html")


def emptrackingrepIndex(request):
    utl.check_authorization(request)
    utl.check_pointaccess(request)
    return render(request, "FET/fet_rep_emptracking.html")


def tasummary(request):
    utl.check_authorization(request)
    utl.check_pointaccess(request)
    return render(request, "FET/ta_summary.html")


def sale_approval(request):
    utl.check_authorization(request)
    utl.check_pointaccess(request)
    if request.method == 'POST':
        token = jwt.token(request)
        obj_lead_approve = mFET.FET_model()
        jsondata = json.loads(request.body.decode('utf-8'))
        obj_lead_approve.action = jsondata.get('parms').get('action')
        obj_lead_approve.soheader_gid = jsondata.get('parms').get('headergid')
        obj_lead_approve.remark = jsondata.get('parms').get('reason')
        obj_lead_approve.create_by = decry_data(request.session['Emp_gid'])
        obj_lead_approve.entity_gid = decry_data(request.session['Entity_gid'])
        out_message = outputReturn(obj_lead_approve.set_saleaprve(), 1)
        return JsonResponse(out_message, safe=False)


def sale_order_get(request):
    utl.check_authorization(request)
    utl.check_pointaccess(request)
    if request.method == 'POST':
        token = jwt.token(request)
        jsondata = json.loads(request.body.decode('utf-8')).get('parms')
        obj = mSales.Sales_Model()
        obj.typ = jsondata.get('type')
        obj.sbtyp = jsondata.get('sub_type')
        params = {'Action': "" + jsondata.get('action')}
        params['Date'] = ""
        params['Customer_Gid'] = jsondata.get('custid')
        params['Emp_Gid'] = jsondata.get('empid')
        params['Limit'] = jsondata.get('limit')
        params['Entity_Gid'] = decry_data(request.session['Entity_gid'])
        datas = jsondata.get('data')
        datas['Classification']['Entity_Gid'] = [decry_data(request.session['Entity_gid'])]
        datas = json.dumps(jsondata.get('data'))
        headers = {"content-type": "application/json", "Authorization": "" + token + ""}
        resp = requests.post("" + ip + "/FET_Approve", params=params,
                             data=datas, headers=headers, verify=False)
        response = resp.content.decode("utf-8")
        return HttpResponse(response)

        # obj_leadsrequest_get = mSales.Sales_Model()
        # obj_leadsrequest_get.action = jsondata.get('parms').get('action')
        # # obj_leadsrequest_get.date = common.convertdbDate(request.session['date'])
        # obj_leadsrequest_get.customer_gid = jsondata.get('parms').get('custid')
        # obj_leadsrequest_get.employee_gid = jsondata.get('parms').get('empid')
        # obj_leadsrequest_get.limit = jsondata.get('parms').get('limit')
        # obj_leadsrequest_get.jsonData = json.dumps(
        #     {"entity_gid": [request.session['Entity_gid']], "client_gid": [jsondata.get('parms').get('Cname')]})
        # obj_leadsrequest_get.jsondata = '{}'
        # df_lead_view = obj_leadsrequest_get.get_sales_order()
        # jdata = df_lead_view.to_json(orient='records')
        # return JsonResponse(json.loads(jdata), safe=False)


def snap_shot_get(request):
    utl.check_authorization(request)
    utl.check_pointaccess(request)
    if request.method == 'POST':
        token = jwt.token(request)
        jsondata = json.loads(request.body.decode('utf-8'))
        obj = mSales.Sales_Model()
        obj.action = jsondata.get('Action')
        obj.jsonData = json.dumps(jsondata.get('data'))
        datas = json.dumps(jsondata.get('data'))
        headers = {"content-type": "application/json", "Authorization": "" + token + ""}
        resp = requests.post("" + ip + "/FET_Review?Action=" + obj.action + "",
                             data=datas, headers=headers, verify=False)
        response = resp.content.decode("utf-8")
        return HttpResponse(response)

    if request.method == 'GET':
        token = jwt.token(request)
        obj_laglong = mSales.Sales_Model()
        obj_laglong.localaction = request.GET['localaction']
        obj_laglong.action = request.GET['action']
        if request.GET['f_date'] == '':
            obj_laglong.f_date = ''
        else:
            obj_laglong.f_date = common.convertDate(request.GET['f_date'])
        if request.GET['t_date'] == '':
            obj_laglong.t_date = ''
        else:
            obj_laglong.t_date = common.convertDate(request.GET['t_date'])
        if request.GET['fu_f_date'] == '':
            obj_laglong.fu_f_date = ''
        else:
            obj_laglong.fu_f_date = common.convertDate(request.GET['fu_f_date'])
        if request.GET['fu_t_date'] == '':
            obj_laglong.fu_t_date = ''
        else:
            obj_laglong.fu_t_date = common.convertDate(request.GET['fu_t_date'])
        if request.GET['rs_f_date'] == '':
            obj_laglong.rs_f_date = ''
        else:
            obj_laglong.rs_f_date = common.convertDate(request.GET['rs_f_date'])
        if request.GET['rs_t_date'] == '':
            obj_laglong.rs_t_date = ''
        else:
            obj_laglong.rs_t_date = common.convertDate(request.GET['rs_t_date'])
        obj_laglong.emp_gid = request.GET['emp_gid']
        obj_laglong.cus_gid = request.GET['cus_gid']
        obj_laglong.type_gid = request.GET['type_gid']
        obj_laglong.custgrp = request.GET['custgrp']
        obj_laglong.loc_gid = request.GET['loc_gid']
        obj_laglong.login_emp_gid = request.GET['login_emp_gid']
        obj_laglong.Cname = request.GET['Cname']
        obj_laglong.entity_gid = json.dumps(decry_data(request.session['Entity_gid']))
        resp = requests.get(
            ip + "/FET_Review?localaction=" + obj_laglong.localaction +
            "&action=" + obj_laglong.action + "&f_date=" + obj_laglong.f_date +
            "&t_date=" + obj_laglong.t_date + "&fu_f_date=" + obj_laglong.fu_f_date
            + "&fu_t_date=" + obj_laglong.fu_t_date + "&rs_f_date=" + obj_laglong.rs_f_date +
            "&rs_t_date=" + obj_laglong.rs_t_date + "&emp_gid=" + obj_laglong.emp_gid +
            "&cus_gid=" + obj_laglong.cus_gid + "&type_gid=" + obj_laglong.type_gid +
            "&custgrp=" + obj_laglong.custgrp + "&loc_gid=" + obj_laglong.loc_gid +
            "&login_emp_gid=" + obj_laglong.login_emp_gid +
            "&entity_gid=" + obj_laglong.entity_gid +
            "&Cname=" + obj_laglong.Cname + "",
            headers={"content-type": "application/json",
                     "Authorization": "" + token + ""},
            verify=False)
        return HttpResponse(resp.content.decode("utf-8"))


def fetcollection(request):
    utl.check_authorization(request)
    utl.check_pointaccess(request)
    token = jwt.token(request)
    jsondata = json.loads(request.body.decode('utf-8'))
    group = jsondata.get('Group')
    type = jsondata.get('Type')
    subtype = jsondata.get('Action')
    # data = jsondata.get('darta')
    params = {'Group': "" + group + "", 'Type': "" + type + "", 'Action': "" + subtype + ""}
    headers = {"content-type": "application/json", "Authorization": "" + token + ""}
    datas = json.dumps(jsondata.get('darta'))
    resp = requests.post("" + ip + "/Cltn_Inv_Map_API", params=params, data=datas, headers=headers, verify=False)
    response = resp.content.decode("utf-8")
    return HttpResponse(response)


def get_collectionapi(request):
    utl.check_authorization(request)
    utl.check_pointaccess(request)
    token = jwt.token(request)
    jsondata = json.loads(request.body.decode('utf-8'))
    type = jsondata.get('Type')
    subtype = jsondata.get('Sub_Type')
    params = {'Type': "" + type + "", 'Sub_Type': "" + subtype + "", "entity": request.session['Entity_gid']}
    headers = {"content-type": "application/json", "Authorization": "" + token + ""}
    datas = json.dumps(jsondata.get('darta'))
    resp = requests.post("" + ip + "/Outstanding_AR", params=params, data=datas, headers=headers, verify=False)
    response = resp.content.decode("utf-8")
    return HttpResponse(response)


def fetprocess(request):
    utl.check_authorization(request)
    utl.check_pointaccess(request)
    token = jwt.token(request)
    jsondata = json.loads(request.body.decode('utf-8'))
    group = jsondata.get('Group')
    type = jsondata.get('Schedule_Gid')
    subtype = jsondata.get('Entity_Gid')
    # data = jsondata.get('darta')
    params = {'Group': "" + group + "", 'Schedule_Gid': "" + str(type) + "", 'Entity_Gid': "" + subtype + ""}
    headers = {"content-type": "application/json", "Authorization": "" + token + ""}
    datas = json.dumps(jsondata.get('darta'))
    resp = requests.post("" + ip + "/FET_ReviewProcess", params=params, data=datas, headers=headers, verify=False)
    response = resp.content.decode("utf-8")
    return HttpResponse(response)


def setschedule_review(request):
    utl.check_authorization(request)
    utl.check_pointaccess(request)
    if request.method == 'POST':
        token = jwt.token(request)
        jsondata = json.loads(request.body.decode('utf-8'))
        obj_schReview = mFET.FET_model()
        obj_schReview.action = jsondata.get('parms').get('action')
        obj_schReview.jsonData = json.dumps(jsondata.get('parms').get('data'))
        obj_schReview.entity_gid = decry_data(request.session['Entity_gid'])
        obj_schReview.create_by = decry_data(request.session['Emp_gid'])
        out_message = common.outputReturn(obj_schReview.set_schedulereview(), 1)
        return JsonResponse(out_message, safe=False)


def fetreview_getexcel(request):
    utl.check_authorization(request)
    utl.check_pointaccess(request)
    try:
        if request.method == 'GET':
            token = jwt.token(request)
            obj_review = mFET.FET_model()
            data = {}
            obj_review.action = request.GET['action']
            if request.GET['emp_gid'] == '0':
                data['employee_gid'] = decry_data(request.session['Emp_gid'])
            else:
                data['employee_gid'] = request.GET['emp_gid']
            if (request.GET['f_date'] != ''):
                data['from_date'] = common.convertDate(request.GET['f_date'])
            if (request.GET['t_date'] != ''):
                data['to_date'] = common.convertDate(request.GET['t_date'])
            if (request.GET['cus_gid'] != ''):
                data['customer_gid'] = request.GET['cus_gid']
            if (request.GET['type_gid'] != ''):
                data['scheduletype_gid'] = request.GET['type_gid']
            if (request.GET['custgrp_gid'] != ''):
                data['customergroup_gid'] = request.GET['custgrp_gid']
            if (request.GET['loc_name'] != ''):
                data['location_name'] = request.GET['loc_name']
            obj_review.jsondata = json.dumps(data)
            obj_review.jsonData = json.dumps(
                {"entity_gid": [decry_data(request.session['Entity_gid'])], "client_gid": []})
            obj_review.entity_gid = decry_data(request.session['Entity_gid'])
            XLSX_MIME = 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
            response = HttpResponse(content_type=XLSX_MIME)
            filename = Excelfilename('FET Review Details')
            response['Content-Disposition'] = 'attachment; filename="{}"'.format(filename)
            writer = pd.ExcelWriter(response, engine='xlsxwriter')
            df_view = obj_review.get_preschedule()
            df_view.index = range(1, len(df_view) + 1)
            df_data = df_view[
                ['customer_name', 'location_name', 'employee_name', 'sctype', 'scdate', 'fupname', 'sale_amount',
                 'sale_netamount', 'state_name']]
            df_data.to_excel(writer, sheet_name='FET Review', index_label='SL NO', startrow=1, startcol=2,
                             freeze_panes=(2, 0),
                             header=['Customer Name', 'Location Name', 'Employee Name', 'Type', 'Date', 'Mode',
                                     'Amount',
                                     'Net Amount', 'State'])
            writer.save()
            return response
    except Exception as e:
        return HttpResponse({"MESSAGE:" + str(e)})


def fetemployee_getexcel(request):
    utl.check_authorization(request)
    utl.check_pointaccess(request)
    try:
        if request.method == 'GET':
            # token = jwt.token(request)
            data = {}
            obj_dayrouteget = mMasters.Masters()
            obj_dayrouteget.action = request.GET['action']
            obj_dayrouteget.employee_gid = request.GET['emp_gid']
            obj_dayrouteget.from_date = common.convertDate(request.GET['date'])
            if request.GET['todate'] == '':
                obj_dayrouteget.to_date = ''
            else:
                obj_dayrouteget.to_date = common.convertDate(request.GET['todate'])
            obj_dayrouteget.entity_gid = decry_data(request.session['Entity_gid'])
            XLSX_MIME = 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
            response = HttpResponse(content_type=XLSX_MIME)
            filename = Excelfilename('Executive Tracking Details_')
            response['Content-Disposition'] = 'attachment; filename="{}"'.format(filename)
            writer = pd.ExcelWriter(response, engine='xlsxwriter')
            df_view = obj_dayrouteget.dayrouteget()
            df_view.index = range(1, len(df_view) + 1)
            df_data = df_view[
                ['employee_name', 'employee_code', 'dayvisit_date', '9_time', '930_time', '10_time', '1030_time',
                 '11_time', '1130_time', '12_time',
                 '1230_time', '13_time', '1330_time', '14_time', '1430_time', '15_time', '1530_time', '16_time',
                 '1630_time', '17_time', '1730_time', '18_time', '1830_time', 'above_time']]
            df_data.to_excel(writer, sheet_name='Employee Tracking', index_label='SL NO', startrow=1, startcol=2,
                             freeze_panes=(2, 0),
                             header=['Employee Name', 'Employee code', 'Date', '09.00-09.30', '09.30-10.00',
                                     '10.00-10.30',
                                     '10.30-11.00', '11.00-11.30', '11.30-12.00', '12.00-12.30',
                                     '12.30-1.00', '1.00-1.30', '1.30-2.00', '2.00-2.30', '2.30-3.00',
                                     '3.00-3.30', '3.30-4.00', '4.00-4.30', '4.30-5.00', '5.00-5.30', '5.30-6.00',
                                     '6.00-6.30', '6.30-7.00', 'above 7.00'])
            writer.save()
            return response
    except Exception as e:
        return HttpResponse({"MESSAGE": e})


def fetreport(request):
    utl.check_authorization(request)
    utl.check_pointaccess(request)
    return render(request, "FET/fet_report.html")


def excelreport(request):
    utl.check_authorization(request)
    utl.check_pointaccess(request)
    try:
        if request.method == 'GET':
            token = jwt.token(request)
            obj_review = mFET.FET_model()
            data = {}
            obj_review.action = request.GET['action']
            obj_review.type = request.GET['type']
            obj_review.jsondata = {"fromdate": request.GET['fromdate'], "todate": request.GET['todate'],
                                   "employee_gid": request.GET['employee_gid'],
                                   "customer_gid": request.GET['customer_gid']}
            obj_review.entity_gid = request.session['Entity_gid']
            XLSX_MIME = 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
            response = HttpResponse(content_type=XLSX_MIME)
            filename = Excelfilename('FET Report Details_')
            response['Content-Disposition'] = 'attachment; filename="{}"'.format(filename)
            # response['Content-Disposition'] = 'attachment; filename="FET Report Excel.xlsx"'
            writer = pd.ExcelWriter(response, engine='xlsxwriter')
            df_view = obj_review.get_reportexcel()
            df_view.index = range(1, len(df_view) + 1)
            df_data = df_view[
                ['days', 'customer_name', 'employee_name', 'schedule_date', 'salescheduledremarks', 'saleschlname',
                 'sale_amount', 'sale_resch_date', 'sale_follup', 'sale_fup_date', 'sale_status', 'coll_fup_date',
                 'coll_resch_date', 'coll_amount', 'coll_follup', 'coll_status', 'collscheduledremarks']]
            df_data.to_excel(writer, sheet_name='FET Review', index_label='SL NO', startrow=1, startcol=2,
                             freeze_panes=(2, 0),
                             header=['Date', 'Customer Name', 'Employee Name', 'Schedule Date', 'Sale Remarks',
                                     'Sale Schedule Name',
                                     'Sale Amount', 'Sale Reschedule Date', 'Sale Followup', 'Sale Followup Date',
                                     'Sale Status', 'Collection Followup Date',
                                     'Collection Reschedule Date', 'Collection Amount', 'Collection FollowUp',
                                     'Collection Status', 'Collection Remarks'])
            writer.save()
            return response
    except Exception as e:
        return HttpResponse({"MESSAGE:" + str(e)})


def fetreportgenarate(request):
    utl.check_authorization(request)
    utl.check_pointaccess(request)
    return render(request, 'FET/fet_reportgenerate.html')


def sale_order_invoice_get(request):
    utl.check_authorization(request)
    utl.check_pointaccess(request)
    if request.method == 'POST':
        token = jwt.token(request)
        jsondata = json.loads(request.body.decode('utf-8'))
        obj_leadsrequest_get = mSales.Sales_Model()
        obj_leadsrequest_get.action = jsondata.get('parms').get('action')
        # obj_leadsrequest_get.date = common.convertdbDate(request.session['date'])
        obj_leadsrequest_get.customer_gid = jsondata.get('parms').get('custid')
        obj_leadsrequest_get.employee_gid = jsondata.get('parms').get('empid')
        obj_leadsrequest_get.limit = jsondata.get('parms').get('limit')
        obj_leadsrequest_get.jsonData = json.dumps(
            {"Entity_Gid": [decry_data(request.session['Entity_gid'])],
             "Client_Gid": [jsondata.get('parms').get('Cname')]})
        obj_leadsrequest_get.jsondata = jsondata.get('parms').get('invoicedetails')
        df_lead_view = obj_leadsrequest_get.get_sales_order()
        jdata = df_lead_view.to_json(orient='records')
        return JsonResponse(json.loads(jdata), safe=False)


def getlaglongfet(request):
    utl.check_authorization(request)
    utl.check_pointaccess(request)
    if request.method == 'GET':
        token = jwt.token(request)
        obj_laglong = mSales.Sales_Model()
        obj_laglong.action = request.GET['Action']
        obj_laglong.employee_gid = request.GET['Emp_gid']
        obj_laglong.From_Date = request.GET['From_Date']
        if request.GET['To_Date'] == '':
            obj_laglong.to_date = ''
        else:
            obj_laglong.to_date = common.convertDate(request.GET['To_Date'])
        obj_laglong.Entity_gid = json.dumps(decry_data(request.session['Entity_gid']))
        resp = requests.get(
            ip + "/LatLongFET?Action=" + obj_laglong.action + "&Emp_gid=" + obj_laglong.employee_gid + "&From_Date=" + obj_laglong.From_Date + "&To_Date=" + obj_laglong.to_date + "&Entity_gid=" + obj_laglong.Entity_gid + "",
            headers={"content-type": "application/json",
                     "Authorization": "" + token + ""},
            verify=False)
        return HttpResponse(resp.content.decode("utf-8"))


def getLogindetails(request):
    utl.check_authorization(request)
    utl.check_pointaccess(request)
    if request.method == 'GET':
        token = jwt.token(request)
        obj_laglong = mSales.Sales_Model()
        obj_laglong.action = request.GET['Action']
        obj_laglong.type = request.GET['Type']
        obj_laglong.jsondata = json.loads(request.GET['Json'])
        obj_laglong.Entity_gid = json.dumps(decry_data(request.session['Entity_gid']))
        resp = requests.post(
            ip + "/LoginDetails?Action=" + obj_laglong.action + "&Type=" + obj_laglong.type + "&Entity_gid=" + obj_laglong.Entity_gid + "",
            data=json.dumps(obj_laglong.jsondata),
            headers={"content-type": "application/json",
                     "Authorization": "" + token + ""},
            verify=False)
        return HttpResponse(resp.content.decode("utf-8"))


def apiget(request):
    utl.check_authorization(request)
    utl.check_pointaccess(request)
    if request.method == 'POST':
        token = jwt.token(request)
        jsondata = json.loads(request.body.decode('utf-8'))

        if (jsondata.get('Group')) == 'GET_CLTN_PAYMENT_SUMMARY':
            jsondata['CHEQUE']['entity'] = request.session['Entity_gid']
            obj = mSales.Sales_Model()
            obj.actn = jsondata.get('Action')
            obj.typ = jsondata.get('Type')
            obj.cltngid = json.dumps(jsondata.get('Collection_Gid'))
            obj.grp = jsondata.get('Group')
            obj.cltndate = jsondata.get('Collection_Date')
            datas = json.dumps(jsondata.get('CHEQUE'))
            resp = requests.post(
                "" + ip + "/Cltn_Inv_Map_API?Action=" + obj.actn + "&Type=" + obj.typ + "&Collection_Gid=" + obj.cltngid + "&Collection_Date=" + obj.cltndate + "&Group=" + obj.grp + "",
                data=datas,
                headers={"content-type": "application/json",
                         "Authorization": "" + token + ""
                         }, verify=False)
            response = resp.content.decode("utf-8")
            return HttpResponse(response)
        else:
            obj = mSales.Sales_Model()
            obj.custid = jsondata.get('params').get('custid')
            data = {"params": {"CLASSIFICATION": {
                "Entity_Gid": request.session['Entity_gid'],
                "Client_Gid": []},
                "DATA": {
                    "CustGroup_Gid": obj.custid,
                    "REF_Name": "3"
                }
            }
            }
            dataa = json.dumps(data)
            resp = requests.post(
                "" + ip + "/Cltn_Inv_Map_API?Action=COLLECTION&Type=INV_MAPPING&Collection_Gid=1&Collection_Date=&Group=GET_CLTN_INV_MAP",
                data=dataa,
                headers={"content-type": "application/json",
                         "Authorization": "" + token + ""
                         }, verify=False)
            response = resp.content.decode("utf-8")
            return HttpResponse(response)


def colset(request):
    utl.check_authorization(request)
    utl.check_pointaccess(request)
    if request.method == 'POST':
        token = jwt.token(request)
        jsondata = json.loads(request.body.decode('utf-8'))
        if (jsondata.get('Group')) == 'SET_INITIAL':
            obj = mSales.Sales_Model()
            obj.actn = jsondata.get('Action')
            obj.typ = jsondata.get('Type')
            obj.grp = jsondata.get('Group')
            obj.cusgid = json.dumps(jsondata.get('Customer_Gid'))
            obj.empgid = jsondata.get('Employee_Gid')
            obj.colmode = jsondata.get('Collection_Mode')
            obj.colamt = json.dumps(jsondata.get('Collection_Amount'))
            obj.coldat = jsondata.get('Collection_Date')
            obj.coldes = jsondata.get('Collection_Description')
            obj.entgid = request.session['Entity_gid']
            obj.colgid = json.dumps(jsondata.get('Collection_Gid'))
            dataa = json.dumps(jsondata.get("Params"))

            resp = requests.post(
                ip + "/FET_Collection_API?Action=" + obj.actn + "&Type=" + obj.typ + "&Group=" + obj.grp +
                "&Customer_Gid=" + obj.cusgid + "&Employee_Gid=" + obj.empgid + "&Collection_Mode=" + obj.colmode +
                "&Collection_Amount=" + obj.colamt + "&Collection_Date=" + obj.coldat + "&Collection_Description=" +
                obj.coldes + "&Entity_Gid=" + obj.entgid + "&Collection_Gid=" + obj.colgid + "",

                data=dataa,
                headers={"content-type": "application/json",
                         "Authorization": "" + token + ""
                         }, verify=False)
            response = resp.content.decode("utf-8")
            return HttpResponse(response)
        elif (jsondata.get('Group')) == 'INV_RECEIPT':
            obj = mSales.Sales_Model()
            obj.actn = jsondata.get('Action')
            obj.typ = jsondata.get('Type')
            obj.cmt = jsondata.get('commit')
            obj.cretby = json.dumps(jsondata.get('Create_by'))
            obj.grp = jsondata.get('Group')
            datas = json.dumps(jsondata.get('data'))

            resp = requests.post(
                "" + ip + "/FET_Collection_API?Action=" + obj.actn + "&Type=" + obj.typ + "&commit=" + obj.cmt +
                "&Create_by=" + obj.cretby + "&Group=" + obj.grp + "",
                "&entity" + request.session['Entity_gid'] + "",
                data=datas,
                headers={"content-type": "application/json",
                         "Authorization": "" + token + ""
                         }, verify=False)
            response = resp.content.decode("utf-8")
            return HttpResponse(response)
        elif (jsondata.get('Group')) == 'UPDATE_STATUS':
            obj = mSales.Sales_Model()
            obj.actn = jsondata.get('Action')
            obj.typ = jsondata.get('Type')
            obj.empgid = jsondata.get('Employee_Gid')
            obj.entitygid = request.session['Entity_gid']
            obj.grp = jsondata.get('Group')
            datas = json.dumps(jsondata.get('data'))
            resp = requests.post(
                "" + ip + "/FET_Collection_API?Action=" + obj.actn + "&Type=" +
                obj.typ + "&Group=" + obj.grp + "&Employee_Gid=" + obj.empgid + "&Entity_Gid=" + obj.entitygid + "",
                data=datas,
                headers={"content-type": "application/json",
                         "Authorization": "" + token + ""
                         }, verify=False)
            response = resp.content.decode("utf-8")
            return HttpResponse(response)
        elif (jsondata.get('Group')) == 'COLLECTION_DELETE':
            obj = mSales.Sales_Model()
            obj.actn = jsondata.get('Action')
            obj.typ = jsondata.get('Type')
            obj.headergid = json.dumps(jsondata.get('Collectionheader_gid'))
            obj.empgid = (jsondata.get('Employee_Gid'))
            obj.entitygid = request.session['Entity_gid']
            obj.grp = jsondata.get('Group')
            datas = {}
            resp = requests.post(
                "" + ip + "/FET_Collection_API?Action=" + obj.actn + "&Type=" + obj.typ + "&Group=" + obj.grp + "&Collection_Gid=" +
                obj.headergid + "&Employee_Gid=" + obj.empgid + "&Entity_Gid=" + obj.entitygid + "",
                data=datas,
                headers={"content-type": "application/json",
                         "Authorization": "" + token + ""
                         }, verify=False)
            response = resp.content.decode("utf-8")
            return HttpResponse(response)

        elif (jsondata.get('Group')) == 'UPDATE_DISPATCH':
            obj = mSales.Sales_Model()
            obj.actn = jsondata.get('Action')
            obj.typ = jsondata.get('Type')
            obj.crtby = json.dumps(jsondata.get('Create_by'))
            obj.grp = jsondata.get('Group')
            obj.inout = jsondata.get('In_Out')
            obj.couid = json.dumps(jsondata.get('Courier_Gid'))
            obj.ddate = jsondata.get('Dispatch_Date')
            obj.sndby = json.dumps(jsondata.get('Send_By'))
            obj.awbn = jsondata.get('AWB_No')
            obj.dmode = jsondata.get('Dispatch_Mode')
            obj.pack = jsondata.get('Packets')
            obj.wght = jsondata.get('Weight')
            obj.dto = jsondata.get('Dispatch_To')
            obj.adrs = jsondata.get('Address')
            obj.cty = jsondata.get('City')
            obj.stat = jsondata.get('State')
            obj.pcode = jsondata.get('Pincode')
            obj.rmrk = jsondata.get('Remark')
            obj.retrnd = jsondata.get('Returned')
            obj.stts = jsondata.get('Status')
            obj.empgid = (jsondata.get('Employee_Gid'))
            obj.entitygid = request.session['Entity_gid']
            obj.grp = jsondata.get('Group')
            datas = json.dumps(jsondata.get('data'))
            resp = requests.post(
                "" + ip + "/FET_Collection_API?Action=" + obj.actn + "&Type=" + obj.typ +
                "&Create_by=" + obj.crtby + "&Group=" + obj.grp + "&In_Out=" + obj.inout + "&Courier_Gid=" + obj.couid +
                "&Dispatch_Date=" + obj.ddate + "&Send_By=" + obj.sndby + "&AWB_No=" + obj.awbn +
                "&Dispatch_Mode=" + obj.dmode + "&Packets=" + obj.pack + "&Weight=" + obj.wght + "&Dispatch_To=" + obj.dto +
                "&Address=" + obj.adrs + "&City=" + obj.cty + "&State=" + obj.stat + "&Pincode=" + obj.pcode + "&Remark=" + obj.rmrk + "&Returned=" + obj.retrnd + "&Status=" + obj.stts + "&Entity_Gid=" + obj.entitygid + "&Employee_Gid=" + obj.empgid + "",
                data=datas,
                headers={"content-type": "application/json",
                         "Authorization": "" + token + ""
                         }, verify=False)
            response = resp.content.decode("utf-8")
            return HttpResponse(response)


def exclread(request):
    utl.check_authorization(request)
    utl.check_pointaccess(request)
    if request.method == 'POST':
        token = jwt.token(request)
        jsondata = json.loads(request.body.decode('utf-8'))
        if (jsondata.get('Group')) == 'BANK_STMT_MAPPING_GET':
            obj = mSales.Sales_Model()
            obj.grp = jsondata.get('Group')
            obj.sbtyp = jsondata.get('Sub_Type')
            obj.typ = jsondata.get('Type')
            datas = json.dumps(jsondata.get('data'))

            headers = {"content-type": "application/json",
                       "Authorization": "" + token + ""
                       }
            params = {'Type': "" + obj.typ + "", 'Sub_Type': "" + obj.sbtyp + "", 'Group': "" + obj.grp + "",
                      "entity": request.session['Entity_gid']}
            resp = requests.post("" + ip + "/BankUpload_API", params=params, data=datas, headers=headers, verify=False)
            response = resp.content.decode("utf-8")
            return HttpResponse(response)
        elif (jsondata.get('Group')) == 'BANK_STMT_MAPPING_SET':
            obj = mSales.Sales_Model()
            obj.grp = jsondata.get('Group')
            obj.actn = jsondata.get('Action')
            obj.empgid = jsondata.get('Employee_Gid')
            obj.typ = jsondata.get('Type')
            datas = json.dumps(jsondata.get('data'))
            headers = {"content-type": "application/json",
                       "Authorization": "" + token + ""
                       }
            params = {'Type': "" + obj.typ + "", 'Group': "" + obj.grp + "", 'Action': "" + obj.actn + "",
                      'Employee_Gid': "" + obj.empgid + "", "entity": request.session['Entity_gid']}
            resp = requests.post("" + ip + "/BankUpload_API", params=params, data=datas, headers=headers, verify=False)
            response = resp.content.decode("utf-8")
            return HttpResponse(response)


def custgroupget(request):
    utl.check_authorization(request)
    utl.check_pointaccess(request)
    if request.method == 'POST':
        token = jwt.token(request)
        jsondata = json.loads(request.body.decode('utf-8'))
        if (jsondata.get('Group')) == 'CUST_GROUP_GET':
            obj = mSales.Sales_Model()
            obj.grp = jsondata.get('Group')
            obj.entygid = jsondata.get('Entity_Gid')
            obj.grpcode = json.dumps(jsondata.get('Cust_Group_Code'))
            obj.grpgid = json.dumps(jsondata.get('Cust_Group_Gid'))
            obj.grpname = jsondata.get('Cust_Group_Name')
            obj.limit = jsondata.get('Query_Limit')
            params = {'Group': "" + obj.grp + "", 'Entity_Gid': "" + obj.entygid + "",
                      'Cust_Group_Gid': "" + obj.grpgid + "", 'Cust_Group_Code': "" + obj.grpcode + "",
                      'Cust_Group_Name': "" + obj.grpname + "", 'Query_Limit': "" + obj.limit + ""}
            headers = {"content-type": "application/json", "Authorization": "" + token + ""}
            datas = {}
            resp = requests.post("" + ip + "/Customer_API", params=params, data=datas, headers=headers, verify=False)
            response = resp.content.decode("utf-8")
            return HttpResponse(response)
        elif (jsondata.get('Group')) == 'CUST_GET':
            obj = mSales.Sales_Model()
            obj.grp = jsondata.get('Group')
            obj.entygid = request.session['Entity_gid']
            params = {'Group': "" + obj.grp + "", 'Entity_Gid': "" + obj.entygid + ""}
            headers = {"content-type": "application/json", "Authorization": "" + token + ""}
            datas = json.dumps(jsondata.get('data'))
            resp = requests.post("" + ip + "/Customer_API", params=params, data=datas, headers=headers, verify=False)
            response = resp.content.decode("utf-8")
            return HttpResponse(response)


def taviewget(request):
    utl.check_authorization(request)
    utl.check_pointaccess(request)
    if request.method == 'POST':
        token = jwt.token(request)
        jsondata = json.loads(request.body.decode('utf-8'))
        jsondata['Params']['CLASSIFICATION']['Entity_Gid'] = request.session['Entity_gid']
        if (jsondata.get('Params').get('Group')) == 'CLAIM_INITIAL_SUMMARY':
            grp = jsondata.get('Params').get('Group')
            typ = jsondata.get('Params').get('Type')
            sbtyp = jsondata.get('Params').get('Sub_Type')
            params = {'Group': "" + grp + "", 'Type': "" + typ + "", 'Sub_Type': "" + sbtyp + ""}
            headers = {"content-type": "application/json", "Authorization": "" + token + ""}
            datas = json.dumps(jsondata)
            resp = requests.post("" + ip + "/Claim_Initial", params=params, data=datas, headers=headers, verify=False)
            response = resp.content.decode("utf-8")
            return HttpResponse(response)


def query_summary_salesget(request):
    utl.check_authorization(request)
    utl.check_pointaccess(request)
    if request.method == 'POST':
        token = jwt.token(request)
        jsondata = json.loads(request.body.decode('utf-8'))
        if (jsondata.get('Params').get('Group')) == 'QUERYSUMMARY':
            obj = mSales.Sales_Model()
            obj.grp = jsondata.get('Params').get('Group')
            obj.typ = jsondata.get('Params').get('Type')
            obj.sbtyp = jsondata.get('Params').get('Sub_Type')
            params = {'Group': "" + obj.grp + "", 'Type': "" + obj.typ + "", 'Sub_Type': "" + obj.sbtyp + "",
                      "entity": request.session['Entity_gid']}
            headers = {"content-type": "application/json", "Authorization": "" + token + ""}
            datas = json.dumps(jsondata)
            resp = requests.post("" + ip + "/apiurl_Query_SummarySales", params=params, data=datas, headers=headers,
                                 verify=False)
            response = resp.content.decode("utf-8")
            return HttpResponse(response)


def query_summary_salesproductget(request):
    utl.check_authorization(request)
    if request.method == 'POST':
        token = jwt.token(request)
        jsondata = json.loads(request.body.decode('utf-8'))
        if (jsondata.get('Params').get('Group')) == 'QUERYSUMMARY':
            grp = jsondata.get('Params').get('Group')
            typ = jsondata.get('Params').get('Type')
            sbtyp = jsondata.get('Params').get('Sub_Type')
            params = {'Group': "" + grp + "", 'Type': "" + typ + "", 'Sub_Type': "" + sbtyp + "",
                      "entity_gid": request.session['Entity_gid']}
            headers = {"content-type": "application/json", "Authorization": "" + token + ""}
            datas = json.dumps(jsondata)
            resp = requests.post("" + ip + "/apiurl_Query_SummarySalesProduct", params=params, data=datas,
                                 headers=headers, verify=False)
            response = resp.content.decode("utf-8")
            return HttpResponse(response)


def query_summary_collectionget(request):
    utl.check_authorization(request)
    utl.check_pointaccess(request)
    if request.method == 'POST':
        token = jwt.token(request)
        jsondata = json.loads(request.body.decode('utf-8'))
        if (jsondata.get('Params').get('Group')) == 'QUERYSUMMARY':
            grp = jsondata.get('Params').get('Group')
            typ = jsondata.get('Params').get('Type')
            sbtyp = jsondata.get('Params').get('Sub_Type')
            params = {'Group': "" + grp + "", 'Type': "" + typ + "", 'Sub_Type': "" + sbtyp + "",
                      "entity": request.session['Entity_gid']}
            headers = {"content-type": "application/json", "Authorization": "" + token + ""}
            datas = json.dumps(jsondata)
            resp = requests.post("" + ip + "/apiurl_Query_SummaryCollection", params=params, data=datas,
                                 headers=headers, verify=False)
            response = resp.content.decode("utf-8")
            return HttpResponse(response)


def query_summary_outstandingget(request):
    utl.check_authorization(request)
    utl.check_pointaccess(request)
    if request.method == 'POST':
        token = jwt.token(request)
        jsondata = json.loads(request.body.decode('utf-8'))
        if (jsondata.get('Params').get('Group')) == 'QUERYSUMMARY':
            grp = jsondata.get('Params').get('Group')
            typ = jsondata.get('Params').get('Type')
            sbtyp = jsondata.get('Params').get('Sub_Type')
            params = {'Group': "" + grp + "", 'Type': "" + typ + "", 'Sub_Type': "" + sbtyp + "",
                      "entity": request.session['Entity_gid']}
            headers = {"content-type": "application/json", "Authorization": "" + token + ""}
            datas = json.dumps(jsondata)
            resp = requests.post("" + ip + "/apiurl_Query_SummaryOutstanding", params=params, data=datas,
                                 headers=headers, verify=False)
            response = resp.content.decode("utf-8")
            return HttpResponse(response)


def query_summary_getcollectionstatus(request):
    utl.check_authorization(request)
    if request.method == 'POST':
        token = jwt.token(request)
        jsondata = json.loads(request.body.decode('utf-8'))
        if (jsondata.get('Params').get('Group')) == 'QUERYSUMMARY':
            grp = jsondata.get('Params').get('Group')
            typ = jsondata.get('Params').get('Type')
            sbtyp = jsondata.get('Params').get('Sub_Type')
            params = {'Group': "" + grp + "", 'Type': "" + typ + "", 'Sub_Type': "" + sbtyp + ""}
            headers = {"content-type": "application/json", "Authorization": "" + token + ""}
            datas = json.dumps(jsondata)
            resp = requests.post("" + ip + "/apiurl_query_summary_getcollectionstatus", params=params, data=datas,
                                 headers=headers, verify=False)
            response = resp.content.decode("utf-8")
            return HttpResponse(response)


def gettadetails(request):
    utl.check_authorization(request)
    utl.check_pointaccess(request)
    if request.method == 'POST':
        token = jwt.token(request)
        jsondata = json.loads(request.body.decode('utf-8'))
        jsondata['Params']['CLASSIFICATION']['Entity_Gid'] = request.session['Entity_gid']
        if (jsondata.get('Params').get('Group')) == 'CLAIM_APPROVE_PROCESS':
            grp = jsondata.get('Params').get('Group')
            typ = jsondata.get('Params').get('Type')
            sbtyp = jsondata.get('Params').get('Sub_Type')
            action = jsondata.get('Params').get('Action')
            empgid = json.dumps(jsondata.get('Params').get('Employee_Gid'))
            params = {'Group': "" + grp + "", 'Type': "" + typ + "", 'Sub_Type': "" + sbtyp + "",
                      'Action': "" + action + "", 'Employee_Gid': "" + empgid + ""}
            headers = {"content-type": "application/json", "Authorization": "" + token + ""}
            datas = json.dumps(jsondata)
            resp = requests.post("" + ip + "/Claim_Initial", params=params, data=datas, headers=headers, verify=False)
            response = resp.content.decode("utf-8")
            return HttpResponse(response)


def getreceipt(request):
    utl.check_authorization(request)
    utl.check_pointaccess(request)
    if request.method == 'POST':
        token = jwt.token(request)
        jsondata = json.loads(request.body.decode('utf-8'))
        if (jsondata.get('Group')) == 'AR_RECEIPT_COLLECTION':
            obj = mSales.Sales_Model()
            obj.grp = jsondata.get('Group')
            obj.typ = jsondata.get('Type')
            obj.sbtyp = jsondata.get('Sub_Type')
            params = {'Group': "" + obj.grp + "", 'Type': "" + obj.typ + "", 'Sub_Type': "" + obj.sbtyp + "",
                      "entity": request.session['Entity_gid']}
            headers = {"content-type": "application/json", "Authorization": "" + token + ""}
            datas = json.dumps(jsondata.get('data'))
            resp = requests.post("" + ip + "/Receipt_AR", params=params, data=datas, headers=headers, verify=False)
            response = resp.content.decode("utf-8")
            return HttpResponse(response)
        elif (jsondata.get('Group')) == 'AR_INV_MAPPING_RECEIPT_SET':
            obj = mSales.Sales_Model()
            obj.grp = jsondata.get('Group')
            obj.typ = jsondata.get('Type')
            obj.cmt = jsondata.get('Commit')
            obj.actn = jsondata.get('Action')

            obj.crtby = jsondata.get('Create_by')
            params = {'Group': "" + obj.grp + "", 'Type': "" + obj.typ + "", 'Action': "" + obj.actn + "",
                      "entity": request.session['Entity_gid'],
                      'Commit': "" + obj.cmt + "", 'Create_by': "" + obj.crtby + ""}
            headers = {"content-type": "application/json", "Authorization": "" + token + ""}
            datas = json.dumps(jsondata.get('data'))
            resp = requests.post("" + ip + "/Receipt_AR", params=params, data=datas, headers=headers, verify=False)
            response = resp.content.decode("utf-8")
            return HttpResponse(response)


def getcustemp(request):
    utl.check_authorization(request)
    utl.check_pointaccess(request)
    if request.method == 'GET':
        token = jwt.token(request)
        obj = mFET.FET_model()
        obj.action = request.GET['action']
        obj.emp_gid = request.session['Emp_gid']
        obj.entity = request.session['Entity_gid']
        resp = requests.get(
            "" + ip + "/Customer_Mapped?action=" + obj.action + "&emp_gid=" + obj.emp_gid + "&Entity_gid=" + obj.entity + "",
            headers={"content-type": "application/json",
                     "Authorization": "" + token + ""
                     }, verify=False)
        response = resp.content.decode("utf-8")
        return HttpResponse(response)


def getbankname(request):
    utl.check_authorization(request)
    utl.check_pointaccess(request)
    if request.method == 'GET':
        token = jwt.token(request)
        obj = mFET.FET_model()
        obj.tblname = request.GET['table_name']
        obj.srchid = request.GET['search_gid']
        obj.srchname = request.GET['search_name']
        obj.entityid = request.GET['entity_gid']
        resp = requests.get(
            "" + ip + "/common_dataAPI?table_name=" + obj.tblname + "&search_gid=" + obj.srchid + "&search_name=" + obj.srchname + "&entity_gid=" + obj.entityid + "",
            headers={"content-type": "application/json",
                     "Authorization": "" + token + ""
                     }, verify=False)
        response = resp.content.decode("utf-8")
        return HttpResponse(response)


def outstndng(request):
    utl.check_authorization(request)
    utl.check_pointaccess(request)
    if request.method == 'POST':
        token = jwt.token(request)
        jsondata = json.loads(request.body.decode('utf-8'))
        if (jsondata.get('type')) == 'OUTSTANDING_AR_RECEIPTMAKING':
            obj = mSales.Sales_Model()
            obj.typ = jsondata.get('type')
            obj.sbtyp = jsondata.get('sub_type')
            params = {'Type': "" + obj.typ + "", 'Sub_Type': "" + obj.sbtyp + "",
                      "entity": request.session['Entity_gid']}
            headers = {"content-type": "application/json", "Authorization": "" + token + ""}
            datas = json.dumps(jsondata.get('data'))
            resp = requests.post("" + ip + "/Outstanding_AR", params=params, data=datas, headers=headers, verify=False)
            response = resp.content.decode("utf-8")
            return HttpResponse(response)
        elif (jsondata.get('type')) == 'OUTSTANDING_AR_BCL':
            obj = mSales.Sales_Model()
            obj.typ = jsondata.get('type')
            obj.sbtyp = jsondata.get('sub_type')
            params = {'Type': "" + obj.typ + "", 'Sub_Type': "" + obj.sbtyp + "",
                      "entity": request.session['Entity_gid']}
            headers = {"content-type": "application/json", "Authorization": "" + token + ""}
            datas = json.dumps(jsondata.get('data'))
            resp = requests.post("" + ip + "/Outstanding_AR", params=params, data=datas, headers=headers, verify=False)
            response = resp.content.decode("utf-8")
            return HttpResponse(response)
        elif (jsondata.get('type')) == 'OUTSTANDING_REPORT_INVOICE_WISE':
            obj = mSales.Sales_Model()
            obj.typ = jsondata.get('type')
            obj.sbtyp = jsondata.get('sub_type')
            params = {'Type': "" + obj.typ + "", 'Sub_Type': "" + obj.sbtyp + "",
                      "entity": request.session['Entity_gid']}
            headers = {"content-type": "application/json", "Authorization": "" + token + ""}
            datas = json.dumps(jsondata.get('data'))
            XLSX_MIME = 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
            response = HttpResponse(content_type=XLSX_MIME)
            filename = Excelfilename('Outstandingreport Details_')
            response['Content-Disposition'] = 'attachment; filename="{}"'.format(filename)
            # response['Content-Disposition'] = 'attachment; filename="Outstandingreport.xlsx"'
            writer = pd.ExcelWriter(response, engine='xlsxwriter')
            resp = requests.post("" + ip + "/Outstanding_AR", params=params, data=datas, headers=headers, verify=False)
            respons = resp.content.decode("utf-8")
            df = json.loads(respons)
            dff = pd.DataFrame(df)
            dff.to_excel(writer, 'Sheet1')
            writer.save()
            return response


def custmer_get(request):
    utl.check_authorization(request)
    utl.check_pointaccess(request)
    if request.method == 'POST':
        token = jwt.token(request)
        jsondata = json.loads(request.body.decode('utf-8'))
        # jsondata['CLASSIFICATION']['Entity_Gid'] = decry_data(request.session['Entity_Gid'])
        if (jsondata.get('Group')) == 'CUST_All_GET':
            obj = mSales.Sales_Model()
            obj.typ = jsondata.get('Type')
            obj.sbtyp = jsondata.get('Sub_Type')
            obj.limit = jsondata.get('Limit')
            params = {"entity": request.session['Entity_gid'], 'Group': "" + jsondata.get('Group') + "",
                      'Type': "" + obj.typ + "", 'Sub_Type': "" + obj.sbtyp + "", 'Limit': "" + obj.limit + ""}
            headers = {"content-type": "application/json", "Authorization": "" + token + ""}
            datas = json.dumps(jsondata.get('data'))
            resp = requests.post("" + ip + "/Customer_Get_API", params=params, data=datas, headers=headers,
                                 verify=False)
            response = resp.content.decode("utf-8")
            return HttpResponse(response)
        elif (jsondata.get('Group')) == 'CUSTOMER_ADDRESS':
            obj = mSales.Sales_Model()
            obj.typ = jsondata.get('Type')
            obj.sbtyp = jsondata.get('Sub_Type')
            obj.limit = jsondata.get('Limit')
            params = {'Group': "" + jsondata.get('Group') + "", 'Type': "" + obj.typ + "",
                      "entity": request.session['Entity_gid'],
                      'Sub_Type': "" + obj.sbtyp + "", 'Limit': "" + obj.limit + ""}
            headers = {"content-type": "application/json", "Authorization": "" + token + ""}
            datas = json.dumps(jsondata.get('data'))
            resp = requests.post("" + ip + "/Customer_Get_API", params=params, data=datas, headers=headers,
                                 verify=False)
            response = resp.content.decode("utf-8")
            return HttpResponse(response)


def getclustermaster(request):
    utl.check_authorization(request)
    utl.check_pointaccess(request)
    if request.method == 'POST':
        token = jwt.token(request)
        jsondata = json.loads(request.body.decode('utf-8'))
        if (jsondata.get('Group')) == 'CLUSTER_EMPMAP_FLAG':
            jsondata = json.loads(request.body.decode('utf-8'))
            # jsondata['Classification']['entity_gid'] = decry_data(request.session['Entity_gid'])
            jsondata['data']['Classification']['entity_gid'] = 1
            group = jsondata.get('Group')
            params = {'Group': "" + group + ""}
            headers = {"content-type": "application/json", "Authorization": "" + token + ""}
            datas = json.dumps(jsondata.get('data'))
            resp = requests.post("" + ip + "/cluster_Master", params=params, data=datas, headers=headers, verify=False)
            response = resp.content.decode("utf-8")
            return HttpResponse(response)


def employeeddl(request):
    utl.check_authorization(request)
    utl.check_pointaccess(request)
    if request.method == 'GET':
        token = jwt.token(request)
        obj = mFET.FET_model()
        obj.entityid = request.GET['entity_gid']
        obj.srchid = request.GET['clusterid']
        obj.action = request.GET['action']
        resp = requests.get(
            "" + ip + "/Employee_Profile?Entity_gid=" + obj.entityid + "&Action=" + obj.action + "&Cluster_Gid=" + obj.srchid + "",
            headers={"content-type": "application/json",
                     "Authorization": "" + token + ""
                     }, verify=False)
        response = resp.content.decode("utf-8")
        return HttpResponse(response)


def Productsmry(request):
    try:
        utl.check_authorization(request)
        if request.method == 'POST':
            token = jwt.token(request)
            jsondata = json.loads(request.body.decode('utf-8'))
            if (jsondata.get('Group')) == "Product_Get":
                form = mFET.FET_model()
                form.type = jsondata.get('Type')
                form.subtype = jsondata.get('SubType')
                form.grp = jsondata.get('Group')
                params = {'Group': "" + form.grp + "", 'Type': "" + form.type + "",
                          'SubType': "" + form.subtype + "",
                          'Entity_gid': json.dumps({'Entity_Gid': request.session['Entity_gid']})}
                common.logger.error([{"LG_Pdct_Token_Test": token[0:20]}])
                headers = {"content-type": "application/json", "Authorization": "" + token + ""}
                datas = json.dumps(jsondata.get('data'))
                resp = requests.post("" + ip + "/Product_Master", params=params, data=datas, headers=headers,
                                     verify=False)
                response = resp.content.decode("utf-8")
                common.logger.error([{"LG_Pdct_Resp": str(resp)[0:100]}])
                common.logger.error([{"LG_Pdct_Response": str(response)[0:50]}])
                return HttpResponse(response)
            elif (jsondata.get('Group')) == "Product_Set":
                form = mFET.FET_model()
                form.action = jsondata.get('action')
                form.type = jsondata.get('type')
                form.group = jsondata.get('Group')
                entity = {"Entity_Gid": request.session['Entity_gid']}
                create_by = {"Create_By": request.session['Emp_gid']}
                jsondata.get('data').update(entity)
                jsondata.get('data').update(create_by)
                params = {'Group': "" + form.group + "", 'Action': "" + form.action + "",
                          'Type': "" + form.type + ""}
                headers = {"content-type": "application/json", "Authorization": "" + token + ""}
                datas = json.dumps(jsondata.get('data'))
                resp = requests.post("" + ip + "/Product_Master", params=params, data=datas, headers=headers,
                                     verify=False)
                response = resp.content.decode("utf-8")
                temp_datas = {}
                try:
                    print(json.loads(response)['MESSAGE'])
                    if (json.loads(response)['MESSAGE'] == 'SUCCESS'):
                        temp_datas = json.loads(datas)
                        data = temp_datas['data']
                        #print(data)
                        master_data=get_data_from_id('Product',data)
                        common.logger.error('product code data:'+str(master_data))
                        data = {'code':master_data['code'],"name": data['product_name'], "weight": int(data['product_weight']) ,
                                "unitprice": int(data['product_unitprice']), "uom_code": master_data['uom_code'],
                                "hsn_code": master_data['hsn_code'], "category_code": master_data['category_code'],
                                "subcategory_code": master_data['subcategory_code'],
                                "productcategory_code": master_data['productcategory_code'],
                                "producttype_code": master_data['producttype_code'],'Entity_Gid':entity['Entity_Gid'],'create_by':create_by['Create_By']}


                        mrobject = MasterRequestObject("PRODUCT", data, 'POST')
                except:
                    common.logger.error(str(traceback.print_exc()))
                try:
                    Stock_impact = None
                    if (temp_datas['Stock_impact'] == 'Y'):
                        Stock_impact = True
                    else:
                        Stock_impact = False
                    from Bigflow.Core.models import get_data_from_id as gdfi
                    print("checkdata: ",temp_datas)
                    data = {'name': temp_datas['Productcat_Name'], 'isprodservice': True, 'stockimpact': Stock_impact,
                            'client_id': temp_datas['Client_Gid'],'Entity_Gid':entity,'create_by':create_by}
                    codes = gdfi('PRODUCTCAT', data)
                    data['code']=codes['code']
                    if (json.loads(response)['MESSAGE'] == 'SUCCESS'):
                        print(data)
                        mrobject = MasterRequestObject("PRODUCT CATEGORY", data, 'POST')
                except:
                    pass
                return HttpResponse(response)

    except Exception as e:
        common.logger.error([{"LG_Pdct_Execption": str(e)}])


def producttypeset(request):
    utl.check_authorization(request)
    if request.method == 'POST':
        token = jwt.token(request)
        jsondata = json.loads(request.body.decode('utf-8'))
        if (jsondata.get(
                'Group')) == 'Product_Type' or 'Product_Type1' or 'Product_Carton_Map' or 'Product_Carton_Map1' or 'insert_data' or 'Product_Category' or 'Product_Category1':
            grp = jsondata.get('Group')
            action = jsondata.get('Action')
            typ = jsondata.get('Type')
            params = {'Group': "" + grp + "", 'Action': "" + action + "", 'Type': "" + typ + ""}
            headers = {"content-type": "application/json", "Authorization": "" + token + ""}
            entity = {"Entity_Gid": request.session['Entity_gid']}
            create_by = {"Create_By": request.session['Emp_gid']}
            jsondata.get('data').update(entity)
            jsondata.get('data').update(create_by)
            datas = json.dumps(jsondata.get('data'))
            temp_datas=json.loads(datas)
            resp = requests.post("" + ip + "/ProductCat_type_Set", params=params, data=datas, headers=headers,
                                 verify=False)
            response = resp.content.decode("utf-8")
            try:
                Stock_impact = None
                if (temp_datas['Stock_impact'] == 'Y'):
                    Stock_impact = True
                else:
                    Stock_impact = False
                from Bigflow.Core.models import get_data_from_id as gdfi
                try:
                    data = {'name': temp_datas['Productcat_Name'], 'isprodservice': True, 'stockimpact': Stock_impact,
                            'client_id': temp_datas['Client_Gid'],'Entity_Gid':entity['Entity_Gid'],'create_by':create_by['Create_By']}
                    if (json.loads(response)['MESSAGE'] == 'SUCCESS'):
                        isprodservice=data.pop('isprodservice')
                        stockimpact=data.pop('stockimpact')
                        codes = gdfi('PRODUCTCAT', data)
                        data['code'] = codes['code']
                        data['stockimpact']=stockimpact
                        data['isprodservice']=isprodservice
                        #print(temp_datas)
                        # print(data)
                        mrobject = MasterRequestObject("PRODUCT CATEGORY", data, 'POST')
                except:
                    pass
            except:
                temp_datas = json.loads(datas)
                #print(temp_datas,json.loads(response)['MESSAGE'])
                codes=get_data_from_id('Product_Type',temp_datas)
                print(codes)
                data = {'code':codes['code'],'productcategory_code': codes['Producttype_Category_code'],
                        'name': str(temp_datas['Producttype_Name']),'Entity_Gid':entity['Entity_Gid'],'create_by':create_by['Create_By']}
                if (json.loads(response)['MESSAGE'] == 'SUCCESS'):
                    mrobject = MasterRequestObject("PRODUCT TYPE", data, 'POST')
            return HttpResponse(response)


# barcode list
def barcodesdata():
    obj_dropdown = mPurchase.Purchase_model()
    obj_dropdown.action = 'Product'
    obj_dropdown.json_data = '{"Table_name": "ap_trn_tinvoiceheader","Column_1": "invoiceheader_gid,invoiceheader_barcode, invoiceheader_imagepath","Column_2": "","Where_Common": "invoiceheader","Where_Primary": "","Primary_Value": "","Order_by": "gid"}'
    obj_dropdown.entity_gid = 1
    df_dropexec = obj_dropdown.get_alltablevalue()
    jdata = df_dropexec
    # df=df_dropexec[['']]
    return jdata


def find_ext(dr, ext):
    return glob(path.join(dr, "*.{}".format(ext)))


def removefile(myfile):
    try:
        os.remove(myfile)
    except OSError as e:  ## if failed, report it back to the user ##
        print("Error: %s - %s." % (e.filename, e.strerror))


# barcode list
def barcodesdata():
    obj_dropdown = mPurchase.Purchase_model()
    obj_dropdown.action = 'Product'
    obj_dropdown.json_data = '{"Table_name": "ap_trn_tinvoiceheader","Column_1": "invoiceheader_gid,invoiceheader_barcode, invoiceheader_imagepath","Column_2": "","Where_Common": "invoiceheader","Where_Primary": "","Primary_Value": "","Order_by": "gid"}'
    obj_dropdown.entity_gid = 1
    df_dropexec = obj_dropdown.get_alltablevalue()
    jdata = df_dropexec
    # df=df_dropexec[['']]
    return jdata


import re
from django.conf import settings


def sorted_aphanumeric(data):
    convert = lambda text: int(text) if text.isdigit() else text.lower()
    alphanum_key = lambda key: [convert(c) for c in re.split('([0-9]+)', key)]
    return sorted(data, key=alphanum_key)


def scanning_barcode(request):
    utl.check_authorization(request)
    utl.check_pointaccess(request)
    if request.method == 'POST':
        token = jwt.token(request)
        dd = base64.b64encode(request.FILES['file'].read())
        current_month = datetime.datetime.now().strftime('%m')
        current_day = datetime.datetime.now().strftime('%d')
        current_year_full = datetime.datetime.now().strftime('%Y')
        pdfcount = request.POST['pdfcount']
        filecount = request.POST['filecount']
        barcodenum = request.POST['barcodenum']
        entity = request.session['Entity_gid']
        employee_gid = request.session['Emp_gid']
        ress = dd.decode("utf-8")
        param = {'Group': "" + 'CLAIM_INITIAL_SET' + "", 'Action': "" + 'Insert' + "",
                 'Type': "" + 'CLAIM_INITIAL' + "", 'Sub_Type': "" + 'TEMP' + "", 'PDF_count': str(pdfcount),
                 'Employee_Gid': + employee_gid}
        resultdata = {
            "Params": {
                "File": [{
                    "File_Name": (request.POST['name']),
                    "File_Extension": (request.POST['file_extension']),
                    "File_Base64data": ress
                }]
            }
        }
        dta = json.dumps(resultdata)
        headers = {"content-type": "application/json", "Authorization": "" + token + ""}
        resp = requests.post("" + ip + "/Scanning", params=param, data=dta, headers=headers, verify=False)
        subpath = (settings.MEDIA_ROOT) + '/INWARD/' + str(current_year_full) + '/' + str(current_month) + '/' + str(
            current_day) + '/' + str(employee_gid)
        file_path = subpath + '/Tempinward/'
        if int(filecount) == int(pdfcount):
            for pat, subdirs, files in os.walk(subpath):
                if 'Bigflow_Image' not in subdirs:
                    Image_dir = "" + subpath + "" + '/Bigflow_Image/'
                    os.mkdir(Image_dir)
                    break
                else:
                    Image_dir = "" + subpath + "" + '/Bigflow_Image/'
                    break
            for pat, subdirs, files in os.walk(subpath):
                if 'Bigflow_pdf' not in subdirs:
                    pdf_dir = "" + subpath + "" + '/Bigflow_pdf/'
                    os.mkdir(pdf_dir)
                    break
                else:
                    pdf_dir = "" + subpath + "" + '/Bigflow_pdf/'
                    break

            pdf_to_imagearray = []
            for pat, subdirs, files in os.walk(file_path):
                time.sleep(5)
                d = sorted_aphanumeric(os.listdir(pat))
                for filename in d:
                    filenam = pat + filename
                    pdf_to_imagearray.append(filenam)
                    with tempfile.TemporaryDirectory() as path:
                        images_from_path = convert_from_path(filenam, output_folder=path, last_page=1, first_page=0)
                    base_filename = os.path.splitext(os.path.basename(filenam))[0] + '.jpg'

                    for page in images_from_path:
                        page.save(os.path.join(Image_dir, base_filename), 'JPEG')
                    removefile(filenam)
            # ---------------------------------------
            imagesarray = []
            for pat, subdirs, files in os.walk(Image_dir):
                d = sorted_aphanumeric(os.listdir(pat))
                for filename in d:
                    filenam = pat + filename
                    imagesarray.append(filenam)
            # ----------------------------------------
            ouputarray = []
            subarray = []
            d = {"bar": '', "image": subarray}
            barcodelist = []
            count = 0
            data = []
            try:
                for i in imagesarray:
                    image = cv2.imread(i, cv2.IMREAD_GRAYSCALE)
                    time.sleep(0.3)
                    barcodes = pyzbar.decode(image)
                    # print(barcodes)
                    inbarnum = 0
                    inbarchar = 0
                    for br in barcodenum:
                        if (br.isdigit()):
                            inbarnum = inbarnum + 1
                        else:
                            inbarchar = inbarchar + 1
                    if barcodes != []:
                        if len(barcodes) >= 1:
                            for barcode in barcodes:
                                barcodeData = barcode.data.decode('utf-8')
                                barcodelist.append(barcodeData)
                                data.append(barcodeData)
                            for j in data:
                                barnum = 0
                                barchar = 0
                                for sub in range(len(j)):
                                    if (j[sub].isdigit()):
                                        barnum = barnum + 1
                                    else:
                                        barchar = barchar + 1
                                if barnum == inbarnum and barchar == inbarchar:
                                    count = count + 1
                                    d = {"bar": count, "image": [i], "barcodename": barcodeData}
                                    ouputarray.append(d)
                                    data = []
                                else:
                                    if d["bar"] == count:
                                        data = []
                                        d["image"].append(i)
                                    d["image"] = list(dict.fromkeys(d["image"]))
                    else:
                        print(count)
                        if d["bar"] == count:
                            d["image"].append(i)
            except Exception as e:
                pass
            if (len(ouputarray) == 0):
                shutil.rmtree(subpath)
                return HttpResponse("No relavent barcode in pdf")
            # ---------------------------------------
            count2 = 0
            for i in range(len(ouputarray)):
                pdf = FPDF()
                count2 = count2 + 1
                for image in ouputarray[i]['image']:
                    print(image)
                    pdf.add_page()
                    pdf.image(image, 10, 10, 190)
                    pdffilename = str(ouputarray[i]['barcodename'])
                    # removefile(image)
                pdf.output("" + pdf_dir + "" + pdffilename + ".pdf", "F")
            # compare barcode
            df = barcodesdata()
            for k in barcodelist:
                Docs = df[df['invoiceheader_barcode'].astype(str).str[:].str.contains(k, na=False, case=False)]
                if not Docs.empty:
                    params = {'Group': 'SCAN_IMAGE_BARCODE', 'Employee_Gid': employee_gid,
                              'pdf_name': str(k), 'entity': entity}
                    headers = {"content-type": "application/json", "Authorization": "" + token + ""}
                    try:

                        with open("" + pdf_dir + "" + str(k) + ".pdf", "rb") as pdf_file:
                            encoded_string = base64.b64encode(pdf_file.read())
                        pdfdecodeddata = encoded_string.decode("utf-8")
                        datas = {"Params": {
                            "File": [{
                                "File_Name": "" + str(k) + "",
                                "File_Extension": "pdf",
                                "File_Base64data": pdfdecodeddata
                            }],
                            "CLASSIFICATION": {"Entity_Gid": [request.session['Entity_gid']]}
                        }}
                        resp = requests.post("" + ip + "/File_Upload_Barcode", params=params, data=json.dumps(datas),
                                             headers=headers,
                                             verify=False)

                    except:
                        continue
            shutil.rmtree(subpath)
            return HttpResponse("SUCESS")
        else:
            pass


def barcode(request):
    utl.check_authorization(request)
    utl.check_pointaccess(request)
    return render(request, "FET/barcodescanning.html")


def micro_token_gen():
    try:
        ip = common.memoapi_url()
        response = requests.post("" + ip + "/usrserv/auth_token", params="",
                                 data='{"username": "apuser","password": "dnNvbHYxMjM="}', headers="", verify=False)
        # response = json.loads(response.content)
        datas = json.loads(response.content.decode("utf-8"))
        access_token = datas.get("token")
        return access_token
    except Exception as e:
        return ({"MESSAGE": "ERROR_OCCURED" + str(e)})



def check_memo_employee_num(data):
    data = json.dumps(data.get('Params').get('Filter'))
    ip = common.memoapi_url()
    generated_token_data = micro_token_gen()
    headers = {"content-type": "application/json", "Authorization": "" + generated_token_data + ""}
    resp = requests.post("" + ip + "/usrserv/employeemobileno", params="", data=data, headers=headers, verify=False)
    response = json.loads(resp.content)
    resp = response['MESSAGE']
    return resp

def update_personal_info(request):
    # utl.check_authorization(request)
    utl.check_pointaccess(request)
    if request.method == 'POST':
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
                        break
                    if i != j:
                        cond_tion = False
                        condition_ = '1'
                if cond_tion:
                    break
        else:
            condition_ = '0'
        if condition_ == '0':
            token = jwt.token(request)
            jsondata = json.loads(request.body.decode('utf-8'))
            obj_qty = mMasters.Masters()
            obj_qty.action = jsondata.get('Params').get('Action')
            obj_qty.GROUP = jsondata.get('Params').get('Group')
            datas = json.dumps(jsondata)
            validatewithmemo = check_memo_employee_num(jsondata)
            if validatewithmemo == 'SUCCESS':
                headers = {"content-type": "application/json", "Authorization": "" + token + ""}
                resp = requests.post("" + ip + "/update_personal_infonum?Action=" + obj_qty.action + ""+ "&GROUP=" + obj_qty.GROUP+"",
                                     data=datas, headers=headers, verify=False)
                response = resp.content.decode("utf-8")
                return HttpResponse(response)
            else:
                return HttpResponse('{"MESSAGE":"Failed in Microservice."}')
        else:
            return HttpResponse('{"MESSAGE":"You are trying to change Mobile number from outside KVB environment. Kindly access the WISEFIN via KVB environment and update your mobile number."}')
