# import datetime
from datetime import timedelta,datetime as dt
import io
import time
import pandas as pd
import numpy as np
import xlsxwriter
from django.shortcuts import render
from xlsxwriter import Workbook
import Bigflow.Core.jwt_file as jwt
from Bigflow.API import view_sales
from Bigflow.Transaction.Model import mFET, mSales
from Bigflow.Report import views_API
import json
import requests
from Bigflow.Purchase.Model import mPurchase
from Bigflow.Report.Model import mPurchase
from dateutil.relativedelta import relativedelta
from django.http import JsonResponse
from django.http import HttpResponse, request
import Bigflow.Core.models as common
from Bigflow.Core.models import decrpt as decry_data

from Bigflow.menuClass import utility
import base64
from Bigflow.API import view_report
from Bigflow.Core.models import Excelfilename

from Bigflow.Report.Model.mastersyncdata import MasterSyncData
from Bigflow.menuClass import utility as utl

from Bigflow.Report.Model import magentsummary
from datetime import datetime
from apscheduler.scheduler import Scheduler

sched = Scheduler()
sched.start()

ip = common.localip()


def StockSummaryIndex(request):
    utl.check_authorization(request)
    return render(request, "Stock_Summary.html")


# Control sheet summary
def Control_Sheet_summary(request):
    utl.check_authorization(request)
    return render(request, "Control_sheet_summary.html")


# sales &Outstanding_control
def Controlsheet(request):
    utl.check_authorization(request)
    return render(request, "Sales_Outstanding_Control_Sheet.html")


# Outstanding_control
def os_Controlsheet(request):
    utl.check_authorization(request)
    return render(request, "Outstanding_controlsheet.html")


# agentsummary
#
# #master_sync_data
def master_sync_data(request):
    utl.check_authorization(request)
    return render(request, "MasterSync_Data.html")


# master_sync_failed
def master_sync_employee(request):
    utl.check_authorization(request)
    return render(request, "MasterSync_Employee.html")


def master_sync_branch(request):
    utl.check_authorization(request)
    return render(request, "MasterSync_Branch.html")


def master_sync_gl(request):
    utl.check_authorization(request)
    return render(request, "MasterSync_Gl.html")


def trandatadetails(request):
    utl.check_authorization(request)
    if request.method == 'POST':
        jsondata = json.loads(request.body.decode('utf-8'))
        action = jsondata.get('Action')
        type = jsondata.get('Type')
        classification = {"entity_gid": decry_data(request.session['Entity_gid'])}
        jsondata['classification'] = classification

        main = json.dumps(jsondata)
        params = {'Action': "" + action + "",
                  'Type': "" + type + ""}
        token = jwt.token(request)
        headers = {"content-type": "application/json", "Authorization": "" + token + ""}
        resp = requests.post("" + ip + "/Agaentsmry", params=params, data=main, headers=headers, verify=False)
        response = resp.content.decode("utf-8")
        return JsonResponse(response, safe=False)


# stock_controlsheet
def stock_controlsheet(request):
    utl.check_authorization(request)
    return render(request, "stock_controlsheet.html")


# PR PO Query Page
def pr_po_query(request):
    utl.check_authorization(request)
    return render(request, 'pr_po_query.html')


def get_alltable(request):
    utl.check_authorization(request)
    utl.check_pointaccess(request)
    if request.method == 'POST':
        jsondata = json.loads(request.body.decode('utf-8'))
        actn = jsondata.get('Action')
        entity = jsondata.get('Entity_Gid')
        if actn == 'emp':
            drop_m = {
                "Table_name": "gal_mst_temployee",
                "Column_1": "employee_gid,employee_name",
                "Column_2": "",
                "Where_Common": "employee",
                "Where_Primary": "dept_gid",
                "Primary_Value": "1",
                "Order_by": "name"
            }
            response = alltable(drop_m, actn, entity)
            return HttpResponse(response)
        elif actn == 'commodity':
            drop_m = {
                "Table_name": "ap_mst_tcommodity",
                "Column_1": "commodity_gid,commodity_name",
                "Column_2": "",
                "Where_Common": "commodity",
                "Where_Primary": "",
                "Primary_Value": "",
                "Order_by": "name"
            }
            response = alltable(drop_m, actn, entity)
            return HttpResponse(response)
        elif actn == 'product':
            drop_m = {
                "Table_name": "gal_mst_tproduct",
                "Column_1": "product_gid,product_name,product_displayname",
                "Column_2": "",
                "Where_Common": "product",
                "Where_Primary": "",
                "Primary_Value": "",
                "Order_by": "code"
            }
            response = alltable(drop_m, actn, entity)
            return HttpResponse(response)
        elif actn == 'branch':
            drop_m = {
                "Table_name": "gal_mst_tbranch",
                "Column_1": "branch_gid,branch_name",
                "Column_2": "",
                "Where_Common": "branch",
                "Where_Primary": "",
                "Primary_Value": "",
                "Order_by": "name"
            }
            response = alltable(drop_m, actn, entity)
            return HttpResponse(response)


def alltable(table_data, act, entity):
    drop_table = {"data": table_data}
    obj = view_sales.SalesOrder_Register()
    obj.action = act
    obj.entity_gid = entity
    params = {'Action': obj.action, 'Entity_Gid': obj.entity_gid}
    token = jwt.token(request)
    headers = {"content-type": "application/json", "Authorization": "" + token + ""}
    datas = json.dumps(drop_table.get('data'))
    resp = requests.post("" + ip + "/All_Tables_Values_Get", params=params, data=datas, headers=headers,
                         verify=False)
    response = resp.content.decode("utf-8")
    return HttpResponse(response)


def Pr_Po_data(request):
    utl.check_authorization(request)
    if request.method == 'POST':
        token = jwt.token(request)
        jsondata = json.loads(request.body.decode('utf-8'))
        obj = view_report.PRPO_Query()
        obj.grp = jsondata.get('params').get('Group')
        obj.typ = jsondata.get('params').get('Type')
        obj.sub = jsondata.get('params').get('Sub_Type')

        params = {"Group": obj.grp, "Type": obj.typ, "Sub_Type": obj.sub}
        token = jwt.token(request)
        headers = {"content-type": "application/json", "Authorization": "" + token + ""}
        datas = json.dumps(jsondata.get('params').get('json'))
        resp = requests.post("" + ip + "/PRPO_Query", params=params, data=datas, headers=headers,
                             verify=False)
        response = resp.content.decode("utf-8")
        return HttpResponse(response)


# Excel UPload for Control-sheet
def Control_Sheet(request):
    utl.check_authorization(request)
    if request.method == 'POST':
        encrypt_ex = base64.b64encode(request.FILES['file'].read())  # convert excel to base64

        dcrypt_ex = encrypt_ex.decode("utf-8")
        entry_id = request.session['Entity_gid']
        excel_file = request.FILES['file']  # geting the excel file from angular
        group = request.POST['Group']
        action = request.POST['Action']

        # subtype = request.POST['SubType']

        ex_type = request.POST['Type']
        drop_value = request.POST['Drop_value']
        created_by = request.session['Emp_gid']
        name = request.POST['name']
        File_Extension = name.split('.')
        # File_Extension = json.dumps(File_Extension[1])
        File_Extension = File_Extension[1]

        df = pd.read_excel(excel_file)
        params = {'Group': "" + group + "", 'Action': "" + action + "", 'Type': "" + ex_type + "",
                  'Create_by': "" + created_by + ""}

        if drop_value == 'outstanding':
            try:
                df = pd.read_excel(excel_file, skiprows=[0, 1, 2, 3, 4, 5, 6, 8])
                # df['Date'] = pd.to_datetime(df['Date'], format='%Y-%m-%d')
                # print(df)
                df = df.iloc[:-1]
                final_df = df[["Party's Name", 'Date', 'Ref. No.', 'Pending', 'Opening']]
                final_df['Opening'] = final_df['Opening'].replace('Dr', ' ', regex=True)
                delivery_date = final_df['Date'].dt.strftime('%Y-%m-%d')
                final_df['Date'] = delivery_date
                final_df.columns = ['Customer_Name', 'Invoice_Date', 'Invoice_No', 'Pending_Amount', 'Amount']

                jdata = final_df.to_dict(orient='records')

                param = {'Group': "" + 'CONTROL_OUTSTANDING' + "", 'Action': "" + 'INSERT' + "",
                         'Type': "" + 'CONTROL_OUTSTANDING' + "", 'SubType': "" + 'TALLY' + "",
                         'Create_by': "" + created_by + ""}

                resultdata = {
                    "Params": {
                        "DETAILS": {
                            "OUTSTANDING_DETAILS": jdata

                        },
                        "File": [{
                            "File_Name": name,
                            "File_Extension": File_Extension,
                            "File_Base64data": dcrypt_ex
                        }],

                        "CLASSIFICATION": {"Entity_Gid": entry_id}
                    }
                }
                dta = json.dumps(resultdata)
                token = jwt.token(request)
                headers = {"content-type": "application/json", "Authorization": "" + token + ""}

                resp = requests.post("" + ip + "/Control_Sheet", params=param, data=dta, headers=headers, verify=False)
                response = resp.content.decode("utf-8")
                return HttpResponse(response)


            except:
                ld_dict = {"DATA": 'ERROR_OCCURED.'}
                return HttpResponse(ld_dict)

        elif drop_value == 'stock':
            try:
                df = pd.read_excel(excel_file, skiprows=[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11])
                date = request.POST['Date']
                Godown_Gid = request.POST['Godown_Gid']
                df = df.iloc[:-1]
                df['Quantity'].fillna(0, inplace=True)
                final_df = df[['Unnamed: 0', 'Quantity']]
                final_df['Quantity'] = final_df['Quantity'].replace('NaN', 0, regex=True)
                final_df.columns = ['Particulars', 'Quantity']
                jdata = final_df.to_dict(orient='records')
                param = {'Group': "" + 'CONTROL_STOCK' + "", 'Action': "" + 'INSERT' + "",
                         'Type': "" + 'CONTROL_STOCK' + "", 'SubType': "" + 'TALLY' + "",
                         'Create_by': "" + created_by + ""}
                resultdata = {
                    "Params": {
                        "DETAILS": {
                            "STOCK_DETAILS": jdata,
                            "Date": date,
                            "Godown_Gid": Godown_Gid
                        },
                        "File": [{
                            "File_Name": name,
                            "File_Extension": File_Extension,
                            "File_Base64data": dcrypt_ex
                        }],
                        "CLASSIFICATION": {"Entity_Gid": entry_id}
                    }
                }
                dta = json.dumps(resultdata)
                token = jwt.token(request)
                headers = {"content-type": "application/json", "Authorization": "" + token + ""}
                resp = requests.post("" + ip + "/Control_Sheet", params=param, data=dta, headers=headers, verify=False)
                response = resp.content.decode("utf-8")
                return HttpResponse(response)

            except:
                ld_dict = {"DATA": 'ERROR_OCCURED.'}
                return HttpResponse(ld_dict)

        else:
            try:

                final_df = df[
                    ['Party Name', 'Item Name', 'Date', 'Voucher Number', 'Billed Quantity', 'Rate', 'Amount']]
                # final_df['Date']=pd.to_datetime(final_df['Date'])
                delivery_date = final_df['Date'].dt.strftime('%Y-%m-%d')
                final_df['Date'] = delivery_date
                final_df.columns = ['Customer_Name', 'Product_Name', 'Invoice_Date', 'Invoice_No', 'Quantity',
                                    'Per_Rate', 'Amount']
                jdata = final_df.to_dict(orient='records')
                resultdata = {
                    "Params": {
                        "DETAILS": {
                            "SALE_DETAILS": jdata

                        },
                        "File": [{
                            "File_Name": name,
                            "File_Extension": File_Extension,
                            "File_Base64data": dcrypt_ex
                        }],

                        "CLASSIFICATION": {"Entity_Gid": entry_id}
                    }
                }
                dta = json.dumps(resultdata)
                token = jwt.token(request)
                headers = {"content-type": "application/json", "Authorization": "" + token + ""}

                resp = requests.post("" + ip + "/Control_Sheet", params=params, data=dta, headers=headers, verify=False)
                response = resp.content.decode("utf-8")
                return HttpResponse(response)
            except:
                ld_dict = {"DATA": 'ERROR_OCCURED.'}

                return HttpResponse(ld_dict)


