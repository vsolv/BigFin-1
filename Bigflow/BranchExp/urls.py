from django.urls import path
from Bigflow.BranchExp import views
#from Bigflow.BranchExp import tasks
from django.conf.urls import url, include


urlpatterns = [
    url(r'^BranchExp/(?P<template_name>[\w-]+)/$', views.Branch_Template , name='Branch_Template'),
    #url(r'^BranchExp/(?P<template_name>[\w-]+)/$', views.Branch_Template , name='Branch_Template'),
    path('Get_expense/', views.Get_expense , name='Get_expense'),
    path('Set_expense/', views.Set_expense , name='Set_expense'),
    path('Set_premises/', views.Set_premises , name='Set_premises'),
    path('Get_premises/', views.Get_premises , name='Get_premises'),
    path('test/', views.test, name='Invoiceheader_set'),
    path('change_value/', views.change_value, name='change_value'),
    path('change_value_l/', views.change_value_l, name='change_value_l'),
    path('insertNewBranchDetails/', views.insertNewBranchDetails, name='insert_branch_details_values'),
    path('GetpropertyType/', views.brGetPropertyType, name='Br_Get_Property_Type'),
    path('get_pr_details/', views.brGetPropertyDetails, name='Br_Get_Property_Details'),
    path('get_category_subcategory/', views.get_category_subcategory, name='Category_SubCategory'),
    path('get_branch_data/', views.get_branch, name='Category_SubCategory'),
    path('get_branch_data/', views.get_branch, name='Category_SubCategory'),
    path('get_BranchExp_Meta_Data/', views.get_BranchExp_Meta_Data, name='get_BranchExp_Meta_Data'),
    path('set_schedule/', views.task_number_one, name='set_schedule'),
    path('Session_Set_Expense_Data/', views.Session_Set_Expense_Data, name='Session_Set_Expense_Data'),
    path('Session_Get_Expnese_Data/', views.Session_Get_Expnese_Data, name='Session_Get_Expnese_Data'),
    # path('thread_testing/', views.thread_testing, name='thread_testing'),
    # path('Invoiceheader_set/', views.Invoiceheader_set, name='Invoiceheader_set'),

    #Br_Makersummary  -#Br_RentCreate

    # path('Expense_Process',view_branchexp.Expense_Process.as_view()),
    #  path('Expense_ProcessSet',view_branchexp.Expense_Process_Set.as_view())



]