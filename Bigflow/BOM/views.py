from django.shortcuts import render
import Bigflow
from django.http import JsonResponse
import json
from Bigflow.menuClass import utility as utl
import datetime
import pandas as pd

common = Bigflow.common
obj_master = Bigflow.mBOM.BOM()


def componentIndex(request):
    utl.check_authorization(request)
    return render(request, "componentsummary.html")


def componentRateIndex(request):
    utl.check_authorization(request)
    return render(request, "componentrate.html")

def componentSupplierRateIndex(request):
    utl.check_authorization(request)
    return render(request, "componentSupplier_Rate.html")

def compnt_get(request):
    utl.check_pointaccess(request)
    if request.method == 'GET':
        obj_master.group = request.GET['group']
        obj_master.type = request.GET['type']
        obj_master.jsonData = json.dumps({})
        obj_master.entity_gid = request.session['Entity_gid']
        df_view = obj_master.get_compnt()
        df_group = (df_view[['component_name','component_minprize','min_suppliername','component_gid']])\
            .groupby(['component_name','component_minprize','min_suppliername','component_gid']).size().reset_index();
        df_groupcustomer = (df_view[['supplier_name']]) \
            .groupby(['supplier_name']).size().reset_index();
        # df_view = (df_view[['supplier_name']])\
        #     .groupby(['supplier_name']).size().reset_index();
        supplier=[]
        for x, main in df_group.iterrows():
            df = {}
            dt = df_view[(df_view['component_gid'] == main['component_gid'])]
            supplier_detail = []
            if not dt.empty:
               for y,m in  dt.iterrows():
                    df[m["supplier_name"]]={"comprate_amount":m["comprate_amount"]}
            supplier.append(df);
        df_group['supplier']=supplier;
        jdata = df_group.to_json(orient='records')
        jdata1 = df_groupcustomer.to_json(orient='records')
        supplier_details = json.loads(jdata)
        supplier_name = json.loads(jdata1)
        data = {'supplier_details': supplier_details, 'supplier_name': supplier_name}
        return JsonResponse(data, safe=False)


def mapped_get(request):
    utl.check_pointaccess(request)
    if request.method == 'GET':
        obj_master.group = request.GET['group']
        obj_master.type = request.GET['type']
        if request.GET['jsondta'] !='0':
            obj_master.jsonData = request.GET['jsondta']
        obj_master.entity_gid = request.session['Entity_gid']
        df_view = obj_master.get_compnt()
        jdata = df_view.to_json(orient='records')
        return JsonResponse(json.loads(jdata), safe=False)


def setcomp(request):
    utl.check_pointaccess(request)
    if request.method == 'POST':
        jsondata = json.loads(request.body.decode('utf-8')).get('parms')
        obj_master.action = jsondata.get('action')
        obj_master.type = jsondata.get('type')
        obj_master.jsonData = json.dumps(jsondata.get('jsond'))
        obj_master.entity_gid = request.session['Entity_gid']
        obj_master.create_by = request.session['Emp_gid']
        out_message = outputReturn(obj_master.set_comp(), 0)
        return JsonResponse(out_message, safe=False)


def outputReturn(tubledtl, index):
    temp = tubledtl[0].split(',')
    if (len(temp) > 1):
        if (index == 0):
            return int(temp[0])
        else:
            return temp[1]
    else:
        return temp[0]