def Four_Line_Mis(request):
    utl.check_authorization(request)
    return render(request, "Four_Line_MIS.html")


def newoverallReportIndex(request):
    # utility.sendFlashNotification("", "", ['dsfsdf', ])
    # utl.check_authorization(request)
    return render(request, "New_Overall_Report.html")


def newoverallReportsmryIndex(request):
    # utility.sendFlashNotification("", "", ['dsfsdf', ])
    # utl.check_authorization(request)
    return render(request, "New_overallreportSmry.html")


def performance_excel(request):
    utl.check_authorization(request)
    utl.check_pointaccess(request)
    if request.method == 'GET':
        jsondata = json.loads(request.GET['Main'])
        jsondata1 = json.loads(request.GET['Sub'])
        obj_totalsales = mSales.Sales_Model()
        obj_totalsales.type = jsondata.get('Type')
        obj_totalsales.sub_type = jsondata.get('Sub_Type')
        obj_totalsales.jsonData = json.dumps(jsondata1.get('Params').get('FILTER'))
        obj_totalsales.json_classification = \
            json.dumps(jsondata1.get('Params').get('CLASSIFICATION'))
        XLSX_MIME = 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        response = HttpResponse(content_type=XLSX_MIME)
        filename = Excelfilename('FourLineMIS_')
        response['Content-Disposition'] = 'attachment; filename="{}"'.format(filename)
        # response['Content-Disposition'] = 'attachment; filename="FourLineMIS.xlsx"'
        writer = pd.ExcelWriter(response, engine='xlsxwriter')
        df_view = obj_totalsales.get_sales()
        df_view['CUSTOMER_NAME'] = df_view['customer_name']
        df_view['CUSTOMER_GROUP_NAME'] = df_view['customergroup_name']
        df_view['EMPLOYEE_NAME'] = df_view['employee_name']
        df_view['BRANCH_NAME'] = df_view['branch_name']
        df_view['DEPARTMENT_NAME'] = df_view['dept_name']
        df_view['LOCATION_NAME'] = df_view['location_name']
        df_view['MONTH_WISE'] = df_view['mntdate']
        df_view['SALES'] = df_view['invtot']
        df_view['RECEIPT'] = df_view['reptamt']
        df_view['CREDIT'] = df_view['cramt']
        df_view['OUTSTANDING'] = df_view['oss']
        final = df_view[
            ['CUSTOMER_NAME', 'CUSTOMER_GROUP_NAME', 'EMPLOYEE_NAME', 'BRANCH_NAME', 'DEPARTMENT_NAME', 'LOCATION_NAME',
             'MONTH_WISE', 'SALES', 'RECEIPT', 'CREDIT', 'OUTSTANDING']]
        final.to_excel(writer, 'Sheet1')
        writer.save()
        return response


def get_totalsales_and_totaloutstanding(request):
    utl.check_authorization(request)
    if request.method == 'POST':
        jsondata = json.loads(request.body.decode('utf-8'))
        obj = views_API.StockAPI()
        obj.group = jsondata.get('Group')
        obj.sub_type = jsondata.get('Sub_Type')
        obj.type = jsondata.get('Type')
        params = {
            'Group': "" + obj.group + "",
            'Type': "" + obj.type + "",
            'Sub_Type': "" + obj.sub_type + "",
            "entity": request.session['Entity_gid']
        }
        datas = json.dumps(jsondata.get('data'))
        token = jwt.token(request)
        headers = {"content-type": "application/json", "Authorization": "" + token + ""}
        resp = requests.post("" + ip + "/Report_Total_Sales", params=params, data=datas, headers=headers, verify=False)
        response = resp.content.decode("utf-8")
        return HttpResponse(response)


# get controlsheetsummary
def getControl_Sheet(request):
    utl.check_authorization(request)
    jsondata = json.loads(request.body.decode('utf-8'))
    if (jsondata.get('Group')) == 'INITIAL_SUMMARY':
        group = jsondata.get('Group')
        type = jsondata.get('Type')
        subtype = jsondata.get('SubType')
        emp_gid = jsondata.get('Employee_Gid')
        # data = jsondata.get('darta')

        params = {'Group': "" + group + "", 'Type': "" + type + "",
                  'SubType': "" + subtype + "", 'Employee_Gid': "" + emp_gid + ""}
        token = jwt.token(request)
        headers = {"content-type": "application/json", "Authorization": "" + token + ""}

        datas = json.dumps(jsondata.get('darta'))
        resp = requests.post("" + ip + "/Control_Sheet", params=params, data=datas, headers=headers, verify=False)
        response = resp.content.decode("utf-8")

        return HttpResponse(response)


# sale summary
def getComparesale(request):
    utl.check_authorization(request)
    if request.method == 'POST':
        jsondata = json.loads(request.body.decode('utf-8'))
        group = jsondata.get('Group')
        type = jsondata.get('Type')
        subtype = jsondata.get('SubType')
        emp_gid = jsondata.get('Employee_Gid')
        # data = jsondata.get('darta')

        params = {'Group': "" + group + "", 'Type': "" + type + "",
                  'SubType': "" + subtype + "", 'Employee_Gid': "" + str(emp_gid) + ""}
        token = jwt.token(request)
        headers = {"content-type": "application/json", "Authorization": "" + token + ""}
        datas = json.dumps(jsondata.get('darta'))
        resp = requests.post("" + ip + "/Control_Sheet", params=params, data=datas, headers=headers, verify=False)
        response = resp.content.decode("utf-8")
        return HttpResponse(response)


# outstanding summary
def getCompareos(request):
    utl.check_authorization(request)
    if request.method == 'POST':
        jsondata = json.loads(request.body.decode('utf-8'))
        group = jsondata.get('Group')
        type = jsondata.get('Type')
        subtype = jsondata.get('SubType')
        emp_gid = jsondata.get('Employee_Gid')
        # data = jsondata.get('darta')
        params = {'Group': "" + group + "", 'Type': "" + type + "",
                  'SubType': "" + subtype + "", 'Employee_Gid': "" + str(emp_gid) + ""}
        token = jwt.token(request)
        headers = {"content-type": "application/json", "Authorization": "" + token + ""}
        datas = json.dumps(jsondata.get('darta'))
        resp = requests.post("" + ip + "/Control_Sheet", params=params, data=datas, headers=headers, verify=False)
        response = resp.content.decode("utf-8")
        return HttpResponse(response)


def setupdate(request):
    utl.check_authorization(request)
    if request.method == 'POST':
        jsondata = json.loads(request.body.decode('utf-8'))
        obj = views_API.StockAPI()
        obj.group = jsondata.get('Group')
        obj.action = jsondata.get('Action')
        obj.type = jsondata.get('Type')
        obj.create_by = request.session['Entity_gid']
        params = {
            'Group': "" + obj.group + "",
            'Action': "" + obj.action + "",
            'Type': "" + obj.type + "",
            'Create_by': "" + obj.create_by + ""
        }
        datas = json.dumps(jsondata.get('data'))
        token = jwt.token(request)
        headers = {"content-type": "application/json", "Authorization": "" + token + ""}
        resp = requests.post("" + ip + "/Stock_Summary_API", params=params, data=datas, headers=headers, verify=False)
        response = resp.content.decode("utf-8")
        return HttpResponse(response)


def StockSum(request):
    utl.check_authorization(request)
    if request.method == "POST":
        jsondata = json.loads(request.body.decode('utf-8'))
        obj = views_API.StockAPI()
        obj.group = jsondata.get('Group')
        obj.type = jsondata.get('Type')
        obj.sub_type = jsondata.get('Sub_Type')
        obj.from_date = jsondata.get('From_Date')
        obj.to_date = jsondata.get('To_Date')
        obj.Product_Gid = jsondata.get('Product_Gid')
        obj.Supplier_Gid = json.dumps(jsondata.get('Supplier_Gid'))
        obj.Entity_Gid = request.session['Entity_gid']
        params = {'Group': "" + obj.group + "", 'Type': "" + obj.type + "", 'Sub_Type': "" + obj.sub_type + "",
                  'From_Date': "" + obj.from_date + "", 'To_Date': "" + obj.to_date + "",
                  'Product_Gid': obj.Product_Gid,
                  'Supplier_Gid': "" + obj.Supplier_Gid + "", 'Entity_Gid': "" + obj.Entity_Gid + ""}
        datas = json.dumps(jsondata.get('data'))

        token = jwt.token(request)
        headers = {"content-type": "application/json", "Authorization": "" + token + ""}
        resp = requests.post("" + ip + "/Stock_Summary_API", params=params, data=datas, headers=headers,
                             verify=False)
        response = resp.content.decode("utf-8")
        return HttpResponse(response)


def stcksumry_overall_rept(request):
    utl.check_authorization(request)
    if request.method == "GET":
        jsondata = json.loads(request.GET['Main'])
        obj = views_API.StockAPI()
        before_date = (datetime.strptime(jsondata.get('Cur_date'), '%Y-%m-%d') - timedelta(days=6)).strftime('%Y-%m-%d')
        obj.group = jsondata.get('Group')
        obj.type = jsondata.get('Type')
        obj.sub_type = jsondata.get('Sub_Type')
        obj.from_date = jsondata.get('From_Date')
        obj.to_date = jsondata.get('To_Date')
        obj.Product_Gid = jsondata.get('Product_Gid')
        obj.Supplier_Gid = json.dumps(jsondata.get('Supplier_Gid'))
        obj.Entity_Gid = request.session['Entity_gid']
        params = {'Group': "" + obj.group + "", 'Type': "" + obj.type + "", 'Sub_Type': "" + obj.sub_type + "",
                  'From_Date': "" + obj.from_date + "", 'To_Date': "" + obj.to_date + "",
                  'Product_Gid': obj.Product_Gid,
                  'Supplier_Gid': "" + obj.Supplier_Gid + "", 'Entity_Gid': "" + obj.Entity_Gid + ""}
        datas = json.dumps(jsondata.get('data'))
        token = jwt.token(request)
        headers = {"content-type": "application/json", "Authorization": "" + token + ""}
        resp = requests.post("" + ip + "/Stock_Summary_API", params=params, data=datas, headers=headers,
                             verify=False)
        stock_curdate = resp.content.decode("utf-8")
        data = json.loads(stock_curdate)
        data = data.get('DATA')
        df_curstk = pd.DataFrame(data)
        data = {"Params":
                    {"FILTER": {"date": before_date}}}
        datas = json.dumps(data)
        token = jwt.token(request)
        headers = {"content-type": "application/json", "Authorization": "" + token + ""}
        resp = requests.post("" + ip + "/Stock_Summary_API", params=params, data=datas, headers=headers,
                             verify=False)
        stock_todate = resp.content.decode("utf-8")
        data = json.loads(stock_todate)
        data = data.get('DATA')
        df_tostk = pd.DataFrame(data)
        obj_sales = mPurchase.Purchase_model()
        obj_sales.type = 'SUMMARY_DATEWISE'
        obj_sales.sub_type = 'ALL'
        obj_sales.fliter = {"From_Date": before_date, "To_Date": jsondata.get('Cur_date')}
        obj_sales.classification = {"Entity_Gid": 1}
        obj_sales.create_by = '1'
        data = obj_sales.get_salescount()
        df_sales = data
        df_cus = df_curstk[['product_name', 'stockbalance_cb']]
        df_yes = df_tostk[['stockbalance_cb']]
        df_cus['yesclsstk'] = df_tostk[['stockbalance_cb']]
        f_data = []
        headerdate = []
        for x, row in df_cus.iterrows():
            product_name = row["product_name"]
            yescb = row["yesclsstk"]
            curcb = row["stockbalance_cb"]
            dteonly = 0
            for y, row in df_sales.iterrows():
                if row["product_name"] == product_name:
                    dteonly = {}
                    date = row["Dates"]
                    headerdate.append(date)
                    qty = int(row["qty"])
                    d = {'product_name': product_name, 'cb1': yescb, date: qty, 'cb2': curcb}
                    dteonly = {date: qty}
                    for e in f_data:
                        for u in list(e):
                            prodname = e[u]
                            if (product_name == prodname):
                                e.update(dteonly)
                                d = {}
                                pass
                    f_data.append(d)
        headerdate = list(dict.fromkeys(headerdate))
        headerdate.sort(key=lambda date: datetime.strptime(date, "%d-%m-%Y"))
        headerdate.insert(0, "product_name")
        headerdate.insert(1, "cb1")
        headerdate.append("cb2")
        XLSX_MIME = 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        response = HttpResponse(content_type=XLSX_MIME)
        filename = Excelfilename('Stock Details')
        response['Content-Disposition'] = 'attachment; filename="{}"'.format(filename)
        # response['Content-Disposition'] = 'attachment; filename="Stock Details.xlsx"'
        writer = pd.ExcelWriter(response, engine='xlsxwriter')
        while ({} in f_data):
            f_data.remove({})
        dff = pd.DataFrame(f_data, columns=headerdate)
        dff.index = range(1, len(dff) + 1)
        dff.to_excel(writer, sheet_name='Stock', index_label='SL NO',
                     freeze_panes=(1, 0),
                     header=headerdate)
        writer.save()
        return response


