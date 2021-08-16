from django.shortcuts import render
import pandas as pd
from Bigflow.Core.models import decrpt as decry_data
from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import HttpResponse
from Bigflow.Collection.Model import mCollection
from Bigflow.Transaction.Model import mFET, mSales
from Bigflow.API import view_sales
from Bigflow.menuClass import utility as utl
# from Bigflow.Sales.models import memp
from django.http import JsonResponse
import json
import numpy as np
import requests
import base64
import datetime
from dateutil.relativedelta import relativedelta
import Bigflow.Core.models as common
import Bigflow.Core.jwt_file as jwt

ip = common.localip()
# token = common.token()


def saleindex(request):
    utl.check_authorization(request)
    utl.check_pointaccess(request)
    return render(request, "saleindex.html")

def Generate_label_popup(request):
    #utl.check_authorization(request)
    utl.check_pointaccess(request)
    return render(request,"Generate_Label_popup.html")


def Dispatch_POD_Updation(request):
    utl.check_authorization(request)
    utl.check_pointaccess(request)
    return render(request, "Dispatch_POD_Updation.html")


def Dispatch_Popup(request):
    # utl.check_authorization(request)
    utl.check_pointaccess(request)
    return render(request, "Dispatch_popup.html")

def Excepted_Courier_Bill(request):
    # utl.check_authorization(request)
    utl.check_pointaccess(request)
    return render(request,"Excepted_Courier_Bill.html")

def Invoice_print_Summary(request):
    utl.check_authorization(request)
    utl.check_pointaccess(request)
    return render(request, "Invoice_Print_Summary.html")


def InvoicePopup(request):
    utl.check_authorization(request)
    utl.check_pointaccess(request)
    return render(request, "Invoice_Popup.html")


def SalesRegisterInvoice(request):
    utl.check_authorization(request)
    utl.check_pointaccess(request)
    return render(request, "SalesRegisterInvoice.html")


def DealerPriceMakerSummary(request):
    utl.check_authorization(request)
    utl.check_pointaccess(request)
    return render(request, "DealerPriceMakerSummary.html")


def Dealer_Add_Popup(request):
    # utl.check_authorization(request)
    utl.check_pointaccess(request)
    return render(request, "Dealer_Add_popup.html")


def DealerPriceApproverSummary(request):
    utl.check_authorization(request)
    utl.check_pointaccess(request)
    return render(request, "DealerPriceApproverSummary.html")


def Dispatchlabelgenerate(request):
    utl.check_authorization(request)
    utl.check_pointaccess(request)
    return render(request, "DispatchLabelGenerate.html")


def CustomerMappingSummary(request):
    utl.check_authorization(request)
    utl.check_pointaccess(request)
    return render(request, "CustomerMappingSummary.html")


def Customer_popup(request):
    # utl.check_authorization(request)
    utl.check_pointaccess(request)
    return render(request, "Customer_popup.html")


def CustomerApproverSummary(request):
    utl.check_authorization(request)
    utl.check_pointaccess(request)
    return render(request, "CustomerApproverSummary.html")


def invcsmry(request):
    utl.check_authorization(request)
    utl.check_pointaccess(request)
    return render(request, "Invoice_Summary.html")


def Invoice_view_popup(request):
    # utl.check_authorization(request)
    utl.check_pointaccess(request)
    return render(request, "Invoice_View_Popup.html")


def Bulkpopup(request):
    # utl.check_authorization(request)
    utl.check_pointaccess(request)
    return render(request, "Invoice_popup1.html")


def Invoice_Cancel_Summary(request):
    utl.check_authorization(request)
    utl.check_pointaccess(request)
    return render(request, "Invoice_Cancel_Summary.html")

# def Product_Type_Popup(request):
#     return render(request,"Product_Type_popup.html")

# def Product_Add_Popup(request):
#     return render(request,"Product_Add_popup.html")

# def Product_Add_Popupcarton(request):
#     return render(request, "Product_Add_Popupcarton.html")
#
# def Product_Type_Popup(request):
#     return render(request,"Product_Type_popup.html")

def weightupdatepop(request):
    # utl.check_authorization(request)
    utl.check_pointaccess(request)
    return render(request, "weightupdatepopup.html")

def branchdetails(request):
    utl.check_authorization(request)
    utl.check_pointaccess(request)
    return render(request,"Classification_view.html")

def ManualLabelGenerate(request):
    utl.check_authorization(request)
    utl.check_pointaccess(request)
    return render(request,"ManualLabelGenerate.html")


def Courier_Explorer(request):
    # utl.check_authorization(request)
    utl.check_pointaccess(request)
    return render(request,"Courier_Explorer.html")

