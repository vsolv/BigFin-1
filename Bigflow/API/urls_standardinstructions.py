from django.urls import path
from Bigflow.API import view_standardinstructions as view_standardinstructions

urlpatterns = [
    path('Set_SI_Details_API', view_standardinstructions.SI_Process_Set.as_view()),
    path('Get_SI_Details_API', view_standardinstructions.SI_Process_Get.as_view()),
    ]



