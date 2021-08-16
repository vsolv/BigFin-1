from django.shortcuts import render
from Bigflow.Inventory.model import mInventory
from Bigflow.Master.Model import mMasters
from Bigflow.Transaction.Model import mFET, mSales
from django.http import JsonResponse
from django.http import HttpResponse
import json
import time
import datetime
import pandas as pd
import Bigflow.Core.models as common
from Bigflow.menuClass import utility as utl

def Inventory_Index(request):
    utl.check_authorization(request)
    return render(request, "stock_inventory.html")

def Inventory_Approval(request):
    utl.check_authorization(request)
    return render(request, "Stock_Approval.html")

def Inventory_Details(request):
    utl.check_authorization(request)
    return render(request, "Stock_DetailsView.html")

def Stock_conversionSummary(request):
    utl.check_authorization(request)
    return render(request,"Stock_conversionSummary.html")


def convertDate(stringDate):
    return datetime.datetime.strptime(stringDate, "%d/%m/%Y").strftime("%Y-%m-%d")

def getstock_details(request):
    utl.check_authorization(request)
    utl.check_pointaccess(request)
    if request.method == 'POST':
        obj_stock = mInventory.Invertory_model()
        jsondata = json.loads(request.body.decode('utf-8'))
        obj_stock.action = jsondata.get('params').get('action')
        obj_stock.type = ''
        obj_stock.jsondata='{}'
        if jsondata.get('params').get('fromdate')=='':
            obj_stock.from_date =''
        else:
            obj_stock.from_date = convertDate(jsondata.get('params').get('fromdate'))
        if jsondata.get('params').get('todate') == '':
            obj_stock.to_date=''
        else:
            obj_stock.to_date =  convertDate(jsondata.get('params').get('todate'))
        obj_stock.product_gid = jsondata.get('params').get('product_gid')
        obj_stock.supplier_gid = jsondata.get('params').get('supplier_gid')
        obj_stock.entity_gid = request.session['Entity_gid']
        df_stock = obj_stock.get_stockdetails()
        jdata = df_stock.to_json(orient='records')
        return JsonResponse(json.loads(jdata), safe=False)

def outputReturn(tubledtl, index):
    temp = tubledtl[0].split(',')
    if (len(temp) > 1):
        if (index == 0):
            return int(temp[0])
        else:
            return temp[1]
    else:
        return temp[0]

def get_purrtnsmry(request):
    utl.check_authorization(request)
    utl.check_pointaccess(request)
    if request.method == 'POST':
        objdata =mInventory.Invertory_model()
        jsondata = json.loads(request.body.decode('utf-8'))
        objdata.type = jsondata.get('parms').get('ls_Type')
        objdata.sub_type = jsondata.get('parms').get('ls_Sub_Type')
        objdata.jsonData = json.dumps({'From_Date':jsondata.get('parms').get('From_Date'),
                                       "To_Date":jsondata.get('parms').get('To_Date'),
                                       "supplier_gid":jsondata.get('parms').get('supplier_gid')})
        objdata.json_classification = json.dumps({'Entity_Gid': [1]})
        obj_cancel_data = objdata.get_purrtn_smry()
        jdata = obj_cancel_data.to_json(orient='records')
        return JsonResponse(json.loads(jdata), safe=False)

def get_pur_rtnsmry(request):
        utl.check_authorization(request)
        utl.check_pointaccess(request)
        if request.method == 'POST':
            objdata = mInventory.Invertory_model()
            jsondata = json.loads(request.body.decode('utf-8'))
            objdata.type = jsondata.get('ls_Type')
            objdata.sub_type = jsondata.get('ls_Sub_Type')
            objdata.jsonData = json.dumps({"From_Date": jsondata.get('data').get('Params').get('Filter').get('From_Date'),
                                           "To_Date": jsondata.get('data').get('Params').get('Filter').get('To_Date'),
                                           "supplier_gid": jsondata.get('data').get('Params').get('Filter').get('supplier_gid')})
            objdata.json_classification = json.dumps({'Entity_Gid': [1]})
            obj_cancel_data = objdata.get_purrtn_smry()
            jdata = obj_cancel_data.to_json(orient='records')
            return JsonResponse(json.loads(jdata), safe=False)


def stockdetials_set(request):
    utl.check_authorization(request)
    utl.check_pointaccess(request)
    if request.method == 'POST':
        obj_add_stock = mInventory.Invertory_model()
        jsondata = json.loads(request.body.decode('utf-8'))
        obj_add_stock.action = jsondata.get('params').get('action')
        obj_add_stock.type = jsondata.get('params').get('type')
        obj_add_stock.jsonData =jsondata.get('params').get('jsonheader')
        obj_add_stock.jsondata='{}'
        obj_add_stock.entity_gid = request.session['Entity_gid']
        obj_add_stock.create_by =request.session['Emp_gid']
        out_message = outputReturn(obj_add_stock.set_stockdetails(), 0)
        return JsonResponse(out_message, safe=False)