def getOutstandingDetails(employee_gid, request):
    type = 'OUTSTANDING_REPORT_INVOICE_WISE'
    sub_type = 'BUCKET'
    params = {'Type': "" + type + "", 'Sub_Type': "" + sub_type + ""}
    filterDetails = {}
    if employee_gid != '0':
        filterDetails['Employee_Gid'] = employee_gid
    data = {'parms': {'filter': filterDetails, 'classification': {'Entity_Gid': [1]}}};
    token = jwt.token(request)
    headers = {"content-type": "application/json", "Authorization": "" + token + ""}
    resp = requests.post("" + ip + "/Outstanding_AR", params=params, data=json.dumps(data), headers=headers,
                         verify=False)
    response_data = resp.content.decode("utf-8")
    response_data = json.loads(response_data)
    dff = pd.DataFrame(response_data.get('DATA'))

    outstandingList = []
    head_columns = ['S.No', 'Customer Name', 'Location', 'Invoice No', 'Invoice Date', 'Quantity', 'Bill Amount'
        , 'Due Amount', 'Due Days', 'Credit Days', '< 30', '30 - 45', '45 - 60', '60 - 75', '75 - 90', '90 - 120',
                    '120 - 150',
                    '150 - 180', '> 180', 'Last pmt Date',
                    'Payment Amt', 'Aging Days', 'Employee Name']
    # ,'Customer Code',]
    # ,'paymentamt','lastpmtdate','aging']

    # bhead_columns = ['S.No', 'Customer Name', 'Employee Name', 'Bill Amount'
    #     , 'Due Amount', '< 30', '30 - 45', '45 - 60', '60 - 75', '75 - 90', '90 - 120', '120 - 150',
    #                  '150 - 180', '> 180', 'paymentamt', 'lastpmtdate', 'aging']
    for y, df in dff.iterrows():
        outstanding = {head_columns[0]: y + 1
            , head_columns[1]: df['customer_name']
            , head_columns[2]: df['location_name']
            , head_columns[3]: df['fetsoutstanding_invoiceno'], head_columns[4]: df['fetsoutstanding_invoicedate']
            , head_columns[5]: df['total_sale_qty'], head_columns[6]: df['fetsoutstanding_netamount']
            , head_columns[7]: df['balance_amount'],
                       head_columns[8]: df['Due_Days'],
                       head_columns[9]: df['fetsoutstanding_creditdays']
                       # ,head_columns[23]: df['customer_code']
                       }
        due_days = df['Due_Days']
        default_vale = 0
        if (due_days <= 30):
            outstanding[head_columns[10]] = df['balance_amount']
        else:
            outstanding[head_columns[10]] = default_vale

        if (due_days > 30 and due_days <= 45):
            outstanding[head_columns[11]] = df['balance_amount']
        else:
            outstanding[head_columns[11]] = default_vale

        if (due_days > 45 and due_days <= 60):
            outstanding[head_columns[12]] = df['balance_amount']
        else:
            outstanding[head_columns[12]] = default_vale

        if (due_days > 60 and due_days <= 75):
            outstanding[head_columns[13]] = df['balance_amount']
        else:
            outstanding[head_columns[13]] = default_vale

        if (due_days > 75 and due_days <= 90):
            outstanding[head_columns[14]] = df['balance_amount']
        else:
            outstanding[head_columns[14]] = default_vale

        if (due_days > 90 and due_days <= 120):
            outstanding[head_columns[15]] = df['balance_amount']
        else:
            outstanding[head_columns[15]] = default_vale

        if (due_days > 120 and due_days <= 150):
            outstanding[head_columns[16]] = df['balance_amount']
        else:
            outstanding[head_columns[16]] = default_vale
        if (due_days > 150 and due_days <= 180):
            outstanding[head_columns[17]] = df['balance_amount']
        else:
            outstanding[head_columns[17]] = default_vale
        if (due_days > 180):
            outstanding[head_columns[18]] = df['balance_amount']
        else:
            outstanding[head_columns[18]] = default_vale
        outstanding[head_columns[19]] = df['last_paid_date']
        outstanding[head_columns[20]] = df['last_paid_amount']
        outstanding[head_columns[21]] = df['aging_days']
        outstanding[head_columns[22]] = df['employee_name']
        # outstanding[bhead_columns[14]] = df['paymentamt']
        # outstanding[head_columns[15]] = df['lastpmtdate']
        # outstanding[head_columns[16]] = df['aging']

        outstandingList.append(outstanding)
    df_data = pd.DataFrame(outstandingList)
    if df_data.empty:
        df_data = pd.DataFrame(columns=head_columns)
    df_data = df_data[head_columns]
    return df_data


def get_Attendance_MIS(request):
    try:
        objdata = mPurchase.PurchaseModel()
        get_values = request.GET
        data = json.dumps(get_values)
        final_data = json.loads(data)
        from_date = final_data.get("from_dates1")
        to_date = final_data.get("to_dates1")
        objdata.Type = 'OUTSTANDING_PRODUCTIVITY'
        objdata.SubType = 'ATTENDANCE'
        jsondata = {
            'Filter': {"From_Date": from_date, "To_Date": to_date}
        }
        Filter = jsondata.get('Filter')
        objdata.Filter = json.dumps(Filter)
        objdata.json_classification = json.dumps({"Entity_Gid": decry_data(request.session['Entity_gid'])})
        XLSX_MIME = 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        response = HttpResponse(content_type=XLSX_MIME)
        filename = Excelfilename('Attendance Details_')
        response['Content-Disposition'] = 'attachment; filename="{}"'.format(filename)
        workbook = Workbook(response, {'in_memory': True})
        writer = pd.ExcelWriter(response, engine='xlsxwriter')
        writer.book = workbook
        df_view = objdata.get_attendance_mis()
        final_df = df_view[['employee_gid', 'employee_name', 'tot', 'workingdays', 'noofcust', 'schdate']]
        final_df1 = df_view[['employee_gid', 'employee_name', 'tot', 'workingdays']]
        final_df1.columns = ['Employee_Gid', 'Employee Name', 'Present Days', 'Working Days']
        final_df.columns = ['Employee_Gid', 'Employee Name', 'Present Days', 'Working Days', 'noofcust', 'schdate']
        final_df2 = final_df1.groupby(['Employee_Gid']).size().reset_index(name='count')
        final_df1.drop_duplicates(subset="Employee Name",
                                  keep='first', inplace=True)
        final_df1.sort_values("Employee Name", axis=0, ascending=True, inplace=True)
        table = pd.pivot_table(final_df, values='noofcust',
                               index=['Employee Name', 'Present Days', 'Working Days'],
                               columns=['schdate'], aggfunc=np.sum, fill_value=0)
        for i, row in final_df1.iterrows():
            for j, row2 in final_df2.iterrows():
                if row['Employee_Gid'] == row2['Employee_Gid']:
                    final_df1.at[i, 'Present Days'] = row2['count']
        table['Grand_Total'] = table.iloc[:, :].sum(1)
        final_df1.drop(["Employee_Gid"], axis=1, inplace=True)
        details = pd.DataFrame(final_df1, columns=['Followup Date'], index=['f'])
        rslt_df = details.sort_values(by=['Followup Date'])
        final_df1.to_excel(writer, sheet_name='Attendance Details', startrow=1, startcol=0,
                           index=False)
        table.to_excel(writer, sheet_name='Attendance Details', startrow=1,
                       startcol=3, index=False)
        rslt_df.to_excel(writer, sheet_name='Attendance Details', startrow=0,
                         startcol=3, index=False)
        writer.save()
        return response
    except Exception as e:
        return JsonResponse({"MESSAGE": "ERROR_OCCURED", "DATA": str(e)})


def get_FollowUp_MIS(request):
    utl.check_authorization(request)
    utl.check_pointaccess(request)
    try:
        objdata = mPurchase.PurchaseModel()
        get_values = request.GET
        data = json.dumps(get_values)
        final_data = json.loads(data)
        objdata.Type = 'Follow_up120'
        objdata.SubType = 'Payment'
        objdata.data = {
            'From_Date': '',
            'To_Date': ''
        }
        # objdata.jsonData = json.dumps('data')
        objdata.json_classification = json.dumps({"Entity_Gid": decry_data(request.session['Entity_gid'])})
        XLSX_MIME = 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        response = HttpResponse(content_type=XLSX_MIME)
        filename = Excelfilename('FollowUp120 Details_')
        response['Content-Disposition'] = 'attachment; filename="{}"'.format(filename)
        writer = pd.ExcelWriter(response, engine='xlsxwriter')
        df_view = objdata.get_followup_mis()
        objdata1 = mPurchase.PurchaseModel()
        get_values = request.GET
        data = json.dumps(get_values)
        final_data = json.loads(data)
        objdata1.Type = 'Follow_up120_count'
        objdata1.SubType = 'Payment_count'
        objdata1.data = {
            'From_Date': '',
            'To_Date': ''
        }
        objdata1.jsonData = json.dumps('data')
        objdata1.json_classification = json.dumps({"Entity_Gid": decry_data(request.session['Entity_gid'])})
        XLSX_MIME = 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        response = HttpResponse(content_type=XLSX_MIME)
        filename = Excelfilename('FollowUp120 Details_')
        response['Content-Disposition'] = 'attachment; filename="{}"'.format(filename)
        writer = pd.ExcelWriter(response, engine='xlsxwriter')
        df_view1 = objdata1.get_followup_mis()

        final_df = df_view[
            ['customer_name', 'customer_code', 'location_name', 'employee_name', 'emphourtrack_date', 'due_amount',
             'Due_Days', 'followup']]
        final_df.columns = ['Customer Name', 'Customer Code', 'Location', 'Employee Name', 'Emphourtrack Date',
                            'Due Amount', 'Due Days', 'Followup']
        final_df.to_excel(writer, sheet_name='FollowUp Details', index=False)

        final_dff = df_view1[
            ['employee_name', 'sumofdueyes', 'sumofduenos', 'followup', 'countofcust']]
        final_dff.columns = ['Employee Name', 'Sum of Due-Yes', 'Sum of Due-nos', 'Followup', 'Count of Customers']
        final_dff.to_excel(writer, sheet_name='Followup total count', index=False)

        writer.save()
        return response


    except Exception as e:
        return JsonResponse({"MESSAGE": "ERROR_OCCURED", "DATA": str(e)})


