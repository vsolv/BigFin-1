from __future__ import unicode_literals

import datetime
import sys
import time

import Bigflow.Core.jwt_file as jwt
import boto3
from Bigflow.menuClass import utility as utl
from django.contrib.sites import requests
from django.http import JsonResponse

from django.shortcuts import render, redirect
from django.http import HttpResponse
import json
import Bigflow.Core.models as common
import Bigflow.API.view_eClaim as eClaim
from Bigflow.eClaim import urls
import requests
from Bigflow.Core.models import decrpt as decry_data
from Bigflow.settings import BASE_DIR,S3_BUCKET_NAME
ip = common.localip()
token = common.token()
import pandas as pd


employee_gid = 0
# eClaim Pages
def eClaim_Template(request,template_name):
    template_name = template_name
    if template_name is not '':
         #utl.check_authorization(request)
         return render(request, template_name+".html")


def eclaim_master(request):
    utl.check_authorization(request)
    if request.method == 'POST':
        jsondata = json.loads(request.body.decode('utf-8'))
        act = jsondata.get('params').get('Action')
        grp = jsondata.get('params').get('Group')
        typ = jsondata.get('params').get('Type')
        sub = jsondata.get('params').get('Sub_Type')
        entity = request.session['Emp_gid']
        token = jwt.token(request)
        params = {"Action":act,"Group": grp, "Type":typ, "Sub_Type":sub,"Employee_Gid" :entity}
        headers = {"content-type": "application/json", "Authorization": "" + token + ""}
        classify = {
            "CLASSIFICATION":{
                "Entity_Gid" : decry_data(request.session['Entity_gid'])
            }}
        jsondata['params']['json']['Params'].update(classify)
        datas = json.dumps(jsondata.get('params').get('json'))
        resp = requests.post("" + ip + "/ECLAIM_MASTER", params=params, data=datas, headers=headers,
                             verify=False)
        response = resp.content.decode("utf-8")
        return HttpResponse(response)

# def eclaim_process_set(request):
#     utl.check_authorization(request)
#     if request.method == 'POST':
#         jsondata = json.loads(request.body.decode('utf-8'))
#         typ = jsondata.get('params').get('Type')
#         params = {"Type": typ,
#                   "Api_Type": "WEB"}
#         token = jwt.token(request)
#         headers = {"content-type": "application/json", "Authorization": "" + token + ""}
#         jsondata['params']['json']['Params']['DETAILS']["processedby"] = decry_data(request.session['Emp_gid'])
#         jsondata['params']['json']['Params']['DETAILS']["createby"] = decry_data(request.session['Emp_gid'])
#         jsondata['params']['json']['Params']['DETAILS']["Entity_Gid"] = decry_data(request.session['Entity_gid'])
#         datas = json.dumps(jsondata.get('params').get('json'))
#         resp = requests.post("" + ip + "/ECLAIM_TRAN", params=params, data=datas, headers=headers,
#                              verify=False)
#         response = resp.content.decode("utf-8")
#         return HttpResponse(response)

# def eclaim_summary(request):
#     utl.check_authorization(request)
#     if request.method == 'GET':
#         typ = request.GET['Type']
#         data = json.loads(request.GET['json'])
#         params = {"Type":typ,
#                   "Api_Type":"WEB"}
#         token = jwt.token(request)
#         headers = {"content-type": "application/json", "Authorization": "" + token + ""}
#         data['Params']["FILTER"]["Entity_Gid"] = decry_data(request.session['Entity_gid'])
#         data['Params']["FILTER"]["Employee_gid"] = decry_data(request.session['Emp_gid'])
#         dictionary = data.get('Params').get("FILTER")
#         for key,value in dictionary.items():
#             params[key] = value
#         resp = requests.get("" + ip + "/ECLAIM_SUMMARY", params=params, data={}, headers=headers,
#                              verify=False)
#         response = resp.content.decode("utf-8")
#         return HttpResponse(response)
#     if request.method == 'POST':
#         jsondata = json.loads(request.body.decode('utf-8'))
#         typ = jsondata.get('params').get('Type')
#         params = {"Type": typ,
#                   "Api_Type": "WEB"}
#         token = jwt.token(request)
#         headers = {"content-type": "application/json", "Authorization": "" + token + ""}
#         jsondata['params']['json']['Params']["FILTER"]["Entity_Gid"] = decry_data(request.session['Entity_gid'])
#         jsondata['params']['json']['Params']["FILTER"]["Entity_Gid_d"] = request.session['Entity_gid']
#         jsondata['params']['json']['Params']["FILTER"]["Employee_gid"] = decry_data(request.session['Emp_gid'])
#         datas = json.dumps(jsondata.get('params').get('json'))
#         resp = requests.post("" + ip + "/ECLAIM_SUMMARY", params=params, data=datas, headers=headers,
#                              verify=False)
#         response = resp.content.decode("utf-8")
#         return HttpResponse(response)

def data_alltablevalue(request):
    utl.check_authorization(request)
    if request.method == 'POST':
        jsondata = json.loads(request.body.decode('utf-8'))
        typ = jsondata.get('params').get('Type')
        params = {"Type": typ}
        token = jwt.token(request)
        headers = {"content-type": "application/json", "Authorization": "" + token + ""}
        datas = {}
        resp = requests.post("" + ip + "/ECLAIM_SUMMARY", params=params, data=datas, headers=headers,
                             verify=False)
        response = resp.content.decode("utf-8")
        return HttpResponse(response)

def get_supplier(request):
    if request.method == 'POST':
        try:
            jsondata = json.loads(request.body.decode('utf-8'))
            grp = jsondata.get('Params').get('Group')
            limit = jsondata.get('Params').get('Limit')
            typ = jsondata.get('Params').get('Type')
            sub = jsondata.get('Params').get('Sub_Type')
            Entity_gid = int(decry_data(request.session['Entity_gid']))
            params = {"Group": grp, "Type": typ, "Sub_Type": sub, "Limit": limit}
            token = jwt.token(request)
            headers = {"content-type": "application/json", "Authorization": "" + token + ""}
            classify = {
                "CLASSIFICATION": {
                    "Entity_Gid": Entity_gid
                }}
            jsondata['Params'].update(classify)
            datas = json.dumps(jsondata)
            resp = requests.post("" + ip + "/MASTER_DATA", params=params, data=datas, headers=headers,
                                 verify=False)
            response = resp.content.decode("utf-8")
            return HttpResponse(response)
        except Exception as e:
            return JsonResponse({"MESSAGE": "ERROR_OCCURED", "DATA": str(e)})

def eclaim_withfile_set(request):
    utl.check_authorization(request)
    if request.method == 'POST':
        files = []
        if request.FILES :
            for i in range(0,len(request.FILES)):
                name = "file"+str(i)
                file_data = request.FILES[name].read()
                millis = int(round(time.time() * 1000))
                file_name_new = str(request.session['Emp_gid']) + '_' +str(millis)+'_'+str(i)+str(request.FILES[name].name)
                contents = file_data
                s3 = boto3.resource('s3')
                s3_obj = s3.Object(bucket_name=S3_BUCKET_NAME, key=file_name_new)
                s3_obj.put(Body=contents)
                content = {
                    "File_path" : file_name_new ,
                    "File_name" : str(request.FILES[name].name),
                    "RefGid":request.POST['tourgid'],
                    "Entity_gid": decry_data(request.session['Entity_gid']),
                    "createby": decry_data(request.session['Emp_gid'])
                }

                files.append(content)
        data_ccbs = request.POST['CCBS']
        data_ccbs = json.loads(data_ccbs)
        employee_gid = onbehalf_check(request)
        data = {
            "Params": {
                "DETAILS": {
                     "tourgid":request.POST['tourgid'],
                     "approvedby":request.POST['approvedby'],
                     "appcomment":request.POST['appcomment'],
                     "status": request.POST['status'],
                     "apptype": request.POST['apptype'],
                     "applevel":request.POST['applevel'],
                     "processedby" :employee_gid,
                     "createby":employee_gid,
                     "CCBS" :data_ccbs
                },
                "FILE":{
                    "File": files
                }
            }
        }
        data = onbehalf_data_exp(request, data)
        params = {"Type": request.POST['Type'],"Api_Type": "WEB"}
        token = jwt.token(request)
        headers = {"content-type": "application/json", "Authorization": "" + token + ""}
        datas = json.dumps(data)
        resp = requests.post("" + ip + "/CLAIM_MAKER_SET", params=params, data=datas, headers=headers,
                             verify=False)
        response = resp.content.decode("utf-8")
        return HttpResponse(response)

def alltable(request,table_data,entity):
    drop_tables = {"data": table_data}
    action = 'Debit'
    entity_gid = entity
    params = {'Action': action, 'Entity_Gid': entity_gid}
    token = jwt.token(request)
    headers = {"content-type": "application/json", "Authorization": "" + token + ""}
    datas = json.dumps(drop_tables.get('data'))
    resp = requests.post("" + ip + "/All_Tables_Values_Get", params=params, data=datas, headers=headers,
                         verify=False)
    response_data = resp.content.decode("utf-8")
    return response_data

from io import BytesIO
from django.http import HttpResponse
from django.template.loader import get_template

from xhtml2pdf import pisa
from django.template import Context


def tcf_pdf(request):
    if request.method == 'POST':
        jsondata = json.loads(request.body.decode('utf-8'))
        Templatename = "tcf"
        file_css = open(BASE_DIR + '/Bigflow/eClaim/templates/tablestyle.text', "r")
        file_css = file_css.read()
        print(file_css)
        content = jsondata.get('params').get('html')
        content = file_css + content
        f = open(BASE_DIR + '/Bigflow/eClaim/templates/%s.html' % Templatename, 'w')
        f.write(content)
        f.close()
        data = {
            'MESSAGE': "SUCCESS",
        }
        return JsonResponse(data)


def download_pdf(request):
    data = {
    }
    pdf = render_to_pdf(BASE_DIR + '/Bigflow/eClaim/templates/tcf.html', data)
    return HttpResponse(pdf, content_type="application/pdf")


