from django.urls import path
from Bigflow.JVWiseFin import views
from django.conf.urls import url, include

urlpatterns = [
    url(r'^JVBigFin/(?P<template_name>[\w-]+)/$', views.JVWiseFin_Templates, name='JVWiseFin_ALL_URL'),
    path('JVWiseFin_Process_Set/',views.JVWiseFin_Process_Set,name="JVWiseFin_Process_Set"),
    path('JVWiseFin_Process_Get/',views.JVWiseFin_Process_Get,name="JVWiseFin_Process_Get"),
    path('JVWiseFin_Upload_Data/',views.JVWiseFin_Upload_Data,name="JVWiseFin_Process_Get"),
    path('JVWiseFin_Session_Set/',views.JVWiseFin_Session_Set,name="JVWiseFin_Session_Set"),
    path('JVWiseFin_Session_Get/',views.JVWiseFin_Session_Get,name="JVWiseFin_Session_Get"),
    path('JVWiseFin_Approve/',views.JVWiseFin_Approve,name="JVWiseFin_Approve"),
    path('JVWiseFin_Accounting_Entry_Data/',views.JVWiseFin_Accounting_Entry_Data,name="JVWiseFin_Approve"),
    path('jvwisefin_get_all_table_metadata_value/',views.jvwisefin_get_all_table_metadata_value,name="jvwisefin_get_all_table_metadata_value"),
    ]