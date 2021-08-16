from django.urls import path
from Bigflow.StandardInstructions import views
from django.conf.urls import url, include

urlpatterns = [
    url(r'^StandardInstructions/(?P<template_name>[\w-]+)/$', views.StandardInstructions_Templates, name='Standard_Insturctions_All_URL'),
    path('Get_All_Table_Metadata_Value/',views.Get_All_Table_Metadata_Value,name="Get_All_Table_Metadata_Value"),
    path('Set_SI/',views.Set_SI_Details,name="Set_SI_Details"),
    path('Get_SI/',views.Get_SI_Details,name="Get_SI_Details"),
    ]