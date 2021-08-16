import io
import pandas as pd
import numpy as np
import requests
from django.core.files.storage import default_storage
from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
import json
import Bigflow.Core.models as common
from datetime import datetime
from django.conf import settings
from django.core.files.base import ContentFile
from Bigflow.ATMA.model import mATMA
from Bigflow.eRMA.model import  mERMA
ip = common.localip()
token = common.token()
headers = {"content-type": "application/json", "Authorization": "" + token + ""}

def barcode_request(request):
    return render(request,'barcode_requestsumamry.html')

def barcode_requestadd(request):
    return render(request,'barcode_requestadd.html')
def barcodesumamry_get(request):
   if request.method == 'POST':
       jsondata = json.loads(request.body.decode('utf-8'))
       if (jsondata.get('Params').get('Group')) == 'Barcoderequest_summary':
           grp = jsondata.get('Params').get('Group')
           typ = jsondata.get('Params').get('Type')
           act = jsondata.get('Params').get('Action')
           data = json.dumps(jsondata.get('Params'))
           params = {'Group': "" + grp + "", 'Type': "" + typ + "", 'Action': "" + act + ""}
           headers = {"content-type": "application/json", "Authorization": "" + token + ""}
           datas = json.dumps(jsondata.get('Params'))
           resp = requests.post("" + ip + "/Erma_Barcode_API", params=params, data=datas, headers=headers, verify=False)
           response = resp.content.decode("utf-8")

           return HttpResponse(response)
def barcode_set(request):
   if request.method == 'POST':
       jsondata = json.loads(request.body.decode('utf-8'))
       if (jsondata.get('Params').get('Group')) == 'Barcoderequest_add':
           grp = jsondata.get('Params').get('Group')
           typ = jsondata.get('Params').get('Type')
           sub_typ = jsondata.get('Params').get('Sub_Type')
           act = jsondata.get('Params').get('Action')
           create_by = jsondata.get('Params').get('Create_By')
           create_by1 = str(create_by)
           data = json.dumps(jsondata.get('Params'))
           params = {'Group': "" + grp + "", 'Type': "" + typ + "", 'Action': "" + act + "", 'Sub_Type': "" + sub_typ + "", 'Create_By': "" + create_by1 + ""}
           headers = {"content-type": "application/json", "Authorization": "" + token + ""}
           datas = json.dumps(jsondata.get('Params'))
           resp = requests.post("" + ip + "/Erma_Barcode_API", params=params, data=datas, headers=headers, verify=False)
           response = resp.content.decode("utf-8")

           return HttpResponse(response)

def rmu2(request):
    return render(request,'rmu2.html')

def erma_archivalrequest_set(request):
   if request.method == 'POST':
       jsondata = json.loads(request.body.decode('utf-8'))
       if (jsondata.get('Group')) == 'ARCHIVAL':
           grp = jsondata.get('Group')
           action=jsondata.get('Action')
           typ = jsondata.get('Type')
           subtyp=jsondata.get('subType')
           data = json.dumps(jsondata.get('data').get('Params'))
           dataw = json.dumps(jsondata.get('data').get('Change'))
           params = {'Group': "" + grp + "", 'Action': "" + action + "", 'Type': "" + typ + "", 'subType': "" + subtyp+ ""}
           headers = {"content-type": "application/json", "Authorization": "" + token + ""}
           datas = json.dumps(jsondata.get('data'))
           resp = requests.post("" + ip + "/erma_archivalrequest_setapi", params=params, data=datas, headers=headers, verify=False)
           response = resp.content.decode("utf-8")
           return HttpResponse(response)


