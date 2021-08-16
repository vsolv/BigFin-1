

from django.urls import path

from Bigflow.API import view_branchexp as view_branchexp


urlpatterns = [
    path('Expense_Process',view_branchexp.Expense_Process.as_view()),
    path('Expense_ProcessSet',view_branchexp.Expense_Process_Set.as_view()),
    path('Br_property', view_branchexp.Property_Process_Get.as_view()),
    path('Br_property_type', view_branchexp.Property_Process_Get.as_view()),
    path('Br_property_Details', view_branchexp.Property_Process_Get.as_view()),
    path('Br_Property_Proccess_Get', view_branchexp.Property_Process_Get.as_view()),
    path('Br_Property_Proccess_Set',view_branchexp.Property_Process_Set.as_view()),
    path('Premises_Process_Set', view_branchexp.Premises_Process_Set.as_view()),
    path('Premises_Process_Get', view_branchexp.Premises_Process_Get.as_view()),
]