def get_FollowUp_90_MIS(request):
    utl.check_authorization(request)
    utl.check_pointaccess(request)
    try:
        objdata = mPurchase.PurchaseModel()
        get_values = request.GET
        data = json.dumps(get_values)
        final_data = json.loads(data)
        objdata.Type = 'Follow_up90'
        objdata.SubType = 'Payment'
        objdata.data = {
            'From_Date': '',
            'To_Date': ''
        }
        # objdata.jsonData = json.dumps('data')
        objdata.json_classification = json.dumps({"Entity_Gid": decry_data(request.session['Entity_gid'])})
        XLSX_MIME = 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        response = HttpResponse(content_type=XLSX_MIME)
        filename = Excelfilename('FollowUp90 Details_')
        response['Content-Disposition'] = 'attachment; filename="{}"'.format(filename)
        writer = pd.ExcelWriter(response, engine='xlsxwriter')
        df_view = objdata.get_followup90_mis()
        objdata1 = mPurchase.PurchaseModel()
        get_values = request.GET
        data = json.dumps(get_values)
        final_data = json.loads(data)
        objdata1.Type = 'Follow_up90_count'
        objdata1.SubType = 'Payment_count'
        objdata1.data = {
            'From_Date': '',
            'To_Date': ''
        }
        # objdata1.jsonData = json.dumps('data')
        objdata1.json_classification = json.dumps({"Entity_Gid": decry_data(request.session['Entity_gid'])})
        XLSX_MIME = 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        response = HttpResponse(content_type=XLSX_MIME)
        filename = Excelfilename('FollowUp90 Details_')
        response['Content-Disposition'] = 'attachment; filename="{}"'.format(filename)
        writer = pd.ExcelWriter(response, engine='xlsxwriter')
        df_view1 = objdata1.get_followup90_mis()

        final_df = df_view[
            ['customer_name', 'customer_code', 'location_name', 'employee_name', 'emphourtrack_date', 'due_amount',
             'Due_Days', 'followup']]
        final_df.columns = ['Customer Name', 'Customer Code', 'Location', 'Employee Name', 'Emphourtrack Date',
                            'Due Amount', 'Due Days', 'Followup']

        final_df.to_excel(writer, sheet_name='FollowUp Details', index=False)

        final_dff = df_view1[
            ['employee_name', 'sumofdueyes', 'sumofduenos', 'followup', 'countofcust']]
        final_dff.columns = ['Employee Name', 'Sum of Due-Yes', 'Sum of Due-nos', 'Followup', 'Count of Customers']
        # final_dff.loc["Total"] = final_dff['Sum of Due-Yes'].sum()
        # final_dff.loc["Total"] = final_dff['Sum of Due-nos'].sum()

        final_dff.to_excel(writer, sheet_name='Followup total count', index=False)

        writer.save()
        return response


    except Exception as e:
        return JsonResponse({"MESSAGE": "ERROR_OCCURED", "DATA": str(e)})


def get_FollowUp_60_MIS(request):
    utl.check_authorization(request)
    utl.check_pointaccess(request)
    try:
        objdata = mPurchase.PurchaseModel()
        get_values = request.GET
        data = json.dumps(get_values)
        final_data = json.loads(data)
        objdata.Type = 'Follow_up60'
        objdata.SubType = 'Payment'
        objdata.data = {
            'From_Date': '',
            'To_Date': ''
        }
        # objdata.jsonData = json.dumps('data')
        objdata.json_classification = json.dumps({'Entity_Gid': [1]})
        XLSX_MIME = 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        response = HttpResponse(content_type=XLSX_MIME)
        x = datetime.datetime.now()
        y = "FollowUp Details_" + (x.strftime("%c")) + '.xlsx'
        response['Content-Disposition'] = 'attachment; filename="{}"'.format(y)
        # response['Content-Disposition'] = 'attachment; filename="FollowUp Details.xlsx"'
        writer = pd.ExcelWriter(response, engine='xlsxwriter')
        df_view = objdata.get_followup60_mis()
        objdata1 = mPurchase.PurchaseModel()
        get_values = request.GET
        data = json.dumps(get_values)
        final_data = json.loads(data)
        objdata1.Type = 'Follow_up60_count'
        objdata1.SubType = 'Payment_count'
        objdata1.data = {
            'From_Date': '',
            'To_Date': ''
        }
        # objdata1.jsonData = json.dumps('data')
        objdata1.json_classification = json.dumps({'Entity_Gid': [1]})
        XLSX_MIME = 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        response = HttpResponse(content_type=XLSX_MIME)
        x = datetime.datetime.now()
        y = "FollowUp Details_" + (x.strftime("%c")) + '.xlsx'
        response['Content-Disposition'] = 'attachment; filename="{}"'.format(y)
        # response['Content-Disposition'] = 'attachment; filename="FollowUp Details.xlsx"'
        writer = pd.ExcelWriter(response, engine='xlsxwriter')
        df_view1 = objdata1.get_followup60_mis()

        final_df = df_view[
            ['customer_name', 'customer_code', 'location_name', 'employee_name', 'emphourtrack_date', 'due_amount',
             'Due_Days', 'followup']]
        final_df.columns = ['Customer Name', 'Customer Code', 'Location', 'Employee Name', 'Emphourtrack Date',
                            'Due Amount', 'Due Days', 'Followup']

        final_df.to_excel(writer, sheet_name='FollowUp Details', index=False)

        final_dff = df_view1[
            ['employee_name', 'sumofdueyes', 'sumofduenos', 'followup', 'countofcust']]
        final_dff.columns = ['Employee Name', 'Sum of Due-Yes', 'Sum of Due-nos', 'Followup', 'Count of Customers']
        # final_dff.loc["Total"] = final_dff['Sum of Due-Yes'].sum()
        # final_dff.loc["Total"] = final_dff['Sum of Due-nos'].sum()

        final_dff.to_excel(writer, sheet_name='Followup total count', index=False)

        writer.save()
        return response


    except Exception as e:
        return JsonResponse({"MESSAGE": "ERROR_OCCURED", "DATA": str(e)})


def get_Chequesinclear_MIS(request):
    utl.check_authorization(request)
    utl.check_pointaccess(request)
    try:
        objdata = mPurchase.PurchaseModel()
        get_values = request.GET
        data = json.dumps(get_values)
        final_data = json.loads(data)
        objdata.Action = 'Summary'
        objdata.Type = ''
        objdata.data = {
            'From_Date': '',
            'To_Date': ''
        }

        objdata.json_classification = json.dumps({"Entity_Gid": decry_data(request.session['Entity_gid'])})
        objdata.ls_create_by = 1
        XLSX_MIME = 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        response = HttpResponse(content_type=XLSX_MIME)
        # response['Content-Disposition'] = 'attachment; filename="Cheque Details.xlsx"'
        filename = Excelfilename('Cheque Details_')
        response['Content-Disposition'] = 'attachment; filename="{}"'.format(filename)
        workbook = Workbook(response, {'in_memory': True})
        writer = pd.ExcelWriter(response, engine='xlsxwriter')
        writer.book = workbook
        df_view = objdata.get_cheques_mis()
        objdata1 = mPurchase.PurchaseModel()
        get_values = request.GET
        data = json.dumps(get_values)
        final_data = json.loads(data)
        objdata1.Action = 'Summary1'
        objdata1.Type = 'Day_Aft_Tomor'
        objdata1.data = {
            'From_Date': '',
            'To_Date': ''
        }

        objdata1.json_classification = json.dumps({"Entity_Gid": decry_data(request.session['Entity_gid'])})
        objdata1.ls_create_by = 1
        XLSX_MIME = 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        response = HttpResponse(content_type=XLSX_MIME)
        filename = Excelfilename('Cheque Details_')
        response['Content-Disposition'] = 'attachment; filename="{}"'.format(filename)

        # output = io.BytesIO()

        # workbook = Workbook(output, {'in_memory': True})
        writer = pd.ExcelWriter(response, engine='xlsxwriter')
        # writer.book = workbook

        df_view1 = objdata1.get_cheques_mis()

        objdata2 = mPurchase.PurchaseModel()
        get_values = request.GET
        data = json.dumps(get_values)
        final_data = json.loads(data)
        objdata2.Action = 'Summary2'
        objdata2.Type = 'Day_After'
        objdata2.data = {
            'From_Date': '',
            'To_Date': ''
        }

        objdata2.json_classification = json.dumps({"Entity_Gid": decry_data(request.session['Entity_gid'])})
        objdata2.ls_create_by = 1
        XLSX_MIME = 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        response = HttpResponse(content_type=XLSX_MIME)
        x = datetime.datetime.now()
        filename = Excelfilename('Cheque Details_')
        response['Content-Disposition'] = 'attachment; filename="{}"'.format(filename)
        writer = pd.ExcelWriter(response, engine='xlsxwriter')

        df_view2 = objdata2.get_cheques_mis()

        objdata3 = mPurchase.PurchaseModel()
        get_values = request.GET
        data = json.dumps(get_values)
        final_data = json.loads(data)
        objdata3.Action = 'Summary3'
        objdata3.Type = 'Deposit_Today'
        objdata3.data = {
            'From_Date': '',
            'To_Date': ''
        }

        objdata3.json_classification = json.dumps({"Entity_Gid": decry_data(request.session['Entity_gid'])})
        objdata3.ls_create_by = 1
        XLSX_MIME = 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        response = HttpResponse(content_type=XLSX_MIME)
        filename = Excelfilename('Cheque Details_')
        response['Content-Disposition'] = 'attachment; filename="{}"'.format(filename)
        # response['Content-Disposition'] = 'attachment; filename="Cheque Details.xlsx"'
        writer = pd.ExcelWriter(response, engine='xlsxwriter')

        df_view3 = objdata3.get_cheques_mis()

        objdata4 = mPurchase.PurchaseModel()
        get_values = request.GET
        data = json.dumps(get_values)
        final_data = json.loads(data)
        objdata4.Action = 'Summary4'
        objdata4.Type = 'Deposit_Yesterdy'
        objdata4.data = {
            'From_Date': '',
            'To_Date': ''
        }

        objdata4.json_classification = json.dumps({"Entity_Gid": decry_data(request.session['Entity_gid'])})
        objdata4.ls_create_by = 1
        XLSX_MIME = 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        response = HttpResponse(content_type=XLSX_MIME)
        filename = Excelfilename('Cheque Details_')
        response['Content-Disposition'] = 'attachment; filename="{}"'.format(filename)
        writer = pd.ExcelWriter(response, engine='xlsxwriter')
        # writer.book = workbook

        df_view4 = objdata4.get_cheques_mis()

        objdata5 = mPurchase.PurchaseModel()
        get_values = request.GET
        data = json.dumps(get_values)
        final_data = json.loads(data)
        objdata5.Action = 'Summary5'
        objdata5.Type = 'Collections_Today'
        objdata5.data = {
            'From_Date': '',
            'To_Date': ''
        }

        objdata5.json_classification = json.dumps({"Entity_Gid": decry_data(request.session['Entity_gid'])})
        objdata5.ls_create_by = 1
        XLSX_MIME = 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        response = HttpResponse(content_type=XLSX_MIME)
        filename = Excelfilename('Cheque Details_')
        response['Content-Disposition'] = 'attachment; filename="{}"'.format(filename)
        writer = pd.ExcelWriter(response, engine='xlsxwriter')
        df_view5 = objdata5.get_cheques_mis()
        final_df = df_view[
            ['Description', 'Expected_Date', 'Value', 'Funds_Expected']]

        final_df.columns = ['Description', 'Expected_Date', 'Value', 'Funds_Expected']
        total_row_count = len(final_df.index) + 3
        column_count = len(final_df.index) - 1
        final_df.index = range(1, len(final_df) + 1)
        final_df.to_excel(writer, sheet_name='Cheque Details', startrow=6, startcol=0, index=True, index_label='S.No')
        ws = writer.sheets['Cheque Details']
        header_format = utility.headerFormat(workbook)
        ws.merge_range(5, 0, 5, column_count, 'FUTURE CLEARING CHEQUE DETAILS', header_format)
        final_df1 = df_view1[
            ['customer_name', 'Collection_Date', 'collected_by', 'deposit_date', 'deposited_by',
             'deposited_amt', 'Funds_expDt', 'Comments']
        ]
        final_df1.columns = ['customer_name', 'Collection_Date', 'collected_by', 'deposit_date', 'deposited_by',
                             'deposited_amt',
                             'Funds_expDt', 'Comments']

        total_row_count = len(final_df1.index) + 3
        column_count = len(final_df.index) - 1
        final_df1.loc['Total'] = pd.Series(final_df1['deposited_amt'].sum(), index=['deposited_amt'])
        final_df1.index = range(1, len(final_df1) + 1)
        final_df1.to_excel(writer, sheet_name='Cheque Details', startrow=15, startcol=0, index=True, index_label='S.No')
        header_format = utility.headerFormat(workbook)
        ws.merge_range(14, 0, 14, 8, 'CHEQUES EXPECTED TO BE DEPOSITED DAY AFTER TOMORROW', header_format)

        final_df2 = df_view2[
            ['customer_name', 'Collection_Date', 'collected_by', 'deposit_date', 'deposited_by',
             'deposited_amt', 'Funds_expDt', 'Comments']
        ]

        final_df2.loc['Total'] = pd.Series(final_df2['deposited_amt'].sum(), index=['deposited_amt'])
        final_df2.columns = ['customer_name', 'Collection_Date', 'collected_by', 'deposit_date', 'deposited_by',
                             'deposited_amt', 'Funds_expDt', 'Comments']

        final_df2.index = range(1, len(final_df2) + 1)

        final_df2.to_excel(writer, sheet_name='Cheque Details', startrow=25, startcol=0, index=True
                           , index_label='S.No'
                           )
        header_format = utility.headerFormat(workbook)

        ws.merge_range(24, 0, 24, 8, 'CHEQUES EXPECTED TO BE DEPOSITED TOMORROW', header_format)

        final_df3 = df_view3[
            ['customer_name', 'Collection_Date', 'collected_by', 'deposit_date', 'deposited_by',
             'deposited_amt', 'Funds_expDt', 'Comments']
        ]
        final_df3.columns = ['customer_name', 'Collection_Date', 'collected_by', 'deposit_date', 'deposited_by',
                             'deposited_amt', 'Funds_expDt', 'Comments']
        final_df3.loc['Total'] = pd.Series(final_df3['deposited_amt'].sum(), index=['deposited_amt'])
        final_df3.index = range(1, len(final_df3) + 1)

        final_df3.to_excel(writer, sheet_name='Cheque Details', startrow=40, startcol=0, index=True, index_label='S.No'
                           )

        header_format = utility.headerFormat(workbook)

        ws.merge_range(39, 0, 39, 8,
                       'CHEQUES DEPOSITED TODAY EXPECTED TO BE  -IN CLEARING STATUS TOMORROW OR DAY AFTER',
                       header_format)

        final_df4 = df_view4[
            ['customer_name', 'Collection_Date', 'collected_by', 'deposit_date', 'deposited_by',
             'deposited_amt', 'Funds_expDt', 'Comments']
        ]
        final_df4.columns = ['customer_name', 'Collection_Date', 'collected_by', 'deposit_date', 'deposited_by',
                             'deposited_amt', 'Funds_expDt', 'Comments']
        final_df4.loc['Total'] = pd.Series(final_df4['deposited_amt'].sum(), index=['deposited_amt'])

        final_df4.index = range(1, len(final_df4) + 1)
        final_df4.to_excel(writer, sheet_name='Cheque Details', startrow=55, startcol=0, index=True, index_label='S.No'
                           )

        header_format = utility.headerFormat(workbook)

        ws.merge_range(54, 0, 54, 8, 'CHEQUES DEPOSITED TODAY OR EARLIER EXPECTED TO BE  -IN CLEARING STATUS TOMORROW',
                       header_format)

        final_df5 = df_view5[
            ['customer_name', 'Collection_Date', 'collected_by', 'deposit_date', 'deposited_by',
             'deposited_amt', 'Funds_expDt', 'Comments']
        ]
        final_df5.columns = ['customer_name', 'Collection_Date', 'collected_by', 'deposit_date', 'deposited_by',
                             'deposited_amt', 'Funds_expDt', 'Comments']
        final_df5.loc['Total'] = pd.Series(final_df5['deposited_amt'].sum(), index=['deposited_amt'])

        final_df5.index = range(1, len(final_df5) + 1)
        final_df5.to_excel(writer, sheet_name='Cheque Details', startrow=70, startcol=0, index=True, index_label='S.No',
                           header=69)
        header_format = utility.headerFormat(workbook)
        ws.merge_range(69, 0, 69, 8, 'TODAYS COLLECTION', header_format)
        writer.save()
        return response


    except Exception as e:
        return JsonResponse({"MESSAGE": "ERROR_OCCURED", "DATA": str(e)})