def excel(request):
    utl.check_authorization(request)
    utl.check_pointaccess(request)
    if request.method == 'POST' and request.FILES['file']:
        try:
            dd = base64.b64encode(request.FILES['file'].read())
            ress = dd.decode("utf-8")
            obj = mSales.Sales_Model()
            obj.grp = request.POST['Group']
            obj.actn = request.POST['Action']
            obj.typ = request.POST['Type']
            obj.sub_typ = request.POST['Sub_Type']
            obj.empgid = request.POST['Create_by']
            obj.name = request.POST['name']
            # obj.employee_gid = json.dumps(request.session['Emp_gid'])
            obj.entity_gid = json.dumps(request.session['Entity_gid'])
            f = request.FILES['file']
            df = pd.read_excel(f)
            batchno = df['BATCHNO']
            manual_weight=df['WGT']
            #delivery_date = pd.to_datetime(df['DLVD_DATE'])

            #print(delivery_date)
            #DAT = df['DLVD_DATE']
            df['DLVD_DATE'] = df['DLVD_DATE'].astype(str)
            #df['new_date_column'] = df['DLVD_DATE1'].dt.date
            # print (delivery_date)
            # pd.to_datetime(df[0]).apply(lambda x:x.strftime('%d/%m/%Y'))
            # x=str(datetime.datetime(delivery_date))
            # y=x.strftime("%d-%m-%Y")
            # date=pd.to_datetime(delivery_date)
            # newf=json.dumps(date.dt.date);
            # strr=delivery_date.strftime("%d-%m-%Y")
            # if len(batchno)==0:
            # return HttpResponse({"MESSAGE":"NOT FOUND"})
            awbno = df['AWB_NO']
            status = df['STATUS']
            df1 = pd.DataFrame({'System_AWB_No': batchno,
                               'POD_AWB_NO': awbno,
                               'Delivery_Status': status,
                               'Delivery_Date':df['DLVD_DATE'],
                               'Manual_Weight':manual_weight})
            ff = df1.to_dict('records')
            # gf=pd.to_datetime(ff);
            # print(gf)
            dataa = {
                "Params": {
                    "HEADER": ff,
                    "File": [{
                        "File_Name": obj.name,
                        "File_Extension": request.POST['file_extension'],
                        "File_Base64data": ress
                    }],
                    "DETAILS": {},
                    "CLASSIFICATION": {"Entity_Gid": obj.entity_gid}
                }
            }

            dta = json.dumps(dataa)
            params = {'Group': "" + obj.grp + "", 'Action': "" + obj.actn + "", 'Type': "" + obj.typ + "",
                      'Sub_Type': "" + obj.sub_typ + "", 'Create_by': "" + obj.empgid + ""}
            token = jwt.token(request)
            headers = {"content-type": "application/json", "Authorization": "" + token + ""}
            resp = requests.post("" + ip + "/DispatchProcess_Set", params=params, data=dta, headers=headers,
                                 verify=False)

            response = resp.content.decode("utf-8")
            return HttpResponse(response)
        except Exception as e:
            return HttpResponse(e)


def excelmonth(request):
    utl.check_authorization(request)
    utl.check_pointaccess(request)
    if request.method == 'POST' and request.FILES['file']:
        try:
            encode64 = base64.b64encode(request.FILES['file'].read())  # converting to files into base64encode
            decode_data = encode64.decode("utf-8")  # now file in bytes ,, while removing bytes is decode now
            f = request.FILES['file']  # reading files
            re_excl = pd.read_excel(f)  # reading excel
            pod_awb_no = re_excl['AWBNO']  # fetching excel column values of AWBNO
            amount = re_excl['AMOUNT'].astype(np.float)
            # float1=float(amount)# fetching excel column values of AMOUNT
            dataframe = pd.DataFrame({'Dispatch_podawbno': pod_awb_no,
                                      'Dispatch_podamt': amount})  # converting into dataframe
            record = dataframe.to_dict(
                'records')  # https://stackoverflow.com/questions/26716616/convert-a-pandas-dataframe-to-a-dictionary
            # visit and learn it....
            # entity id taken from session
            dataa = {
                "Params": {
                    "HEADER": record,
                    "File": [{
                        "File_Name": (request.POST['name']),
                        "File_Extension": (request.POST['file_extension']),
                        "File_Base64data": (decode_data)
                    }],
                    "DETAILS": {},
                    "CLASSIFICATION": {"Entity_Gid": [json.dumps(request.session['Entity_gid'])]}
                }

            }
            dta = json.dumps(dataa)
            params = {'Group': "" + request.POST['Group'] + "", 'Action': "" + request.POST['Action'] + "",
                      'Type': "" + request.POST['Type'] + "", 'Sub_Type': "" + request.POST['Sub_Type'] + "",
                      'Create_by': "" + request.POST['Create_by'] + ""}
            token = jwt.token(request)
            headers = {"content-type": "application/json", "Authorization": "" + token + ""}
            resp = requests.post("" + ip + "/DispatchProcess_Set", params=params, data=dta, headers=headers,
                                 verify=False)
            response = resp.content.decode("utf-8")
            return HttpResponse(response)

        except Exception as e:
            return HttpResponse(e)




def salesget(request):
    utl.check_authorization(request)
    utl.check_pointaccess(request)
    if request.method == 'POST':
        jsondata = json.loads(request.body.decode('utf-8'))
        if (jsondata.get('Group')) == 'SO_Register':
            obj = view_sales.SalesOrder_Register()
            obj.grp = jsondata.get('Group')
            obj.actn = jsondata.get('Action')
            obj.dte = jsondata.get('date')
            obj.cusgid = json.dumps(jsondata.get('cust_gid'))
            obj.empgid = request.session['Emp_gid']
            entity = request.session['Entity_gid']
            obj.lmt = json.dumps(jsondata.get('limit'))
            params = {'Group': "" + obj.grp + "", 'Action': "" + obj.actn + "", 'date': "" + obj.dte + "",
                      'cust_gid': "" + obj.cusgid + "", 'Emp_Gid': "" + obj.empgid + "", 'limit': "" + obj.lmt + "","entity":entity}
            token = jwt.token(request)
            headers = {"content-type": "application/json", "Authorization": "" + token + ""}
            datas = json.dumps(jsondata.get('data'))
            resp = requests.post("" + ip + "/SalesOrder_APIGet", params=params, data=datas, headers=headers,
                                 verify=False)
            response = resp.content.decode("utf-8")
            return HttpResponse(response)
        elif (jsondata.get('Group')) == 'SO_Invoice_Register':
            obj = view_sales.SalesOrder_Register()
            obj.grp = jsondata.get('Group')
            obj.actn = jsondata.get('Action')
            obj.dte = jsondata.get('date')
            obj.cusgid = json.dumps(jsondata.get('cust_gid'))
            obj.empgid = request.session['Emp_gid']
            obj.lmt = json.dumps(jsondata.get('limit'))
            entity = request.session['Entity_gid']
            params = {'Group': "" + obj.grp + "", 'Action': "" + obj.actn + "", 'date': "" + obj.dte + "",
                      'cust_gid': "" + obj.cusgid + "", 'Emp_Gid': "" + obj.empgid + "", 'limit': "" + obj.lmt + "","entity":entity }
            token = jwt.token(request)
            headers = {"content-type": "application/json", "Authorization": "" + token + ""}
            datas = json.dumps(jsondata.get('data'))
            resp = requests.post("" + ip + "/SalesOrder_APIGet", params=params, data=datas, headers=headers,
                                 verify=False)
            response = resp.content.decode("utf-8")
            return HttpResponse(response)


