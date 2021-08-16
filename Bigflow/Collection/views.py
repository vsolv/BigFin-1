from django.core.files.storage import default_storage
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import HttpResponse
from Bigflow.Collection.Model import mCollection
from Bigflow.Transaction.Model import mFET, mSales
from django.http import JsonResponse
import json
import io
from dateutil.relativedelta import relativedelta
import pandas as pd
import Bigflow.Core.models as common
from django.conf import settings
from datetime import datetime
from django.core.files.base import ContentFile
import requests
import PyPDF2
from Bigflow.menuClass import utility as utl
import Bigflow.Core.jwt_file as jwt
ip = common.localip()
# token = common.token()


# Create your views here.
def Collectionindex(request):
    utl.check_authorization(request)
    return render(request, "Collectionindex.html")


def CollectionSummary(request):
    utl.check_authorization(request)
    return render(request, "Collection_daysummary.html")


def CollectionHOSummary(request):
    utl.check_authorization(request)
    return render(request, "Collection_HOSummary.html")


def CollectionReceiptSummary(request):
    utl.check_authorization(request)
    return render(request, "Collection_Receipt_Summary.html")



def ReceiptSummary(request):
    utl.check_authorization(request)
    if request.method == 'POST':

        jsondata = json.loads(request.body.decode('utf-8'))
        obj = mSales.Sales_Model()
        obj.grp = jsondata.get('Group')
        obj.typ = jsondata.get('Type')
        obj.sbtyp = jsondata.get('Sub_Type')
        params = {'Group': "" + obj.grp + "", 'Type': "" + obj.typ + "", 'Sub_Type': "" + obj.sbtyp + "","entity":request.session['Entity_gid']}
        token = jwt.token(request)
        headers = {"content-type": "application/json", "Authorization": "" + token + ""}
        datas = json.dumps(jsondata.get('data'))
        resp = requests.post("" + ip + "/Receipt_AR", params=params, data=datas, headers=headers, verify=False)
        response = resp.content.decode("utf-8")
        return HttpResponse(response)


def CancelReceipt(request):
    utl.check_authorization(request)
    if request.method == 'POST':
        jsondata = json.loads(request.body.decode('utf-8'))
        obj = mSales.Sales_Model()
        obj.action = jsondata.get('Action')
        obj.type = jsondata.get('Type')
        obj.sub_type = jsondata.get('Sub_Type')
        obj.group = jsondata.get('Group')
        obj.employee_id = jsondata.get('Employee_Gid')
        token = jwt.token(request)
        params = {'Action': "" + obj.action + "", 'Type': "" + obj.type + "", 'Sub_Type': "" + obj.sub_type + "",
                  'Group': "" + obj.group + "", 'Employee_Gid': "" + obj.employee_id + ""}
        headers = {"content-type": "application/json", "Authorization": "" + token + ""}
        datas = json.dumps(jsondata.get('data'))
        resp = requests.post("" + ip + "/Receipt_Process_API", params=params, data=datas, headers=headers, verify=False)
        response = resp.content.decode("utf-8")
        return HttpResponse(response)


class Collection_API(APIView):
    def post(self, request):
        try:
            if self.request.query_params.get("Group") == "GET_CLTN_INV_MAP":
                obj_cltn = mCollection.Collection_model()
                obj_cltn.action = self.request.query_params.get("Action")
                obj_cltn.type = self.request.query_params.get("Type")
                obj_cltn.collectionheader_gid = self.request.query_params.get("Collection_Gid")
                obj_cltn.name = ''
                obj_cltn.date = ''
                obj_cltn.jsonData = json.loads(request.body.decode('utf-8')).get('params').get('DATA')
                obj_cltn.jsondata = json.loads(request.body.decode('utf-8')).get('params').get('CLASSIFICATION')
                out_message = obj_cltn.get_collection_inv_map()
                if out_message.empty == False:
                    json_data = json.loads(out_message.to_json(orient='records'))
                    return Response({"MESSAGE": "FOUND", "DATA": json_data})
                else:
                    return Response({"MESSAGE": "NOT_FOUND"})

        except Exception as e:
            return Response({"MESSAGE": "ERROR", "DATA": str(e)})

    def get(self, request):
        try:
            if self.request.query_params.get("Group") == "GET_OUTSTAND":
                obj_outstand = mFET.FET_model()
                obj_outstand.action = self.request.query_params.get("Action")
                obj_outstand.from_date = self.request.query_params.get("From_date")
                obj_outstand.to_date = self.request.query_params.get("To_date")
                obj_outstand.customer_gid = self.request.query_params.get("Cust_gid")
                obj_outstand.employee_gid = self.request.query_params.get("Emp_gid")
                obj_outstand.limit = self.request.query_params.get("limit")
                obj_outstand.entity_gid = self.request.query_params.get("Entity_gid")
                out_message = obj_outstand.get_outstanding_fet()
                if out_message.empty == False:
                    json_data = json.loads(out_message.to_json(orient='records'))
                    return Response({"MESSAGE": "FOUND", "DATA": json_data})
                else:
                    return Response({"MESSAGE": "NOT_FOUND"})

        except Exception as e:
            return Response({"MESSAGE": "ERROR", "DATA": str(e)})