def excelgen1(request):
    if request.method == 'POST' and request.FILES['file']:
        try:
            current_month = datetime.now().strftime('%m')
            current_day = datetime.now().strftime('%d')
            current_year_full = datetime.now().strftime('%Y')
            save_path = str(settings.MEDIA_ROOT)+ '/Bank_Recon/'+str(current_year_full)+'/'+str(current_month)+'/'+str(current_day)+'/'+str(request.POST['name'])
            path = default_storage.save(str(save_path), ContentFile('new content'))
            path = default_storage.save(str(save_path), request.FILES['file'])

            objProductdetail = mERMA.ERMA_model()
            grp = request.POST['Group']
            objProductdetail.action = request.POST['Action']
            objProductdetail.entity_gid=1

            objProductdetail.product_gid = request.POST['product_gid']
            gid = request.POST['Gid']
            filepath = path
            name = request.POST['name']

            objProductdetail.jsonData = json.dumps({"product_gid":request.POST['product_gid']})
            objProductdetail.json_classification=json.dumps({"entity_gid":"1"})
            df=objProductdetail.ermaproductget()
            ff = df.to_dict('records')

            for eachrow in ff:
                    refno1=  eachrow['product_refno1']
                    refno2 = eachrow['product_refno2']
                    refno3 = eachrow['product_refno3']
                    refno4 = eachrow['product_refno4']
                    refno5 = eachrow['product_refno5']
                    refno6 = eachrow['product_refno6']

                    arcrefno1 = eachrow['product_arcrefno1']
                    arcrefno2 = eachrow['product_arcrefno2']
                    arcrefno3 = eachrow['product_arcrefno3']
                    arcrefno4 = eachrow['product_arcrefno4']
                    arcrefno5 = eachrow['product_arcrefno5']
                    arcrefno6 = eachrow['product_arcrefno6']

            f = request.FILES['file']
            dfarchivaldtlExcel = pd.read_excel(f, skiprows=[0], sheetname='Sheet1')

            df_cartonbarcode = dfarchivaldtlExcel['CARTON BARCODE']
            df_filebarcode = dfarchivaldtlExcel['FILE BARCODE']

            dictionary_archival= {"CartonBarcode": df_cartonbarcode, "FileBarcode": df_filebarcode}

            if refno1 != '':
                    df_refno1 = dfarchivaldtlExcel[refno1]
                    df_refno1.fillna('', inplace=True)
                    dictionary_archival[refno1]=df_refno1
            if refno2 != '':
                    df_refno2 = dfarchivaldtlExcel[refno2]
                    df_refno2.fillna('', inplace=True)
                    dictionary_archival[refno2] = df_refno2
            if refno3 != '':
                    df_refno3 = dfarchivaldtlExcel[refno3]
                    df_refno3.fillna('', inplace=True)
                    dictionary_archival[refno3] = df_refno3
            if refno4 != '':
                    df_refno4 = dfarchivaldtlExcel[refno4]
                    df_refno4.fillna('', inplace=True)
                    dictionary_archival[refno4] = df_refno4
            if refno5 != '':
                    df_refno5 = dfarchivaldtlExcel[refno5]
                    df_refno5.fillna('', inplace=True)
                    dictionary_archival[refno5] = df_refno5
            if refno6 != '':
                    df_refno6 = dfarchivaldtlExcel[refno6]
                    df_refno6.fillna('', inplace=True)
                    dictionary_archival[refno6] = df_refno6

            dfarchivaldetail=pd.DataFrame(dictionary_archival)

            archivaldtlList=[]
            for row in dfarchivaldetail.itertuples():
                cbarcode=row.__getitem__(1)
                fbarcode=row.__getitem__(2)
                remarks = ""

                objcBarcode = mERMA.ERMA_model()
                objcBarcode.jsonData = json.dumps({"BARCODENO": cbarcode,"BARCODETYPE":"CARTON BARCODE"})
                objcBarcode.json_classification=json.dumps({"Entity_Gid":"1"})
                out_message = objcBarcode.erma_getbarcode()
                if out_message.get("MESSAGE") == 'VALID':
                    remarks += ""
                else:
                    remarks += out_message.get("MESSAGE")

                objFBarcode = mERMA.ERMA_model()
                objFBarcode.jsonData = json.dumps({"BARCODENO": fbarcode, "BARCODETYPE": "FILE BARCODE"})
                objFBarcode.json_classification = json.dumps({"Entity_Gid": "1"})
                out_message = objFBarcode.erma_getbarcode()
                if out_message.get("MESSAGE") == 'VALID':
                    remarks += ""
                else:
                    remarks += out_message.get("MESSAGE")

                rowlist = [cbarcode, fbarcode]
                columnslist = ["CartonBarcode", "FileBarcode"]
                if refno1 != '':
                    columnslist.append(refno1)
                    rowlist.append(row.__getitem__(3))
                if refno2 != '':
                    columnslist.append(refno2)
                    rowlist.append(row.__getitem__(4))
                if refno3 != '':
                    columnslist.append(refno3)
                    rowlist.append(row.__getitem__(5))
                if refno4 != '':
                    columnslist.append(refno4)
                    rowlist.append(row.__getitem__(6))
                if refno5 != '':
                    columnslist.append(refno5)
                    rowlist.append(row.__getitem__(7))
                if refno6 != '':
                    columnslist.append(refno6)
                    rowlist.append(row.__getitem__(8))

                columnslist.append("Remarks")
                rowlist.append(remarks)
                archivaldtlList.append(rowlist)

            dfnew = pd.DataFrame(archivaldtlList,columns=columnslist)
            ff = dfnew.to_dict('records')
            resp=ff
            response = json.dumps(resp)
            return HttpResponse(response)
        except Exception as e:
            return JsonResponse(e, safe=False)

def barcode_assignsummary(request):
    return render(request,'barcode_assignsummary.html')

def barcode_assign(request):
    return render(request,'barcode_assign.html')

def rmu2(request):
    return render(request,'rmu2.html')

def archival_summary(request):
    return render(request,'archival_summary.html')

def Archival_details(request):
    return render(request,'Archival_details.html')