def get_Outstanding_comparison(request):
    if request.method == 'POST':
        objdata = mPurchase.PurchaseModel()
        jsondata = json.loads(request.body.decode('utf-8'))
        objdata.type = jsondata.get('Type')
        objdata.sub_type = jsondata.get('SubType')
        objdata.jsondata = json.dumps({'Entity_Gid': 1})
        df2 = objdata.get_Outstanding_comparison()
        # jdata = obj_cancel_data.to_json(orient='records')
        # data=jdata
        objdata.type = 'OUTSTANDING_COMPARISON'
        objdata.sub_type = 'BUCKETNEW'
        objdata.jsondata = json.dumps({'Entity_Gid': 1})
        df1 = objdata.get_Outstanding_comparison()
        # jdata = obj_cancel_data.to_json(orient='records')
        # data1=jdata
        # return JsonResponse(json.loads(jdata), safe=False)
        objdata.type = 'OUTSTANDING_COMPARISON'
        objdata.sub_type = 'BUCKETPAYMENT'
        objdata.jsondata = json.dumps({'Entity_Gid': 1})
        df3 = objdata.get_Outstanding_comparison()
        df3['payment_120'] = pd.to_numeric(df3['payment_120'], errors='coerce')
        df3['payment_90'] = pd.to_numeric(df3['payment_90'], errors='coerce')

        # Main logic
        for i, row in df1.iterrows():
            for j, row2 in df2.iterrows():
                if row['fetsoutstanding_invoiceno'] == row2['fetsoutstanding_invoiceno']:  # compare with invoice number
                    df1.at[i, 'old_90'] = row2['old_90']  # add old 90 in df1 with value
                    df1.at[i, 'old_120'] = row2['old_120']
            for k, row3 in df3.iterrows():
                if row['fetsoutstanding_invoiceno'] == row3['fetsoutstanding_invoiceno']:
                    df1.at[i, 'payment_90'] = row3['payment_90']
                    df1.at[i, 'payment_120'] = row3['payment_120']
        df1 = df1.fillna(value='')

        # change new 90 and 120 as old 90 and old 120
        for i, row in df1.iterrows():
            if row['old_90'] == '':
                df1.at[i, 'old_90'] = row['BillAmount_90']
            if row['old_120'] == '':
                df1.at[i, 'old_120'] = row['BillAmount_120']
        df1 = df1[['CustomerName', 'EmployeeName', 'old_90', 'old_120', 'new_90',
                   'new_120', 'payment_90', 'payment_120']]

        return JsonResponse(json.loads(df1.to_json(orient='records')), safe=False)


# def outstandingExcel(request):
#     utl.check_authorization(request)
#     utl.check_pointaccess(request)
#     if request.method == 'GET':
#
#         employee_gid = request.GET['employee_gid']
#
#         head_columns = ['S.No', 'Customer Name', 'Location', 'Invoice No', 'Invoice Date', 'Quantity', 'Bill Amount'
#
#             , 'Due Amount', 'Due Days','Credit Days', '< 30', '30 - 45', '45 - 60', '60 - 75', '75 - 90', '90 - 120', '120 - 150',
#
#                         '150 - 180', '> 180', 'Last pmt Date', 'Payment Amt', 'Aging Days', 'Employee Name', 'Bpayment']
#
#         bhead_columns = ['S.No', 'Customer Name', 'Employee Name', 'Bill Amount'
#
#             , 'Due Amount', '< 30', '30 - 45', '45 - 60', '60 - 75', '75 - 90', '90 - 120', '120 - 150',
#
#                          '150 - 180', '> 180', 'Bpayment']
#
#         df_data = getOutstandingDetails(employee_gid)
#
#         df_group = df_data
#         df_group = df_data[['Customer Name', 'Quantity', 'Bill Amount', 'Due Amount',
#                             'Due Days', '< 30', '30 - 45', '45 - 60', '60 - 75',
#                             '75 - 90', '90 - 120',
#                             '120 - 150', '150 - 180', '> 180',
#                             ]].groupby('Customer Name').sum().reset_index()
#
#         df_group = df_group.drop(['Bpayment'], axis=1)
#         df_group['Bpayment'] = 0
#         df_group['Employee Name'] = ''
#         for i, row1 in df_group.iterrows():
#             for j, row2 in df_data.iterrows():
#                 if row2['Customer Name'] == row1['Customer Name']:
#                     df_group.at[i, 'Employee Name'] = row2['Employee Name']
#                     if row1['Bpayment'] != row2['Payment Amt']:
#                         df_group.at[i, 'Bpayment'] = row2['Payment Amt']
#
#         df_data = df_data.drop(['Bpayment', 'Blastpayment', 'Baging'], axis=1)
#         payment19 = df_data['Payment Amt'].sum()
#
#         df_group = df_group.reset_index()
#         df_group.index = range(1, len(df_group) + 1)
#         total_row_count = len(df_data.index) + 3
#         column_count = len(df_data.columns) - 1
#         btotal_row_count = len(df_group.index) + 3
#         bcolumn_count = len(df_group.columns)
#         XLSX_MIME = 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
#         response = HttpResponse(content_type=XLSX_MIME)
#         response['Content-Disposition'] = 'attachment; filename="OutstandingReport.xlsx"'
#         writer = pd.ExcelWriter(response, engine='xlsxwriter')
#         workbook = writer.book
#         df_data.to_excel(writer, sheet_name='OutstandingReport', startrow=3, startcol=0, index=False
#                          , freeze_panes=(4, 0)
#                          )
#         df_group.to_excel(writer, sheet_name='Branchwise', startrow=3, startcol=0, index=True, index_label='S.No'
#                           , freeze_panes=(4, 0))
#
#         if employee_gid != 0:
#             header_text = request.GET['employee_name']
#
#         if employee_gid == '0':
#             header_text = 'ALL Employee'
#         ws = writer.sheets['OutstandingReport']
#
#         header_format = utility.headerFormat(workbook)
#         subheader_format = utility.subHeaderFormat(workbook)
#         ws.merge_range(2, 4, 2, column_count, header_text, subheader_format)
#         ws.merge_range(0, 0, 0, column_count, 'VSOLV ENGINEERING INDIA PVT LTD', header_format)
#         ws.merge_range(1, 0, 1, column_count, 'CUSTOMER OUTSTANDING REPORT', subheader_format)
#         ws.merge_range(2, 0, 2, 3, 'Date: ' + datetime.datetime.today().strftime("%d/%m/%Y"),
#                        subheader_format)
#         # branchwise
#
#         ws = writer.sheets['Branchwise']
#         ws.merge_range(2, 4, 2, column_count, header_text, subheader_format)
#         ws.merge_range(0, 0, 0, bcolumn_count, 'VSOLV ENGINEERING INDIA PVT LTD', header_format)
#         ws.merge_range(1, 0, 1, bcolumn_count
#                        , 'CUSTOMER OUTSTANDING REPORT - Branchwise', subheader_format)
#         ws.merge_range(2, 0, 2, 3, 'Date: ' + datetime.datetime.today().strftime("%d/%m/%Y"),
#                        subheader_format)
#
#         writer.save()
#         workbook.close()
#         return response