def Collectionbankrecon(request):
    utl.check_authorization(request)
    return render(request, "Collection_bankrecon.html")


def Collectionreceipt(request):
    utl.check_authorization(request)
    return render(request, "Collection_receipt.html")

def CreateDiscountIndex(request):
    utl.check_authorization(request)
    return render(request,"Create_Discount.html")

def Collectioncreate(request):
    utl.check_authorization(request)
    return render(request, "CollectionCreate.html")

def excelgen(request):
    utl.check_authorization(request)
    if request.method == 'POST' and request.FILES['file']:
        try:
            token = jwt.token(request)
            current_month = datetime.now().strftime('%m')
            current_day = datetime.now().strftime('%d')
            current_year_full = datetime.now().strftime('%Y')
            save_path = str(settings.MEDIA_ROOT)+ '/Bank_Recon/'+str(current_year_full)+'/'+str(current_month)+'/'+str(current_day)+'/'+str(request.POST['name'])
            path = default_storage.save(str(save_path), ContentFile('new content'))
            path = default_storage.save(str(save_path), request.FILES['file'])
            obj = mSales.Sales_Model()
            obj.grp = request.POST['Group']
            obj.actn = request.POST['Action']
            obj.typ = request.POST['Type']
            obj.empgid = request.POST['Employee_Gid']
            obj.gid = request.POST['Gid']
            obj.filepath = path
            obj.name = request.POST['name']
            f = request.FILES['file']
            df = pd.read_excel(f, skiprows=[0, 1, 2, 3, 4, 5], sheetname='OpTransactionHistoryUX3')
            no = df['No.']
            id = df['Transaction ID']
            date = df['Value Date']
            txndate = df['Txn Posted Date']
            des = df['Description']
            crdr = df['Cr/Dr']
            chenum = df['ChequeNo.']
            amnt = df['Transaction Amount(INR)']
            availbal = df['Available Balance(INR)']
            df = pd.DataFrame(
                {'SNo': no, 'Tran_Id': id, 'Value_Date': date, 'Posted_Date': txndate, 'Cheque_No': chenum,
                 'Description': des, 'CR_DR': crdr, 'Transaction_Amount': amnt, 'Status': 'RECEIVED',
                 'Balance_Amount': availbal})
            # dd = df.set_index('SNo').T.to_dict('list')
            ff = df.to_dict('records')
            sd = {"params": {"DATA": {"Bank_Gid": "" + obj.gid + "", "BANK_STMT": ff}, "FILE": {
                "FILE": {"File_Gid": "0", "File_Name": obj.name , "File_Path": obj.filepath}},
                             "CLASSIFICATION": {"entity_gid": request.session['Entity_gid'], "client_gid": []}}}
            datas = json.dumps(sd)
            resp = requests.post(
                "" + ip + "/BankUpload_API?Group=" + obj.grp + "&Action=" + obj.actn + "&Type=" + obj.typ + "&Employee_Gid=" + obj.empgid + "",
                data=datas,
                headers = {"content-type": "application/json", "Authorization": "" + token + ""}, verify=False)
            response = resp.content.decode("utf-8")
            return HttpResponse(response)
        except Exception as e:
            return JsonResponse(e, safe=False)



def getOutStanding(request):
    utl.check_authorization(request)
    if request.method == 'POST':
        token = jwt.token(request)
        jsondata = json.loads(request.body.decode('utf-8'))
        params = {'Type': 'OUTSTANDING_AR', 'Sub_Type': 'INV_MAPPING_RECEIPT'}
        datas = {'parms': {'filter': {'Customer_Group_Gid': jsondata.get('cust_group_gid')}, 'classification': {'Entity_Gid': request.session['Entity_gid']}}}
        headers = {"content-type": "application/json", "Authorization": "" + token + ""}
        resp = requests.post("" + ip + "/Outstanding_AR",
                             params=params, data=json.dumps(datas), headers=headers,
                             verify=False)
        response = resp.content.decode("utf-8")
        return HttpResponse(response)