def render_to_pdf(template_src, context_dict):
    template = get_template(template_src)
    html = template.render(context_dict)
    result = BytesIO()
    pdf = pisa.pisaDocument(BytesIO(html.encode("ISO-8859-1")), result)
    if not pdf.err:
        return HttpResponse(result.getvalue(), content_type='application/pdf')
    return None

def ECF_data_Get(request):
    utl.check_authorization(request)
    if request.method == 'POST':
        jsondata = json.loads(request.body.decode('utf-8'))
        token = jwt.token(request)
        params = {}
        headers = {"content-type": "application/json", "Authorization": "" + token + ""}
        classify = {
            "CLASSIFICATION":{
                "Entity_Gid" : decry_data(request.session['Entity_gid'])
            }}
        jsondata['params'].update(classify)
        jsondata['params']['filter']['create_by'] = decry_data(request.session['Emp_gid'])
        datas = json.dumps(jsondata.get('params'))
        resp = requests.post("" + ip + "/ECFInvoice_Get", params=params, data=datas, headers=headers,
                             verify=False)
        response = json.loads(resp.content.decode("utf-8"))
        pdf = HttpResponse(content_type='application/pdf')
        pdf['Content-Disposition'] = 'attachment; filename="somefilename.pdf"'
        pdf = render_to_pdf(BASE_DIR + '/Bigflow/Templates/Shared/claimform_template.html', response)
        pdf2 = read_xlsx(pdf)
        return pdf2

import xlrd
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch, cm
from PyPDF2 import PdfFileWriter, PdfFileReader
from reportlab.lib.colors import HexColor
# create watermarked booklet
def final_booklets(file_name,booklet):
    watermark_obj = PdfFileReader(file_name)
    watermark_page = watermark_obj.getPage(0)
    pdf_reader = PdfFileReader(booklet)
    pdf_writer = PdfFileWriter()

    # Watermark all the pages
    for page in range(pdf_reader.getNumPages()):
        page = pdf_reader.getPage(page)
        page.mergePage(watermark_page)
        pdf_writer.addPage(page)

    output3 = io.BytesIO()
    pdf_writer.write(output3)
    return output3

# Create watermark pdf again each email address
def watermark_pdf(target,booklet):
    output = io.BytesIO()
    c = canvas.Canvas(output)
    pdf_reader = PdfFileReader(booklet)
    for page in range(pdf_reader.getNumPages()):
        c.saveState()
        # with open(BASE_DIR + '/Bigflow/static/Images/kvb_logo.jpg', 'rb') as f:
        #     image= f.read()
        c.drawImage( BASE_DIR + '/Bigflow/static/Images/kvb_logo1.jpeg',500, 0, 50, 50)
        c.setFillColor(HexColor('#D3D3D3'),0.38)

        c.setFont("Helvetica", 30)
        c.translate(8*cm, 8*cm)
        #c.setFillColorRGB(0.5, 0.5, 0.5)  # gray
        c.rotate(45)
        # c.drawRightString(0,0,target)
        c.drawString(-7 * cm, 0 * cm, target)
        c.drawString(7 * cm, 0 * cm, target)
        c.drawString(0 * cm, 7 * cm, target)
        c.drawString(0 * cm, -7 * cm, target)
        c.setFillAlpha(0.2)
        c.restoreState()
        c.showPage()
    c.save()
    output = final_booklets(output,booklet)
    return output
# Read the sheet to get everyones email address
import io
def read_xlsx(fn):
    file = io.BytesIO(fn.content)
    target = "Karur Vysya bank"
    output = watermark_pdf(target,file)
    return HttpResponse(output.getvalue(), content_type='application/pdf')


def eclaim_summary(request):
    utl.check_authorization(request)
    if request.method == 'POST':
        jsondata = json.loads(request.body.decode('utf-8'))
        typ = jsondata.get('params').get('Type')
        if typ =='CLAIM_REQUEST':
            params = {"Type": typ,
                      "Api_Type": "WEB"}
            token = jwt.token(request)
            headers = {"content-type": "application/json", "Authorization": "" + token + ""}
            jsondata['params']['json']['Params']["FILTER"]["Entity_Gid"] = decry_data(request.session['Entity_gid'])
            jsondata['params']['json']['Params']["FILTER"]["Entity_Gid_d"] = request.session['Entity_gid']
            jsondata['params']['json']['Params']["FILTER"]["Employee_gid"] = decry_data(request.session['Emp_gid'])
            datas = json.dumps(jsondata.get('params').get('json'))
            resp = requests.post("" + ip + "/TOUR_MAKER_SUMMARY", params=params, data=datas, headers=headers,
                                 verify=False)
            response = resp.content.decode("utf-8")
            return HttpResponse(response)
        elif typ == 'GET_APPROVAL':
            params = {"Type": typ,
                      "Api_Type": "WEB"}
            token = jwt.token(request)
            employee_gid = onbehalf_check_smry(request,jsondata)
            headers = {"content-type": "application/json", "Authorization": "" + token + ""}
            jsondata['params']['json']['Params']["FILTER"]["Entity_Gid"] = decry_data(request.session['Entity_gid'])
            jsondata['params']['json']['Params']["FILTER"]["Entity_Gid_d"] = request.session['Entity_gid']
            jsondata['params']['json']['Params']["FILTER"]["Employee_gid"] = employee_gid
            datas = json.dumps(jsondata.get('params').get('json'))
            resp = requests.post("" + ip + "/ECLAIM_APPROVAL_SUMMARY", params=params, data=datas, headers=headers,
                                 verify=False)
            response = resp.content.decode("utf-8")
            return HttpResponse(response)
        elif typ == 'ADVANCE_SUMMARY':
            params = {"Type": typ,
                      "Api_Type": "WEB"}
            token = jwt.token(request)
            headers = {"content-type": "application/json", "Authorization": "" + token + ""}
            jsondata['params']['json']['Params']["FILTER"]["Entity_Gid"] = decry_data(request.session['Entity_gid'])
            jsondata['params']['json']['Params']["FILTER"]["Entity_Gid_d"] = request.session['Entity_gid']
            jsondata['params']['json']['Params']["FILTER"]["Employee_gid"] = decry_data(request.session['Emp_gid'])
            datas = json.dumps(jsondata.get('params').get('json'))
            resp = requests.post("" + ip + "/ADVANCE_MAKER_SUMMARY", params=params, data=datas, headers=headers,
                                 verify=False)
            response = resp.content.decode("utf-8")
            return HttpResponse(response)
        elif typ == 'TOUR_TO_ADVANCE':
            params = {"Type": request.session['type'],
                      "Api_Type": "WEB"}
            token = jwt.token(request)
            headers = {"content-type": "application/json", "Authorization": "" + token + ""}
            jsondata['params']['json']['Params']["FILTER"]["Entity_Gid"] = decry_data(request.session['Entity_gid'])
            jsondata['params']['json']['Params']["FILTER"]["Entity_Gid_d"] = request.session['Entity_gid']
            jsondata['params']['json']['Params']["FILTER"]["Employee_gid"] = decry_data(request.session['Emp_gid'])
            jsondata['params']['json']['Params']["FILTER"]["type"] = request.session['type']
            jsondata = onbehalf_filter_data(request,jsondata)
            datas = json.dumps(jsondata.get('params').get('json'))
            resp = requests.post("" + ip + "/ADVANCE_MAKER_LIST", params=params, data=datas, headers=headers,
                                 verify=False)
            response = resp.content.decode("utf-8")
            return HttpResponse(response)

        elif typ == 'TOUR_TO_CANCEL':
            params = {"Type": request.session['type'],
                      "Api_Type": "WEB"}
            token = jwt.token(request)
            headers = {"content-type": "application/json", "Authorization": "" + token + ""}
            jsondata['params']['json']['Params']["FILTER"]["Entity_Gid"] = decry_data(request.session['Entity_gid'])
            jsondata['params']['json']['Params']["FILTER"]["Entity_Gid_d"] = request.session['Entity_gid']
            jsondata['params']['json']['Params']["FILTER"]["Employee_gid"] = decry_data(request.session['Emp_gid'])
            jsondata['params']['json']['Params']["FILTER"]["type"] = request.session['type']
            jsondata = onbehalf_filter_data(request,jsondata)
            datas = json.dumps(jsondata.get('params').get('json'))
            resp = requests.post("" + ip + "/TOUR_CANCEL_LIST", params=params, data=datas, headers=headers,
                                 verify=False)
            response = resp.content.decode("utf-8")
            return HttpResponse(response)

        elif typ == 'ADVANCE_TO_CANCEL':
            params = {"Type": request.session['type'],
                      "Api_Type": "WEB"}
            token = jwt.token(request)
            headers = {"content-type": "application/json", "Authorization": "" + token + ""}
            jsondata['params']['json']['Params']["FILTER"]["Entity_Gid"] = decry_data(request.session['Entity_gid'])
            jsondata['params']['json']['Params']["FILTER"]["Entity_Gid_d"] = request.session['Entity_gid']
            jsondata['params']['json']['Params']["FILTER"]["Employee_gid"] = decry_data(request.session['Emp_gid'])
            jsondata['params']['json']['Params']["FILTER"]["type"] = request.session['type']
            jsondata = onbehalf_filter_data(request,jsondata)
            datas = json.dumps(jsondata.get('params').get('json'))
            resp = requests.post("" + ip + "/ADVANCE_CANCEL_LIST", params=params, data=datas, headers=headers,
                                 verify=False)
            response = resp.content.decode("utf-8")
            return HttpResponse(response)

        elif typ == 'CLAIM_SUMMARY':
            params = {"Type": typ,
                      "Api_Type": "WEB"}
            token = jwt.token(request)
            headers = {"content-type": "application/json", "Authorization": "" + token + ""}
            jsondata['params']['json']['Params']["FILTER"]["Entity_Gid"] = decry_data(request.session['Entity_gid'])
            jsondata['params']['json']['Params']["FILTER"]["Entity_Gid_d"] = request.session['Entity_gid']
            jsondata['params']['json']['Params']["FILTER"]["Employee_gid"] = decry_data(request.session['Emp_gid'])
            datas = json.dumps(jsondata.get('params').get('json'))
            resp = requests.post("" + ip + "/CLAIM_MAKER_SUMMARY", params=params, data=datas, headers=headers,
                                 verify=False)
            response = resp.content.decode("utf-8")
            return HttpResponse(response)

        elif typ == 'TOUR_CANCEL':
            params = {"Type": typ,
                      "Api_Type": "WEB"}
            token = jwt.token(request)
            headers = {"content-type": "application/json", "Authorization": "" + token + ""}
            jsondata['params']['json']['Params']["FILTER"]["Entity_Gid"] = decry_data(request.session['Entity_gid'])
            jsondata['params']['json']['Params']["FILTER"]["Entity_Gid_d"] = request.session['Entity_gid']
            jsondata['params']['json']['Params']["FILTER"]["Employee_gid"] = decry_data(request.session['Emp_gid'])
            datas = json.dumps(jsondata.get('params').get('json'))
            resp = requests.post("" + ip + "/CANCEL_MAKER_SUMMARY", params=params, data=datas, headers=headers,
                                 verify=False)
            response = resp.content.decode("utf-8")
            return HttpResponse(response)

        elif typ =='TOUR_REPORT_SUMMARY':
            params = {"Type": typ,
                      "Api_Type": "WEB"}
            token = jwt.token(request)
            headers = {"content-type": "application/json", "Authorization": "" + token + ""}
            jsondata['params']['json']['Params']["FILTER"]["Entity_Gid"] = decry_data(request.session['Entity_gid'])
            # jsondata['params']['json']['Params']["FILTER"]["Entity_Gid_d"] = request.session['Entity_gid']
            # jsondata['params']['json']['Params']["FILTER"]["Employee_gid"] = decry_data(request.session['Emp_gid'])
            datas = json.dumps(jsondata.get('params').get('json'))
            resp = requests.post("" + ip + "/TOUR_REPORT_SUMMARY", params=params, data=datas, headers=headers,
                                 verify=False)
            response = resp.content.decode("utf-8")
            return HttpResponse(response)

        elif typ =='TOUR_REPORT_SUMMARY_EMPLOYEE':
            params = {"Type": typ,
                      "Api_Type": "WEB"}
            token = jwt.token(request)
            headers = {"content-type": "application/json", "Authorization": "" + token + ""}
            jsondata['params']['json']['Params']["FILTER"]["Entity_Gid"] = decry_data(request.session['Entity_gid'])
            # jsondata['params']['json']['Params']["FILTER"]["Entity_Gid_d"] = request.session['Entity_gid']
            jsondata['params']['json']['Params']["FILTER"]["Employee_gid"] = decry_data(request.session['Emp_gid'])
            datas = json.dumps(jsondata.get('params').get('json'))
            resp = requests.post("" + ip + "/TOUR_REPORT_SUMMARY", params=params, data=datas, headers=headers,
                                 verify=False)
            response = resp.content.decode("utf-8")
            return HttpResponse(response)