def outstandingExcel(request):
    if request.method == 'GET':
        employee_gid = request.GET['employee_gid']
        head_columns = ['S.No', 'Customer Name', 'Location', 'Ref No', 'Due Date', 'Quantity', 'Bill Amount'
            , 'Due Amount', 'Due Days', 'Credit Days', '< 30', '30 - 45', '45 - 60', '60 - 75', '75 - 90', '90 - 120',
                        '120 - 150',
                        '150 - 180', '> 180', 'Last pmt Date', 'Payment Amt',
                        'Aging Days', 'Employee Name']
        # ,'Customer Code']
        # ,'paymentamt','lastpmtdate','aging']

        bhead_columns = ['S.No', 'Customer Name', 'Employee Name', 'Bill Amount'
            , 'Due Amount', '< 30', '30 - 45', '45 - 60', '60 - 75', '75 - 90', '90 - 120', '120 - 150',
                         '150 - 180', '> 180']
        df_data = getOutstandingDetails(employee_gid, request)

        df_group = df_data.groupby([head_columns[1], head_columns[22]])[
            [head_columns[6], head_columns[7], head_columns[10], head_columns[11]
                , head_columns[12], head_columns[13], head_columns[14], head_columns[15]
                , head_columns[16], head_columns[17], head_columns[18]
             # ,'paymentamt'
             ]].sum()
        # df_data = df_data.drop(['paymentamt','lastpmtdate','aging'], axis=1)
        payment19 = df_data['Payment Amt'].sum()
        # payment15=df_data['Payment Amt'].sum()
        Due7 = df_data['Due Amount'].sum()
        greater30 = df_data['< 30'].sum()
        thiry = df_data['30 - 45'].sum()
        fourtyfive = df_data['45 - 60'].sum()
        sixty = df_data['60 - 75'].sum()
        seventyfive = df_data['75 - 90'].sum()
        ninty = df_data['90 - 120'].sum()
        one20 = df_data['120 - 150'].sum()
        one50 = df_data['150 - 180'].sum()
        greter180 = df_data['> 180'].sum()
        Bill6 = df_data['Bill Amount'].sum()
        # df_group = df_data(head_columns[1]).aggregate({head_columns[6]: Total
        #                                                           , head_columns[7]: 'sum'
        #                                                           , head_columns[9]: 'sum', head_columns[10]: 'sum'
        #                                                           , head_columns[11]: 'sum', head_columns[12]: 'sum'
        #                                                           , head_columns[13]: 'sum', head_columns[14]: 'sum'
        #                                                           , head_columns[15]: 'sum', head_columns[16]: 'sum'
        #                                                           , head_columns[17]: 'sum', head_columns[18]: 'max'
        #                                                           , head_columns[19]: 'max', head_columns[20]: 'max'})
        df_group = df_group.reset_index()
        df_group.index = range(1, len(df_group) + 1)

        total_row_count = len(df_data.index) + 3
        column_count = len(df_data.columns) - 1
        btotal_row_count = len(df_group.index) + 3
        bcolumn_count = len(df_group.columns)
        # btotal_row_count = len(df_group1.index) + 3

        # bcolumn_count = len(df_group1.columns) + 2
        output = io.BytesIO()
        workbook = Workbook(output, {'in_memory': True})

        writer = pd.ExcelWriter(output, engine='xlsxwriter')

        writer.book = workbook
        df_data.to_excel(writer, sheet_name='OutstandingReport', startrow=3, startcol=0, index=False
                         , freeze_panes=(4, 0))
        df_group.to_excel(writer, sheet_name='Branchwise', startrow=3, startcol=0, index=True, index_label='S.No'
                          , freeze_panes=(4, 0))

        header = []
        tableheaderFormat = utility.tableHeader(workbook)
        for i in range(0, len(head_columns)):
            head = {'header': head_columns[i], 'header_format': tableheaderFormat}
            if (i == 5):
                head['total_string'] = 'Total'
            if (i == 6):
                head['total_string'] = str(Bill6)
            if (i == 7):
                head['total_string'] = str(Due7)
            if (i == 9):
                head['total_string'] = str(greater30)
            if (i == 10):
                head['total_string'] = str(thiry)
            if (i == 11):
                head['total_string'] = str(fourtyfive)
            if (i == 12):
                head['total_string'] = str(sixty)
            if (i == 13):
                head['total_string'] = str(seventyfive)
            if (i == 14):
                head['total_string'] = str(ninty)
            if (i == 15):
                head['total_string'] = str(one20)
            if (i == 16):
                head['total_string'] = str(one50)
            if (i == 17):
                head['total_string'] = str(greter180)
            if (i == 19):
                head['total_string'] = str(payment19)
            header.append(head)
        ws = writer.sheets['OutstandingReport']
        ws.add_table(3, 0, total_row_count + 1, column_count,
                     {'header_row': True, 'style': 'Table Style Light 2', 'banded_rows': 0, 'banded_columns': 0
                         , 'total_row': 1
                         , 'autofilter': True, 'columns': header})
        header_format = utility.headerFormat(workbook)
        subheader_format = utility.subHeaderFormat(workbook)
        ws.merge_range(0, 0, 0, column_count, 'VSOLV ENGINEERING INDIA PVT LTD', header_format)
        ws.merge_range(1, 0, 1, column_count, 'CUSTOMER OUTSTANDING REPORT', subheader_format)
        ws.merge_range(2, 0, 2, 3, 'Date: ' + datetime.today().strftime("%d/%m/%Y"),
                       subheader_format)
        if employee_gid != 0:
            header_text = request.GET['employee_name']
        if employee_gid == '0':
            header_text = 'ALL Employee'
        ws.merge_range(2, 4, 2, column_count, header_text, subheader_format)
        # ws.set_row(row=3, cell_format=tableHeader(workbook))
        number_format = utility.numberFormat(workbook)
        ws.set_column(6, 7, cell_format=number_format)
        ws.set_column(9, 17, cell_format=number_format)
        ws.set_column(19, 19, cell_format=number_format)
        # ws.set_column(3,4,None,{'hidden': True})
        ws.set_column('F:F', None, None, {'hidden': True})
        ws.set_column('G:G', None, None, {'hidden': True})


        # branchwise
        header = []
        for i in range(0, len(bhead_columns)):
            head = {'header': bhead_columns[i], 'header_format': tableheaderFormat}
            if (i == 2):
                head['total_string'] = 'Total'
            if (i == 3):
                head['total_string'] = str(Bill6)
            if (i == 4):
                head['total_string'] = str(Due7)
            if (i == 5):
                head['total_string'] = str(greater30)
            if (i == 6):
                head['total_string'] = str(thiry)
            if (i == 7):
                head['total_string'] = str(fourtyfive)
            if (i == 8):
                head['total_string'] = str(sixty)
            if (i == 9):
                head['total_string'] = str(seventyfive)
            if (i == 10):
                head['total_string'] = str(ninty)
            if (i == 11):
                head['total_string'] = str(one20)
            if (i == 12):
                head['total_string'] = str(one50)
            if (i == 13):
                head['total_string'] = str(greter180)
            # if (i == 14):
            #     head['total_string'] = str(payment15)
            header.append(head)

        ws = writer.sheets['Branchwise']
        ws.add_table(3, 0, btotal_row_count + 1, bcolumn_count,
                     {'header_row': True, 'style': 'Table Style Light 2', 'banded_rows': 0, 'banded_columns': 0
                         , 'total_row': 1
                         , 'autofilter': True, 'columns': header})
        ws.merge_range(0, 0, 0, bcolumn_count, 'VSOLV ENGINEERING INDIA PVT LTD', header_format)
        ws.merge_range(1, 0, 1, bcolumn_count
                       , 'CUSTOMER OUTSTANDING REPORT - Branchwise', subheader_format)
        ws.merge_range(2, 0, 2, 2, 'Date: ' + datetime.today().strftime("%d/%m/%Y"),
                       subheader_format)
        if employee_gid != 0:
            header_text = request.GET['employee_name']
        if employee_gid == '0':
            header_text = 'ALL Employee'
        ws.merge_range(2, 4, 2, bcolumn_count, header_text, subheader_format)
        # ws.set_column(3, 4, cell_format=number_format)
        ws.set_column(2, 2, cell_format=number_format)
        ws.set_column(11, 11, cell_format=number_format)
        ws.set_column(2, 10, cell_format=number_format)
        ws.set_column(12, 12, cell_format=number_format)
        # ws.set_column(19, 19, cell_format=number_format)
        ws.set_column('D:D', None, None, {'hidden': True})
        ws.set_column('C:C', None, None, {'hidden': True})
        writer.save()
        workbook.close()
        # XLSX_MIME = 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        # response = HttpResponse(content_type=XLSX_MIME)
        # filename = Excelfilename('FourLineMIS_')
        # response['Content-Disposition'] = 'attachment; filename="{}"'.format(filename)
        return getReponse(output, "Outstanding Report.xlsx")


