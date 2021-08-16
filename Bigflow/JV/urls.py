from django.urls import path
from Bigflow.JV import views
from django.conf.urls import url, include

urlpatterns = [
    url(r'^JV/(?P<template_name>[\w-]+)/$', views.JV_Templates, name='JV_ALL_URL'),
    path('JV_Process_Set/',views.JV_Process_Set,name="JV_Process_Set"),
    path('JV_Process_Get/',views.JV_Process_Get,name="JV_Process_Get"),
    path('JV_Upload_Data/',views.JV_Upload_Data,name="JV_Process_Get"),
    path('JV_Session_Set/',views.JV_Session_Set,name="JV_Session_Set"),
    path('JV_Session_Get/',views.JV_Session_Get,name="JV_Session_Get"),
    path('JV_Approve/',views.JV_Approve,name="JV_Approve"),
    path('JV_Accounting_Entry_Data/',views.JV_Accounting_Entry_Data,name="JV_Approve"),
    path('jv_get_all_table_metadata_value/',views.jv_get_all_table_metadata_value,name="jv_get_all_table_metadata_value"),
    ]