def eclaim_dropdata(request):
    utl.check_authorization(request)
    if request.method == 'GET':
        typ = request.GET['Type']
        data = json.loads(request.GET['json'])
        if typ =='TOUR_REASON':
            params = {"Type": typ,
                      "Api_Type": "WEB"}
            token = jwt.token(request)
            headers = {"content-type": "application/json", "Authorization": "" + token + ""}
            data['Params']["FILTER"]["Entity_Gid"] = decry_data(request.session['Entity_gid'])
            data['Params']["FILTER"]["Employee_gid"] = decry_data(request.session['Emp_gid'])
            dictionary = data.get('Params').get("FILTER")
            for key,value in dictionary.items():
                params[key] = value
            resp = requests.get("" + ip + "/TOUR_REASON_LIST", params=params, data={}, headers=headers,
                                 verify=False)
            response = resp.content.decode("utf-8")
            return HttpResponse(response)

        elif typ =='APPROVAL_FLOW':
            params = {"Type": typ,
                      "Api_Type": "WEB"}
            token = jwt.token(request)
            headers = {"content-type": "application/json", "Authorization": "" + token + ""}
            data['Params']["FILTER"]["Entity_Gid"] = decry_data(request.session['Entity_gid'])
            data['Params']["FILTER"]["Employee_gid"] = decry_data(request.session['Emp_gid'])
            dictionary = data.get('Params').get("FILTER")
            for key,value in dictionary.items():
                params[key] = value
            resp = requests.get("" + ip + "/APPROVAL_FLOW", params=params, data={}, headers=headers,
                                 verify=False)
            response = resp.content.decode("utf-8")
            return HttpResponse(response)

        elif typ == 'APPROVER_LIST':
            params = {"Type": request.session['type'],
                "Api_Type": "WEB"}
            token = jwt.token(request)
            employee_gid = onbehalf_check(request)
            headers = {"content-type": "application/json", "Authorization": "" + token + ""}
            data['Params']["FILTER"]["Entity_Gid"] = decry_data(request.session['Entity_gid'])
            data['Params']["FILTER"]["Employee_gid"] = employee_gid
            dictionary = data.get('Params').get("FILTER")
            for key,value in dictionary.items():
                params[key] = value
            resp = requests.get("" + ip + "/APPROVER_LIST_GET", params=params, data={}, headers=headers,
                                 verify=False)
            response = resp.content.decode("utf-8")
            return HttpResponse(response)

        elif typ =='EMP_BRANCH':
            params = {"Type": typ,
                      "Api_Type": "WEB"}
            token = jwt.token(request)
            headers = {"content-type": "application/json", "Authorization": "" + token + ""}
            data['Params']["FILTER"]["Entity_Gid"] = decry_data(request.session['Entity_gid'])
            data['Params']["FILTER"]["Employee_gid"] = decry_data(request.session['Emp_gid'])
            dictionary = data.get('Params').get("FILTER")
            for key,value in dictionary.items():
                params[key] = value
            resp = requests.get("" + ip + "/EMPLOYEE_LIST", params=params, data={}, headers=headers,
                                 verify=False)
            response = resp.content.decode("utf-8")
            return HttpResponse(response)

        elif typ =='EMP_BRANCH_WITH_EMP':
            params = {"Type": typ,
                      "Api_Type": "WEB"}
            token = jwt.token(request)
            headers = {"content-type": "application/json", "Authorization": "" + token + ""}
            data['Params']["FILTER"]["Entity_Gid"] = decry_data(request.session['Entity_gid'])
            dictionary = data.get('Params').get("FILTER")
            for key,value in dictionary.items():
                params[key] = value
            resp = requests.get("" + ip + "/EMPLOYEE_LIST", params=params, data={}, headers=headers,
                                 verify=False)
            response = resp.content.decode("utf-8")
            return HttpResponse(response)

        elif typ =='EMPLOYEE_DATA':
            params = {"Type": request.session['type'],
                      "Api_Type": "WEB"}
            token = jwt.token(request)
            employee_gid = onbehalf_check(request)
            headers = {"content-type": "application/json", "Authorization": "" + token + ""}
            data['Params']["FILTER"]["Entity_Gid"] = decry_data(request.session['Entity_gid'])
            data['Params']["FILTER"]["Employee_gid"] = employee_gid
            dictionary = data.get('Params').get("FILTER")
            for key,value in dictionary.items():
                params[key] = value
            resp = requests.get("" + ip + "/EMPLOYEE_DATA_GET", params=params, data={}, headers=headers,
                                 verify=False)
            response = resp.content.decode("utf-8")
            return HttpResponse(response)

        elif typ =='GET_BRANCH':
            params = {"Api_Type": "WEB"}
            token = jwt.token(request)
            headers = {"content-type": "application/json", "Authorization": "" + token + ""}
            data['Params']["FILTER"]["Entity_Gid"] = decry_data(request.session['Entity_gid'])
            data['Params']["FILTER"]["Employee_gid"] = decry_data(request.session['Emp_gid'])
            dictionary = data.get('Params').get("FILTER")
            for key,value in dictionary.items():
                params[key] = value
            resp = requests.get("" + ip + "/BRANCH_LIST", params=params, data={}, headers=headers,
                                 verify=False)
            response = resp.content.decode("utf-8")
            return HttpResponse(response)

        elif typ =='ELIGIBLE':
            params = {"Type": typ,
                      "Api_Type": "WEB"}
            token = jwt.token(request)
            headers = {"content-type": "application/json", "Authorization": "" + token + ""}
            data['Params']["FILTER"]["Entity_Gid"] = decry_data(request.session['Entity_gid'])
            data['Params']["FILTER"]["Employee_gid"] = decry_data(request.session['Emp_gid'])
            dictionary = data.get('Params').get("FILTER")
            for key,value in dictionary.items():
                params[key] = value
            resp = requests.get("" + ip + "/ELIGIBLE_TRAVEL_TYPE", params=params, data={}, headers=headers,
                                 verify=False)
            response = resp.content.decode("utf-8")
            return HttpResponse(response)

        elif typ =='TOUR_DETAILS':
            params = {"Type": typ,
                      "Api_Type": "WEB"}
            token = jwt.token(request)
            headers = {"content-type": "application/json", "Authorization": "" + token + ""}
            data['Params']["FILTER"]["Entity_Gid"] = decry_data(request.session['Entity_gid'])
            data['Params']["FILTER"]["Employee_gid"] = decry_data(request.session['Emp_gid'])
            dictionary = data.get('Params').get("FILTER")
            for key,value in dictionary.items():
                params[key] = value
            resp = requests.get("" + ip + "/TOUR_DETAILS_GET", params=params, data={}, headers=headers,
                                 verify=False)
            response = resp.content.decode("utf-8")
            return HttpResponse(response)

        elif typ =='TOUR_ADVANCE_GET':
            params = {"Type": typ,
                      "Api_Type": "WEB"}
            token = jwt.token(request)
            headers = {"content-type": "application/json", "Authorization": "" + token + ""}
            data['Params']["FILTER"]["Entity_Gid"] = decry_data(request.session['Entity_gid'])
            data['Params']["FILTER"]["Employee_gid"] = decry_data(request.session['Emp_gid'])
            dictionary = data.get('Params').get("FILTER")
            for key,value in dictionary.items():
                params[key] = value
            resp = requests.get("" + ip + "/TOUR_ADVANCE_GET", params=params, data={}, headers=headers,
                                 verify=False)
            response = resp.content.decode("utf-8")
            return HttpResponse(response)

        elif typ =='CLAIM_EXPENSE':
            params = {"Type": typ,
                      "Api_Type": "WEB"}
            token = jwt.token(request)
            headers = {"content-type": "application/json", "Authorization": "" + token + ""}
            data['Params']["FILTER"]["Entity_Gid"] = decry_data(request.session['Entity_gid'])
            data['Params']["FILTER"]["Employee_gid"] = decry_data(request.session['Emp_gid'])
            dictionary = data.get('Params').get("FILTER")
            for key,value in dictionary.items():
                params[key] = value
            resp = requests.get("" + ip + "/EXPENSE_LIST", params=params, data={}, headers=headers,
                                 verify=False)
            response = resp.content.decode("utf-8")
            return HttpResponse(response)

        elif typ =='CLAIMED_EXPENSE':
            params = {"Type": typ,
                      "Api_Type": "WEB"}
            token = jwt.token(request)
            headers = {"content-type": "application/json", "Authorization": "" + token + ""}
            data['Params']["FILTER"]["Entity_Gid"] = decry_data(request.session['Entity_gid'])
            data['Params']["FILTER"]["Employee_gid"] = decry_data(request.session['Emp_gid'])
            dictionary = data.get('Params').get("FILTER")
            for key,value in dictionary.items():
                params[key] = value
            resp = requests.get("" + ip + "/EXPENSE_SUMMARY_GET", params=params, data={}, headers=headers,
                                 verify=False)
            response = resp.content.decode("utf-8")
            return HttpResponse(response)

        elif typ =='BS':
            entity = request.session['Entity_gid']
            drop_b = {
                "Table_name": "ap_mst_tbs",
                "Column_1": "tbs_gid as bs_gid,tbs_code as bs_code,tbs_no as bs_no,tbs_name as bs_name",
                "Column_2": "",
                "Where_Common": "tbs",
                "Where_Primary": "",
                "Primary_Value": "",
                "Order_by": "no"
            }
            response = alltable(request, drop_b, entity)
            return HttpResponse(response)

        elif typ =='CC':
            bs_gid = data.get('Bs_gid')
            entity = request.session['Entity_gid']
            drop_b = {
                "Table_name": "ap_mst_tcc",
                "Column_1": "tcc_gid as cc_gid,tcc_code as cc_code,tcc_no as cc_no,tcc_name as cc_name",
                "Column_2": "",
                "Where_Common": "tcc",
                "Where_Primary": "bsgid",
                "Primary_Value": bs_gid,
                "Order_by": "no"
            }
            response = alltable(request, drop_b, entity)
            return HttpResponse(response)

        elif typ =='HIERARCHY':
            bs_gid = data.get('Bs_gid')
            entity = request.session['Entity_gid']
            drop_b = {
                "Table_name": "gal_mst_thierarchy",
                "Column_1": "hierarchy_gid, hierarchy_layer, hierarchy_order",
                "Column_2": "",
                "Where_Common": "hierarchy",
                "Where_Primary": "",
                "Primary_Value": "",
                "Order_by": "gid"
            }
            response = alltable(request, drop_b, entity)
            return HttpResponse(response)

        elif typ =='GET_CITY':
            params = {"Type": typ,
                      "Api_Type": "WEB"}
            token = jwt.token(request)
            headers = {"content-type": "application/json", "Authorization": "" + token + ""}
            data['Params']["FILTER"]["Entity_Gid"] = decry_data(request.session['Entity_gid'])
            data['Params']["FILTER"]["Employee_gid"] = decry_data(request.session['Emp_gid'])
            dictionary = data.get('Params').get("FILTER")
            for key,value in dictionary.items():
                params[key] = value
            resp = requests.get("" + ip + "/EXPENSE_CITY_LIST", params=params, data={}, headers=headers,
                                 verify=False)
            response = resp.content.decode("utf-8")
            return HttpResponse(response)

        elif typ =='GST_GET':
            params = {"Type": typ,
                      "Api_Type": "WEB"}
            token = jwt.token(request)
            headers = {"content-type": "application/json", "Authorization": "" + token + ""}
            data['Params']["FILTER"]["Entity_Gid"] = decry_data(request.session['Entity_gid'])
            data['Params']["FILTER"]["Employee_gid"] = decry_data(request.session['Emp_gid'])
            dictionary = data.get('Params').get("FILTER")
            for key,value in dictionary.items():
                params[key] = value
            resp = requests.get("" + ip + "/GST_LIST_GET", params=params, data={}, headers=headers,
                                 verify=False)
            response = resp.content.decode("utf-8")
            return HttpResponse(response)

        elif typ =='ELIGIBLE_PKG':
            params = {"Type": typ,
                      "Api_Type": "WEB"}
            token = jwt.token(request)
            headers = {"content-type": "application/json", "Authorization": "" + token + ""}
            data['Params']["FILTER"]["Entity_Gid"] = decry_data(request.session['Entity_gid'])
            data['Params']["FILTER"]["Employee_gid"] = decry_data(request.session['Emp_gid'])
            dictionary = data.get('Params').get("FILTER")
            for key,value in dictionary.items():
                params[key] = value
            resp = requests.get("" + ip + "/PKG_ELIGIBLE_GET", params=params, data={}, headers=headers,
                                 verify=False)
            response = resp.content.decode("utf-8")
            return HttpResponse(response)

        elif typ =='EMP_DEPENDENT':
            params = {"Type": typ,
                      "Api_Type": "WEB"}
            token = jwt.token(request)
            headers = {"content-type": "application/json", "Authorization": "" + token + ""}
            data['Params']["FILTER"]["Entity_Gid"] = decry_data(request.session['Entity_gid'])
            data['Params']["FILTER"]["Employee_gid"] = decry_data(request.session['Emp_gid'])
            dictionary = data.get('Params').get("FILTER")
            for key,value in dictionary.items():
                params[key] = value
            resp = requests.get("" + ip + "/EMP_DEPENDENT_LIST", params=params, data={}, headers=headers,
                                 verify=False)
            response = resp.content.decode("utf-8")
            return HttpResponse(response)

        elif typ =='ELIGIBLE_TRAVEL':
            params = {"Type": typ,
                      "Api_Type": "WEB"}
            token = jwt.token(request)
            headers = {"content-type": "application/json", "Authorization": "" + token + ""}
            data['Params']["FILTER"]["Entity_Gid"] = decry_data(request.session['Entity_gid'])
            data['Params']["FILTER"]["Employee_gid"] = decry_data(request.session['Emp_gid'])
            dictionary = data.get('Params').get("FILTER")
            for key,value in dictionary.items():
                params[key] = value
            resp = requests.get("" + ip + "/TRAVEL_ELIGIBLE_GET", params=params, data={}, headers=headers,
                                 verify=False)
            response = resp.content.decode("utf-8")
            return HttpResponse(response)

        elif typ =='PAYMENT_STATUS':
            params = {"Type": typ,
                      "Api_Type": "WEB"}
            token = jwt.token(request)
            headers = {"content-type": "application/json", "Authorization": "" + token + ""}
            data['Params']["FILTER"]["Entity_Gid"] = decry_data(request.session['Entity_gid'])
            data['Params']["FILTER"]["Employee_gid"] = decry_data(request.session['Emp_gid'])
            dictionary = data.get('Params').get("FILTER")
            for key,value in dictionary.items():
                params[key] = value
            resp = requests.get("" + ip + "/INVOICE_PAYMENT_STATUS", params=params, data={}, headers=headers,
                                 verify=False)
            response = resp.content.decode("utf-8")
            return HttpResponse(response)

        elif typ =='GET_ONBEHALF':
            params = {"Type": typ,
                      "Api_Type": "WEB"}
            token = jwt.token(request)
            headers = {"content-type": "application/json", "Authorization": "" + token + ""}
            data['Params']["FILTER"]["Entity_Gid"] = decry_data(request.session['Entity_gid'])
            data['Params']["FILTER"]["Employee_gid"] = decry_data(request.session['Emp_gid'])
            dictionary = data.get('Params').get("FILTER")
            for key,value in dictionary.items():
                params[key] = value
            resp = requests.get("" + ip + "/ONBEHALF_GET", params=params, data={}, headers=headers,
                                 verify=False)
            response = resp.content.decode("utf-8")
            return HttpResponse(response)

        elif typ =='TOUR_APPROVER':
            params = {"Type": typ,
                      "Api_Type": "WEB"}
            token = jwt.token(request)
            headers = {"content-type": "application/json", "Authorization": "" + token + ""}
            data['Params']["FILTER"]["Entity_Gid"] = decry_data(request.session['Entity_gid'])
            data['Params']["FILTER"]["Employee_gid"] = decry_data(request.session['Emp_gid'])
            dictionary = data.get('Params').get("FILTER")
            for key,value in dictionary.items():
                params[key] = value
            resp = requests.get("" + ip + "/TOUR_APPROVER_GET", params=params, data={}, headers=headers,
                                 verify=False)
            response = resp.content.decode("utf-8")
            return HttpResponse(response)

        elif typ =='GET_ONBEHALF_DROPDOWN':
            params = {"Type": typ,
                      "Api_Type": "WEB"}
            token = jwt.token(request)
            headers = {"content-type": "application/json", "Authorization": "" + token + ""}
            data['Params']["FILTER"]["Entity_Gid"] = decry_data(request.session['Entity_gid'])
            data['Params']["FILTER"]["Employee_gid"] = decry_data(request.session['Emp_gid'])
            dictionary = data.get('Params').get("FILTER")
            for key,value in dictionary.items():
                params[key] = value
            resp = requests.get("" + ip + "/ONBEHALF_DROPDOWN_GET", params=params, data={}, headers=headers,
                                 verify=False)
            response = resp.content.decode("utf-8")
            return HttpResponse(response)

        elif typ =='EMPLOYEE_ONBEHALF':
            params = {"Type": typ,
                      "Api_Type": "WEB"}
            token = jwt.token(request)
            headers = {"content-type": "application/json", "Authorization": "" + token + ""}
            data['Params']["FILTER"]["Entity_Gid"] = decry_data(request.session['Entity_gid'])
            data['Params']["FILTER"]["Employee_gid"] = decry_data(request.session['Emp_gid'])
            dictionary = data.get('Params').get("FILTER")
            for key, value in dictionary.items():
                params[key] = value
            resp = requests.get("" + ip + "/EMPLOYEE_ONBEHALF", params=params, data=data, headers=headers,
                                 verify=False)
            response = resp.content.decode("utf-8")
            return HttpResponse(response)

        elif typ =='CCBS_GET':
            params = {"Type": typ,
                      "Api_Type": "WEB"}
            token = jwt.token(request)
            headers = {"content-type": "application/json", "Authorization": "" + token + ""}
            data['Params']["FILTER"]["Entity_Gid"] = decry_data(request.session['Entity_gid'])
            data['Params']["FILTER"]["Employee_gid"] = decry_data(request.session['Emp_gid'])
            dictionary = data.get('Params').get("FILTER")
            for key, value in dictionary.items():
                params[key] = value
            resp = requests.get("" + ip + "/CCBS_GET", params=params, data=data, headers=headers,
                                 verify=False)
            response = resp.content.decode("utf-8")
            return HttpResponse(response)

        elif typ == 'RECOVERY':
            params = {"Type": typ,
                      "Employee_gid" :decry_data(request.session['Emp_gid']),
                      "Api_Type": "WEB"}
            token = jwt.token(request)
            headers = {"content-type": "application/json", "Authorization": "" + token + ""}
            data['Params']["FILTER"]["Entity_Gid"] = decry_data(request.session['Entity_gid'])
            data['Params']["FILTER"]["Employee_gid"] = decry_data(request.session['Emp_gid'])
            dictionary = data.get('Params').get("FILTER")
            for key, value in dictionary.items():
                params[key] = value
            resp = requests.get("" + ip + "/RECOVERY_GET", params=params, data=data, headers=headers,
                                 verify=False)
            response = resp.content.decode("utf-8")
            return HttpResponse(response)

        elif typ == 'AP_ADVANCE':
            params = {"Type": typ,
                      "Api_Type": "WEB"}
            token = jwt.token(request)
            headers = {"content-type": "application/json", "Authorization": "" + token + ""}
            data['Params']["FILTER"]["Entity_Gid"] = decry_data(request.session['Entity_gid'])
            data['Params']["FILTER"]["Employee_gid"] = decry_data(request.session['Emp_gid'])
            dictionary = data.get('Params').get("FILTER")
            for key, value in dictionary.items():
                params[key] = value
            resp = requests.get("" + ip + "/AP_ADVANCE_GET", params=params, data=data, headers=headers,
                                 verify=False)
            response = resp.content.decode("utf-8")
            return HttpResponse(response)
        elif typ == 'BRANCHWISE_PENDING':
            params = {"Type": typ,
                      "Api_Type": "WEB"}
            token = jwt.token(request)
            headers = {"content-type": "application/json", "Authorization": "" + token + ""}
            data['Params']["FILTER"]["Entity_Gid"] = decry_data(request.session['Entity_gid'])
            data['Params']["FILTER"]["Employee_gid"] = decry_data(request.session['Emp_gid'])
            dictionary = data.get('Params').get("FILTER")
            for key, value in dictionary.items():
                params[key] = value
            resp = requests.get("" + ip + "/BRANCH_PENDING_COUNT", params=params, data=data, headers=headers,
                                 verify=False)
            response = resp.content.decode("utf-8")
            return HttpResponse(response)