def prod_get(request):
    utl.check_authorization(request)
    utl.check_pointaccess(request)
    if request.method == 'GET':
        obj = view_sales.SalesOrder_Register()
        obj.prodname = request.GET['Product_Name']
        obj.lmt = request.GET['Limit']
        obj.entity_gid = json.dumps(request.session['Entity_gid'])
        token = jwt.token(request)
        resp = requests.get(
            "" + ip + "/Product_Sales?Limit=" + obj.lmt + "&Product_Name=" + obj.prodname + "&Entity_gid=" + obj.entity_gid + "",
            headers={"content-type": "application/json",
                     "Authorization": "" + token + ""
                     }, verify=False)
        response = resp.content.decode("utf-8")
        return HttpResponse(response)


def compaiget(request):
    utl.check_authorization(request)
    utl.check_pointaccess(request)
    if request.method == 'POST':
        jsondata = json.loads(request.body.decode('utf-8'))
        if (jsondata.get('Group')) == 'CAMPAIGN_GET':
            obj = view_sales.SalesOrder_Register()
            obj.grp = jsondata.get('Group')
            obj.typ = jsondata.get('Type')
            obj.sbtyp = jsondata.get('SubType')
            entity = request.session['Entity_gid']
            params = {'Group': "" + obj.grp + "", 'Type': "" + obj.typ + "", 'Subtype': "" + obj.sbtyp + "","entity":entity}
            token = jwt.token(request)
            headers = {"content-type": "application/json", "Authorization": "" + token + ""}

            datas = json.dumps(jsondata.get('data'))
            resp = requests.post("" + ip + "/Campaign_API_Get", params=params, data=datas, headers=headers,
                                 verify=False)
            response = resp.content.decode("utf-8")
            return HttpResponse(response)


def prcsmry(request):
    utl.check_authorization(request)
    utl.check_pointaccess(request)
    if request.method == 'POST':
        entity = request.session['Entity_gid']
        jsondata = json.loads(request.body.decode('utf-8'))
        if (jsondata.get('Group')) == 'SUMMARY':
            obj = view_sales.SalesOrder_Register()
            obj.grp = jsondata.get('Group')
            obj.typ = jsondata.get('Type')
            obj.sbtyp = jsondata.get('Sub_Type')
            obj.empgid = request.session['Emp_gid']
            entity=request.session['Entity_gid']
            obj.lmt = json.dumps(jsondata.get('Limit'))
            params = {'Group': "" + obj.grp + "", 'Type': "" + obj.typ + "", 'Sub_Type': "" + obj.sbtyp + "",
                      'Employee_Gid': "" + obj.empgid + "", 'Limit': "" + obj.lmt + "","entity":entity}
            token = jwt.token(request)
            headers = {"content-type": "application/json", "Authorization": "" + token + ""}
            datas = json.dumps(jsondata.get('data'))
            resp = requests.post("" + ip + "/Dealer_Price_API", params=params, data=datas, headers=headers,
                                 verify=False)
            response = resp.content.decode("utf-8")
            return HttpResponse(response)
        elif (jsondata.get('Group')) == 'MAKER':
            obj = view_sales.SalesOrder_Register()
            obj.grp = jsondata.get('Group')
            obj.typ = jsondata.get('Type')
            obj.actn = jsondata.get('Action')
            entity = request.session['Entity_gid']
            obj.empgid = request.session['Emp_gid']
            params = {'Group': "" + obj.grp + "", 'Type': "" + obj.typ + "", 'Action': "" + obj.actn + "",
                      'Employee_Gid': "" + obj.empgid + "","entity":entity}
            token = jwt.token(request)
            headers = {"content-type": "application/json", "Authorization": "" + token + ""}
            datas = json.dumps(jsondata.get('data'))
            resp = requests.post("" + ip + "/Dealer_Price_API", params=params, data=datas, headers=headers,
                                 verify=False)
            response = resp.content.decode("utf-8")
            return HttpResponse(response)
        elif (jsondata.get('Group')) == 'STATUS':
            obj = view_sales.SalesOrder_Register()
            obj.grp = jsondata.get('Group')
            obj.typ = jsondata.get('Type')
            obj.actn = jsondata.get('Action')
            entity = request.session['Entity_gid']
            obj.empgid = request.session['Emp_gid']
            params = {'Group': "" + obj.grp + "", 'Type': "" + obj.typ + "", 'Action': "" + obj.actn + "",
                      'Employee_Gid': "" + obj.empgid + "","entity":entity}
            token = jwt.token(request)
            headers = {"content-type": "application/json", "Authorization": "" + token + ""}
            datas = json.dumps(jsondata.get('data'))
            resp = requests.post("" + ip + "/Dealer_Price_API", params=params, data=datas, headers=headers,
                                 verify=False)
            response = resp.content.decode("utf-8")
            return HttpResponse(response)
        elif (jsondata.get('Group')) == 'DEALER_PRICE_UNIQUE':
            obj = view_sales.SalesOrder_Register()
            obj.grp = jsondata.get('Group')
            obj.typ = jsondata.get('Type')
            obj.sbtyp = jsondata.get('Sub_Type')
            obj.empgid = request.session['Emp_gid']
            params = {'Group': "" + obj.grp + "", 'Type': "" + obj.typ + "", 'Sub_Type': "" + obj.sbtyp + "",
                      'Employee_Gid': "" + obj.empgid + "","entity":entity}
            token = jwt.token(request)
            headers = {"content-type": "application/json", "Authorization": "" + token + ""}
            datas = json.dumps(jsondata.get('data'))
            resp = requests.post("" + ip + "/Dealer_Price_API", params=params, data=datas, headers=headers,
                                 verify=False)
            response = resp.content.decode("utf-8")
            return HttpResponse(response)


