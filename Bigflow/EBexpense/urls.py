from django.conf.urls import url
from django.urls import path
from Bigflow.EBexpense import views
from Bigflow.Transaction import views as transaction

urlpatterns = [
    path('ebdetails_smry/', views.electricitysmry, name='POApproval_index'),
    path('ebdetails_co_dosmry/', views.electricity_CO_DO_smry, name='electricity_CO_DO_smry'),
    path('ebdetails_co_do_aprvlsmry/', views.electricity_CO_DO_aprvlsmry, name='electricity_CO_DO_aprvlsmry'),
    path('ebdetails_paymentsmry/', views.electricitytxnsmry, name='POApproval_index'),
    path('ebdetails_querysmry/', views.electricityquerysmry, name='POApproval_index'),
    path('ebdetailsaprvl_smry/', views.electricityapprovalsmry, name='POApproval_index'),
    path('ebdetailsquery_paymtsmry/', views.electricitypaymentquerysmry, name='POApproval_index'),
    path('ebdetails_create/', views.electricitycreate, name='electricitycreate'),
    path('ebdetails_mstrtotxn/', views.electricitymastertxnsummary, name='electricitymastertxnsummary'),
    path('ebconsumerdata_validate/', views.ebconsumerdatavalidate, name='electricitycreate'),
    path('get_view_tble/', views.get_view_tble_view, name='get_view_tble'),
    path('get_view_tble_1/', views.get_view_tble_view_1, name='get_view_tble'),
    path('set_reportdata/', views.set_reportdata, name='set_reportdata'),
    path('ebconsumer_payment/', views.ebconsumerpayment, name='electricitycreate'),
    path('ebdatainsert/', views.set_ebdata, name='set_ebdata'),
    path('eb_mainsmry/', views.get_eb_smry, name='get_eb_smry'),
    path('eb_fetch_validateonly/', views.eb_fetch_validte, name='eb_fetch_validte'),
    # path('getreport_data/', views.getreport_data, name='get_eb_smry'),
    path('master_txn_eb_Data/', views.master_txn_eb_Data, name='get_eb_smry'),
    path('eb_status_insert/', views.eb_status_insert, name='eb_status_insert'),

]