def tour_set_file(request):
    utl.check_authorization(request)
    if request.method == 'POST':
        files = []
        if request.FILES:
            for i in range(0, len(request.FILES)):
                name = "file" + str(i)
                file_data = request.FILES[name].read()
                millis = int(round(time.time() * 1000))
                file_name_new = str(request.session['Emp_gid']) + '_' +str(millis) + '_' + str(i) + str(request.FILES[name].name)
                contents = file_data
                s3 = boto3.resource('s3')
                s3_obj = s3.Object(bucket_name=S3_BUCKET_NAME, key=file_name_new)
                s3_obj.put(Body=contents)
                content = {
                    "File_path": file_name_new,
                    "File_name": str(request.FILES[name].name),
                    "RefGid": request.POST['tourgid'],
                    "Entity_gid": decry_data(request.session['Entity_gid']),
                    "createby": decry_data(request.session['Emp_gid'])
                }

                files.append(content)
        jsondata = json.loads(request.POST['Tour'])
        type = jsondata.get('params').get('Type')
        if type =='TOUR_MAKER':
            params = {"Type": type,
                      "Api_Type": "WEB"}
            token = jwt.token(request)
            employee_gid = onbehalf_check(request)
            jsondata = onbehalf_data(request,jsondata)
            headers = {"content-type": "application/json", "Authorization": "" + token + ""}
            jsondata['params']['json']['Params']['DETAILS']["processedby"] = employee_gid
            jsondata['params']['json']['Params']['DETAILS']["createby"] = employee_gid
            jsondata['params']['json']['Params']['DETAILS']["Entity_Gid"] = decry_data(request.session['Entity_gid'])
            classify = {
                "FILE": {
                    "File": files
                }}
            jsondata['params']['json']['Params'].update(classify)
            datas = json.dumps(jsondata.get('params').get('json'))
            resp = requests.post("" + ip + "/TOUR_MAKER_SET", params=params, data=datas, headers=headers,
                                 verify=False)
            response = resp.content.decode("utf-8")
            return HttpResponse(response)

