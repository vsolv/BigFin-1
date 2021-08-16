from django.urls import path
from Bigflow.ServiceManagement import views
from django.conf.urls import url, include

urlpatterns = [
    url(r'^ServiceManagement/(?P<template_name>[\w-]+)/$', views.Service_Management_Template, name='Service_Management_Template'),
    # path('AMC_Maker_Summary/' ,views.amc_Maker_Summary, name='servicesummary'),
    # path('AMC_Create/' ,views.amc_Create, name='amc_create'),
    path('Get_Service_Management/',views.get_Service_Management,name='Get_Service_Details'),
    path('Set_Service_Management/',views.set_Service_Management,name='Set_Service_Managament'),
    path('Get_Category/',views.category_data,name="Get_Category_Data"),
    path('Set_AMC_Details/',views.set_AMC_Details,name="Set_Amc_Details"),
    path('Get_AMC_Details/', views.get_AMC_Details, name="Get_Amc_Details"),
    path('Get_All_Table_Metadata/',views.Get_All_Table_Metadata,name="Get_All_Table_Metadata"),
    path('Get_Employee/',views.Get_Employee_Data,name="Get_All_Table_Metadata"),
    path('SMS_Followup_File_Upload/',views.sms_File_Upload,name="Get_All_Table_Metadata"),
    ]