def get_state(request):
    utl.check_authorization(request)
    utl.check_pointaccess(request)
    if request.method == 'POST':
        jsondata = json.loads(request.body.decode('utf-8'))
        if (jsondata.get('Type')) == 'DDL':
            obj = view_sales.SalesOrder_Register()
            obj.typ = jsondata.get('Type')
            obj.sbtyp = jsondata.get('Subtype')
            entity=request.session['Entity_gid']
            obj.empgid = jsondata.get('Emp_Gid')
            params = {'Emp_Gid': "" + obj.empgid + "", 'Type': "" + obj.typ + "",
                      'Subtype': "" + obj.sbtyp + "","entity":entity}
            token = jwt.token(request)
            headers = {"content-type": "application/json", "Authorization": "" + token + ""}
            datas = json.dumps(jsondata.get('data'))
            resp = requests.post("" + ip + "/StatePrice_API_Get", params=params, data=datas, headers=headers,
                                 verify=False)
            response = resp.content.decode("utf-8")
            return HttpResponse(response)

def get_prod(request):
    utl.check_authorization(request)
    utl.check_pointaccess(request)
    try:
        if request.method == 'POST':
            jsondata = json.loads(request.body.decode('utf-8'))
            obj = view_sales.SalesOrder_Register()
            obj.actn = jsondata.get('Action')
            obj.entity_gid = request.session['Entity_gid']
            params = {'Action': "" + obj.actn + "", 'Entity_Gid': "" + obj.entity_gid + ""}
            token = jwt.token(request)
            headers = {"content-type": "application/json", "Authorization": "" + token + ""}
            datas = json.dumps(jsondata.get('data'))
            log_data = [{"BEFORE_ALL_TABLES_VALUES_GET": datas}]
            common.logger.error(log_data)
            resp = requests.post("" + ip + "/All_Tables_Values_Get", params=params, data=datas, headers=headers,
                                 verify=False)
            response = resp.content.decode("utf-8")
            log_data = [{"AFTER_ALL_TABLES_VALUES_GET": len(response)}]
            common.logger.error(log_data)
            return HttpResponse(response)
    except Exception as e:
        common.logger.error(str(e),"All_Tables_Values_Get")
        return Response({"MESSAGE": "ERROR_OCCURED", "DATA": str(e)})



def prodmapgsmry(request):
    utl.check_authorization(request)
    utl.check_pointaccess(request)
    entity=request.session['Entity_gid']
    if request.method == 'POST':
        jsondata = json.loads(request.body.decode('utf-8'))
        if (jsondata.get('Group')) == 'SUMMARY':
            obj = view_sales.SalesOrder_Register()
            obj.grp = jsondata.get('Group')
            obj.typ = jsondata.get('Type')
            obj.sbtyp = jsondata.get('Sub_Type')
            obj.empgid = request.session['Emp_gid']
            obj.lmt = json.dumps(jsondata.get('Limit'))
            params = {'Group': "" + obj.grp + "", 'Type': "" + obj.typ + "", 'Sub_Type': "" + obj.sbtyp + "",
                      'Employee_Gid': "" + obj.empgid + "", 'Limit': "" + obj.lmt + "","entity":entity}
            token = jwt.token(request)
            headers = {"content-type": "application/json", "Authorization": "" + token + ""}
            datas = json.dumps(jsondata.get('data'))
            resp = requests.post("" + ip + "/Rate_Card_API", params=params, data=datas, headers=headers, verify=False)
            response = resp.content.decode("utf-8")
            return HttpResponse(response)
        elif (jsondata.get('Group')) == 'MAKER':
            obj = view_sales.SalesOrder_Register()
            obj.grp = jsondata.get('Group')
            obj.typ = jsondata.get('Type')
            obj.actn = jsondata.get('Action')
            obj.empgid = request.session['Emp_gid']
            params = {'Group': "" + obj.grp + "", 'Type': "" + obj.typ + "", 'Action': "" + obj.actn + "",
                      'Employee_Gid': "" + obj.empgid + "","entity":entity}
            token = jwt.token(request)
            headers = {"content-type": "application/json", "Authorization": "" + token + ""}
            token = jwt.token(request)
            datas = json.dumps(jsondata.get('data'))
            resp = requests.post("" + ip + "/Rate_Card_API", params=params, data=datas, headers=headers, verify=False)
            response = resp.content.decode("utf-8")
            return HttpResponse(response)
        elif (jsondata.get('Group')) == 'BULK_SUMMARY':
            obj = view_sales.SalesOrder_Register()
            obj.grp = jsondata.get('Group')
            obj.typ = jsondata.get('Type')
            obj.sbtyp = jsondata.get('Sub_Type')
            obj.empgid = request.session['Emp_gid']
            params = {'Group': "" + obj.grp + "", 'Type': "" + obj.typ + "", 'Sub_Type': "" + obj.sbtyp + "",
                      'Employee_Gid': "" + obj.empgid + "","entity":entity}
            token = jwt.token(request)
            headers = {"content-type": "application/json", "Authorization": "" + token + ""}
            datas = json.dumps(jsondata.get('data'))
            resp = requests.post("" + ip + "/Rate_Card_API", params=params, data=datas, headers=headers, verify=False)
            response = resp.content.decode("utf-8")
            return HttpResponse(response)
        elif (jsondata.get('Group')) == 'STATUS':
            obj = view_sales.SalesOrder_Register()
            obj.grp = jsondata.get('Group')
            obj.typ = jsondata.get('Type')
            obj.actn = jsondata.get('Action')
            obj.empgid = request.session['Emp_gid']
            params = {'Group': "" + obj.grp + "", 'Type': "" + obj.typ + "", 'Action': "" + obj.actn + "",
                      'Employee_Gid': "" + obj.empgid + "","entity":entity}
            token = jwt.token(request)
            headers = {"content-type": "application/json", "Authorization": "" + token + ""}
            datas = json.dumps(jsondata.get('data'))
            resp = requests.post("" + ip + "/Rate_Card_API", params=params, data=datas, headers=headers, verify=False)
            response = resp.content.decode("utf-8")
            return HttpResponse(response)


