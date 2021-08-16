from django.urls import path
from Bigflow.Proofing import views
from Bigflow.Proofing import views_API


urlpatterns = [
    path('mainmaster/', views.mainmaster, name='mainmaster'),
    path('intfileupload/', views.fileuploadmaster, name='fileuploadmaster'),
    path('mainentryget/', views.Entry_Get, name='Entry_Get'),
    path('excelgen1/', views.excelgen1, name='excelgen1'),



    #API URL
    path('integrity_upload', views_API.Integrity_API.as_view()),
    ]
