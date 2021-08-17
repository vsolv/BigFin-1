import io
import os

import boto3
import requests
from django.core.files.storage import default_storage
from django.shortcuts import render
from django.http import JsonResponse, HttpResponse, StreamingHttpResponse
import json
from Bigflow.Core.models import decrpt as decry_data
import Bigflow.Core.jwt_file as jwt
from Bigflow.AP.model import mAP
from Bigflow.StandardInstructions.Model import mStandardInstructions
from Bigflow.BranchExp.model import mBranch
import pandas as pd
from datetime import datetime
from Bigflow.settings import S3_BUCKET_NAME
from django.core.mail import EmailMessage
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.template.loader import render_to_string, get_template
from django.template import Context
from django.template import Context, Template, RequestContext
from django.views import View
import Bigflow.Core.models as common
import barcode
from barcode.writer import ImageWriter
from Bigflow.Core import views as master_views
from pathlib import Path
# from tabulate import tabulate
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from django.conf import settings
from datetime import datetime
import time
import pytz
import re
import Bigflow.Core.views as CoreViews
# from Bigflow.API import views`
from Bigflow.settings import BASE_DIR
from Bigflow.menuClass import utility as utl

from apscheduler.scheduler import Scheduler

sched = Scheduler()
sched.start()

ip = common.localip()
token = common.token()


def billentryIndex(request):
    utl.check_authorization(request)
    return render(request, "AP_billentry.html")


def billentry_checker(request):
    utl.check_authorization(request)
    return render(request, "AP_Billentry_Checker.html")


def APsummary(request):
    utl.check_authorization(request)
    return render(request, "AP_APSummary.html")


def bill(request):
    utl.check_authorization(request)
    return render(request, "AP_BILL.html")


def POinvoice(request):
    utl.check_authorization(request)
    return render(request, "AP_POinvoicemk.html")


def Stalesummary(request):
    utl.check_authorization(request)
    return render(request, "AP_Stalesummary.html")


def ECF_billentry_checker(request):
    utl.check_authorization(request)
    return render(request, "ECF_Billentry_Checker.html")


def Invoicesummary(request):
    utl.check_authorization(request)
    return render(request, "AP_invoicesummary.html")


def AP_Report(request):
    utl.check_authorization(request)
    return render(request, "AP_Report.html")


def GL_Report(request):
    utl.check_authorization(request)
    return render(request, "GL_Report.html")


def Inward_entry(request):
    utl.check_authorization(request)
    return render(request, "AP_Invoice-Inwardentry.html")


def Approvalsummary(request):
    utl.check_authorization(request)
    return render(request, "AP_Approvalsummary.html")


def AP_History(request):
    utl.check_authorization(request)
    return render(request, "AP_History.html")


def PreparePayment(request):
    utl.check_authorization(request)
    return render(request, "AP_Paymentsummary.html")


def PrepareFile(request):
    utl.check_authorization(request)
    return render(request, "AP_Payment.html")


def paymentupdate(request):
    utl.check_authorization(request)
    return render(request, "AP_PaymentUpdation.html")


def Rejectsummary(request):
    utl.check_authorization(request)
    return render(request, "AP_Rejectsummary.html")


def claimrejection(request):
    utl.check_authorization(request)
    return render(request, "AP_Claimrejection.html")


def billentryedit(request):
    utl.check_authorization(request)
    return render(request, "AP_billentryEdit.html")


def Makersummary(request):
    utl.check_authorization(request)
    return render(request, "AP_makersummary.html", {"my_data": {}})


def AP_PaymentStatus(request):
    utl.check_authorization(request)
    return render(request, "AP_PaymentStatus.html")


def Checkersummary(request):
    utl.check_authorization(request)
    return render(request, "AP_CheckerSummary.html")


def Ap_Bounce(request):
    utl.check_authorization(request)
    return render(request, "AP_Bounce.html")


def Ecf_Invoiceentry(request):
    utl.check_authorization(request)
    request.session['ECFINVOICE'] = 'LOCAL'
    return render(request, "ECF_invoiceentry.html")


def Ecf_InvoiceentryCO(request):
    utl.check_authorization(request)
    request.session['ECFINVOICE'] = 'BRANCH'
    return render(request, "ECF_invoiceentry.html")


def ECFinventryCO_Summary(request):
    utl.check_authorization(request)
    return render(request, "ECF_CO_Summary.html")


def EcfInvoicevalue_get(request):
    utl.check_pointaccess(request)
    data = {}
    data['ECFINVOICE'] = request.session['ECFINVOICE']
    data['Emp_gid'] = int(decry_data(request.session['Emp_gid']))
    jdata = data
    return JsonResponse(jdata, safe=False)


def Ecf_billentry(request):
    utl.check_authorization(request)
    return render(request, "ECF_billentry.html")


def ECFPOinvoicemk(request):
    utl.check_authorization(request)
    return render(request, "ECF_POinvoicemk.html")


def ECFApproval(request):
    utl.check_authorization(request)
    return render(request, "ECF_ApprovalSummary.html")


def APECF_entry(request):
    utl.check_authorization(request)
    return render(request, "AP_ECFbillentry.html")


def ECFSummary(request):
    utl.check_authorization(request)
    return render(request, "ECF_Summary.html")


def ECF_Claim_Status_Report(request):
    utl.check_authorization(request)
    return render(request, "ECF_Claim_Status_Report.html")


def Ap_EmployeeQuery(request):
    utl.check_authorization(request)
    return render(request, "Ap_EmployeeQuery.html")


def ECF_AP_Billentry_Checker(request):
    utl.check_authorization(request)
    return render(request, "ECF_AP_Billentry_Checker.html")


def Ap_EmployeeQuery_demo(request):
    # utl.check_authorization(request)
    return render(request, "Ap_EmployeeQuery_demo.html")


def Ecf_ClaimQuery(request):
    # utl.check_authorization(request)
    return render(request, "ECF_ClaimQuery.html")


def Ecf_ClaimQueryCO_DO(request):
    # utl.check_authorization(request)
    return render(request, "ECF_ClaimQueryCO_DO.html")


def AP_GL_Balance(request):
    utl.check_authorization(request)
    return render(request, "AP_GL_Balance.html")


def AP_Accounting_Entry_Query(request):
    utl.check_authorization(request)
    return render(request, "AP_Accounting_Entry_Query.html")


def AP_Accounting_WiseFin_Entry_Query(request):
    utl.check_authorization(request)
    return render(request, "AP_Accounting_WiseFin_Entry_Query.html")


def AP_Onward_Invoice(request):
    utl.check_authorization(request)
    return render(request, "AP_Onward_Invoice.html")


def AP_Onward_Sale_Approval(request):
    utl.check_authorization(request)
    return render(request, "AP_Onward_Sale_Approval.html")


def AP_Onward_Sale_Summary(request):
    utl.check_authorization(request)
    return render(request, "AP_Onward_Sale_Summary.html")


def AP_Ammort_Summary(request):
    utl.check_authorization(request)
    return render(request, "AP_Ammort_Summary.html")


def AP_Ammort_Approval_Summary(request):
    utl.check_authorization(request)
    return render(request, "AP_Ammort_Approval_Summary.html")


def AP_Ammort_Schedule_Summary(request):
    utl.check_authorization(request)
    return render(request, "AP_Ammort_Schedule_Summary.html")


def AP_Ammort_Schedule_Creation(request):
    utl.check_authorization(request)
    return render(request, "AP_Ammort_Schedule_Creation.html")


def AP_Ammort_Approval_Summary(request):
    utl.check_authorization(request)
    return render(request, "AP_Ammort_Approval_Summary.html")


def AP_Ammort_Approval(request):
    utl.check_authorization(request)
    return render(request, "AP_Ammort_Approval.html")


def AP_Ammort_Schedule_Process(request):
    utl.check_authorization(request)
    return render(request, "AP_Ammort_Schedule_Process.html")


def AP_Ammort_Edit(request):
    utl.check_authorization(request)
    return render(request, "AP_Ammort_Edit.html")


def Mst_Emp_Bank(request):
    utl.check_authorization(request)
    return render(request, "Mst_Emp_Bank.html")


def Mst_Branch_Bank(request):
    utl.check_authorization(request)
    return render(request, "Mst_Branch_Bank.html")


def pmd_branch_summary(request):
    utl.check_authorization(request)
    return render(request, "PMD_Branch_Summary.html")


def pmd_create(request):
    utl.check_authorization(request)
    return render(request, "PMD_Create.html")


def AP_Failed_Transaction(request):
    utl.check_authorization(request)
    return render(request, "AP_Failed_Transaction.html")


def AP_Advance_Summary(request):
    utl.check_authorization(request)
    return render(request, "AP_Advance_Summary.html")


def AP_Entry_Update_Summary(request):
    utl.check_authorization(request)
    return render(request, "AP_Entry_Update_Summary.html")


def getgrndetail(request):
    utl.check_pointaccess(request)
    utl.check_authorization(request)
    if request.method == 'POST':
        grn_dtl = mAP.ap_model()
        jsondata = json.loads(request.body.decode('utf-8'))
        grn_dtl.action = jsondata.get('params').get('action')
        grn_dtl.POnumber = jsondata.get('params').get('POnumber')
        grn_dtl.supplier_gid = jsondata.get('params').get('supplier_gid')
        grn_dtl.entity_gid = int(decry_data(request.session['Entity_gid']))
        dtl = grn_dtl.get_grn()
        jdata = dtl.to_json(orient='records')
        return JsonResponse(json.loads(jdata), safe=False)


def outputSplit(tubledtl, index):
    temp = tubledtl[0].split(',')
    if (len(temp) > 1):
        if (index == 0):
            return int(temp[0])
        else:
            return temp[1]
    else:
        return temp[0]


def inwarddtl_get(request):
    utl.check_pointaccess(request)
    utl.check_authorization(request)
    if request.method == 'POST':
        try:
            path = request.path
            inward_dtl = mAP.ap_model()
            jsondata = json.loads(request.body.decode('utf-8'))
            inward_dtl.action = jsondata.get('params').get('action')
            inward_dtl.type = jsondata.get('params').get('type')
            inward_dtl.FILTER_JSON = jsondata.get('params').get('FILTER_JSON')
            inward_dtl.entity_gid = int(decry_data(request.session['Entity_gid']))
            common.main_fun1(request.read(), path)
            out = outputSplit(inward_dtl.get_inwarddtl(), 1)
            return JsonResponse(out, safe=False)
        except Exception as e:
            return JsonResponse({"MESSAGE": "ERROR_OCCURED", "DATA": str(e)})


def Invoice_set(request):
    utl.check_pointaccess(request)
    utl.check_authorization(request)
    if request.method == 'POST':
        try:
            path = request.path
            inward_dtl = mAP.ap_model()
            jsondata = json.loads(request.body.decode('utf-8'))
            inward_dtl.action = jsondata.get('params').get('action')
            inward_dtl.type = jsondata.get('params').get('type')
            inward_dtl.header_json = jsondata.get('params').get('header_json')
            inward_dtl.detail_json = jsondata.get('params').get('detail_json')
            inward_dtl.invoice_json = jsondata.get('params').get('invoice_json')
            inward_dtl.debit_json = jsondata.get('params').get('debit_json')
            inward_dtl.credit_json = jsondata.get('params').get('credit_json')
            inward_dtl.status_json = jsondata.get('params').get('status_json')
            inward_dtl.entity_gid = int(decry_data(request.session['Entity_gid']))
            inward_dtl.employee_gid = int(decry_data(request.session['Emp_gid']))
            common.main_fun1(request.read(), path)
            out = outputSplit(inward_dtl.set_Invoice(), 1)
            return JsonResponse(out, safe=False)
        except Exception as e:
            return JsonResponse({"MESSAGE": "ERROR_OCCURED", "DATA": str(e)})


def common_lock_data(request):
    # utl.check_pointaccess(request)
    # utl.check_authorization(request)
    if request.method == 'POST':
        try:
            path = request.path
            object = mAP.ap_model()
            jsondata = json.loads(request.body.decode('utf-8'))
            entity_gid = int(decry_data(request.session['Entity_gid']))
            employee_gid = int(decry_data(request.session['Emp_gid']))
            action = jsondata.get('action')
            type = jsondata.get('type')
            if (action == "INSERT" and (type == "AP_LOCK" or type == "AP_FORCE_UNLOCK")):
                object.action = jsondata.get('action')
                object.type = jsondata.get('type')
                object.filter = json.dumps(jsondata.get("filter"))
                object.classification = json.dumps({"Entity_Gid": entity_gid, "Emp_gid": employee_gid})
                object.create_by = employee_gid
                out = object.common_lock_set()
                # common.main_fun1(request.read(), path)
                return JsonResponse(out, safe=False)
        except Exception as e:
            return JsonResponse({"MESSAGE": "ERROR_OCCURED", "DATA": str(e)})


def APInvoice_get(request):
    utl.check_pointaccess(request)
    utl.check_authorization(request)
    if request.method == 'POST':
        try:
            path = request.path
            invoice_get = mAP.ap_model()
            jsondata = json.loads(request.body.decode('utf-8'))
            invoice_get.action = jsondata.get('params').get('action')
            invoice_get.ponumber = jsondata.get('params').get('ponumber')
            invoice_get.supplier_gid = jsondata.get('params').get('supplier_gid')
            invoice_get.inwarddetail_gid = jsondata.get('params').get('inwarddetail_gid')
            invoice_get.inwardheader_gid = jsondata.get('params').get('inwardheader_gid')
            invoice_get.status = jsondata.get('params').get('status')
            invoice_get.entity_gid = int(decry_data(request.session['Entity_gid']))
            invoice_get.state_gid = request.session['Entity_state_gid']
            invoice_get.limit = jsondata.get('params').get('limit')
            common.main_fun1(request.read(), path)
            out = invoice_get.Invoice_get()
            jdata = out.to_json(orient='records')
            return JsonResponse(json.loads(jdata), safe=False)
        except Exception as e:
            return JsonResponse({"MESSAGE": "ERROR_OCCURED", "DATA": str(e)})


def Credit_get(request):
    utl.check_pointaccess(request)
    utl.check_authorization(request)
    if request.method == 'POST':
        try:
            path = request.path
            credit_get = mAP.ap_model()
            jsondata = json.loads(request.body.decode('utf-8'))
            credit_get.type = jsondata.get('params').get('type')
            credit_get.supplier_gid = jsondata.get('params').get('supplier_gid')
            credit_get.entity_gid = int(decry_data(request.session['Entity_gid']))
            common.main_fun1(request.read(), path)
            out = credit_get.credit_get()
            jdata = out.to_json(orient='records')
            return JsonResponse(json.loads(jdata), safe=False)
        except Exception as e:
            return JsonResponse({"MESSAGE": "ERROR_OCCURED", "DATA": str(e)})


def get_Mail_Templates_Data(request):
    if request.method == 'POST':
        try:
            path = request.path
            object = mAP.ap_model()
            jsondata = json.loads(request.body.decode('utf-8'))
            entity_gid = int(decry_data(request.session['Entity_gid']))
            employee_gid = int(decry_data(request.session['Emp_gid']))
            action = jsondata.get('params').get('action')
            type = jsondata.get('params').get('type')
            sub_type = jsondata.get('params').get('sub_type')
            if (action == "GET" and type == "MAIL_TEMPLATE" and sub_type == "BOUNCE_MAIL"):
                object.action = jsondata.get('params').get('action')
                object.type = jsondata.get('params').get('type')
                object.filter = json.dumps(jsondata.get('params').get("filter"))
                object.classification = json.dumps({"Entity_Gid": entity_gid, "Emp_gid": employee_gid})
                out = object.get_multiple_email_templates_data()
                Mail_Data = out.get("Mail_Data")[0].get("mailtemplate_body")
                Header_Data = out.get("Header_Data")[0]
                for (k, v) in Header_Data.items():
                    value = str(v)
                    key = "{{" + k + "}}"
                    Mail_Data = Mail_Data.replace(key, value);
                cleanr = re.compile('<.*?>')
                body_text = re.sub(cleanr, '', Mail_Data)
                final_values = {"Data": out, "Body_Text": body_text}
                return JsonResponse(final_values, safe=False)
            elif (action == "GET" and type == "MAIL_DETAIL" and sub_type == "SENDED_MAIL"):
                object.action = jsondata.get('params').get('action')
                object.type = jsondata.get('params').get('type')
                object.filter = json.dumps(jsondata.get('params').get("filter"))
                object.classification = json.dumps({"Entity_Gid": entity_gid, "Emp_gid": employee_gid})
                out = object.get_send_mail()
                jdata = out.to_json(orient='records')
                return JsonResponse(json.loads(jdata), safe=False)
        except Exception as e:
            return JsonResponse({"MESSAGE": "ERROR_OCCURED", "DATA": str(e)})


def fa_accounging_entry(request):
    # utl.check_pointaccess(request)
    # utl.check_authorization(request)
    if request.method == 'POST':
        try:
            log_data = []
            path = request.path
            inward_dtl = mAP.ap_model()
            jsondata = json.loads(request.body.decode('utf-8'))
            entity_gid = int(decry_data(request.session['Entity_gid']))
            employee_gid = int(decry_data(request.session['Emp_gid']))
            inward_dtl.action = "GET"
            inward_dtl.type = "FA_ENTRY"
            invoicehd_Gid = jsondata.get('filter').get('InvoiceHeader_Gid')
            inward_dtl.filter = json.dumps({"InvoiceHeader_Gid": invoicehd_Gid})
            inward_dtl.classification = json.dumps({"Entity_Gid": entity_gid})
            out = inward_dtl.get_invoice_all()
            jdata = json.loads(out.to_json(orient='records'))
            jdata = jdata[0]
            jdata['DETAILS'] = json.loads(jdata.get('DETAILS'))
            data = {
                "Params": {
                    "DETAILS": jdata,
                    "CHANGE": {},
                    "STATUS": {},
                    "CLASSIFICATION": {
                        "Entity_Gid": entity_gid
                    }
                }
            }
            data = json.dumps(data)
            params = {'Group': "FA_ASSET_CLEARANCE", 'Type': "FA_CLEARANCE",
                      "Sub_Type": "INITIAL", "Action": "INSERT", "Employee_Gid": employee_gid}
            token = jwt.token(request)

            log_data = [{"BEFORE_FA_API_DATA": data}]
            common.logger.error(log_data)

            headers = {"content-type": "application/json", "Authorization": "" + token + ""}
            try:
                result = requests.post("" + ip + "/FA_TRAN", params=params, headers=headers, data=data,
                                       verify=False)
                results = json.loads(result.content.decode("utf-8"))

                log_data = [{"AFTER_FA_API_DATA": results}]
                common.logger.error(log_data)

                if results["MESSAGE"] == "SUCCESS":
                    try:
                        print("Vignesh")
                        apfa_obj = mAP.ap_model()
                        apfa_obj.action = "UPDATE"
                        apfa_obj.type = "APTOFA_FLAG"
                        apfa_obj.filter = json.dumps({"InvoiceHeader_Gid": invoicehd_Gid})
                        apfa_obj.classification = '{}'
                        # common.main_fun1(request.read(), path)
                        output = apfa_obj.ap_update_flag()
                        print(output[0])
                        if (output[0] == "SUCCESS"):
                            print(results)
                            return HttpResponse(json.dumps(results))
                        else:
                            return JsonResponse({"MESSAGE": "ERROR_OCCURED", "APTOFA_STATUS_FLAG": output})

                    except Exception as e:
                        return JsonResponse({"MESSAGE": "ERROR_OCCURED", "DATA": str(e)})
                else:
                    return HttpResponse(results)

            except Exception as e:
                return JsonResponse({"MESSAGE": "ERROR_OCCURED", "DATA": str(e)})
        except Exception as e:
            return JsonResponse({"MESSAGE": "ERROR_OCCURED", "DATA": str(e)})


def Invoiceheader_Mail_set(request):
    utl.check_pointaccess(request)
    utl.check_authorization(request)
    if request.method == 'POST':
        try:
            path = request.path
            inward_dtl = mAP.ap_model()
            jsondata = json.loads(request.body.decode('utf-8'))
            body = jsondata.get("params").get("status_json").get("email_text")
            subject = jsondata.get("params").get("status_json").get("subject_")
            email = EmailMessage(subject, body, to=["vsolvstab@gmail.com"])
            email.send()
            if (jsondata.get('params').get('action') == 'UPDATE' and jsondata.get('params').get(
                    'type') == 'MAIL_STATUS'):
                try:
                    inward_dtl.action = jsondata.get('params').get('action')
                    inward_dtl.type = jsondata.get('params').get('type')
                    inward_dtl.header_json = jsondata.get('params').get('header_json')
                    inward_dtl.debit_json = jsondata.get('params').get('debit_json')
                    inward_dtl.detail_json = jsondata.get('params').get('detail_json')
                    email_text_value = jsondata.get('params').get('status_json').get("email_text")
                    email_text = email_text_value.replace("\'", " ")
                    json_filter = jsondata.get('params').get('status_json')
                    json_filter["email_text"] = email_text
                    inward_dtl.status_json = json_filter
                    inward_dtl.entity_gid = int(decry_data(request.session['Entity_gid']))
                    inward_dtl.employee_gid = int(decry_data(request.session['Emp_gid']))
                    # common.main_fun1(request.read(), path)
                    out = outputSplit(inward_dtl.set_Invoiceheader(), 1)
                    if (out == "SUCCESS"):
                        return JsonResponse(out, safe=False)
                    else:
                        return JsonResponse({"MESSAGE": "Email Successfully Sended Data Not Updated", "DATA": out})
                except Exception as e:
                    return JsonResponse({"MESSAGE": "ERROR_OCCURED", "DATA": str(e)})
        except Exception as e:
            return JsonResponse("Email_Not_Send", safe=False)


def HSN_get(request):
    utl.check_pointaccess(request)
    utl.check_authorization(request)
    if request.method == 'POST':
        try:
            path = request.path
            credit_get = mAP.ap_model()
            credit_get.type = "HSN"
            credit_get.group = "HSN"
            credit_get.filter = {}
            credit_get.entity_gid = int(decry_data(request.session['Entity_gid']))
            common.main_fun1(request.read(), path)
            out = credit_get.hsn_get()
            jdata = out.to_json(orient='records')
            return JsonResponse(json.loads(jdata), safe=False)
        except Exception as e:
            return JsonResponse({"MESSAGE": "ERROR_OCCURED", "DATA": str(e)})


def Hsntax_get(request):
    utl.check_pointaccess(request)
    utl.check_authorization(request)
    if request.method == 'POST':
        try:
            path = request.path
            tax = mAP.ap_model()
            jsondata = json.loads(request.body.decode('utf-8'))
            tax.hsndtl = jsondata.get('params').get('hsndtl')
            tax.entity_gid = int(decry_data(request.session['Entity_gid']))
            tax.group = jsondata.get('params').get('group')
            common.main_fun1(request.read(), path)
            out = tax.hsn_taxget()
            data1 = pd.DataFrame(out, columns=['gst'])
            # data1 = {"detail":out}
            jdata = data1.to_json(orient='records')
            return JsonResponse(jdata, safe=False)
        except Exception as e:
            return JsonResponse({"MESSAGE": "ERROR_OCCURED", "DATA": str(e)})


def HsntaxCredit_get(request):
    utl.check_pointaccess(request)
    utl.check_authorization(request)
    if request.method == 'POST':
        try:
            path = request.path
            tax = mAP.ap_model()
            jsondata = json.loads(request.body.decode('utf-8'))
            group = jsondata.get("params").get("group")
            if (group == "TDS_DATAGET"):
                tax.hsndtl = jsondata.get('params').get('hsndtl')
                tax.entity_gid = int(decry_data(request.session['Entity_gid']))
                tax.group = jsondata.get('params').get('group')
                common.main_fun1(request.read(), path)
                out = tax.hsn_Credittaxget_multiple()
                # jdata = out.to_json(orient='records')
                return JsonResponse(out, safe=False)
            else:
                tax.hsndtl = jsondata.get('params').get('hsndtl')
                tax.entity_gid = int(decry_data(request.session['Entity_gid']))
                tax.group = jsondata.get('params').get('group')
                common.main_fun1(request.read(), path)
                out = tax.hsn_Credittaxget()
                jdata = out.to_json(orient='records')
                return JsonResponse(jdata, safe=False)
        except Exception as e:
            return JsonResponse({"MESSAGE": "ERROR_OCCURED", "DATA": str(e)})


def tablevalue(request):
    utl.check_pointaccess(request)
    utl.check_authorization(request)
    if request.method == 'POST':
        dropdown = mAP.ap_model()
        jsondata = json.loads(request.body.decode('utf-8'))
        dropdown.type = "DEBIT"
        dropdown.tablevalue = jsondata.get('params').get('tablevalue')
        dropdown.entity_gid = int(decry_data(request.session['Entity_gid']))
        out = dropdown.tablevalue_get()
        jdata = out.to_json(orient='records')
        return JsonResponse(json.loads(jdata), safe=False)


def ap_cat_get_sp(request):
    utl.check_pointaccess(request)
    utl.check_authorization(request)
    if request.method == 'POST':
        dropdown = mAP.ap_model()
        jsondata = json.loads(request.body.decode('utf-8'))
        dropdown.type = "DEBIT"
        dropdown.tablevalue = jsondata.get('params').get('tablevalue')
        dropdown.entity_gid = int(decry_data(request.session['Entity_gid']))
        out = dropdown.get_ap_cat()
        jdata = out.to_json(orient='records')
        return JsonResponse(json.loads(jdata), safe=False)


def ap_paymode_details(request):
    utl.check_pointaccess(request)
    utl.check_authorization(request)
    if request.method == 'POST':
        try:
            path = request.path
            employee_gid = int(decry_data(request.session['Emp_gid']))
            entity_gid = int(decry_data(request.session['Entity_gid']))
            invoice_set = mAP.ap_model()
            jsondata = json.loads(request.body.decode('utf-8'))
            invoice_set.action = jsondata.get('action')
            invoice_set.type = jsondata.get('type')
            filter = jsondata.get('filter')
            invoice_set.filter = json.dumps(filter)
            invoice_set.classification = json.dumps({"Entity_Gid": entity_gid})
            invoice_set.create_by = employee_gid
            common.main_fun1(request.read(), path)
            out = invoice_set.get_ap_paymode_details()
            jdata = out.to_json(orient='records')
            return JsonResponse(json.loads(jdata), safe=False)
        except Exception as e:
            return JsonResponse({"MESSAGE": "ERROR_OCCURED", "DATA": str(e)})


def get_subcategory_data(request):
    utl.check_pointaccess(request)
    utl.check_authorization(request)
    if request.method == 'POST':
        dropdown = mAP.ap_model()
        jsondata = json.loads(request.body.decode('utf-8'))
        dropdown.type = "DEBIT"
        dropdown.tablevalue = jsondata.get('params').get('tablevalue')
        dropdown.entity_gid = int(decry_data(request.session['Entity_gid']))
        out = dropdown.subcategory_tablevalue_get()
        jdata = out.to_json(orient='records')
        return JsonResponse(json.loads(jdata), safe=False)


def APInvoiceChecker_get(request):
    utl.check_pointaccess(request)
    utl.check_authorization(request)
    if request.method == 'POST':
        try:
            invoice_get = mAP.ap_model()
            jsondata = json.loads(request.body.decode('utf-8'))
            invoice_get.action = jsondata.get('params').get('action')
            invoice_get.ponumber = jsondata.get('params').get('ponumber')
            invoice_get.supplier_gid = jsondata.get('params').get('supplier_gid')
            invoice_get.inwarddetail_gid = jsondata.get('params').get('inwarddetail_gid')
            invoice_get.inwardheader_gid = jsondata.get('params').get('inwardheader_gid')
            invoice_get.status = jsondata.get('params').get('status')
            invoice_get.entity_gid = int(decry_data(request.session['Entity_gid']))
            invoice_get.state_gid = request.session['Entity_state_gid']
            out = invoice_get.Invoice_get()
            out = out.fillna(0)
            if invoice_get.action == 'INVOICE_DETAILS_EDIT':
                df_invoice = (out[['invoicedetails_gid', 'invoicedetails_item', 'invoicedetails_desc',
                                   'invoicedetails_hsncode', 'invoicedetails_unitprice', 'invoicedetails_qty',
                                   'invoicedetails_sgst',
                                   'invoicedetails_cgst', 'invoicedetails_igst', 'invoicedetails_amount',
                                   'invoicedetails_discount', 'invoicedetails_totalamt', 'DEBIT_DETAILS']]).groupby(
                    ['invoicedetails_gid', 'invoicedetails_item', 'invoicedetails_desc', 'invoicedetails_hsncode',
                     'invoicedetails_unitprice', 'invoicedetails_qty', 'invoicedetails_sgst',
                     'invoicedetails_cgst', 'invoicedetails_igst', 'invoicedetails_amount', 'invoicedetails_discount',
                     'invoicedetails_totalamt', 'DEBIT_DETAILS']).size().reset_index();
                df_debit = out.groupby(
                    ['invoicedetails_gid', 'debit_gid', 'debit_categorygid', 'debit_subcategorygid',
                     'debit_glno', 'debit_amount', 'DEBIT_DETAILS']).size().reset_index()
                df_credit = (
                    out[['credit_gid', 'credit_paymodegid', 'credit_refno', 'bankbranch_ifsccode',
                         'bankdetails_bank_gid',
                         'credit_glno', 'credit_amount', 'Paymode_name', 'bankdetails_beneficiaryname',
                         'credit_suppliertaxtrate', 'credit_suppliertaxtype',
                         'ppxdetails_ppxheadergid', 'ppxdetails_gid', 'bankbranch_name']]).groupby(
                    ['credit_gid', 'credit_paymodegid', 'credit_refno', 'bankbranch_ifsccode', 'bankdetails_bank_gid',
                     'credit_glno', 'credit_amount', 'Paymode_name', 'bankdetails_beneficiaryname',
                     'credit_suppliertaxtrate', 'credit_suppliertaxtype',
                     'ppxdetails_ppxheadergid', 'ppxdetails_gid', 'bankbranch_name']).size().reset_index();
                df_credit.loc[df_credit['Paymode_name'] != 'NEFT', 'bankbranch_ifsccode'] = ''
                df_credit.loc[df_credit['Paymode_name'] != 'NEFT', 'bankdetails_beneficiaryname'] = ''
                df_credit.loc[df_credit['Paymode_name'] != 'NEFT', 'bankbranch_name'] = ''
            else:
                df_invoice = (out[['invoicedetails_gid', 'invoicedetails_item', 'invoicedetails_desc',
                                   'invoicedetails_hsncode', 'invoicedetails_unitprice', 'invoicedetails_qty',
                                   'invoicedetails_sgst',
                                   'invoicedetails_cgst', 'invoicedetails_igst', 'invoicedetails_amount',
                                   'invoicedetails_discount',
                                   'invoicedetails_totalamt', 'DEBIT_DETAILS']]).groupby(
                    ['invoicedetails_gid', 'invoicedetails_item', 'invoicedetails_desc', 'invoicedetails_hsncode',
                     'invoicedetails_unitprice', 'invoicedetails_qty', 'invoicedetails_sgst',
                     'invoicedetails_cgst', 'invoicedetails_igst', 'invoicedetails_amount', 'invoicedetails_discount',
                     'invoicedetails_totalamt', 'DEBIT_DETAILS']).size().reset_index();
                df_debit = out.groupby(
                    ['invoicedetails_gid', 'debit_gid', 'debit_categorygid', 'debit_subcategorygid',
                     'debit_glno', 'debit_amount']).size().reset_index();
                df_credit = (
                    out[['credit_gid', 'credit_paymodegid', 'credit_refno', 'bankbranch_ifsccode',
                         'bankdetails_bank_gid',
                         'credit_glno', 'credit_amount', 'Paymode_name', 'bankdetails_beneficiaryname',
                         'ppxdetails_ppxheadergid', 'ppxdetails_gid', 'bankbranch_name'
                         ]]).groupby(
                    ['credit_gid', 'credit_paymodegid', 'credit_refno', 'bankbranch_ifsccode', 'bankdetails_bank_gid',
                     'credit_glno', 'credit_amount', 'Paymode_name', 'bankdetails_beneficiaryname',
                     'ppxdetails_ppxheadergid', 'ppxdetails_gid', 'bankbranch_name'
                     ]).size().reset_index();
                df_credit.loc[df_credit['Paymode_name'] != 'NEFT', 'bankbranch_ifsccode'] = ''
                df_credit.loc[df_credit['Paymode_name'] != 'NEFT', 'bankdetails_beneficiaryname'] = ''
                df_credit.loc[df_credit['Paymode_name'] != 'NEFT', 'bankbranch_name'] = ''

            data = {}
            data['invoice'] = json.loads(df_invoice.to_json(orient='records'))
            data['debit'] = json.loads(df_debit.to_json(orient='records'))
            data['credit'] = json.loads(df_credit.to_json(orient='records'))
            jdata = data
            return JsonResponse(jdata, safe=False)

        except Exception as e:
            return JsonResponse({"MESSAGE": "ERROR_OCCURED", "DATA": str(e)})


def get_Onward_Invoice(request):
    utl.check_pointaccess(request)
    utl.check_authorization(request)
    if request.method == 'POST':
        try:
            path = request.path
            invoice_get = mAP.ap_model()
            jsondata = json.loads(request.body.decode('utf-8'))
            invoice_get.action = jsondata.get('params').get('action')
            invoice_get.ponumber = jsondata.get('params').get('ponumber')
            invoice_get.supplier_gid = jsondata.get('params').get('supplier_gid')
            invoice_get.inwarddetail_gid = jsondata.get('params').get('inwarddetail_gid')
            invoice_get.inwardheader_gid = jsondata.get('params').get('inwardheader_gid')
            invoice_get.status = jsondata.get('params').get('status')
            invoice_get.entity_gid = int(decry_data(request.session['Entity_gid']))
            invoice_get.state_gid = request.session['Entity_state_gid']
            common.main_fun1(request.read(), path)
            out = invoice_get.Invoice_get()
            jdata = out.to_json(orient='records')
            return JsonResponse(jdata, safe=False)
        except Exception as e:
            return JsonResponse({"MESSAGE": "ERROR_OCCURED", "DATA": str(e)})


def set_Onward_Invoice(request):
    utl.check_pointaccess(request)
    utl.check_authorization(request)
    if request.method == 'POST':
        try:
            path = request.path
            invoice_set = mAP.ap_model()
            jsondata = json.loads(request.body.decode('utf-8'))
            invoice_set.action = jsondata.get('params').get('action')
            invoice_set.type = jsondata.get('params').get('type')
            invoice_set.sub_type = jsondata.get('params').get('sub_type')
            filter = jsondata.get('filter')
            status = jsondata.get('status')
            invoice_set.status = json.dumps(status)
            invoice_set.filter = json.dumps(filter)
            invoice_set.classification = json.dumps({"Entity_Gid": int(decry_data(request.session['Entity_gid']))})
            invoice_set.create_by = int(decry_data(request.session['Emp_gid']))
            common.main_fun1(request.read(), path)
            out = invoice_set.Invoice_set()
            return HttpResponse(out)
        except Exception as e:
            return JsonResponse({"MESSAGE": "ERROR_OCCURED", "DATA": str(e)})


def get_Onward_data(request):
    utl.check_pointaccess(request)
    utl.check_authorization(request)
    if request.method == 'POST':
        try:
            path = request.path
            invoice_set = mAP.ap_model()
            jsondata = json.loads(request.body.decode('utf-8'))
            action = jsondata.get('params').get('action')
            type = jsondata.get('params').get('type')
            if (action == "GET" and type == "ONWARD_SALES"):
                invoice_set.action = jsondata.get('params').get('action')
                invoice_set.type = jsondata.get('params').get('type')
                filter = jsondata.get('filter')
                invoice_set.filter = json.dumps({})
                invoice_set.classification = json.dumps({"Entity_Gid": int(decry_data(request.session['Entity_gid']))})
                invoice_set.create_by = int(decry_data(request.session['Emp_gid']))
                out = invoice_set.get_invoice_all()
                common.main_fun1(request.read(), path)
                jdata = out.to_json(orient='records')
                return JsonResponse(json.loads(jdata), safe=False)
            elif (action == "GET" and (
                    type == "INVOICE_MAKER_SUMMARY" or type == "INVOICE_MAKER_SUMMARY_COUNT" or type == "INVOICE_PAYMENT" or
                    type == "AP_CREDIT_AMOUNT" or type == "AP_INVOICEHEADER_GET" or type == "AP_CREDIT_AMOUNT_COUNT" or
                    type == "AP_INVOICE_PAYMENT_GET" or type == "ENTRY_QUERY" or
                    type == "MAIL_STATUS" or type == "AP_PAYMENTDETAILS" or type == "PO_NOGET" or
                    type == "INWARD_MAKER_SUMMARY" or type == "INWARD_MAKER_SUMMARY_COUNT" or
                    type == "EMP_DETAILS" or type == "SUPPLIER_DETAILS" or type == "BRANCH_DATA_BY_ID" or
                    type == "CREDIT_DETAILS" or type == "WISEFIN_ENTER" or type == "INVOICE_FAILED_SUMMARY" or type == "INVOICE_FAILED_SUMMARY_COUNT")):
                invoice_set.action = jsondata.get('params').get('action')
                invoice_set.type = jsondata.get('params').get('type')
                filter = jsondata.get('params').get('filter')
                invoice_set.filter = json.dumps(filter)
                invoice_set.classification = json.dumps({"Entity_Gid": int(decry_data(request.session['Entity_gid']))})
                invoice_set.create_by = int(decry_data(request.session['Emp_gid']))
                common.main_fun1(request.read(), path)
                out = invoice_set.get_invoice_all()
                jdata = out.to_json(orient='records')
                return JsonResponse(json.loads(jdata), safe=False)

            elif (action == "GET" and (type == "DEBIT_DETAILS" or type == "CCBS_DETAILS")):
                invoice_set.action = jsondata.get('params').get('action')
                invoice_set.type = jsondata.get('params').get('type')
                filter = jsondata.get('params').get('filter')
                invoice_set.filter = json.dumps(filter)
                invoice_set.classification = json.dumps({"Entity_Gid": int(decry_data(request.session['Entity_gid']))})
                common.main_fun1(request.read(), path)
                out = invoice_set.get_ap_debit_details()
                jdata = out.to_json(orient='records')
                return JsonResponse(json.loads(jdata), safe=False)
            elif (action == "GET" and (
                    type == "AP_ENTER_GET" or type == "ECF_TRANS_GET" or type == "AP_WISEFIN_ENTER_GET")):
                invoice_set.action = jsondata.get('params').get('action')
                invoice_set.type = jsondata.get('params').get('type')
                filter = jsondata.get('params').get('filter')
                invoice_set.filter = json.dumps(filter)
                invoice_set.classification = json.dumps({"Entity_Gid": int(decry_data(request.session['Entity_gid']))})
                common.main_fun1(request.read(), path)
                out = invoice_set.get_transaction_details()
                jdata = out.to_json(orient='records')
                return JsonResponse(json.loads(jdata), safe=False)

            elif (action == "GET" and type == "FILE_DETAIL"):
                invoice_set.action = jsondata.get('params').get('action')
                invoice_set.type = jsondata.get('params').get('type')
                filter = jsondata.get('params').get('filter')
                invoice_set.filter = json.dumps(filter)
                invoice_set.classification = json.dumps({"Entity_Gid": int(decry_data(request.session['Entity_gid']))})
                common.main_fun1(request.read(), path)
                out = invoice_set.get_ecf_file_details()
                jdata = out.to_json(orient='records')
                return JsonResponse(json.loads(jdata), safe=False)
            elif (action == "GET" and type == "INVOICE_DETAILS_EDIT"):
                invoice_set.action = jsondata.get('params').get('action')
                invoice_set.type = jsondata.get('params').get('type')
                filter = jsondata.get('params').get('filter')
                invoice_set.filter = json.dumps(filter)
                invoice_set.classification = json.dumps({"Entity_Gid": int(decry_data(request.session['Entity_gid']))})
                invoice_set.create_by = int(decry_data(request.session['Emp_gid']))
                common.main_fun1(request.read(), path)
                jdata = invoice_set.get_billentry_all()
                # jdata = out.to_json(orient='records')
                return JsonResponse(jdata, safe=False)
            elif (action == "GET" and type == "AP_ALL_ENTER_GET"):
                invoice_set.action = jsondata.get('params').get('action')
                invoice_set.type = jsondata.get('params').get('type')
                filter = jsondata.get('params').get('filter')
                invoice_set.filter = json.dumps(filter)
                invoice_set.classification = json.dumps({"Entity_Gid": int(decry_data(request.session['Entity_gid']))})
                invoice_set.create_by = int(decry_data(request.session['Emp_gid']))
                common.main_fun1(request.read(), path)
                jdata = invoice_set.ap_process_get_double_data()
                # jdata = out.to_json(orient='records')
                return JsonResponse(jdata, safe=False)
            elif (action == "GET" and type == "ECF_INVOICE_PAYMENT_GET"):
                invoice_set.action = jsondata.get('params').get('action')
                invoice_set.type = jsondata.get('params').get('type')
                filter = jsondata.get('params').get('filter')
                invoice_set.filter = json.dumps(filter)
                invoice_set.classification = json.dumps({"Entity_Gid": int(decry_data(request.session['Entity_gid']))})
                invoice_set.create_by = int(decry_data(request.session['Emp_gid']))
                common.main_fun1(request.read(), path)
                jdata = invoice_set.ecf_payment_details()
                # jdata = out.to_json(orient='records'
                return JsonResponse(jdata, safe=False)
        except Exception as e:
            return JsonResponse({"MESSAGE": "ERROR_OCCURED", "DATA": str(e)})


def get_Onward_data_demo(request):
    # utl.check_pointaccess(request)
    # utl.check_authorization(request)
    if request.method == 'POST':
        try:
            path = request.path
            invoice_set = mAP.ap_model()
            jsondata = json.loads(request.body.decode('utf-8'))
            action = jsondata.get('params').get('action')
            type = jsondata.get('params').get('type')
            if (action == "GET" and type == "ONWARD_SALES"):
                invoice_set.action = jsondata.get('params').get('action')
                invoice_set.type = jsondata.get('params').get('type')
                filter = jsondata.get('filter')
                invoice_set.filter = json.dumps({})
                invoice_set.classification = json.dumps({"Entity_Gid": int(decry_data(request.session['Entity_gid']))})
                invoice_set.create_by = int(decry_data(request.session['Emp_gid']))
                out = invoice_set.get_invoice_all_demo()
                # common.main_fun1(request.read(), path)
                jdata = out.to_json(orient='records')
                return JsonResponse(json.loads(jdata), safe=False)
            elif (action == "GET" and (
                    type == "INVOICE_MAKER_SUMMARY" or type == "INVOICE_PAYMENT" or
                    type == "ECF_TRANS_GET" or type == "AP_CREDIT_AMOUNT" or type == "AP_INVOICEHEADER_GET" or
                    type == "AP_INVOICE_PAYMENT_GET" or type == "AP_ENTER_GET" or type == "ENTRY_QUERY" or
                    type == "MAIL_STATUS" or type == "AP_PAYMENTDETAILS" or type == "PO_NOGET" or
                    type == "AP_WISEFIN_ENTER_GET" or type == "INWARD_MAKER_SUMMARY" or
                    type == "EMP_DETAILS" or type == "SUPPLIER_DETAILS" or
                    type == "CREDIT_DETAILS" or type == "WISEFIN_ENTER")):
                invoice_set.action = jsondata.get('params').get('action')
                invoice_set.type = jsondata.get('params').get('type')
                filter = jsondata.get('params').get('filter')
                invoice_set.filter = json.dumps(filter)
                invoice_set.classification = json.dumps({"Entity_Gid": int(decry_data(request.session['Entity_gid']))})
                invoice_set.create_by = int(decry_data(request.session['Emp_gid']))
                # common.main_fun1(request.read(), path)
                out = invoice_set.get_invoice_all_demo()
                jdata = out.to_json(orient='records')
                return JsonResponse(json.loads(jdata), safe=False)
        except Exception as e:
            return JsonResponse({"MESSAGE": "ERROR_OCCURED", "DATA": str(e)})


def get_Accounting_Entry_Data(request):
    utl.check_pointaccess(request)
    utl.check_authorization(request)
    if request.method == 'GET':
        try:
            invoice_set = mAP.ap_model()
            get_values = request.GET
            data = json.dumps(get_values)
            final_data = json.loads(data)
            action = final_data.get("action")
            type = final_data.get("type")
            entity_gid = int(decry_data(request.session['Entity_gid']))
            employee_gid = int(decry_data(request.session['Emp_gid']))
            if (action == "GET" and type == "ENTRY_QUERY"):
                cr_number = final_data.get("download_cr_number")
                from_date = final_data.get("download_from_date")
                to_date = final_data.get("download_to_date")
                supplier_gid = final_data.get("download_supplier_gid")
                branch_gid = final_data.get("download_branch_gid")
                if branch_gid == None:
                    branch_gid = ""
                if supplier_gid == None:
                    supplier_gid = ""
                if cr_number == None:
                    cr_number = ""
                if from_date == None:
                    from_date = ""
                if to_date == None:
                    to_date = ""
                jsondata = {'action': action,
                            'filter': {"entry_refno": cr_number, "fromdate": from_date,
                                       "todate": to_date, "supplier_gid": supplier_gid, "branch_gid": branch_gid,
                                       "Page_Index": 0, "Page_Size": 100000}, 'type': type}

                invoice_set.action = jsondata.get('action')
                invoice_set.type = jsondata.get('type')
                filter = jsondata.get('filter')
                invoice_set.filter = json.dumps(filter)
                invoice_set.classification = json.dumps({"Entity_Gid": entity_gid})
                XLSX_MIME = 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
                response = HttpResponse(content_type=XLSX_MIME)
                response['Content-Disposition'] = 'attachment; filename="Accountin_Entry_Data.xlsx"'
                writer = pd.ExcelWriter(response, engine='xlsxwriter')
                df_view = invoice_set.get_invoice_all()
                final_df = df_view[
                    ['entry_refno', 'entry_transactiondate', 'entry_gl', 'gl_name', 'entry_amt', 'entry_type',
                     'supplier_branchname', 'branch_name', 'entry_module']]
                final_df.columns = ['ENTRY_REFNO', 'ENTRY_TRANSACTION_DATE', 'ENTRY_GL', 'ENTRY_GL_NAME',
                                    'ENTRY_AMOUNT', 'ENTRY_TYPE',
                                    'SUPPLIER_NAME', 'BRANCH_NAME', 'ENTRY_MODULE']
                final_df.to_excel(writer, index=False)
                writer.save()
                return response
            elif (action == "GET" and type == "AP_REPORT"):
                txn_type = final_data.get("download_txn_type")
                download_employee_gid = final_data.get("download_employee_gid")
                txn_status = final_data.get("download_txn_status")
                from_date = final_data.get("download_from_date")
                to_date = final_data.get("download_to_date")
                supplier_gid = final_data.get("download_supplier_gid")
                branch_gid = final_data.get("download_branch_gid")

                jsondata = {'action': action, 'type': type,
                            'filter': {"InvoiceHeader_Status": txn_status, "InvoiceHeader_Gid": "",
                                       "invoiceheader_invoicetype": txn_type,
                                       "employee_gid": download_employee_gid,
                                       "fromdate": from_date, "todate": to_date, "supplier_gid": supplier_gid,
                                       "branch_gid": branch_gid, "InvoiceHeader_InvoiceDate": ""}}

                invoice_set.action = jsondata.get('action')
                invoice_set.type = jsondata.get('type')
                filter = jsondata.get('filter')
                invoice_set.filter = json.dumps(filter)
                invoice_set.classification = json.dumps({"Entity_Gid": entity_gid})
                XLSX_MIME = 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
                response = HttpResponse(content_type=XLSX_MIME)
                response['Content-Disposition'] = 'attachment; filename="GST_Report.xlsx"'
                writer = pd.ExcelWriter(response, engine='xlsxwriter')
                df_view = invoice_set.get_invoice_all()
                df_view['temp_var'] = ""
                df_view['S_No'] = range(1, 1 + len(df_view))
                final_df = df_view[
                    ['S_No', 'branch_name', 'branch_code', 'branchgst', 'supplier_code', 'supplier_branchname',
                     'supplier_gstno', 'address_1', 'address_2', 'address_3',
                     'address_pincode', 'district_name', 'City_Name',
                     'state_name', 'temp_var', 'temp_var', 'invoiceheader_invoiceno',
                     'invoiceheader_invoicedate', 'product_name', 'product_isrcm', 'product_isblocked',
                     'invoicedetails_amount', 'invoicedetails_hsncode',
                     'taxrate', 'debit_glno', 'temp_var', 'invoicedetails_qty',
                     'invoicedetails_unitprice', 'invoicedetails_cgst', 'invoicedetails_sgst', 'invoicedetails_igst',
                     'temp_var', 'invoiceheader_roundoff', 'invoiceheader_deductionamount', 'invoicedetails_totalamt',
                     'invoiceheader_crno', 'paymentheader_date', 'invoiceheader_invoicetype', 'invoicedetails_desc',
                     'invoiceheader_status', 'invoiceheader_captalisedflag', 'invoiceheader_rcmapplicable',
                     'subcategory_gstblocked',
                     'invoicedetails_cgst', 'invoicedetails_sgst', 'invoicedetails_igst', 'temp_var',
                     'expensed_cgst', 'expensed_sgst', 'expensed_igst', 'temp_var',
                     'credit_cgst', 'credit_sgst', 'credit_igst', 'temp_var',
                     'credit_suppliertaxtype', 'credit_amount', 'TAXID',
                     'credit_suppliertaxtrate', 'credit_taxableamount']]

                final_df.columns = ['S. No', 'Branch', 'Branch Code', 'Branch GST', 'Vendor Code',
                                    'Vendor Name', 'GSTIN', 'Vendor Address1', 'Vendor Address2', 'Vendor Address3',
                                    'Pincode', 'District', 'City',
                                    'State', 'Mobile', 'Email ID', 'Invoice No',
                                    'Invoice Date', 'Product Name', 'Product Is RCM', 'Product Is Blocked',
                                    'Taxable Value', 'Goods / Services HSN / SAC',
                                    'Goods/Services GST Rate', 'Goods/Services GL Code', 'Goods/Services UoM',
                                    'Goods/Services Qty',
                                    'Unit Price', 'Invoice CGST', 'Invoice SGST', 'Invoice IGST',
                                    'CESS', 'Round OFF', 'Other Deduction', 'Total Invoice Value',
                                    'EMC NO', 'PAYMENT DATE', 'Transaction Type', 'Transaction Type Description',
                                    'Transaction Status', 'Capitalisation Flag', 'RCM Applicability Tag',
                                    'Is the credit blocked',
                                    'Total Credit Available CGST', 'Total Credit Available SGST',
                                    'Total Credit Available IGST', 'Total Credit Available Total',
                                    'Credit Expensed CGST', 'Credit Expensed SGST', 'Credit Expensed IGST',
                                    'Credit Expensed Total',
                                    'Credit Available CGST', 'Credit Available SGST', 'Credit Available IGST',
                                    'Credit Available Total',
                                    'TDS Type', 'TDS Amount', 'TAXID',
                                    'Tax Rate', 'Taxable Amount']
                final_df.to_excel(writer, index=False)
                writer.save()
                return response
            elif (action == "GET" and type == "AP_NONGST"):
                txn_type = final_data.get("download_txn_type")
                download_employee_gid = final_data.get("download_employee_gid")
                txn_status = final_data.get("download_txn_status")
                from_date = final_data.get("download_from_date")
                to_date = final_data.get("download_to_date")
                supplier_gid = final_data.get("download_supplier_gid")
                branch_gid = final_data.get("download_branch_gid")

                jsondata = {'action': action, 'type': type,
                            'filter': {"InvoiceHeader_Status": txn_status, "InvoiceHeader_Gid": "",
                                       "invoiceheader_invoicetype": txn_type,
                                       "employee_gid": download_employee_gid,
                                       "fromdate": from_date, "todate": to_date, "supplier_gid": supplier_gid,
                                       "branch_gid": branch_gid, "InvoiceHeader_InvoiceDate": ""}}

                invoice_set.action = jsondata.get('action')
                invoice_set.type = jsondata.get('type')
                filter = jsondata.get('filter')
                invoice_set.filter = json.dumps(filter)
                invoice_set.classification = json.dumps({"Entity_Gid": entity_gid})
                XLSX_MIME = 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
                response = HttpResponse(content_type=XLSX_MIME)
                response['Content-Disposition'] = 'attachment; filename="NonGST_Report.xlsx"'
                writer = pd.ExcelWriter(response, engine='xlsxwriter')
                df_view = invoice_set.get_invoice_all()
                df_view['temp_var'] = ""
                df_view['S_No'] = range(1, 1 + len(df_view))
                final_df = df_view[
                    ['S_No', 'branch_name', 'branch_code', 'branchgst', 'supplier_code', 'supplier_branchname',
                     'supplier_gstno', 'address_1', 'address_2', 'address_3',
                     'address_pincode', 'district_name', 'City_Name',
                     'state_name', 'temp_var', 'temp_var', 'invoiceheader_invoiceno',
                     'invoiceheader_invoicedate', 'product_name', 'product_isrcm', 'product_isblocked',
                     'invoicedetails_amount', 'invoicedetails_hsncode',
                     'taxrate', 'debit_glno', 'temp_var', 'invoicedetails_qty',
                     'invoicedetails_unitprice', 'invoicedetails_cgst', 'invoicedetails_sgst', 'invoicedetails_igst',
                     'temp_var', 'invoiceheader_roundoff', 'invoiceheader_deductionamount', 'invoicedetails_totalamt',
                     'invoiceheader_crno', 'paymentheader_date', 'invoiceheader_invoicetype', 'invoicedetails_desc',
                     'invoiceheader_status', 'invoiceheader_captalisedflag', 'invoiceheader_rcmapplicable',
                     'subcategory_gstblocked',
                     'invoicedetails_cgst', 'invoicedetails_sgst', 'invoicedetails_igst', 'temp_var',
                     'expensed_cgst', 'expensed_sgst', 'expensed_igst', 'temp_var',
                     'credit_cgst', 'credit_sgst', 'credit_igst', 'temp_var',
                     'credit_suppliertaxtype', 'credit_amount', 'TAXID',
                     'credit_suppliertaxtrate', 'credit_taxableamount']]

                final_df.columns = ['S. No', 'Branch', 'Branch Code', 'Branch GST', 'Vendor Code',
                                    'Vendor Name', 'GSTIN', 'Vendor Address1', 'Vendor Address2', 'Vendor Address3',
                                    'Pincode', 'District', 'City',
                                    'State', 'Mobile', 'Email ID', 'Invoice No',
                                    'Invoice Date', 'Product Name', 'Product Is RCM', 'Product Is Blocked',
                                    'Taxable Value', 'Goods / Services HSN / SAC',
                                    'Goods/Services GST Rate', 'Goods/Services GL Code', 'Goods/Services UoM',
                                    'Goods/Services Qty',
                                    'Unit Price', 'Invoice CGST', 'Invoice SGST', 'Invoice IGST',
                                    'CESS', 'Round OFF', 'Other Deduction', 'Total Invoice Value',
                                    'EMC NO', 'PAYMENT DATE', 'Transaction Type', 'Transaction Type Description',
                                    'Transaction Status', 'Capitalisation Flag', 'RCM Applicability Tag',
                                    'Is the credit blocked',
                                    'Total Credit Available CGST', 'Total Credit Available SGST',
                                    'Total Credit Available IGST', 'Total Credit Available Total',
                                    'Credit Expensed CGST', 'Credit Expensed SGST', 'Credit Expensed IGST',
                                    'Credit Expensed Total',
                                    'Credit Available CGST', 'Credit Available SGST', 'Credit Available IGST',
                                    'Credit Available Total',
                                    'TDS Type', 'TDS Amount', 'TAXID',
                                    'Tax Rate', 'Taxable Amount']
                final_df.to_excel(writer, index=False)
                writer.save()
                return response

            elif (action == "GET" and type == "AP_RCM"):
                txn_type = final_data.get("download_txn_type")
                download_employee_gid = final_data.get("download_employee_gid")
                txn_status = final_data.get("download_txn_status")
                from_date = final_data.get("download_from_date")
                to_date = final_data.get("download_to_date")
                supplier_gid = final_data.get("download_supplier_gid")
                branch_gid = final_data.get("download_branch_gid")

                jsondata = {'action': action, 'type': type,
                            'filter': {"InvoiceHeader_Status": txn_status, "InvoiceHeader_Gid": "",
                                       "invoiceheader_invoicetype": txn_type,
                                       "employee_gid": download_employee_gid,
                                       "fromdate": from_date, "todate": to_date, "supplier_gid": supplier_gid,
                                       "branch_gid": branch_gid, "InvoiceHeader_InvoiceDate": ""}}

                invoice_set.action = jsondata.get('action')
                invoice_set.type = jsondata.get('type')
                filter = jsondata.get('filter')
                invoice_set.filter = json.dumps(filter)
                invoice_set.classification = json.dumps({"Entity_Gid": entity_gid})
                XLSX_MIME = 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
                response = HttpResponse(content_type=XLSX_MIME)
                response['Content-Disposition'] = 'attachment; filename="RCM_Report.xlsx"'
                writer = pd.ExcelWriter(response, engine='xlsxwriter')
                df_view = invoice_set.get_invoice_all()
                df_view['temp_var'] = ""
                df_view['S_No'] = range(1, 1 + len(df_view))
                final_df = df_view[
                    ['S_No', 'branch_name', 'branch_code', 'branchgst', 'supplier_code',
                     'supplier_branchname', 'supplier_gstno', 'address_1', 'address_2', 'address_3',
                     'address_pincode', 'district_name', 'City_Name', 'state_name',
                     'temp_var', 'temp_var', 'invoiceheader_invoiceno',
                     'invoiceheader_invoicedate', 'product_name', 'product_isrcm', 'product_isblocked',
                     'invoicedetails_amount', 'invoicedetails_hsncode',
                     'taxrate', 'debit_glno', 'temp_var', 'invoicedetails_qty',
                     'invoicedetails_unitprice', 'invoicedetails_cgst', 'invoicedetails_sgst', 'invoicedetails_igst',
                     'temp_var', 'invoiceheader_roundoff', 'invoiceheader_deductionamount', 'invoicedetails_totalamt',
                     'invoiceheader_crno', 'paymentheader_date', 'invoiceheader_invoicetype', 'invoicedetails_desc',
                     'invoiceheader_status', 'invoiceheader_captalisedflag', 'invoiceheader_rcmapplicable',
                     'subcategory_gstblocked',
                     'invoicedetails_cgst', 'invoicedetails_sgst', 'invoicedetails_igst', 'temp_var',
                     'expensed_cgst', 'expensed_sgst', 'expensed_igst', 'temp_var',
                     'credit_cgst', 'credit_sgst', 'credit_igst', 'temp_var',
                     'credit_suppliertaxtype', 'credit_amount', 'TAXID',
                     'credit_suppliertaxtrate', 'credit_taxableamount']]

                final_df.columns = ['S. No', 'Branch', 'Branch Code', 'Branch GST', 'Vendor Code',
                                    'Vendor Name', 'GSTIN', 'Vendor Address1', 'Vendor Address2', 'Vendor Address3',
                                    'Pincode', 'District', 'City', 'State',
                                    'Mobile', 'Email ID', 'Invoice No',
                                    'Invoice Date', 'Product Name', 'Product Is RCM', 'Product Is Blocked',
                                    'Taxable Value', 'Goods / Services HSN / SAC',
                                    'Goods/Services GST Rate', 'Goods/Services GL Code', 'Goods/Services UoM',
                                    'Goods/Services Qty',
                                    'Unit Price', 'Invoice CGST', 'Invoice SGST', 'Invoice IGST',
                                    'CESS', 'Round OFF', 'Other Deduction', 'Total Invoice Value',
                                    'EMC NO', 'PAYMENT DATE', 'Transaction Type', 'Transaction Type Description',
                                    'Transaction Status', 'Capitalisation Flag', 'RCM Applicability Tag',
                                    'Is the credit blocked',
                                    'Total Credit Available CGST', 'Total Credit Available SGST',
                                    'Total Credit Available IGST', 'Total Credit Available Total',
                                    'Credit Expensed CGST', 'Credit Expensed SGST', 'Credit Expensed IGST',
                                    'Credit Expensed Total',
                                    'Credit Available CGST', 'Credit Available SGST', 'Credit Available IGST',
                                    'Credit Available Total',
                                    'TDS Type', 'TDS Amount', 'TAXID',
                                    'Tax Rate', 'Taxable Amount']
                final_df.to_excel(writer, index=False)
                writer.save()
                return response

            elif (action == "GET" and type == "AP_IMPREST"):
                txn_type = final_data.get("download_txn_type")
                download_employee_gid = final_data.get("download_employee_gid")
                txn_status = final_data.get("download_txn_status")
                from_date = final_data.get("download_from_date")
                to_date = final_data.get("download_to_date")
                supplier_gid = final_data.get("download_supplier_gid")
                branch_gid = final_data.get("download_branch_gid")

                jsondata = {'action': action, 'type': type,
                            'filter': {"InvoiceHeader_Status": txn_status, "InvoiceHeader_Gid": "",
                                       "invoiceheader_invoicetype": txn_type,
                                       "employee_gid": download_employee_gid,
                                       "fromdate": from_date, "todate": to_date, "supplier_gid": supplier_gid,
                                       "branch_gid": branch_gid, "InvoiceHeader_InvoiceDate": ""}}

                invoice_set.action = jsondata.get('action')
                invoice_set.type = jsondata.get('type')
                filter = jsondata.get('filter')
                invoice_set.filter = json.dumps(filter)
                invoice_set.classification = json.dumps({"Entity_Gid": entity_gid})
                XLSX_MIME = 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
                response = HttpResponse(content_type=XLSX_MIME)
                response['Content-Disposition'] = 'attachment; filename="Imprest_Report.xlsx"'
                writer = pd.ExcelWriter(response, engine='xlsxwriter')
                df_view = invoice_set.get_invoice_all()
                df_view['temp_var'] = ""
                df_view['S_No'] = range(1, 1 + len(df_view))
                final_df = df_view[
                    ['S_No', 'branch_name', 'branch_code', 'branchgst', 'supplier_code', 'supplier_branchname',
                     'supplier_gstno', 'temp_var', 'temp_var',
                     'temp_var', 'temp_var', 'temp_var', 'invoiceheader_invoiceno',
                     'invoiceheader_invoicedate', 'invoicedetails_item', 'invoicedetails_amount',
                     'invoicedetails_hsncode',
                     'taxrate', 'debit_glno', 'temp_var', 'invoicedetails_qty',
                     'invoicedetails_unitprice', 'invoicedetails_cgst', 'invoicedetails_sgst', 'invoicedetails_igst',
                     'temp_var', 'invoiceheader_roundoff', 'invoiceheader_deductionamount', 'invoicedetails_totalamt',
                     'invoiceheader_crno', 'paymentheader_date', 'invoiceheader_invoicetype', 'invoicedetails_desc',
                     'invoiceheader_status', 'invoiceheader_captalisedflag', 'invoiceheader_rcmapplicable',
                     'subcategory_gstblocked',
                     'invoicedetails_cgst', 'invoicedetails_sgst', 'invoicedetails_igst', 'temp_var',
                     'expensed_cgst', 'expensed_sgst', 'expensed_igst', 'temp_var',
                     'credit_cgst', 'credit_sgst', 'credit_igst', 'temp_var',
                     'TAXID']]

                final_df.columns = ['S. No', 'Branch', 'Branch Code', 'Branch GST', 'Vendor Code',
                                    'Vendor Name', 'GSTIN', 'Vendor Address', 'Pincode',
                                    'State', 'Mobile', 'Email ID', 'Invoice No',
                                    'Invoice Date', 'Product Name', 'Taxable Value', 'Goods / Services HSN / SAC',
                                    'Goods/Services GST Rate', 'Goods/Services GL Code', 'Goods/Services UoM',
                                    'Goods/Services Qty',
                                    'Unit Price', 'Invoice CGST', 'Invoice SGST', 'Invoice IGST',
                                    'CESS', 'Round OFF', 'Other Deduction', 'Total Invoice Value',
                                    'EMC NO', 'PAYMENT DATE', 'Transaction Type', 'Transaction Type Description',
                                    'Transaction Status', 'Capitalisation Flag', 'RCM Applicability Tag',
                                    'Is the credit blocked',
                                    'Total Credit Available CGST', 'Total Credit Available SGST',
                                    'Total Credit Available IGST', 'Total Credit Available Total',
                                    'Credit Expensed CGST', 'Credit Expensed SGST', 'Credit Expensed IGST',
                                    'Credit Expensed Total',
                                    'Credit Available CGST', 'Credit Available SGST', 'Credit Available IGST',
                                    'Credit Available Total',
                                    'TAXID']
                final_df.to_excel(writer, index=False)
                writer.save()
                return response
            elif (action == "GET" and type == "AP_CREDITREPORT"):
                txn_type = final_data.get("download_txn_type")
                download_employee_gid = final_data.get("download_employee_gid")
                txn_status = final_data.get("download_txn_status")
                from_date = final_data.get("download_from_date")
                to_date = final_data.get("download_to_date")
                supplier_gid = final_data.get("download_supplier_gid")
                branch_gid = final_data.get("download_branch_gid")

                jsondata = {'action': action, 'type': type,
                            'filter': {"InvoiceHeader_Status": txn_status, "InvoiceHeader_Gid": "",
                                       "invoiceheader_invoicetype": txn_type,
                                       "employee_gid": download_employee_gid,
                                       "fromdate": from_date, "todate": to_date, "supplier_gid": supplier_gid,
                                       "branch_gid": branch_gid, "InvoiceHeader_InvoiceDate": ""}}

                invoice_set.action = jsondata.get('action')
                invoice_set.type = jsondata.get('type')
                filter = jsondata.get('filter')
                invoice_set.filter = json.dumps(filter)
                invoice_set.classification = json.dumps({"Entity_Gid": entity_gid})
                XLSX_MIME = 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
                response = HttpResponse(content_type=XLSX_MIME)
                response['Content-Disposition'] = 'attachment; filename="Credit_Rport.xlsx"'
                writer = pd.ExcelWriter(response, engine='xlsxwriter')
                df_view = invoice_set.get_invoice_all()
                final_df = df_view[
                    ['invoiceheader_crno', 'invoiceheader_invoicetype', 'invoiceheader_status', 'employee_name',
                     'paymentheader_pvno', 'paymentheader_date', 'paymentdetails_amount', 'paymode_name',
                     'invoiceheader_invoiceno', 'invoiceheader_invoicedate', 'supplier_name', 'supplier_code',
                     'supplier_branchname',
                     'credit_amount', 'credit_suppliertaxtype', 'credit_suppliertaxtrate']]

                final_df.columns = ['EMC NO', 'Transaction Type', 'Transaction Status', 'Raiser Name',
                                    'Payment ID', 'Payment Date', 'Payment Amount', 'Payment Mode',
                                    'Invoice No', 'Invoice Date', 'Vendor Name', 'Vendor Code', 'Vendor Branch Name',
                                    'TDS Amount', 'TDS Section', 'TDS Rate']
                final_df.to_excel(writer, index=False)
                writer.save()
                return response
            elif (action == "GET" and type == "AP_INVOICEHEADER_GET"):
                InvoiceHeader_CRNo = final_data.get("invoiceheader_crno")
                InvoiceHeader_Type_temp = final_data.get("selectedtype")
                res = json.loads(InvoiceHeader_Type_temp)
                InvoiceHeader_Type = ','.join(map(str, res))
                supplier_name = final_data.get("supplier_name")
                invoiceheader_branchgid = final_data.get("branch_gid")
                InvoiceHeader_InvoiceNo = final_data.get("invoicenum")
                InvoiceHeader_Amount = final_data.get("invoiceamt")
                InvoiceHeader_Status_Temp = final_data.get("status")
                InvoiceHeader_temp_staus = json.loads(InvoiceHeader_Status_Temp)
                InvoiceHeader_Status = ','.join(map(str, InvoiceHeader_temp_staus))

                fromdate = final_data.get("from_date")
                todate = final_data.get("to_date")

                jsondata = {'action': action, 'type': type,
                            'filter': {"InvoiceHeader_Status": InvoiceHeader_Status,
                                       "InvoiceHeader_Gid": "",
                                       "InvoiceHeader_InvoiceType": InvoiceHeader_Type,
                                       "InvoiceHeader_InvoiceDate": "",
                                       "fromdate": fromdate, "todate": todate,
                                       "invoiceheader_branchgid": invoiceheader_branchgid,
                                       "InvoiceHeader_CRNo": InvoiceHeader_CRNo,
                                       "InvoiceHeader_InvoiceNo": InvoiceHeader_InvoiceNo,
                                       "InvoiceHeader_Amount": InvoiceHeader_Amount,
                                       "Supplier_Name": supplier_name}}

                invoice_set.action = jsondata.get('action')
                invoice_set.type = jsondata.get('type')
                filter = jsondata.get('filter')
                invoice_set.filter = json.dumps(filter)
                invoice_set.classification = json.dumps({"Entity_Gid": entity_gid})
                XLSX_MIME = 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
                response = HttpResponse(content_type=XLSX_MIME)
                response['Content-Disposition'] = 'attachment; filename="Rport.xlsx"'
                writer = pd.ExcelWriter(response, engine='xlsxwriter')
                df_view = invoice_set.get_invoice_all()
                final_df = df_view[['invoiceheader_crno', 'invoiceheader_invoicetype',
                                    'invoiceheader_gst', 'invoiceheader_invoicedate',
                                    'invoiceheader_invoiceno', 'invoiceheader_dedupeinvoiceno',
                                    'invoiceheader_taxableamt', 'invoiceheader_otheramount',
                                    'invoiceheader_amount', 'invoiceheader_roundoff',
                                    'invoiceheader_captalisedflag', 'invoiceheader_remarks',
                                    'supplier_gstno', 'invoiceheader_status',
                                    'invoiceheader_onwardinvoice', 'invoiceheader_amortinvoice',
                                    'invoiceheader_barcode',
                                    'invoiceheader_rmubarcode', 'invoiceheader_dueadjustment',
                                    'invoiceheader_ppx',
                                    'invoiceheader_rcmapplicable', 'supplier_branchname',
                                    'Supplier_code', 'employee_name', 'employee_code',
                                    'designation_name']]

                final_df.columns = ['CR Number', 'Invoice Type',
                                    'GST', 'Invoice Date',
                                    'Invoice Number', 'Invoice Dedupe Number',
                                    'Taxable Amount', 'Other Amount',
                                    'Invoice Header Amount', 'Roundoff',
                                    'Captalised Flag', 'Remark',
                                    'Supplier GST Number', 'Invoice Status',
                                    'Onwardinvoice', 'Amort Invoice',
                                    'Invoice Barcode',
                                    'Invoice RMU Barcode', 'Due Adjustment',
                                    'Invoice PPX',
                                    'RCM Applicable', 'Supplier Name',
                                    'Supplier Code', 'Employee Name', 'Employee Code',
                                    'Designation']
                final_df.to_excel(writer, index=False)
                writer.save()
                return response
            elif (action == "GET" and type == "ECF_HEADER_BY_BRANCH"):
                InvoiceHeader_CRNo = final_data.get("invoiceheader_crno")
                InvoiceHeader_Type = final_data.get("invoice_type")
                supplier_name = final_data.get("supplier_name")
                invoiceheader_branchgid = request.session['Branch_gid']
                invoiceheader_Employee_gid = final_data.get("employee_gid")
                InvoiceHeader_InvoiceNo = final_data.get("invoice_number")
                InvoiceHeader_AP_Status = final_data.get("ap_status")
                InvoiceHeader_ECF_Status = final_data.get("ecf_status")
                InvoiceHeader_Min_Amt = final_data.get("min_amount")
                InvoiceHeader_Max_Amt = final_data.get("max_amount")
                fromdate = final_data.get("from_date")
                todate = final_data.get("to_date")

                jsondata = {'action': action, 'type': type,
                            'filter': {"ecf_number": InvoiceHeader_CRNo,
                                       "invoiceheader_invoicetype": InvoiceHeader_Type,
                                       "employee_name": invoiceheader_Employee_gid,
                                       "invoiceheader_invoiceno": InvoiceHeader_InvoiceNo,
                                       "ap_status": InvoiceHeader_AP_Status,
                                       "ecf_status": InvoiceHeader_ECF_Status, "supplier_name": supplier_name,
                                       "branch_gid": invoiceheader_branchgid,
                                       "from_date": fromdate, "to_date": todate, "min_amount": InvoiceHeader_Min_Amt,
                                       "max_amount": InvoiceHeader_Max_Amt}}

                invoice_set.action = jsondata.get('action')
                invoice_set.type = jsondata.get('type')
                filter = jsondata.get('filter')
                invoice_set.filter = json.dumps(filter)
                invoice_set.classification = json.dumps({"Entity_Gid": entity_gid})
                XLSX_MIME = 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
                response = HttpResponse(content_type=XLSX_MIME)
                response['Content-Disposition'] = 'attachment; filename="ECF Report.xlsx"'
                writer = pd.ExcelWriter(response, engine='xlsxwriter')
                df_view = invoice_set.get_ecf_details()
                final_df = df_view[['invoiceheader_crno', 'invoiceheader_invoicetype',
                                    'invoiceheader_invoicedate',
                                    'invoiceheader_invoiceno', 'invoiceheader_amount',
                                    'ecf_status', 'ap_status'
                                    ]]

                final_df.columns = ['CR Number', 'Invoice Type',
                                    'Invoice Date',
                                    'Invoice Number', 'Invoice Header Amount',
                                    'ECF Status', 'AP Status'
                                    ]
                final_df.to_excel(writer, index=False)
                writer.save()
                return response
            elif (action == "GET" and type == "INVOICE_MAKER_SUMMARY"):
                InvoiceHeader_CRNo = final_data.get("invoiceheader_crno")
                InvoiceHeader_Type = final_data.get("invoice_type")
                supplier_name = final_data.get("supplier_name")
                InvoiceHeader_InvoiceNo = final_data.get("invoice_number")
                InvoiceHeader_Status = final_data.get("invoice_status")
                InvoiceHeader_Min_Amt = final_data.get("min_amount")
                InvoiceHeader_Max_Amt = final_data.get("max_amount")
                fromdate = final_data.get("from_date")
                todate = final_data.get("to_date")
                employee_gid = int(decry_data(request.session['Emp_gid']))

                jsondata = {'action': action, 'type': type,
                            'filter': {"ecf_number": InvoiceHeader_CRNo, "invoice_type": InvoiceHeader_Type,
                                       "employee_gid": employee_gid,
                                       "supplier_name": supplier_name, "invoice_number": InvoiceHeader_InvoiceNo,
                                       "from_date": fromdate, "to_date": todate, "min_amount": InvoiceHeader_Min_Amt,
                                       "max_amount": InvoiceHeader_Max_Amt,
                                       "invoiceheader_status": InvoiceHeader_Status}}

                invoice_set.action = jsondata.get('action')
                invoice_set.type = jsondata.get('type')
                filter = jsondata.get('filter')
                invoice_set.filter = json.dumps(filter)
                invoice_set.classification = json.dumps({"Entity_Gid": entity_gid})
                XLSX_MIME = 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
                response = HttpResponse(content_type=XLSX_MIME)
                response['Content-Disposition'] = 'attachment; filename="ECF Report.xlsx"'
                writer = pd.ExcelWriter(response, engine='xlsxwriter')
                df_view = invoice_set.get_ecf_details()
                final_df = df_view[['invoiceheader_crno', 'invoiceheader_invoicetype',
                                    'invoiceheader_invoiceno', 'invoiceheader_invoicedate_full',
                                    'invoiceheader_otheramount', 'invoiceheader_amount',
                                    'invoiceheader_status', 'IS_GST', 'invoiceheader_remarks']]

                final_df.columns = ['CR Number', 'Invoice Type',
                                    'Invoice Number', 'Invoice Date',
                                    'Invoice Other Amount', "Invoice Header Amount",
                                    'Invoice Status', 'IS GST', "Invoice Remarks"
                                    ]
                final_df.to_excel(writer, index=False)
                writer.save()
                return response
            elif (action == "GET" and type == "AP_TDS"):
                jsondata = {'action': action, 'type': type,
                            'filter': {}}

                invoice_set.action = jsondata.get('action')
                invoice_set.type = jsondata.get('type')

                txn_type = final_data.get("download_txn_type")
                download_employee_gid = final_data.get("download_employee_gid")
                txn_status = final_data.get("download_txn_status")
                from_date = final_data.get("download_from_date")
                to_date = final_data.get("download_to_date")
                supplier_gid = final_data.get("download_supplier_gid")
                branch_gid = final_data.get("download_branch_gid")

                filter = {"InvoiceHeader_Status": txn_status, "InvoiceHeader_Gid": "",
                          "invoiceheader_invoicetype": txn_type,
                          "employee_gid": download_employee_gid, "fromdate": from_date, "todate": to_date,
                          "supplier_gid": supplier_gid, "branch_gid": branch_gid, "InvoiceHeader_InvoiceDate": ""}
                invoice_set.filter = json.dumps(filter)
                invoice_set.classification = json.dumps({"Entity_Gid": entity_gid})
                XLSX_MIME = 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
                response = HttpResponse(content_type=XLSX_MIME)
                response['Content-Disposition'] = 'attachment; filename="TDS_Rport.xlsx"'
                writer = pd.ExcelWriter(response, engine='xlsxwriter')
                df_view = invoice_set.get_invoice_all()
                df_view['null_values'] = ""
                df_view['S_No'] = range(1, 1 + len(df_view))
                final_df = df_view[['S_No', 'Deductor TAN', 'Deductor PAN', 'Deductor NAME', 'branch_code',
                                    'company', 'supplier_panno', 'supplier_branchname', 'address_1', 'address_2',
                                    'address_3', 'credit_taxableamount', 'paymentheader_date',
                                    'paymentheader_date', 'credit_suppliertaxtype', 'credit_suppliertaxtrate',
                                    'credit_amount', 'null_values', 'null_values', 'null_values',
                                    'credit_tdsexcempted', 'null_values',
                                    'invoiceheader_taxableamt', 'invoiceheader_invoiceno',
                                    'invoiceheader_crno', 'paymentdetails_amount']]
                final_df.columns = ['S.No', 'Deductor TAN', 'Deductor PAN', 'Deductor Name', 'Deductor branch',
                                    'Deductee Code', 'PAN', 'Vendor Name', 'Address 1', 'Address 2',
                                    'Address 3', 'TDS Base Amount', 'Date of deduction',
                                    'Date of Payment', 'Section', 'Rate at which TDS deducted  (including LDC Rate)',
                                    'TDS Amount', 'Surcharge', 'Edu cess', 'HEC',
                                    'LDC/Lower deduction certificate', 'Reason for Non-deduction / Lower Deduction',
                                    'Invoice Taxable Amount', 'Invoice Number',
                                    'Invoice CR Number', 'Amount Paid']
                final_df.to_excel(writer, index=False)
                writer.save()
                return response

            elif (action == "GET" and type == "WISEFIN_ENTER"):
                jsondata = {'action': action, 'type': type,
                            'filter': {}}

                invoice_set.action = jsondata.get('action')
                invoice_set.type = jsondata.get('type')
                gl_number = final_data.get("download_gl_number")
                branch_gid = final_data.get("download_branch_gid")

                filter = {"branch_gid": branch_gid, "gl_number": gl_number}
                invoice_set.filter = json.dumps(filter)
                invoice_set.classification = json.dumps({"Entity_Gid": entity_gid})
                XLSX_MIME = 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
                response = HttpResponse(content_type=XLSX_MIME)
                response['Content-Disposition'] = 'attachment; filename="WiseFin_Entry_Rport.xlsx"'
                writer = pd.ExcelWriter(response, engine='xlsxwriter')
                df_view = invoice_set.get_invoice_all()
                df_view['null_values'] = ""
                df_view['S_No'] = range(1, 1 + len(df_view))
                final_df = df_view[['S_No', 'bigfentry_fiscalyear', 'bigfentry_module', 'bigfentry_gl',
                                    'entry_type', 'bigfentry_amt']]
                final_df.columns = ['S.No', 'Financial Year', 'Entry Module', 'Entry GL',
                                    'D/C', 'Amount']
                final_df.to_excel(writer, index=False)
                writer.save()
                return response

            elif (action == "GET" and type == "AP_DAILY_GL_REPORT"):
                invoice_set.action = final_data.get('action')
                invoice_set.type = final_data.get('type')
                gl_type_name = final_data.get("gl_type_name")
                branch_gid = final_data.get("branch_gid")
                from_date = final_data.get("download_from_date")
                to_date = final_data.get("download_to_date")
                filter = {"fromdate": from_date, "todate": to_date, "branch_gid": branch_gid,
                          "gl_type_name": gl_type_name}
                invoice_set.filter = json.dumps(filter)
                invoice_set.classification = json.dumps({"Entity_Gid": entity_gid})
                XLSX_MIME = 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
                response = HttpResponse(content_type=XLSX_MIME)
                response['Content-Disposition'] = 'attachment; filename="Daily_GL_Report.xlsx"'
                writer = pd.ExcelWriter(response, engine='xlsxwriter')
                df_view = invoice_set.get_gl_report()
                df_view['null_values'] = ""
                df_view['S_No'] = range(1, 1 + len(df_view))
                final_df = df_view[['S_No', 'branch_name', 'branch_code', 'dayentry_gl', 'dayentry_transactiondate',
                                    'dayentry_debitamt', 'dayentry_creditamt', 'dayentry_openingbalc',
                                    'dayentry_closingbalc']]
                final_df.columns = ['S.No', 'Branch Name', 'Branch Code', 'GL Number', 'Date',
                                    'Debit Amount', 'Credit Amount', 'Opening  Balance', 'Closing Balance']
                final_df.to_excel(writer, index=False)
                writer.save()
                return response
            elif (action == "ADVANCE" and type == "PPX"):
                invoice_set.action = final_data.get('action')
                invoice_set.type = final_data.get('type')
                Type_ = final_data.get("Type_")
                Employee_gid = final_data.get("Employee_gid")
                Supplier_gid = final_data.get("Supplier_gid")
                Branch_gid = final_data.get("Branch_gid")
                filter = {"Type_": Type_, "Employee_gid": Employee_gid, "Supplier_gid": Supplier_gid,
                          "Branch_gid": Branch_gid}
                invoice_set.filter = json.dumps(filter)
                invoice_set.classification = json.dumps({"Entity_Gid": entity_gid})
                XLSX_MIME = 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
                response = HttpResponse(content_type=XLSX_MIME)
                response['Content-Disposition'] = 'attachment; filename="Advance_Report.xlsx"'
                writer = pd.ExcelWriter(response, engine='xlsxwriter')
                df_view = invoice_set.get_advance_details()
                df_view['null_values'] = ""
                df_view['S_No'] = range(1, 1 + len(df_view))
                final_df = df_view[
                    ['S_No', 'invoiceheader_crno', 'branch_name', 'branch_code', 'supplier_name', 'supplier_code',
                     'invoiceheader_ponumber',
                     'ppxheader_amount', 'ppxheader_balance', 'ppxheader_date', 'debit_glno', 'Advance_By',
                     'invoiceheader_remarks']]
                final_df.columns = ['S.No', 'Invoice Header CRNO', 'Branch Name', 'Branch Code', 'Supplier Name',
                                    'Supplier Code', 'PO Number',
                                    'PPX Header Amount', 'PPX Header Balance', 'PPX Header Date', 'Debit GL No',
                                    'Advance By', 'Remark']
                final_df.to_excel(writer, index=False)
                writer.save()
                return response
            elif (action == "GET" and type == "AP_TRANSACTION_GL_REPORT"):
                invoice_set.action = final_data.get('action')
                invoice_set.type = final_data.get('type')
                gl_number = final_data.get("gl_number")
                branch_gid = final_data.get("branch_gid")
                from_date = final_data.get("download_from_date")
                to_date = final_data.get("download_to_date")
                filter = {"fromdate": from_date, "todate": to_date, "gl_number": gl_number, "branch_gid": branch_gid}
                invoice_set.filter = json.dumps(filter)
                invoice_set.classification = json.dumps({"Entity_Gid": entity_gid})
                XLSX_MIME = 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
                response = HttpResponse(content_type=XLSX_MIME)
                response['Content-Disposition'] = 'attachment; filename="Transaction_Report.xlsx"'
                writer = pd.ExcelWriter(response, engine='xlsxwriter')
                df_view = invoice_set.get_gl_report()
                json_data = df_view.to_json(orient='records')
                json_data = json.loads(json_data)
                opeing_balance = json_data[0].get("opening")
                lenth_of_list = len(json_data)
                closing_balance = json_data[lenth_of_list - 1].get("closing")
                gl_header = "GL STATEMENT - " + str(gl_number)
                peroid_from_to_date = "PERIOD FROM " + str(from_date) + " TO " + str(to_date)
                df1 = pd.DataFrame(
                    {
                        gl_header: [peroid_from_to_date, "Opening Balance", "Closing Balance"],
                        "": ["", opeing_balance, closing_balance]
                    }, index=["", "", ""],
                )
                # final = pd.concat([df4, final_df], axis=1)
                # final = df4.append(final_df)
                # final.to_excel(writer, index=False)
                # writer.save()
                # return response
                df1.to_excel(writer, sheet_name='Sheet1', startcol=-1)  # Default position, cell A1.
                df_view['null_values'] = ""
                df_view['AC_CCY'] = "INR"
                df_view['S_No'] = range(1, 1 + len(df_view))
                df_view.loc[df_view['entry_type'] == 1, 'entry_type'] = "D"
                df_view.loc[df_view['entry_type'] == 2, 'entry_type'] = "C"

                final_df = df_view[['S_No', 'branch_code', 'branch_name', 'entry_transactiondate',
                                    'entry_glremarks', 'entry_type', 'AC_CCY', 'entry_amt', 'closing']]
                final_df.columns = ['S.No', 'BRANCH CODE', 'BRANCH_NAME', 'DATE',
                                    'NARRATION', 'DR/CR', 'CCY', 'EQ LCY AMOUNT', 'RUNNING BALANCE']
                final_df.to_excel(writer, sheet_name='Sheet1', startcol=-1, startrow=5)
                writer.save()
                return response

        except Exception as e:
            return JsonResponse({"MESSAGE": "ERROR_OCCURED", "DATA": str(e)})


def ecf_common_report(request):
    utl.check_pointaccess(request)
    utl.check_authorization(request)
    if request.method == 'GET':
        try:
            invoice_set = mAP.ap_model()
            get_values = request.GET
            data = json.dumps(get_values)
            final_data = json.loads(data)
            action = final_data.get("action")
            type = final_data.get("type")
            ap_status = final_data.get("ap_status")
            ecf_status = final_data.get("ecf_status")

            send_file_name = 'attachment; filename="Status_Report.xlsx"'
            entity_gid = int(decry_data(request.session['Entity_gid']))
            employee_gid = int(decry_data(request.session['Emp_gid']))
            Branch_Gid = request.session['Branch_gid']
            if (action == "GET" and type == "ECF_STATUS"):
                filter = {"ecf_number": "", "invoiceheader_invoicetype": "", "employee_name": "",
                          "invoiceheader_invoiceno": "", "ap_status": ap_status,
                          "ecf_status": ecf_status, "supplier_name": " ", "branch_gid": Branch_Gid, "from_date": "",
                          "to_date": "", "min_amount": "", "max_amount": ""}
                invoice_set.action = action
                invoice_set.type = "ECF_Report"
                invoice_set.filter = json.dumps(filter)
                invoice_set.classification = json.dumps({"Entity_Gid": entity_gid})
                XLSX_MIME = 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
                response = HttpResponse(content_type=XLSX_MIME)
                response['Content-Disposition'] = send_file_name
                writer = pd.ExcelWriter(response, engine='xlsxwriter')
                df_view = invoice_set.get_ecf_details()
                final_df = df_view[
                    ['invoiceheader_crno', 'invoiceheader_invoicetype', 'supplier_name', 'invoiceheader_invoiceno',
                     'invoiceheader_amount', 'invoiceheader_taxableamt', 'ecf_status', 'ap_status']]
                final_df.columns = ['CR Number', 'Invoice Type', 'Supplier Name', 'Invoice Number',
                                    'Invoice Header Amount', 'Invoice Taxable Amount', 'ECF Status', 'AP Status']
                final_df.to_excel(writer, index=False)
                writer.save()
                return response
        except Exception as e:
            return JsonResponse({"MESSAGE": "ERROR_OCCURED", "DATA": str(e)})


def getDedubeData(request):
    utl.check_pointaccess(request)
    utl.check_authorization(request)
    if request.method == 'POST':
        try:
            path = request.path
            dedube_get = mAP.ap_model()
            jsondata = json.loads(request.body.decode('utf-8'))
            action = jsondata.get('params').get('action')
            type = jsondata.get('params').get('type')
            if (action == "GET" and type == "DEDUBE_INVOICE_HEADER"):
                dedube_get.action = action
                dedube_get.type = type
                dedube_get.filter = json.dumps(jsondata.get('params').get('filter'))
                dedube_get.classification = json.dumps({"Entity_Gid": int(decry_data(request.session['Entity_gid']))})
                dedube_get.create_by = int(decry_data(request.session['Emp_gid']))
                common.main_fun1(request.read(), path)
                output = dedube_get.get_dedube_details()
                return JsonResponse(output, safe=False)
        except Exception as e:
            return JsonResponse({"MESSAGE": "ERROR_OCCURED", "DATA": str(e)})


def get_GL_Report(request):
    utl.check_pointaccess(request)
    utl.check_authorization(request)
    if request.method == 'POST':
        try:
            path = request.path
            dedube_get = mAP.ap_model()
            jsondata = json.loads(request.body.decode('utf-8'))
            action = jsondata.get('action')
            type = jsondata.get('type')
            if (action == "GET" and (type == "AP_TRANSACTION_GL_REPORT" or type == "AP_DAILY_GL_REPORT")):
                dedube_get.action = action
                dedube_get.type = type
                dedube_get.filter = json.dumps(jsondata.get('filter'))
                dedube_get.classification = json.dumps({"Entity_Gid": int(decry_data(request.session['Entity_gid']))})
                dedube_get.create_by = int(decry_data(request.session['Emp_gid']))
                common.main_fun1(request.read(), path)
                output = dedube_get.get_gl_report()
                jdata = output.to_json(orient='records')
                return JsonResponse(json.loads(jdata), safe=False)
        except Exception as e:
            return JsonResponse({"MESSAGE": "ERROR_OCCURED", "DATA": str(e)})


def set_Ammort(request):
    utl.check_pointaccess(request)
    utl.check_authorization(request)
    if request.method == 'POST':
        try:
            path = request.path
            ammort_set = mAP.ap_model()
            jsondata = json.loads(request.body.decode('utf-8'))
            action = jsondata.get('params').get('action')
            type = jsondata.get('params').get('type')
            if (action == "INSERT" and type == "AMMORT_SCHEDULE_SET"):
                ammort_set.action = action
                ammort_set.type = type
                ammort_set.filter = json.dumps(jsondata.get('params').get('filter'))
                ammort_set.classification = json.dumps({"Entity_Gid": int(decry_data(request.session['Entity_gid']))})
                ammort_set.create_by = int(decry_data(request.session['Emp_gid']))
                common.main_fun1(request.read(), path)
                output = ammort_set.set_ammort_details()
                return HttpResponse(output)
        except Exception as e:
            return JsonResponse({"MESSAGE": "ERROR_OCCURED", "DATA": str(e)})


def AP_History_get(request):
    utl.check_pointaccess(request)
    utl.check_authorization(request)
    if request.method == 'POST':
        try:
            path = request.path
            history = mAP.ap_model()
            jsondata = json.loads(request.body.decode('utf-8'))
            history.group = jsondata.get('params').get('group')
            history.type = jsondata.get('params').get('type')
            history.entity_gid = int(decry_data(request.session['Entity_gid']))
            history.refvalue = jsondata.get('params').get('refvalue')
            common.main_fun1(request.read(), path)
            out = history.History_get()
            jdata = out.to_json(orient='records')
            return JsonResponse(jdata, safe=False)
        except Exception as e:
            return JsonResponse({"MESSAGE": "ERROR_OCCURED", "DATA": str(e)})


def AP_status_update(data):
    Status = data.get("Status")
    file_data = data.get("file_data")
    try:
        inward_dtl = mAP.ap_model()
        inward_dtl.action = "UPDATE"
        inward_dtl.type = "STATUS"
        inward_dtl.header_json = '{}'
        inward_dtl.debit_json = '{}'
        inward_dtl.detail_json = '{}'
        inward_dtl.entity_gid = data.get("entity_gid")
        inward_dtl.employee_gid = data.get("employee_gid")
        if (
                Status == "AP INITIATED" or Status == "PAY INITIATED" or Status == "NEFT INITIATED" or Status == "DD INITIATED" or Status == "TRANSACTION INITIATED"):
            Invoice_Header_Gid = data.get("Invoice_Header_Gid")
            inward_dtl.status_json = {"Invoice_Header_Gid": Invoice_Header_Gid, "Status": Status,
                                      "file_data": file_data}
            final_out = outputSplit(inward_dtl.set_Invoiceheader_status_update(), 1)
            return final_out
    except Exception as e:
        common.logger.error(e)
        return JsonResponse({"MESSAGE": "ERROR_OCCURED_ON" + " " + Status + " " + "STATUS_UPDATE", "DATA": str(e)})


def AP_Header_Update(data):
    try:
        entity_gid = data.get("entity_gid")
        employee_gid = data.get("employee_gid")
        type = data.get("type")
        inward_dtl = mAP.ap_model()
        inward_dtl.action = "UPDATE"
        inward_dtl.type = type
        inward_dtl.header_json = {"HEADER": [data]}
        inward_dtl.debit_json = {}
        inward_dtl.detail_json = {}
        inward_dtl.status_json = {}
        inward_dtl.entity_gid = entity_gid
        inward_dtl.employee_gid = employee_gid
        outs = outputSplit(inward_dtl.set_Invoiceheader(), 1)
        return outs
    except Exception as e:
        common.logger.error(e)
        return JsonResponse({"MESSAGE": "ERROR_OCCURED_ON_INVOICE_HEADER_UPDATE", "DATA": str(e)})


def Dynamic_Status_Update(request):
    utl.check_pointaccess(request)
    utl.check_authorization(request)
    if request.method == 'POST':
        try:
            path = request.path
            inward_dtl = mAP.ap_model()
            jsondata = json.loads(request.body.decode('utf-8'))
            if (jsondata.get('params').get('action') == 'UPDATE'):
                inward_dtl.action = jsondata.get('params').get('action')
                inward_dtl.type = jsondata.get('params').get('type')
                inward_dtl.header_json = jsondata.get('params').get('header_json')
                inward_dtl.debit_json = jsondata.get('params').get('debit_json')
                inward_dtl.detail_json = jsondata.get('params').get('detail_json')
                inward_dtl.status_json = jsondata.get('params').get('status_json')
                inward_dtl.entity_gid = int(decry_data(request.session['Entity_gid']))
                inward_dtl.employee_gid = int(decry_data(request.session['Emp_gid']))
                common.main_fun1(request.read(), path)
                out = outputSplit(inward_dtl.set_Invoiceheader_status_update(), 1)
                return JsonResponse(out, safe=False)
        except Exception as e:
            return JsonResponse({"MESSAGE": "ERROR_OCCURED", "DATA": str(e)})


def Dynamic_Invoiceheader_set(request):
    utl.check_pointaccess(request)
    utl.check_authorization(request)
    if request.method == 'POST':
        try:
            path = request.path
            inward_dtl = mAP.ap_model()
            jsondata = json.loads(request.body.decode('utf-8'))
            inward_dtl.action = jsondata.get('params').get('action')
            inward_dtl.type = jsondata.get('params').get('type')
            inward_dtl.header_json = jsondata.get('params').get('header_json')
            inward_dtl.debit_json = jsondata.get('params').get('debit_json')
            inward_dtl.detail_json = jsondata.get('params').get('detail_json')
            inward_dtl.status_json = jsondata.get('params').get('status_json')
            inward_dtl.entity_gid = int(decry_data(request.session['Entity_gid']))
            inward_dtl.employee_gid = int(decry_data(request.session['Emp_gid']))
            common.main_fun1(request.read(), path)
            final_out = outputSplit(inward_dtl.set_Invoiceheader(), 1)
            return JsonResponse(final_out, safe=False)
        except Exception as e:
            return JsonResponse({"MESSAGE": "ERROR_OCCURED", "DATA": str(e)})


import logging
import threading
import time
import subprocess
import sys


def Invoiceheader_set(request):
    jsondata = json.loads(request.body.decode('utf-8'))
    Status = jsondata.get('params').get('status_json').get('Status')
    Is_approve_and_pay = jsondata.get('params').get('status_json').get('Is_approve_and_pay')
    if (Status == 'APPROVED' and Is_approve_and_pay == 'Y'):
        # output = subprocess.Popen([sys.executable, Invoiceheader_set1(request)],shell=True,
        #                  stdout=subprocess.PIPE,
        #                  stderr=subprocess.STDOUT)
        # pid_ = output.pid
        # print("pid",pid_)
        # jsonS,_ = output.communicate()
        # d = json.loads(jsonS)
        # return JsonResponse(d)
        # print(threading.get_ident())
        x = threading.Thread(target=approve_and_pay(request), args=(1,))
        pass
        x.start()
        # invoice_header_gid = jsondata.get('params').get('status_json').get('Invoice_Header_Gid')
        # entity_gid = int(decry_data(request.session['Entity_gid']))
        # employee_gid = int(decry_data(request.session['Emp_gid']))
        # status_update_data = {"Invoice_Header_Gid": invoice_header_gid, "entity_gid": entity_gid,"employee_gid": employee_gid, "Status": "TRANSACTION INITIATED"}
        # ap_status_update_result = AP_status_update(status_update_data)
    else:
        return Invoiceheader_set1(request)


def Invoiceheader_set1(request):
    utl.check_pointaccess(request)
    utl.check_authorization(request)
    if request.method == 'POST':
        try:
            path = request.path
            inward_dtl = mAP.ap_model()
            jsondata = json.loads(request.body.decode('utf-8'))
            if (jsondata.get('params').get('status_json').get('Status') != 'APPROVED'):
                try:
                    inward_dtl.action = jsondata.get('params').get('action')
                    inward_dtl.type = jsondata.get('params').get('type')
                    inward_dtl.header_json = jsondata.get('params').get('header_json')
                    inward_dtl.debit_json = jsondata.get('params').get('debit_json')
                    inward_dtl.detail_json = jsondata.get('params').get('detail_json')
                    inward_dtl.status_json = jsondata.get('params').get('status_json')
                    inward_dtl.entity_gid = int(decry_data(request.session['Entity_gid']))
                    inward_dtl.employee_gid = int(decry_data(request.session['Emp_gid']))
                    common.main_fun1(request.read(), path)
                    out = ""
                    result_data = ""
                    header_gid = ""
                    if (jsondata.get('params').get('action') == 'INSERT' and jsondata.get('params').get(
                            'type') == 'INVOICE_HEADER'):
                        result_data = inward_dtl.set_Invoiceheader()
                        out_data = result_data[0].split(",")
                        header_gid = out_data[0]
                        if (header_gid == "INVOICE ALREADY EXISTS."):
                            return JsonResponse(header_gid, safe=False)
                        out = out_data[1]
                    else:
                        # out = outputSplit(inward_dtl.set_Invoiceheader(), 1)
                        out = outputSplit(inward_dtl.set_Invoiceheader_status_update(), 1)

                    if (jsondata.get('params').get('action') == 'INSERT' and
                            jsondata.get('params').get('type') == 'INVOICE_HEADER' and out == "SUCCESS"):
                        try:
                            inward_dtl.action = "GET"
                            inward_dtl.type = "MAIL_TEMPLATE"
                            inward_dtl.filter = json.dumps({"template_name": "AP_INVOICECREATION",
                                                            "header_gid": header_gid, "queryname": "INVOICE_CREATION"})
                            inward_dtl.classification = json.dumps(
                                {"Entity_Gid": inward_dtl.entity_gid, "Emp_gid": inward_dtl.employee_gid})
                            templates_data = inward_dtl.get_multiple_email_templates_data()
                            Mail_Data = templates_data.get("Mail_Data")[0].get("mailtemplate_body")
                            Header_Data = templates_data.get("Header_Data")[0]
                            for (k, v) in Header_Data.items():
                                value = str(v)
                                key = "{{" + k + "}}"
                                Mail_Data = Mail_Data.replace(key, value);
                            cleanr = re.compile('<.*?>')
                            body_text = re.sub(cleanr, '', Mail_Data)
                            # to_email="rvignesh@vsolv.co.in"
                            to_email = "vsolvstab@gmail.com"
                            # email = EmailMessage('Invoice Created Successfully',body_text,to=[to_email])
                            # email.send()
                            mail_status = CoreViews.sending_mail(Mail_Data, to_email, body_text)
                            if (mail_status == "SUCCESS"):
                                return JsonResponse(mail_status, safe=False)
                            else:
                                mail_error_message = 'Invoice created successfully, mail sending error,' + mail_status
                                return JsonResponse({"MESSAGE": "ERROR_OCCURED", "ERROR": mail_error_message})
                        except Exception as e:
                            return JsonResponse("Email_Not_Send", safe=False)
                    if (jsondata.get('params').get('action') == 'UPDATE' and
                            jsondata.get('params').get('type') == 'STATUS' and
                            jsondata.get('params').get('status_json').get('Status') == 'BOUNCE' and out == "SUCCESS"):
                        try:
                            header_gid = jsondata.get('params').get('status_json').get("Invoice_Header_Gid")
                            inward_dtl.action = "GET"
                            inward_dtl.type = "MAIL_TEMPLATE"
                            inward_dtl.filter = json.dumps({"template_name": "BOUNCE_PROCESS",
                                                            "header_gid": header_gid, "queryname": "BOUNCE"})
                            inward_dtl.classification = json.dumps(
                                {"Entity_Gid": inward_dtl.entity_gid, "Emp_gid": inward_dtl.employee_gid})
                            templates_data = inward_dtl.get_multiple_email_templates_data()
                            Mail_Data = templates_data.get("Mail_Data")[0].get("mailtemplate_body")
                            Header_Data = templates_data.get("Header_Data")[0]
                            for (k, v) in Header_Data.items():
                                value = str(v)
                                key = "{{" + k + "}}"
                                Mail_Data = Mail_Data.replace(key, value);
                            cleanr = re.compile('<.*?>')
                            body_text = re.sub(cleanr, '', Mail_Data)
                            to_email = "vsolvstab@gmail.com"
                            # email = EmailMessage('Invoice Bounced', body_text, to=[to_email])
                            # email.send()
                            # return JsonResponse(out, safe=False)
                            # to_email = "rvignesh@vsolv.co.in"
                            mail_status = CoreViews.sending_mail(Mail_Data, to_email, body_text)
                            if (mail_status == "SUCCESS"):
                                return JsonResponse(mail_status, safe=False)
                            else:
                                mail_error_message = mail_status
                                return JsonResponse({"MESSAGE": "ERROR_OCCURED", "ERROR": mail_error_message})
                        except Exception as e:
                            return JsonResponse("Email_Not_Send", safe=False)
                    else:
                        return JsonResponse(out, safe=False)
                except Exception as e:
                    return JsonResponse({"MESSAGE": "ERROR_OCCURED", "DATA": str(e)})

            elif (jsondata.get('params').get('action') == 'UPDATE' and
                  jsondata.get('params').get('type') == 'STATUS' and
                  jsondata.get('params').get('status_json').get('Status') == 'APPROVED'):
                try:
                    current_month = datetime.now().strftime('%m')
                    current_day = datetime.now().strftime('%d')
                    current_year_full = datetime.now().strftime('%Y')
                    today_date = str(current_day + "/" + current_month + "/" + current_year_full)
                    Is_approve_and_pay = jsondata.get('params').get('status_json').get('Is_approve_and_pay')
                    invoice_header_gid = jsondata.get('params').get('status_json').get('Invoice_Header_Gid')
                    file_data = jsondata.get('params').get('status_json').get('file_data')
                    Invoice_Type = jsondata.get('params').get('status_json').get('Invoice_Type')
                    cr_no = jsondata.get('params').get('status_json').get('ref_no')
                    status = jsondata.get('params').get('status_json').get('Header_Status')
                    Remark = jsondata.get('params').get('status_json').get('Remark')
                    entity_gid = int(decry_data(request.session['Entity_gid']))
                    employee_gid = int(decry_data(request.session['Emp_gid']))
                    ap_statu_update_result = ""
                    try:
                        status_update_data = {"Invoice_Header_Gid": invoice_header_gid, "entity_gid": entity_gid,
                                              "employee_gid": employee_gid, "Status": "AP INITIATED",
                                              "file_data": file_data}
                        ap_statu_update_result = AP_status_update(status_update_data)
                        if (ap_statu_update_result == "SUCCESS"):
                            pass
                        else:
                            return JsonResponse(
                                {"MESSAGE": "ERROR_OCCURED_ON_AP INITIATED_UPDATION", "OUT": ap_statu_update_result})
                    except Exception as e:
                        common.logger.error(e)
                        return JsonResponse({"MESSAGE": "ERROR_OCCURED_ON_AP INITIATED_UPDATION", "DATA": str(e)})
                    inward_dtl.action = "INSERT"
                    inward_dtl.type = "INITIAL_SET"
                    inward_dtl.filter = json.dumps({"InvoiceHeader_Gid": invoice_header_gid,
                                                    "cr_no": cr_no, "Status_": status, "Invoice_Type": Invoice_Type})
                    inward_dtl.classification = json.dumps({"Entity_Gid": entity_gid})
                    inward_dtl.create_by = employee_gid
                    out = outputSplit(inward_dtl.set_accounting_entry(), 1)
                    if (out == 'SUCCESS' or out == 'ALREADY INSERTED'):

                        try:
                            Final_status = "APPROVED"
                            Invoice_Header_Gid = jsondata.get('params').get('status_json').get("Invoice_Header_Gid")
                            inward_dtl.action = "UPDATE"
                            inward_dtl.type = "INVOICE_HEADER_UPDATE"
                            inward_dtl.header_json = {
                                "HEADER": [{"Invoice_Header_Gid": Invoice_Header_Gid, "refno": "cbsnumber",
                                            "status_": Final_status,
                                            "crno": cr_no, "Remark": Remark}]}
                            inward_dtl.debit_json = {}
                            inward_dtl.detail_json = {}
                            inward_dtl.status_json = {}
                            inward_dtl.entity_gid = entity_gid
                            inward_dtl.employee_gid = employee_gid
                            outs = outputSplit(inward_dtl.set_Invoiceheader(), 1)
                            return JsonResponse(outs, safe=False)
                        except Exception as e:
                            common.logger.error(e)
                            return JsonResponse({"MESSAGE": "ERROR_OCCURED_ON_AP INITIATED_UPDATION", "DATA": str(e)})

                        try:
                            inward_dtl.action = "GET"
                            inward_dtl.type = "AP_ENTER_DETAIL_GET"
                            ref_no = jsondata.get('params').get('status_json').get('ref_no')
                            inward_dtl.filter = json.dumps({"entry_refno": ref_no, "entry_module": "AP"})
                            inward_dtl.classification = json.dumps({"Entity_Gid": entity_gid})
                            datas = inward_dtl.get_invoice_all()
                            Fund_Transfer_Dtls_data = datas.get("entry_detail")[0]
                            Fund_Transfer_Dtls_data = json.loads(Fund_Transfer_Dtls_data)

                            orginal_data_frame = pd.DataFrame(Fund_Transfer_Dtls_data.get("Fund_Transfer_Dtls"))
                            data_frame = pd.DataFrame(Fund_Transfer_Dtls_data.get("Fund_Transfer_Dtls"))

                            data_frame['Amount'] = data_frame['Amount'].astype(float)
                            Credit_amount = data_frame.loc[data_frame['Cr_Dr_Flag'] == 'C', 'Amount'].sum()
                            Debit_amount = data_frame.loc[data_frame['Cr_Dr_Flag'] == 'D', 'Amount'].sum()
                            Credit_amount = str(round(float(Credit_amount), 2))
                            Debit_amount = str(round(float(Debit_amount), 2))
                            if (Credit_amount == Debit_amount):

                                Unique_Values = data_frame.Entry_refno.unique()
                                Unique_Values_Length = len(Unique_Values)
                                Final_Unique_Values = []
                                for i in range(len(Unique_Values)):
                                    Single_Unique_Values = Unique_Values[i]
                                    Fetched_values = data_frame[(data_frame['Entry_refno'] == Single_Unique_Values)]
                                    Final_send_data = orginal_data_frame[
                                        (orginal_data_frame['Entry_refno'] == Single_Unique_Values)]

                                    send_Credit_amount = Fetched_values.loc[
                                        Fetched_values['Cr_Dr_Flag'] == 'C', 'Amount'].sum()
                                    send_Debit_amount = Fetched_values.loc[
                                        Fetched_values['Cr_Dr_Flag'] == 'D', 'Amount'].sum()
                                    send_Credit_amount = str(round(float(send_Credit_amount), 2))
                                    send_Debit_amount = str(round(float(send_Debit_amount), 2))

                                    if (send_Credit_amount == send_Debit_amount):

                                        send_data = Final_send_data.to_json(orient='records')
                                        send_data = json.loads(send_data)

                                        branch_code = Fund_Transfer_Dtls_data.get("Fund_Transfer_Dtls")[0].get(
                                            "Brn_Code")
                                        CBSDATE = ""
                                        NEFT_ACCOUNT_NUMBER = ""
                                        # CBSDATE=Fund_Transfer_Dtls_data.get("Fund_Transfer_Dtls")[0].get("CBSDATE")
                                        try:
                                            # pass
                                            CBSDATE_DATA = str(common.get_server_date("GET_CBSDATE_ACCOUNT_NUMBER")[0])
                                            CBSDATE_DATA_LIST = CBSDATE_DATA.split(",")
                                            NEFT_ACCOUNT_NUMBER = CBSDATE_DATA_LIST[0]
                                            CBSDATE = CBSDATE_DATA_LIST[1]
                                        except Exception as e:
                                            common.logger.error(e)
                                            return JsonResponse(
                                                {"MESSAGE": "ERROR_OCCURED_ON_CBSDATE_AND_ACCOUNT_NUMBER_GET",
                                                 "DATA": str(e)})

                                        try:
                                            token_status = 1
                                            generated_token_data = master_views.master_sync_Data_("GET", "get_data",
                                                                                                  employee_gid)
                                            log_data = generated_token_data
                                            token = generated_token_data.get("DATA")[0].get("clienttoken_name")
                                            if (token == " " or token == None):
                                                token_status = 0
                                            if token_status == 1:
                                                try:
                                                    data = {"Src_Channel": "EMS", "ApplicationId": Single_Unique_Values,
                                                            "TransactionBranch": branch_code, "Txn_Date": CBSDATE,
                                                            "productType": "DP", "Fund_Transfer_Dtls": send_data}
                                                    data = json.dumps(data)
                                                    log_data = [{"BEFORE_AMOUNT_TRANSFER_API_DATA": data}]
                                                    common.logger.error(log_data)

                                                    client_api = common.clientapi()
                                                    headers = {"Content-Type": "application/json",
                                                               "Authorization": "Bearer " + token}
                                                    result = requests.post(
                                                        "" + client_api + "/nbfc/v1/mwr/amount-transfer",
                                                        headers=headers, data=data, verify=False)
                                                    results = result.content.decode("utf-8")
                                                    results_data = json.loads(results)
                                                    log_data = [{"AFTER_AMOUNT_TRANSFER_API_DATA": results_data}]
                                                    common.logger.error(log_data)

                                                    ErrorStatus = results_data.get("CbsStatus")[0].get("ErrorMessage")
                                                    ErrorCode = results_data.get("CbsStatus")[0].get("ErrorCode")
                                                    if (ErrorStatus == "Success" and ErrorCode == '0'):
                                                        CBSReferenceNo = results_data.get("CbsStatus")[0].get(
                                                            "CBSReferenceNo")
                                                        try:
                                                            count_values = i + 1
                                                            Final_status = "ENTRY"
                                                            if (count_values == len(Unique_Values)):
                                                                Final_status = "APPROVED"
                                                            Invoice_Header_Gid = jsondata.get('params').get(
                                                                'status_json').get("Invoice_Header_Gid")
                                                            inward_dtl.action = "UPDATE"
                                                            inward_dtl.type = "INVOICE_HEADER_UPDATE"
                                                            inward_dtl.header_json = {
                                                                "HEADER": [{"Invoice_Header_Gid": Invoice_Header_Gid,
                                                                            "refno": CBSReferenceNo,
                                                                            "status_": Final_status,
                                                                            "crno": Single_Unique_Values,
                                                                            "Remark": Remark}]}
                                                            inward_dtl.debit_json = {}
                                                            inward_dtl.detail_json = {}
                                                            inward_dtl.status_json = {}
                                                            inward_dtl.entity_gid = entity_gid
                                                            inward_dtl.employee_gid = employee_gid
                                                            outs = outputSplit(inward_dtl.set_Invoiceheader(), 1)
                                                            if (outs == "SUCCESS"):
                                                                Final_Unique_Values.append("SUCCESS")
                                                                if (len(Final_Unique_Values) == len(Unique_Values)):
                                                                    if (Is_approve_and_pay == "Y"):
                                                                        try:
                                                                            invoice_set = mAP.ap_model()
                                                                            invoice_set.action = "GET"
                                                                            invoice_set.type = "AP_PAYMENTDETAILS"
                                                                            filter = {
                                                                                "InvoiceHeader_Status": "APPROVED",
                                                                                "InvoiceHeader_Gid": [
                                                                                    invoice_header_gid],
                                                                                "InvoiceHeader_InvoiceDate": "",
                                                                                "fromdate": "",
                                                                                "invoiceheader_branchgid": "",
                                                                                "Page_Index": 0, "Page_Size": 10}
                                                                            invoice_set.filter = json.dumps(filter)
                                                                            invoice_set.classification = json.dumps(
                                                                                {"Entity_Gid": entity_gid})
                                                                            invoice_set.create_by = employee_gid
                                                                            out = invoice_set.get_invoice_all()
                                                                            jdata = out.to_json(orient='records')
                                                                            jdata = json.loads(jdata)
                                                                            Paymentheader_Amount = 0
                                                                            Payment_Mode = ""
                                                                            for i in jdata:
                                                                                i['Amt_topay'] = i.get("credit_amount")
                                                                                if (
                                                                                        i.get("paymode_name") != "CREDITGL"):
                                                                                    Payment_Mode = i.get("paymode_name")
                                                                                    paymode_glno = i.get("paymode_glno")
                                                                                    credit_ddtranbranch = i.get(
                                                                                        "credit_ddtranbranch")
                                                                                    credit_ddpaybranch = i.get(
                                                                                        "credit_ddpaybranch")
                                                                                    bankbranch_name = i.get(
                                                                                        "bankbranch_name")
                                                                                    bankdetails_acno = i.get(
                                                                                        "bankdetails_acno")
                                                                                    ifsccode = i.get(
                                                                                        "bankbranch_ifsccode")
                                                                                    beneficiaryname = i.get(
                                                                                        "bankdetails_beneficiaryname")
                                                                                    bank_name = i.get("bank_name")
                                                                                    invoiceheader_remarks = i.get(
                                                                                        "invoiceheader_remarks")
                                                                                    invoiceheader_gid = i.get(
                                                                                        "invoiceheader_gid")
                                                                                    invoiceheader_status = i.get(
                                                                                        "invoiceheader_status")
                                                                                    invoiceheader_crno = i.get(
                                                                                        "invoiceheader_crno")
                                                                                    invoiceheader_invoiceno = i.get(
                                                                                        "invoiceheader_invoiceno")
                                                                                    credit_bankgid = i.get(
                                                                                        "credit_bankgid")
                                                                                if (i.get("invoiceheader_ppx") == "E"):
                                                                                    Ref_id = i.get(
                                                                                        "invoiceheader_employeegid")
                                                                                    Header_type = "EMPLOYEE_PAYMENT"
                                                                                elif (
                                                                                        i.get("invoiceheader_ppx") == "I"):
                                                                                    Ref_id = i.get(
                                                                                        "invoiceheader_branchgid")
                                                                                    Header_type = "BRANCH_PAYMENT"
                                                                                else:
                                                                                    Ref_id = i.get("supplier_gid")
                                                                                    Header_type = "SUPPLIER_PAYMENT"

                                                                                Paymentheader_Amount = Paymentheader_Amount + i.get(
                                                                                    "credit_amount")
                                                                            Paymentheader_Amount = round(
                                                                                Paymentheader_Amount, 2)
                                                                            if (Payment_Mode == ""):
                                                                                Payment_Mode = "CREDITGL";
                                                                                credit_bankgid = 0;
                                                                                bankbranch_name = "null";
                                                                                bankdetails_acno = "null";
                                                                                ifsccode = "null";
                                                                                beneficiaryname = "null";
                                                                                paymode_glno = "null";
                                                                                credit_ddtranbranch = "";
                                                                                credit_ddpaybranch = "";

                                                                            datenow = str(
                                                                                datetime.now().strftime("%Y-%m-%d"))
                                                                            pass_data = {'params': {'action': 'Insert',
                                                                                                    'type': 'PAYMENT_ADD',
                                                                                                    'header_json': {
                                                                                                        'HEADER': [{
                                                                                                                       'Paymentheader_Amount': Paymentheader_Amount,
                                                                                                                       'Payment_Mode': Payment_Mode,
                                                                                                                       'paymode_glno': paymode_glno,
                                                                                                                       'credit_ddtranbranch': credit_ddtranbranch,
                                                                                                                       "Paymentheader_Status": "PAYMENT INITIATE",
                                                                                                                       'credit_ddpaybranch': credit_ddpaybranch,
                                                                                                                       "bankbranch_name": bankbranch_name,
                                                                                                                       "Remark": "PAYMENT INITIATE",
                                                                                                                       "Bank_Detail_Gid": credit_bankgid,
                                                                                                                       "Paymentheader_Date": datenow,
                                                                                                                       "REF_Gid": Ref_id,
                                                                                                                       "Header_type": Header_type,
                                                                                                                       "bankdetails_acno": bankdetails_acno,
                                                                                                                       "ifsccode": ifsccode,
                                                                                                                       "beneficiaryname": beneficiaryname}]},
                                                                                                    'detail_json': {
                                                                                                        'DETAILS': jdata},
                                                                                                    'other_json': {},
                                                                                                    'status_json': {}}}
                                                                            return APpayment_set_function(pass_data,
                                                                                                          employee_gid,
                                                                                                          entity_gid)

                                                                        except Exception as e:
                                                                            common.logger.error(e)
                                                                            return JsonResponse({
                                                                                                    "MESSAGE": "ERROR_OCCURED_ON_PAYMENT_FUNCTION",
                                                                                                    "DATA": str(e)})
                                                                    else:
                                                                        return JsonResponse(outs, safe=False)
                                                            else:
                                                                return JsonResponse({
                                                                                        "MESSAGE": "ERROR_OCCURED_ON_INVOICE_HEADER_UPDATE",
                                                                                        "DATA": outs,
                                                                                        "AMOUNT_TRANSFER_DATA": results_data})
                                                        except Exception as e:
                                                            common.logger.error(e)
                                                            return JsonResponse(
                                                                {"MESSAGE": "ERROR_OCCURED_ON_INVOICE_HEADER_UPDATE",
                                                                 "DATA": str(e), "AMOUNT_TRANSFER_DATA": results_data})
                                                    else:
                                                        return JsonResponse(
                                                            {"MESSAGE": "FAILED", "FAILED_STATUS": results_data})
                                                except Exception as e:
                                                    common.logger.error(e)
                                                    return JsonResponse(
                                                        {"MESSAGE": "ERROR_OCCURED_ON_AMOUNT_TRANSFER_CLINET_API",
                                                         "DATA": str(e), "log_data": log_data})
                                            else:
                                                return JsonResponse({
                                                                        "MESSAGE": "ERROR_OCCURED_ON_TOKEN_GENERATIONS OR INVALID AUTHENTICATONS"})
                                        except Exception as e:
                                            common.logger.error(e)
                                            return JsonResponse(
                                                {"MESSAGE": "ERROR_OCCURED_TOKEN_GENERATION", "DATA": str(e),
                                                 "log_data": log_data})
                                    else:
                                        return JsonResponse({"MESSAGE": "Credit Amount and Debit Amount Not Equal"})
                            else:
                                return JsonResponse({"MESSAGE": "Credit Amount and Debit Amount Not Equal"})
                        except Exception as e:
                            common.logger.error(e)
                            return JsonResponse({"MESSAGE": "ERROR_OCCURED_ON_ENTRY_DETAILS_GET", "DATA": str(e)})
                    return JsonResponse({"MESSAGE": "ERROR_OCCURED_ON_INITIAL_SET", "DATA": out})
                except Exception as e:
                    common.logger.error(e)
                    return JsonResponse({"MESSAGE": "ERROR_OCCURED_ON_ACCOUNTING_ENTRY_INITIAL_SET", "DATA": str(e)})
        except Exception as e:
            common.logger.error(e)
            return JsonResponse({"MESSAGE": "ERROR_OCCURED_ON_STATUS_UPDATE", "DATA": str(e)})


def approve_and_pay(request):
    utl.check_pointaccess(request)
    utl.check_authorization(request)
    if request.method == 'POST':
        try:
            path = request.path
            inward_dtl = mAP.ap_model()
            jsondata = json.loads(request.body.decode('utf-8'))
            if (jsondata.get('params').get('action') == 'UPDATE' and
                    jsondata.get('params').get('type') == 'STATUS' and
                    jsondata.get('params').get('status_json').get('Status') == 'APPROVED'):
                try:
                    current_month = datetime.now().strftime('%m')
                    current_day = datetime.now().strftime('%d')
                    current_year_full = datetime.now().strftime('%Y')
                    today_date = str(current_day + "/" + current_month + "/" + current_year_full)
                    Is_approve_and_pay = jsondata.get('params').get('status_json').get('Is_approve_and_pay')
                    invoice_header_gid = jsondata.get('params').get('status_json').get('Invoice_Header_Gid')
                    file_data = jsondata.get('params').get('status_json').get('file_data')
                    Invoice_Type = jsondata.get('params').get('status_json').get('Invoice_Type')
                    cr_no = jsondata.get('params').get('status_json').get('ref_no')
                    status = jsondata.get('params').get('status_json').get('Header_Status')
                    entity_gid = int(decry_data(request.session['Entity_gid']))
                    employee_gid = int(decry_data(request.session['Emp_gid']))
                    ap_statu_update_result = ""
                    try:
                        status_update_data = {"Invoice_Header_Gid": invoice_header_gid, "entity_gid": entity_gid,
                                              "employee_gid": employee_gid, "Status": "AP INITIATED",
                                              "file_data": file_data}
                        ap_statu_update_result = AP_status_update(status_update_data)
                        if (ap_statu_update_result == "SUCCESS"):
                            try:
                                inward_dtl.action = "INSERT"
                                inward_dtl.type = "INITIAL_SET"
                                inward_dtl.filter = json.dumps({"InvoiceHeader_Gid": invoice_header_gid,
                                                                "cr_no": cr_no, "Status_": status,
                                                                "Invoice_Type": Invoice_Type})
                                inward_dtl.classification = json.dumps({"Entity_Gid": entity_gid})
                                inward_dtl.create_by = employee_gid
                                out = outputSplit(inward_dtl.set_accounting_entry(), 1)
                                if (out == 'SUCCESS' or out == 'ALREADY INSERTED'):
                                    try:
                                        inward_dtl.action = "GET"
                                        inward_dtl.type = "AP_ENTER_DETAIL_GET"
                                        ref_no = jsondata.get('params').get('status_json').get('ref_no')
                                        inward_dtl.filter = json.dumps({"entry_refno": ref_no, "entry_module": "AP"})
                                        inward_dtl.classification = json.dumps({"Entity_Gid": entity_gid})
                                        datas = inward_dtl.get_invoice_all()
                                        Fund_Transfer_Dtls_data = datas.get("entry_detail")[0]
                                        Fund_Transfer_Dtls_data = json.loads(Fund_Transfer_Dtls_data)

                                        orginal_data_frame = pd.DataFrame(
                                            Fund_Transfer_Dtls_data.get("Fund_Transfer_Dtls"))
                                        data_frame = pd.DataFrame(Fund_Transfer_Dtls_data.get("Fund_Transfer_Dtls"))

                                        data_frame['Amount'] = data_frame['Amount'].astype(float)
                                        Credit_amount = data_frame.loc[data_frame['Cr_Dr_Flag'] == 'C', 'Amount'].sum()
                                        Debit_amount = data_frame.loc[data_frame['Cr_Dr_Flag'] == 'D', 'Amount'].sum()
                                        Credit_amount = str(round(float(Credit_amount), 2))
                                        Debit_amount = str(round(float(Debit_amount), 2))
                                        if (Credit_amount == Debit_amount):

                                            Unique_Values = data_frame.Entry_refno.unique()
                                            Unique_Values_Length = len(Unique_Values)
                                            Final_Unique_Values = []
                                            for i in range(len(Unique_Values)):
                                                Single_Unique_Values = Unique_Values[i]
                                                Fetched_values = data_frame[
                                                    (data_frame['Entry_refno'] == Single_Unique_Values)]
                                                Final_send_data = orginal_data_frame[
                                                    (orginal_data_frame['Entry_refno'] == Single_Unique_Values)]

                                                send_Credit_amount = Fetched_values.loc[
                                                    Fetched_values['Cr_Dr_Flag'] == 'C', 'Amount'].sum()
                                                send_Debit_amount = Fetched_values.loc[
                                                    Fetched_values['Cr_Dr_Flag'] == 'D', 'Amount'].sum()
                                                send_Credit_amount = str(round(float(send_Credit_amount), 2))
                                                send_Debit_amount = str(round(float(send_Debit_amount), 2))

                                                if (send_Credit_amount == send_Debit_amount):

                                                    send_data = Final_send_data.to_json(orient='records')
                                                    send_data = json.loads(send_data)

                                                    branch_code = Fund_Transfer_Dtls_data.get("Fund_Transfer_Dtls")[
                                                        0].get("Brn_Code")
                                                    CBSDATE = ""
                                                    NEFT_ACCOUNT_NUMBER = ""
                                                    # CBSDATE=Fund_Transfer_Dtls_data.get("Fund_Transfer_Dtls")[0].get("CBSDATE")
                                                    try:
                                                        # pass
                                                        CBSDATE_DATA = str(
                                                            common.get_server_date("GET_CBSDATE_ACCOUNT_NUMBER")[0])
                                                        CBSDATE_DATA_LIST = CBSDATE_DATA.split(",")
                                                        NEFT_ACCOUNT_NUMBER = CBSDATE_DATA_LIST[0]
                                                        CBSDATE = CBSDATE_DATA_LIST[1]
                                                    except Exception as e:
                                                        common.logger.error(e)
                                                        header_update_data = {"Invoice_Header_Gid": invoice_header_gid,
                                                                              "entity_gid": entity_gid,
                                                                              "type": "ERROR_UPDATE",
                                                                              "employee_gid": employee_gid,
                                                                              "Error_log": {
                                                                                  "MESSAGE": "ERROR_OCCURED_ON_CBSDATE_AND_ACCOUNT_NUMBER_GET_",
                                                                                  "DATA": str(e)}}
                                                        AP_Header_Update_result = AP_Header_Update(header_update_data)
                                                        # pass
                                                        # return JsonResponse({"MESSAGE": "ERROR_OCCURED_ON_CBSDATE_AND_ACCOUNT_NUMBER_GET", "DATA": str(e)})

                                                    try:
                                                        token_status = 1
                                                        generated_token_data = master_views.master_sync_Data_("GET",
                                                                                                              "get_data",
                                                                                                              employee_gid)
                                                        log_data = generated_token_data
                                                        token = generated_token_data.get("DATA")[0].get(
                                                            "clienttoken_name")
                                                        if (token == " " or token == None):
                                                            token_status = 0
                                                        if token_status == 1:
                                                            try:
                                                                data = {"Src_Channel": "EMS",
                                                                        "ApplicationId": Single_Unique_Values,
                                                                        "TransactionBranch": branch_code,
                                                                        "Txn_Date": CBSDATE,
                                                                        "productType": "DP",
                                                                        "Fund_Transfer_Dtls": send_data}
                                                                data = json.dumps(data)
                                                                log_data = [{"BEFORE_AMOUNT_TRANSFER_API_DATA": data}]
                                                                common.logger.error(log_data)

                                                                client_api = common.clientapi()
                                                                headers = {"Content-Type": "application/json",
                                                                           "Authorization": "Bearer " + token}
                                                                result = requests.post(
                                                                    "" + client_api + "/nbfc/v1/mwr/amount-transfer",
                                                                    headers=headers, data=data, verify=False)
                                                                results = result.content.decode("utf-8")
                                                                log_data.append({"API_RESULT": results})
                                                                results_data = json.loads(results)
                                                                log_data = [
                                                                    {"AFTER_AMOUNT_TRANSFER_API_DATA": results_data}]
                                                                common.logger.error(log_data)

                                                                ErrorStatus = results_data.get("CbsStatus")[0].get(
                                                                    "ErrorMessage")
                                                                ErrorCode = results_data.get("CbsStatus")[0].get(
                                                                    "ErrorCode")
                                                                if (ErrorStatus == "Success" and ErrorCode == '0'):
                                                                    CBSReferenceNo = results_data.get("CbsStatus")[
                                                                        0].get("CBSReferenceNo")
                                                                    try:
                                                                        count_values = i + 1
                                                                        Final_status = "ENTRY"
                                                                        if (count_values == len(Unique_Values)):
                                                                            Final_status = "APPROVED"
                                                                        Invoice_Header_Gid = jsondata.get('params').get(
                                                                            'status_json').get("Invoice_Header_Gid")
                                                                        inward_dtl.action = "UPDATE"
                                                                        inward_dtl.type = "INVOICE_HEADER_UPDATE"
                                                                        inward_dtl.header_json = {
                                                                            "HEADER": [{
                                                                                "Invoice_Header_Gid": Invoice_Header_Gid,
                                                                                "refno": CBSReferenceNo,
                                                                                "status_": Final_status,
                                                                                "crno": Single_Unique_Values}]}
                                                                        inward_dtl.debit_json = {}
                                                                        inward_dtl.detail_json = {}
                                                                        inward_dtl.status_json = {}
                                                                        inward_dtl.entity_gid = entity_gid
                                                                        inward_dtl.employee_gid = employee_gid
                                                                        outs = outputSplit(
                                                                            inward_dtl.set_Invoiceheader(), 1)
                                                                        if (outs == "SUCCESS"):
                                                                            Final_Unique_Values.append("SUCCESS")
                                                                            if (len(Final_Unique_Values) == len(
                                                                                    Unique_Values)):
                                                                                if (Is_approve_and_pay == "Y"):
                                                                                    try:
                                                                                        invoice_set = mAP.ap_model()
                                                                                        invoice_set.action = "GET"
                                                                                        invoice_set.type = "AP_PAYMENTDETAILS"
                                                                                        filter = {
                                                                                            "InvoiceHeader_Status": "APPROVED",
                                                                                            "InvoiceHeader_Gid": [
                                                                                                invoice_header_gid],
                                                                                            "InvoiceHeader_InvoiceDate": "",
                                                                                            "fromdate": "",
                                                                                            "invoiceheader_branchgid": "",
                                                                                            "Page_Index": 0,
                                                                                            "Page_Size": 10}
                                                                                        invoice_set.filter = json.dumps(
                                                                                            filter)
                                                                                        invoice_set.classification = json.dumps(
                                                                                            {"Entity_Gid": entity_gid})
                                                                                        invoice_set.create_by = employee_gid
                                                                                        out = invoice_set.get_invoice_all()
                                                                                        jdata = out.to_json(
                                                                                            orient='records')
                                                                                        jdata = json.loads(jdata)
                                                                                        Paymentheader_Amount = 0
                                                                                        Payment_Mode = ""
                                                                                        for i in jdata:
                                                                                            i['Amt_topay'] = i.get(
                                                                                                "credit_amount")
                                                                                            if (i.get(
                                                                                                    "paymode_name") != "CREDITGL"):
                                                                                                Payment_Mode = i.get(
                                                                                                    "paymode_name")
                                                                                                paymode_glno = i.get(
                                                                                                    "paymode_glno")
                                                                                                credit_ddtranbranch = i.get(
                                                                                                    "credit_ddtranbranch")
                                                                                                credit_ddpaybranch = i.get(
                                                                                                    "credit_ddpaybranch")
                                                                                                bankbranch_name = i.get(
                                                                                                    "bankbranch_name")
                                                                                                bankdetails_acno = i.get(
                                                                                                    "bankdetails_acno")
                                                                                                ifsccode = i.get(
                                                                                                    "bankbranch_ifsccode")
                                                                                                beneficiaryname = i.get(
                                                                                                    "bankdetails_beneficiaryname")
                                                                                                bank_name = i.get(
                                                                                                    "bank_name")
                                                                                                invoiceheader_remarks = i.get(
                                                                                                    "invoiceheader_remarks")
                                                                                                invoiceheader_gid = i.get(
                                                                                                    "invoiceheader_gid")
                                                                                                invoiceheader_status = i.get(
                                                                                                    "invoiceheader_status")
                                                                                                invoiceheader_crno = i.get(
                                                                                                    "invoiceheader_crno")
                                                                                                invoiceheader_invoiceno = i.get(
                                                                                                    "invoiceheader_invoiceno")
                                                                                                credit_bankgid = i.get(
                                                                                                    "credit_bankgid")
                                                                                            if (i.get(
                                                                                                    "invoiceheader_ppx") == "E"):
                                                                                                Ref_id = i.get(
                                                                                                    "invoiceheader_employeegid")
                                                                                                Header_type = "EMPLOYEE_PAYMENT"
                                                                                            elif (i.get(
                                                                                                    "invoiceheader_ppx") == "I"):
                                                                                                Ref_id = i.get(
                                                                                                    "invoiceheader_branchgid")
                                                                                                Header_type = "BRANCH_PAYMENT"
                                                                                            else:
                                                                                                Ref_id = i.get(
                                                                                                    "supplier_gid")
                                                                                                Header_type = "SUPPLIER_PAYMENT"

                                                                                            Paymentheader_Amount = Paymentheader_Amount + i.get(
                                                                                                "credit_amount")
                                                                                        Paymentheader_Amount = round(
                                                                                            Paymentheader_Amount, 2)
                                                                                        if (Payment_Mode == ""):
                                                                                            Payment_Mode = "CREDITGL";
                                                                                            credit_bankgid = 0;
                                                                                            bankbranch_name = "null";
                                                                                            bankdetails_acno = "null";
                                                                                            ifsccode = "null";
                                                                                            beneficiaryname = "null";
                                                                                            paymode_glno = "null";
                                                                                            credit_ddtranbranch = "";
                                                                                            credit_ddpaybranch = "";

                                                                                        datenow = str(
                                                                                            datetime.now().strftime(
                                                                                                "%Y-%m-%d"))
                                                                                        pass_data = {'params': {
                                                                                            'action': 'Insert',
                                                                                            'type': 'PAYMENT_ADD',
                                                                                            'header_json': {'HEADER': [{
                                                                                                'Paymentheader_Amount': Paymentheader_Amount,
                                                                                                'Payment_Mode': Payment_Mode,
                                                                                                'paymode_glno': paymode_glno,
                                                                                                'credit_ddtranbranch': credit_ddtranbranch,
                                                                                                "Paymentheader_Status": "PAYMENT INITIATE",
                                                                                                'credit_ddpaybranch': credit_ddpaybranch,
                                                                                                "bankbranch_name": bankbranch_name,
                                                                                                "Remark": "PAYMENT INITIATE",
                                                                                                "Bank_Detail_Gid": credit_bankgid,
                                                                                                "Paymentheader_Date": datenow,
                                                                                                "REF_Gid": Ref_id,
                                                                                                "Header_type": Header_type,
                                                                                                "bankdetails_acno": bankdetails_acno,
                                                                                                "ifsccode": ifsccode,
                                                                                                "beneficiaryname": beneficiaryname}]},
                                                                                            'detail_json': {
                                                                                                'DETAILS': jdata},
                                                                                            'other_json': {},
                                                                                            'status_json': {}}}
                                                                                        APpayment_set_function_approve_and_pay_result = APpayment_set_function_approve_and_pay(
                                                                                            pass_data, employee_gid,
                                                                                            entity_gid)

                                                                                    except Exception as e:
                                                                                        common.logger.error(e)
                                                                                        header_update_data = {
                                                                                            "Invoice_Header_Gid": invoice_header_gid,
                                                                                            "entity_gid": entity_gid,
                                                                                            "type": "ERROR_UPDATE",
                                                                                            "employee_gid": employee_gid,
                                                                                            "Error_log": {
                                                                                                "MESSAGE": "ERROR_OCCURED_ON_AP_PAYMENTDETAILS_GET_",
                                                                                                "DATA": str(e)}}
                                                                                        AP_Header_Update_result = AP_Header_Update(
                                                                                            header_update_data)
                                                                                        # pass
                                                                                        # return JsonResponse({"MESSAGE": "ERROR_OCCURED_ON_PAYMENT_FUNCTION","DATA": str(e)})
                                                                                else:
                                                                                    header_update_data = {
                                                                                        "Invoice_Header_Gid": invoice_header_gid,
                                                                                        "entity_gid": entity_gid,
                                                                                        "type": "ERROR_UPDATE",
                                                                                        "employee_gid": employee_gid,
                                                                                        "Error_log": {
                                                                                            "MESSAGE": "ERROR_OCCURED_ON_AP INITIATED_UPDATION",
                                                                                            "DATA": outs}}
                                                                                    AP_Header_Update_result = AP_Header_Update(
                                                                                        header_update_data)
                                                                                    # pass
                                                                                    # return JsonResponse(outs, safe=False)
                                                                        else:
                                                                            # pass
                                                                            header_update_data = {
                                                                                "Invoice_Header_Gid": invoice_header_gid,
                                                                                "entity_gid": entity_gid,
                                                                                "type": "ERROR_UPDATE",
                                                                                "employee_gid": employee_gid,
                                                                                "Error_log": {
                                                                                    "MESSAGE": "ERROR_OCCURED_ON_INVOICE_HEADER_UPDATE",
                                                                                    "OUTPUT_DATA": outs,
                                                                                    "AMOUNT_TRANSFER_DATA": results_data}}
                                                                            AP_Header_Update_result = AP_Header_Update(
                                                                                header_update_data)
                                                                            # return JsonResponse({"MESSAGE": "ERROR_OCCURED_ON_INVOICE_HEADER_UPDATE","DATA": outs,"AMOUNT_TRANSFER_DATA":results_data})
                                                                    except Exception as e:
                                                                        common.logger.error(e)
                                                                        header_update_data = {
                                                                            "Invoice_Header_Gid": invoice_header_gid,
                                                                            "entity_gid": entity_gid,
                                                                            "type": "ERROR_UPDATE",
                                                                            "employee_gid": employee_gid,
                                                                            "Error_log": {
                                                                                "MESSAGE": "ERROR_OCCURED_ON_INVOICE_HEADER_UPDATE_",
                                                                                "AMOUNT_TRANSFER_DATA": results_data}}
                                                                        AP_Header_Update_result = AP_Header_Update(
                                                                            header_update_data)
                                                                        # return JsonResponse({"MESSAGE": "ERROR_OCCURED_ON_INVOICE_HEADER_UPDATE","DATA": str(e),"AMOUNT_TRANSFER_DATA":results_data})
                                                                else:
                                                                    header_update_data = {
                                                                        "Invoice_Header_Gid": invoice_header_gid,
                                                                        "entity_gid": entity_gid,
                                                                        "type": "ERROR_UPDATE",
                                                                        "employee_gid": employee_gid,
                                                                        "Error_log": {"MESSAGE": "FAILED",
                                                                                      "FAILED_STATUS": results_data}}
                                                                    AP_Header_Update_result = AP_Header_Update(
                                                                        header_update_data)
                                                                    # return JsonResponse({"MESSAGE": "FAILED", "FAILED_STATUS": results_data})
                                                            except Exception as e:
                                                                common.logger.error(e)
                                                                header_update_data = {
                                                                    "Invoice_Header_Gid": invoice_header_gid,
                                                                    "entity_gid": entity_gid,
                                                                    "type": "ERROR_UPDATE",
                                                                    "employee_gid": employee_gid,
                                                                    "Error_log": {
                                                                        "MESSAGE": "ERROR_OCCURED_ON_AMOUNT_TRANSFER_CLINET_API_",
                                                                        "log_data": log_data}}
                                                                AP_Header_Update_result = AP_Header_Update(
                                                                    header_update_data)
                                                                # return JsonResponse({"MESSAGE": "ERROR_OCCURED_ON_AMOUNT_TRANSFER_CLINET_API","DATA": str(e), "log_data": log_data})
                                                        else:
                                                            header_update_data = {
                                                                "Invoice_Header_Gid": invoice_header_gid,
                                                                "entity_gid": entity_gid, "type": "ERROR_UPDATE",
                                                                "employee_gid": employee_gid, "Error_log": {
                                                                    "MESSAGE": "ERROR_OCCURED_ON_TOKEN_GENERATIONS OR INVALID AUTHENTICATONS"}}
                                                            AP_Header_Update_result = AP_Header_Update(
                                                                header_update_data)
                                                            # return JsonResponse({"MESSAGE": "ERROR_OCCURED_ON_TOKEN_GENERATIONS OR INVALID AUTHENTICATONS"})
                                                    except Exception as e:
                                                        common.logger.error(e)
                                                        header_update_data = {"Invoice_Header_Gid": invoice_header_gid,
                                                                              "entity_gid": entity_gid,
                                                                              "type": "ERROR_UPDATE",
                                                                              "employee_gid": employee_gid,
                                                                              "Error_log": {
                                                                                  "MESSAGE": "ERROR_OCCURED_TOKEN_GENERATION_",
                                                                                  "DATA": str(e), "log_data": log_data}}
                                                        AP_Header_Update_result = AP_Header_Update(header_update_data)
                                                        # return JsonResponse({"MESSAGE": "ERROR_OCCURED_TOKEN_GENERATION", "DATA": str(e),"log_data": log_data})
                                                else:
                                                    header_update_data = {"Invoice_Header_Gid": invoice_header_gid,
                                                                          "entity_gid": entity_gid,
                                                                          "type": "ERROR_UPDATE",
                                                                          "employee_gid": employee_gid, "Error_log": {
                                                            "MESSAGE": "Credit Amount and Debit Amount Not Equal"}}
                                                    AP_Header_Update_result = AP_Header_Update(header_update_data)
                                                    # return JsonResponse({"MESSAGE": "Credit Amount and Debit Amount Not Equal"})
                                        else:
                                            header_update_data = {"Invoice_Header_Gid": invoice_header_gid,
                                                                  "entity_gid": entity_gid, "type": "ERROR_UPDATE",
                                                                  "employee_gid": employee_gid, "Error_log": {
                                                    "MESSAGE": "Credit Amount and Debit Amount Not Equal"}}
                                            AP_Header_Update_result = AP_Header_Update(header_update_data)
                                            # return JsonResponse({"MESSAGE": "Credit Amount and Debit Amount Not Equal"})
                                    except Exception as e:
                                        common.logger.error(e)
                                        header_update_data = {"Invoice_Header_Gid": invoice_header_gid,
                                                              "entity_gid": entity_gid, "type": "ERROR_UPDATE",
                                                              "employee_gid": employee_gid,
                                                              "Error_log": {
                                                                  "MESSAGE": "ERROR_OCCURED_ON_ENTRY_DETAILS_GET_",
                                                                  "DATA": str(e)}}
                                        AP_Header_Update_result = AP_Header_Update(header_update_data)
                                        # return JsonResponse({"MESSAGE": "ERROR_OCCURED_ON_ENTRY_DETAILS_GET", "DATA": str(e)})
                                # return JsonResponse({"MESSAGE": "ERROR_OCCURED_ON_INITIAL_SET", "DATA":out})
                                # pass
                                else:
                                    header_update_data = {"Invoice_Header_Gid": invoice_header_gid,
                                                          "entity_gid": entity_gid,
                                                          "type": "ERROR_UPDATE", "employee_gid": employee_gid,
                                                          "Error_log": {
                                                              "MESSAGE": "ERROR_OCCURED_ON_ACCOUNTING_ENTRY_INITIAL_SET",
                                                              "OUTPUT": out}}
                                    AP_Header_Update_result = AP_Header_Update(header_update_data)
                            except Exception as e:
                                common.logger.error(e)
                                header_update_data = {"Invoice_Header_Gid": invoice_header_gid,
                                                      "entity_gid": entity_gid,
                                                      "type": "ERROR_UPDATE", "employee_gid": employee_gid,
                                                      "Error_log": {
                                                          "MESSAGE": "ERROR_OCCURED_ON_ACCOUNTING_ENTRY_INITIAL_SET_",
                                                          "DATA": str(e), "RESULT": out}}
                                AP_Header_Update_result = AP_Header_Update(header_update_data)

                        else:
                            header_update_data = {"Invoice_Header_Gid": invoice_header_gid, "entity_gid": entity_gid,
                                                  "type": "ERROR_UPDATE", "employee_gid": employee_gid,
                                                  "Error_log": {"MESSAGE": "ERROR_OCCURED_ON_AP INITIATED_UPDATION",
                                                                "OUT": ap_statu_update_result}}
                            AP_Header_Update_result = AP_Header_Update(header_update_data)
                            # return JsonResponse({"MESSAGE": "ERROR_OCCURED_ON_AP INITIATED_UPDATION","OUT":ap_statu_update_result})
                    except Exception as e:
                        common.logger.error(e)
                        header_update_data = {"Invoice_Header_Gid": invoice_header_gid, "entity_gid": entity_gid,
                                              "type": "ERROR_UPDATE", "employee_gid": employee_gid,
                                              "Error_log": {"MESSAGE": "ERROR_OCCURED_ON_", "DATA": str(e)}}
                        AP_Header_Update_result = AP_Header_Update(header_update_data)
                        # return JsonResponse({"MESSAGE": "ERROR_OCCURED_ON_AP INITIATED_UPDATION", "DATA": str(e)})
                except Exception as e:
                    common.logger.error(e)
                    header_update_data = {"Invoice_Header_Gid": invoice_header_gid,
                                          "entity_gid": entity_gid, "type": "ERROR_UPDATE",
                                          "employee_gid": employee_gid,
                                          "Error_log": {"MESSAGE": "ERROR_OCCURED_", "DATA": str(e)}}
                    AP_Header_Update_result = AP_Header_Update(header_update_data)
                    # return JsonResponse({"MESSAGE": "ERROR_OCCURED_ON_ACCOUNTING_ENTRY_INITIAL_SET", "DATA": str(e)})
                    # pass
        except Exception as e:
            common.logger.error(e)
            header_update_data = {"Invoice_Header_Gid": invoice_header_gid, "entity_gid": entity_gid,
                                  "type": "ERROR_UPDATE", "employee_gid": employee_gid,
                                  "Error_log": {"MESSAGE": "ERROR_OCCURED_", "DATA": str(e)}}
            AP_Header_Update_result = AP_Header_Update(header_update_data)
            # return JsonResponse({"MESSAGE": "ERROR_OCCURED_ON_STATUS_UPDATE", "DATA": str(e)})


def ap_initail_and_accounting_entry(request):
    utl.check_pointaccess(request)
    utl.check_authorization(request)
    if request.method == 'POST':
        try:
            path = request.path
            inward_dtl = mAP.ap_model()
            jsondata = json.loads(request.body.decode('utf-8'))
            now_today_date = datetime.now()
            today_date = now_today_date.strftime("%d/%m/%Y")

            invoice_header_gid = jsondata.get('params').get('status_json').get('Invoice_Header_Gid')
            Invoice_Type = jsondata.get('params').get('status_json').get('Invoice_Type')
            cr_no = jsondata.get('params').get('status_json').get('ref_no')
            status = jsondata.get('params').get('status_json').get('Header_Status')
            entity_gid = int(decry_data(request.session['Entity_gid']))
            employee_gid = int(decry_data(request.session['Emp_gid']))
            try:
                common.main_fun1(request.read(), path)
            except Exception as e:
                common.logger.error(e)
                return JsonResponse({"MESSAGE": "ERROR_OCCURED_ON_XML", "DATA": str(e)})

            ap_statu_update_result = ""
            try:
                status_update_data = {"Invoice_Header_Gid": invoice_header_gid, "entity_gid": entity_gid,
                                      "employee_gid": employee_gid, "Status": "AP INITIATED"}
                ap_statu_update_result = AP_status_update(status_update_data)
                if (ap_statu_update_result == "SUCCESS"):
                    try:
                        inward_dtl.action = "INSERT"
                        inward_dtl.type = "INITIAL_SET"
                        inward_dtl.filter = json.dumps({"InvoiceHeader_Gid": invoice_header_gid,
                                                        "cr_no": cr_no, "Status_": status,
                                                        "Invoice_Type": Invoice_Type})
                        inward_dtl.classification = json.dumps({"Entity_Gid": entity_gid})
                        inward_dtl.create_by = employee_gid
                        out = outputSplit(inward_dtl.set_accounting_entry(), 1)
                        return JsonResponse(out, safe=False)
                    except Exception as e:
                        common.logger.error(e)
                        return JsonResponse({"MESSAGE": "ERROR_OCCURED_ON_AP_ACCOUNTING_ENTRY_SET", "DATA": str(e)})
                else:
                    return JsonResponse(
                        {"MESSAGE": "ERROR_OCCURED_ON_AP INITIATED_UPDATION", "OUT": ap_statu_update_result})
            except Exception as e:
                common.logger.error(e)
                return JsonResponse({"MESSAGE": "ERROR_OCCURED_ON_AP INITIATED_UPDATION", "DATA": str(e)})
        except Exception as e:
            common.logger.error(e)
            return JsonResponse({"MESSAGE": "ERROR_OCCURED", "DATA": str(e)})


def ap_entry_details_get_amount_transfer_api(request):
    utl.check_pointaccess(request)
    utl.check_authorization(request)
    if request.method == 'POST':
        try:
            path = request.path
            inward_dtl = mAP.ap_model()
            jsondata = json.loads(request.body.decode('utf-8'))
            entity_gid = int(decry_data(request.session['Entity_gid']))
            employee_gid = int(decry_data(request.session['Emp_gid']))
            try:
                common.main_fun1(request.read(), path)
            except Exception as e:
                common.logger.error(e)
                return JsonResponse({"MESSAGE": "ERROR_OCCURED_ON_XML", "DATA": str(e)})

            inward_dtl.action = "GET"
            inward_dtl.type = "AP_ENTER_DETAIL_GET"
            ref_no = jsondata.get('params').get('status_json').get('ref_no')
            inward_dtl.filter = json.dumps({"entry_refno": ref_no, "entry_module": "AP"})
            inward_dtl.classification = json.dumps({"Entity_Gid": entity_gid})
            datas = inward_dtl.get_invoice_all()

            Fund_Transfer_Dtls_data = datas.get("entry_detail")[0]
            Fund_Transfer_Dtls_data = json.loads(Fund_Transfer_Dtls_data)
            orginal_data_frame = pd.DataFrame(Fund_Transfer_Dtls_data.get("Fund_Transfer_Dtls"))
            data_frame = pd.DataFrame(Fund_Transfer_Dtls_data.get("Fund_Transfer_Dtls"))
            data_frame['Amount'] = data_frame['Amount'].astype(float)
            Credit_amount = data_frame.loc[data_frame['Cr_Dr_Flag'] == 'C', 'Amount'].sum()
            Debit_amount = data_frame.loc[data_frame['Cr_Dr_Flag'] == 'D', 'Amount'].sum()
            Credit_amount = str(round(float(Credit_amount), 2))
            Debit_amount = str(round(float(Debit_amount), 2))
            if (Credit_amount == Debit_amount):

                Unique_Values = data_frame.Entry_refno.unique()
                Unique_Values_Length = len(Unique_Values)
                Final_Unique_Values = []
                for i in range(len(Unique_Values)):
                    Single_Unique_Values = Unique_Values[i]
                    Fetched_values = data_frame[(data_frame['Entry_refno'] == Single_Unique_Values)]
                    Final_send_data = orginal_data_frame[(orginal_data_frame['Entry_refno'] == Single_Unique_Values)]

                    send_Credit_amount = Fetched_values.loc[Fetched_values['Cr_Dr_Flag'] == 'C', 'Amount'].sum()
                    send_Debit_amount = Fetched_values.loc[Fetched_values['Cr_Dr_Flag'] == 'D', 'Amount'].sum()
                    send_Credit_amount = str(round(float(send_Credit_amount), 2))
                    send_Debit_amount = str(round(float(send_Debit_amount), 2))
                    if (send_Credit_amount == send_Debit_amount):
                        send_data = Final_send_data.to_json(orient='records')
                        send_data = json.loads(send_data)

                        branch_code = Fund_Transfer_Dtls_data.get("Fund_Transfer_Dtls")[0].get("Brn_Code")
                        CBSDATE = ""
                        NEFT_ACCOUNT_NUMBER = ""
                        # CBSDATE=Fund_Transfer_Dtls_data.get("Fund_Transfer_Dtls")[0].get("CBSDATE")
                        try:
                            # pass
                            CBSDATE_DATA = str(common.get_server_date("GET_CBSDATE_ACCOUNT_NUMBER")[0])
                            CBSDATE_DATA_LIST = CBSDATE_DATA.split(",")
                            NEFT_ACCOUNT_NUMBER = CBSDATE_DATA_LIST[0]
                            CBSDATE = CBSDATE_DATA_LIST[1]
                        except Exception as e:
                            common.logger.error(e)
                            return JsonResponse(
                                {"MESSAGE": "ERROR_OCCURED_ON_CBSDATE_AND_ACCOUNT_NUMBER_GET", "DATA": str(e)})

                        data = {"Src_Channel": "EMS", "ApplicationId": Single_Unique_Values,
                                "TransactionBranch": branch_code, "Txn_Date": CBSDATE, "productType": "DP",
                                "Fund_Transfer_Dtls": send_data}

                        try:
                            log_data = [{"BEFORE_AMOUNT_TRANSFER_API_DATA": data}]
                            common.logger.error(log_data)

                            data = json.dumps(data)
                            token_status = 1
                            generated_token_data = master_views.master_sync_Data_("GET", "get_data", employee_gid)
                            log_data = generated_token_data
                            token = generated_token_data.get("DATA")[0].get("clienttoken_name")
                            if (token == " " or token == None):
                                token_status = 0
                            if token_status == 1:
                                try:
                                    client_api = common.clientapi()
                                    headers = {"Content-Type": "application/json",
                                               "Authorization": "Bearer " + token}
                                    result = requests.post("" + client_api + "/nbfc/v1/mwr/amount-transfer",
                                                           headers=headers, data=data, verify=False)
                                    results = result.content.decode("utf-8")
                                    results_data = json.loads(results)
                                    log_data = [{"AFTER_AMOUNT_TRANSFER_API_DATA": results_data}]
                                    common.logger.error(log_data)

                                    ErrorStatus = results_data.get("CbsStatus")[0].get("ErrorMessage")
                                    ErrorCode = results_data.get("CbsStatus")[0].get("ErrorCode")
                                    if (ErrorStatus == "Success" and ErrorCode == '0'):
                                        CBSReferenceNo = results_data.get("CbsStatus")[0].get("CBSReferenceNo")
                                        try:
                                            count_values = i + 1
                                            Final_status = "ENTRY"
                                            if (count_values == len(Unique_Values)):
                                                Final_status = "APPROVED"
                                            Invoice_Header_Gid = jsondata.get('params').get('status_json').get(
                                                "Invoice_Header_Gid")
                                            inward_dtl.action = "UPDATE"
                                            inward_dtl.type = "INVOICE_HEADER_UPDATE"
                                            inward_dtl.header_json = {
                                                "HEADER": [{"Invoice_Header_Gid": Invoice_Header_Gid,
                                                            "refno": CBSReferenceNo, "status_": Final_status,
                                                            "crno": Single_Unique_Values}]}
                                            inward_dtl.debit_json = {}
                                            inward_dtl.detail_json = {}
                                            inward_dtl.status_json = {}
                                            inward_dtl.entity_gid = entity_gid
                                            inward_dtl.employee_gid = employee_gid
                                            outs = outputSplit(inward_dtl.set_Invoiceheader(), 1)
                                            if (outs == "SUCCESS"):
                                                Final_Unique_Values.append("SUCCESS")
                                                if (len(Final_Unique_Values) == len(Unique_Values)):
                                                    return JsonResponse(outs, safe=False)
                                            else:
                                                return JsonResponse(
                                                    {"MESSAGE": "ERROR_OCCURED_ON_INVOICE_HEADER_UPDATE", "DATA": outs})
                                        except Exception as e:
                                            common.logger.error(e)
                                            return JsonResponse(
                                                {"MESSAGE": "ERROR_OCCURED_ON_INVOICE_HEADER_UPDATE", "DATA": str(e)})
                                    else:
                                        return JsonResponse({"MESSAGE": "FAILED", "FAILED_STATUS": results_data})
                                except Exception as e:
                                    common.logger.error(e)
                                    return JsonResponse(
                                        {"MESSAGE": "ERROR_OCCURED_ON_AMOUNT_TRANSFER_CLINET_API", "DATA": str(e),
                                         "log_data": log_data})
                            else:
                                return JsonResponse(
                                    {"MESSAGE": "ERROR_OCCURED_ON_TOKEN_GENERATIONS OR INVALID AUTHENTICATONS"})
                        except Exception as e:
                            common.logger.error(e)
                            return JsonResponse(
                                {"MESSAGE": "ERROR_OCCURED_TOKEN_GENERATION", "DATA": str(e), "log_data": log_data})
                    else:
                        return JsonResponse({"MESSAGE": "Credit Amount and Debit Amount Not Equal"})
            else:
                return JsonResponse({"MESSAGE": "Credit Amount and Debit Amount Not Equal"})
        except Exception as e:
            common.logger.error(e)
            return JsonResponse({"MESSAGE": "ERROR_OCCURED_ON_ENTRY_DETAILS_GET", "DATA": str(e)})


def APpayment_set(request):
    utl.check_pointaccess(request)
    utl.check_authorization(request)
    if request.method == 'POST':
        try:
            path = request.path
            inward_dtl = mAP.ap_model()
            jsondata = json.loads(request.body.decode('utf-8'))
            common.main_fun1(request.read(), path)
            current_month = datetime.now().strftime('%m')
            current_day = datetime.now().strftime('%d')
            current_year_full = datetime.now().strftime('%Y')
            today_date = str(current_day + "/" + current_month + "/" + current_year_full)
            if (jsondata.get('params').get('action') == "Insert" and jsondata.get('params').get(
                    'type') == "PAYMENT_ADD"):
                header_json_data = jsondata.get('params').get('header_json').get('HEADER')
                detail_json_data = jsondata.get('params').get('detail_json').get('DETAILS')
                number_of_data = len(header_json_data)
                entity_gid = int(decry_data(request.session['Entity_gid']))
                employee_gid = int(decry_data(request.session['Emp_gid']))
                Final_Header_Status_Data = []
                for i in range(len(header_json_data)):
                    try:
                        execute = 1
                        header_data = {"HEADER": [header_json_data[i]]}
                        details_data = {"DETAILS": detail_json_data}
                        invoiceheader_gid = details_data.get("DETAILS")[0].get("invoiceheader_gid")
                        invoiceheader_status = details_data.get("DETAILS")[0].get("invoiceheader_status")
                        invoiceheader_crno = details_data.get("DETAILS")[0].get("invoiceheader_crno")
                        invoiceheader_invoiceno = details_data.get("DETAILS")[0].get("invoiceheader_invoiceno")
                        invoiceheader_dedupeinvoiceno = details_data.get("DETAILS")[0].get(
                            "invoiceheader_dedupeinvoiceno")
                        invoiceheader_remarks = details_data.get("DETAILS")[0].get("invoiceheader_remarks")
                        Header_Amount = header_data.get("HEADER")[0].get("Paymentheader_Amount")
                        Payment_Mode = header_data.get("HEADER")[0].get("Payment_Mode")
                        Payment_Mode_GL = header_data.get("HEADER")[0].get("paymode_glno")
                        Credit_DDtran_Branch = header_data.get("HEADER")[0].get("credit_ddtranbranch")
                        Credit_DDpay_Branch = header_data.get("HEADER")[0].get("credit_ddpaybranch")
                        header_data["HEADER"][0]["invoiceheader_gid"] = invoiceheader_gid
                        bank_details = header_data.get("HEADER")[0]
                        bankbranch_name = bank_details.get("bankbranch_name")
                        bankdetails_acno = bank_details.get("bankdetails_acno")
                        ifsccode = bank_details.get("ifsccode")
                        beneficiaryname = bank_details.get("beneficiaryname")
                        bank_name = details_data.get("DETAILS")[0].get("bank_name")

                        ap_statu_update_result = ""
                        try:
                            status_update_data = {"Invoice_Header_Gid": invoiceheader_gid, "entity_gid": entity_gid,
                                                  "employee_gid": employee_gid, "Status": "PAY INITIATED"}
                            ap_statu_update_result = AP_status_update(status_update_data)
                            if (ap_statu_update_result == "SUCCESS"):
                                pass
                            else:
                                return JsonResponse({"MESSAGE": "ERROR_OCCURED_ON_AP INITIATED_UPDATION",
                                                     "OUT": ap_statu_update_result})
                        except Exception as e:
                            common.logger.error(e)
                            return JsonResponse({"MESSAGE": "ERROR_OCCURED_ON_AP INITIATED_UPDATION", "DATA": str(e)})

                        out_put_data = "NOT_NEFT"
                        neft_status1=""
                        if (Payment_Mode == "NEFT"):
                            neft_status1="NEFT_PASS"
                            header_data_df = pd.DataFrame(detail_json_data)
                            NEFT_Header_Amount = round(
                                header_data_df.loc[header_data_df['paymode_name'] == 'NEFT', 'credit_amount'].sum(), 2)
                            if (
                                    bankbranch_name == None or bankdetails_acno == None or ifsccode == None and beneficiaryname == None):
                                execute = 0
                                Header_Status_Data = {"invoiceheader_crno": invoiceheader_crno,
                                                      "ERROR_MESSAGE": "MISSING_BANK_DETAILS"}
                                Final_Header_Status_Data.append(Header_Status_Data)
                        if (Payment_Mode == "DD"):
                            neft_status1="DD_PASS"
                            header_data_df = pd.DataFrame(detail_json_data)
                            DD_Header_Amount = round(
                                header_data_df.loc[header_data_df['paymode_name'] == 'DD', 'credit_amount'].sum(), 2)
                            if (beneficiaryname == None):
                                execute = 0
                                Header_Status_Data = {"invoiceheader_crno": invoiceheader_crno,
                                                      "ERROR_MESSAGE": "MISSING_BENEFICIARY_NAME"}
                                Final_Header_Status_Data.append(Header_Status_Data)
                            elif (Payment_Mode_GL == None):
                                execute = 0
                                Header_Status_Data = {"invoiceheader_crno": invoiceheader_crno,
                                                      "ERROR_MESSAGE": "MISSING_PAYMODE_GL_DETAILS"}
                                Final_Header_Status_Data.append(Header_Status_Data)
                            elif (
                                    Credit_DDpay_Branch == None or Credit_DDtran_Branch == None or Credit_DDpay_Branch == '0' or Credit_DDtran_Branch == '0'):
                                execute = 0
                                Header_Status_Data = {"invoiceheader_crno": invoiceheader_crno,
                                                      "ERROR_MESSAGE": "MISSING_PAYMODE_CREDIT_DD_PAYBRANCH OR CREDIT_DDTRAN_BRANCH"}
                                Final_Header_Status_Data.append(Header_Status_Data)
                        if (execute == 1):
                            try:
                                inward_dtl.action = jsondata.get('params').get('action')
                                inward_dtl.type = jsondata.get('params').get('type')
                                inward_dtl.header_json = header_data
                                inward_dtl.detail_json = details_data
                                inward_dtl.other_json = jsondata.get('params').get('other_json')
                                inward_dtl.status_json = jsondata.get('params').get('status_json')
                                inward_dtl.entity_gid = entity_gid
                                inward_dtl.employee_gid = employee_gid
                                out_put_data = inward_dtl.set_payment()
                                out_data = out_put_data[0].split(",")
                                pv_number = out_data[0]
                                out = out_data[1]
                                if (out == "SUCCESS" and jsondata.get("params").get('type') == "PAYMENT_ADD"):
                                    try:
                                        inward_dtl.action = "GET"
                                        inward_dtl.type = "AP_ENTER_DETAIL_GET"
                                        # ref_no = jsondata.get('params').get('status_json').get('ref_no')
                                        inward_dtl.filter = json.dumps(
                                            {"entry_refno": invoiceheader_crno, "entry_module": "PAYMENT"})
                                        inward_dtl.classification = json.dumps({"Entity_Gid": entity_gid})
                                        datas = inward_dtl.get_invoice_all()
                                        Fund_Transfer_Dtls_data = datas.get("entry_detail")[0]
                                        Fund_Transfer_Dtls_data = json.loads(Fund_Transfer_Dtls_data)
                                        branch_code = Fund_Transfer_Dtls_data.get("Fund_Transfer_Dtls")[0].get(
                                            "Brn_Code")
                                        branch_name = Fund_Transfer_Dtls_data.get("Fund_Transfer_Dtls")[0].get(
                                            "Brn_name")
                                        CBSDATE = ""
                                        NEFT_ACCOUNT_NUMBER = ""
                                        # CBSDATE=Fund_Transfer_Dtls_data.get("Fund_Transfer_Dtls")[0].get("CBSDATE")

                                        try:
                                            inward_dtl.action = "UPDATE"
                                            inward_dtl.type = "STATUS"
                                            inward_dtl.header_json = '{}'
                                            inward_dtl.debit_json = '{}'
                                            inward_dtl.detail_json = '{}'
                                            inward_dtl.status_json = {
                                                "Invoice_Header_Gid": invoiceheader_gid,
                                                "Status": "PAYMENT",
                                                "crno": invoiceheader_crno,
                                                "cbsno": "N", "pvno": invoiceheader_crno,
                                                "neftstatus": neft_status1}
                                            inward_dtl.entity_gid = entity_gid
                                            inward_dtl.employee_gid = employee_gid
                                            final_out = outputSplit(inward_dtl.set_Invoiceheader_status_update(), 1)
                                            return JsonResponse(final_out, safe=False)
                                        except Exception as e:
                                            return JsonResponse(
                                                {"MESSAGE": "ERROR_OCCURED_STATUS_UPDATE", "DATA": str(e)})


                                        try:
                                            # pass
                                            CBSDATE_DATA = str(common.get_server_date("GET_CBSDATE_ACCOUNT_NUMBER")[0])
                                            CBSDATE_DATA_LIST = CBSDATE_DATA.split(",")
                                            NEFT_ACCOUNT_NUMBER = CBSDATE_DATA_LIST[0]
                                            CBSDATE = CBSDATE_DATA_LIST[1]
                                        except Exception as e:
                                            common.logger.error(e)
                                            return JsonResponse(
                                                {"MESSAGE": "ERROR_OCCURED_ON_CBSDATE_AND_ACCOUNT_NUMBER_GET",
                                                 "DATA": str(e)})

                                        data = {"Src_Channel": "EMS", "ApplicationId": pv_number,
                                                "TransactionBranch": branch_code,
                                                "Txn_Date": CBSDATE, "productType": "DP",
                                                "Fund_Transfer_Dtls": Fund_Transfer_Dtls_data.get("Fund_Transfer_Dtls")}
                                        try:
                                            amount_transfer_message = ""
                                            if (invoiceheader_status != "TXN FAILED"):
                                                if (invoiceheader_status != "AMOUNT TRAN"):
                                                    log_data = [{"BEFORE_AMOUNT_TRANSFER_API_DATA": data}]
                                                    common.logger.error(log_data)
                                                    data = json.dumps(data)
                                                    token_status = 1
                                                    try:
                                                        generated_token_data = master_views.master_sync_Data_("GET",
                                                                                                              "get_data",
                                                                                                              employee_gid)
                                                    except Exception as e:
                                                        common.logger.error(e)
                                                        return JsonResponse(
                                                            {"MESSAGE": "ERROR_OCCURED_ON_TOKEN_GENERATION",
                                                             "DATA": str(e)})
                                                    log_data = generated_token_data
                                                    token = generated_token_data.get("DATA")[0].get("clienttoken_name")
                                                    if (token == " " or token == None):
                                                        token_status = 0
                                                    if token_status == 1:
                                                        try:
                                                            client_api = common.clientapi()
                                                            headers = {"Content-Type": "application/json",
                                                                       "Authorization": "Bearer " + token}
                                                            result = requests.post(
                                                                "" + client_api + "/nbfc/v1/mwr/amount-transfer",
                                                                headers=headers, data=data, verify=False)
                                                            results = result.content.decode("utf-8")
                                                            results_data = json.loads(results)
                                                            log_data = [
                                                                {"AFTER_AMOUNT_TRANSFER_API_DATA": results_data}]
                                                            common.logger.error(log_data)

                                                            ErrorStatus = results_data.get("CbsStatus")[0].get(
                                                                "ErrorMessage")
                                                            ErrorCode = results_data.get("CbsStatus")[0].get(
                                                                "ErrorCode")
                                                            if (ErrorStatus == "Success" and ErrorCode == '0'):
                                                                cbsno_ref_number = results_data.get("CbsStatus")[0].get(
                                                                    "CBSReferenceNo")
                                                                if (
                                                                        Payment_Mode == "KVBAC" or Payment_Mode == "BRA" or Payment_Mode == "ERA"):
                                                                    amount_transfer_message = "SUCCESS"
                                                                else:
                                                                    try:
                                                                        inward_dtl.action = "UPDATE"
                                                                        inward_dtl.type = "STATUS"
                                                                        inward_dtl.header_json = '{}'
                                                                        inward_dtl.debit_json = '{}'
                                                                        inward_dtl.detail_json = '{}'
                                                                        inward_dtl.status_json = {
                                                                            "Invoice_Header_Gid": invoiceheader_gid,
                                                                            "Status": "AMOUNT TRAN",
                                                                            "crno": invoiceheader_crno,
                                                                            "cbsno": cbsno_ref_number,
                                                                            "pvno": pv_number,
                                                                            "neftstatus": "TRAN_PASS"}
                                                                        inward_dtl.entity_gid = entity_gid
                                                                        inward_dtl.employee_gid = employee_gid
                                                                        final_out = outputSplit(
                                                                            inward_dtl.set_Invoiceheader_status_update(),
                                                                            1)
                                                                        if (final_out == "SUCCESS"):
                                                                            amount_transfer_message = "SUCCESS"
                                                                            pass
                                                                        else:
                                                                            return JsonResponse({
                                                                                                    "MESSAGE": "ERROR_OCCURED_ON_AMOUNT_TRN_SUCCESS_STATUS_UPDATE",
                                                                                                    "UPDATE_STATUS": final_out})
                                                                    except Exception as e:
                                                                        common.logger.error(e)
                                                                        return JsonResponse({
                                                                                                "MESSAGE": "ERROR_OCCURED_ON_AMOUNT_TRN_SUCCESS_STATUS_UPDATE",
                                                                                                "DATA": str(e)})
                                                            else:
                                                                return JsonResponse({"MESSAGE": "FAILED",
                                                                                     "FAILED_STATUS": results_data})
                                                        except Exception as e:
                                                            common.logger.error(e)
                                                            return JsonResponse(
                                                                {"MESSAGE": "ERROR_OCCURED_ON_AMOUNT_TRANSFER_API",
                                                                 "DATA": str(e)})
                                                    else:
                                                        return JsonResponse({
                                                                                "MESSAGE": "ERROR_OCCURED_ON_TOKEN_GENERATIONS OR INVALID AUTHENTICATONS",
                                                                                "TOKEN_LOG": log_data})
                                                else:
                                                    amount_transfer_message = "SUCCESS"
                                                    cbsno_ref_number = "N"
                                            else:
                                                amount_transfer_message = "SUCCESS"
                                                cbsno_ref_number = "N"
                                            if (amount_transfer_message == "SUCCESS"):
                                                if (Payment_Mode == "NEFT"):
                                                    default_paymode = "NEFT"
                                                    if (bank_name == "KARUR VYSYA BANK"):
                                                        default_paymode = "IFT"

                                                    neft_statu_update_result = ""
                                                    try:
                                                        neft_status_update_data = {
                                                            "Invoice_Header_Gid": invoiceheader_gid,
                                                            "entity_gid": entity_gid, "employee_gid": employee_gid,
                                                            "cbsno": cbsno_ref_number,
                                                            "pvno": pv_number, "Status": "NEFT INITIATED"}
                                                        neft_statu_update_result = AP_status_update(
                                                            neft_status_update_data)
                                                        if (neft_statu_update_result == "SUCCESS"):
                                                            pass
                                                        else:
                                                            return JsonResponse(
                                                                {"MESSAGE": "ERROR_OCCURED_ON_NEFT_INITIATED_UPDATION",
                                                                 "OUT": neft_statu_update_result})
                                                    except Exception as e:
                                                        common.logger.error(e)
                                                        return JsonResponse(
                                                            {"MESSAGE": "ERROR_OCCURED_ON_NEFT_INITIATED_UPDATION",
                                                             "DATA": str(e)})

                                                    data2 = {"productType": "DP", "ApplicationId": pv_number,
                                                             "FundTransferDetails": [{
                                                                 "PaymentMode": default_paymode,
                                                                 "ApplicationNumber": "11",
                                                                 "MobileNo": "1111111111",
                                                                 "AccountNo": NEFT_ACCOUNT_NUMBER,
                                                                 "Amount": str(NEFT_Header_Amount),
                                                                 "BenAcctNo": bankdetails_acno,
                                                                 "BenAcctType": "CA",
                                                                 "BenIFSC": ifsccode,
                                                                 "BenName": beneficiaryname,
                                                                 "Remarks": "Inv" + str(
                                                                     invoiceheader_dedupeinvoiceno) + " " + str(
                                                                     branch_code) + " " + str(branch_name),
                                                                 "RemitterMobileNo": "8072488536", "TranId": pv_number,
                                                                 "ApplicationDate": CBSDATE, "RetryFlag": "N"}]}
                                                    try:

                                                        log_data = [{"BEFORE_NEFT_PAYEMENT_API_DATA": data2}]
                                                        common.logger.error(log_data)

                                                        data = json.dumps(data2)
                                                        token_status = 1
                                                        try:
                                                            generated_token_data = master_views.master_sync_Data_("GET",
                                                                                                                  "get_data",
                                                                                                                  employee_gid)
                                                        except Exception as e:
                                                            common.logger.error(e)
                                                            return JsonResponse(
                                                                {"MESSAGE": "ERROR_OCCURED_ON_TOKEN_GENERATION",
                                                                 "DATA": str(e)})
                                                        log_data = generated_token_data
                                                        token = generated_token_data.get("DATA")[0].get(
                                                            "clienttoken_name")
                                                        if (token == " " or token == None):
                                                            token_status = 0
                                                        if token_status == 1:
                                                            try:
                                                                client_api = common.clientapi()
                                                                headers = {"Content-Type": "application/json",
                                                                           "Authorization": "Bearer " + token}
                                                                result = requests.post(
                                                                    "" + client_api + "/nbfc//v1/mwr/payment",
                                                                    headers=headers, data=data, verify=False)
                                                                results = result.content.decode("utf-8")
                                                                neft_results_data = json.loads(results)
                                                                log_data = [
                                                                    {"AFTER_NEFT_PAYEMENT_API_DATA": neft_results_data}]
                                                                common.logger.error(log_data)
                                                                if (neft_results_data.get(
                                                                        "ErrorMessage") == "Success" and neft_results_data.get(
                                                                        "ErrorCode") == '0'):
                                                                    try:
                                                                        inward_dtl.action = "UPDATE"
                                                                        inward_dtl.type = "STATUS"
                                                                        inward_dtl.header_json = '{}'
                                                                        inward_dtl.debit_json = '{}'
                                                                        inward_dtl.detail_json = '{}'
                                                                        inward_dtl.status_json = {
                                                                            "Invoice_Header_Gid": invoiceheader_gid,
                                                                            "Status": "PAYMENT",
                                                                            "crno": invoiceheader_crno,
                                                                            "cbsno": "N", "pvno": pv_number,
                                                                            "neftstatus": "NEFT_PASS"}
                                                                        inward_dtl.entity_gid = entity_gid
                                                                        inward_dtl.employee_gid = employee_gid
                                                                        final_out = outputSplit(
                                                                            inward_dtl.set_Invoiceheader_status_update(),
                                                                            1)
                                                                        return JsonResponse(final_out, safe=False)
                                                                    except Exception as e:
                                                                        return JsonResponse({
                                                                                                "MESSAGE": "ERROR_OCCURED_ON_NEFT_SUCCESS_STATUS_UPDATE",
                                                                                                "DATA": str(e)})
                                                                else:
                                                                    try:
                                                                        inward_dtl.action = "UPDATE"
                                                                        inward_dtl.type = "STATUS"
                                                                        inward_dtl.header_json = '{}'
                                                                        inward_dtl.debit_json = '{}'
                                                                        inward_dtl.detail_json = '{}'
                                                                        inward_dtl.status_json = {
                                                                            "Invoice_Header_Gid": invoiceheader_gid,
                                                                            "Status": "TXN FAILED",
                                                                            "crno": invoiceheader_crno,
                                                                            "cbsno": "N", "pvno": pv_number,
                                                                            "neftstatus": "NEFT_FAIL"}
                                                                        inward_dtl.entity_gid = entity_gid
                                                                        inward_dtl.employee_gid = employee_gid
                                                                        final_out = outputSplit(
                                                                            inward_dtl.set_Invoiceheader_status_update(),
                                                                            1)
                                                                        return JsonResponse(
                                                                            {"MESSAGE": "ERROR_OCCURED_ON_NEFT_API",
                                                                             "DATA": neft_results_data,
                                                                             "UPDATE_STATUS": final_out})
                                                                    except Exception as e:
                                                                        return JsonResponse({
                                                                                                "MESSAGE": "ERROR_OCCURED_ON_NEFT_NOT_SUCCESS_AND_STATUS_UPDATE",
                                                                                                "DATA": str(e)})
                                                            except Exception as e:
                                                                common.logger.error(e)
                                                                return JsonResponse(
                                                                    {"MESSAGE": "ERROR_OCCURED_ON_NEFT_API",
                                                                     "DATA": str(e)})
                                                        else:
                                                            return JsonResponse({
                                                                                    "MESSAGE": "ERROR_OCCURED_ON_TOKEN_GENERATIONS OR INVALID AUTHENTICATONS",
                                                                                    "TOKEN_LOG": log_data})
                                                    except Exception as e:
                                                        try:
                                                            inward_dtl.action = "UPDATE"
                                                            inward_dtl.type = "STATUS"
                                                            inward_dtl.header_json = '{}'
                                                            inward_dtl.debit_json = '{}'
                                                            inward_dtl.detail_json = '{}'
                                                            inward_dtl.status_json = {
                                                                "Invoice_Header_Gid": invoiceheader_gid,
                                                                "Status": "TXN FAILED", "crno": invoiceheader_crno,
                                                                "cbsno": "N", "pvno": pv_number,
                                                                "neftstatus": "NEFT_FAIL"}
                                                            inward_dtl.entity_gid = entity_gid
                                                            inward_dtl.employee_gid = employee_gid
                                                            final_out = outputSplit(
                                                                inward_dtl.set_Invoiceheader_status_update(), 1)
                                                            return JsonResponse(
                                                                {"MESSAGE": "ERROR_OCCURED_ON_NEFT_LOCAL_API",
                                                                 "DATA": str(e), "UPDATE_STATUS": final_out})

                                                        except Exception as e1:
                                                            common.logger.error(e1)
                                                            return JsonResponse({
                                                                                    "MESSAGE": "ERROR_OCCURED_ON_NEFT_LOCAL_API_AND_STATUS_UPDATE_FAILED",
                                                                                    "DATA": str(e1)})

                                                elif (Payment_Mode == "DD"):
                                                    dd_statu_update_result = ""
                                                    try:
                                                        dd_status_update_data = {
                                                            "Invoice_Header_Gid": invoiceheader_gid,
                                                            "entity_gid": entity_gid, "cbsno": cbsno_ref_number,
                                                            "pvno": pv_number, "employee_gid": employee_gid,
                                                            "Status": "DD INITIATED"}
                                                        dd_statu_update_result = AP_status_update(dd_status_update_data)
                                                        if (dd_statu_update_result == "SUCCESS"):
                                                            pass
                                                        else:
                                                            return JsonResponse(
                                                                {"MESSAGE": "ERROR_OCCURED_ON_DD_INITIATED_UPDATION",
                                                                 "OUT": dd_statu_update_result})
                                                    except Exception as e:
                                                        common.logger.error(e)
                                                        return JsonResponse(
                                                            {"MESSAGE": "ERROR_OCCURED_ON_DD_INITIATED_UPDATION",
                                                             "DATA": str(e)})

                                                    data3 = {"productType": "DP", "SrcChannel": "EMC-AG",
                                                             "Channel": "API",
                                                             "BankCode": "53",
                                                             "UserId": "SYSTELLER",
                                                             "serviceName": "DD_Payment_Api",
                                                             "ApplicationId": pv_number,
                                                             "TxnDate": CBSDATE,
                                                             "TransactionBranch": Credit_DDtran_Branch,
                                                             "DDPaymentDetails": [{
                                                                 "ApplicantId": pv_number,
                                                                 "AccountId": Payment_Mode_GL,
                                                                 "AccountInstrumentNumber": "",
                                                                 "BeneficiaryAddress": "sdfasdfsdfasdfa asd, sdfasdfas",
                                                                 "City": "Mumbai",
                                                                 "Country": "India",
                                                                 "State": "TN",
                                                                 "ZipCode": "600097",
                                                                 "BeneficiaryIdentification": "AIFPJ9987J",
                                                                 "BeneficiaryName": beneficiaryname,
                                                                 "InstrumentAmount": str(DD_Header_Amount),
                                                                 "IssueBankCode": "53",
                                                                 "Narrative": str(
                                                                     invoiceheader_dedupeinvoiceno) + " " + str(
                                                                     branch_name),
                                                                 "PayableBranch": Credit_DDpay_Branch,
                                                             }
                                                             ]
                                                             }

                                                    try:
                                                        log_data = [{"BEFORE_DD_PAYEMENT_API_DATA": data3}]
                                                        common.logger.error(log_data)

                                                        data = json.dumps(data3)
                                                        token_status = 1
                                                        try:
                                                            generated_token_data = master_views.master_sync_Data_("GET",
                                                                                                                  "get_data",
                                                                                                                  employee_gid)
                                                        except Exception as e:
                                                            common.logger.error(e)
                                                            return JsonResponse(
                                                                {"MESSAGE": "ERROR_OCCURED_ON_TOKEN_GENERATION",
                                                                 "DATA": str(e)})
                                                        log_data = generated_token_data
                                                        token = generated_token_data.get("DATA")[0].get(
                                                            "clienttoken_name")
                                                        if (token == " " or token == None):
                                                            token_status = 0
                                                        if token_status == 1:
                                                            try:
                                                                client_api = common.clientapi()
                                                                headers = {"Content-Type": "application/json",
                                                                           "Authorization": "Bearer " + token}
                                                                result = requests.post(
                                                                    "" + client_api + "/nbfc/v1/mwr/dd-payment",
                                                                    headers=headers, data=data, verify=False)
                                                                results = result.content.decode("utf-8")
                                                                dd_results_data = json.loads(results)
                                                                log_data = [
                                                                    {"AFTER_DD_PAYEMENT_API_DATA": dd_results_data}]
                                                                common.logger.error(log_data)
                                                                if (dd_results_data.get(
                                                                        "ErrorMessage") == "Success" and dd_results_data.get(
                                                                        "ErrorCode") == '0'):
                                                                    try:
                                                                        inward_dtl.action = "UPDATE"
                                                                        inward_dtl.type = "STATUS"
                                                                        inward_dtl.header_json = '{}'
                                                                        inward_dtl.debit_json = '{}'
                                                                        inward_dtl.detail_json = '{}'
                                                                        inward_dtl.status_json = {
                                                                            "Invoice_Header_Gid": invoiceheader_gid,
                                                                            "Status": "PAYMENT",
                                                                            "crno": invoiceheader_crno,
                                                                            "cbsno": "N", "pvno": pv_number,
                                                                            "neftstatus": "DD_PASS"}
                                                                        inward_dtl.entity_gid = entity_gid
                                                                        inward_dtl.employee_gid = employee_gid
                                                                        final_out = outputSplit(
                                                                            inward_dtl.set_Invoiceheader_status_update(),
                                                                            1)
                                                                        return JsonResponse(final_out, safe=False)
                                                                    except Exception as e:
                                                                        common.logger.error(e)
                                                                        return JsonResponse({
                                                                                                "MESSAGE": "ERROR_OCCURED_ON_DD_SUCCESS_STATUS_UPDATE",
                                                                                                "DATA": str(e)})
                                                                else:
                                                                    try:
                                                                        inward_dtl.action = "UPDATE"
                                                                        inward_dtl.type = "STATUS"
                                                                        inward_dtl.header_json = '{}'
                                                                        inward_dtl.debit_json = '{}'
                                                                        inward_dtl.detail_json = '{}'
                                                                        inward_dtl.status_json = {
                                                                            "Invoice_Header_Gid": invoiceheader_gid,
                                                                            "Status": "TXN FAILED",
                                                                            "crno": invoiceheader_crno,
                                                                            "cbsno": "N", "pvno": pv_number,
                                                                            "neftstatus": "DD_FAIL"}
                                                                        inward_dtl.entity_gid = entity_gid
                                                                        inward_dtl.employee_gid = employee_gid
                                                                        final_out = outputSplit(
                                                                            inward_dtl.set_Invoiceheader_status_update(),
                                                                            1)
                                                                        return JsonResponse(
                                                                            {"MESSAGE": "ERROR_OCCURED_ON_DD_API",
                                                                             "DATA": dd_results_data,
                                                                             "UPDATE_STATUS": final_out})
                                                                    except Exception as e:
                                                                        common.logger.error(e)
                                                                        return JsonResponse({
                                                                                                "MESSAGE": "ERROR_OCCURED_ON_DD_NOT_SUCCESS_AND_STATUS_UPDATE",
                                                                                                "DATA": str(e)})
                                                            except Exception as e:
                                                                try:
                                                                    inward_dtl.action = "UPDATE"
                                                                    inward_dtl.type = "STATUS"
                                                                    inward_dtl.header_json = '{}'
                                                                    inward_dtl.debit_json = '{}'
                                                                    inward_dtl.detail_json = '{}'
                                                                    inward_dtl.status_json = {
                                                                        "Invoice_Header_Gid": invoiceheader_gid,
                                                                        "Status": "TXN FAILED",
                                                                        "crno": invoiceheader_crno,
                                                                        "cbsno": "N", "pvno": pv_number,
                                                                        "neftstatus": "NEFT_FAIL"}
                                                                    inward_dtl.entity_gid = entity_gid
                                                                    inward_dtl.employee_gid = employee_gid
                                                                    final_out = outputSplit(
                                                                        inward_dtl.set_Invoiceheader_status_update(), 1)
                                                                    return JsonResponse(
                                                                        {"MESSAGE": "ERROR_OCCURED_ON_DD_API",
                                                                         "DATA": str(e), "UPDATE_STATUS": final_out})

                                                                except Exception as e1:
                                                                    common.logger.error(e1)
                                                                    return JsonResponse({
                                                                                            "MESSAGE": "ERROR_OCCURED_ON_DD_LOCAL_API_AND_STATUS_UPDATE_FAILED",
                                                                                            "DATA": str(e1)})
                                                        else:
                                                            return JsonResponse({
                                                                                    "MESSAGE": "ERROR_OCCURED_ON_TOKEN_GENERATIONS OR INVALID AUTHENTICATONS",
                                                                                    "TOKEN_LOG": log_data})
                                                    except Exception as e:
                                                        common.logger.error(e)
                                                        return JsonResponse(
                                                            {"MESSAGE": "ERROR_OCCURED_ON_DD_API", "DATA": str(e)})

                                                else:
                                                    try:
                                                        inward_dtl.action = "UPDATE"
                                                        inward_dtl.type = "STATUS"
                                                        inward_dtl.header_json = '{}'
                                                        inward_dtl.debit_json = '{}'
                                                        inward_dtl.detail_json = '{}'
                                                        inward_dtl.status_json = {
                                                            "Invoice_Header_Gid": invoiceheader_gid,
                                                            "Status": "PAYMENT",
                                                            "crno": invoiceheader_crno, "cbsno": cbsno_ref_number,
                                                            "pvno": pv_number, "neftstatus": "NOT_NEFT"}
                                                        inward_dtl.entity_gid = entity_gid
                                                        inward_dtl.employee_gid = employee_gid
                                                        final_out = outputSplit(
                                                            inward_dtl.set_Invoiceheader_status_update(), 1)
                                                        return JsonResponse(final_out, safe=False)
                                                    except Exception as e:
                                                        common.logger.error(e)
                                                        return JsonResponse({
                                                                                "MESSAGE": "ERROR_OCCURED_AMOUNT_TRANSFER_SUCCESS_FINAL_STATUS_UPDATE_FAILED",
                                                                                "DATA": str(e)})
                                            else:
                                                return JsonResponse({"MESSAGE": results_data})

                                        except Exception as e:
                                            common.logger.error(e)
                                            return JsonResponse(
                                                {"MESSAGE": "ERROR_OCCURED_ON_AMOUNT_TRANSFER_API", "DATA": str(e)})

                                    except Exception as e:
                                        common.logger.error(e)
                                        return JsonResponse(
                                            {"MESSAGE": "ERROR_OCCURED_AP_ENTER_DETAIL_GET", "DATA": str(e)})
                                else:
                                    return JsonResponse({"MESSAGE": out_put_data})
                            except Exception as e:
                                common.logger.error(e)
                                return JsonResponse(
                                    {"MESSAGE": "ERROR_OCCURED_ON_PAYMENT_INSERT", "PAYMENT_OUT_PUT": out_put_data,
                                     "DATA": str(e)})
                        else:
                            return JsonResponse(Final_Header_Status_Data, safe=False)

                    except Exception as e:
                        common.logger.error(e)
                        return JsonResponse({"MESSAGE": "ERROR_OCCURED_ON_BANK_DETAILS_GET", "DATA": str(e)})
            else:
                try:
                    inward_dtl.action = jsondata.get('params').get('action')
                    inward_dtl.type = jsondata.get('params').get('type')
                    inward_dtl.header_json = jsondata.get('params').get('header_json')
                    inward_dtl.detail_json = jsondata.get('params').get('detail_json')
                    inward_dtl.other_json = jsondata.get('params').get('other_json')
                    inward_dtl.status_json = jsondata.get('params').get('status_json')
                    inward_dtl.entity_gid = int(decry_data(request.session['Entity_gid']))
                    inward_dtl.employee_gid = int(decry_data(request.session['Emp_gid']))
                    out = outputSplit(inward_dtl.set_payment(), 1)
                    return JsonResponse(out, safe=False)
                except Exception as e:
                    common.logger.error(e)
                    return JsonResponse({"MESSAGE": "ERROR_OCCURED", "DATA": str(e)})

        except Exception as e:
            common.logger.error(e)
            return JsonResponse({"MESSAGE": "ERROR_OCCURED", "DATA": str(e)})


def APpayment_set_function(jsondata, employee_gid, entity_gid):
    try:
        inward_dtl = mAP.ap_model()
        current_month = datetime.now().strftime('%m')
        current_day = datetime.now().strftime('%d')
        current_year_full = datetime.now().strftime('%Y')
        today_date = str(current_day + "/" + current_month + "/" + current_year_full)
        if (jsondata.get('params').get('action') == "Insert" and jsondata.get('params').get('type') == "PAYMENT_ADD"):
            header_json_data = jsondata.get('params').get('header_json').get('HEADER')
            detail_json_data = jsondata.get('params').get('detail_json').get('DETAILS')
            number_of_data = len(header_json_data)

            Final_Header_Status_Data = []
            for i in range(len(header_json_data)):
                try:
                    execute = 1
                    header_data = {"HEADER": [header_json_data[i]]}
                    details_data = {"DETAILS": detail_json_data}
                    invoiceheader_gid = details_data.get("DETAILS")[0].get("invoiceheader_gid")
                    invoiceheader_status = details_data.get("DETAILS")[0].get("invoiceheader_status")
                    invoiceheader_crno = details_data.get("DETAILS")[0].get("invoiceheader_crno")
                    invoiceheader_invoiceno = details_data.get("DETAILS")[0].get("invoiceheader_invoiceno")
                    invoiceheader_remarks = details_data.get("DETAILS")[0].get("invoiceheader_remarks")
                    Header_Amount = header_data.get("HEADER")[0].get("Paymentheader_Amount")
                    Payment_Mode = header_data.get("HEADER")[0].get("Payment_Mode")
                    Payment_Mode_GL = header_data.get("HEADER")[0].get("paymode_glno")
                    Credit_DDtran_Branch = header_data.get("HEADER")[0].get("credit_ddtranbranch")
                    Credit_DDpay_Branch = header_data.get("HEADER")[0].get("credit_ddpaybranch")
                    header_data["HEADER"][0]["invoiceheader_gid"] = invoiceheader_gid
                    bank_details = header_data.get("HEADER")[0]
                    bankbranch_name = bank_details.get("bankbranch_name")
                    bankdetails_acno = bank_details.get("bankdetails_acno")
                    ifsccode = bank_details.get("ifsccode")
                    beneficiaryname = bank_details.get("beneficiaryname")
                    bank_name = details_data.get("DETAILS")[0].get("bank_name")

                    ap_statu_update_result = ""
                    try:
                        status_update_data = {"Invoice_Header_Gid": invoiceheader_gid, "entity_gid": entity_gid,
                                              "employee_gid": employee_gid, "Status": "PAY INITIATED"}
                        ap_statu_update_result = AP_status_update(status_update_data)
                        if (ap_statu_update_result == "SUCCESS"):
                            pass
                        else:
                            return JsonResponse(
                                {"MESSAGE": "ERROR_OCCURED_ON_AP INITIATED_UPDATION", "OUT": ap_statu_update_result})
                    except Exception as e:
                        common.logger.error(e)
                        return JsonResponse({"MESSAGE": "ERROR_OCCURED_ON_AP INITIATED_UPDATION", "DATA": str(e)})

                    out_put_data = ""
                    if (Payment_Mode == "NEFT"):
                        header_data_df = pd.DataFrame(detail_json_data)
                        NEFT_Header_Amount = round(
                            header_data_df.loc[header_data_df['paymode_name'] == 'NEFT', 'credit_amount'].sum(), 2)
                        if (
                                bankbranch_name == None or bankdetails_acno == None or ifsccode == None and beneficiaryname == None):
                            execute = 0
                            Header_Status_Data = {"invoiceheader_crno": invoiceheader_crno,
                                                  "ERROR_MESSAGE": "MISSING_BANK_DETAILS"}
                            Final_Header_Status_Data.append(Header_Status_Data)
                    if (Payment_Mode == "DD"):
                        header_data_df = pd.DataFrame(detail_json_data)
                        DD_Header_Amount = round(
                            header_data_df.loc[header_data_df['paymode_name'] == 'DD', 'credit_amount'].sum(), 2)
                        if (beneficiaryname == None):
                            execute = 0
                            Header_Status_Data = {"invoiceheader_crno": invoiceheader_crno,
                                                  "ERROR_MESSAGE": "MISSING_BENEFICIARY_NAME"}
                            Final_Header_Status_Data.append(Header_Status_Data)
                        elif (Payment_Mode_GL == None):
                            execute = 0
                            Header_Status_Data = {"invoiceheader_crno": invoiceheader_crno,
                                                  "ERROR_MESSAGE": "MISSING_PAYMODE_GL_DETAILS"}
                            Final_Header_Status_Data.append(Header_Status_Data)
                        elif (
                                Credit_DDpay_Branch == None or Credit_DDtran_Branch == None or Credit_DDpay_Branch == '0' or Credit_DDtran_Branch == '0'):
                            execute = 0
                            Header_Status_Data = {"invoiceheader_crno": invoiceheader_crno,
                                                  "ERROR_MESSAGE": "MISSING_PAYMODE_CREDIT_DD_PAYBRANCH OR CREDIT_DDTRAN_BRANCH"}
                            Final_Header_Status_Data.append(Header_Status_Data)
                    if (execute == 1):
                        try:
                            inward_dtl.action = jsondata.get('params').get('action')
                            inward_dtl.type = jsondata.get('params').get('type')
                            inward_dtl.header_json = header_data
                            inward_dtl.detail_json = details_data
                            inward_dtl.other_json = jsondata.get('params').get('other_json')
                            inward_dtl.status_json = jsondata.get('params').get('status_json')
                            inward_dtl.entity_gid = entity_gid
                            inward_dtl.employee_gid = employee_gid
                            out_put_data = inward_dtl.set_payment()
                            out_data = out_put_data[0].split(",")
                            pv_number = out_data[0]
                            out = out_data[1]
                            if (out == "SUCCESS" and jsondata.get("params").get('type') == "PAYMENT_ADD"):
                                try:
                                    inward_dtl.action = "GET"
                                    inward_dtl.type = "AP_ENTER_DETAIL_GET"
                                    # ref_no = jsondata.get('params').get('status_json').get('ref_no')
                                    inward_dtl.filter = json.dumps(
                                        {"entry_refno": invoiceheader_crno, "entry_module": "PAYMENT"})
                                    inward_dtl.classification = json.dumps({"Entity_Gid": entity_gid})
                                    datas = inward_dtl.get_invoice_all()
                                    Fund_Transfer_Dtls_data = datas.get("entry_detail")[0]
                                    Fund_Transfer_Dtls_data = json.loads(Fund_Transfer_Dtls_data)
                                    branch_code = Fund_Transfer_Dtls_data.get("Fund_Transfer_Dtls")[0].get("Brn_Code")
                                    branch_name = Fund_Transfer_Dtls_data.get("Fund_Transfer_Dtls")[0].get("Brn_name")
                                    CBSDATE = ""
                                    NEFT_ACCOUNT_NUMBER = ""
                                    # CBSDATE=Fund_Transfer_Dtls_data.get("Fund_Transfer_Dtls")[0].get("CBSDATE")
                                    try:
                                        # pass
                                        CBSDATE_DATA = str(common.get_server_date("GET_CBSDATE_ACCOUNT_NUMBER")[0])
                                        CBSDATE_DATA_LIST = CBSDATE_DATA.split(",")
                                        NEFT_ACCOUNT_NUMBER = CBSDATE_DATA_LIST[0]
                                        CBSDATE = CBSDATE_DATA_LIST[1]
                                    except Exception as e:
                                        common.logger.error(e)
                                        return JsonResponse(
                                            {"MESSAGE": "ERROR_OCCURED_ON_CBSDATE_AND_ACCOUNT_NUMBER_GET",
                                             "DATA": str(e)})

                                    data = {"Src_Channel": "EMS", "ApplicationId": pv_number,
                                            "TransactionBranch": branch_code,
                                            "Txn_Date": CBSDATE, "productType": "DP",
                                            "Fund_Transfer_Dtls": Fund_Transfer_Dtls_data.get("Fund_Transfer_Dtls")}
                                    try:
                                        amount_transfer_message = ""
                                        if (invoiceheader_status != "TXN FAILED"):
                                            if (invoiceheader_status != "AMOUNT TRAN"):
                                                log_data = [{"BEFORE_AMOUNT_TRANSFER_API_DATA": data}]
                                                common.logger.error(log_data)
                                                data = json.dumps(data)
                                                token_status = 1
                                                try:
                                                    generated_token_data = master_views.master_sync_Data_("GET",
                                                                                                          "get_data",
                                                                                                          employee_gid)
                                                except Exception as e:
                                                    common.logger.error(e)
                                                    return JsonResponse({"MESSAGE": "ERROR_OCCURED_ON_TOKEN_GENERATION",
                                                                         "DATA": str(e)})
                                                log_data = generated_token_data
                                                token = generated_token_data.get("DATA")[0].get("clienttoken_name")
                                                if (token == " " or token == None):
                                                    token_status = 0
                                                if token_status == 1:
                                                    try:
                                                        client_api = common.clientapi()
                                                        headers = {"Content-Type": "application/json",
                                                                   "Authorization": "Bearer " + token}
                                                        result = requests.post(
                                                            "" + client_api + "/nbfc/v1/mwr/amount-transfer",
                                                            headers=headers, data=data, verify=False)
                                                        results = result.content.decode("utf-8")
                                                        results_data = json.loads(results)
                                                        log_data = [{"AFTER_AMOUNT_TRANSFER_API_DATA": results_data}]
                                                        common.logger.error(log_data)

                                                        ErrorStatus = results_data.get("CbsStatus")[0].get(
                                                            "ErrorMessage")
                                                        ErrorCode = results_data.get("CbsStatus")[0].get("ErrorCode")
                                                        if (ErrorStatus == "Success" and ErrorCode == '0'):
                                                            cbsno_ref_number = results_data.get("CbsStatus")[0].get(
                                                                "CBSReferenceNo")
                                                            if (
                                                                    Payment_Mode == "KVBAC" or Payment_Mode == "BRA" or Payment_Mode == "ERA"):
                                                                amount_transfer_message = "SUCCESS"
                                                            else:
                                                                try:
                                                                    inward_dtl.action = "UPDATE"
                                                                    inward_dtl.type = "STATUS"
                                                                    inward_dtl.header_json = '{}'
                                                                    inward_dtl.debit_json = '{}'
                                                                    inward_dtl.detail_json = '{}'
                                                                    inward_dtl.status_json = {
                                                                        "Invoice_Header_Gid": invoiceheader_gid,
                                                                        "Status": "AMOUNT TRAN",
                                                                        "crno": invoiceheader_crno,
                                                                        "cbsno": cbsno_ref_number, "pvno": pv_number,
                                                                        "neftstatus": "TRAN_PASS"}
                                                                    inward_dtl.entity_gid = entity_gid
                                                                    inward_dtl.employee_gid = employee_gid
                                                                    final_out = outputSplit(
                                                                        inward_dtl.set_Invoiceheader_status_update(), 1)
                                                                    if (final_out == "SUCCESS"):
                                                                        amount_transfer_message = "SUCCESS"
                                                                        pass
                                                                    else:
                                                                        return JsonResponse({
                                                                                                "MESSAGE": "ERROR_OCCURED_ON_AMOUNT_TRN_SUCCESS_STATUS_UPDATE",
                                                                                                "UPDATE_STATUS": final_out})
                                                                except Exception as e:
                                                                    common.logger.error(e)
                                                                    return JsonResponse({
                                                                                            "MESSAGE": "ERROR_OCCURED_ON_AMOUNT_TRN_SUCCESS_STATUS_UPDATE",
                                                                                            "DATA": str(e)})
                                                        else:
                                                            return JsonResponse(
                                                                {"MESSAGE": "FAILED", "FAILED_STATUS": results_data})
                                                    except Exception as e:
                                                        common.logger.error(e)
                                                        return JsonResponse(
                                                            {"MESSAGE": "ERROR_OCCURED_ON_AMOUNT_TRANSFER_API",
                                                             "DATA": str(e)})
                                                else:
                                                    return JsonResponse({
                                                                            "MESSAGE": "ERROR_OCCURED_ON_TOKEN_GENERATIONS OR INVALID AUTHENTICATONS",
                                                                            "TOKEN_LOG": log_data})
                                            else:
                                                amount_transfer_message = "SUCCESS"
                                                cbsno_ref_number = "N"
                                        else:
                                            amount_transfer_message = "SUCCESS"
                                            cbsno_ref_number = "N"
                                        if (amount_transfer_message == "SUCCESS"):
                                            if (Payment_Mode == "NEFT"):
                                                default_paymode = "NEFT"
                                                if (bank_name == "KARUR VYSYA BANK"):
                                                    default_paymode = "IFT"

                                                neft_statu_update_result = ""
                                                try:
                                                    neft_status_update_data = {"Invoice_Header_Gid": invoiceheader_gid,
                                                                               "entity_gid": entity_gid,
                                                                               "employee_gid": employee_gid,
                                                                               "cbsno": cbsno_ref_number,
                                                                               "pvno": pv_number,
                                                                               "Status": "NEFT INITIATED"}
                                                    neft_statu_update_result = AP_status_update(neft_status_update_data)
                                                    if (neft_statu_update_result == "SUCCESS"):
                                                        pass
                                                    else:
                                                        return JsonResponse(
                                                            {"MESSAGE": "ERROR_OCCURED_ON_NEFT_INITIATED_UPDATION",
                                                             "OUT": neft_statu_update_result})
                                                except Exception as e:
                                                    common.logger.error(e)
                                                    return JsonResponse(
                                                        {"MESSAGE": "ERROR_OCCURED_ON_NEFT_INITIATED_UPDATION",
                                                         "DATA": str(e)})

                                                data2 = {"productType": "DP", "ApplicationId": pv_number,
                                                         "FundTransferDetails": [{
                                                             "PaymentMode": default_paymode,
                                                             "ApplicationNumber": "11",
                                                             "MobileNo": "1111111111",
                                                             "AccountNo": NEFT_ACCOUNT_NUMBER,
                                                             "Amount": str(NEFT_Header_Amount),
                                                             "BenAcctNo": bankdetails_acno,
                                                             "BenAcctType": "CA",
                                                             "BenIFSC": ifsccode,
                                                             "BenName": beneficiaryname,
                                                             "Remarks": "Inv" + str(
                                                                 invoiceheader_invoiceno) + " " + str(
                                                                 branch_code) + " " + str(branch_name),
                                                             "RemitterMobileNo": "8072488536", "TranId": pv_number,
                                                             "ApplicationDate": CBSDATE, "RetryFlag": "N"}]}
                                                try:

                                                    log_data = [{"BEFORE_NEFT_PAYEMENT_API_DATA": data2}]
                                                    common.logger.error(log_data)

                                                    data = json.dumps(data2)
                                                    token_status = 1
                                                    try:
                                                        generated_token_data = master_views.master_sync_Data_("GET",
                                                                                                              "get_data",
                                                                                                              employee_gid)
                                                    except Exception as e:
                                                        common.logger.error(e)
                                                        return JsonResponse(
                                                            {"MESSAGE": "ERROR_OCCURED_ON_TOKEN_GENERATION",
                                                             "DATA": str(e)})
                                                    log_data = generated_token_data
                                                    token = generated_token_data.get("DATA")[0].get("clienttoken_name")
                                                    if (token == " " or token == None):
                                                        token_status = 0
                                                    if token_status == 1:
                                                        try:
                                                            client_api = common.clientapi()
                                                            headers = {"Content-Type": "application/json",
                                                                       "Authorization": "Bearer " + token}
                                                            result = requests.post(
                                                                "" + client_api + "/nbfc//v1/mwr/payment",
                                                                headers=headers, data=data, verify=False)
                                                            results = result.content.decode("utf-8")
                                                            neft_results_data = json.loads(results)
                                                            log_data = [
                                                                {"AFTER_NEFT_PAYEMENT_API_DATA": neft_results_data}]
                                                            common.logger.error(log_data)
                                                            if (neft_results_data.get(
                                                                    "ErrorMessage") == "Success" and neft_results_data.get(
                                                                    "ErrorCode") == '0'):
                                                                try:
                                                                    inward_dtl.action = "UPDATE"
                                                                    inward_dtl.type = "STATUS"
                                                                    inward_dtl.header_json = '{}'
                                                                    inward_dtl.debit_json = '{}'
                                                                    inward_dtl.detail_json = '{}'
                                                                    inward_dtl.status_json = {
                                                                        "Invoice_Header_Gid": invoiceheader_gid,
                                                                        "Status": "PAYMENT", "crno": invoiceheader_crno,
                                                                        "cbsno": "N", "pvno": pv_number,
                                                                        "neftstatus": "NEFT_PASS"}
                                                                    inward_dtl.entity_gid = entity_gid
                                                                    inward_dtl.employee_gid = employee_gid
                                                                    final_out = outputSplit(
                                                                        inward_dtl.set_Invoiceheader_status_update(), 1)
                                                                    return JsonResponse(final_out, safe=False)
                                                                except Exception as e:
                                                                    return JsonResponse({
                                                                                            "MESSAGE": "ERROR_OCCURED_ON_NEFT_SUCCESS_STATUS_UPDATE",
                                                                                            "DATA": str(e)})
                                                            else:
                                                                try:
                                                                    inward_dtl.action = "UPDATE"
                                                                    inward_dtl.type = "STATUS"
                                                                    inward_dtl.header_json = '{}'
                                                                    inward_dtl.debit_json = '{}'
                                                                    inward_dtl.detail_json = '{}'
                                                                    inward_dtl.status_json = {
                                                                        "Invoice_Header_Gid": invoiceheader_gid,
                                                                        "Status": "TXN FAILED",
                                                                        "crno": invoiceheader_crno,
                                                                        "cbsno": "N", "pvno": pv_number,
                                                                        "neftstatus": "NEFT_FAIL"}
                                                                    inward_dtl.entity_gid = entity_gid
                                                                    inward_dtl.employee_gid = employee_gid
                                                                    final_out = outputSplit(
                                                                        inward_dtl.set_Invoiceheader_status_update(), 1)
                                                                    return JsonResponse(
                                                                        {"MESSAGE": "ERROR_OCCURED_ON_NEFT_API",
                                                                         "DATA": neft_results_data,
                                                                         "UPDATE_STATUS": final_out})
                                                                except Exception as e:
                                                                    return JsonResponse({
                                                                                            "MESSAGE": "ERROR_OCCURED_ON_NEFT_NOT_SUCCESS_AND_STATUS_UPDATE",
                                                                                            "DATA": str(e)})
                                                        except Exception as e:
                                                            common.logger.error(e)
                                                            return JsonResponse({"MESSAGE": "ERROR_OCCURED_ON_NEFT_API",
                                                                                 "DATA": str(e)})
                                                    else:
                                                        return JsonResponse({
                                                                                "MESSAGE": "ERROR_OCCURED_ON_TOKEN_GENERATIONS OR INVALID AUTHENTICATONS",
                                                                                "TOKEN_LOG": log_data})
                                                except Exception as e:
                                                    try:
                                                        inward_dtl.action = "UPDATE"
                                                        inward_dtl.type = "STATUS"
                                                        inward_dtl.header_json = '{}'
                                                        inward_dtl.debit_json = '{}'
                                                        inward_dtl.detail_json = '{}'
                                                        inward_dtl.status_json = {
                                                            "Invoice_Header_Gid": invoiceheader_gid,
                                                            "Status": "TXN FAILED", "crno": invoiceheader_crno,
                                                            "cbsno": "N", "pvno": pv_number, "neftstatus": "NEFT_FAIL"}
                                                        inward_dtl.entity_gid = entity_gid
                                                        inward_dtl.employee_gid = employee_gid
                                                        final_out = outputSplit(
                                                            inward_dtl.set_Invoiceheader_status_update(), 1)
                                                        return JsonResponse(
                                                            {"MESSAGE": "ERROR_OCCURED_ON_NEFT_LOCAL_API",
                                                             "DATA": str(e), "UPDATE_STATUS": final_out})

                                                    except Exception as e1:
                                                        common.logger.error(e1)
                                                        return JsonResponse({
                                                                                "MESSAGE": "ERROR_OCCURED_ON_NEFT_LOCAL_API_AND_STATUS_UPDATE_FAILED",
                                                                                "DATA": str(e1)})

                                            elif (Payment_Mode == "DD"):
                                                dd_statu_update_result = ""
                                                try:
                                                    dd_status_update_data = {"Invoice_Header_Gid": invoiceheader_gid,
                                                                             "entity_gid": entity_gid,
                                                                             "cbsno": cbsno_ref_number,
                                                                             "pvno": pv_number,
                                                                             "employee_gid": employee_gid,
                                                                             "Status": "DD INITIATED"}
                                                    dd_statu_update_result = AP_status_update(dd_status_update_data)
                                                    if (dd_statu_update_result == "SUCCESS"):
                                                        pass
                                                    else:
                                                        return JsonResponse(
                                                            {"MESSAGE": "ERROR_OCCURED_ON_DD_INITIATED_UPDATION",
                                                             "OUT": dd_statu_update_result})
                                                except Exception as e:
                                                    common.logger.error(e)
                                                    return JsonResponse(
                                                        {"MESSAGE": "ERROR_OCCURED_ON_DD_INITIATED_UPDATION",
                                                         "DATA": str(e)})

                                                data3 = {"productType": "DP", "SrcChannel": "EMC-AG",
                                                         "Channel": "API",
                                                         "BankCode": "53",
                                                         "UserId": "SYSTELLER",
                                                         "serviceName": "DD_Payment_Api",
                                                         "ApplicationId": pv_number,
                                                         "TxnDate": CBSDATE, "TransactionBranch": Credit_DDtran_Branch,
                                                         "DDPaymentDetails": [{
                                                             "ApplicantId": pv_number,
                                                             "AccountId": Payment_Mode_GL,
                                                             "AccountInstrumentNumber": "",
                                                             "BeneficiaryAddress": "sdfasdfsdfasdfa asd, sdfasdfas",
                                                             "City": "Mumbai",
                                                             "Country": "India",
                                                             "State": "TN",
                                                             "ZipCode": "600097",
                                                             "BeneficiaryIdentification": "AIFPJ9987J",
                                                             "BeneficiaryName": beneficiaryname,
                                                             "InstrumentAmount": str(DD_Header_Amount),
                                                             "IssueBankCode": "53",
                                                             "Narrative": str(invoiceheader_invoiceno) + " " + str(
                                                                 branch_name),
                                                             "PayableBranch": Credit_DDpay_Branch,
                                                         }
                                                         ]
                                                         }

                                                try:
                                                    log_data = [{"BEFORE_DD_PAYEMENT_API_DATA": data3}]
                                                    common.logger.error(log_data)

                                                    data = json.dumps(data3)
                                                    token_status = 1
                                                    try:
                                                        generated_token_data = master_views.master_sync_Data_("GET",
                                                                                                              "get_data",
                                                                                                              employee_gid)
                                                    except Exception as e:
                                                        common.logger.error(e)
                                                        return JsonResponse(
                                                            {"MESSAGE": "ERROR_OCCURED_ON_TOKEN_GENERATION",
                                                             "DATA": str(e)})
                                                    log_data = generated_token_data
                                                    token = generated_token_data.get("DATA")[0].get("clienttoken_name")
                                                    if (token == " " or token == None):
                                                        token_status = 0
                                                    if token_status == 1:
                                                        try:
                                                            client_api = common.clientapi()
                                                            headers = {"Content-Type": "application/json",
                                                                       "Authorization": "Bearer " + token}
                                                            result = requests.post(
                                                                "" + client_api + "/nbfc/v1/mwr/dd-payment",
                                                                headers=headers, data=data, verify=False)
                                                            results = result.content.decode("utf-8")
                                                            dd_results_data = json.loads(results)
                                                            log_data = [{"AFTER_DD_PAYEMENT_API_DATA": dd_results_data}]
                                                            common.logger.error(log_data)
                                                            if (dd_results_data.get(
                                                                    "ErrorMessage") == "Success" and dd_results_data.get(
                                                                    "ErrorCode") == '0'):
                                                                try:
                                                                    inward_dtl.action = "UPDATE"
                                                                    inward_dtl.type = "STATUS"
                                                                    inward_dtl.header_json = '{}'
                                                                    inward_dtl.debit_json = '{}'
                                                                    inward_dtl.detail_json = '{}'
                                                                    inward_dtl.status_json = {
                                                                        "Invoice_Header_Gid": invoiceheader_gid,
                                                                        "Status": "PAYMENT", "crno": invoiceheader_crno,
                                                                        "cbsno": "N", "pvno": pv_number,
                                                                        "neftstatus": "DD_PASS"}
                                                                    inward_dtl.entity_gid = entity_gid
                                                                    inward_dtl.employee_gid = employee_gid
                                                                    final_out = outputSplit(
                                                                        inward_dtl.set_Invoiceheader_status_update(), 1)
                                                                    return JsonResponse(final_out, safe=False)
                                                                except Exception as e:
                                                                    common.logger.error(e)
                                                                    return JsonResponse({
                                                                                            "MESSAGE": "ERROR_OCCURED_ON_DD_SUCCESS_STATUS_UPDATE",
                                                                                            "DATA": str(e)})
                                                            else:
                                                                try:
                                                                    inward_dtl.action = "UPDATE"
                                                                    inward_dtl.type = "STATUS"
                                                                    inward_dtl.header_json = '{}'
                                                                    inward_dtl.debit_json = '{}'
                                                                    inward_dtl.detail_json = '{}'
                                                                    inward_dtl.status_json = {
                                                                        "Invoice_Header_Gid": invoiceheader_gid,
                                                                        "Status": "TXN FAILED",
                                                                        "crno": invoiceheader_crno,
                                                                        "cbsno": "N", "pvno": pv_number,
                                                                        "neftstatus": "DD_FAIL"}
                                                                    inward_dtl.entity_gid = entity_gid
                                                                    inward_dtl.employee_gid = employee_gid
                                                                    final_out = outputSplit(
                                                                        inward_dtl.set_Invoiceheader_status_update(), 1)
                                                                    return JsonResponse(
                                                                        {"MESSAGE": "ERROR_OCCURED_ON_DD_API",
                                                                         "DATA": dd_results_data,
                                                                         "UPDATE_STATUS": final_out})
                                                                except Exception as e:
                                                                    common.logger.error(e)
                                                                    return JsonResponse({
                                                                                            "MESSAGE": "ERROR_OCCURED_ON_DD_NOT_SUCCESS_AND_STATUS_UPDATE",
                                                                                            "DATA": str(e)})
                                                        except Exception as e:
                                                            try:
                                                                inward_dtl.action = "UPDATE"
                                                                inward_dtl.type = "STATUS"
                                                                inward_dtl.header_json = '{}'
                                                                inward_dtl.debit_json = '{}'
                                                                inward_dtl.detail_json = '{}'
                                                                inward_dtl.status_json = {
                                                                    "Invoice_Header_Gid": invoiceheader_gid,
                                                                    "Status": "TXN FAILED", "crno": invoiceheader_crno,
                                                                    "cbsno": "N", "pvno": pv_number,
                                                                    "neftstatus": "NEFT_FAIL"}
                                                                inward_dtl.entity_gid = entity_gid
                                                                inward_dtl.employee_gid = employee_gid
                                                                final_out = outputSplit(
                                                                    inward_dtl.set_Invoiceheader_status_update(), 1)
                                                                return JsonResponse(
                                                                    {"MESSAGE": "ERROR_OCCURED_ON_DD_API",
                                                                     "DATA": str(e), "UPDATE_STATUS": final_out})

                                                            except Exception as e1:
                                                                common.logger.error(e1)
                                                                return JsonResponse({
                                                                                        "MESSAGE": "ERROR_OCCURED_ON_DD_LOCAL_API_AND_STATUS_UPDATE_FAILED",
                                                                                        "DATA": str(e1)})
                                                    else:
                                                        return JsonResponse({
                                                                                "MESSAGE": "ERROR_OCCURED_ON_TOKEN_GENERATIONS OR INVALID AUTHENTICATONS",
                                                                                "TOKEN_LOG": log_data})
                                                except Exception as e:
                                                    common.logger.error(e)
                                                    return JsonResponse(
                                                        {"MESSAGE": "ERROR_OCCURED_ON_DD_API", "DATA": str(e)})

                                            else:
                                                try:
                                                    inward_dtl.action = "UPDATE"
                                                    inward_dtl.type = "STATUS"
                                                    inward_dtl.header_json = '{}'
                                                    inward_dtl.debit_json = '{}'
                                                    inward_dtl.detail_json = '{}'
                                                    inward_dtl.status_json = {"Invoice_Header_Gid": invoiceheader_gid,
                                                                              "Status": "PAYMENT",
                                                                              "crno": invoiceheader_crno,
                                                                              "cbsno": cbsno_ref_number,
                                                                              "pvno": pv_number,
                                                                              "neftstatus": "NOT_NEFT"}
                                                    inward_dtl.entity_gid = entity_gid
                                                    inward_dtl.employee_gid = employee_gid
                                                    final_out = outputSplit(
                                                        inward_dtl.set_Invoiceheader_status_update(), 1)
                                                    return JsonResponse(final_out, safe=False)
                                                except Exception as e:
                                                    common.logger.error(e)
                                                    return JsonResponse({
                                                                            "MESSAGE": "ERROR_OCCURED_AMOUNT_TRANSFER_SUCCESS_FINAL_STATUS_UPDATE_FAILED",
                                                                            "DATA": str(e)})
                                        else:
                                            return JsonResponse({"MESSAGE": results_data})

                                    except Exception as e:
                                        common.logger.error(e)
                                        return JsonResponse(
                                            {"MESSAGE": "ERROR_OCCURED_ON_AMOUNT_TRANSFER_API", "DATA": str(e)})

                                except Exception as e:
                                    common.logger.error(e)
                                    return JsonResponse(
                                        {"MESSAGE": "ERROR_OCCURED_AP_ENTER_DETAIL_GET", "DATA": str(e)})
                            else:
                                return JsonResponse({"MESSAGE": out_put_data})
                        except Exception as e:
                            common.logger.error(e)
                            return JsonResponse(
                                {"MESSAGE": "ERROR_OCCURED_ON_PAYMENT_INSERT", "PAYMENT_OUT_PUT": out_put_data,
                                 "DATA": str(e)})
                    else:
                        return JsonResponse(Final_Header_Status_Data, safe=False)

                except Exception as e:
                    common.logger.error(e)
                    return JsonResponse({"MESSAGE": "ERROR_OCCURED_ON_BANK_DETAILS_GET", "DATA": str(e)})
        else:
            try:
                inward_dtl.action = jsondata.get('params').get('action')
                inward_dtl.type = jsondata.get('params').get('type')
                inward_dtl.header_json = jsondata.get('params').get('header_json')
                inward_dtl.detail_json = jsondata.get('params').get('detail_json')
                inward_dtl.other_json = jsondata.get('params').get('other_json')
                inward_dtl.status_json = jsondata.get('params').get('status_json')
                inward_dtl.entity_gid = entity_gid
                inward_dtl.employee_gid = employee_gid
                out = outputSplit(inward_dtl.set_payment(), 1)
                return JsonResponse(out, safe=False)
            except Exception as e:
                common.logger.error(e)
                return JsonResponse({"MESSAGE": "ERROR_OCCURED", "DATA": str(e)})

    except Exception as e:
        common.logger.error(e)
        return JsonResponse({"MESSAGE": "ERROR_OCCURED", "DATA": str(e)})


def APpayment_set_function_approve_and_pay(jsondata, employee_gid, entity_gid):
    try:
        inward_dtl = mAP.ap_model()
        current_month = datetime.now().strftime('%m')
        current_day = datetime.now().strftime('%d')
        current_year_full = datetime.now().strftime('%Y')
        today_date = str(current_day + "/" + current_month + "/" + current_year_full)
        if (jsondata.get('params').get('action') == "Insert" and jsondata.get('params').get('type') == "PAYMENT_ADD"):
            header_json_data = jsondata.get('params').get('header_json').get('HEADER')
            detail_json_data = jsondata.get('params').get('detail_json').get('DETAILS')
            number_of_data = len(header_json_data)

            Final_Header_Status_Data = []
            for i in range(len(header_json_data)):
                try:
                    execute = 1
                    header_data = {"HEADER": [header_json_data[i]]}
                    details_data = {"DETAILS": detail_json_data}
                    invoiceheader_gid = details_data.get("DETAILS")[0].get("invoiceheader_gid")
                    invoiceheader_status = details_data.get("DETAILS")[0].get("invoiceheader_status")
                    invoiceheader_crno = details_data.get("DETAILS")[0].get("invoiceheader_crno")
                    invoiceheader_invoiceno = details_data.get("DETAILS")[0].get("invoiceheader_invoiceno")
                    invoiceheader_dedupeinvoiceno = details_data.get("DETAILS")[0].get("invoiceheader_dedupeinvoiceno")
                    invoiceheader_remarks = details_data.get("DETAILS")[0].get("invoiceheader_remarks")
                    Header_Amount = header_data.get("HEADER")[0].get("Paymentheader_Amount")
                    Payment_Mode = header_data.get("HEADER")[0].get("Payment_Mode")
                    Payment_Mode_GL = header_data.get("HEADER")[0].get("paymode_glno")
                    Credit_DDtran_Branch = header_data.get("HEADER")[0].get("credit_ddtranbranch")
                    Credit_DDpay_Branch = header_data.get("HEADER")[0].get("credit_ddpaybranch")
                    header_data["HEADER"][0]["invoiceheader_gid"] = invoiceheader_gid
                    bank_details = header_data.get("HEADER")[0]
                    bankbranch_name = bank_details.get("bankbranch_name")
                    bankdetails_acno = bank_details.get("bankdetails_acno")
                    ifsccode = bank_details.get("ifsccode")
                    beneficiaryname = bank_details.get("beneficiaryname")
                    bank_name = details_data.get("DETAILS")[0].get("bank_name")

                    ap_statu_update_result = ""
                    try:
                        status_update_data = {"Invoice_Header_Gid": invoiceheader_gid, "entity_gid": entity_gid,
                                              "employee_gid": employee_gid, "Status": "PAY INITIATED"}
                        ap_statu_update_result = AP_status_update(status_update_data)
                        if (ap_statu_update_result == "SUCCESS"):
                            out_put_data = ""
                            if (Payment_Mode == "NEFT"):
                                header_data_df = pd.DataFrame(detail_json_data)
                                NEFT_Header_Amount = round(
                                    header_data_df.loc[header_data_df['paymode_name'] == 'NEFT', 'credit_amount'].sum(),
                                    2)
                                if (
                                        bankbranch_name == None or bankdetails_acno == None or ifsccode == None and beneficiaryname == None):
                                    execute = 0
                                    Header_Status_Data = {"invoiceheader_crno": invoiceheader_crno,
                                                          "ERROR_MESSAGE": "MISSING_BANK_DETAILS"}
                                    Final_Header_Status_Data.append(Header_Status_Data)
                            if (Payment_Mode == "DD"):
                                header_data_df = pd.DataFrame(detail_json_data)
                                DD_Header_Amount = round(
                                    header_data_df.loc[header_data_df['paymode_name'] == 'DD', 'credit_amount'].sum(),
                                    2)
                                if (beneficiaryname == None):
                                    execute = 0
                                    Header_Status_Data = {"invoiceheader_crno": invoiceheader_crno,
                                                          "ERROR_MESSAGE": "MISSING_BENEFICIARY_NAME"}
                                    Final_Header_Status_Data.append(Header_Status_Data)
                                elif (Payment_Mode_GL == None):
                                    execute = 0
                                    Header_Status_Data = {"invoiceheader_crno": invoiceheader_crno,
                                                          "ERROR_MESSAGE": "MISSING_PAYMODE_GL_DETAILS"}
                                    Final_Header_Status_Data.append(Header_Status_Data)
                                elif (
                                        Credit_DDpay_Branch == None or Credit_DDtran_Branch == None or Credit_DDpay_Branch == '0' or Credit_DDtran_Branch == '0'):
                                    execute = 0
                                    Header_Status_Data = {"invoiceheader_crno": invoiceheader_crno,
                                                          "ERROR_MESSAGE": "MISSING_PAYMODE_CREDIT_DD_PAYBRANCH OR CREDIT_DDTRAN_BRANCH"}
                                    Final_Header_Status_Data.append(Header_Status_Data)
                            if (execute == 1):
                                try:
                                    inward_dtl.action = jsondata.get('params').get('action')
                                    inward_dtl.type = jsondata.get('params').get('type')
                                    inward_dtl.header_json = header_data
                                    inward_dtl.detail_json = details_data
                                    inward_dtl.other_json = jsondata.get('params').get('other_json')
                                    inward_dtl.status_json = jsondata.get('params').get('status_json')
                                    inward_dtl.entity_gid = entity_gid
                                    inward_dtl.employee_gid = employee_gid
                                    out_put_data = inward_dtl.set_payment()
                                    out_data = out_put_data[0].split(",")
                                    pv_number = out_data[0]
                                    out = out_data[1]
                                    if (out == "SUCCESS" and jsondata.get("params").get('type') == "PAYMENT_ADD"):
                                        try:
                                            inward_dtl.action = "GET"
                                            inward_dtl.type = "AP_ENTER_DETAIL_GET"
                                            # ref_no = jsondata.get('params').get('status_json').get('ref_no')
                                            inward_dtl.filter = json.dumps(
                                                {"entry_refno": invoiceheader_crno, "entry_module": "PAYMENT"})
                                            inward_dtl.classification = json.dumps({"Entity_Gid": entity_gid})
                                            datas = inward_dtl.get_invoice_all()
                                            Fund_Transfer_Dtls_data = datas.get("entry_detail")[0]
                                            Fund_Transfer_Dtls_data = json.loads(Fund_Transfer_Dtls_data)
                                            branch_code = Fund_Transfer_Dtls_data.get("Fund_Transfer_Dtls")[0].get(
                                                "Brn_Code")
                                            branch_name = Fund_Transfer_Dtls_data.get("Fund_Transfer_Dtls")[0].get(
                                                "Brn_name")
                                            CBSDATE = ""
                                            NEFT_ACCOUNT_NUMBER = ""
                                            # CBSDATE=Fund_Transfer_Dtls_data.get("Fund_Transfer_Dtls")[0].get("CBSDATE")
                                            try:
                                                # pass
                                                CBSDATE_DATA = str(
                                                    common.get_server_date("GET_CBSDATE_ACCOUNT_NUMBER")[0])
                                                CBSDATE_DATA_LIST = CBSDATE_DATA.split(",")
                                                NEFT_ACCOUNT_NUMBER = CBSDATE_DATA_LIST[0]
                                                CBSDATE = CBSDATE_DATA_LIST[1]
                                            except Exception as e:
                                                common.logger.error(e)
                                                pass
                                                # return JsonResponse({"MESSAGE": "ERROR_OCCURED_ON_CBSDATE_AND_ACCOUNT_NUMBER_GET","DATA": str(e)})

                                            data = {"Src_Channel": "EMS", "ApplicationId": pv_number,
                                                    "TransactionBranch": branch_code,
                                                    "Txn_Date": CBSDATE, "productType": "DP",
                                                    "Fund_Transfer_Dtls": Fund_Transfer_Dtls_data.get(
                                                        "Fund_Transfer_Dtls")}
                                            try:
                                                amount_transfer_message = ""
                                                if (invoiceheader_status != "TXN FAILED"):
                                                    if (invoiceheader_status != "AMOUNT TRAN"):
                                                        log_data = [{"BEFORE_AMOUNT_TRANSFER_API_DATA": data}]
                                                        common.logger.error(log_data)
                                                        data = json.dumps(data)
                                                        token_status = 1
                                                        try:
                                                            generated_token_data = master_views.master_sync_Data_("GET",
                                                                                                                  "get_data",
                                                                                                                  employee_gid)
                                                        except Exception as e:
                                                            common.logger.error(e)
                                                            pass
                                                            # return JsonResponse({"MESSAGE": "ERROR_OCCURED_ON_TOKEN_GENERATION","DATA": str(e)})
                                                        log_data = generated_token_data
                                                        token = generated_token_data.get("DATA")[0].get(
                                                            "clienttoken_name")
                                                        if (token == " " or token == None):
                                                            token_status = 0
                                                        if token_status == 1:
                                                            try:
                                                                client_api = common.clientapi()
                                                                headers = {"Content-Type": "application/json",
                                                                           "Authorization": "Bearer " + token}
                                                                result = requests.post(
                                                                    "" + client_api + "/nbfc/v1/mwr/amount-transfer",
                                                                    headers=headers, data=data, verify=False)
                                                                results = result.content.decode("utf-8")
                                                                results_data = json.loads(results)
                                                                log_data = [
                                                                    {"AFTER_AMOUNT_TRANSFER_API_DATA": results_data}]
                                                                common.logger.error(log_data)

                                                                ErrorStatus = results_data.get("CbsStatus")[0].get(
                                                                    "ErrorMessage")
                                                                ErrorCode = results_data.get("CbsStatus")[0].get(
                                                                    "ErrorCode")
                                                                if (ErrorStatus == "Success" and ErrorCode == '0'):
                                                                    cbsno_ref_number = results_data.get("CbsStatus")[
                                                                        0].get("CBSReferenceNo")
                                                                    if (
                                                                            Payment_Mode == "KVBAC" or Payment_Mode == "BRA" or Payment_Mode == "ERA"):
                                                                        amount_transfer_message = "SUCCESS"
                                                                    else:
                                                                        try:
                                                                            inward_dtl.action = "UPDATE"
                                                                            inward_dtl.type = "STATUS"
                                                                            inward_dtl.header_json = '{}'
                                                                            inward_dtl.debit_json = '{}'
                                                                            inward_dtl.detail_json = '{}'
                                                                            inward_dtl.status_json = {
                                                                                "Invoice_Header_Gid": invoiceheader_gid,
                                                                                "Status": "AMOUNT TRAN",
                                                                                "crno": invoiceheader_crno,
                                                                                "cbsno": cbsno_ref_number,
                                                                                "pvno": pv_number,
                                                                                "neftstatus": "TRAN_PASS"}
                                                                            inward_dtl.entity_gid = entity_gid
                                                                            inward_dtl.employee_gid = employee_gid
                                                                            final_out = outputSplit(
                                                                                inward_dtl.set_Invoiceheader_status_update(),
                                                                                1)
                                                                            if (final_out == "SUCCESS"):
                                                                                amount_transfer_message = "SUCCESS"
                                                                                pass
                                                                            else:
                                                                                header_update_data = {
                                                                                    "Invoice_Header_Gid": invoiceheader_gid,
                                                                                    "entity_gid": entity_gid,
                                                                                    "type": "ERROR_UPDATE",
                                                                                    "employee_gid": employee_gid,
                                                                                    "Error_log": {
                                                                                        "MESSAGE": "ERROR_OCCURED_ON_AMOUNT_TRN_SUCCESS_STATUS_UPDATE",
                                                                                        "UPDATE_STATUS": final_out}}
                                                                                AP_Header_Update_result = AP_Header_Update(
                                                                                    header_update_data)
                                                                                # return JsonResponse({"MESSAGE": "ERROR_OCCURED_ON_AMOUNT_TRN_SUCCESS_STATUS_UPDATE","UPDATE_STATUS": final_out})
                                                                        except Exception as e:
                                                                            common.logger.error(e)
                                                                            header_update_data = {
                                                                                "Invoice_Header_Gid": invoiceheader_gid,
                                                                                "entity_gid": entity_gid,
                                                                                "type": "ERROR_UPDATE",
                                                                                "employee_gid": employee_gid,
                                                                                "Error_log": {
                                                                                    "MESSAGE": "ERROR_OCCURED_ON_AMOUNT_TRN_SUCCESS_STATUS_UPDATE_",
                                                                                    "DATA": str(e)}}
                                                                            AP_Header_Update_result = AP_Header_Update(
                                                                                header_update_data)
                                                                            # return JsonResponse({"MESSAGE": "ERROR_OCCURED_ON_AMOUNT_TRN_SUCCESS_STATUS_UPDATE","DATA": str(e)})
                                                                            # pass
                                                                else:
                                                                    header_update_data = {
                                                                        "Invoice_Header_Gid": invoiceheader_gid,
                                                                        "entity_gid": entity_gid,
                                                                        "type": "ERROR_UPDATE",
                                                                        "employee_gid": employee_gid,
                                                                        "Error_log": {"MESSAGE": "FAILED",
                                                                                      "FAILED_STATUS": {
                                                                                          "MESSAGE": "FAILED",
                                                                                          "FAILED_STATUS": results_data}}}
                                                                    AP_Header_Update_result = AP_Header_Update(
                                                                        header_update_data)
                                                                    # return JsonResponse({"MESSAGE": "FAILED", "FAILED_STATUS": results_data})
                                                                    pass
                                                            except Exception as e:
                                                                common.logger.error(e)
                                                                header_update_data = {
                                                                    "Invoice_Header_Gid": invoiceheader_gid,
                                                                    "entity_gid": entity_gid,
                                                                    "type": "ERROR_UPDATE",
                                                                    "employee_gid": employee_gid, "Error_log": {
                                                                        "MESSAGE": "ERROR_OCCURED_ON_AMOUNT_TRANSFER_API_",
                                                                        "DATA": str(e)}}
                                                                AP_Header_Update_result = AP_Header_Update(
                                                                    header_update_data)
                                                                # return JsonResponse({"MESSAGE": "ERROR_OCCURED_ON_AMOUNT_TRANSFER_API","DATA": str(e)})

                                                        else:
                                                            # return JsonResponse({"MESSAGE": "ERROR_OCCURED_ON_TOKEN_GENERATIONS OR INVALID AUTHENTICATONS","TOKEN_LOG": log_data})
                                                            pass
                                                    else:
                                                        amount_transfer_message = "SUCCESS"
                                                        cbsno_ref_number = "N"
                                                else:
                                                    amount_transfer_message = "SUCCESS"
                                                    cbsno_ref_number = "N"
                                                if (amount_transfer_message == "SUCCESS"):
                                                    if (Payment_Mode == "NEFT"):
                                                        default_paymode = "NEFT"
                                                        if (bank_name == "KARUR VYSYA BANK"):
                                                            default_paymode = "IFT"

                                                        neft_statu_update_result = ""
                                                        try:
                                                            neft_status_update_data = {
                                                                "Invoice_Header_Gid": invoiceheader_gid,
                                                                "entity_gid": entity_gid,
                                                                "employee_gid": employee_gid,
                                                                "cbsno": cbsno_ref_number,
                                                                "pvno": pv_number,
                                                                "Status": "NEFT INITIATED"}
                                                            neft_statu_update_result = AP_status_update(
                                                                neft_status_update_data)
                                                            if (neft_statu_update_result == "SUCCESS"):
                                                                pass
                                                            else:
                                                                header_update_data = {
                                                                    "Invoice_Header_Gid": invoiceheader_gid,
                                                                    "entity_gid": entity_gid,
                                                                    "type": "ERROR_UPDATE",
                                                                    "employee_gid": employee_gid,
                                                                    "Error_log": {
                                                                        "MESSAGE": "ERROR_OCCURED_ON_NEFT_INITIATED_UPDATION",
                                                                        "OUT": neft_statu_update_result}}
                                                                AP_Header_Update_result = AP_Header_Update(
                                                                    header_update_data)
                                                                # return JsonResponse({"MESSAGE": "ERROR_OCCURED_ON_NEFT_INITIATED_UPDATION","OUT": neft_statu_update_result})
                                                        except Exception as e:
                                                            common.logger.error(e)
                                                            header_update_data = {
                                                                "Invoice_Header_Gid": invoiceheader_gid,
                                                                "entity_gid": entity_gid,
                                                                "type": "ERROR_UPDATE",
                                                                "employee_gid": employee_gid,
                                                                "Error_log": {
                                                                    "MESSAGE": "ERROR_OCCURED_ON_NEFT_INITIATED_UPDATION",
                                                                    "DATA": str(e)}}
                                                            AP_Header_Update_result = AP_Header_Update(
                                                                header_update_data)
                                                            # return JsonResponse({"MESSAGE": "ERROR_OCCURED_ON_NEFT_INITIATED_UPDATION","DATA": str(e)})

                                                        data2 = {"productType": "DP", "ApplicationId": pv_number,
                                                                 "FundTransferDetails": [{
                                                                     "PaymentMode": default_paymode,
                                                                     "ApplicationNumber": "11",
                                                                     "MobileNo": "1111111111",
                                                                     "AccountNo": NEFT_ACCOUNT_NUMBER,
                                                                     "Amount": str(NEFT_Header_Amount),
                                                                     "BenAcctNo": bankdetails_acno,
                                                                     "BenAcctType": "CA",
                                                                     "BenIFSC": ifsccode,
                                                                     "BenName": beneficiaryname,
                                                                     "Remarks": "Inv" + str(
                                                                         invoiceheader_dedupeinvoiceno) + " " + str(
                                                                         branch_code) + " " + str(branch_name),
                                                                     "RemitterMobileNo": "8072488536",
                                                                     "TranId": pv_number,
                                                                     "ApplicationDate": CBSDATE, "RetryFlag": "N"}]}
                                                        try:

                                                            log_data = [{"BEFORE_NEFT_PAYEMENT_API_DATA": data2}]
                                                            common.logger.error(log_data)

                                                            data = json.dumps(data2)
                                                            token_status = 1
                                                            try:
                                                                generated_token_data = master_views.master_sync_Data_(
                                                                    "GET",
                                                                    "get_data",
                                                                    employee_gid)
                                                            except Exception as e:
                                                                common.logger.error(e)
                                                                # return JsonResponse({"MESSAGE": "ERROR_OCCURED_ON_TOKEN_GENERATION","DATA": str(e)})
                                                                pass
                                                            log_data = generated_token_data
                                                            token = generated_token_data.get("DATA")[0].get(
                                                                "clienttoken_name")
                                                            if (token == " " or token == None):
                                                                token_status = 0
                                                            if token_status == 1:
                                                                try:
                                                                    client_api = common.clientapi()
                                                                    headers = {"Content-Type": "application/json",
                                                                               "Authorization": "Bearer " + token}
                                                                    result = requests.post(
                                                                        "" + client_api + "/nbfc//v1/mwr/payment",
                                                                        headers=headers, data=data, verify=False)
                                                                    results = result.content.decode("utf-8")
                                                                    neft_results_data = json.loads(results)
                                                                    log_data = [
                                                                        {
                                                                            "AFTER_NEFT_PAYEMENT_API_DATA": neft_results_data}]
                                                                    common.logger.error(log_data)
                                                                    if (neft_results_data.get(
                                                                            "ErrorMessage") == "Success" and neft_results_data.get(
                                                                        "ErrorCode") == '0'):
                                                                        try:
                                                                            inward_dtl.action = "UPDATE"
                                                                            inward_dtl.type = "STATUS"
                                                                            inward_dtl.header_json = '{}'
                                                                            inward_dtl.debit_json = '{}'
                                                                            inward_dtl.detail_json = '{}'
                                                                            inward_dtl.status_json = {
                                                                                "Invoice_Header_Gid": invoiceheader_gid,
                                                                                "Status": "PAYMENT",
                                                                                "crno": invoiceheader_crno,
                                                                                "cbsno": "N", "pvno": pv_number,
                                                                                "neftstatus": "NEFT_PASS"}
                                                                            inward_dtl.entity_gid = entity_gid
                                                                            inward_dtl.employee_gid = employee_gid
                                                                            final_out = outputSplit(
                                                                                inward_dtl.set_Invoiceheader_status_update(),
                                                                                1)
                                                                            return JsonResponse(final_out, safe=False)
                                                                        except Exception as e:
                                                                            header_update_data = {
                                                                                "Invoice_Header_Gid": invoiceheader_gid,
                                                                                "entity_gid": entity_gid,
                                                                                "type": "ERROR_UPDATE",
                                                                                "employee_gid": employee_gid,
                                                                                "Error_log": {
                                                                                    "MESSAGE": "ERROR_OCCURED_ON_NEFT_SUCCESS_STATUS_UPDATE",
                                                                                    "DATA": str(e)}}
                                                                            AP_Header_Update_result = AP_Header_Update(
                                                                                header_update_data)
                                                                            # return JsonResponse({
                                                                            #                       "MESSAGE": "ERROR_OCCURED_ON_NEFT_SUCCESS_STATUS_UPDATE",
                                                                            #                      "DATA": str(e)})

                                                                    else:
                                                                        try:
                                                                            inward_dtl.action = "UPDATE"
                                                                            inward_dtl.type = "STATUS"
                                                                            inward_dtl.header_json = '{}'
                                                                            inward_dtl.debit_json = '{}'
                                                                            inward_dtl.detail_json = '{}'
                                                                            inward_dtl.status_json = {
                                                                                "Invoice_Header_Gid": invoiceheader_gid,
                                                                                "Status": "TXN FAILED",
                                                                                "crno": invoiceheader_crno,
                                                                                "cbsno": "N", "pvno": pv_number,
                                                                                "neftstatus": "NEFT_FAIL"}
                                                                            inward_dtl.entity_gid = entity_gid
                                                                            inward_dtl.employee_gid = employee_gid
                                                                            final_out = outputSplit(
                                                                                inward_dtl.set_Invoiceheader_status_update(),
                                                                                1)
                                                                            header_update_data = {
                                                                                "Invoice_Header_Gid": invoiceheader_gid,
                                                                                "entity_gid": entity_gid,
                                                                                "type": "ERROR_UPDATE",
                                                                                "employee_gid": employee_gid,
                                                                                "Error_log": {
                                                                                    "MESSAGE": "ERROR_OCCURED_ON_NEFT_API",
                                                                                    "DATA": neft_results_data,
                                                                                    "UPDATE_STATUS": final_out}}
                                                                            AP_Header_Update_result = AP_Header_Update(
                                                                                header_update_data)
                                                                            # return JsonResponse(
                                                                            #   {"MESSAGE": "ERROR_OCCURED_ON_NEFT_API",
                                                                            #   "DATA": neft_results_data,
                                                                            #  "UPDATE_STATUS": final_out})

                                                                        except Exception as e:
                                                                            header_update_data = {
                                                                                "Invoice_Header_Gid": invoiceheader_gid,
                                                                                "entity_gid": entity_gid,
                                                                                "type": "ERROR_UPDATE",
                                                                                "employee_gid": employee_gid,
                                                                                "Error_log": {
                                                                                    "MESSAGE": "ERROR_OCCURED_ON_NEFT_NOT_SUCCESS_AND_STATUS_UPDATE",
                                                                                    "DATA": str(e)}}
                                                                            AP_Header_Update_result = AP_Header_Update(
                                                                                header_update_data)
                                                                            # return JsonResponse({
                                                                            #                       "MESSAGE": "ERROR_OCCURED_ON_NEFT_NOT_SUCCESS_AND_STATUS_UPDATE",
                                                                            #                      "DATA": str(e)})
                                                                except Exception as e:
                                                                    common.logger.error(e)
                                                                    header_update_data = {
                                                                        "Invoice_Header_Gid": invoiceheader_gid,
                                                                        "entity_gid": entity_gid,
                                                                        "type": "ERROR_UPDATE",
                                                                        "employee_gid": employee_gid,
                                                                        "Error_log": {
                                                                            "MESSAGE": "ERROR_OCCURED_ON_NEFT_API",
                                                                            "DATA": str(e)}}
                                                                    AP_Header_Update_result = AP_Header_Update(
                                                                        header_update_data)
                                                                    # return JsonResponse({"MESSAGE": "ERROR_OCCURED_ON_NEFT_API",
                                                                    #                    "DATA": str(e)})
                                                            else:
                                                                # return JsonResponse({
                                                                #                       "MESSAGE": "ERROR_OCCURED_ON_TOKEN_GENERATIONS OR INVALID AUTHENTICATONS",
                                                                #                        "TOKEN_LOG": log_data})
                                                                pass
                                                        except Exception as e:
                                                            try:
                                                                inward_dtl.action = "UPDATE"
                                                                inward_dtl.type = "STATUS"
                                                                inward_dtl.header_json = '{}'
                                                                inward_dtl.debit_json = '{}'
                                                                inward_dtl.detail_json = '{}'
                                                                inward_dtl.status_json = {
                                                                    "Invoice_Header_Gid": invoiceheader_gid,
                                                                    "Status": "TXN FAILED", "crno": invoiceheader_crno,
                                                                    "cbsno": "N", "pvno": pv_number,
                                                                    "neftstatus": "NEFT_FAIL"}
                                                                inward_dtl.entity_gid = entity_gid
                                                                inward_dtl.employee_gid = employee_gid
                                                                final_out = outputSplit(
                                                                    inward_dtl.set_Invoiceheader_status_update(), 1)
                                                                header_update_data = {
                                                                    "Invoice_Header_Gid": invoiceheader_gid,
                                                                    "entity_gid": entity_gid,
                                                                    "type": "ERROR_UPDATE",
                                                                    "employee_gid": employee_gid,
                                                                    "Error_log": {
                                                                        "MESSAGE": "ERROR_OCCURED_ON_NEFT_LOCAL_API",
                                                                        "DATA": str(e), "UPDATE_STATUS": final_out}}
                                                                AP_Header_Update_result = AP_Header_Update(
                                                                    header_update_data)
                                                                # return JsonResponse(
                                                                #    {"MESSAGE": "ERROR_OCCURED_ON_NEFT_LOCAL_API",
                                                                #     "DATA": str(e), "UPDATE_STATUS": final_out})

                                                            except Exception as e1:
                                                                common.logger.error(e1)
                                                                header_update_data = {
                                                                    "Invoice_Header_Gid": invoiceheader_gid,
                                                                    "entity_gid": entity_gid, "type": "ERROR_UPDATE",
                                                                    "employee_gid": employee_gid,
                                                                    "Error_log": {
                                                                        "MESSAGE": "ERROR_OCCURED_ON_NEFT_LOCAL_API_AND_STATUS_UPDATE_FAILED",
                                                                        "DATA": str(e1)}}
                                                                AP_Header_Update_result = AP_Header_Update(
                                                                    header_update_data)
                                                                # return JsonResponse({
                                                                #                       "MESSAGE": "ERROR_OCCURED_ON_NEFT_LOCAL_API_AND_STATUS_UPDATE_FAILED",
                                                                #                        "DATA": str(e1)})

                                                    elif (Payment_Mode == "DD"):
                                                        dd_statu_update_result = ""
                                                        try:
                                                            dd_status_update_data = {
                                                                "Invoice_Header_Gid": invoiceheader_gid,
                                                                "entity_gid": entity_gid,
                                                                "cbsno": cbsno_ref_number,
                                                                "pvno": pv_number,
                                                                "employee_gid": employee_gid,
                                                                "Status": "DD INITIATED"}
                                                            dd_statu_update_result = AP_status_update(
                                                                dd_status_update_data)
                                                            if (dd_statu_update_result == "SUCCESS"):
                                                                pass
                                                            else:
                                                                header_update_data = {
                                                                    "Invoice_Header_Gid": invoiceheader_gid,
                                                                    "entity_gid": entity_gid,
                                                                    "type": "ERROR_UPDATE",
                                                                    "employee_gid": employee_gid,
                                                                    "Error_log": {
                                                                        "MESSAGE": "ERROR_OCCURED_ON_DD_INITIATED_UPDATION",
                                                                        "OUT": dd_statu_update_result}}
                                                                AP_Header_Update_result = AP_Header_Update(
                                                                    header_update_data)
                                                                # return JsonResponse(
                                                                #    {"MESSAGE": "ERROR_OCCURED_ON_DD_INITIATED_UPDATION",
                                                                #    "OUT": dd_statu_update_result})
                                                        except Exception as e:
                                                            common.logger.error(e)
                                                            header_update_data = {
                                                                "Invoice_Header_Gid": invoiceheader_gid,
                                                                "entity_gid": entity_gid,
                                                                "type": "ERROR_UPDATE", "employee_gid": employee_gid,
                                                                "Error_log": {
                                                                    "MESSAGE": "ERROR_OCCURED_ON_DD_INITIATED_UPDATION",
                                                                    "DATA": str(e)}}
                                                            AP_Header_Update_result = AP_Header_Update(
                                                                header_update_data)
                                                            # return JsonResponse(
                                                            #    {"MESSAGE": "ERROR_OCCURED_ON_DD_INITIATED_UPDATION",
                                                            #     "DATA": str(e)})
                                                            # pass

                                                        data3 = {"productType": "DP", "SrcChannel": "EMC-AG",
                                                                 "Channel": "API",
                                                                 "BankCode": "53",
                                                                 "UserId": "SYSTELLER",
                                                                 "serviceName": "DD_Payment_Api",
                                                                 "ApplicationId": pv_number,
                                                                 "TxnDate": CBSDATE,
                                                                 "TransactionBranch": Credit_DDtran_Branch,
                                                                 "DDPaymentDetails": [{
                                                                     "ApplicantId": pv_number,
                                                                     "AccountId": Payment_Mode_GL,
                                                                     "AccountInstrumentNumber": "",
                                                                     "BeneficiaryAddress": "sdfasdfsdfasdfa asd, sdfasdfas",
                                                                     "City": "Mumbai",
                                                                     "Country": "India",
                                                                     "State": "TN",
                                                                     "ZipCode": "600097",
                                                                     "BeneficiaryIdentification": "AIFPJ9987J",
                                                                     "BeneficiaryName": beneficiaryname,
                                                                     "InstrumentAmount": str(DD_Header_Amount),
                                                                     "IssueBankCode": "53",
                                                                     "Narrative": str(
                                                                         invoiceheader_dedupeinvoiceno) + " " + str(
                                                                         branch_name),
                                                                     "PayableBranch": Credit_DDpay_Branch,
                                                                 }
                                                                 ]
                                                                 }

                                                        try:
                                                            log_data = [{"BEFORE_DD_PAYEMENT_API_DATA": data3}]
                                                            common.logger.error(log_data)
                                                            data = json.dumps(data3)
                                                            token_status = 1
                                                            try:
                                                                generated_token_data = master_views.master_sync_Data_(
                                                                    "GET",
                                                                    "get_data",
                                                                    employee_gid)
                                                            except Exception as e:
                                                                common.logger.error(e)
                                                                # return JsonResponse(
                                                                #    {"MESSAGE": "ERROR_OCCURED_ON_TOKEN_GENERATION",
                                                                #     "DATA": str(e)})
                                                                pass
                                                            log_data = generated_token_data
                                                            token = generated_token_data.get("DATA")[0].get(
                                                                "clienttoken_name")
                                                            if (token == " " or token == None):
                                                                token_status = 0
                                                            if token_status == 1:
                                                                try:
                                                                    client_api = common.clientapi()
                                                                    headers = {"Content-Type": "application/json",
                                                                               "Authorization": "Bearer " + token}
                                                                    result = requests.post(
                                                                        "" + client_api + "/nbfc/v1/mwr/dd-payment",
                                                                        headers=headers, data=data, verify=False)
                                                                    results = result.content.decode("utf-8")
                                                                    dd_results_data = json.loads(results)
                                                                    log_data = [
                                                                        {"AFTER_DD_PAYEMENT_API_DATA": dd_results_data}]
                                                                    common.logger.error(log_data)
                                                                    if (dd_results_data.get(
                                                                            "ErrorMessage") == "Success" and dd_results_data.get(
                                                                        "ErrorCode") == '0'):
                                                                        try:
                                                                            inward_dtl.action = "UPDATE"
                                                                            inward_dtl.type = "STATUS"
                                                                            inward_dtl.header_json = '{}'
                                                                            inward_dtl.debit_json = '{}'
                                                                            inward_dtl.detail_json = '{}'
                                                                            inward_dtl.status_json = {
                                                                                "Invoice_Header_Gid": invoiceheader_gid,
                                                                                "Status": "PAYMENT",
                                                                                "crno": invoiceheader_crno,
                                                                                "cbsno": "N", "pvno": pv_number,
                                                                                "neftstatus": "DD_PASS"}
                                                                            inward_dtl.entity_gid = entity_gid
                                                                            inward_dtl.employee_gid = employee_gid
                                                                            final_out = outputSplit(
                                                                                inward_dtl.set_Invoiceheader_status_update(),
                                                                                1)
                                                                            return JsonResponse(final_out, safe=False)
                                                                        except Exception as e:
                                                                            common.logger.error(e)
                                                                            header_update_data = {
                                                                                "Invoice_Header_Gid": invoiceheader_gid,
                                                                                "entity_gid": entity_gid,
                                                                                "type": "ERROR_UPDATE",
                                                                                "employee_gid": employee_gid,
                                                                                "Error_log": {
                                                                                    "MESSAGE": "ERROR_OCCURED_ON_DD_SUCCESS_STATUS_UPDATE",
                                                                                    "DATA": str(e)}}
                                                                            AP_Header_Update_result = AP_Header_Update(
                                                                                header_update_data)
                                                                            # return JsonResponse({
                                                                            #                        "MESSAGE": "ERROR_OCCURED_ON_DD_SUCCESS_STATUS_UPDATE",
                                                                            #                        "DATA": str(e)})
                                                                            # pass
                                                                    else:
                                                                        try:
                                                                            inward_dtl.action = "UPDATE"
                                                                            inward_dtl.type = "STATUS"
                                                                            inward_dtl.header_json = '{}'
                                                                            inward_dtl.debit_json = '{}'
                                                                            inward_dtl.detail_json = '{}'
                                                                            inward_dtl.status_json = {
                                                                                "Invoice_Header_Gid": invoiceheader_gid,
                                                                                "Status": "TXN FAILED",
                                                                                "crno": invoiceheader_crno,
                                                                                "cbsno": "N", "pvno": pv_number,
                                                                                "neftstatus": "DD_FAIL"}
                                                                            inward_dtl.entity_gid = entity_gid
                                                                            inward_dtl.employee_gid = employee_gid
                                                                            final_out = outputSplit(
                                                                                inward_dtl.set_Invoiceheader_status_update(),
                                                                                1)
                                                                            header_update_data = {
                                                                                "Invoice_Header_Gid": invoiceheader_gid,
                                                                                "entity_gid": entity_gid,
                                                                                "type": "ERROR_UPDATE",
                                                                                "employee_gid": employee_gid,
                                                                                "Error_log": {
                                                                                    "MESSAGE": "ERROR_OCCURED_ON_DD_API",
                                                                                    "DATA": dd_results_data,
                                                                                    "UPDATE_STATUS": final_out}}
                                                                            AP_Header_Update_result = AP_Header_Update(
                                                                                header_update_data)
                                                                            # return JsonResponse(
                                                                            #    {"MESSAGE": "ERROR_OCCURED_ON_DD_API",
                                                                            #     "DATA": dd_results_data,
                                                                            #     "UPDATE_STATUS": final_out})
                                                                            pass
                                                                        except Exception as e:
                                                                            common.logger.error(e)
                                                                            header_update_data = {
                                                                                "Invoice_Header_Gid": invoiceheader_gid,
                                                                                "entity_gid": entity_gid,
                                                                                "type": "ERROR_UPDATE",
                                                                                "employee_gid": employee_gid,
                                                                                "Error_log": {
                                                                                    "MESSAGE": "ERROR_OCCURED_ON_DD_NOT_SUCCESS_AND_STATUS_UPDATE",
                                                                                    "DATA": str(e)}}
                                                                            AP_Header_Update_result = AP_Header_Update(
                                                                                header_update_data)
                                                                            # return JsonResponse({
                                                                            #                        "MESSAGE": "ERROR_OCCURED_ON_DD_NOT_SUCCESS_AND_STATUS_UPDATE",
                                                                            #                        "DATA": str(e)})
                                                                            # pass
                                                                except Exception as e:
                                                                    try:
                                                                        inward_dtl.action = "UPDATE"
                                                                        inward_dtl.type = "STATUS"
                                                                        inward_dtl.header_json = '{}'
                                                                        inward_dtl.debit_json = '{}'
                                                                        inward_dtl.detail_json = '{}'
                                                                        inward_dtl.status_json = {
                                                                            "Invoice_Header_Gid": invoiceheader_gid,
                                                                            "Status": "TXN FAILED",
                                                                            "crno": invoiceheader_crno,
                                                                            "cbsno": "N", "pvno": pv_number,
                                                                            "neftstatus": "NEFT_FAIL"}
                                                                        inward_dtl.entity_gid = entity_gid
                                                                        inward_dtl.employee_gid = employee_gid
                                                                        final_out = outputSplit(
                                                                            inward_dtl.set_Invoiceheader_status_update(),
                                                                            1)
                                                                        header_update_data = {
                                                                            "Invoice_Header_Gid": invoiceheader_gid,
                                                                            "entity_gid": entity_gid,
                                                                            "type": "ERROR_UPDATE",
                                                                            "employee_gid": employee_gid,
                                                                            "Error_log": {
                                                                                "MESSAGE": "ERROR_OCCURED_ON_DD_API",
                                                                                "DATA": str(e),
                                                                                "UPDATE_STATUS": final_out}}
                                                                        AP_Header_Update_result = AP_Header_Update(
                                                                            header_update_data)
                                                                        # return JsonResponse(
                                                                        #    {"MESSAGE": "ERROR_OCCURED_ON_DD_API",
                                                                        #     "DATA": str(e), "UPDATE_STATUS": final_out})
                                                                        # pass

                                                                    except Exception as e1:
                                                                        common.logger.error(e1)
                                                                        header_update_data = {
                                                                            "Invoice_Header_Gid": invoiceheader_gid,
                                                                            "entity_gid": entity_gid,
                                                                            "type": "ERROR_UPDATE",
                                                                            "employee_gid": employee_gid,
                                                                            "Error_log": {
                                                                                "MESSAGE": "ERROR_OCCURED_ON_DD_LOCAL_API_AND_STATUS_UPDATE_FAILED",
                                                                                "DATA": str(e1)}}
                                                                        AP_Header_Update_result = AP_Header_Update(
                                                                            header_update_data)
                                                                    # return JsonResponse({
                                                                    #                         "MESSAGE": "ERROR_OCCURED_ON_DD_LOCAL_API_AND_STATUS_UPDATE_FAILED",
                                                                    #                        "DATA": str(e1)})

                                                            else:
                                                                header_update_data = {
                                                                    "Invoice_Header_Gid": invoiceheader_gid,
                                                                    "entity_gid": entity_gid, "type": "ERROR_UPDATE",
                                                                    "employee_gid": employee_gid,
                                                                    "Error_log": {
                                                                        "MESSAGE": "ERROR_OCCURED_ON_TOKEN_GENERATIONS OR INVALID AUTHENTICATONS",
                                                                        "TOKEN_LOG": log_data}}
                                                                AP_Header_Update_result = AP_Header_Update(
                                                                    header_update_data)
                                                                # return JsonResponse({
                                                                #                        "MESSAGE": "ERROR_OCCURED_ON_TOKEN_GENERATIONS OR INVALID AUTHENTICATONS",
                                                                #                        "TOKEN_LOG": log_data})
                                                                # pass
                                                        except Exception as e:
                                                            common.logger.error(e)
                                                            header_update_data = {
                                                                "Invoice_Header_Gid": invoiceheader_gid,
                                                                "entity_gid": entity_gid,
                                                                "type": "ERROR_UPDATE", "employee_gid": employee_gid,
                                                                "Error_log": {"MESSAGE": "ERROR_OCCURED_ON_DD_API",
                                                                              "DATA": str(e)}}
                                                            AP_Header_Update_result = AP_Header_Update(
                                                                header_update_data)
                                                            # return JsonResponse(
                                                            #    {"MESSAGE": "ERROR_OCCURED_ON_DD_API", "DATA": str(e)})
                                                            # pass

                                                    else:
                                                        try:
                                                            inward_dtl.action = "UPDATE"
                                                            inward_dtl.type = "STATUS"
                                                            inward_dtl.header_json = '{}'
                                                            inward_dtl.debit_json = '{}'
                                                            inward_dtl.detail_json = '{}'
                                                            inward_dtl.status_json = {
                                                                "Invoice_Header_Gid": invoiceheader_gid,
                                                                "Status": "PAYMENT",
                                                                "crno": invoiceheader_crno,
                                                                "cbsno": cbsno_ref_number,
                                                                "pvno": pv_number,
                                                                "neftstatus": "NOT_NEFT"}
                                                            inward_dtl.entity_gid = entity_gid
                                                            inward_dtl.employee_gid = employee_gid
                                                            final_out = outputSplit(
                                                                inward_dtl.set_Invoiceheader_status_update(), 1)
                                                            return JsonResponse(final_out, safe=False)
                                                        except Exception as e:
                                                            common.logger.error(e)
                                                            header_update_data = {
                                                                "Invoice_Header_Gid": invoiceheader_gid,
                                                                "entity_gid": entity_gid,
                                                                "type": "ERROR_UPDATE", "employee_gid": employee_gid,
                                                                "Error_log": {
                                                                    "MESSAGE": "ERROR_OCCURED_AMOUNT_TRANSFER_SUCCESS_FINAL_STATUS_UPDATE_FAILED",
                                                                    "DATA": str(e)}}
                                                            AP_Header_Update_result = AP_Header_Update(
                                                                header_update_data)
                                                            # return JsonResponse({
                                                            #                        "MESSAGE": "ERROR_OCCURED_AMOUNT_TRANSFER_SUCCESS_FINAL_STATUS_UPDATE_FAILED",
                                                            #                        "DATA": str(e)})
                                                            # pass
                                                else:
                                                    header_update_data = {"Invoice_Header_Gid": invoiceheader_gid,
                                                                          "entity_gid": entity_gid,
                                                                          "type": "ERROR_UPDATE",
                                                                          "employee_gid": employee_gid,
                                                                          "Error_log": {"MESSAGE": results_data}}
                                                    AP_Header_Update_result = AP_Header_Update(header_update_data)
                                                    # return JsonResponse({"MESSAGE": results_data})
                                                    # pass

                                            except Exception as e:
                                                common.logger.error(e)
                                                header_update_data = {"Invoice_Header_Gid": invoiceheader_gid,
                                                                      "entity_gid": entity_gid,
                                                                      "type": "ERROR_UPDATE",
                                                                      "employee_gid": employee_gid,
                                                                      "Error_log": {
                                                                          "MESSAGE": "ERROR_OCCURED_ON_AMOUNT_TRANSFER_API_",
                                                                          "DATA": str(e)}}
                                                AP_Header_Update_result = AP_Header_Update(header_update_data)
                                                # return JsonResponse({"MESSAGE": "ERROR_OCCURED_ON_AMOUNT_TRANSFER_API", "DATA": str(e)})
                                                # pass

                                        except Exception as e:
                                            common.logger.error(e)
                                            header_update_data = {"Invoice_Header_Gid": invoiceheader_gid,
                                                                  "entity_gid": entity_gid,
                                                                  "type": "ERROR_UPDATE", "employee_gid": employee_gid,
                                                                  "Error_log": {
                                                                      "MESSAGE": "ERROR_OCCURED_AP_ENTER_DETAIL_GET_",
                                                                      "DATA": str(e)}}
                                            AP_Header_Update_result = AP_Header_Update(header_update_data)
                                            # return JsonResponse({"MESSAGE": "ERROR_OCCURED_AP_ENTER_DETAIL_GET", "DATA": str(e)})
                                            # pass
                                    else:
                                        header_update_data = {"Invoice_Header_Gid": invoiceheader_gid,
                                                              "entity_gid": entity_gid,
                                                              "type": "ERROR_UPDATE", "employee_gid": employee_gid,
                                                              "Error_log": {"MESSAGE": out_put_data}}
                                        AP_Header_Update_result = AP_Header_Update(header_update_data)
                                        # return JsonResponse({"MESSAGE": out_put_data})
                                        # pass
                                except Exception as e:
                                    common.logger.error(e)
                                    header_update_data = {"Invoice_Header_Gid": invoiceheader_gid,
                                                          "entity_gid": entity_gid,
                                                          "type": "ERROR_UPDATE", "employee_gid": employee_gid,
                                                          "Error_log": {"MESSAGE": "ERROR_OCCURED_ON_PAYMENT_INSERT_",
                                                                        "PAYMENT_OUT_PUT": out_put_data,
                                                                        "DATA": str(e)}}
                                    AP_Header_Update_result = AP_Header_Update(header_update_data)
                                    # return JsonResponse({"MESSAGE": "ERROR_OCCURED_ON_PAYMENT_INSERT", "PAYMENT_OUT_PUT": out_put_data,"DATA": str(e)})
                                    # pass
                            else:
                                header_update_data = {"Invoice_Header_Gid": invoiceheader_gid, "entity_gid": entity_gid,
                                                      "type": "ERROR_UPDATE", "employee_gid": employee_gid,
                                                      "Error_log": Final_Header_Status_Data}
                                AP_Header_Update_result = AP_Header_Update(header_update_data)
                                # return JsonResponse(Final_Header_Status_Data, safe=False)
                                # pass
                        else:
                            header_update_data = {"Invoice_Header_Gid": invoiceheader_gid, "entity_gid": entity_gid,
                                                  "type": "ERROR_UPDATE", "employee_gid": employee_gid,
                                                  "Error_log": {"MESSAGE": "ERROR_OCCURED_ON_PAY_INITIATED_UPDATION",
                                                                "OUT": ap_statu_update_result}}
                            AP_Header_Update_result = AP_Header_Update(header_update_data)
                            # pass
                            # return JsonResponse({"MESSAGE": "ERROR_OCCURED_ON_AP INITIATED_UPDATION", "OUT": ap_statu_update_result})
                    except Exception as e:
                        common.logger.error(e)
                        header_update_data = {"Invoice_Header_Gid": invoiceheader_gid, "entity_gid": entity_gid,
                                              "type": "ERROR_UPDATE", "employee_gid": employee_gid,
                                              "Error_log": {"MESSAGE": "ERROR_OCCURED_ON_PAY_INITIATED_UPDATION_",
                                                            "DATA": str(e)}}
                        AP_Header_Update_result = AP_Header_Update(header_update_data)
                        # return JsonResponse({"MESSAGE": "ERROR_OCCURED_ON_AP INITIATED_UPDATION", "DATA": str(e)})
                except Exception as e:
                    common.logger.error(e)
                    header_update_data = {"Invoice_Header_Gid": invoiceheader_gid, "entity_gid": entity_gid,
                                          "type": "ERROR_UPDATE", "employee_gid": employee_gid,
                                          "Error_log": {"MESSAGE": "ERROR_OCCURED_", "DATA": str(e)}}
                    AP_Header_Update_result = AP_Header_Update(header_update_data)
                    # return JsonResponse({"MESSAGE": "ERROR_OCCURED_ON_BANK_DETAILS_GET", "DATA": str(e)})
                    # pass
        else:
            try:
                inward_dtl.action = jsondata.get('params').get('action')
                inward_dtl.type = jsondata.get('params').get('type')
                inward_dtl.header_json = jsondata.get('params').get('header_json')
                inward_dtl.detail_json = jsondata.get('params').get('detail_json')
                inward_dtl.other_json = jsondata.get('params').get('other_json')
                inward_dtl.status_json = jsondata.get('params').get('status_json')
                inward_dtl.entity_gid = entity_gid
                inward_dtl.employee_gid = employee_gid
                out = outputSplit(inward_dtl.set_payment(), 1)
                return JsonResponse(out, safe=False)
            except Exception as e:
                common.logger.error(e)

                # return JsonResponse({"MESSAGE": "ERROR_OCCURED", "DATA": str(e)})
                pass

    except Exception as e:
        common.logger.error(e)
        # return JsonResponse({"MESSAGE": "ERROR_OCCURED", "DATA": str(e)})
        pass


# @sched.interval_schedule(minutes=2)
# @sched.interval_schedule(minutes=1)
# @sched.interval_schedule(seconds=1)
def approve_and_pay_auto_load():
    try:
        obj_ap = mAP.ap_model()
        obj_ap.action = 'UPDATE'
        obj_ap.type = 'ERROR_FLAG'
        obj_ap.filter = '{}'
        obj_ap.classification = '{}'
        ld_out_message = obj_ap.ap_update_flag()
        try:
            inward_dtl = mAP.ap_model()
            inward_dtl.action = "GET"
            inward_dtl.type = "TRANSACTION_INITIATED"
            inward_dtl.filter = '{}'
            inward_dtl.classification = json.dumps({"Entity_Gid": 1})
            load_data = inward_dtl.get_invoice_all()
            extract_load_data = load_data.to_json(orient='records')
            json_data = json.loads(extract_load_data)
            if (len(json_data) != 0):
                for i in json_data:
                    try:
                        inward_dtl = mAP.ap_model()
                        jsondata = {
                            'params': {'action': 'UPDATE', 'type': 'STATUS', 'header_json': {}, 'debit_json': {},
                                       'detail_json': {},
                                       'status_json': {'Invoice_Header_Gid': i.get("invoiceheader_gid"),
                                                       'Status': 'APPROVED', 'Header_Status': 'CHECKER',
                                                       'Invoice_Type': i.get("invoiceheader_invoicetype"),
                                                       'Is_approve_and_pay': 'Y', 'file_data': [],
                                                       'ref_no': i.get("invoiceheader_crno"),
                                                       'branch_gid': i.get("invoiceheader_branchgid")}}}
                        if (jsondata.get('params').get('action') == 'UPDATE' and
                                jsondata.get('params').get('type') == 'STATUS' and
                                jsondata.get('params').get('status_json').get('Status') == 'APPROVED'):
                            try:
                                current_month = datetime.now().strftime('%m')
                                current_day = datetime.now().strftime('%d')
                                current_year_full = datetime.now().strftime('%Y')
                                today_date = str(current_day + "/" + current_month + "/" + current_year_full)
                                Is_approve_and_pay = jsondata.get('params').get('status_json').get('Is_approve_and_pay')
                                invoice_header_gid = jsondata.get('params').get('status_json').get('Invoice_Header_Gid')
                                Invoice_Type = jsondata.get('params').get('status_json').get('Invoice_Type')
                                cr_no = jsondata.get('params').get('status_json').get('ref_no')
                                status = jsondata.get('params').get('status_json').get('Header_Status')
                                entity_gid = i.get("entity_gid")
                                employee_gid = i.get("update_by")
                                ap_statu_update_result = ""
                                try:
                                    status_update_data = {"Invoice_Header_Gid": invoice_header_gid,
                                                          "entity_gid": entity_gid,
                                                          "employee_gid": employee_gid, "Status": "AP INITIATED"}
                                    ap_statu_update_result = AP_status_update(status_update_data)
                                    if (ap_statu_update_result == "SUCCESS"):
                                        try:
                                            inward_dtl.action = "INSERT"
                                            inward_dtl.type = "INITIAL_SET"
                                            inward_dtl.filter = json.dumps({"InvoiceHeader_Gid": invoice_header_gid,
                                                                            "cr_no": cr_no, "Status_": status,
                                                                            "Invoice_Type": Invoice_Type})
                                            inward_dtl.classification = json.dumps({"Entity_Gid": entity_gid})
                                            inward_dtl.create_by = employee_gid
                                            out = outputSplit(inward_dtl.set_accounting_entry(), 1)
                                            if (out == 'SUCCESS' or out == 'ALREADY INSERTED'):
                                                try:
                                                    inward_dtl.action = "GET"
                                                    inward_dtl.type = "AP_ENTER_DETAIL_GET"
                                                    ref_no = jsondata.get('params').get('status_json').get('ref_no')
                                                    inward_dtl.filter = json.dumps(
                                                        {"entry_refno": ref_no, "entry_module": "AP"})
                                                    inward_dtl.classification = json.dumps({"Entity_Gid": entity_gid})
                                                    datas = inward_dtl.get_invoice_all()
                                                    Fund_Transfer_Dtls_data = datas.get("entry_detail")[0]
                                                    Fund_Transfer_Dtls_data = json.loads(Fund_Transfer_Dtls_data)

                                                    orginal_data_frame = pd.DataFrame(
                                                        Fund_Transfer_Dtls_data.get("Fund_Transfer_Dtls"))
                                                    data_frame = pd.DataFrame(
                                                        Fund_Transfer_Dtls_data.get("Fund_Transfer_Dtls"))

                                                    data_frame['Amount'] = data_frame['Amount'].astype(float)
                                                    Credit_amount = data_frame.loc[
                                                        data_frame['Cr_Dr_Flag'] == 'C', 'Amount'].sum()
                                                    Debit_amount = data_frame.loc[
                                                        data_frame['Cr_Dr_Flag'] == 'D', 'Amount'].sum()
                                                    Credit_amount = str(round(float(Credit_amount), 2))
                                                    Debit_amount = str(round(float(Debit_amount), 2))
                                                    if (Credit_amount == Debit_amount):

                                                        Unique_Values = data_frame.Entry_refno.unique()
                                                        Unique_Values_Length = len(Unique_Values)
                                                        Final_Unique_Values = []
                                                        for i in range(len(Unique_Values)):
                                                            Single_Unique_Values = Unique_Values[i]
                                                            Fetched_values = data_frame[
                                                                (data_frame['Entry_refno'] == Single_Unique_Values)]
                                                            Final_send_data = orginal_data_frame[
                                                                (orginal_data_frame[
                                                                     'Entry_refno'] == Single_Unique_Values)]

                                                            send_Credit_amount = Fetched_values.loc[
                                                                Fetched_values['Cr_Dr_Flag'] == 'C', 'Amount'].sum()
                                                            send_Debit_amount = Fetched_values.loc[
                                                                Fetched_values['Cr_Dr_Flag'] == 'D', 'Amount'].sum()
                                                            send_Credit_amount = str(
                                                                round(float(send_Credit_amount), 2))
                                                            send_Debit_amount = str(round(float(send_Debit_amount), 2))

                                                            if (send_Credit_amount == send_Debit_amount):

                                                                send_data = Final_send_data.to_json(orient='records')
                                                                send_data = json.loads(send_data)

                                                                branch_code = \
                                                                    Fund_Transfer_Dtls_data.get("Fund_Transfer_Dtls")[
                                                                        0].get("Brn_Code")
                                                                CBSDATE = ""
                                                                NEFT_ACCOUNT_NUMBER = ""
                                                                # CBSDATE=Fund_Transfer_Dtls_data.get("Fund_Transfer_Dtls")[0].get("CBSDATE")
                                                                try:
                                                                    # pass
                                                                    CBSDATE_DATA = str(
                                                                        common.get_server_date(
                                                                            "GET_CBSDATE_ACCOUNT_NUMBER")[0])
                                                                    CBSDATE_DATA_LIST = CBSDATE_DATA.split(",")
                                                                    NEFT_ACCOUNT_NUMBER = CBSDATE_DATA_LIST[0]
                                                                    CBSDATE = CBSDATE_DATA_LIST[1]
                                                                except Exception as e:
                                                                    common.logger.error(e)
                                                                    header_update_data = {
                                                                        "Invoice_Header_Gid": invoice_header_gid,
                                                                        "entity_gid": entity_gid,
                                                                        "type": "ERROR_UPDATE",
                                                                        "employee_gid": employee_gid,
                                                                        "Error_log": {
                                                                            "MESSAGE": "ERROR_OCCURED_ON_CBSDATE_AND_ACCOUNT_NUMBER_GET_",
                                                                            "DATA": str(e)}}
                                                                    AP_Header_Update_result = AP_Header_Update(
                                                                        header_update_data)
                                                                    # pass
                                                                    # return JsonResponse({"MESSAGE": "ERROR_OCCURED_ON_CBSDATE_AND_ACCOUNT_NUMBER_GET", "DATA": str(e)})

                                                                try:
                                                                    token_status = 1
                                                                    generated_token_data = master_views.master_sync_Data_(
                                                                        "GET",
                                                                        "get_data",
                                                                        employee_gid)
                                                                    log_data = generated_token_data
                                                                    token = generated_token_data.get("DATA")[0].get(
                                                                        "clienttoken_name")
                                                                    if (token == " " or token == None):
                                                                        token_status = 0
                                                                    if token_status == 1:
                                                                        try:
                                                                            data = {"Src_Channel": "EMS",
                                                                                    "ApplicationId": Single_Unique_Values,
                                                                                    "TransactionBranch": branch_code,
                                                                                    "Txn_Date": CBSDATE,
                                                                                    "productType": "DP",
                                                                                    "Fund_Transfer_Dtls": send_data}
                                                                            data = json.dumps(data)
                                                                            log_data = [{
                                                                                "BEFORE_AMOUNT_TRANSFER_API_DATA": data}]
                                                                            common.logger.error(log_data)

                                                                            client_api = common.clientapi()
                                                                            headers = {
                                                                                "Content-Type": "application/json",
                                                                                "Authorization": "Bearer " + token}
                                                                            result = requests.post(
                                                                                "" + client_api + "/nbfc/v1/mwr/amount-transfer",
                                                                                headers=headers, data=data,
                                                                                verify=False)
                                                                            results = result.content.decode("utf-8")
                                                                            results_data = json.loads(results)
                                                                            log_data = [
                                                                                {
                                                                                    "AFTER_AMOUNT_TRANSFER_API_DATA": results_data}]
                                                                            common.logger.error(log_data)

                                                                            ErrorStatus = results_data.get("CbsStatus")[
                                                                                0].get(
                                                                                "ErrorMessage")
                                                                            ErrorCode = results_data.get("CbsStatus")[
                                                                                0].get(
                                                                                "ErrorCode")
                                                                            if (
                                                                                    ErrorStatus == "Success" and ErrorCode == '0'):
                                                                                CBSReferenceNo = \
                                                                                    results_data.get("CbsStatus")[
                                                                                        0].get("CBSReferenceNo")
                                                                                try:
                                                                                    count_values = i + 1
                                                                                    Final_status = "ENTRY"
                                                                                    if (count_values == len(
                                                                                            Unique_Values)):
                                                                                        Final_status = "APPROVED"
                                                                                    Invoice_Header_Gid = jsondata.get(
                                                                                        'params').get(
                                                                                        'status_json').get(
                                                                                        "Invoice_Header_Gid")
                                                                                    inward_dtl.action = "UPDATE"
                                                                                    inward_dtl.type = "INVOICE_HEADER_UPDATE"
                                                                                    inward_dtl.header_json = {
                                                                                        "HEADER": [{
                                                                                            "Invoice_Header_Gid": Invoice_Header_Gid,
                                                                                            "refno": CBSReferenceNo,
                                                                                            "status_": Final_status,
                                                                                            "crno": Single_Unique_Values}]}
                                                                                    inward_dtl.debit_json = {}
                                                                                    inward_dtl.detail_json = {}
                                                                                    inward_dtl.status_json = {}
                                                                                    inward_dtl.entity_gid = entity_gid
                                                                                    inward_dtl.employee_gid = employee_gid
                                                                                    outs = outputSplit(
                                                                                        inward_dtl.set_Invoiceheader(),
                                                                                        1)
                                                                                    if (outs == "SUCCESS"):
                                                                                        Final_Unique_Values.append(
                                                                                            "SUCCESS")
                                                                                        if (len(
                                                                                                Final_Unique_Values) == len(
                                                                                            Unique_Values)):
                                                                                            if (
                                                                                                    Is_approve_and_pay == "Y"):
                                                                                                try:
                                                                                                    invoice_set = mAP.ap_model()
                                                                                                    invoice_set.action = "GET"
                                                                                                    invoice_set.type = "AP_PAYMENTDETAILS"
                                                                                                    filter = {
                                                                                                        "InvoiceHeader_Status": "APPROVED",
                                                                                                        "InvoiceHeader_Gid": [
                                                                                                            invoice_header_gid],
                                                                                                        "InvoiceHeader_InvoiceDate": "",
                                                                                                        "fromdate": "",
                                                                                                        "invoiceheader_branchgid": "",
                                                                                                        "Page_Index": 0,
                                                                                                        "Page_Size": 10}
                                                                                                    invoice_set.filter = json.dumps(
                                                                                                        filter)
                                                                                                    invoice_set.classification = json.dumps(
                                                                                                        {
                                                                                                            "Entity_Gid": entity_gid})
                                                                                                    invoice_set.create_by = employee_gid
                                                                                                    out = invoice_set.get_invoice_all()
                                                                                                    jdata = out.to_json(
                                                                                                        orient='records')
                                                                                                    jdata = json.loads(
                                                                                                        jdata)
                                                                                                    Paymentheader_Amount = 0
                                                                                                    Payment_Mode = ""
                                                                                                    for i in jdata:
                                                                                                        i[
                                                                                                            'Amt_topay'] = i.get(
                                                                                                            "credit_amount")
                                                                                                        if (i.get(
                                                                                                                "paymode_name") != "CREDITGL"):
                                                                                                            Payment_Mode = i.get(
                                                                                                                "paymode_name")
                                                                                                            paymode_glno = i.get(
                                                                                                                "paymode_glno")
                                                                                                            credit_ddtranbranch = i.get(
                                                                                                                "credit_ddtranbranch")
                                                                                                            credit_ddpaybranch = i.get(
                                                                                                                "credit_ddpaybranch")
                                                                                                            bankbranch_name = i.get(
                                                                                                                "bankbranch_name")
                                                                                                            bankdetails_acno = i.get(
                                                                                                                "bankdetails_acno")
                                                                                                            ifsccode = i.get(
                                                                                                                "bankbranch_ifsccode")
                                                                                                            beneficiaryname = i.get(
                                                                                                                "bankdetails_beneficiaryname")
                                                                                                            bank_name = i.get(
                                                                                                                "bank_name")
                                                                                                            invoiceheader_remarks = i.get(
                                                                                                                "invoiceheader_remarks")
                                                                                                            invoiceheader_gid = i.get(
                                                                                                                "invoiceheader_gid")
                                                                                                            invoiceheader_status = i.get(
                                                                                                                "invoiceheader_status")
                                                                                                            invoiceheader_crno = i.get(
                                                                                                                "invoiceheader_crno")
                                                                                                            invoiceheader_invoiceno = i.get(
                                                                                                                "invoiceheader_invoiceno")
                                                                                                            credit_bankgid = i.get(
                                                                                                                "credit_bankgid")
                                                                                                        if (i.get(
                                                                                                                "invoiceheader_ppx") == "E"):
                                                                                                            Ref_id = i.get(
                                                                                                                "invoiceheader_employeegid")
                                                                                                            Header_type = "EMPLOYEE_PAYMENT"
                                                                                                        elif (i.get(
                                                                                                                "invoiceheader_ppx") == "I"):
                                                                                                            Ref_id = i.get(
                                                                                                                "invoiceheader_branchgid")
                                                                                                            Header_type = "BRANCH_PAYMENT"
                                                                                                        else:
                                                                                                            Ref_id = i.get(
                                                                                                                "supplier_gid")
                                                                                                            Header_type = "SUPPLIER_PAYMENT"

                                                                                                        Paymentheader_Amount = Paymentheader_Amount + i.get(
                                                                                                            "credit_amount")
                                                                                                    Paymentheader_Amount = round(
                                                                                                        Paymentheader_Amount,
                                                                                                        2)
                                                                                                    if (
                                                                                                            Payment_Mode == ""):
                                                                                                        Payment_Mode = "CREDITGL";
                                                                                                        credit_bankgid = 0;
                                                                                                        bankbranch_name = "null";
                                                                                                        bankdetails_acno = "null";
                                                                                                        ifsccode = "null";
                                                                                                        beneficiaryname = "null";
                                                                                                        paymode_glno = "null";
                                                                                                        credit_ddtranbranch = "";
                                                                                                        credit_ddpaybranch = "";

                                                                                                    datenow = str(
                                                                                                        datetime.now().strftime(
                                                                                                            "%Y-%m-%d"))
                                                                                                    pass_data = {
                                                                                                        'params': {
                                                                                                            'action': 'Insert',
                                                                                                            'type': 'PAYMENT_ADD',
                                                                                                            'header_json': {
                                                                                                                'HEADER': [
                                                                                                                    {
                                                                                                                        'Paymentheader_Amount': Paymentheader_Amount,
                                                                                                                        'Payment_Mode': Payment_Mode,
                                                                                                                        'paymode_glno': paymode_glno,
                                                                                                                        'credit_ddtranbranch': credit_ddtranbranch,
                                                                                                                        "Paymentheader_Status": "PAYMENT INITIATE",
                                                                                                                        'credit_ddpaybranch': credit_ddpaybranch,
                                                                                                                        "bankbranch_name": bankbranch_name,
                                                                                                                        "Remark": "PAYMENT INITIATE",
                                                                                                                        "Bank_Detail_Gid": credit_bankgid,
                                                                                                                        "Paymentheader_Date": datenow,
                                                                                                                        "REF_Gid": Ref_id,
                                                                                                                        "Header_type": Header_type,
                                                                                                                        "bankdetails_acno": bankdetails_acno,
                                                                                                                        "ifsccode": ifsccode,
                                                                                                                        "beneficiaryname": beneficiaryname}]},
                                                                                                            'detail_json': {
                                                                                                                'DETAILS': jdata},
                                                                                                            'other_json': {},
                                                                                                            'status_json': {}}}
                                                                                                    APpayment_set_function_approve_and_pay_result = APpayment_set_function_approve_and_pay(
                                                                                                        pass_data,
                                                                                                        employee_gid,
                                                                                                        entity_gid)

                                                                                                except Exception as e:
                                                                                                    common.logger.error(
                                                                                                        e)
                                                                                                    header_update_data = {
                                                                                                        "Invoice_Header_Gid": invoice_header_gid,
                                                                                                        "entity_gid": entity_gid,
                                                                                                        "type": "ERROR_UPDATE",
                                                                                                        "employee_gid": employee_gid,
                                                                                                        "Error_log": {
                                                                                                            "MESSAGE": "ERROR_OCCURED_ON_AP_PAYMENTDETAILS_GET_",
                                                                                                            "DATA": str(
                                                                                                                e)}}
                                                                                                    AP_Header_Update_result = AP_Header_Update(
                                                                                                        header_update_data)
                                                                                                    # pass
                                                                                                    # return JsonResponse({"MESSAGE": "ERROR_OCCURED_ON_PAYMENT_FUNCTION","DATA": str(e)})
                                                                                            else:
                                                                                                header_update_data = {
                                                                                                    "Invoice_Header_Gid": invoice_header_gid,
                                                                                                    "entity_gid": entity_gid,
                                                                                                    "type": "ERROR_UPDATE",
                                                                                                    "employee_gid": employee_gid,
                                                                                                    "Error_log": {
                                                                                                        "MESSAGE": "ERROR_OCCURED_ON_AP INITIATED_UPDATION",
                                                                                                        "DATA": outs}}
                                                                                                AP_Header_Update_result = AP_Header_Update(
                                                                                                    header_update_data)
                                                                                                # pass
                                                                                                # return JsonResponse(outs, safe=False)
                                                                                    else:
                                                                                        # pass
                                                                                        header_update_data = {
                                                                                            "Invoice_Header_Gid": invoice_header_gid,
                                                                                            "entity_gid": entity_gid,
                                                                                            "type": "ERROR_UPDATE",
                                                                                            "employee_gid": employee_gid,
                                                                                            "Error_log": {
                                                                                                "MESSAGE": "ERROR_OCCURED_ON_INVOICE_HEADER_UPDATE",
                                                                                                "OUTPUT_DATA": outs,
                                                                                                "AMOUNT_TRANSFER_DATA": results_data}}
                                                                                        AP_Header_Update_result = AP_Header_Update(
                                                                                            header_update_data)
                                                                                        # return JsonResponse({"MESSAGE": "ERROR_OCCURED_ON_INVOICE_HEADER_UPDATE","DATA": outs,"AMOUNT_TRANSFER_DATA":results_data})
                                                                                except Exception as e:
                                                                                    common.logger.error(e)
                                                                                    header_update_data = {
                                                                                        "Invoice_Header_Gid": invoice_header_gid,
                                                                                        "entity_gid": entity_gid,
                                                                                        "type": "ERROR_UPDATE",
                                                                                        "employee_gid": employee_gid,
                                                                                        "Error_log": {
                                                                                            "MESSAGE": "ERROR_OCCURED_ON_INVOICE_HEADER_UPDATE_",
                                                                                            "AMOUNT_TRANSFER_DATA": results_data}}
                                                                                    AP_Header_Update_result = AP_Header_Update(
                                                                                        header_update_data)
                                                                                    # return JsonResponse({"MESSAGE": "ERROR_OCCURED_ON_INVOICE_HEADER_UPDATE","DATA": str(e),"AMOUNT_TRANSFER_DATA":results_data})
                                                                            else:
                                                                                header_update_data = {
                                                                                    "Invoice_Header_Gid": invoice_header_gid,
                                                                                    "entity_gid": entity_gid,
                                                                                    "type": "ERROR_UPDATE",
                                                                                    "employee_gid": employee_gid,
                                                                                    "Error_log": {"MESSAGE": "FAILED",
                                                                                                  "FAILED_STATUS": results_data}}
                                                                                AP_Header_Update_result = AP_Header_Update(
                                                                                    header_update_data)
                                                                                # return JsonResponse({"MESSAGE": "FAILED", "FAILED_STATUS": results_data})
                                                                        except Exception as e:
                                                                            common.logger.error(e)
                                                                            header_update_data = {
                                                                                "Invoice_Header_Gid": invoice_header_gid,
                                                                                "entity_gid": entity_gid,
                                                                                "type": "ERROR_UPDATE",
                                                                                "employee_gid": employee_gid,
                                                                                "Error_log": {
                                                                                    "MESSAGE": "ERROR_OCCURED_ON_AMOUNT_TRANSFER_CLINET_API_",
                                                                                    "log_data": log_data}}
                                                                            AP_Header_Update_result = AP_Header_Update(
                                                                                header_update_data)
                                                                            # return JsonResponse({"MESSAGE": "ERROR_OCCURED_ON_AMOUNT_TRANSFER_CLINET_API","DATA": str(e), "log_data": log_data})
                                                                    else:
                                                                        header_update_data = {
                                                                            "Invoice_Header_Gid": invoice_header_gid,
                                                                            "entity_gid": entity_gid,
                                                                            "type": "ERROR_UPDATE",
                                                                            "employee_gid": employee_gid, "Error_log": {
                                                                                "MESSAGE": "ERROR_OCCURED_ON_TOKEN_GENERATIONS OR INVALID AUTHENTICATONS"}}
                                                                        AP_Header_Update_result = AP_Header_Update(
                                                                            header_update_data)
                                                                        # return JsonResponse({"MESSAGE": "ERROR_OCCURED_ON_TOKEN_GENERATIONS OR INVALID AUTHENTICATONS"})
                                                                except Exception as e:
                                                                    common.logger.error(e)
                                                                    header_update_data = {
                                                                        "Invoice_Header_Gid": invoice_header_gid,
                                                                        "entity_gid": entity_gid,
                                                                        "type": "ERROR_UPDATE",
                                                                        "employee_gid": employee_gid,
                                                                        "Error_log": {
                                                                            "MESSAGE": "ERROR_OCCURED_TOKEN_GENERATION_",
                                                                            "DATA": str(e), "log_data": log_data}}
                                                                    AP_Header_Update_result = AP_Header_Update(
                                                                        header_update_data)
                                                                    # return JsonResponse({"MESSAGE": "ERROR_OCCURED_TOKEN_GENERATION", "DATA": str(e),"log_data": log_data})
                                                            else:
                                                                header_update_data = {
                                                                    "Invoice_Header_Gid": invoice_header_gid,
                                                                    "entity_gid": entity_gid,
                                                                    "type": "ERROR_UPDATE",
                                                                    "employee_gid": employee_gid, "Error_log": {
                                                                        "MESSAGE": "Credit Amount and Debit Amount Not Equal"}}
                                                                AP_Header_Update_result = AP_Header_Update(
                                                                    header_update_data)
                                                                # return JsonResponse({"MESSAGE": "Credit Amount and Debit Amount Not Equal"})
                                                    else:
                                                        header_update_data = {"Invoice_Header_Gid": invoice_header_gid,
                                                                              "entity_gid": entity_gid,
                                                                              "type": "ERROR_UPDATE",
                                                                              "employee_gid": employee_gid,
                                                                              "Error_log": {
                                                                                  "MESSAGE": "Credit Amount and Debit Amount Not Equal"}}
                                                        AP_Header_Update_result = AP_Header_Update(header_update_data)
                                                        # return JsonResponse({"MESSAGE": "Credit Amount and Debit Amount Not Equal"})
                                                except Exception as e:
                                                    common.logger.error(e)
                                                    header_update_data = {"Invoice_Header_Gid": invoice_header_gid,
                                                                          "entity_gid": entity_gid,
                                                                          "type": "ERROR_UPDATE",
                                                                          "employee_gid": employee_gid,
                                                                          "Error_log": {
                                                                              "MESSAGE": "ERROR_OCCURED_ON_ENTRY_DETAILS_GET_",
                                                                              "DATA": str(e)}}
                                                    AP_Header_Update_result = AP_Header_Update(header_update_data)
                                                    # return JsonResponse({"MESSAGE": "ERROR_OCCURED_ON_ENTRY_DETAILS_GET", "DATA": str(e)})
                                            # return JsonResponse({"MESSAGE": "ERROR_OCCURED_ON_INITIAL_SET", "DATA":out})
                                            # pass
                                            else:
                                                header_update_data = {"Invoice_Header_Gid": invoice_header_gid,
                                                                      "entity_gid": entity_gid,
                                                                      "type": "ERROR_UPDATE",
                                                                      "employee_gid": employee_gid,
                                                                      "Error_log": {
                                                                          "MESSAGE": "ERROR_OCCURED_ON_ACCOUNTING_ENTRY_INITIAL_SET",
                                                                          "OUTPUT": out}}
                                                AP_Header_Update_result = AP_Header_Update(header_update_data)
                                        except Exception as e:
                                            common.logger.error(e)
                                            header_update_data = {"Invoice_Header_Gid": invoice_header_gid,
                                                                  "entity_gid": entity_gid,
                                                                  "type": "ERROR_UPDATE", "employee_gid": employee_gid,
                                                                  "Error_log": {
                                                                      "MESSAGE": "ERROR_OCCURED_ON_ACCOUNTING_ENTRY_INITIAL_SET_",
                                                                      "DATA": str(e), "RESULT": out}}
                                            AP_Header_Update_result = AP_Header_Update(header_update_data)

                                    else:
                                        header_update_data = {"Invoice_Header_Gid": invoice_header_gid,
                                                              "entity_gid": entity_gid,
                                                              "type": "ERROR_UPDATE", "employee_gid": employee_gid,
                                                              "Error_log": {
                                                                  "MESSAGE": "ERROR_OCCURED_ON_AP INITIATED_UPDATION",
                                                                  "OUT": ap_statu_update_result}}
                                        AP_Header_Update_result = AP_Header_Update(header_update_data)
                                        # return JsonResponse({"MESSAGE": "ERROR_OCCURED_ON_AP INITIATED_UPDATION","OUT":ap_statu_update_result})
                                except Exception as e:
                                    common.logger.error(e)
                                    header_update_data = {"Invoice_Header_Gid": invoice_header_gid,
                                                          "entity_gid": entity_gid,
                                                          "type": "ERROR_UPDATE", "employee_gid": employee_gid,
                                                          "Error_log": {"MESSAGE": "ERROR_OCCURED_ON_", "DATA": str(e)}}
                                    AP_Header_Update_result = AP_Header_Update(header_update_data)
                                    # return JsonResponse({"MESSAGE": "ERROR_OCCURED_ON_AP INITIATED_UPDATION", "DATA": str(e)})
                            except Exception as e:
                                common.logger.error(e)
                                header_update_data = {"Invoice_Header_Gid": invoice_header_gid,
                                                      "entity_gid": entity_gid, "type": "ERROR_UPDATE",
                                                      "employee_gid": employee_gid,
                                                      "Error_log": {"MESSAGE": "ERROR_OCCURED_", "DATA": str(e)}}
                                AP_Header_Update_result = AP_Header_Update(header_update_data)
                                # return JsonResponse({"MESSAGE": "ERROR_OCCURED_ON_ACCOUNTING_ENTRY_INITIAL_SET", "DATA": str(e)})
                                # pass


                    except Exception as e:
                        common.logger.error(e)
                        pass
                        # return JsonResponse({"MESSAGE": "ERROR_OCCURED_ON_STATUS_UPDATE", "DATA": str(e)})
            else:
                pass
        except Exception as e:
            common.logger.error(e)
            pass
            # return JsonResponse({"MESSAGE": "ERROR_OCCURED_ON_STATUS_UPDATE", "DATA": str(e)})
    except Exception as e:
        common.logger.error(e)
        pass


def Rejectdata(request):
    utl.check_pointaccess(request)
    utl.check_authorization(request)
    if request.method == 'POST':
        try:
            path = request.path
            reject = mAP.ap_model()
            jsondata = json.loads(request.body.decode('utf-8'))
            reject.group = jsondata.get('params').get('group')
            reject.type = jsondata.get('params').get('type')
            reject.reject_json = jsondata.get('params').get('reject_json')
            reject.entity_gid = int(decry_data(request.session['Entity_gid']))
            common.main_fun1(request.read(), path)
            out = reject.rejectdata_get()
            jdata = out.to_json(orient='records')
            return JsonResponse(jdata, safe=False)
        except Exception as e:
            return JsonResponse({"MESSAGE": "ERROR_OCCURED", "DATA": str(e)})


def Getreason_data(request):
    utl.check_pointaccess(request)
    utl.check_authorization(request)
    if request.method == 'POST':
        try:
            path = request.path
            reject = mAP.ap_model()
            jsondata = json.loads(request.body.decode('utf-8'))
            reject.type = jsondata.get('params').get('type')
            reject.reason_json = jsondata.get('params').get('reason_json')
            reject.entity_gid = int(decry_data(request.session['Entity_gid']))
            common.main_fun1(request.read(), path)
            out = reject.getreasondata()
            jdata = out.to_json(orient='records')
            return JsonResponse(jdata, safe=False)
        except Exception as e:
            return JsonResponse({"MESSAGE": "ERROR_OCCURED", "DATA": str(e)})


def APrejectinv_set(request):
    utl.check_pointaccess(request)
    utl.check_authorization(request)
    if request.method == 'POST':
        try:
            path = request.path
            reject = mAP.ap_model()
            jsondata = json.loads(request.body.decode('utf-8'))
            reject.action = jsondata.get('params').get('action')
            reject.type = jsondata.get('params').get('type')
            reject.reject_json = jsondata.get('params').get('reject_json')
            reject.entity_gid = int(decry_data(request.session['Entity_gid']))
            reject.employee_gid = int(decry_data(request.session['Emp_gid']))
            common.main_fun1(request.read(), path)
            out = outputSplit(reject.set_Invoicereject(), 1)
            return JsonResponse(out, safe=False)
        except Exception as e:
            return JsonResponse({"MESSAGE": "ERROR_OCCURED", "DATA": str(e)})


def Paymmentdtl_get(request):
    utl.check_pointaccess(request)
    utl.check_authorization(request)
    if request.method == 'POST':
        try:
            path = request.path
            payment = mAP.ap_model()
            jsondata = json.loads(request.body.decode('utf-8'))
            payment.group = jsondata.get('params').get('group')
            payment.type = jsondata.get('params').get('type')
            payment.pay_json = jsondata.get('params').get('pay_json')
            payment.entity_gid = int(decry_data(request.session['Entity_gid']))
            common.main_fun1(request.read(), path)
            out = payment.getpaymentdtl()
            jdata = out.to_json(orient='records')
            return JsonResponse(jdata, safe=False)
        except Exception as e:
            return JsonResponse({"MESSAGE": "ERROR_OCCURED", "DATA": str(e)})


def Dropdown_detail_ap(request):
    utl.check_pointaccess(request)
    utl.check_authorization(request)
    if request.method == 'POST':
        try:
            path = request.path
            dropdown = mAP.ap_model()
            jsondata = json.loads(request.body.decode('utf-8'))
            dropdown.tablename = jsondata.get('params').get('tablename')
            dropdown.gid = jsondata.get('params').get('gid')
            dropdown.name = jsondata.get('params').get('name')
            dropdown.entity_gid = int(decry_data(request.session['Entity_gid']))
            common.main_fun1(request.read(), path)
            data = dropdown.get_dropdown_detail()
            jdata = data.to_json(orient='records')
            return JsonResponse(jdata, safe=False)
        except Exception as e:
            return JsonResponse({"MESSAGE": "ERROR_OCCURED", "DATA": str(e)})


def PPPXDeatails_get(request):
    utl.check_pointaccess(request)
    utl.check_authorization(request)
    if request.method == 'POST':
        try:
            path = request.path
            details = mAP.ap_model()
            jsondata = json.loads(request.body.decode('utf-8'))
            details.group = jsondata.get('params').get('group')
            details.type = jsondata.get('params').get('type')
            details.filter = jsondata.get('params').get('Filterdata')
            details.entity_gid = int(decry_data(request.session['Entity_gid']))
            common.main_fun1(request.read(), path)
            data = details.get_ppxdetails()
            jdata = data.to_json(orient='records')
            return JsonResponse(jdata, safe=False)
        except Exception as e:
            return JsonResponse({"MESSAGE": "ERROR_OCCURED", "DATA": str(e)})


def PPPXDeatails_set(request):
    utl.check_pointaccess(request)
    utl.check_authorization(request)
    if request.method == 'POST':
        details = mAP.ap_model()
        jsondata = json.loads(request.body.decode('utf-8'))
        details.action = jsondata.get('params').get('action')
        details.type = ''
        details.header_json = jsondata.get('params').get('header_json')
        details.detail_json = jsondata.get('params').get('detail_json')
        details.entity_gid = int(decry_data(request.session['Entity_gid']))
        details.employee_gid = int(decry_data(request.session['Emp_gid']))
        data = outputSplit(details.set_ppxdetails(), 1)
        return JsonResponse(data, safe=False)


def getpayment_excel(request):
    utl.check_pointaccess(request)
    utl.check_authorization(request)
    df = pd.read_excel(open(str(settings.MEDIA_ROOT) + "/" + "bankdetails.xlsx", 'rb'), sheetname='Sheet1')
    XLSX_MIME = 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    response = HttpResponse(content_type=XLSX_MIME)
    response['Content-Disposition'] = 'attachment; filename="PythonExport.xlsx"'
    writer = pd.ExcelWriter(response, engine='xlsxwriter')
    df.loc[0, 'Bank Name'] = "ICICI"
    df.to_excel(writer, 'Sheet1', index=False)
    email = EmailMessage('Subject', "", to=['vsolvstab@gmail.com'])
    attachment = export_excel(df)
    email.attach('invoice.xlsx', attachment, 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    email.send()
    writer.save()
    return response


def export_excel(df):
    with io.BytesIO() as buffer:
        writer = pd.ExcelWriter(buffer)
        df.to_excel(writer, index=False)
        writer.save()
        return buffer.getvalue()


def Dispatch_Set_Payment(request):
    utl.check_pointaccess(request)
    utl.check_authorization(request)
    if request.method == 'POST':
        try:
            path = request.path
            details = mAP.ap_model()
            jsondata = json.loads(request.body.decode('utf-8'))
            lst = jsondata.get('dispatch_data')
            for x in lst:
                details.action = x.get('action')
                details.type = x.get('type')
                details.in_out = x.get('in_out')
                details.courier_gid = x.get('courier_gid')
                details.Dispatch_date = x.get('Dispatch_date')
                details.send_by = int(decry_data(request.session['Emp_gid']))
                details.awbno = x.get('awbno')
                details.dispatch_mode = x.get('dispatch_mode')
                details.dispatch_type = x.get('dispatch_type')
                details.packets = x.get('packets')
                details.weight = x.get('weight')
                details.dispatch_to = x.get('dispatch_to')
                details.address = x.get('address')
                details.city = x.get('city')
                details.state = x.get('state')
                details.pincode = x.get('pincode')
                details.remark = x.get('remark')
                details.returned = x.get('returned')
                details.returned_on = x.get('returned_on')
                details.returned_remark = x.get('returned_remark')
                details.pod = x.get('pod')
                details.pod_image = x.get('pod_image')
                details.isactive = x.get('isactive')
                details.isremoved = x.get('isremoved')
                details.dispatch_gid = x.get('dispatch_gid')
                details.status = x.get('status')
            details.PAYMENT_JSON = jsondata.get('payment_dtl')
            details.entity_gid = int(decry_data(request.session['Entity_gid']))
            details.employee_gid = int(decry_data(request.session['Emp_gid']))
            common.main_fun1(request.read(), path)
            Service_out = outputSplit(details.set_Dispatchpayment(), 0)
            return JsonResponse(Service_out, safe=False)
        except Exception as e:
            return JsonResponse({"MESSAGE": "ERROR_OCCURED", "DATA": str(e)})


def auditchklist_get(request):
    utl.check_pointaccess(request)
    utl.check_authorization(request)
    if request.method == 'POST':
        try:
            details = mAP.ap_model()
            path = request.path
            jsondata = json.loads(request.body.decode('utf-8'))
            details.type = jsondata.get('params').get('type')
            details.header_gid = jsondata.get('params').get('header_gid')
            details.chk_type = jsondata.get('params').get('chk_type')
            details.entity_gid = int(decry_data(request.session['Entity_gid']))
            common.main_fun1(request.read(), path)
            data = details.get_auditchklist()
            jdata = data.to_json(orient='records')
            return JsonResponse(jdata, safe=False)
        except Exception as e:
            return JsonResponse({"MESSAGE": "ERROR_OCCURED", "DATA": str(e)})


def auditchklist_set(request):
    utl.check_pointaccess(request)
    utl.check_authorization(request)
    if request.method == 'POST':
        try:
            path = request.path
            details = mAP.ap_model()
            jsondata = json.loads(request.body.decode('utf-8'))
            details.action = jsondata.get('params').get('action')
            details.type = jsondata.get('params').get('type')
            details.chklist_json = jsondata.get('params').get('chklist_json')
            details.entity_gid = int(decry_data(request.session['Entity_gid']))
            details.employee_gid = int(decry_data(request.session['Emp_gid']))
            common.main_fun1(request.read(), path)
            out = outputSplit(details.auditchklist(), 1)
            return JsonResponse(out, safe=False)
        except Exception as e:
            return JsonResponse({"MESSAGE": "ERROR_OCCURED", "DATA": str(e)})


def Get_address_ap(request):
    utl.check_pointaccess(request)
    utl.check_authorization(request)
    if request.method == 'POST':
        try:
            path = request.path
            obj_customer_ddl = mAP.ap_model()
            jsondata = json.loads(request.body.decode('utf-8'))
            obj_customer_ddl.location_gid = jsondata.get('params').get('Address_gid')
            obj_customer_ddl.entity_gid = int(decry_data(request.session['Entity_gid']))
            common.main_fun1(request.read(), path)
            df_customer_ddl = obj_customer_ddl.Address_Get()
            jdata = df_customer_ddl.to_json(orient='records')
            return JsonResponse(json.loads(jdata), safe=False)
        except Exception as e:
            return JsonResponse({"MESSAGE": "ERROR_OCCURED", "DATA": str(e)})


def PODDispatch_Set_AP(request):
    utl.check_pointaccess(request)
    utl.check_authorization(request)
    if request.method == 'POST':
        try:
            path = request.path
            dispatch_dtl = mAP.ap_model()
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
                dispatch_dtl.entity_gid = int(decry_data(request.session['Entity_gid']))
            dispatch_dtl.employee_gid = int(decry_data(request.session['Emp_gid']))
            common.main_fun1(request.read(), path)
            Service_out = dispatch_dtl.set_PODDispatch_ap()
            return JsonResponse(Service_out, safe=False)
        except Exception as e:
            return JsonResponse({"MESSAGE": "ERROR_OCCURED", "DATA": str(e)})


def upload_image_ap(request):
    utl.check_pointaccess(request)
    utl.check_authorization(request)
    if request.method == 'POST' and request.FILES['file']:
        try:
            current_month = datetime.now().strftime('%m')
            current_day = datetime.now().strftime('%d')
            current_year_full = datetime.now().strftime('%Y')
            save_path = str(settings.MEDIA_ROOT) + '/AP_POD/' + str(current_year_full) + '/' + str(
                current_month) + '/' + str(current_day) + '/' + str(request.POST['filename'])
            path = default_storage.save(str(save_path), request.FILES['file'])
            db_path = 'media/AP_POD/' + str(current_year_full) + '/' + str(
                current_month) + '/' + str(current_day) + '/' + str(request.POST['filename'])
            # path = default_storage.save(str(save_path), request.FILES['file'])
            return JsonResponse({"MESSAGE": "SUCCESS", "IMAGE_URL": db_path})
        except Exception as ex:
            return JsonResponse({"DATA": str(ex)})


def APStale_set(request):
    utl.check_pointaccess(request)
    utl.check_authorization(request)
    if request.method == 'POST':
        try:
            path = request.path
            details = mAP.ap_model()
            jsondata = json.loads(request.body.decode('utf-8'))
            details.action = jsondata.get('params').get('action')
            details.type = ''
            details.header_json = jsondata.get('params').get('header_json')
            details.entity_gid = int(decry_data(request.session['Entity_gid']))
            details.employee_gid = int(decry_data(request.session['Emp_gid']))
            common.main_fun1(request.read(), path)
            data = outputSplit(details.set_APstale(), 1)
            return JsonResponse(data, safe=False)
        except Exception as e:
            return JsonResponse({"MESSAGE": "ERROR_OCCURED", "DATA": str(e)})


def APNeftExcel_downld(request):
    utl.check_pointaccess(request)
    utl.check_authorization(request)
    if request.method == 'POST':
        try:
            jsondata = json.loads(request.body.decode('utf-8'))
            Amount = jsondata.get('params').get('Amount')
            ACCno = jsondata.get('params').get('ACCno')
            IFSC_code = jsondata.get('params').get('IFSC_code')
            BENIFICIARY_NAME = jsondata.get('params').get('BENIFICIARY_NAME')
            df = pd.read_excel(open(str(settings.MEDIA_ROOT) + "/" + "bankdetails.xlsx", 'rb'), sheetname='Sheet1')
            XLSX_MIME = 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
            response = HttpResponse(content_type=XLSX_MIME)
            response['Content-Disposition'] = 'attachment; filename="PythonExport.xlsx"'
            writer = pd.ExcelWriter(response, engine='xlsxwriter')
            df.loc[0, 'Bank Name'] = ""
            df.loc[0, 'Amount'] = Amount
            df.loc[0, 'Bank beneficiary'] = BENIFICIARY_NAME
            df.loc[0, 'Bank IFSC'] = IFSC_code
            df.loc[0, 'Acc'] = ACCno
            df.to_excel(writer, 'Sheet1', index=False)
            email = EmailMessage('Subject', "", to=['vsolvstab@gmail.com'])
            attachment = export_excel(df)
            email.attach('invoice.xlsx', attachment,
                         'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
            email.send()
            writer.save()
            return JsonResponse({"MESSAGE": "SUCCESS"})
        except Exception as ex:
            return JsonResponse({"DATA": str(ex)})


def stalesummary_get(request):
    utl.check_pointaccess(request)
    utl.check_authorization(request)
    if request.method == 'POST':
        try:
            path = request.path
            details = mAP.ap_model()
            jsondata = json.loads(request.body.decode('utf-8'))
            details.type = jsondata.get('params').get('type')
            details.sub_type = jsondata.get('params').get('sub_type')
            details.filter_json = '{"Payment_Header_Gid":""}'
            details.entity_gid = int(decry_data(request.session['Entity_gid']))
            details.employee_gid = int(decry_data(request.session['Emp_gid']))
            common.main_fun1(request.read(), path)
            data = details.get_stale()
            jdata = data.to_json(orient='records')
            return JsonResponse(jdata, safe=False)
        except Exception as e:
            return JsonResponse({"MESSAGE": "ERROR_OCCURED", "DATA": str(e)})


def classificationdata_get(request):
    utl.check_pointaccess(request)
    utl.check_authorization(request)
    if request.method == 'POST':
        try:
            path = request.path
            classify = mAP.ap_model()
            jsondata = json.loads(request.body.decode('utf-8'))
            classify.type = jsondata.get('params').get('type')
            classify.sub_type = jsondata.get('params').get('Sub_Type')
            classify.jsonData = json.dumps(jsondata.get('params').get('FILTER'))
            classify.json_classification = jsondata.get('params').get('CLASSIFICATION')
            classify.json_classification["Entity_Gid"][0] = int(int(decry_data(request.session['Entity_gid'])))
            common.main_fun1(request.read(), path)
            ld_out_message = classify.get_classification_summary()
            ld_dict = {"DATA": json.loads(ld_out_message.get("DATA").to_json(orient='records')), "MESSAGE": 'FOUND'}
            return JsonResponse(ld_dict, safe=False)
        except Exception as e:
            return JsonResponse({"MESSAGE": "ERROR_OCCURED", "DATA": str(e)})


def supplierdata_get(request):
    utl.check_authorization(request)
    utl.check_pointaccess(request)
    if request.method == 'POST':
        try:
            path = request.path
            classify = mAP.ap_model()
            jsondata = json.loads(request.body.decode('utf-8'))
            classify.type = jsondata.get('params').get('type')
            classify.sub_type = jsondata.get('params').get('Sub_Type')
            classify.jsonData = json.dumps(jsondata.get('params').get('FILTER'))
            classify.json_classification = jsondata.get('params').get('CLASSIFICATION')
            classify.json_classification["Entity_Gid"][0] = int(decry_data(request.session['Entity_gid']))
            common.main_fun1(request.read(), path)
            ld_out_message = classify.get_supplier_data()
            ld_dict = {"DATA": json.loads(ld_out_message.get("DATA").to_json(orient='records')), "MESSAGE": 'FOUND'}
            return JsonResponse(ld_dict, safe=False)
        except Exception as e:
            return JsonResponse({"MESSAGE": "ERROR_OCCURED", "DATA": str(e)})


# ECF

def ECFInvoiceheader_set(request):
    utl.check_pointaccess(request)
    utl.check_authorization(request)
    if request.method == 'POST':
        try:
            path = request.path
            inward_dtl = mAP.ap_model()
            jsondata = json.loads(request.body.decode('utf-8'))
            entity_gid = int(decry_data(request.session['Entity_gid']))
            employee_gid = int(decry_data(request.session['Emp_gid']))
            action = jsondata.get('params').get('action')
            type = jsondata.get('params').get('type')
            # type=jsondata.get('params').get('type')
            # if (action=="INSERT" and type=="INVOICE_HEADER"):
            #     jsondata["params"]["header_json"]["HEADER"][0]["Employee_gid"] = employee_gid
            # jsondata["params"]["header_json"]["HEADER"][0]["Employee_gid"] = employee_gid
            html_file_except = ""
            html_file_status = 1
            if (type == "INVOICE_HEADER"):
                try:
                    notepad = jsondata.get("params").get("header_json").get("HEADER")[0].get("notepad")
                    if notepad != "":

                        millis = int(round(time.time() * 1000))
                        filename = str(employee_gid) + "_" + str(millis) + '.txt'
                        s3 = boto3.resource('s3')
                        object = s3.Object(S3_BUCKET_NAME, filename)
                        object.put(Body=notepad)
                        jsondata['params']['header_json']['HEADER'][0]['html_file_ky'] = filename
                        jsondata['params']['header_json']['HEADER'][0]['notepad'] = ""
                    else:
                        filename = ""
                except Exception as e:
                    html_file_status = 0
                    html_file_except = {"MESSAGE": "ERROR_OCCURED", "DATA": str(e)}
            inward_dtl.action = jsondata.get('params').get('action')
            inward_dtl.type = jsondata.get('params').get('type')
            inward_dtl.header_json = jsondata.get('params').get('header_json')
            inward_dtl.debit_json = jsondata.get('params').get('debit_json')
            inward_dtl.detail_json = jsondata.get('params').get('detail_json')
            inward_dtl.status_json = jsondata.get('params').get('status_json')
            inward_dtl.entity_gid = entity_gid
            inward_dtl.employee_gid = employee_gid
            status = inward_dtl.status_json.get("Status")
            if (inward_dtl.action == "UPDATE" and inward_dtl.type == "STATUS" and status == "APPROVED"):
                find_creted = inward_dtl.header_json[0].get("invoiceheader_employeegid")
                if (find_creted == inward_dtl.employee_gid):
                    return JsonResponse("Invoice Creater Can't Be Approve", safe=False)
                else:
                    common.main_fun1(request.read(), path)
                    # out = outputSplit(inward_dtl.set_ECFInvoiceheader(), 1)
                    out = outputSplit(inward_dtl.set_ECFInvoice_Status(), 1)
            else:
                common.main_fun1(request.read(), path)
                out = outputSplit(inward_dtl.set_ECFInvoiceheader(), 1)
            if (inward_dtl.action == "UPDATE" and inward_dtl.type == "STATUS" and out == "SUCCESS"):
                if (status == "APPROVED" or status == "REJECTED"):
                    entity_gid = int(decry_data(request.session['Entity_gid']))
                    create_by = int(decry_data(request.session['Emp_gid']))
                    try:
                        invoiceheader_data = inward_dtl.header_json[0]
                        invoiceheader_gid = invoiceheader_data.get("invoiceheader_gid")
                        inward_dtl.action = "GET"
                        inward_dtl.type = "MAIL_TEMPLATE"
                        inward_dtl.filter = json.dumps({"template_name": "ECF_APPROVE", "header_gid": invoiceheader_gid,
                                                        "queryname": "ECF APPROVE"})
                        inward_dtl.classification = json.dumps(
                            {"Entity_Gid": inward_dtl.entity_gid, "Emp_gid": inward_dtl.employee_gid})
                        templates_data = inward_dtl.get_multiple_email_templates_data()
                        Mail_Data = templates_data.get("Mail_Data")[0].get("mailtemplate_body")
                        Header_Data = templates_data.get("Header_Data")[0]
                        for (k, v) in Header_Data.items():
                            value = str(v)
                            key = "{{" + k + "}}"
                            Mail_Data = Mail_Data.replace(key, value);
                        cleanr = re.compile('<.*?>')
                        body_text = re.sub(cleanr, '', Mail_Data)
                        # email = EmailMessage('ECF Approved Successfully', body_text, to=[to_email])
                        # email.send()
                        # to_email = "rvignesh@vsolv.co.in"
                        to_email = "vsolvstab@gmail.com"
                        mail_status = CoreViews.sending_mail(Mail_Data, to_email, body_text)
                        if (mail_status == "SUCCESS"):
                            return JsonResponse(mail_status, safe=False)
                        else:
                            mail_error_message = mail_status
                            return JsonResponse({"MESSAGE": "ERROR_OCCURED", "ERROR": mail_error_message})
                    except Exception as ex:
                        return JsonResponse("Email_Not_Send", safe=False)
                else:
                    JsonResponse(out, safe=False)
            if (type == "INVOICE_HEADER" and html_file_status == 0):
                return JsonResponse({"MESSAGE": "ERROR_OCCURED",
                                     "DATA": {"ECF_CREATION_STATUS": out, "NOTES_INSERT_STATUS": html_file_except}})
            return JsonResponse(out, safe=False)
        except Exception as e:
            return JsonResponse({"MESSAGE": "ERROR_OCCURED", "DATA": str(e)})


def ECF_Multiple_set(request):
    utl.check_pointaccess(request)
    utl.check_authorization(request)
    if request.method == 'POST':
        inward_dtl = mAP.ap_model()
        jsondata = json.loads(request.body.decode('utf-8'))
        if (jsondata.get('params').get('action') == "UPDATE" and jsondata.get('params').get(
                'type') == "STATUS" and jsondata.get('params').get('sub_type') == "MULTIPLE_UPDATE"):
            all_header = jsondata.get('params').get('status_json')
            all_header_length = len(all_header)
            all_header_final_status = 0;
            for x in all_header:
                try:
                    inward_dtl.action = jsondata.get('params').get('action')
                    inward_dtl.type = jsondata.get('params').get('type')
                    inward_dtl.header_json = jsondata.get('params').get('header_json')
                    inward_dtl.debit_json = jsondata.get('params').get('debit_json')
                    inward_dtl.detail_json = jsondata.get('params').get('detail_json')
                    inward_dtl.status_json = x
                    inward_dtl.entity_gid = int(decry_data(request.session['Entity_gid']))
                    inward_dtl.employee_gid = int(decry_data(request.session['Emp_gid']))
                    out = outputSplit(inward_dtl.set_ECFInvoiceheader(), 1)
                    if out == 'SUCCESS':
                        all_header_final_status += 1

                except Exception as e:
                    return JsonResponse({"MESSAGE": "ERROR_OCCURED"})

            if (all_header_final_status == all_header_length):
                return JsonResponse(out, safe=False)
            else:
                out = "Some Invoice Not Approved"
                return JsonResponse(out, safe=False)


def ECFInvoice_get(request):
    utl.check_pointaccess(request)
    utl.check_authorization(request)
    if request.method == 'POST':
        try:
            path = request.path
            invoice_get = mAP.ap_model()
            jsondata = json.loads(request.body.decode('utf-8'))
            invoice_get.action = jsondata.get('params').get('action')
            invoice_get.ecfnumber = jsondata.get('params').get('ecfnumber')
            invoice_get.supplier_gid = jsondata.get('params').get('supplier_gid')
            invoice_get.inwarddetail_gid = jsondata.get('params').get('inwarddetail_gid')
            invoice_get.inwardheader_gid = jsondata.get('params').get('inwardheader_gid')
            invoice_get.status = jsondata.get('params').get('status')
            invoice_get.entity_gid = int(decry_data(request.session['Entity_gid']))
            invoice_get.state_gid = request.session['Entity_state_gid']
            common.main_fun1(request.read(), path)
            out = invoice_get.ECFInvoice_get()
            jdata = out.to_json(orient='records')
            return JsonResponse(json.loads(jdata), safe=False)
        except Exception as e:
            return JsonResponse({"MESSAGE": "ERROR_OCCURED", "DATA": str(e)})


def ECFInvoice_set(request):
    utl.check_pointaccess(request)
    utl.check_authorization(request)
    if request.method == 'POST':
        try:
            path = request.path
            inward_dtl = mAP.ap_model()
            jsondata = json.loads(request.body.decode('utf-8'))
            inward_dtl.action = jsondata.get('params').get('action')
            inward_dtl.type = jsondata.get('params').get('type')
            inward_dtl.header_json = jsondata.get('params').get('header_json')
            inward_dtl.detail_json = jsondata.get('params').get('detail_json')
            inward_dtl.invoice_json = jsondata.get('params').get('invoice_json')
            inward_dtl.debit_json = jsondata.get('params').get('debit_json')
            inward_dtl.credit_json = jsondata.get('params').get('credit_json')
            inward_dtl.status_json = jsondata.get('params').get('status_json')
            inward_dtl.entity_gid = int(decry_data(request.session['Entity_gid']))
            inward_dtl.employee_gid = int(decry_data(request.session['Emp_gid']))
            common.main_fun1(request.read(), path)
            out = outputSplit(inward_dtl.ECFset_Invoice(), 1)
            return JsonResponse(out, safe=False)
        except Exception as e:
            return JsonResponse({"MESSAGE": "ERROR_OCCURED", "DATA": str(e)})


def ECFInvoiceChecker_get(request):
    utl.check_pointaccess(request)
    utl.check_authorization(request)
    if request.method == 'POST':
        try:
            path = request.path
            invoice_get = mAP.ap_model()
            jsondata = json.loads(request.body.decode('utf-8'))
            invoice_get.action = jsondata.get('params').get('action')
            invoice_get.ecfnumber = jsondata.get('params').get('ecfnumber')
            invoice_get.supplier_gid = jsondata.get('params').get('supplier_gid')
            invoice_get.inwarddetail_gid = jsondata.get('params').get('inwarddetail_gid')
            invoice_get.inwardheader_gid = jsondata.get('params').get('inwardheader_gid')
            invoice_get.status = jsondata.get('params').get('status')
            invoice_get.entity_gid = int(decry_data(request.session['Entity_gid']))
            invoice_get.state_gid = request.session['Entity_state_gid']
            common.main_fun1(request.read(), path)
            out = invoice_get.ECFInvoice_get()
            out = out.fillna(0)
            if invoice_get.action == 'INVOICE_DETAILS_EDIT':
                df_invoice = (out[['invoicedetails_gid', 'invoicedetails_item', 'invoicedetails_desc',
                                   'invoicedetails_hsncode', 'invoicedetails_unitprice', 'invoicedetails_qty',
                                   'invoicedetails_sgst',
                                   'invoicedetails_cgst', 'invoicedetails_igst', 'invoicedetails_amount',
                                   'invoicedetails_totalamt']]).groupby(
                    ['invoicedetails_gid', 'invoicedetails_item', 'invoicedetails_desc', 'invoicedetails_hsncode',
                     'invoicedetails_unitprice', 'invoicedetails_qty', 'invoicedetails_sgst',
                     'invoicedetails_cgst', 'invoicedetails_igst', 'invoicedetails_amount',
                     'invoicedetails_totalamt']).size().reset_index();
                df_debit = out.groupby(
                    ['invoicedetails_gid', 'debit_gid', 'debit_categorygid', 'debit_subcategorygid',
                     'debit_glno', 'debit_amount', 'ccbsjsondata', 'tbs_name']).size().reset_index()
                df_credit = (out[['credit_gid', 'credit_paymodegid', 'credit_refno', 'bankbranch_ifsccode',
                                  'credit_glno', 'credit_amount', 'Paymode_name', 'bankdetails_beneficiaryname',
                                  'credit_suppliertaxtrate', 'suppliertax_panno', 'credit_suppliertaxtype',
                                  'ppxdetails_ppxheadergid', 'ppxdetails_gid', 'bankbranch_name']]).groupby(
                    ['credit_gid', 'credit_paymodegid', 'credit_refno', 'bankbranch_ifsccode',
                     'credit_glno', 'credit_amount', 'Paymode_name', 'bankdetails_beneficiaryname',
                     'credit_suppliertaxtrate', 'suppliertax_panno', 'credit_suppliertaxtype',
                     'ppxdetails_ppxheadergid', 'ppxdetails_gid', 'bankbranch_name']).size().reset_index();
                df_credit.loc[df_credit['Paymode_name'] != 'NEFT', 'bankbranch_ifsccode'] = ''
                df_credit.loc[df_credit['Paymode_name'] != 'NEFT', 'bankdetails_beneficiaryname'] = ''
                df_credit.loc[df_credit['Paymode_name'] != 'NEFT', 'bankbranch_name'] = ''
            else:
                df_invoice = (out[['invoicedetails_gid', 'invoicedetails_item', 'invoicedetails_desc',
                                   'invoicedetails_hsncode', 'invoicedetails_unitprice', 'invoicedetails_qty',
                                   'invoicedetails_sgst',
                                   'invoicedetails_cgst', 'invoicedetails_igst', 'invoicedetails_amount',
                                   'invoicedetails_totalamt']]).groupby(
                    ['invoicedetails_gid', 'invoicedetails_item', 'invoicedetails_desc', 'invoicedetails_hsncode',
                     'invoicedetails_unitprice', 'invoicedetails_qty', 'invoicedetails_sgst',
                     'invoicedetails_cgst', 'invoicedetails_igst', 'invoicedetails_amount',
                     'invoicedetails_totalamt']).size().reset_index();
                df_debit = out.groupby(
                    ['invoicedetails_gid', 'debit_gid', 'debit_categorygid', 'debit_subcategorygid',
                     'debit_glno', 'debit_amount', 'ccbsjsondata']).size().reset_index();
                df_credit = (out[['credit_gid', 'credit_paymodegid', 'credit_refno', 'bankbranch_ifsccode',
                                  'credit_glno', 'credit_amount', 'Paymode_name', 'bankdetails_beneficiaryname',
                                  'ppxdetails_ppxheadergid', 'ppxdetails_gid', 'bankbranch_name'
                                  ]]).groupby(
                    ['credit_gid', 'credit_paymodegid', 'credit_refno', 'bankbranch_ifsccode',
                     'credit_glno', 'credit_amount', 'Paymode_name', 'bankdetails_beneficiaryname',
                     'ppxdetails_ppxheadergid', 'ppxdetails_gid', 'bankbranch_name'
                     ]).size().reset_index();
                df_credit.loc[df_credit['Paymode_name'] != 'NEFT', 'bankbranch_ifsccode'] = ''
                df_credit.loc[df_credit['Paymode_name'] != 'NEFT', 'bankdetails_beneficiaryname'] = ''
                df_credit.loc[df_credit['Paymode_name'] != 'NEFT', 'bankbranch_name'] = ''

            data = {}
            data['invoice'] = json.loads(df_invoice.to_json(orient='records'))
            data['debit'] = json.loads(df_debit.to_json(orient='records'))
            data['credit'] = json.loads(df_credit.to_json(orient='records'))
            jdata = data
            return JsonResponse(jdata, safe=False)
        except Exception as e:
            return JsonResponse({"MESSAGE": "ERROR_OCCURED", "DATA": str(e)})


def ECF_ApChecker_get(request):
    utl.check_pointaccess(request)
    utl.check_authorization(request)
    if request.method == 'POST':
        try:
            path = request.path
            invoice_get = mAP.ap_model()
            jsondata = json.loads(request.body.decode('utf-8'))
            invoice_get.action = jsondata.get('params').get('action')
            invoice_get.ecfnumber = jsondata.get('params').get('ecfnumber')
            invoice_get.supplier_gid = jsondata.get('params').get('supplier_gid')
            invoice_get.inwarddetail_gid = jsondata.get('params').get('inwarddetail_gid')
            invoice_get.inwardheader_gid = jsondata.get('params').get('inwardheader_gid')
            invoice_get.status = jsondata.get('params').get('status')
            invoice_get.entity_gid = int(decry_data(request.session['Entity_gid']))
            invoice_get.state_gid = request.session['Entity_state_gid']
            common.main_fun1(request.read(), path)
            out = invoice_get.ECFInvoice_get()
            out = out.fillna(0)
            if invoice_get.action == 'ECF_DETAILS_EDIT':
                df_invoice = (
                    out[['invoicedetails_gid', 'invoiceheader_taxableamt', 'invoicedetails_item', 'invoicedetails_desc',
                         'invoicedetails_hsncode', 'invoicedetails_unitprice', 'invoicedetails_qty',
                         'invoicedetails_sgst',
                         'invoicedetails_cgst', 'invoicedetails_igst', 'invoicedetails_amount',
                         'invoicedetails_discount', 'invoicedetails_totalamt', 'DEBIT_DETAILS']]).groupby(
                    ['invoicedetails_gid', 'invoiceheader_taxableamt', 'invoicedetails_item', 'invoicedetails_desc',
                     'invoicedetails_hsncode',
                     'invoicedetails_unitprice', 'invoicedetails_qty', 'invoicedetails_sgst',
                     'invoicedetails_cgst', 'invoicedetails_igst', 'invoicedetails_amount', 'invoicedetails_discount',
                     'invoicedetails_totalamt', 'DEBIT_DETAILS']).size().reset_index();
                df_debit = out.groupby(
                    ['invoicedetails_gid', 'debit_gid', 'debit_categorygid', 'debit_subcategorygid',
                     'debit_glno', 'debit_amount', 'DEBIT_DETAILS']).size().reset_index()
                df_credit = (out[
                    ['bankdetails_gid', 'credit_gid', 'credit_paymodegid', 'credit_refno', 'bankbranch_ifsccode',
                     'bankdetails_bank_gid',
                     'credit_glno', 'credit_amount', 'Paymode_name', 'bankdetails_beneficiaryname',
                     'credit_suppliertaxtrate', 'credit_suppliertaxtype',
                     'ppxdetails_ppxheadergid', 'ppxdetails_gid', 'bankbranch_name', 'credit_taxableamount',
                     'credit_categorygid', 'credit_subcategorygid']]).groupby(
                    ['bankdetails_gid', 'credit_gid', 'credit_paymodegid', 'credit_refno', 'bankbranch_ifsccode',
                     'bankdetails_bank_gid',
                     'credit_glno', 'credit_amount', 'Paymode_name', 'bankdetails_beneficiaryname',
                     'credit_suppliertaxtrate', 'credit_suppliertaxtype',
                     'ppxdetails_ppxheadergid', 'ppxdetails_gid', 'bankbranch_name', 'credit_taxableamount',
                     'credit_categorygid', 'credit_subcategorygid']).size().reset_index();
                df_credit.loc[df_credit['Paymode_name'] != 'NEFT', 'bankbranch_ifsccode'] = ''
                df_credit.loc[df_credit['Paymode_name'] != 'NEFT', 'bankdetails_beneficiaryname'] = ''
                df_credit.loc[df_credit['Paymode_name'] != 'NEFT', 'bankbranch_name'] = ''
            else:
                df_invoice = (out[['invoicedetails_gid', 'invoicedetails_item', 'invoicedetails_desc',
                                   'invoicedetails_hsncode', 'invoicedetails_unitprice', 'invoicedetails_qty',
                                   'invoicedetails_sgst',
                                   'invoicedetails_cgst', 'invoicedetails_igst', 'invoicedetails_amount',
                                   'invoicedetails_discount',
                                   'invoicedetails_totalamt', 'DEBIT_DETAILS']]).groupby(
                    ['invoicedetails_gid', 'invoicedetails_item', 'invoicedetails_desc', 'invoicedetails_hsncode',
                     'invoicedetails_unitprice', 'invoicedetails_qty', 'invoicedetails_sgst',
                     'invoicedetails_cgst', 'invoicedetails_igst', 'invoicedetails_amount', 'invoicedetails_discount',
                     'invoicedetails_totalamt', 'DEBIT_DETAILS']).size().reset_index();
                df_debit = out.groupby(
                    ['invoicedetails_gid', 'debit_gid', 'debit_categorygid', 'debit_subcategorygid',
                     'debit_glno', 'debit_amount']).size().reset_index();
                df_credit = (out[['credit_gid', 'credit_paymodegid', 'credit_refno', 'bankbranch_ifsccode',
                                  'credit_glno', 'credit_amount', 'Paymode_name', 'bankdetails_beneficiaryname',
                                  'ppxdetails_ppxheadergid', 'ppxdetails_gid', 'bankbranch_name'
                                  ]]).groupby(
                    ['credit_gid', 'credit_paymodegid', 'credit_refno', 'bankbranch_ifsccode',
                     'credit_glno', 'credit_amount', 'Paymode_name', 'bankdetails_beneficiaryname',
                     'ppxdetails_ppxheadergid', 'ppxdetails_gid', 'bankbranch_name'
                     ]).size().reset_index();
                df_credit.loc[df_credit['Paymode_name'] != 'NEFT', 'bankbranch_ifsccode'] = ''
                df_credit.loc[df_credit['Paymode_name'] != 'NEFT', 'bankdetails_beneficiaryname'] = ''
                df_credit.loc[df_credit['Paymode_name'] != 'NEFT', 'bankbranch_name'] = ''

            data = {}
            data['invoice'] = json.loads(df_invoice.to_json(orient='records'))
            data['debit'] = json.loads(df_debit.to_json(orient='records'))
            data['credit'] = json.loads(df_credit.to_json(orient='records'))
            jdata = data
            return JsonResponse(jdata, safe=False)
        except Exception as e:
            return JsonResponse({"MESSAGE": "ERROR_OCCURED", "DATA": str(e)})


import tempfile
from num2words import num2words
from camelcase import CamelCase


def common_pdf_gen(output, create_by):
    ecf_no = str(output.get('INVOICE_HEADER')[0].get('invoiceheader_crno'))
    EAN = barcode.get_barcode_class('Code128')
    ean = EAN(ecf_no, writer=ImageWriter())
    concat_filename = str(create_by) + "_" + str(ecf_no) + "_" + "ecf_barcode" + ".png"
    save_file = str(create_by) + "_" + str(ecf_no) + "_" + "ecf_barcode"
    tmp = tempfile.NamedTemporaryFile()
    with open(tmp.name, 'wb') as f:
        EAN(ecf_no, writer=ImageWriter()).write(f)
    with open(tmp.name, 'rb') as f:
        contents = f.read()
    s3 = boto3.resource('s3')
    s3_obj = s3.Object(bucket_name=S3_BUCKET_NAME, key=concat_filename)
    s3_obj.put(Body=contents)
    s3_client = boto3.client('s3', 'ap-south-1')
    response = s3_client.generate_presigned_url('get_object',
                                                Params={'Bucket': S3_BUCKET_NAME,
                                                        'Key': concat_filename},
                                                ExpiresIn=3600)
    classify = {
        "bar_code_path": response,
        "logo_path": ip + "/static/Images/kvbLogo.png"
    }
    output['INVOICE_HEADER'][0].update(classify)
    invoicedetails_totalamt = 0
    for i in output.get('INVOICE_DETAIL'):
        invoicedetails_totalamt = invoicedetails_totalamt + i.get('invoicedetails_totalamt')

    debit_amount = 0
    for i in output.get('DEBIT'):
        debit_amount = debit_amount + i.get('debit_amount')

    credit_amount = 0
    for i in output.get('CREDIT'):
        credit_amount = credit_amount + i.get('credit_amount')

    no_to_words = num2words(int(invoicedetails_totalamt))
    output['title_pdf'] = "Expense Claim Form - " + str(
        output.get('INVOICE_HEADER')[0].get('invoiceheader_invoicetype'))
    c = CamelCase()
    no_to_words = str(no_to_words)
    output['no_to_words'] = c.hump(no_to_words)
    output['credit_amount'] = str(credit_amount) + "0"
    output['debit_amount'] = str(debit_amount) + "0"
    output['invoicedetails_totalamt'] = str(invoicedetails_totalamt) + "0"
    pdf = HttpResponse(content_type='application/pdf')
    pdf['Content-Disposition'] = 'attachment; filename="somefilename.pdf"'
    pdf = render_to_pdf(BASE_DIR + '/Bigflow/Templates/Shared/claimform_template.html', output)
    return pdf


def render_to_pdf(template_src, context_dict):
    template = get_template(template_src)
    html = template.render(context_dict)
    result = BytesIO()
    pdf = pisa.pisaDocument(BytesIO(html.encode("ISO-8859-1")), result)
    if not pdf.err:
        return HttpResponse(result.getvalue(), content_type='application/pdf')
    return None


def ECF_Process_Get(request):
    utl.check_pointaccess(request)
    utl.check_authorization(request)
    if request.method == 'POST':
        try:
            ecf_obj = mAP.ap_model()
            path = request.path
            jsondata = json.loads(request.body.decode('utf-8'))
            create_by = int(decry_data(request.session['Emp_gid']))
            Entity_gid = int(decry_data(request.session['Entity_gid']))
            jsondata["params"]["filter"]["employee_gid"] = create_by
            action = jsondata.get('params').get('action')
            type = jsondata.get('params').get('type')
            if (action == "GET" and (
                    type == "INVOICE_MAKER_SUMMARY" or type == "COMMODITY_DATA" or type == "INVOICE_MAKER_SUMMARY_COUNT" or
                    type == "APPROVER_NAME" or type == "GL_DETAILS" or
                    type == "PO_NUMBER" or type == "ECF_HEADER_DATA" or type == "ECF_TO_AP_DATA" or
                    type == "NOTE_DATA")):
                ecf_obj.action = action
                ecf_obj.type = type
                ecf_obj.filter = json.dumps(jsondata.get('params').get('filter'))
                ecf_obj.classification = json.dumps({"Entity_Gid": Entity_gid})
                ecf_obj.create_by = create_by
                common.main_fun1(request.read(), path)
                output = ecf_obj.get_ecf_details()
                jdata = output.to_json(orient='records')
                return JsonResponse(json.loads(jdata), safe=False)
            elif (action == "GET" and (type == "DEBIT_DETAILS" or type == "CCBS_DETAILS")):
                ecf_obj.action = action
                ecf_obj.type = type
                ecf_obj.filter = json.dumps(jsondata.get('params').get('filter'))
                ecf_obj.classification = json.dumps({"Entity_Gid": Entity_gid})
                ecf_obj.create_by = create_by
                common.main_fun1(request.read(), path)
                output = ecf_obj.get_ecf_debit_details()
                jdata = output.to_json(orient='records')
                return JsonResponse(json.loads(jdata), safe=False)
            elif (action == "GET" and type == "FIND_ECF_DUPLICATE"):
                ecf_obj.action = action
                ecf_obj.type = type
                ecf_obj.filter = json.dumps(jsondata.get('params').get('filter'))
                ecf_obj.classification = json.dumps({"Entity_Gid": Entity_gid})
                ecf_obj.create_by = create_by
                common.main_fun1(request.read(), path)
                output = ecf_obj.get_ecf_duplicate_details()
                jdata = output.to_json(orient='records')
                return JsonResponse(json.loads(jdata), safe=False)
            elif (action == "GET" and type == "CREDIT_DETAILS"):
                ecf_obj.action = action
                ecf_obj.type = type
                ecf_obj.filter = json.dumps(jsondata.get('params').get('filter'))
                ecf_obj.classification = json.dumps({"Entity_Gid": Entity_gid})
                ecf_obj.create_by = create_by
                common.main_fun1(request.read(), path)
                output = ecf_obj.get_ecf_credit_details()
                jdata = output.to_json(orient='records')
                return JsonResponse(json.loads(jdata), safe=False)
            elif (action == "GET" and (type == "ECF_HEADER_BY_BRANCH" or type == "ECF_HEADER_BY_BRANCH_COUNT")):
                ecf_obj.action = action
                ecf_obj.type = type
                Branch_Gid = request.session['Branch_gid']
                jsondata['params']['filter']['branch_gid'] = Branch_Gid
                ecf_obj.filter = json.dumps(jsondata.get('params').get('filter'))
                ecf_obj.classification = json.dumps({"Entity_Gid": Entity_gid})
                ecf_obj.create_by = create_by
                common.main_fun1(request.read(), path)
                output = ecf_obj.get_ecf_details()
                jdata = output.to_json(orient='records')
                return JsonResponse(json.loads(jdata), safe=False)
            elif (action == "GET" and type == "ECF_CO_HEADER_BY_BRANCH"):
                ecf_obj.action = action
                ecf_obj.type = "ECF_HEADER_BY_BRANCHCO"
                ecf_obj.filter = json.dumps(jsondata.get('params').get('filter'))
                ecf_obj.classification = json.dumps({"Entity_Gid": Entity_gid})
                ecf_obj.create_by = create_by
                common.main_fun1(request.read(), path)
                output = ecf_obj.get_ecf_details()
                jdata = output.to_json(orient='records')
                return JsonResponse(json.loads(jdata), safe=False)
            elif (action == "GET" and type == "ECF_HEADER_BY_BRANCHCO_COUNT"):
                ecf_obj.action = action
                ecf_obj.type = type
                ecf_obj.filter = json.dumps(jsondata.get('params').get('filter'))
                ecf_obj.classification = json.dumps({"Entity_Gid": Entity_gid})
                ecf_obj.create_by = create_by
                common.main_fun1(request.read(), path)
                output = ecf_obj.get_ecf_details()
                jdata = output.to_json(orient='records')
                return JsonResponse(json.loads(jdata), safe=False)
            elif (action == "GET" and type == "INVOICE_APPROVAL"):
                ecf_obj.action = action
                ecf_obj.type = type
                ecf_obj.filter = json.dumps(jsondata.get('params').get('filter'))
                ecf_obj.classification = json.dumps({"Entity_Gid": Entity_gid})
                ecf_obj.create_by = create_by
                common.main_fun1(request.read(), path)
                output = ecf_obj.get_ecf_approval_details()
                jdata = output.to_json(orient='records')
                return JsonResponse(json.loads(jdata), safe=False)
            elif (action == "GET" and type == "INVOICE_DETAILS_EDIT"):
                ecf_obj.action = action
                ecf_obj.type = type
                ecf_obj.filter = json.dumps(jsondata.get('params').get('filter'))
                ecf_obj.classification = json.dumps({"Entity_Gid": Entity_gid})
                ecf_obj.create_by = int(decry_data(request.session['Emp_gid']))
                common.main_fun1(request.read(), path)
                output = ecf_obj.get_ecf_billentry_details()
                return JsonResponse(output, safe=False)
            elif (action == "GET" and type == "APPROVER_NAME_1"):
                ecf_obj.action = action
                ecf_obj.type = type
                ecf_obj.filter = json.dumps(jsondata.get('params').get('filter'))
                ecf_obj.classification = json.dumps({"Entity_Gid": Entity_gid})
                ecf_obj.create_by = request.session['Emp_gid']
                common.main_fun1(request.read(), path)
                output = ecf_obj.get_ecfAP_billentry_details()
                return JsonResponse(output, safe=False)
            elif (action == "GET" and type == "BARCODE_GENERATION"):
                ecf_obj.action = action
                ecf_obj.type = type
                ecf_obj.filter = json.dumps(jsondata.get('params').get('filter'))
                ecf_obj.classification = json.dumps({"Entity_Gid": Entity_gid})
                ecf_obj.create_by = create_by
                output = ecf_obj.get_ecf_pdf_data()
                ecf_no = str(output.get('INVOICE_HEADER')[0].get('invoiceheader_crno'))
                invoice_set = mAP.ap_model()
                invoice_set.action = 'GET'
                invoice_set.type = 'ECF_TRANS_GET'
                filter = {
                    "Ref_Name": "ECF_INVOICE",
                    "RefTable_Gid": output.get('INVOICE_HEADER')[0].get('invoiceheader_gid')
                }
                invoice_set.filter = json.dumps(filter)
                invoice_set.classification = json.dumps({"Entity_Gid": Entity_gid})
                invoice_set.create_by = create_by
                out = invoice_set.get_invoice_all()
                jdata = out.to_json(orient='records')
                jdata = json.loads(jdata)
                output['TRAN_DATA'] = jdata
                retuendata = common_pdf_gen(output, create_by)
                return retuendata
            elif (action == "GET" and type == "BARCODE_GENERATION_AP"):
                ecf_obj.action = action
                ecf_obj.type = "INVOICE_HEADER"
                data = jsondata.get('params').get('filter')
                data['Entity_Gid'] = Entity_gid
                ecf_obj.filter = json.dumps(data)
                output_hd = ecf_obj.get_hedergid_crnno()
                jdata = output_hd.to_json(orient='records')
                jdata = json.loads(jdata)
                if jdata != []:
                    hedergid = jdata[0].get('invoiceheader_gid')
                    ecf_obj.action = action
                    ecf_obj.type = "BARCODE_GENERATION"
                    ecf_obj.filter = json.dumps({"InvoiceHeader_Gid": hedergid})
                    ecf_obj.classification = json.dumps({"Entity_Gid": Entity_gid})
                    ecf_obj.create_by = create_by
                    output = ecf_obj.get_ecf_pdf_data()
                    ecf_no = str(output.get('INVOICE_HEADER')[0].get('invoiceheader_crno'))
                    invoice_set = mAP.ap_model()
                    invoice_set.action = 'GET'
                    invoice_set.type = 'ECF_TRANS_GET'
                    filter = {
                        "Ref_Name": "ECF_INVOICE",
                        "RefTable_Gid": output.get('INVOICE_HEADER')[0].get('invoiceheader_gid')
                    }
                    invoice_set.filter = json.dumps(filter)
                    invoice_set.classification = json.dumps({"Entity_Gid": Entity_gid})
                    invoice_set.create_by = create_by
                    out = invoice_set.get_invoice_all()
                    jdata = out.to_json(orient='records')
                    jdata = json.loads(jdata)
                    output['TRAN_DATA'] = jdata
                    retuendata = common_pdf_gen(output, create_by)
                    return retuendata
        except Exception as e:
            return JsonResponse({"MESSAGE": "ERROR_OCCURED", "DATA": str(e)})


def set_Ammort(request):
    utl.check_pointaccess(request)
    utl.check_authorization(request)
    if request.method == 'POST':
        try:
            path = request.path
            ammort_set = mAP.ap_model()
            jsondata = json.loads(request.body.decode('utf-8'))
            action = jsondata.get('params').get('action')
            type = jsondata.get('params').get('type')
            if (action == "INSERT" and (type == "AMMORT_SCHEDULE_SET" or type == "AMMORT_STATUS")):
                ammort_set.action = action
                ammort_set.type = type
                ammort_set.filter = json.dumps(jsondata.get('params').get('filter'))
                ammort_set.classification = json.dumps({"Entity_Gid": int(decry_data(request.session['Entity_gid']))})
                ammort_set.create_by = int(decry_data(request.session['Emp_gid']))
                common.main_fun1(request.read(), path)
                output = ammort_set.set_ammort_details()
                return HttpResponse(output)
            if (action == "UPDATE" and (type == "AMMORT_STATUS_UPDATE" or type == "AMMORT_HOLD_UPDATE")):
                ammort_set.action = action
                ammort_set.type = type
                ammort_set.filter = json.dumps(jsondata.get('params').get('filter'))
                ammort_set.classification = json.dumps({"Entity_Gid": int(decry_data(request.session['Entity_gid']))})
                ammort_set.create_by = int(decry_data(request.session['Emp_gid']))
                common.main_fun1(request.read(), path)
                output = ammort_set.set_ammort_details()
                return HttpResponse(output)
        except Exception as e:
            return JsonResponse({"MESSAGE": "ERROR_OCCURED", "DATA": str(e)})


def get_Ammort(request):
    utl.check_pointaccess(request)
    utl.check_authorization(request)
    if request.method == 'POST':
        try:
            path = request.path
            ammort_get = mAP.ap_model()
            jsondata = json.loads(request.body.decode('utf-8'))
            action = jsondata.get('params').get('action')
            type = jsondata.get('params').get('type')
            if (action == "GET" and (
                    type == "AMMORT_SUMMARY" or type == "AMMORT_HEADER_DETAIL" or type == "AMMORT_DATE" or type == "AMMORT_CCBS_DETAIL")):
                ammort_get.action = action
                ammort_get.type = type
                ammort_get.filter = json.dumps(jsondata.get('params').get('filter'))
                ammort_get.classification = json.dumps({"Entity_Gid": int(decry_data(request.session['Entity_gid']))})
                ammort_get.create_by = int(decry_data(request.session['Emp_gid']))
                common.main_fun1(request.read(), path)
                output = ammort_get.get_ammort_details()
                jdata = output.to_json(orient='records')
                return JsonResponse(json.loads(jdata), safe=False)
        except Exception as e:
            return JsonResponse({"MESSAGE": "ERROR_OCCURED", "DATA": str(e)})


def get_tablevalue(request):
    utl.check_authorization(request)
    utl.check_pointaccess(request)
    if request.method == 'POST':
        try:
            dropdown = mAP.ap_model()
            path = request.path
            jsondata = json.loads(request.body.decode('utf-8'))
            dropdown.tablevalue = jsondata.get('data')
            dropdown.entity_gid = int(decry_data(request.session['Entity_gid']))
            common.main_fun1(request.read(), path)
            out = dropdown.tablevalue_get()
            jdata = out.to_json(orient='records')
            return JsonResponse(json.loads(jdata), safe=False)
        except Exception as e:
            return JsonResponse({"MESSAGE": "ERROR_OCCURED", "DATA": str(e)})


def get_subcat(request):
    utl.check_authorization(request)
    utl.check_pointaccess(request)
    if request.method == 'POST':
        try:
            path = request.path
            dropdown = mAP.ap_model()
            jsondata = json.loads(request.body.decode('utf-8'))
            dropdown.type = jsondata.get("Type")
            dropdown.sub_type = jsondata.get("Sub_type")
            dropdown.jsonData = json.dumps(jsondata.get("data").get("FILTER"))
            dropdown.json_classification = json.dumps({"Entity_Gid": int(decry_data(request.session['Entity_gid']))})
            common.main_fun1(request.read(), path)
            out = dropdown.get_CCBS_Master_Value()
            jdata = out.to_json(orient='records')
            return JsonResponse(json.loads(jdata), safe=False)
        except Exception as e:
            return JsonResponse({"MESSAGE": "ERROR_OCCURED", "DATA": str(e)})


def get_ccbs_data(request):
    utl.check_pointaccess(request)
    utl.check_authorization(request)
    if request.method == 'POST':
        try:
            path = request.path
            dropdown = mAP.ap_model()
            jsondata = json.loads(request.body.decode('utf-8'))
            action = jsondata.get('params').get('action')
            type = jsondata.get('params').get('type')
            sub_type = jsondata.get('params').get('sub_type')
            if action == "Get" and type == "Metadata" and sub_type == "BS_DATA":
                table_data = {
                    "Table_name": "ap_mst_tbs",
                    "Column_1": "tbs_code,tbs_gid,tbs_name",
                    "Column_2": "",
                    "Where_Common": "tbs",
                    "Where_Primary": "",
                    "Primary_Value": "",
                    "Order_by": "gid"
                }
                jsonData1 = table_data
            if action == "Get" and type == "Metadata" and sub_type == "CC_DATA":
                filter = jsondata.get('params').get('filter')
                bs_gid = filter.get('bs_gid');
                table_data = {
                    "Table_name": "ap_mst_tcc",
                    "Column_1": "tcc_gid,tcc_code,tcc_name",
                    "Column_2": "",
                    "Where_Common": "tcc",
                    "Where_Primary": "bsgid",
                    "Primary_Value": bs_gid,
                    "Order_by": "gid"
                }
                jsonData1 = table_data
            dropdown.action = action
            dropdown.tablevalue = jsonData1
            dropdown.entity_gid = int(decry_data(request.session['Entity_gid']))
            common.main_fun1(request.read(), path)
            out = dropdown.tablevalue_get()
            jdata = out.to_json(orient='records')
            return JsonResponse(json.loads(jdata), safe=False)
        except Exception as e:
            return JsonResponse({"MESSAGE": "ERROR_OCCURED", "DATA": str(e)})


def run_ammort(request):
    utl.check_pointaccess(request)
    utl.check_authorization(request)
    if request.method == 'POST':
        try:
            path = request.path
            jsondata = json.loads(request.body.decode('utf-8'))
            Amort_Month = jsondata.get("params").get("filter").get("Month")
            Amort_Year = jsondata.get("params").get("filter").get("Year")
            ammort_get = mAP.ap_model()
            ammort_get.action = jsondata.get("params").get("action")
            ammort_get.type = jsondata.get("params").get("type")
            ammort_get.filter = json.dumps(jsondata.get("params").get("filter"))
            ammort_get.classification = json.dumps({"Entity_Gid": int(decry_data(request.session['Entity_gid']))})
            ammort_get.create_by = int(decry_data(request.session['Emp_gid']))
            output = ammort_get.get_ammort_details()
            jdata = output.to_json(orient='records')
            result_data = json.loads(jdata)
            log_data = []
            success_cout = 0;
            # ammortdetail_amortheadergid
            output = ""
            for i in result_data:
                try:
                    ammort_set = mAP.ap_model()
                    action = 'AMMORT_RUN'
                    type = 'AMMORT_SCHEDULE'
                    ammort_set.action = action
                    ammort_set.type = type
                    ammort_set.filter = json.dumps(
                        {"DETAILS": {"AmortDetails_Gid": i.get('ammortdetail_amortheadergid'),
                                     "Month": Amort_Month, "Year": Amort_Year}})
                    ammort_set.classification = json.dumps(
                        {"Entity_Gid": int(decry_data(request.session['Entity_gid']))})
                    ammort_set.create_by = int(decry_data(request.session['Emp_gid']))
                    # common.main_fun1(request.read(), path)
                    output = ammort_set.set_ammort_details()
                except Exception as e:
                    log_data.append(i)
                    common.logger.error(e)
                    return JsonResponse(
                        {"MESSAGE": "ERROR_OCCURED",
                         "ERROR_MESSAGE": "ERROR ON AMORT DETAILS SET", "LOG_DATA": log_data,
                         "DATA": str(e)})
            return HttpResponse(output)
        except Exception as e:
            common.logger.error(e)
            return JsonResponse(
                {"MESSAGE": "ERROR_OCCURED", "ERROR_MESSAGE": "ERROR ON AMORT DETAILS GET", "DATA": str(e)})


def run_standardinstruction(request):
    utl.check_pointaccess(request)
    utl.check_authorization(request)
    if request.method == 'POST':
        try:
            path = request.path
            si_get = mStandardInstructions.StandardInstuctions()
            si_get.action = 'GET'
            si_get.type = 'SI_GID'
            si_get.filter = '{}'
            si_get.classification = json.dumps({"Entity_Gid": int(decry_data(request.session['Entity_gid']))})
            si_get.create_by = int(decry_data(request.session['Emp_gid']))
            output = si_get.get_SI()
            for index, row in output.iterrows():
                si_set = mStandardInstructions.StandardInstuctions()
                action = 'SI'
                type = 'SI_SCHEDULE'
                si_set.action = action
                si_set.type = type
                si_set.filter = '{"DETAILS": {"standardinstructiondetails_gid": [' + str(
                    row['standardinstructiondetails_gid']) + ']}}'
                si_set.classification = json.dumps({"Entity_Gid": int(decry_data(request.session['Entity_gid']))})
                si_set.create_by = int(decry_data(request.session['Emp_gid']))
                common.main_fun1(request.read(), path)
                output = si_set.set_SI()
            return HttpResponse(output)
        except Exception as e:
            return JsonResponse({"MESSAGE": "ERROR_OCCURED", "DATA": str(e)})


def run_branchexp(request):
    utl.check_pointaccess(request)
    utl.check_authorization(request)
    if request.method == 'POST':
        try:
            path = request.path
            br_get = mBranch.BranchExp_model()
            br_get.type = 'EXPENSE'
            br_get.sub_type = 'EXPENSE_GID'
            br_get.jsonData = '{}'
            br_get.json_classification = json.dumps({"Entity_Gid": int(decry_data(request.session['Entity_gid']))})
            br_get.create_by = int(decry_data(request.session['Emp_gid']))
            output = br_get.get_expensedetails()
            for index, row in output['DATA'].iterrows():
                log_data = []
                br_set = mBranch.BranchExp_model()
                action = 'COLUMN'
                type = 'ECF_UPDATE'
                br_set.action = action
                br_set.type = type
                br_set.jsonData = '{"DETAILS": {"branchexpensedetails_gid": [' + str(
                    row['branchexpensedetails_gid']) + ']}}'
                br_set.json_classification = json.dumps({"Entity_Gid": int(decry_data(request.session['Entity_gid']))})
                output = br_set.set_expensedetails()
                log_data = [{"BRANCH_EXP_RUN_OUTPUT_LOG": output}]
                common.logger.error(log_data)
            return HttpResponse(output)
        except Exception as e:
            log_data = [{"BRANCH_EXP_RUN_EXCEPTION_LOG": e}]
            common.logger.error(log_data)
            return JsonResponse({"MESSAGE": "ERROR_OCCURED", "DATA": str(e)})


def get_bank_data(request):
    utl.check_authorization(request)
    utl.check_pointaccess(request)
    if request.method == 'POST':
        try:
            path = request.path
            token = jwt.token(request)
            jsondata = json.loads(request.body.decode('utf-8'))
            if (jsondata.get('params').get('Groups')) == 'GET_EMP':
                entity = request.session['Entity_gid']
                drop_b = {
                    "Table_name": "gal_mst_temployee",
                    "Column_1": "employee_code,employee_name,employee_gid",
                    "Column_2": "",
                    "Where_Common": "employee",
                    "Where_Primary": "",
                    "Primary_Value": "",
                    "Order_by": "gid"
                }
                response = alltable(drop_b, entity, token)
                return HttpResponse(response)
            elif (jsondata.get('params').get('Groups')) == 'GET_PAYMODE':
                entity = request.session['Entity_gid']
                drop_b = {
                    "Table_name": "gal_mst_tpaymode",
                    "Column_1": "paymode_gid,paymode_code,Paymode_name",
                    "Column_2": "",
                    "Where_Common": "paymode",
                    "Where_Primary": "paymode_gid",
                    "Primary_Value": "",
                    "Order_by": "code"
                }
                response = alltable(drop_b, entity, token)
                return HttpResponse(response)
            elif (jsondata.get('params').get('Groups')) == 'GET_BANK':
                entity = request.session['Entity_gid']
                drop_b = {
                    "Table_name": "gal_mst_tbank",
                    "Column_1": "bank_gid,bank_code,bank_name",
                    "Column_2": "",
                    "Where_Common": "bank",
                    "Where_Primary": "bank_gid",
                    "Primary_Value": "",
                    "Order_by": "name"
                }
                response = alltable(drop_b, entity, token)
                return HttpResponse(response)
            elif (jsondata.get('params').get('Groups')) == 'GET_BANK_BRANCH':
                bank_gid = jsondata.get('params').get('Bank_Gid')
                entity = request.session['Entity_gid']
                drop_b = {
                    "Table_name": "gal_mst_tbankbranch",
                    "Column_1": "bankbranch_gid,bankbranch_name",
                    "Column_2": "",
                    "Where_Common": "bankbranch",
                    "Where_Primary": "bank_gid",
                    "Primary_Value": bank_gid,
                    "Order_by": "name"
                }
                response = alltable(drop_b, entity, token)
                return HttpResponse(response)
            elif (jsondata.get('params').get('Groups')) == 'EMP_BANK':
                act = jsondata.get('params').get('Action')
                grp = jsondata.get('params').get('Group')
                typ = jsondata.get('params').get('Type')
                sub = jsondata.get('params').get('Sub_Type')
                entity = int(decry_data(request.session['Entity_gid']))
                params = {"Action": act, "Group": grp, "Type": typ, "Sub_Type": sub,
                          "Employee_Gid": entity}
                headers = {"content-type": "application/json", "Authorization": "" + token + ""}
                classify = {
                    "CLASSIFICATION": {
                        "Entity_Gid": int(decry_data(request.session['Entity_gid']))
                    }}
                jsondata['params']['json']['Params'].update(classify)
                datas = json.dumps(jsondata.get('params').get('json'))
                resp = requests.post("" + ip + "/EMP_BANK_DATA", params=params, data=datas, headers=headers,
                                     verify=False)
                response = resp.content.decode("utf-8")
                return HttpResponse(response)
        except Exception as e:
            return JsonResponse({"MESSAGE": "ERROR_OCCURED", "DATA": str(e)})


def alltable(table_data, entity, token):
    drop_tables = {"data": table_data}
    action = ''
    entity_gid = entity
    params = {'Action': action, 'Entity_Gid': entity_gid}
    headers = {"content-type": "application/json", "Authorization": "" + token + ""}
    datas = json.dumps(drop_tables.get('data'))
    resp = requests.post("" + ip + "/All_Tables_Values_Get", params=params, data=datas, headers=headers,
                         verify=False)
    response_data = resp.content.decode("utf-8")
    return response_data


def ap_all_table_values_get(request):
    utl.check_pointaccess(request)
    utl.check_authorization(request)
    if request.method == 'POST':
        try:
            path = request.path
            jsondata = json.loads(request.body.decode('utf-8'))
            entity_gid = request.session['Entity_gid']
            params = {'Entity_Gid': entity_gid}
            token = jwt.token(request)
            headers = {"content-type": "application/json", "Authorization": "" + token + ""}
            datas = json.dumps(jsondata.get('filter'))
            resp = requests.post("" + ip + "/All_Tables_Values_Get", params=params, data=datas, headers=headers,
                                 verify=False)
            response_data = resp.content.decode("utf-8")
            return HttpResponse(response_data)
        except Exception as e:
            return JsonResponse({"MESSAGE": "ERROR_OCCURED", "DATA": str(e)})


def ap_set_dispatch(request):
    if request.method == 'POST':
        try:
            path = request.path
            dispatch = mAP.ap_model()
            jsondata = json.loads(request.body.decode('utf-8'))
            action = jsondata.get('action')
            type = jsondata.get('type')
            create_by = int(decry_data(request.session['Emp_gid']))
            if (action == "INSERT" and type == "DISPATCH"):
                dispatch.action = action
                dispatch.type = type
                jsondata['filter']['li_sent_by'] = create_by
                dispatch.filter = json.dumps(jsondata.get('filter'))
                dispatch.classification = json.dumps({"Entity_Gid": int(decry_data(request.session['Entity_gid']))})
                dispatch.create_by = create_by
                common.main_fun1(request.read(), path)
                output = dispatch.set_dispatch_details()
                return HttpResponse(output)
        except Exception as e:
            return JsonResponse({"MESSAGE": "ERROR_OCCURED", "DATA": str(e)})


def ap_get_dispatch(request):
    utl.check_pointaccess(request)
    utl.check_authorization(request)
    if request.method == 'POST':
        try:
            path = request.path
            ammort_get = mAP.ap_model()
            jsondata = json.loads(request.body.decode('utf-8'))
            action = jsondata.get('action')
            type = jsondata.get('type')
            if (action == "GET" and type == "GET_DISPATCH_DETAIL"):
                ammort_get.action = action
                ammort_get.type = type
                ammort_get.filter = json.dumps(jsondata.get('filter'))
                ammort_get.classification = json.dumps({"Entity_Gid": int(decry_data(request.session['Entity_gid']))})
                common.main_fun1(request.read(), path)
                output = ammort_get.get_ap_pod()
                jdata = output.to_json(orient='records')
                return JsonResponse(json.loads(jdata), safe=False)
        except Exception as e:
            return JsonResponse({"MESSAGE": "ERROR_OCCURED", "DATA": str(e)})


def get_supplier(request):
    utl.check_pointaccess(request)
    utl.check_authorization(request)
    if request.method == 'POST':
        try:
            path = request.path
            jsondata = json.loads(request.body.decode('utf-8'))
            invoice_get = mAP.ap_model()
            invoice_get.grp = jsondata.get('Params').get('Group')
            invoice_get.limit = jsondata.get('Params').get('Limit')
            invoice_get.type = jsondata.get('Params').get('Type')
            invoice_get.sub_type = jsondata.get('Params').get('Sub_Type')
            invoice_get.filter_json = json.dumps(jsondata.get('Params').get('FILTER'))
            entity_gid = int(decry_data(request.session['Entity_gid']))
            invoice_get.json_classification = json.dumps({"Entity_Gid": entity_gid})
            out_message = invoice_get.get_master_data()
            if out_message.get("MESSAGE") == 'FOUND':
                ld_dict = {"DATA": json.loads(out_message.get("DATA").to_json(orient='records')),
                           "MESSAGE": "FOUND"}
            elif out_message.get("MESSAGE") == 'NOT_FOUND':
                ld_dict = {"MESSAGE": out_message.get("MESSAGE")}
            else:
                ld_dict = {"MESSAGE": 'ERROR_OCCURED.' + out_message.get("MESSAGE")}
            return JsonResponse(ld_dict)

        except Exception as e:
            return JsonResponse({"MESSAGE": "ERROR_OCCURED", "DATA": str(e)})


def APInvoice_get_(request):
    utl.check_pointaccess(request)
    utl.check_authorization(request)
    if request.method == 'POST':
        try:
            path = request.path
            invoice_get = mAP.ap_model()
            jsondata = json.loads(request.body.decode('utf-8'))
            invoice_get.action = jsondata.get('params').get('action')
            invoice_get.ponumber = jsondata.get('params').get('ponumber')
            invoice_get.supplier_gid = jsondata.get('params').get('supplier_gid')
            invoice_get.inwarddetail_gid = jsondata.get('params').get('inwarddetail_gid')
            invoice_get.inwardheader_gid = jsondata.get('params').get('inwardheader_gid')
            invoice_get.status = jsondata.get('params').get('status')
            invoice_get.entity_gid = int(decry_data(request.session['Entity_gid']))
            invoice_get.state_gid = request.session['Entity_state_gid']
            invoice_get.limit = jsondata.get('params').get('limit')
            common.main_fun1(request.read(), path)
            out = invoice_get.Invoice_get_()
            jdata = out.to_json(orient='records')
            return JsonResponse(json.loads(jdata), safe=False)
        except Exception as e:
            return JsonResponse({"MESSAGE": "ERROR_OCCURED", "DATA": str(e)})


from io import BytesIO
from django.http import HttpResponse
from django.template.loader import get_template

from xhtml2pdf import pisa
from django.template import Context


def html_pdf(request):
    utl.check_pointaccess(request)
    utl.check_authorization(request)
    if request.method == 'POST':
        jsondata = json.loads(request.body.decode('utf-8'))
        Templatename = "ecf"
        file_css = open(BASE_DIR + '/Bigflow/AP/templates/tablestyle.text', "r")
        file_css = file_css.read()
        content = jsondata.get('params').get('html')
        content = file_css + content
        f = open(BASE_DIR + '/Bigflow/AP/templates/%s.html' % Templatename, 'w')
        f.write(content)
        f.close()
        data = {
            'MESSAGE': "SUCCESS",
        }
        return JsonResponse(data)


def down_pdf(request):
    utl.check_pointaccess(request)
    data = {
    }
    pdf = render_to_pdf(BASE_DIR + '/Bigflow/AP/templates/ecf.html', data)
    return HttpResponse(pdf, content_type="application/pdf")


def render_to_pdf(template_src, context_dict):
    template = get_template(template_src)
    html = template.render(context_dict)
    result = BytesIO()
    pdf = pisa.pisaDocument(BytesIO(html.encode("ISO-8859-1")), result)
    if not pdf.err:
        return HttpResponse(result.getvalue(), content_type='application/pdf')
    return None


def get_delmat(request):
    utl.check_pointaccess(request)
    utl.check_authorization(request)
    if request.method == 'POST':
        try:
            path = request.path
            object_data = mAP.ap_model()
            jsondata = json.loads(request.body.decode('utf-8'))
            action = jsondata.get('params').get('action')
            create_by = int(decry_data(request.session['Emp_gid']))
            Entity_gid = int(decry_data(request.session['Entity_gid']))
            type = jsondata.get('params').get('type')
            if (action == "limit" and type == "DELMAT") or (
                    action == "limit" and type == "DELMAT_EMPLOYEE_LIMIT" or type == "DELMAT_DETAIL" or type == "DELMAT_COMMODITY"):
                jsondata['params']['filter']['employee_gid'] = create_by
                object_data.action = action
                object_data.type = type
                object_data.filter = json.dumps(jsondata.get('params').get('filter'))
                object_data.classification = json.dumps({"Entity_Gid": Entity_gid})
                object_data.create_by = create_by
                common.main_fun1(request.read(), path)
                output = object_data.get_delmat_datas()
                jdata = output.to_json(orient='records')
                return JsonResponse(json.loads(jdata), safe=False)
        except Exception as e:
            return JsonResponse({"MESSAGE": "ERROR_OCCURED", "DATA": str(e)})


def get_APbankdetails(request):
    utl.check_pointaccess(request)
    utl.check_authorization(request)
    if request.method == 'POST':
        try:
            path = request.path
            invoice_set = mAP.ap_model()
            jsondata = json.loads(request.body.decode('utf-8'))
            invoice_set.action = jsondata.get('params').get('action')
            invoice_set.type = jsondata.get('params').get('type')
            filter = jsondata.get('params').get('filter')
            invoice_set.filter = json.dumps(filter)
            invoice_set.classification = json.dumps({"Entity_Gid": int(decry_data(request.session['Entity_gid']))})
            invoice_set.create_by = int(decry_data(request.session['Emp_gid']))
            common.main_fun1(request.read(), path)
            jdata = invoice_set.get_APbankdetails()
            jdata = jdata.to_json(orient='records')
            return JsonResponse(jdata, safe=False)
        except Exception as e:
            return JsonResponse({"MESSAGE": "ERROR_OCCURED", "DATA": str(e)})


def get_bank_details(request):
    utl.check_pointaccess(request)
    utl.check_authorization(request)
    if request.method == 'GET':
        obj_bank_detail = mAP.ap_model()
        obj_bank_detail.entity_gid = decry_data(request.session['Entity_gid'])
        df_bank_view = obj_bank_detail.get_bank_details()
        jdata = df_bank_view.to_json(orient='records')
        return JsonResponse(json.loads(jdata), safe=False)


def get_pmd_data(request):
    utl.check_pointaccess(request)
    utl.check_authorization(request)
    if request.method == 'POST':
        try:
            path = request.path
            object_data = mAP.ap_model()
            jsondata = json.loads(request.body.decode('utf-8'))
            action = jsondata.get('action')
            create_by = int(decry_data(request.session['Emp_gid']))
            Entity_gid = int(decry_data(request.session['Entity_gid']))
            type = jsondata.get('type')
            if (action == "GET" and (type == "PMD_SUMMARY" or type == "PMD_DETAILS" or type == "ACTIVE_PMD_SUMMARY")):
                object_data.action = action
                object_data.type = type
                object_data.filter = json.dumps(jsondata.get('filter'))
                object_data.classification = json.dumps({"Entity_Gid": Entity_gid, "create_by": create_by})
                object_data.create_by = create_by
                common.main_fun1(request.read(), path)
                output = object_data.get_pmd_details()
                jdata = output.to_json(orient='records')
                return JsonResponse(json.loads(jdata), safe=False)
        except Exception as e:
            return JsonResponse({"MESSAGE": "ERROR_OCCURED", "DATA": str(e)})


def advance_get(request):
    utl.check_pointaccess(request)
    utl.check_authorization(request)
    if request.method == 'POST':
        try:
            path = request.path
            object_data = mAP.ap_model()
            jsondata = json.loads(request.body.decode('utf-8'))
            action = jsondata.get('action')
            create_by = int(decry_data(request.session['Emp_gid']))
            Entity_gid = int(decry_data(request.session['Entity_gid']))
            type = jsondata.get('type')
            if (action == "ADVANCE" and type == "PPX"):
                object_data.action = action
                object_data.type = type
                object_data.filter = json.dumps(jsondata.get('filter'))
                object_data.classification = json.dumps({"Entity_Gid": Entity_gid, "create_by": create_by})
                object_data.create_by = create_by
                common.main_fun1(request.read(), path)
                output = object_data.get_advance_details()
                jdata = output.to_json(orient='records')
                return JsonResponse(json.loads(jdata), safe=False)
        except Exception as e:
            return JsonResponse({"MESSAGE": "ERROR_OCCURED", "DATA": str(e)})


def entry_update_get(request):
    utl.check_pointaccess(request)
    utl.check_authorization(request)
    if request.method == 'POST':
        try:
            path = request.path
            object_data = mAP.ap_model()
            jsondata = json.loads(request.body.decode('utf-8'))
            action = jsondata.get('action')
            create_by = int(decry_data(request.session['Emp_gid']))
            Entity_gid = int(decry_data(request.session['Entity_gid']))
            type = jsondata.get('type')
            if (action == "ENTRY"):
                object_data.action = action
                object_data.type = type
                object_data.filter = json.dumps(jsondata.get('filter'))
                # object_data.classification = json.dumps({"Entity_Gid": Entity_gid,"create_by":create_by})
                object_data.create_by = create_by
                common.main_fun1(request.read(), path)
                output = object_data.get_EntryUpdate()
                jdata = output.to_json(orient='records')
                return JsonResponse(json.loads(jdata), safe=False)
        except Exception as e:
            return JsonResponse({"MESSAGE": "ERROR_OCCURED", "DATA": str(e)})


def entry_update_set(request):
    utl.check_pointaccess(request)
    utl.check_authorization(request)
    if request.method == 'POST':
        try:
            path = request.path
            object_data = mAP.ap_model()
            jsondata = json.loads(request.body.decode('utf-8'))
            action = jsondata.get('action')
            create_by = int(decry_data(request.session['Emp_gid']))
            Entity_gid = int(decry_data(request.session['Entity_gid']))
            type = jsondata.get('type')
            if (action == "UPDATE"):
                object_data.action = action
                object_data.type = type
                object_data.filter = json.dumps(jsondata.get('filter'))
                object_data.classification = json.dumps({"Entity_Gid": Entity_gid, "create_by": create_by})
                object_data.create_by = create_by
                common.main_fun1(request.read(), path)
                output = object_data.set_EntryUpdate()
                # jdata = output.to_json(orient='records')
                # return JsonResponse(json.loads(output), safe=False)
                return HttpResponse(output)
        except Exception as e:
            return JsonResponse({"MESSAGE": "ERROR_OCCURED", "DATA": str(e)})


def set_pmd_data(request):
    utl.check_pointaccess(request)
    utl.check_authorization(request)
    if request.method == 'POST':
        try:
            path = request.path
            pmd_obj = mAP.ap_model()
            jsondata = json.loads(request.body.decode('utf-8'))
            action = jsondata.get('action')
            type = jsondata.get('type')
            create_by = int(decry_data(request.session['Emp_gid']))
            Entity_Gid = int(decry_data(request.session['Entity_gid']))
            if (action == "INSERT" and type == "PMD_SET"):
                pmd_obj.action = action
                pmd_obj.type = type
                pmd_obj.filter = json.dumps(jsondata.get('filter'))
                pmd_obj.classification = json.dumps({"Entity_Gid": Entity_Gid, "create_by": create_by})
                common.main_fun1(request.read(), path)
                output = pmd_obj.set_pmd_details()
                return HttpResponse(output)
        except Exception as e:
            return JsonResponse({"MESSAGE": "ERROR_OCCURED", "DATA": str(e)})


def set_file_details(request):
    utl.check_pointaccess(request)
    utl.check_authorization(request)
    if request.method == 'POST':
        try:
            path = request.path
            pmd_obj = mAP.ap_model()
            jsondata = json.loads(request.body.decode('utf-8'))
            action = jsondata.get('action')
            type = jsondata.get('type')
            create_by = int(decry_data(request.session['Emp_gid']))
            Entity_Gid = int(decry_data(request.session['Entity_gid']))
            if (action == "UPDATE" and type == "FILE_DETAIL_SET"):
                pmd_obj.action = action
                pmd_obj.type = type
                pmd_obj.filter = json.dumps(jsondata.get('filter'))
                pmd_obj.classification = json.dumps({"Entity_Gid": Entity_Gid, "create_by": create_by})
                pmd_obj.create_by = create_by
                common.main_fun1(request.read(), path)
                output = pmd_obj.set_file_details()
                return HttpResponse(output)
        except Exception as e:
            return JsonResponse({"MESSAGE": "ERROR_OCCURED", "DATA": str(e)})


def Session_Get_AP_Data(request):
    utl.check_pointaccess(request)
    utl.check_authorization(request)
    if request.method == 'POST':
        jsondata = json.loads(request.body.decode('utf-8'))
        action = jsondata.get('action')
        type = jsondata.get('type')
        session_keys = jsondata.get("filter")
        data = {}
        if action == "GET":
            for (k, v) in session_keys.items():
                data[k] = request.session[k]
        return JsonResponse(data, safe=False)


from multiprocessing.pool import ThreadPool as Pool


def gl_day_entry_genrate_with_Thread(action, type, filter, classification):
    branch_gid = filter.get("branch_gid")
    create_by = classification.get("create_by")
    pmd_obj = mAP.ap_model()
    pmd_obj.action = action
    pmd_obj.type = type
    pmd_obj.filter = json.dumps(filter)
    pmd_obj.classification = json.dumps(classification)
    pmd_obj.employee_gid = create_by
    output = pmd_obj.set_day_entry_details()
    if (output[0] != "SUCCESS"):
        log_data = [{"DAY_ENTRY_SET_FAILED_DATA": {"branch_Gid": branch_gid}}]
        common.logger.error(log_data)


def gl_day_entry_generate(request):
    utl.check_pointaccess(request)
    utl.check_authorization(request)
    if request.method == 'POST':
        try:
            path = request.path
            pmd_obj = mAP.ap_model()
            jsondata = json.loads(request.body.decode('utf-8'))
            action = jsondata.get('action')
            type = jsondata.get('type')
            create_by = int(decry_data(request.session['Emp_gid']))
            Entity_Gid = int(decry_data(request.session['Entity_gid']))
            common.main_fun1(request.read(), path)
            if (action == "INSERT" and type == "INITIAL_SET"):
                token = jwt.token(request)
                branch_querys = {"Table_name": "gal_mst_tbranch", "Column_1": "branch_gid,branch_code,branch_name",
                                 "Column_2": "", "Where_Common": "branch", "Where_Primary": "",
                                 "Primary_Value": "", "Order_by": "gid"}
                data = alltable(branch_querys, Entity_Gid, token)
                jsondata = json.loads(data)
                Branch_details = jsondata.get("DATA")
                pool_size = 10
                pool = Pool(pool_size)
                for branch in Branch_details:
                    log_data = []
                    branch_gid = branch.get("branch_gid")
                    filter = {"branch_Gid": branch_gid}
                    classification = {"Entity_Gid": Entity_Gid, "create_by": create_by}
                    # x = threading.Thread(target=gl_day_entry_genrate_with_Thread(action,type,filter,classification), args=(4,))
                    # pass
                    # x.start()
                    pool.apply_async(gl_day_entry_genrate_with_Thread, (action, type, filter, classification,))
                pool.close()
                pool.join()
                # return HttpResponse(output)
        except Exception as e:
            return JsonResponse({"MESSAGE": "ERROR_OCCURED", "DATA": str(e)})