from django.urls import path
from Bigflow.API import view_ap as ap_api_view

urlpatterns = [
    path('EMP_BANK_DATA', ap_api_view.Emp_Bank_Details.as_view()),
    path('AP_Bank_API', ap_api_view.AP_Bank_API.as_view()),
    path('AP_Bank_DD_API', ap_api_view.AP_Bank_DD_API.as_view()),
    path('ECFInvoice', ap_api_view.ECFInvoice_set.as_view()),
    path('ECFInvoice_Get', ap_api_view.ECFInvoice_get.as_view()),
    path('AP_DD_Status_Update', ap_api_view.AP_DD_Status_Update.as_view()),
    path('AP_NEFT_Status_Update', ap_api_view.AP_NEFT_Status_Update.as_view()),

    path('ECF_STATUS_GET', ap_api_view.ECFstatus_get.as_view()),
    path('ECF_STATUS_SET', ap_api_view.ECFStatus_set.as_view()),
    path('AP_STATUS_SET', ap_api_view.APStatus_set.as_view()),
    path('WS_PROFFING_API', ap_api_view.WS_PROFFING_API.as_view()),


    ]