def set_inv(request):
    utl.check_authorization(request)
    utl.check_pointaccess(request)
    if request.method == 'POST':
        jsondata = json.loads(request.body.decode('utf-8'))
        if (jsondata.get('Group')) == 'SALES_INV_PROCESS':
            obj = view_sales.SalesOrder_Register()
            obj.grp = jsondata.get('Group')
            obj.actn = jsondata.get('Action')
            obj.typ = jsondata.get('Type')
            obj.crtby = request.session['Emp_gid']
            obj.cmt = jsondata.get('Is_Commit')
            params = {'Group': "" + obj.grp + "","entity":request.session['Entity_gid'], 'Action': "" + obj.actn + "", 'Type': "" + obj.typ + "",
                      'Create_by': "" + obj.crtby + "", 'Is_Commit': "" + obj.cmt + ""}
            token = jwt.token(request)
            headers = {"content-type": "application/json", "Authorization": "" + token + ""}
            datas = json.dumps(jsondata.get('data'))
            resp = requests.post("" + ip + "/SalesInv_Process_set", params=params, data=datas, headers=headers,
                                 verify=False)
            response = resp.content.decode("utf-8")
            return HttpResponse(response)
        elif (jsondata.get('Group')) == 'INV_Process_Single_GET':
            jsondata['data']['Params']['HEADER']['Employee_Gid'] = request.session['Emp_gid']
            obj = view_sales.SalesOrder_Register()
            obj.sbtyp = jsondata.get('Sub_Type')
            obj.grp = jsondata.get('Group')
            obj.typ = jsondata.get('Type')
            params = { "entity":request.session['Entity_gid'],'Sub_Type': "" + obj.sbtyp + "", 'Group': "" + obj.grp + "", 'Type': "" + obj.typ + ""}
            token = jwt.token(request)
            headers = {"content-type": "application/json", "Authorization": "" + token + ""}
            datas = json.dumps(jsondata.get('data'))
            resp = requests.post("" + ip + "/SalesInv_Process_set", params=params, data=datas, headers=headers,
                                 verify=False)
            response = resp.content.decode("utf-8")
            return HttpResponse(response)
        elif (jsondata.get('Group')) == 'UPDATE_STATUS':
            obj = view_sales.SalesOrder_Register()
            jsondata['data']['Params']['HEADER']['Employee_Gid'] = request.session['Emp_gid']
            obj.actn = jsondata.get('Action')
            obj.grp = jsondata.get('Group')
            obj.typ = jsondata.get('Type')
            obj.cmt = jsondata.get('Is_Commit')
            obj.crtby =  request.session['Emp_gid']
            # entity = request.session['Entity_gid']
            params = {"entity":request.session['Entity_gid'],'Action': "" + obj.actn + "", 'Create_by': "" + obj.crtby + "", 'Group': "" + obj.grp + "",
                      'Type': "" + obj.typ + "", 'Is_Commit': "" + obj.cmt + ""}
            token = jwt.token(request)
            headers = {"content-type": "application/json", "Authorization": "" + token + ""}
            datas = json.dumps(jsondata.get('data'))
            resp = requests.post("" + ip + "/SalesInv_Process_set", params=params, data=datas, headers=headers,
                                 verify=False)
            response = resp.content.decode("utf-8")
            return HttpResponse(response)

        elif (jsondata.get('Group')) == 'SALES_INV_CANCEL':
            obj = view_sales.SalesOrder_Register()
            obj.actn = jsondata.get('Action')
            obj.grp = jsondata.get('Group')
            obj.typ = jsondata.get('Type')
            obj.cmt = jsondata.get('Is_Commit')
            obj.crtby =  request.session['Emp_gid']
            entity = request.session['Entity_gid']
            params = {"entity":entity,'Action': "" + obj.actn + "", 'Create_by': "" + obj.crtby + "", 'Group': "" + obj.grp + "",
                      'Type': "" + obj.typ + "", 'Is_Commit': "" + obj.cmt + ""}
            token = jwt.token(request)
            headers = {"content-type": "application/json", "Authorization": "" + token + ""}
            datas = json.dumps(jsondata.get('data'))
            resp = requests.post("" + ip + "/SalesInv_Process_set", params=params, data=datas, headers=headers,
                                 verify=False)
            response = resp.content.decode("utf-8")
            return HttpResponse(response)

        elif (jsondata.get('Group')) == 'SALES_PARTIAL_CANCEL':
            obj = view_sales.SalesOrder_Register()
            obj.actn = jsondata.get('Action')
            obj.grp = jsondata.get('Group')
            entity = request.session['Entity_gid']
            obj.crtby =  request.session['Emp_gid']
            params = {'entity':entity,'Action': "" + obj.actn + "", 'Create_by': "" + obj.crtby + "", 'Group': "" + obj.grp + ""
                     }
            token = jwt.token(request)
            headers = {"content-type": "application/json", "Authorization": "" + token + ""}
            datas = json.dumps(jsondata.get('data'))
            resp = requests.post("" + ip + "/SalesInv_Process_set", params=params, data=datas, headers=headers,
                                 verify=False)
            response = resp.content.decode("utf-8")
            return HttpResponse(response)

