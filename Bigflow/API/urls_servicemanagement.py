from django.urls import path
from Bigflow.API import view_servicemanagement as view_service_mgm

urlpatterns = [
    path('Get_Service_Management_Api',view_service_mgm.Service_Management_Get.as_view()),
    path('Set_Service_Management_Api', view_service_mgm.Service_Management_Set.as_view()),
    path('Set_AMC_Details_Api',view_service_mgm.AMC_Details_Set.as_view()),
    path('Get_AMC_Details_Api', view_service_mgm.AMC_Details_Get.as_view()),
    path('All_Tables_Values_Get_Metadata', view_service_mgm.All_Tables_Values_Get_Metadata.as_view()),
    path('All_Tables_Values_Get_Data', view_service_mgm.All_Tables_Values_Get_Data.as_view()),
    path('Pr_Detail_Set_Api', view_service_mgm.Pr_Creation.as_view()),
    ]