def eclaim_process_set(request):
    # utl.check_authorization(request)
    if request.method == 'POST':
        jsondata = json.loads(request.body.decode('utf-8'))
        type = jsondata.get('params').get('Type')
        if type =='MOVE_REJECT':
            params = {"Type": type,
                      "Api_Type": "WEB"}
            token = jwt.token(request)
            headers = {"content-type": "application/json", "Authorization": "" + token + ""}
            jsondata['params']['json']['Params']['DETAILS']["processedby"] = decry_data(request.session['Emp_gid'])
            jsondata['params']['json']['Params']['DETAILS']["createby"] = decry_data(request.session['Emp_gid'])
            jsondata['params']['json']['Params']['DETAILS']["Entity_Gid"] = decry_data(request.session['Entity_gid'])
            #jsondata = onbehalf_data_aprvl(request, jsondata)
            datas = json.dumps(jsondata.get('params').get('json'))
            resp = requests.post("" + ip + "/ECLAIM_REJECT_SET", params=params, data=datas, headers=headers,
                                 verify=False)
            response = resp.content.decode("utf-8")
            return HttpResponse(response)

        elif type =='MOVE_APPROVE_II':
            params = {"Type": type,
                      "Api_Type": "WEB"}
            token = jwt.token(request)
            headers = {"content-type": "application/json", "Authorization": "" + token + ""}
            jsondata['params']['json']['Params']['DETAILS']["processedby"] = decry_data(request.session['Emp_gid'])
            jsondata['params']['json']['Params']['DETAILS']["createby"] = decry_data(request.session['Emp_gid'])
            jsondata['params']['json']['Params']['DETAILS']["Entity_Gid"] = decry_data(request.session['Entity_gid'])
            #jsondata = onbehalf_data_aprvl(request, jsondata)
            datas = json.dumps(jsondata.get('params').get('json'))
            resp = requests.post("" + ip + "/ECLAIM_APPROVE_SET", params=params, data=datas, headers=headers,
                                 verify=False)
            response = resp.content.decode("utf-8")
            return HttpResponse(response)

        elif type =='ECLAIM_RETURN':
            params = {"Type": type,
                      "Api_Type": "WEB"}
            token = jwt.token(request)
            headers = {"content-type": "application/json", "Authorization": "" + token + ""}
            jsondata['params']['json']['Params']['DETAILS']["processedby"] = decry_data(request.session['Emp_gid'])
            jsondata['params']['json']['Params']['DETAILS']["createby"] = decry_data(request.session['Emp_gid'])
            jsondata['params']['json']['Params']['DETAILS']["Entity_Gid"] = decry_data(request.session['Entity_gid'])
            #jsondata = onbehalf_data_aprvl(request, jsondata)
            datas = json.dumps(jsondata.get('params').get('json'))
            resp = requests.post("" + ip + "/ECLAIM_RETURN_SET", params=params, data=datas, headers=headers,
                                 verify=False)
            response = resp.content.decode("utf-8")
            return HttpResponse(response)

        elif type =='TOUR_FORWARD':
            params = {"Type": type,
                      "Api_Type": "WEB"}
            token = jwt.token(request)
            headers = {"content-type": "application/json", "Authorization": "" + token + ""}
            jsondata['params']['json']['Params']['DETAILS']["processedby"] = decry_data(request.session['Emp_gid'])
            jsondata['params']['json']['Params']['DETAILS']["createby"] = decry_data(request.session['Emp_gid'])
            jsondata['params']['json']['Params']['DETAILS']["Entity_Gid"] = decry_data(request.session['Entity_gid'])
            datas = json.dumps(jsondata.get('params').get('json'))
            resp = requests.post("" + ip + "/TOUR_FORWARD_SET", params=params, data=datas, headers=headers,
                                 verify=False)
            response = resp.content.decode("utf-8")
            return HttpResponse(response)

        elif type =='TOUR_ADVANCE':
            params = {"Type": type,
                      "Api_Type": "WEB"}
            token = jwt.token(request)
            employee_gid = onbehalf_check(request)
            headers = {"content-type": "application/json", "Authorization": "" + token + ""}
            jsondata['params']['json']['Params']['DETAILS']["processedby"] = employee_gid
            jsondata['params']['json']['Params']['DETAILS']["createby"] = employee_gid
            jsondata['params']['json']['Params']['DETAILS']["Entity_Gid"] = decry_data(request.session['Entity_gid'])
            jsondata = onbehalf_data(request, jsondata)
            datas = json.dumps(jsondata.get('params').get('json'))
            resp = requests.post("" + ip + "/TOUR_ADVANCE_SET", params=params, data=datas, headers=headers,
                                 verify=False)
            response = resp.content.decode("utf-8")
            return HttpResponse(response)

        elif type =='ONBEHALF_SET':
            params = {"Type": type,
                      "Api_Type": "WEB"}
            token = jwt.token(request)
            headers = {"content-type": "application/json", "Authorization": "" + token + ""}
            jsondata['params']['json']['Params']['DETAILS']["processedby"] = decry_data(request.session['Emp_gid'])
            jsondata['params']['json']['Params']['DETAILS']["createby"] = decry_data(request.session['Emp_gid'])
            jsondata['params']['json']['Params']['DETAILS']["Entity_Gid"] = decry_data(request.session['Entity_gid'])
            datas = json.dumps(jsondata.get('params').get('json'))
            resp = requests.post("" + ip + "/ONBEHALF_SET", params=params, data=datas, headers=headers,
                                 verify=False)
            response = resp.content.decode("utf-8")
            return HttpResponse(response)

        elif type =='APPROVER_SET':
            params = {"Type": type,
                      "Api_Type": "WEB"}
            token = jwt.token(request)
            headers = {"content-type": "application/json", "Authorization": "" + token + ""}
            jsondata['params']['json']['Params']['DETAILS']["processedby"] = decry_data(request.session['Emp_gid'])
            jsondata['params']['json']['Params']['DETAILS']["createby"] = decry_data(request.session['Emp_gid'])
            jsondata['params']['json']['Params']['DETAILS']["Entity_Gid"] = decry_data(request.session['Entity_gid'])
            datas = json.dumps(jsondata.get('params').get('json'))
            resp = requests.post("" + ip + "/APPROVER_SET", params=params, data=datas, headers=headers,
                                 verify=False)
            response = resp.content.decode("utf-8")
            return HttpResponse(response)

        elif type =='EXPENSE_DELETE':
            params = {"Type": type,
                      "Api_Type": "WEB"}
            token = jwt.token(request)
            headers = {"content-type": "application/json", "Authorization": "" + token + ""}
            jsondata['params']['json']['Params']['FILTER']["processedby"] = decry_data(request.session['Emp_gid'])
            jsondata['params']['json']['Params']['FILTER']["createby"] = decry_data(request.session['Emp_gid'])
            jsondata['params']['json']['Params']['FILTER']["Entity_Gid"] = decry_data(request.session['Entity_gid'])
            datas = json.dumps(jsondata.get('params').get('json'))
            resp = requests.post("" + ip + "/EXPENSE_DELETE", params=params, data=datas, headers=headers,
                                 verify=False)
            response = resp.content.decode("utf-8")
            return HttpResponse(response)

        elif type =='TOUR_CANCEL':
            params = {"Type": type,
                      "Api_Type": "WEB"}
            token = jwt.token(request)
            headers = {"content-type": "application/json", "Authorization": "" + token + ""}
            jsondata['params']['json']['Params']['DETAILS']["processedby"] = decry_data(request.session['Emp_gid'])
            jsondata['params']['json']['Params']['DETAILS']["createby"] = decry_data(request.session['Emp_gid'])
            jsondata['params']['json']['Params']['DETAILS']["Entity_Gid"] = decry_data(request.session['Entity_gid'])
            datas = json.dumps(jsondata.get('params').get('json'))
            resp = requests.post("" + ip + "/TOUR_CANCEL_SET", params=params, data=datas, headers=headers,
                                 verify=False)
            response = resp.content.decode("utf-8")
            return HttpResponse(response)

        elif type =='ADVANCE_ADJUST':
            params = {"Type": type,
                      "Api_Type": "WEB"}
            token = jwt.token(request)
            headers = {"content-type": "application/json", "Authorization": "" + token + ""}
            jsondata['params']['json']['Params']['DETAILS']["processedby"] = decry_data(request.session['Emp_gid'])
            jsondata['params']['json']['Params']['DETAILS']["createby"] = decry_data(request.session['Emp_gid'])
            jsondata['params']['json']['Params']['DETAILS']["Entity_Gid"] = decry_data(request.session['Entity_gid'])
            datas = json.dumps(jsondata.get('params').get('json'))
            resp = requests.post("" + ip + "/ADVANCE_ADJUST", params=params, data=datas, headers=headers,
                                 verify=False)
            response = resp.content.decode("utf-8")
            return HttpResponse(response)

        elif type =='ADVANCE_RECOVERY':
            params = {"Type": type,
                      "Api_Type": "WEB"}
            token = jwt.token(request)
            headers = {"content-type": "application/json", "Authorization": "" + token + ""}
            jsondata['params']['json']['Params']['DETAILS']["processedby"] = decry_data(request.session['Emp_gid'])
            jsondata['params']['json']['Params']['DETAILS']["createby"] = decry_data(request.session['Emp_gid'])
            jsondata['params']['json']['Params']['DETAILS']["Entity_Gid"] = decry_data(request.session['Entity_gid'])
            datas = json.dumps(jsondata.get('params').get('json'))
            resp = requests.post("" + ip + "/ADVANCE_RECOVERY", params=params, data=datas, headers=headers,
                                 verify=False)
            response = resp.content.decode("utf-8")
            return HttpResponse(response)

        elif type =='CCBS_SET':
            params = {"Type": type,
                      "Api_Type": "WEB"}
            token = jwt.token(request)
            headers = {"content-type": "application/json", "Authorization": "" + token + ""}
            datas = json.dumps(jsondata.get('params').get('json'))
            resp = requests.post("" + ip + "/CCBS_SET", params=params, data=datas, headers=headers,
                                 verify=False)
            response = resp.content.decode("utf-8")
            return HttpResponse(response)

