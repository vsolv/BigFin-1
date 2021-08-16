from django.db import models

# Create your models here.
def url():
    return "https://174.138.120.196/bigflowdemo/Outstanding_AR?Type=OUTSTANDING_REPORT_INVOICE_WISE&Sub_Type=BUCKET"

def params():
    type = "OUTSTANDING_REPORT_INVOICE_WISE"
    sub_type = "BUCKET"
    params = {'Type': "" + type + "", 'Sub_Type': "" + sub_type + ""}
    return params

def header():
    header = {'Authorization': 'Token 7111797114100105971106449505132'}
    return header

def data():
    data = {"parms": {
"filter":{"Employee_Gid":"21",
         "Customer_Group_Gid":"0"},
"classification":{"Entity_Gid":[1]}

}}
    return data