def set_sal(request):
    utl.check_authorization(request)
    utl.check_pointaccess(request)
    if request.method == 'POST':
        jsondata = json.loads(request.body.decode('utf-8'))
        obj = view_sales.SalesOrder_Register()
        obj.grp = jsondata.get('Group')
        obj.typ = jsondata.get('Type')
        obj.sub = jsondata.get('Sub_Type')
        # jsondata['data']['Params']['FILTER']['Employee_Gid'] = request.session['Emp_gid']
        entity=request.session['Entity_gid']
        params = {'Group': "" + obj.grp + "", 'Type': "" + obj.typ + "", 'Sub_Type': "" + obj.sub + "","entity":entity,"Create_by":request.session['Emp_gid']}
        token = jwt.token(request)
        headers = {"content-type": "application/json", "Authorization": "" + token + ""}
        datas = json.dumps(jsondata.get('data'))
        resp = requests.post("" + ip + "/SalesInv_Process_set", params=params, data=datas, headers=headers,
                             verify=False)
        response = resp.content.decode("utf-8")
        return HttpResponse(response)


def getinvsmry(request):
    utl.check_authorization(request)
    utl.check_pointaccess(request)
    if request.method == 'POST':
        jsondata = json.loads(request.body.decode('utf-8'))
        obj = view_sales.SalesOrder_Register()
        obj.grp = jsondata.get('Group')
        obj.typ = jsondata.get('Type')
        obj.sbtyp = jsondata.get('Sub_Type')
        obj.crtby = request.session['Emp_gid']
        entity = request.session['Entity_gid']
        params = {'Employee_Gid': "" + obj.crtby + "", 'Group': "" + obj.grp + "", 'Type': "" + obj.typ + "",
                  'Sub_Type': "" + obj.sbtyp + "","entity":entity,"Create_by":obj.crtby}
        token = jwt.token(request)
        headers = {"content-type": "application/json", "Authorization": "" + token + ""}
        datas = json.dumps(jsondata.get('data'))
        resp = requests.post("" + ip + "/Invoice_Dispatch_API", params=params, data=datas, headers=headers,
                             verify=False)
        response = resp.content.decode("utf-8")
        return HttpResponse(response)


def SetDispatchValue(request):
    utl.check_authorization(request)
    utl.check_pointaccess(request)
    if request.method == 'POST':
        jsondata = json.loads(request.body.decode('utf-8'))
        obj = view_sales.SalesOrder_Register()
        obj.employee_gid = request.session['Emp_gid']
        params = {'Employee_Gid': "" + obj.employee_gid + ""}
        token = jwt.token(request)
        headers = {"content-type": "application/json", "Authorization": "" + token + ""}
        datas = jsondata.get('data')
        datas['Employee_Gid'] = obj.employee_gid
        datas = json.dumps(jsondata.get('data'))
        resp = requests.post("" + ip + "/Sales_Dispatch", params=params, data=datas, headers=headers, verify=False)
        response = resp.content.decode("utf-8")
        return HttpResponse(response)


def CampaignEventAPI(request):
    utl.check_authorization(request)
    if request.method == 'POST':
        jsondata = json.loads(request.body.decode('utf-8'))
        obj = view_sales.SalesOrder_Register()
        obj.action = jsondata.get('Action')
        obj.type = jsondata.get('Type')
        obj.group = jsondata.get('Group')
        obj.empgid = request.session['Emp_gid']
        params = {'Group': "" + obj.group + "", 'Type': "" + obj.type + "",'Emp_Gid': "" + obj.empgid + "", 'Action': "" + obj.action + ""}
        token = jwt.token(request)
        headers = {"content-type": "application/json", "Authorization": "" + token + ""}
        datas = json.dumps(jsondata.get('data'))
        resp = requests.post("" + ip + "/SalesOrder_APIGet", params=params, data=datas, headers=headers, verify=False)
        response = resp.content.decode("utf-8")
        return HttpResponse(response)