def expense_detail(request):
    utl.check_authorization(request)
    if request.method == 'GET':
        typ = request.GET['Type']
        data = json.loads(request.GET['json'])
        if typ =='DLYDM':
            params = {"Type": typ,
                      "Api_Type": "WEB"}
            token = jwt.token(request)
            headers = {"content-type": "application/json", "Authorization": "" + token + ""}
            data['Params']["FILTER"]["Entity_Gid"] = decry_data(request.session['Entity_gid'])
            data['Params']["FILTER"]["Employee_gid"] = decry_data(request.session['Emp_gid'])
            dictionary = data.get('Params').get("FILTER")
            for key,value in dictionary.items():
                params[key] = value
            resp = requests.get("" + ip + "/DAILYDIEM_EXP_DETAIL_GET", params=params, data={}, headers=headers,
                                 verify=False)
            response = resp.content.decode("utf-8")
            return HttpResponse(response)

        elif typ =='TRVL':
            params = {"Type": typ,
                      "Api_Type": "WEB"}
            token = jwt.token(request)
            headers = {"content-type": "application/json", "Authorization": "" + token + ""}
            data['Params']["FILTER"]["Entity_Gid"] = decry_data(request.session['Entity_gid'])
            data['Params']["FILTER"]["Employee_gid"] = decry_data(request.session['Emp_gid'])
            dictionary = data.get('Params').get("FILTER")
            for key,value in dictionary.items():
                params[key] = value
            resp = requests.get("" + ip + "/TRAVEL_EXP_DETAIL_GET", params=params, data={}, headers=headers,
                                 verify=False)
            response = resp.content.decode("utf-8")
            return HttpResponse(response)

        elif typ =='INCDL':
            params = {"Type": typ,
                      "Api_Type": "WEB"}
            token = jwt.token(request)
            headers = {"content-type": "application/json", "Authorization": "" + token + ""}
            data['Params']["FILTER"]["Entity_Gid"] = decry_data(request.session['Entity_gid'])
            data['Params']["FILTER"]["Employee_gid"] = decry_data(request.session['Emp_gid'])
            dictionary = data.get('Params').get("FILTER")
            for key,value in dictionary.items():
                params[key] = value
            resp = requests.get("" + ip + "/INCIDENTAL_EXP_DETAIL_GET", params=params, data={}, headers=headers,
                                 verify=False)
            response = resp.content.decode("utf-8")
            return HttpResponse(response)

        elif typ =='LCONV':
            params = {"Type": typ,
                      "Api_Type": "WEB"}
            token = jwt.token(request)
            headers = {"content-type": "application/json", "Authorization": "" + token + ""}
            data['Params']["FILTER"]["Entity_Gid"] = decry_data(request.session['Entity_gid'])
            data['Params']["FILTER"]["Employee_gid"] = decry_data(request.session['Emp_gid'])
            dictionary = data.get('Params').get("FILTER")
            for key,value in dictionary.items():
                params[key] = value
            resp = requests.get("" + ip + "/LOCCONV_EXP_DETAIL_GET", params=params, data={}, headers=headers,
                                 verify=False)
            response = resp.content.decode("utf-8")
            return HttpResponse(response)

        elif typ =='LODG':
            params = {"Type": typ,
                      "Api_Type": "WEB"}
            token = jwt.token(request)
            headers = {"content-type": "application/json", "Authorization": "" + token + ""}
            data['Params']["FILTER"]["Entity_Gid"] = decry_data(request.session['Entity_gid'])
            data['Params']["FILTER"]["Employee_gid"] = decry_data(request.session['Emp_gid'])
            dictionary = data.get('Params').get("FILTER")
            for key,value in dictionary.items():
                params[key] = value
            resp = requests.get("" + ip + "/LODGING_EXP_DETAIL_GET", params=params, data={}, headers=headers,
                                 verify=False)
            response = resp.content.decode("utf-8")
            return HttpResponse(response)

        elif typ =='MISC':
            params = {"Type": typ,
                      "Api_Type": "WEB"}
            token = jwt.token(request)
            headers = {"content-type": "application/json", "Authorization": "" + token + ""}
            data['Params']["FILTER"]["Entity_Gid"] = decry_data(request.session['Entity_gid'])
            data['Params']["FILTER"]["Employee_gid"] = decry_data(request.session['Emp_gid'])
            dictionary = data.get('Params').get("FILTER")
            for key,value in dictionary.items():
                params[key] = value
            resp = requests.get("" + ip + "/MISC_EXP_DETAIL_GET", params=params, data={}, headers=headers,
                                 verify=False)
            response = resp.content.decode("utf-8")
            return HttpResponse(response)

        elif typ =='PCKG':
            params = {"Type": typ,
                      "Api_Type": "WEB"}
            token = jwt.token(request)
            headers = {"content-type": "application/json", "Authorization": "" + token + ""}
            data['Params']["FILTER"]["Entity_Gid"] = decry_data(request.session['Entity_gid'])
            data['Params']["FILTER"]["Employee_gid"] = decry_data(request.session['Emp_gid'])
            dictionary = data.get('Params').get("FILTER")
            for key,value in dictionary.items():
                params[key] = value
            resp = requests.get("" + ip + "/PKGMVG_EXP_DETAIL_GET", params=params, data={}, headers=headers,
                                 verify=False)
            response = resp.content.decode("utf-8")
            return HttpResponse(response)

    elif request.method == 'POST':
        jsondata = json.loads(request.body.decode('utf-8'))
        typ = jsondata.get('params').get('Type')
        if typ == 'ELIGIBLE_AMOUNT_DAILYDIEM':
            params = {"Type": request.session['type'],
                      "Api_Type": "WEB"}
            employee_gid = onbehalf_check(request)
            token = jwt.token(request)
            headers = {"content-type": "application/json", "Authorization": "" + token + ""}
            jsondata['params']['json']['Params']["FILTER"]["Entity_Gid"] = decry_data(request.session['Entity_gid'])
            jsondata['params']['json']['Params']["FILTER"]["Entity_Gid_d"] = request.session['Entity_gid']
            jsondata['params']['json']['Params']["FILTER"]["Employee_gid"] = employee_gid
            datas = json.dumps(jsondata.get('params').get('json').get('Params').get('FILTER'))
            resp = requests.post("" + ip + "/DAILYDIEM_EXP_ELIGIBLITY_CALC", params=params, data=datas, headers=headers,
                                 verify=False)
            response = resp.content.decode("utf-8")
            return HttpResponse(response)

        elif typ == 'ELIGIBLE_AMOUNT_TRAVEL':
            params = {"Type": request.session['type'],
                      "Api_Type": "WEB"}
            employee_gid = onbehalf_check(request)
            token = jwt.token(request)
            headers = {"content-type": "application/json", "Authorization": "" + token + ""}
            jsondata['params']['json']['Params']["FILTER"]["Entity_Gid"] = decry_data(request.session['Entity_gid'])
            jsondata['params']['json']['Params']["FILTER"]["Entity_Gid_d"] = request.session['Entity_gid']
            jsondata['params']['json']['Params']["FILTER"]["Employee_gid"] = employee_gid
            datas = json.dumps(jsondata.get('params').get('json').get('Params').get('FILTER'))
            resp = requests.post("" + ip + "/TRAVEL_EXP_ELIGIBLITY_CALC", params=params, data=datas, headers=headers,
                                 verify=False)
            response = resp.content.decode("utf-8")
            return HttpResponse(response)

        elif typ == 'ELIGIBLE_AMOUNT_INCI':
            params = {"Type": request.session['type'],
                      "Api_Type": "WEB"}
            employee_gid = onbehalf_check(request)
            token = jwt.token(request)
            headers = {"content-type": "application/json", "Authorization": "" + token + ""}
            jsondata['params']['json']['Params']["FILTER"]["Entity_Gid"] = decry_data(request.session['Entity_gid'])
            jsondata['params']['json']['Params']["FILTER"]["Entity_Gid_d"] = request.session['Entity_gid']
            jsondata['params']['json']['Params']["FILTER"]["Employee_gid"] = employee_gid
            datas = json.dumps(jsondata.get('params').get('json').get('Params').get('FILTER'))
            resp = requests.post("" + ip + "/INCIDENTAL_EXP_ELIGIBLITY_CALC", params=params, data=datas, headers=headers,
                                 verify=False)
            response = resp.content.decode("utf-8")
            return HttpResponse(response)

        elif typ == 'ELIGIBLE_AMOUNT_LODG':
            params = {"Type": request.session['type'],
                      "Api_Type": "WEB"}
            employee_gid = onbehalf_check(request)
            token = jwt.token(request)
            headers = {"content-type": "application/json", "Authorization": "" + token + ""}
            jsondata['params']['json']['Params']["FILTER"]["Entity_Gid"] = decry_data(request.session['Entity_gid'])
            jsondata['params']['json']['Params']["FILTER"]["Entity_Gid_d"] = request.session['Entity_gid']
            jsondata['params']['json']['Params']["FILTER"]["Employee_gid"] = employee_gid
            datas = json.dumps(jsondata.get('params').get('json').get('Params').get('FILTER'))
            resp = requests.post("" + ip + "/LODGING_EXP_ELIGIBLITY_CALC", params=params, data=datas, headers=headers,
                                 verify=False)
            response = resp.content.decode("utf-8")
            return HttpResponse(response)

        elif typ == 'ELIGIBLE_AMOUNT_LOC':
            params = {"Type": request.session['type'],
                      "Api_Type": "WEB"}
            employee_gid = onbehalf_check(request)
            token = jwt.token(request)
            headers = {"content-type": "application/json", "Authorization": "" + token + ""}
            jsondata['params']['json']['Params']["FILTER"]["Entity_Gid"] = decry_data(request.session['Entity_gid'])
            jsondata['params']['json']['Params']["FILTER"]["Entity_Gid_d"] = request.session['Entity_gid']
            jsondata['params']['json']['Params']["FILTER"]["Employee_gid"] = employee_gid
            datas = json.dumps(jsondata.get('params').get('json').get('Params').get('FILTER'))
            resp = requests.post("" + ip + "/LOCCONV_EXP_ELIGIBLITY_CALC", params=params, data=datas, headers=headers,
                                 verify=False)
            response = resp.content.decode("utf-8")
            return HttpResponse(response)

        elif typ == 'ELIGIBLE_AMOUNT_PKG':
            params = {"Type": request.session['type'],
                      "Api_Type": "WEB"}
            employee_gid = onbehalf_check(request)
            token = jwt.token(request)
            headers = {"content-type": "application/json", "Authorization": "" + token + ""}
            jsondata['params']['json']['Params']["FILTER"]["Entity_Gid"] = decry_data(request.session['Entity_gid'])
            jsondata['params']['json']['Params']["FILTER"]["Entity_Gid_d"] = request.session['Entity_gid']
            jsondata['params']['json']['Params']["FILTER"]["Employee_gid"] = employee_gid
            datas = json.dumps(jsondata.get('params').get('json').get('Params').get('FILTER'))
            resp = requests.post("" + ip + "/PKGMVG_EXP_ELIGIBLITY_CALC", params=params, data=datas, headers=headers,
                                 verify=False)
            response = resp.content.decode("utf-8")
            return HttpResponse(response)

        elif typ == 'ELIGIBLE_AMOUNT_MISC':
            params = {"Type": request.session['type'],
                      "Api_Type": "WEB"}
            employee_gid = onbehalf_check(request)
            token = jwt.token(request)
            headers = {"content-type": "application/json", "Authorization": "" + token + ""}
            jsondata['params']['json']['Params']["FILTER"]["Entity_Gid"] = decry_data(request.session['Entity_gid'])
            jsondata['params']['json']['Params']["FILTER"]["Entity_Gid_d"] = request.session['Entity_gid']
            jsondata['params']['json']['Params']["FILTER"]["Employee_gid"] = employee_gid
            datas = json.dumps(jsondata.get('params').get('json').get('Params').get('FILTER'))
            resp = requests.post("" + ip + "/MISC_EXP_ELIGIBLITY_CALC", params=params, data=datas, headers=headers,
                                 verify=False)
            response = resp.content.decode("utf-8")
            return HttpResponse(response)

        elif typ == 'APPROVE_AMT':
            params = {"Type": typ,
                      "Api_Type": "WEB"}
            token = jwt.token(request)
            employee_gid = onbehalf_check(request)
            headers = {"content-type": "application/json", "Authorization": "" + token + ""}
            jsondata['params']['json']['Params']['DETAILS']["processedby"] = employee_gid
            jsondata['params']['json']['Params']['DETAILS']["createby"] = employee_gid
            jsondata['params']['json']['Params']['DETAILS']["Entity_Gid"] = decry_data(request.session['Entity_gid'])
            datas = json.dumps(jsondata.get('params').get('json'))
            resp = requests.post("" + ip + "/APPROVE_AMOUNT_CHANGE_SET", params=params, data=datas, headers=headers,
                                 verify=False)
            response = resp.content.decode("utf-8")
            return HttpResponse(response)

        elif typ == 'DAILY_DIEM':
            params = {"Type": request.session['type'],
                      "Api_Type": "WEB"}
            token = jwt.token(request)
            employee_gid = onbehalf_check(request)
            headers = {"content-type": "application/json", "Authorization": "" + token + ""}
            jsondata['params']['json']['Params']['DETAILS']["processedby"] = employee_gid
            jsondata['params']['json']['Params']['DETAILS']["createby"] = employee_gid
            jsondata['params']['json']['Params']['DETAILS']["Entity_Gid"] = decry_data(request.session['Entity_gid'])
            jsondata = onbehalf_data(request, jsondata)
            datas = json.dumps(jsondata.get('params').get('json'))
            resp = requests.post("" + ip + "/DAILYDIEM_EXP_DETAIL_SET", params=params, data=datas, headers=headers,
                                 verify=False)
            response = resp.content.decode("utf-8")
            return HttpResponse(response)

        elif typ == 'LODGING':
            params = {"Type": request.session['type'],
                      "Api_Type": "WEB"}
            token = jwt.token(request)
            employee_gid = onbehalf_check(request)
            headers = {"content-type": "application/json", "Authorization": "" + token + ""}
            jsondata['params']['json']['Params']['DETAILS']["processedby"] = employee_gid
            jsondata['params']['json']['Params']['DETAILS']["createby"] = employee_gid
            jsondata['params']['json']['Params']['DETAILS']["Entity_Gid"] = decry_data(request.session['Entity_gid'])
            jsondata = onbehalf_data(request, jsondata)
            datas = json.dumps(jsondata.get('params').get('json'))
            resp = requests.post("" + ip + "/LODGING_EXP_DETAIL_SET", params=params, data=datas, headers=headers,
                                 verify=False)
            response = resp.content.decode("utf-8")
            return HttpResponse(response)

        elif typ == 'LOC_CON':
            params = {"Type": request.session['type'],
                      "Api_Type": "WEB"}
            token = jwt.token(request)
            employee_gid = onbehalf_check(request)
            headers = {"content-type": "application/json", "Authorization": "" + token + ""}
            jsondata['params']['json']['Params']['DETAILS']["processedby"] = employee_gid
            jsondata['params']['json']['Params']['DETAILS']["createby"] = employee_gid
            jsondata['params']['json']['Params']['DETAILS']["Entity_Gid"] = decry_data(request.session['Entity_gid'])
            jsondata = onbehalf_data(request, jsondata)
            datas = json.dumps(jsondata.get('params').get('json'))
            resp = requests.post("" + ip + "/LOCCONV_EXP_DETAIL_SET", params=params, data=datas, headers=headers,
                                 verify=False)
            response = resp.content.decode("utf-8")
            return HttpResponse(response)

        elif typ == 'MISCELLANEOUS':
            params = {"Type": request.session['type'],
                      "Api_Type": "WEB"}
            token = jwt.token(request)
            employee_gid = onbehalf_check(request)
            headers = {"content-type": "application/json", "Authorization": "" + token + ""}
            jsondata['params']['json']['Params']['DETAILS']["processedby"] = employee_gid
            jsondata['params']['json']['Params']['DETAILS']["createby"] = employee_gid
            jsondata['params']['json']['Params']['DETAILS']["Entity_Gid"] = decry_data(request.session['Entity_gid'])
            jsondata = onbehalf_data(request, jsondata)
            datas = json.dumps(jsondata.get('params').get('json'))
            resp = requests.post("" + ip + "/MISC_EXP_DETAIL_SET", params=params, data=datas, headers=headers,
                                 verify=False)
            response = resp.content.decode("utf-8")
            return HttpResponse(response)

        elif typ == 'PKG_MOVING':
            params = {"Type": request.session['type'],
                      "Api_Type": "WEB"}
            token = jwt.token(request)
            employee_gid = onbehalf_check(request)
            headers = {"content-type": "application/json", "Authorization": "" + token + ""}
            jsondata['params']['json']['Params']['DETAILS']["processedby"] = employee_gid
            jsondata['params']['json']['Params']['DETAILS']["createby"] = employee_gid
            jsondata['params']['json']['Params']['DETAILS']["Entity_Gid"] = decry_data(request.session['Entity_gid'])
            jsondata = onbehalf_data(request, jsondata)
            datas = json.dumps(jsondata.get('params').get('json'))
            resp = requests.post("" + ip + "/PKGMVG_EXP_DETAIL_SET", params=params, data=datas, headers=headers,
                                 verify=False)
            response = resp.content.decode("utf-8")
            return HttpResponse(response)

        elif typ == 'TRAVEL_EXP':
            params = {"Type": request.session['type'],
                      "Api_Type": "WEB"}
            token = jwt.token(request)
            employee_gid = onbehalf_check(request)
            headers = {"content-type": "application/json", "Authorization": "" + token + ""}
            jsondata['params']['json']['Params']['DETAILS']["processedby"] = employee_gid
            jsondata['params']['json']['Params']['DETAILS']["createby"] = employee_gid
            jsondata['params']['json']['Params']['DETAILS']["Entity_Gid"] = decry_data(request.session['Entity_gid'])
            jsondata = onbehalf_data(request, jsondata)
            datas = json.dumps(jsondata.get('params').get('json'))
            resp = requests.post("" + ip + "/TRAVEL_EXP_DETAIL_SET", params=params, data=datas, headers=headers,
                                 verify=False)
            response = resp.content.decode("utf-8")
            return HttpResponse(response)

        elif typ == 'INCIDENTAL':
            params = {"Type": request.session['type'],
                      "Api_Type": "WEB"}
            token = jwt.token(request)
            employee_gid = onbehalf_check(request)
            headers = {"content-type": "application/json", "Authorization": "" + token + ""}
            jsondata['params']['json']['Params']['DETAILS']["processedby"] = employee_gid
            jsondata['params']['json']['Params']['DETAILS']["createby"] = employee_gid
            jsondata['params']['json']['Params']['DETAILS']["Entity_Gid"] = decry_data(request.session['Entity_gid'])
            jsondata = onbehalf_data(request, jsondata)
            datas = json.dumps(jsondata.get('params').get('json'))
            resp = requests.post("" + ip + "/INCIDENTAL_EXP_DETAIL_SET", params=params, data=datas, headers=headers,
                                 verify=False)
            response = resp.content.decode("utf-8")
            return HttpResponse(response)