def getReponse(ioStream, fileName):
    ioStream.seek(0)
    response = HttpResponse(ioStream.read(),
                            content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
    response['Content-Disposition'] = "attachment; filename=" + fileName
    ioStream.close()
    return response


def outstandingReportIndex(request):
    utl.check_authorization(request)
    return render(request, "Overall_Report.html")


def out_summary(request):
    utl.check_authorization(request)
    return render(request, "Outstanding_Summary.html")


def invoicesmryy_get(request):
    # utl.check_authorization(request)
    # utl.check_pointaccess(request)
    try:
        objdata = mPurchase.PurchaseModel()
        get_values = request.GET
        data = json.dumps(get_values)
        final_data = json.loads(data)
        from_date = final_data.get("from_date")
        # custgroupgid=final_data.get("customergroup_gid")
        objdata.type = 'OUTSTANDING_REPORT'
        objdata.subtype = 'SUMMARY'
        objdata.data = {
            'Invoice_wise': "Y",
            'Outstanding_date': from_date,
            'Employee_Gid': '',
            'Customer_Gid': '',
            'customergroup_gid': ''
        }

        objdata.json_classification = json.dumps({"Entity_Gid": decry_data(request.session['Entity_gid'])})
        # common.main_fun1(request.read(), request.path)
        XLSX_MIME = 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        response = HttpResponse(content_type=XLSX_MIME)
        obj_cancel_data = objdata.invoicesummaryy_get()
        workbook = Workbook(response, {'in_memory': True})
        filename = Excelfilename('OutstandingSummary Details_')
        response['Content-Disposition'] = 'attachment; filename="{}"'.format(filename)
        # response['Content-Disposition'] = 'attachment; filename="Invoicewise Details.xlsx"'
        writer = pd.ExcelWriter(response, engine='xlsxwriter')
        writer.book = workbook
        objdata1 = mPurchase.PurchaseModel()
        get_values = request.GET
        data = json.dumps(get_values)
        final_data = json.loads(data)
        from_date = final_data.get("from_date")
        objdata1.type = 'OUTSTANDING_REPORT'
        objdata1.subtype = 'SUMMARY'
        objdata1.data = {
            'Invoice_wise': " ",
            'Outstanding_date': from_date,
            'Employee_Gid': '',
            'Customer_Gid': '',
            'customergroup_gid': ''
        }

        objdata1.jsonData = json.dumps('data')
        # objdata1.json_classification = json.dumps({'Entity_Gid': [1]})
        objdata1.json_classification = json.dumps({"Entity_Gid": decry_data(request.session['Entity_gid'])})
        # common.main_fun1(request.read(), request.path)
        # XLSX_MIME = 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        # response = HttpResponse(content_type=XLSX_MIME)
        df_view1 = objdata1.invoicesummaryy_get()
        workbook = Workbook(response, {'in_memory': True})
        # filename = Excelfilename('OutstandingSummary Details_')
        # response['Content-Disposition'] = 'attachment; filename="{}"'.format(filename)
        # response['Content-Disposition'] = 'attachment; filename="Invoicewise Details.xlsx"'
        # writer = pd.ExcelWriter(response, engine='xlsxwriter')
        # writer.book = workbook
        final_df = obj_cancel_data[
            ['customer_name', 'employee_name', 'fetsoutstanding_invoiceno', 'fetsoutstanding_netamount',
             'paid', 'balance_amount', 'Due_Days']]

        final_df.columns = ['Customer Name', 'Executive Name', 'Invoice No', 'Bill Amount', 'Payment Amount',
                            'Due Amount', 'Due_Days']
        final_dff = df_view1[
            ['customer_name', 'employee_name', 'netamt', 'paid', 'balance_amount', 'Due_Days']]

        final_dff.columns = ['Customer Name', 'Executive Name', 'Bill Amount', 'Payment Amount',
                             'Due Amount', 'Due_Days']
        default_value = 0

        for i, row in final_dff.iterrows():
            if row['Due_Days'] <= 30 and row['Due_Days'] > 0:
                final_dff.at[i, '0-30'] = row['Due Amount']
            else:
                final_dff.at[i, '0-30'] = default_value
            if row['Due_Days'] <= 60 and row['Due_Days'] > 30:
                final_dff.at[i, '30-60'] = row['Due Amount']
            else:
                final_dff.at[i, '30-60'] = default_value
            if row['Due_Days'] <= 90 and row['Due_Days'] > 60:
                final_dff.at[i, '60-90'] = row['Due Amount']
            else:
                final_dff.at[i, '60-90'] = default_value
            if row['Due_Days'] <= 120 and row['Due_Days'] > 90:
                final_dff.at[i, '90-120'] = row['Due Amount']
            else:
                final_dff.at[i, '90-120'] = default_value
            if row['Due_Days'] >= 120:
                final_dff.at[i, '>120'] = row['Due Amount']
            else:
                final_dff.at[i, '>120'] = default_value

        for i, row in final_df.iterrows():

            if row['Due_Days'] <= 30 and row['Due_Days'] > 0:
                final_df.at[i, '0-30'] = row['Due Amount']
            else:
                final_df.at[i, '0-30'] = default_value
            if row['Due_Days'] <= 60 and row['Due_Days'] > 30:
                final_df.at[i, '30-60'] = row['Due Amount']
            else:
                final_df.at[i, '30-60'] = default_value
            if row['Due_Days'] <= 90 and row['Due_Days'] > 60:
                final_df.at[i, '60-90'] = row['Due Amount']
            else:
                final_df.at[i, '60-90'] = default_value
            if row['Due_Days'] <= 120 and row['Due_Days'] > 90:
                final_df.at[i, '90-120'] = row['Due Amount']
            else:
                final_df.at[i, '90-120'] = default_value
            if row['Due_Days'] >= 120:
                final_df.at[i, '>120'] = row['Due Amount']
            else:
                final_df.at[i, '>120'] = default_value

        final_df.to_excel(writer, sheet_name='Invoicewise Details', startrow=1, startcol=0,
                          index=False)
        final_dff.to_excel(writer, sheet_name='Branchwise Details', startrow=1, startcol=0,
                           index=False)

        writer.save()
        return response

    except Exception as e:
        return JsonResponse({"MESSAGE": "ERROR_OCCURED", "DATA": str(e)})


def invoicesmry_get(request):
    # utl.check_authorization(request)
    # utl.check_pointaccess(request)
    try:
        if request.method == 'POST':
            # token = jwt.token(request)
            objdata = mPurchase.PurchaseModel()
            jsondata = json.loads(request.body.decode('utf-8'))
            objdata.type = jsondata.get('Type')
            objdata.subtype = jsondata.get('SubType')
            objdata.json_Data = json.dumps(jsondata.get('data').get('params').get('Filter'))
            # objdata.json_classification=decry_data(request.session['Entity_gid'])
            objdata.json_classification = json.dumps({"Entity_Gid": decry_data(request.session['Entity_gid'])})
            # print(request.read())
            common.main_fun1(request.read(), request.path)
            final_df = objdata.invoicesummary_get()

            default_value = 0

            for i, row in final_df.iterrows():
                if row['Due_Days'] <= 30 and row['Due_Days'] > 0:
                    final_df.at[i, 'Due_30'] = row['balance_amount']
                else:
                    final_df.at[i, 'Due_30'] = default_value

                if row['Due_Days'] <= 60 and row['Due_Days'] > 30:
                    final_df.at[i, 'Due_60'] = row['balance_amount']

                else:
                    final_df.at[i, 'Due_60'] = default_value

                if row['Due_Days'] <= 90 and row['Due_Days'] > 60:
                    final_df.at[i, 'Due_90'] = row['balance_amount']
                else:
                    final_df.at[i, 'Due_90'] = default_value

                if row['Due_Days'] <= 120 and row['Due_Days'] > 90:
                    final_df.at[i, 'Due_120'] = row['balance_amount']
                else:
                    final_df.at[i, 'Due_120'] = default_value

                if row['Due_Days'] >= 120:
                    final_df.at[i, 'Due120'] = row['balance_amount']
                else:
                    final_df.at[i, 'Due120'] = default_value
            final_df = final_df.to_json(orient='records')
            return JsonResponse(json.loads(final_df), safe=False)
    except Exception as e:
        return JsonResponse({"MESSAGE": "ERROR_OCCURED", "DATA": str(e)})


def branchsmry_get(request):
    # utl.check_authorization(request)
    # utl.check_pointaccess(request)
    try:
        if request.method == 'POST':
            # token = jwt.token(request)
            objdata = mPurchase.PurchaseModel()
            jsondata = json.loads(request.body.decode('utf-8'))
            objdata.type = jsondata.get('Type')
            objdata.subtype = jsondata.get('SubType')
            objdata.json_Datas = json.dumps(jsondata.get('data').get('params').get('Filter'))
            objdata.json_classification = json.dumps({"Entity_Gid": decry_data(request.session['Entity_gid'])})
            common.main_fun1(request.read(), request.path)
            final_dff = objdata.branchsummary_get()
            default_value = 0
            for i, row in final_dff.iterrows():
                if row['Due_Days'] <= 30 and row['Due_Days'] > 0:
                    final_dff.at[i, 'Due_30'] = row['balance_amount']
                else:
                    final_dff.at[i, 'Due_30'] = default_value
                if row['Due_Days'] <= 60 and row['Due_Days'] > 30:
                    final_dff.at[i, 'Due_60'] = row['balance_amount']
                else:
                    final_dff.at[i, 'Due_60'] = default_value
                if row['Due_Days'] <= 90 and row['Due_Days'] > 60:
                    final_dff.at[i, 'Due_90'] = row['balance_amount']
                else:
                    final_dff.at[i, 'Due_90'] = default_value
                if row['Due_Days'] <= 120 and row['Due_Days'] > 90:
                    final_dff.at[i, 'Due_120'] = row['balance_amount']
                else:
                    final_dff.at[i, 'Due_120'] = default_value

                if row['Due_Days'] >= 120:
                    final_dff.at[i, 'Due120'] = row['balance_amount']
                else:

                    final_dff.at[i, 'Due120'] = default_value
            final_dff = final_dff.to_json(orient='records')
            return JsonResponse(json.loads(final_dff), safe=False)


    except Exception as e:
        return JsonResponse({"MESSAGE": "ERROR_OCCURED", "DATA": str(e)})


def employeename_get(request):
    # utl.check_authorization(request)
    # utl.check_pointaccess(request)
    try:
        if request.method == 'POST':
            objdata = mPurchase.PurchaseModel()
            jsondata = json.loads(request.body.decode('utf-8'))
            objdata.type = jsondata.get('action')
            objdata.subtype = jsondata.get('type')
            objdata.json_Data = json.dumps(jsondata.get('data').get('Params'))
            objdata.json_classification = json.dumps({"Entity_Gid": decry_data(request.session['Entity_gid'])})
            common.main_fun1(request.read(), request.path)
            emp_data = objdata.empname_get()
            jdata = emp_data.to_json(orient='records')
            return JsonResponse(json.loads(jdata), safe=False)
    except Exception as e:
        return JsonResponse({"MESSAGE": "ERROR_OCCURED", "DATA": str(e)})


def custgrpname_get(request):
    # utl.check_authorization(request)
    # utl.check_pointaccess(request)
    try:
        if request.method == 'POST':
            objdata = mPurchase.PurchaseModel()
            jsondata = json.loads(request.body.decode('utf-8'))
            objdata.type = jsondata.get('action')
            objdata.subtype = jsondata.get('type')
            objdata.json_Data = json.dumps(jsondata.get('data').get('Params'))
            objdata.json_classification = json.dumps({"Entity_Gid": decry_data(request.session['Entity_gid'])})
            common.main_fun1(request.read(), request.path)
            custgroup_data = objdata.custgrp_get()
            jdata = custgroup_data.to_json(orient='records')
            return JsonResponse(json.loads(jdata), safe=False)
    except Exception as e:
        return JsonResponse({"MESSAGE": "ERROR_OCCURED", "DATA": str(e)})


def custname_get(request):
    # utl.check_authorization(request)
    # utl.check_pointaccess(request)
    try:
        if request.method == 'POST':
            objdata = mPurchase.PurchaseModel()
            jsondata = json.loads(request.body.decode('utf-8'))
            objdata.type = jsondata.get('action')
            objdata.subtype = jsondata.get('type')
            objdata.jsonDatas = json.dumps(jsondata.get('data').get('Params').get('FILTER'))
            objdata.json_classification = json.dumps({"Entity_Gid": decry_data(request.session['Entity_gid'])})
            common.main_fun1(request.read(), request.path)
            custname_data = objdata.cust_get()
            # return JsonResponse(obj_cancel_data, safe=False)
            jdata = custname_data.to_json(orient='records')
            return JsonResponse(json.loads(jdata), safe=False)

    except Exception as e:
        return JsonResponse({"MESSAGE": "ERROR_OCCURED", "DATA": str(e)})


def querysummaryIndex(request):
    utl.check_authorization(request)
    return render(request, "Query_Summary.html")


# masterSyncData
# from Bigflow.Core.views import master_sync_Data_

def master_sync_get(request):
    utl.check_authorization(request)
    if request.method == 'POST':
        jsondata = json.loads(request.body.decode('utf-8'))
        type = jsondata.get('params').get('Type')
        group = jsondata.get('params').get('Group')
        action = jsondata.get('params').get('Action')
        params = {'Type': type, 'Action': action, 'Group': group}
        token = jwt.token(request)
        datas = json.dumps(jsondata)
        headers = {"content-type": "application/json", "Authorization": "" + token + ""}
        resp = requests.post("" + ip + "/Master_Sync_Data_API", params=params, data=datas, headers=headers,
                             verify=False)
        response = resp.content.decode("utf-8")
        return JsonResponse(response, safe=False)


def master_sync_employee_get(request):
    utl.check_authorization(request)
    if request.method == 'POST':
        jsondata = json.loads(request.body.decode('utf-8'))
        type = jsondata.get('params').get('Type')
        group = jsondata.get('params').get('Group')
        action = jsondata.get('params').get('Action')
        params = {'Type': type, 'Action': action, 'Group': group}
        datas = json.dumps(jsondata)
        token = jwt.token(request)
        headers = {"content-type": "application/json", "Authorization": "" + token + ""}
        resp = requests.post("" + ip + "/Master_Sync_Data_API", params=params, data=datas, headers=headers,
                             verify=False)
        response = resp.content.decode("utf-8")
        return JsonResponse(response, safe=False)


def master_sync_branch_get(request):
    utl.check_authorization(request)
    if request.method == 'POST':
        jsondata = json.loads(request.body.decode('utf-8'))
        type = jsondata.get('params').get('Type')
        group = jsondata.get('params').get('Group')
        action = jsondata.get('params').get('Action')
        params = {'Type': type, 'Action': action, 'Group': group}
        datas = json.dumps(jsondata)
        token = jwt.token(request)
        headers = {"content-type": "application/json", "Authorization": "" + token + ""}
        resp = requests.post("" + ip + "/Master_Sync_Data_API", params=params, data=datas, headers=headers,
                             verify=False)
        response = resp.content.decode("utf-8")
        return JsonResponse(response, safe=False)


def master_sync_gl_get(request):
    utl.check_authorization(request)
    if request.method == 'POST':
        jsondata = json.loads(request.body.decode('utf-8'))
        type = jsondata.get('params').get('Type')
        group = jsondata.get('params').get('Group')
        action = jsondata.get('params').get('Action')
        params = {'Type': type, 'Action': action, 'Group': group}
        datas = json.dumps(jsondata)
        token = jwt.token(request)
        headers = {"content-type": "application/json", "Authorization": "" + token + ""}
        resp = requests.post("" + ip + "/Master_Sync_Data_API", params=params, data=datas, headers=headers,
                             verify=False)
        response = resp.content.decode("utf-8")
        return JsonResponse(response, safe=False)


def report_PPR_main(request):
    return render(request, 'PPR_Report.html')


def PPR_report_url(request):
    if request.method == 'POST':
        jsondata = json.loads(request.body.decode('utf-8'))
        if (jsondata.get('Group')) == 'sector':
            grp = jsondata.get('Group')
            action = jsondata.get('Action')
            typ = jsondata.get('Group')
            params = {'Group': "" + grp + "", 'Action': "" + action + "", 'Type': "" + typ + ""}
            token = jwt.token(request)
            headers = {"content-type": "application/json", "Authorization": "" + token + ""}
            datas = json.dumps(jsondata.get('data'))
            resp = requests.post("" + ip + "/AllTableValues_Get", params=params, data=datas, headers=headers,
                                 verify=False)
            response = resp.content.decode("utf-8")
            return HttpResponse(response)

        elif (jsondata.get('Group')) == 'bussinessName':
            grp = jsondata.get('Group')
            action = jsondata.get('Action')
            typ = jsondata.get('Group')
            params = {'Group': "" + grp + "", 'Action': "" + action + "", 'Type': "" + typ + ""}
            token = jwt.token(request)
            headers = {"content-type": "application/json", "Authorization": "" + token + ""}
            datas = json.dumps(jsondata.get('data'))
            resp = requests.post("" + ip + "/AllTableValues_Get", params=params, data=datas, headers=headers,
                                 verify=False)
            response = resp.content.decode("utf-8")
            return HttpResponse(response)

        elif (jsondata.get('Group')) == 'bussinessGid':
            grp = jsondata.get('Group')
            action = jsondata.get('Action')
            typ = jsondata.get('Group')
            params = {'Group': "" + grp + "", 'Action': "" + action + "", 'Type': "" + typ + ""}
            token = jwt.token(request)
            headers = {"content-type": "application/json", "Authorization": "" + token + ""}
            datas = json.dumps(jsondata.get('data'))
            resp = requests.post("" + ip + "/AllTableValues_Get", params=params, data=datas, headers=headers,
                                 verify=False)
            response = resp.content.decode("utf-8")
            return HttpResponse(response)

        elif (jsondata.get('Group')) == 'PPR_Data':
            grp = jsondata.get('Group')
            action = jsondata.get('Action')
            typ = jsondata.get('Group')
            params = {'Group': "" + grp + "", 'Action': "" + action + "", 'Type': "" + typ + ""}
            token = jwt.token(request)
            headers = {"content-type": "application/json", "Authorization": "" + token + ""}
            datas = json.dumps(jsondata.get('data'))
            resp = requests.post("" + ip + "/PPR_Data_Get", params=params, data=datas, headers=headers, verify=False)
            response = resp.content.decode("utf-8")
            return HttpResponse(response)

        elif (jsondata.get('Group')) == 'bussinessGidname':
            grp = jsondata.get('Group')
            action = jsondata.get('Action')
            typ = jsondata.get('Group')
            params = {'Group': "" + grp + "", 'Action': "" + action + "", 'Type': "" + typ + ""}
            token = jwt.token(request)
            headers = {"content-type": "application/json", "Authorization": "" + token + ""}
            datas = json.dumps(jsondata.get('data'))
            resp = requests.post("" + ip + "/AllTableValues_Get", params=params, data=datas, headers=headers,
                                 verify=False)
            response = resp.content.decode("utf-8")
            return HttpResponse(response)


class store_ppr_XL_data:
    def __init__(self):
        self.ppr_xl_data = {}


def Generate_PPR_XL(request):
    try:
        if request.method == 'POST':
            jsondata = json.loads(request.body.decode('utf-8'))
            store_ppr_XL_data.ppr_xl_data = {}
            store_ppr_XL_data.ppr_xl_data = jsondata
            return JsonResponse({"MESSAGE": "Created"})
        elif request.method == 'GET':
            XLSX_MIME = 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
            response = HttpResponse(content_type=XLSX_MIME)
            response['Content-Disposition'] = 'attachment; filename="PPR_report.xlsx"'
            writer = pd.ExcelWriter(response, engine='xlsxwriter')
            header = pd.DataFrame([f"Profitablity Report for {store_ppr_XL_data.ppr_xl_data['M_Q']}"], columns=[""])
            header.to_excel(writer, 'Sheet1', index=False, startrow=0, startcol=0)
            filter_data_xl = pd.DataFrame(np.array(list(store_ppr_XL_data.ppr_xl_data["filter_data"].items())),
                                          columns=["Filter", "Selected"])
            filter_data_xl.to_excel(writer, 'Sheet1', index=False, startrow=4, startcol=0)
            convertTo_XL = pd.DataFrame(store_ppr_XL_data.ppr_xl_data["data"])
            convertTo_XL.to_excel(writer, 'Sheet1', index=False, startrow=13, startcol=0)
            workbook = writer.book
            worksheet = writer.sheets['Sheet1']
            fmt_header = workbook.add_format({"bold": True, "border": 5, "align": "center"})
            fmt_header_M_Q = workbook.add_format({"bold": True, "align": "center"})
            for col, value in enumerate(convertTo_XL.columns.values):
                worksheet.write(13, col, value, fmt_header)
            for col, value in enumerate(filter_data_xl.columns.values):
                worksheet.write(4, col, value, fmt_header)
            for col, value in enumerate(header.columns.values):
                worksheet.write(0, col, value, fmt_header_M_Q)
            writer.save()
            return response
    except Exception as e:
        return JsonResponse({"MESSAGE": "ERROR_OCCURED", "DATA": str(e)})


def Auto_PPR_Set_schdule():
    Current_date_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    obj = magentsummary.control()
    obj.action = "Insert"
    obj.jsonData = json.dumps({"tran_todate": str(Current_date_time)})
    obj.dataw = json.dumps({"Entity_Gid": "1", "Create_By": "0ADMIN"})
    common.logger.error([{"BEFORE_PPRDATA_AUTO_START": {
        "PPR_Auto_Schdule": str(datetime.now().strftime("%Y-%m-%d %H:%M:%S")), "Response": ""}}])
    response = obj.sp_PPR_Data_Set_frm_gen()
    common.logger.error([{"AFTER_PPRDATA_AUTO_END": {
        "PPR_Auto_Schdule": str(datetime.now().strftime("%Y-%m-%d %H:%M:%S")), "Response": str(response)}}])


sched.add_cron_job(Auto_PPR_Set_schdule, hour=7, minute=50)


# def Auto_PPR_Set_schdule():
#
#     Current_date_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
#     json_body = json.dumps({
#         "Params": {"tran_todate": str(Current_date_time)},
#         "Classification": {"Entity_Gid": "1", "Create_By": "0ADMIN"}
#     })
#     params = {"Group": "PPR_SET", "Action": "Insert", "Local": ""}
#     common.logger.error(
#         [{"BEFORE_PPRDATA_AUTO_START": {"PPR_Auto_Schdule": str(datetime.now().strftime("%Y-%m-%d %H:%M:%S")),"Response":""}}])
#     resp = requests.post("" + ip + "/PPR_Data_Set", params=params, data=json_body,
#                          verify=False)
#     response = resp.content.decode("utf-8")
#     print("sidhu",response)
#     common.logger.error([{"AFTER_PPRDATA_AUTO_END":{"PPR_Auto_Schdule":str(datetime.now().strftime("%Y-%m-%d %H:%M:%S")),"Response":str(response)}}])


# sched.add_cron_job(Auto_PPR_Set_schdule, hour=21, minute=30)
# sched.add_cron_job(Auto_PPR_Set_schdule, hour=6, minute=47)


def PPR_Schudle(request):
    try:
        if request.method == 'GET':
            Entity_gid = request.session['Entity_gid']
            Create_By = request.session['Emp_gid']
            Current_date_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            json_body = json.dumps({
                "Params": {"tran_todate": str(Current_date_time)},
                "Classification": {"Entity_Gid": Entity_gid, "Create_By": Create_By}
            })
            params = {"Group": "PPR_SET", "Action": "Insert"}
            token = jwt.token(request)
            headers = {"content-type": "application/json", "Authorization": "" + token + ""}
            common.logger.error([{"BEFORE_PPRDATA_MANUAL_END": {
                "PPR_Auto_Schdule": str(datetime.now().strftime("%Y-%m-%d %H:%M:%S")), "Response": ""}}])
            resp = requests.post("" + ip + "/PPR_Data_Set", params=params, data=json_body, headers=headers,
                                 verify=False)
            common.logger.error([{"AFTER_PPRDATA_MANUAL_END": {
                "PPR_Auto_Schdule": str(datetime.now().strftime("%Y-%m-%d %H:%M:%S")), "Response": resp}}])

            response = resp.content.decode("utf-8")
            return HttpResponse(response)
    except Exception as e:
        return JsonResponse({"MESSAGE": "ERROR_OCCURED", "DATA": str(e)})


def ppr_supplier_report(request):
    return render(request, 'PPR_Supplier_report.html')


def Budget_Summary(request):
    return render(request, 'Budget_Summary.html')


def PPR_Budget_Get_Summary(request):
    if request.method == 'POST':
        try:
            jsondata = json.loads(request.body.decode('utf-8'))
            if (jsondata.get(
                    'Group')) == 'SUMMARY' or "FinYear_Fetch" or "Sector_Fetch" or "Business_Fetch" or "Bs_Fetch" or "CC_Fetch" or "Expense_grp":
                grp = jsondata.get('Group')
                action = jsondata.get('Action')
                typ = jsondata.get('Group')
                params = {'Group': "" + grp + "", 'Action': "" + action + "", 'Type': "" + typ + ""}
                token = jwt.token(request)
                headers = {"content-type": "application/json", "Authorization": "" + token + ""}
                datas = json.dumps(jsondata.get('data'))
                resp = requests.post("" + ip + "/PPR_Budget_Get", params=params, data=datas, headers=headers,
                                     verify=False)
                response = resp.content.decode("utf-8")
                return HttpResponse(response)
        except Exception as e:
            return JsonResponse({"MESSAGE": "ERROR_OCCURED", "DATA": str(e)})


def PPR_Budget_Excel_Upload(request):
    return render(request, 'PPR_excel_upload.html')


def PPR_Budget_Upload_XL_genetate_Json(request):
    if request.method == 'POST':
        try:
            Entity_gid = request.session['Entity_gid']
            Create_By = request.session['Emp_gid']
            params = {'Group': "PPR_FIND_ALL", 'Action': "GET"}
            token = jwt.token(request)
            headers = {"content-type": "application/json", "Authorization": "" + token + ""}
            excel_data_DF = pd.read_excel(request.FILES['file'])
            column_arr = [
                'Sl. No',
                'Date',
                'Financial Year',
                'Quarter (in nos)',
                'Month (in numarical)',
                'Branch Code',
                'Sector Name',
                'Business Name',
                'BS Name',
                'CC Name',
                'Category Code',
                'Subcategory Code',
                'GL No',
                'Budget Amount'
            ]
            if column_arr == list(excel_data_DF.columns):
                Json_data_XL = excel_data_DF.drop(
                    ["Sl. No"],
                    axis=1).rename(columns={
                    "Branch Code": "Branch", "Sector Name": "Sector", "Business Name": "Bizname", "BS Name": "BS",
                    "CC Name": "CC",
                    "Category Code": "Category", "Subcategory Code": "Subcategory", "GL No": "CBSGL",
                    "Budget Amount": "Amount", "Financial Year": "Fin_year", "Quarter (in nos)": "Quarter",
                    "Month (in numarical)": "trn_month"
                }).to_json(orient="records", date_format="iso")
                print(Json_data_XL)
                datas = json.dumps({"Params": {"detail": json.loads(Json_data_XL)},
                                    "Classification": {"Entity_Gid": Entity_gid, "Create_By": Create_By}})
                resp = requests.post("" + ip + "/PPR_Budget_Get", params=params, data=datas, headers=headers,
                                     verify=False)
                response = resp.content.decode("utf-8")
                return HttpResponse(response)
            elif column_arr != list(excel_data_DF.columns):
                return JsonResponse({"MESSAGE": "Wrong Format"})
        except Exception as e:
            return JsonResponse({"MESSAGE": "ERROR_OCCURED", "DATA": str(e)})


def PPR_Buget_XL_Set(request):
    if request.method == 'POST':
        try:
            jsondata = json.loads(request.body.decode('utf-8'))
            if (jsondata.get('Group')) == 'Budget_Insert':
                grp = jsondata.get('Group')
                action = jsondata.get('Action')
                typ = jsondata.get('Group')
                params = {'Group': "" + grp + "", 'Action': "" + action + "", 'Type': "" + typ + ""}
                token = jwt.token(request)
                headers = {"content-type": "application/json", "Authorization": "" + token + ""}
                datas = json.dumps(jsondata.get('data'))
                resp = requests.post("" + ip + "/PPR_Budget_Set", params=params, data=datas, headers=headers,
                                     verify=False)
                response = resp.content.decode("utf-8")
                return HttpResponse(response)
        except Exception as e:
            return JsonResponse({"MESSAGE": "ERROR_OCCURED", "DATA": str(e)})


def Budget_builder(request):
    return render(request, 'Budget_builder.html')


def Budget_reviewer(request):
    return render(request, 'Budget_Review.html')


def Budget_approval(request):
    return render(request, 'Budget_Approval.html')