def get_prodlabl(request):
    utl.check_authorization(request)
    utl.check_pointaccess(request)
    if request.method == 'POST':
        jsondata = json.loads(request.body.decode('utf-8'))
        if (jsondata.get('Group')) == 'SALES_SPLIT_QUANTITY':
            obj = view_sales.SalesOrder_Register()
            obj.type = jsondata.get('Type')
            obj.subtyp = jsondata.get('Sub_Type')
            obj.grp = jsondata.get('Group')
            entity = request.session['Entity_gid']
            jsondata['data']['Params']['FILTER']['Employee_Gid'] = request.session['Emp_gid']
            params = {'Type': "" + obj.type + "", 'Sub_Type': "" + obj.subtyp + "", 'Group': "" + obj.grp + "","entity":entity}
            token = jwt.token(request)

            headers = {"content-type": "application/json", "Authorization": "" + token + ""}
            datas = json.dumps(jsondata.get('data'))
            resp = requests.post("" + ip + "/DispatchProcess_Get", params=params, data=datas, headers=headers,
                                 verify=False)
            response = resp.content.decode("utf-8")
            return HttpResponse(response)

        elif (jsondata.get('Group')) == 'SALES_FULL_QUANTITY':
            obj = view_sales.SalesOrder_Register()
            obj.type = jsondata.get('Type')
            obj.subtyp = jsondata.get('Sub_Type')
            obj.grp = jsondata.get('Group')
            jsondata['data']['Params']['FILTER']['Employee_Gid'] = request.session['Emp_gid']
            entity = request.session['Entity_gid']
            params = {'Type': "" + obj.type + "", 'Sub_Type': "" + obj.subtyp + "", 'Group': "" + obj.grp + "","entity":entity}
            token = jwt.token(request)
            headers = {"content-type": "application/json", "Authorization": "" + token + ""}
            datas = json.dumps(jsondata.get('data'))
            resp = requests.post("" + ip + "/DispatchProcess_Get", params=params, data=datas, headers=headers,
                                 verify=False)
            response = resp.content.decode("utf-8")
            return HttpResponse(response)

        elif (jsondata.get('Group')) == 'DISPATCH_POD_SUMMARY':
            obj = view_sales.SalesOrder_Register()
            obj.type = jsondata.get('Type')
            obj.subtyp = jsondata.get('Sub_Type')
            obj.grp = jsondata.get('Group')
            entity = request.session['Entity_gid']
            jsondata['data']['Params']['FILTER']['Employee_Gid'] = request.session['Emp_gid']
            params = {'Type': "" + obj.type + "", 'Sub_Type': "" + obj.subtyp + "", 'Group': "" + obj.grp + "","entity":entity}
            token = jwt.token(request)
            headers = {"content-type": "application/json", "Authorization": "" + token + ""}
            datas = json.dumps(jsondata.get('data'))
            resp = requests.post("" + ip + "/DispatchProcess_Get", params=params, data=datas, headers=headers,
                                 verify=False)
            response = resp.content.decode("utf-8")
            return HttpResponse(response)

        elif (jsondata.get('Group')) == 'LABEL_PRINT_SALES':
            obj = view_sales.SalesOrder_Register()
            obj.type = jsondata.get('Type')
            obj.subtyp = jsondata.get('Sub_Type')
            obj.grp = jsondata.get('Group')
            jsondata['data']['Params']['FILTER']['Employee_Gid'] = request.session['Emp_gid']
            entity = request.session['Entity_gid']
            params = {'Type': "" + obj.type + "", 'Sub_Type': "" + obj.subtyp + "", 'Group': "" + obj.grp + "","entity":entity}
            token = jwt.token(request)

            headers = {"content-type": "application/json", "Authorization": "" + token + ""}
            datas = json.dumps(jsondata.get('data'))
            resp = requests.post("" + ip + "/DispatchProcess_Get", params=params, data=datas, headers=headers,
                                 verify=False)
            response = resp.content.decode("utf-8")
            return HttpResponse(response)

        elif (jsondata.get('Group')) == 'GENERATE_AWB_NO':
            obj = view_sales.SalesOrder_Register()
            obj.type = jsondata.get('Type')
            obj.subtyp = jsondata.get('Sub_Type')
            obj.grp = jsondata.get('Group')
            jsondata['data']['Params']['FILTER']['Employee_Gid'] = request.session['Emp_gid']
            params = {'Type': "" + obj.type + "", 'Sub_Type': "" + obj.subtyp + "", 'Group': "" + obj.grp + "", "entity" : request.session['Entity_gid']}
            token = jwt.token(request)
            headers = {"content-type": "application/json", "Authorization": "" + token + ""}
            datas = json.dumps(jsondata.get('data'))
            resp = requests.post("" + ip + "/DispatchProcess_Get", params=params, data=datas, headers=headers,
                                 verify=False)
            response = resp.content.decode("utf-8")
            return HttpResponse(response)

        elif (jsondata.get('Group')) == 'CONSIGNMENT_DETAILS':
            obj = view_sales.SalesOrder_Register()
            obj.type = jsondata.get('Type')
            obj.subtyp = jsondata.get('Sub_Type')
            jsondata['data']['Params']['FILTER']['Employee_Gid']= request.session['Emp_gid']

            obj.grp = jsondata.get('Group')
            entity = request.session['Entity_gid']
            params = {'Type': "" + obj.type + "", 'Sub_Type': "" + obj.subtyp + "", 'Group': "" + obj.grp + "","entity": entity}
            token = jwt.token(request)
            headers = {"content-type": "application/json", "Authorization": "" + token + ""}
            datas = json.dumps(jsondata.get('data'))
            resp = requests.post("" + ip + "/DispatchProcess_Get", params=params, data=datas, headers=headers,
                                 verify=False)
            response = resp.content.decode("utf-8")
            return HttpResponse(response)

        elif (jsondata.get('Group')) == 'Courier_Explorer':
            obj = view_sales.SalesOrder_Register()
            obj.type = jsondata.get('Type')
            obj.subtyp = jsondata.get('Sub_Type')
            obj.grp = jsondata.get('Group')
            entity = request.session['Entity_gid']
            jsondata['data']['Params']['FILTER']['Employee_Gid'] = request.session['Emp_gid']
            params = {'Type': "" + obj.type + "", 'Sub_Type': "" + obj.subtyp + "", 'Group': "" + obj.grp + "","entity":entity}
            token = jwt.token(request)
            headers = {"content-type": "application/json", "Authorization": "" + token + ""}
            datas = json.dumps(jsondata.get('data'))
            resp = requests.post("" + ip + "/DispatchProcess_Get", params=params, data=datas, headers=headers,
                                 verify=False)
            response = resp.content.decode("utf-8")
            return HttpResponse(response)