def setDiscountDetails(request):
    utl.check_authorization(request)
    if request.method == "POST":
        jsondata = json.loads(request.body.decode('utf-8'))
        if jsondata.get("employeeid")!='':
            params = {'Action': 'UPDATE', 'Type': 'RECEIPT_MAKE', 'Sub_Type': 'EMPLOYEE_RECEIPT',
                      'Group': 'RECEIPT_MAKE_DISCOUNT',
                      'Employee_Gid': request.session['Emp_gid']}
            json_header = {"Receipt_From": "EMPLOYEE",
                           "Receipt_Date": datetime.today().strftime("%Y-%m-%d"),
                           "Receipt_VoucherType": "R",
                           "Receipt_Type": "EMPLOYEE_RECEIPT",
                           "Receipt_REFName": "EMPLOYEE_RECEIPT",
                           "Receipt_Amount": jsondata.get('discount_amount'),
                           "Receipt_Remarks": jsondata.get("discount_remark"),
                           "Employee_Gid": jsondata.get("employeeid")
                           }
        else:
            params = {'Action': 'UPDATE', 'Type': 'RECEIPT_MAKE', 'Sub_Type': 'DISCOUNT',
                      'Group': 'RECEIPT_MAKE_DISCOUNT',
                      'Employee_Gid': request.session['Emp_gid']}
            json_header = {"Receipt_From": "CUSTOMER",
                           "Receipt_Date": datetime.today().strftime("%Y-%m-%d"),
                           "Receipt_VoucherType": "C",
                           "Receipt_Type": "CREDIT_NOTE",
                           "Receipt_REFName": jsondata.get('Discount_Remark'),
                           "Receipt_Amount": jsondata.get('discount_amount'),
                           "Receipt_Remarks": jsondata.get("discount_remark")}



        json_details = jsondata.get('data')
        token = jwt.token(request)
        datas = {'params': {'DATA': {'HEADER': json_header, 'DETAILS': json_details},
                           'CLASSIFICATION': {'Entity_Gid': request.session['Entity_gid'], 'Client_Gid': []}}}
        headers = {"content-type": "application/json", "Authorization": "" + token + ""}
        resp = requests.post("" + ip + "/Receipt_Process_API",
                             params=params, data=json.dumps(datas), headers=headers,
                             verify=False)
        response = resp.content.decode("utf-8")
        return HttpResponse(response)


def pdfupload(request):
    utl.check_authorization(request)
    utl.check_pointaccess(request)
    if request.method == 'POST':
        try:
            jsondata = json.loads(request.body.decode("utf-8"))
            filename = jsondata.get('filename')
            gid = json.dumps(jsondata.get('gid'))
            file_url = "http://174.138.120.196:8089/pentaho/content/reporting/execute/steel-wheels/dashboards/newpages.pdf?solution=steel-wheels&path=/dashboards&name=multione.prpt&userid=joe&password=password&po_gid="+gid+""
            r = requests.get(file_url, stream=True)
            current_month = datetime.now().strftime('%m')
            current_day = datetime.now().strftime('%d')
            current_year_full = datetime.now().strftime('%Y')
            save_path = str(settings.MEDIA_ROOT) + '/Invoice/' + str(current_year_full) + '/' + str(
                current_month) + '/' + str(
                current_day) + '/' + str(filename+'.pdf')
            path = default_storage.save(str(save_path), ContentFile('new content'))
            with open(str(save_path), "wb") as pdf:
                for chunk in r.iter_content(chunk_size=1024):
                    # writing one chunk at a time to pdf file
                    if chunk:
                        pdf.write(chunk)
            return HttpResponse("data:{MESSAGE:SUCCESS}")
        except Exception as e:
            return JsonResponse(e, safe=False)

def downloadpdf(request):
    utl.check_authorization(request)
    utl.check_pointaccess(request)
    if request.method == 'POST':
        try:
            jsondata = json.loads(request.body.decode("utf-8"))
            filename = jsondata.get('filename')
            current_month = datetime.now().strftime('%m')
            current_day = datetime.now().strftime('%d')
            current_year_full = datetime.now().strftime('%Y')
            save_path = str(settings.MEDIA_ROOT) + '/Invoice/' + str(current_year_full) + '/' + str(
                current_month) + '/' + str(
                current_day) + '/' + str(filename + '.pdf')
            pdf1File = open(save_path, 'rb')
            pdf1Reader = PyPDF2.PdfFileReader(pdf1File)
            pdfWriter = PyPDF2.PdfFileWriter()

            for pageNum in range(pdf1Reader.numPages):
                pageObj = pdf1Reader.getPage(pageNum)
                pdfWriter.addPage(pageObj)

            pdfOutputFile = open(filename+'.pdf', 'wb')
            pdfWriter.write(pdfOutputFile)
            pdfOutputFile.close()
            pdf1File.close()
            return HttpResponse({"MESSAGE:SUCCESS"})
        except Exception as e:
            return JsonResponse(e, safe=False)

def get_cutoff(request):
    utl.check_authorization(request)
    utl.check_pointaccess(request)

    if request.method == 'POST':
            objdata = mCollection.Collection_model()
            jsondata = json.loads(request.body.decode('utf-8'))
            objdata.group = jsondata.get('Group')
            objdata.action = jsondata.get('Action')
            objdata.type = jsondata.get('Type')
            objdata.collectionheader_gid =0
            objdata.name = ''
            objdata.date = ''
            objdata.jsonData = json.dumps({
                "Due_Day": jsondata.get('data').get('Due_Day'),
                'Cutoff_Date': jsondata.get('data').get('Cutoff_Date'),
                "From_Date": jsondata.get('data').get('From_Date'),
                "To_Date": jsondata.get('data').get('To_Date'),
                 })
            objdata.json_classification = objdata.json_classification = json.dumps({'Entity_Gid': [1]})
            obj_cancel_data = objdata.get_cutoff()
            jdata = obj_cancel_data.to_json(orient='records')
            return JsonResponse(json.loads(jdata), safe=False)