def tour_generate_xl(request):
    # utl.check_authorization(request)
    if request.method == 'GET':
        typ = request.GET['Type']
        if typ =='EMPLOYEE_WISE':
            params = {"Type": typ,
                      "Api_Type": "WEB"}
            token = jwt.token(request)
            data={
                "Params":{
                    "FILTER":{

                    }
                }
            }
            data['Params']["FILTER"]['employee_gid'] = request.GET['employee_gid']
            data['Params']["FILTER"]['tourno'] = request.GET['tourno']
            data['Params']["FILTER"]['tourreqdate'] = request.GET['reqdate']
            data['Params']["FILTER"]['onbehalfgid'] = request.GET['onbehalfgid']
            data['Params']["FILTER"]['Entity_gid'] = decry_data(request.session['Entity_gid'])
            headers = {"content-type": "application/json", "Authorization": "" + token + ""}
            datas = json.dumps(data)
            resp = requests.post("" + ip + "/TOUR_REPORT_DOWNLOAD", params=params, data=datas, headers=headers,
                                 verify=False)
            response = resp.content
            XLSX_MIME = 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
            # response['Content-Disposition'] = 'attachment; filename="TA_Report.xlsx"'
            return HttpResponse(response, content_type=XLSX_MIME)
            # return response
        elif typ =='TOUR_DETAIL':
            params = {"Type": typ,
                      "Api_Type": "WEB",
                      "Tour_Gid": request.GET['tourgid'],
                      }
            token = jwt.token(request)
            data = {}
            headers = {"content-type": "application/json", "Authorization": "" + token + ""}
            datas = json.dumps(data)
            resp = requests.get("" + ip + "/TOUR_DETAIL_REPORT_DOWNLOAD", params=params, data=datas, headers=headers,
                                 verify=False)
            response = resp.content
            XLSX_MIME = 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
            # response['Content-Disposition'] = 'attachment; filename="TA_Report.xlsx"'
            return HttpResponse(response, content_type=XLSX_MIME)
            # return response
        elif typ =='TOUR_EXPENSE':
            params = {"Type": typ,
                      "Api_Type": "WEB",
                      "Tour_Gid": request.GET['tourgid'],
                      }
            token = jwt.token(request)
            data = {}
            headers = {"content-type": "application/json", "Authorization": "" + token + ""}
            datas = json.dumps(data)
            resp = requests.get("" + ip + "/TOUR_EXPENSE_REPORT_DOWNLOAD", params=params, data=datas, headers=headers,
                                 verify=False)
            response = resp.content
            XLSX_MIME = 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
            # response['Content-Disposition'] = 'attachment; filename="TA_Report.xlsx"'
            return HttpResponse(response, content_type=XLSX_MIME)
            # return response



