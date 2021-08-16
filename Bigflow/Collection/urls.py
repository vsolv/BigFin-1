from django.urls import path
from Bigflow.Collection import views
from Bigflow.Collection import views_API

urlpatterns = [
    path('Invoice_Mapping/', views.Collectionindex, name='Collection Index'),
    path('Payment_Summary/', views.CollectionSummary, name='Collection Summary'),
    path('Payment_HO_Summary/', views.CollectionHOSummary, name='Collection HOSummary'),
    path('Bank_Reconcile_Summary/', views.Collectionbankrecon, name='Collection Bank'),
    path('Receipt_Making/', views.Collectionreceipt, name='Collection Receipt'),

    path('collectioncrea/', views.Collectioncreate, name='Collectioncreate'),
    path('createDiscount/', views.CreateDiscountIndex, name='Create Discount'),
    path('getOutStanding/', views.getOutStanding, name='OutStanding Get'),
    path('get_cutoff/',views.get_cutoff,name='getcutoff'),
    path('setDiscountDetails/', views.setDiscountDetails, name='Set Discount Details'),
    ## API - urls
    path('Cltn_Inv_Map_API', views_API.Collection_API.as_view()),
    path('FET_Collection_API', views_API.FET_Collection_API.as_view()),
    path('BankUpload_API', views_API.BankUpload_API.as_view()),
    path('BankImage_API', views_API.Bankimageapi.as_view()),
    path('Receipt_AR', views_API.Receipt_AR.as_view()),
    path('Outstanding_AR', views_API.OutstandingCustomer_Get.as_view()),
    path('Receipt_Process_API', views_API.Receipt_Process_API.as_view()),

    ### API-Masters:
    path('Customer_API', views_API.Customer_API.as_view()),
    path('common_dataAPI', views_API.common_dataAPI.as_view()),

    path('Customer_Get_API', views_API.Customer_Get_API.as_view()),

    path('excelgen/', views.excelgen, name='excel'),
    path('pdfupload/', views.pdfupload, name='pdfupload'),
    path('downloadpdf/', views.downloadpdf, name='downloadpdf'),
    ### recepit summary
    path('getreceipt/', views.ReceiptSummary, name="receiptsummary"),
    path('cancelreceipt/', views.CancelReceipt, name="cancelreceipt"),

]
