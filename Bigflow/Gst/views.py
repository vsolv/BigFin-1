
from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
import json
from Bigflow.Gst.model import mgst
import pandas as pd
from django.conf import settings
from datetime import datetime
from django.core.files.storage import default_storage
import requests
from Bigflow.Transaction.Model import mFET, mSales
import itertools





def Gstrecon(request):
    return render(request, "Gst_Recon.html")

def Gst_MatchesSummary(request):
    return render(request, "Gst_MatchesSummary.html")

def gstexcel_set(request):
    if request.method == 'POST' and request.FILES['file']:

            gstmodel = mgst.Gst_model()
            gstmodel.name = request.POST['name']
            gstmodel.action = request.POST['Action']
            gstmodel.sub_type = 'upload'
            gstmodel.entity_gid = request.session['Entity_gid']
            gstmodel.employee_gid = request.session['Emp_gid']
            current_month = datetime.now().strftime('%m')
            current_day = datetime.now().strftime('%d')
            current_year_full = datetime.now().strftime('%Y')
            save_path = str(settings.MEDIA_ROOT)+ '/GST_File/'+str(current_year_full)+'/'+str(current_month)+'/'+str(current_day)+'/'+str(request.POST['name'])
            path = default_storage.save(str(save_path), request.FILES['file'])
            df = pd.read_excel(request.FILES['file'])
            filing_period = pd.to_datetime(df['Filing Period'], format = '%Y%m%d')
            filing_period = filing_period.apply(lambda x: x.strftime('%Y-%m-%d'))
            filing_status = df['Supplier Filing Status'].values.tolist()
            supplier_gstin = df['Supplier GSTIN'].values.tolist()
            supplier_name = df['Supplier Name'].values.tolist()
            invoice_number = df['Invoice Number'].values.tolist()
            invoice_date = pd.to_datetime(df['Invoice Date'], format = '%Y%m%d')
            invoice_date = invoice_date.apply(lambda x: x.strftime('%Y-%m-%d'))
            customer_gstin = df['Customer GSTIN'].values.tolist()
            state_code = df['Place of Supply (State Code)'].values.tolist()
            reverse_charge = df['Reverse Charge'].values.tolist()
            invoce_type = df['Invoice Type'].values.tolist()
            tax_rate = df['Tax Rate'].values.tolist()
            taxable_amount = df['Taxable Amount'].values.tolist()
            igst_amount = df['IGST Amount'].values.tolist()
            cgst_amount = df['CGST Amount'].values.tolist()
            sgst_amount = df['SGST Amount'].values.tolist()
            cess_amount = df['Cess Amount'].values.tolist()
            total = df['Total'].values.tolist()
            list_data = []
            import math
            igst_amount = [0 if math.isnan(x) else x for x in igst_amount]
            cgst_amount = [0 if math.isnan(x) else x for x in cgst_amount]
            sgst_amount = [0 if math.isnan(x) else x for x in sgst_amount]
            cess_amount = [0 if math.isnan(x) else x for x in cess_amount]
            for (filing_period, filing_status, supplier_gstin, supplier_name, invoice_number, invoice_date, customer_gstin,
                 state_code, reverse_charge, invoce_type, tax_rate, taxable_amount, igst_amount, cgst_amount, sgst_amount,
                 cess_amount, total) in itertools.zip_longest(filing_period, filing_status, supplier_gstin, supplier_name,
                                                              invoice_number, invoice_date,
                                                              customer_gstin, state_code, reverse_charge, invoce_type,
                                                              tax_rate, taxable_amount, igst_amount,
                                                              cgst_amount, sgst_amount, cess_amount, total):
               value = dict(gstupload_Filing_Period=filing_period, gstupload_Supplier_Filing_Status=filing_status,
                                                  gstupload_Supplier_GSTIN=supplier_gstin,
                                                  gstupload_Supplier_Name=supplier_name,
                                                  gstupload_Invoice_Number=invoice_number,
                                                  gstupload_Invoice_Date=invoice_date,
                                                  gstupload_Customer_GSTIN=customer_gstin,
                                                  gstupload_Place_of_Supply_StateCode=state_code,
                                                  gstupload_Reverse_Charge=reverse_charge,
                                                  gstupload_Invoice_Type=invoce_type, gstupload_Tax_Rate=tax_rate,
                                                  gstupload_Taxable_Amount=taxable_amount,
                                                  gstupload_IGST_Amount=igst_amount, gstupload_CGST_Amount=cgst_amount,
                                                  gstupload_SGST_Amount=sgst_amount, gstupload_Cess_Amount=cess_amount,
                                                  gstupload_Total=total,
                                                   gstupload_filegid=1
                                                  )
               list_data.append(value)
            gstdatadict = {}
            gstdatadict["GSTDATA"] = list_data
            gstmodel.filter_json = gstdatadict
            data = gstmodel.set_gst()
            out = outputSplit(data, 1)
            return JsonResponse(out, safe=False)

def outputSplit(tubledtl,index):
    temp=tubledtl[0].split(',')
    if(len(temp)>1):
        if (index==0):
            return int(temp[0])
        else:
            return temp[1]
    else:
        return  temp[0]



def gstsummary_get(request):
    if request.method == 'POST':
        gstmodel = mgst.Gst_model()
        jsondata = json.loads(request.body.decode('utf-8'))
        gstmodel.type =  jsondata.get('params').get('type')
        gstmodel.sub_type =  jsondata.get('params').get('sub_type')
        gstmodel.filter_json ='{"gstupload_Supplier_GSTIN":""}'
        gstmodel.entity_gid = request.session['Entity_gid']
        gstmodel.employee_gid = request.session['Emp_gid']
        data = gstmodel.get_gstsummary()
        jdata = data.to_json(orient='records')
        return JsonResponse(jdata, safe=False)


def Gstvalidate_set(request):
    if request.method == 'POST':
        gstmodel = mgst.Gst_model()
        jsondata = json.loads(request.body.decode('utf-8'))
        gstmodel.action = jsondata.get('params').get('action')
        gstmodel.sub_type =  'Validate'
        gstmodel.filter_json =   jsondata.get('params').get('filter')
        gstmodel.entity_gid = request.session['Entity_gid']
        gstmodel.employee_gid = request.session['Emp_gid']
        data =outputSplit( gstmodel.set_gst(), 1)
        return JsonResponse(data, safe=False)

def gstmatched_get(request):
    if request.method == 'POST':
        gstmodel = mgst.Gst_model()
        jsondata = json.loads(request.body.decode('utf-8'))
        gstmodel.type =  jsondata.get('params').get('type')
        gstmodel.sub_type =  jsondata.get('params').get('sub_type')
        gstmodel.filter_json ='{"gstupload_Supplier_GSTIN":""}'
        gstmodel.entity_gid = request.session['Entity_gid']
        gstmodel.employee_gid = request.session['Emp_gid']
        data = gstmodel.get_gstsummary()
        jdata = data.to_json(orient='records')
        return JsonResponse(jdata, safe=False)