def set_prodlabl(request):
    utl.check_authorization(request)
    utl.check_pointaccess(request)
    if request.method == 'POST':
        jsondata = json.loads(request.body.decode('utf-8'))
        if (jsondata.get('Group')) == 'CARTON_SALES':
            obj = view_sales.SalesOrder_Register()
            obj.type = jsondata.get('Type')
            obj.actn = jsondata.get('Action')
            obj.crtby = json.dumps(jsondata.get('Create_by'))
            obj.subtyp = jsondata.get('Sub_Type')
            obj.grp = jsondata.get('Group')
            params = {'Type': "" + obj.type + "", 'Action': "" + obj.actn + "", 'Sub_Type': "" + obj.subtyp + "",
                      'Group': "" + obj.grp + "", 'Create_by': "" + request.session['Emp_gid'] + "","entity":request.session['Entity_gid']}
            token = jwt.token(request)
            headers = {"content-type": "application/json", "Authorization": "" + token + ""}
            datas = json.dumps(jsondata.get('data'))
            resp = requests.post("" + ip + "/DispatchProcess_Set", params=params, data=datas, headers=headers,
                                 verify=False)
            response = resp.content.decode("utf-8")
            return HttpResponse(response)
        elif (jsondata.get('Group')) == 'CARTON_SPLIT':
            obj = view_sales.SalesOrder_Register()
            obj.type = jsondata.get('Type')
            obj.actn = jsondata.get('Action')
            obj.crtby = json.dumps(jsondata.get('Create_by'))
            obj.subtyp = jsondata.get('Sub_Type')
            obj.grp = jsondata.get('Group')
            params = {'Type': "" + obj.type + "", 'Action': "" + obj.actn + "", 'Sub_Type': "" + obj.subtyp + "",
                      'Group': "" + obj.grp + "", 'Create_by': "" + request.session['Emp_gid'] + "","entity":request.session['Entity_gid']}
            token = jwt.token(request)
            headers = {"content-type": "application/json", "Authorization": "" + token + ""}
            datas = json.dumps(jsondata.get('data'))
            resp = requests.post("" + ip + "/DispatchProcess_Set", params=params, data=datas, headers=headers,
                                 verify=False)
            response = resp.content.decode("utf-8")
            return HttpResponse(response)
        elif (jsondata.get('Group')) == 'DISPATCH_WEIGHT_UPDATE':
            obj = view_sales.SalesOrder_Register()
            obj.grp = jsondata.get('Group')
            obj.actn = jsondata.get('Action')
            obj.type = jsondata.get('Type')
            obj.subtyp = jsondata.get('Sub_Type')

            params = {'Group': "" + obj.grp + "", 'Action': "" + obj.actn + "",
                      'Type': "" + obj.type + "", 'Sub_Type': "" + obj.subtyp + "", 'Create_by': "" + request.session['Emp_gid'] + "","entity":request.session['Entity_gid']}
            token = jwt.token(request)
            headers = {"content-type": "application/json", "Authorization": "" + token + ""}
            datas = json.dumps(jsondata.get('data'))
            resp = requests.post("" + ip + "/DispatchProcess_Set", params=params, data=datas, headers=headers,
                                 verify=False)
            response = resp.content.decode("utf-8")
            return HttpResponse(response)
        elif (jsondata.get('Group')) == 'LABEL_PRINT_FLAG':
            obj = view_sales.SalesOrder_Register()
            obj.grp = jsondata.get('Group')
            obj.actn = jsondata.get('Action')
            obj.type = jsondata.get('Type')
            obj.subtyp = jsondata.get('Sub_Type')
            obj.crtby = json.dumps(jsondata.get('Create_by'))
            params = {'Group': "" + obj.grp + "", 'Action': "" + obj.actn + "",
                      'Type': "" + obj.type + "", 'Sub_Type': "" + obj.subtyp + "", 'Create_by': "" + request.session['Emp_gid'] + "","entity":request.session['Entity_gid']}
            token = jwt.token(request)
            headers = {"content-type": "application/json", "Authorization": "" + token + ""}
            datas = json.dumps(jsondata.get('data'))
            resp = requests.post("" + ip + "/DispatchProcess_Set", params=params, data=datas, headers=headers,
                                 verify=False)
            response = resp.content.decode("utf-8")
            return HttpResponse(response)


def masterdrpdwn(request):
    utl.check_authorization(request)
    utl.check_pointaccess(request)
    if request.method == 'POST':
        jsondata = json.loads(request.body.decode('utf-8'))
        # jsondata['Params']['CLASSIFICATION']={['Entity_Gid']}
        if (jsondata.get('Group')) == 'GET_ALL_PRODUCT':
            obj = view_sales.SalesOrder_Register()
            obj.grp = jsondata.get('Group')
            obj.typ = jsondata.get('Type')
            obj.sbtyp = jsondata.get('Sub_Type')
            params = {'Group': "" + obj.grp + "", 'Type': "" + obj.typ + "", 'Sub_Type': "" + obj.sbtyp + "",
                      'Entity_Gid':request.session['Entity_gid']}
            token = jwt.token(request)
            headers = {"content-type": "application/json", "Authorization": "" + token + ""}
            datas = json.dumps(jsondata.get('data'))
            resp = requests.post("" + ip + "/All_product_get", params=params, data=datas, headers=headers, verify=False)
            response = resp.content.decode("utf-8")
            return HttpResponse(response)


def branchdrpdown(request):
    utl.check_authorization(request)
    utl.check_pointaccess(request)
    if request.method == 'POST':
        jsondata = json.loads(request.body.decode('utf-8'))
        grp = jsondata.get('Group')
        typ = jsondata.get('Type')
        sbtyp =jsondata.get('SubType')
        entity= request.session['Entity_gid']
        params = {'Group': ""+grp +"",'Type':""+typ+"",'Sub_Type':""+sbtyp+"","entity":entity}
        token = jwt.token(request)
        headers = {"content-type": "application/json","Authorization": ""+token+""}
        datas = json.dumps(jsondata.get('data'))
        resp = requests.post(""+ip+"/Classification_Get",params=params,data = datas,headers= headers, verify=False)
        response = resp.content.decode("utf-8")
        return HttpResponse(response)