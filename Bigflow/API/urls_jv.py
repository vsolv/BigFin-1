from django.urls import path
from Bigflow.API import view_jv as view_jv_API

urlpatterns = [
    path('JV_Process_Set_API', view_jv_API.JV_Process_Set_API.as_view()),
    path('JV_Process_Get_API', view_jv_API.JV_Process_Get_API.as_view()),
    ]



