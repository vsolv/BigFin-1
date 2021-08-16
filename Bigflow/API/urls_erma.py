from django.urls import path
from Bigflow.API import view_erma as view_erm
from Bigflow.API import view_service as view_service
from Bigflow.API import view_master as view_master
from Bigflow.API import view_sales as view_sales
from Bigflow.API import view_report as view_report
from Bigflow.Report import views_API as view_stock
from Bigflow.API import view_Claim as view_Claim
from django.conf.urls import url, include
#from Bigflow.API import view_purchase as view_purchase
#from Bigflow.API import view_fa as view_fa

from django.contrib import admin

urlpatterns = [
path('eRMAArchival_API', view_erm.eRMAArchival_API.as_view()),
path('Erma_Barcode_API', view_erm.Erma_Barcode_API.as_view()),
    ]