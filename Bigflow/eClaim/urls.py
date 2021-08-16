from django.urls import path
from django.conf.urls import url
from Bigflow.eClaim import views
urlpatterns = [
    path('eClaim_master_data/', views.eclaim_master, name="eclaim_master"),
    path('eclaim_summary/', views.eclaim_summary, name="eclaim_summary"),
    path('eclaim_process_set/', views.eclaim_process_set, name="eclaim_process_set"),
    path('tour_set_file/', views.tour_set_file, name="tour_set_file"),
    path('eclaim_withfile_set/', views.eclaim_withfile_set, name="eclaim_process_set"),
    path('data_alltablevalue/', views.data_alltablevalue, name="data_alltablevalue"),
    path('tcf_to_pdf/', views.tcf_pdf, name="tcf_pdf"),
    path('download_pdf/', views.download_pdf, name="get_pdf"),
    path('ecf_data_get/', views.ECF_data_Get, name="ecf_data_get"),
    path('Get_Supplier/', views.get_supplier, name="get_supplier"),
    path('eclaim_dropdata/', views.eclaim_dropdata, name="eclaim_dropdata"),
    path('expense_detail/', views.expense_detail, name="expense_detail"),
    path('session_set_expense/', views.session_set_expense, name="session_set_expense"),
    path('session_get_expnese/', views.session_get_expnese, name="session_get_expnese"),
    path('tour_gen_xl/', views.tour_generate_xl, name="tour_generate_xl"),
    # eClaim Pages
    url(r'^eClaim/(?P<template_name>[\w-]+)/$', views.eClaim_Template , name='eClaim_Template'),
]