def stock_sales_order_get(request):
    utl.check_authorization(request)
    utl.check_pointaccess(request)
    if request.method == 'POST':
        obj_salesget =  mSales.Sales_Model()
        jsondata = json.loads(request.body.decode('utf-8'))
        obj_salesget.action = jsondata.get('parms').get('action')
        obj_salesget.customer_gid = jsondata.get('parms').get('custid')
        obj_salesget.employee_gid = 0
        obj_salesget.date = common.convertdbDate(request.session['date'])
        obj_salesget.jsonData = json.dumps(
            {"Entity_Gid": [request.session['Entity_gid']], "Client_Gid": [jsondata.get('parms').get('Cname')]})
        if jsondata.get('parms').get('filter')=='{}':
            obj_salesget.jsondata = '{}'
        else:
            obj_salesget.jsondata=jsondata.get('parms').get('filter')
        obj_salesget.limit = 30
        setsales_order = obj_salesget.get_sales_order()
        jdata = setsales_order.to_json(orient='records')
        return JsonResponse(json.loads(jdata), safe=False)

def return_set(request):
    utl.check_authorization(request)
    utl.check_pointaccess(request)
    if request.method == 'POST':
        obj_return = mInventory.Invertory_model()
        jsondata = json.loads(request.body.decode('utf-8'))
        obj_return.action = jsondata.get('parms').get('action')
        obj_return.jsonData =jsondata.get('parms').get('jsonheader')
        obj_return.jsonData_sec = jsondata.get('parms').get('jsondetails')
        obj_return.jsondata=jsondata.get('parms').get('jsonreceipt')
        obj_return.entity_gid = request.session['Entity_gid']
        obj_return.create_by =request.session['Emp_gid']
        out_message = outputReturn(obj_return.set_recepit(), 1)
        return JsonResponse(out_message, safe=False)

def get_recepit(request):
    utl.check_authorization(request)
    utl.check_pointaccess(request)
    if request.method == 'POST':
        obj_return = mInventory.Invertory_model()
        jsondata = json.loads(request.body.decode('utf-8'))
        obj_return.action = jsondata.get('params').get('action')
        obj_return.customer_gid = jsondata.get('params').get('customer_gid')
        obj_return.supplier_gid = jsondata.get('params').get('supplier_gid')
        obj_return.receipt_gid=jsondata.get('params').get('receipt_gid')
        obj_return.receiptdetails_gid = jsondata.get('params').get('receiptdetails_gid')
        obj_return.status = jsondata.get('params').get('status')
        obj_return.entity_gid = request.session['Entity_gid']
        df_return = obj_return.get_receipt()
        jdata = df_return.to_json(orient='records')
        return JsonResponse(json.loads(jdata), safe=False)


def sales_favproduct(request):
    utl.check_authorization(request)
    utl.check_pointaccess(request)
    if request.method == 'POST':
        obj_sales_fav_pdct = mFET.FET_model()
        jsondata = json.loads(request.body.decode('utf-8'))
        obj_sales_fav_pdct.customer_gid = jsondata.get('parms').get('custid')
        obj_sales_fav_pdct.product_type = 1
        obj_sales_fav_pdct.entity_gid = request.session['Entity_gid']
        df_sales_fav_pdct = obj_sales_fav_pdct.get_sales_fav_product()
        jdata = df_sales_fav_pdct.to_json(orient='records')
        return JsonResponse(json.loads(jdata), safe=False)

def get_metadata(request):
    utl.check_authorization(request)
    utl.check_pointaccess(request)
    if request.method == 'GET':
        obj_custdata = mMasters.Masters()
        obj_custdata.table_name = request.GET['tablename']
        obj_custdata.column_name = request.GET['columnname']
        obj_custdata.entity_gid = request.session['Entity_gid']
        dict_custdata = obj_custdata.getmetadata()
        jdata = dict_custdata.to_json(orient='records')
        return JsonResponse(jdata, safe=False)


def stockconvert_set(request):
    utl.check_authorization(request)
    utl.check_pointaccess(request)
    if request.method == 'POST':
        obj_stock = mInventory.Invertory_model()
        jsondata = json.loads(request.body.decode('utf-8'))
        obj_stock.action = jsondata.get('params').get('action')
        obj_stock.jsonheader =jsondata.get('params').get('jsonheader')
        obj_stock.jsondetails =jsondata.get('params').get('jsondetails')
        obj_stock.entity_gid = request.session['Entity_gid']
        obj_stock.create_by =request.session['Emp_gid']
        out_message = outputReturn(obj_stock.set_stockconvert(), 1)
        return JsonResponse(out_message, safe=False)

def get_conversionsummary(request):
    utl.check_authorization(request)
    utl.check_pointaccess(request)
    if request.method == 'POST':
        obj_return = mInventory.Invertory_model()
        jsondata = json.loads(request.body.decode('utf-8'))
        obj_return.action = jsondata.get('params').get('action')
        obj_return.customer_gid = jsondata.get('params').get('customer_gid')
        obj_return.supplier_gid = jsondata.get('params').get('supplier_gid')
        obj_return.receipt_gid=jsondata.get('params').get('receipt_gid')
        obj_return.receiptdetails_gid = jsondata.get('params').get('receiptdetails_gid')
        obj_return.status = jsondata.get('params').get('status')
        obj_return.entity_gid = request.session['Entity_gid']
        df_return = obj_return.get_conversion()
        jdata = df_return.to_json(orient='records')
        return JsonResponse(json.loads(jdata), safe=False)

