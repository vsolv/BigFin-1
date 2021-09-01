import datetime
import json
import traceback
from Bigflow.menuClass import utility as utl
from django.shortcuts import render

def demo_fet(request):
    utl.check_authorization(request)
    return render(request, "DemoFet_Set.html")
def demo_fet_get(request):
    from django.http import HttpResponse
    import pandas as pd
    from django.db import connection
    cursor=connection.cursor()
    paramet=('@message',)
    cursor.callproc('sp_DemoFet_Get',paramet)
    field_names = [i[0] for i in cursor.description]
    print(field_names)
    # for record in cursor.fetchall():
    #     print(record)
    df=pd.DataFrame.from_records(list(cursor.fetchall()),columns=field_names)
    json_df=(df.to_json(orient='records'))
    return HttpResponse(str(json_df))
def demo_fet_set(request):
    import xlrd
    from django.db import connection
    from django.http.response import JsonResponse
    xfile=request.FILES['file']
    wb =  xlrd.open_workbook(file_contents=xfile.read())
    sheet = wb.sheet_by_index(0)
    cols=['Slno','Ason','Product_Type','LAN_No','Cust_ID','Cust_Name','Loan_Amt','Loan_Due_Month','Outstanding_amt','Monthly_EMI','Invoice_No','Executive_Name','Region']
    print(sheet.ncols)
    no_cols=sheet.ncols
    no_rows=sheet.nrows
    record={}
    records=[]
    try:
        for row_no in range(2,no_rows):
            for col_no in range(no_cols):
                if col_no not in (1,7):
                    record[cols[col_no]]=sheet.cell_value(row_no,col_no)
                    if (cols[col_no])=='Executive_Name':
                        if record[cols[col_no]]=='' or record[cols[col_no]]==None:
                            message="Executive Name not given for Record"
                            return JsonResponse({"MESSAGE":message})
                        pass
                else:
                    if col_no==1:
                        record[cols[col_no]]=str(datetime.datetime(*xlrd.xldate_as_tuple(sheet.cell_value(row_no,col_no), wb.datemode)))
                    else:
                        record[cols[col_no]]=str(datetime.datetime(*xlrd.xldate_as_tuple(sheet.cell_value(row_no,col_no), wb.datemode)))
            records.append(record)
            record={}
        cursor=connection.cursor()
        paramet=('INSERT',json.dumps(records),'@message')
        cursor.callproc('sp_DemoFet_Set',paramet)
        cursor.execute('select @message')
        if(cursor.fetchone()=='SUCCESS'):
            return JsonResponse({"MESSAGE":"SUCCESS"})
    except:
        traceback.print_exc()
        return JsonResponse({"MESSAGE":"FAIL"})