def session_set_expense(request):
    utl.check_authorization(request)
    if request.method == 'POST':
        jsondata = json.loads(request.body.decode('utf-8'))
        session_key_values=jsondata.get('Params').get('FILTER')
        for (k, v) in session_key_values.items():
            request.session[k] = v
        return HttpResponse("SUCCESS")

def session_get_expnese(request):
    utl.check_authorization(request)
    if request.method == 'POST':
        jsondata = json.loads(request.body.decode('utf-8'))
        session_keys=jsondata.get('Params').get('FILTER')
        data={}
        for (k, v) in session_keys.items():
            data[k]=request.session[k]
        return JsonResponse(data, safe=False)


def onbehalf_check(request):
    type = request.session['type']
    if type =='SELF':
        employee_gid = decry_data(request.session['Emp_gid'])
        return employee_gid
    elif type =='ONBEHALF':
        employee_gid = request.session['onbehalfgid']
        return employee_gid
    else:
        employee_gid = decry_data(request.session['Emp_gid'])
        return employee_gid

def onbehalf_check_smry(request,jdata):
    type = jdata.get('params').get('json').get('Params').get('FILTER').get('type')
    if type =='SELF':
        employee_gid = decry_data(request.session['Emp_gid'])
        return employee_gid
    elif type =='ONBEHALF':
        employee_gid = jdata.get('params').get('json').get('Params').get('FILTER').get('onbehalfgid')
        return employee_gid

def onbehalf_data(request,data):
    type = request.session['type']
    if type =='ONBEHALF':
        data['params']['json']['Params']['DETAILS']["onbehalfof"] = decry_data(request.session['Emp_gid'])
        return data
    else:
        return data

def onbehalf_data_exp(request,data):
    type = request.session['type']
    if type =='ONBEHALF':
        data['Params']['DETAILS']["onbehalfof"] = decry_data(request.session['Emp_gid'])
        return data
    else:
        return data

def onbehalf_filter_data(request,data):
    type = request.session['type']
    if type =='ONBEHALF':
        data['params']['json']['Params']["FILTER"]["onbehalfgid"] = request.session['onbehalfgid']
        return data
    else:
        return data

def onbehalf_data_aprvl(request,data):
    type = request.session['type']
    if type =='ONBEHALF':
        data['params']['json']['Params']['DETAILS']["onbehalfgid"] = request.session['onbehalfgid']
        data['params']['json']['Params']['DETAILS']["type"] = request.session['type']
        return data
    else:
        data['params']['json']['Params']['DETAILS']["type"] = request.session['type']
        return data