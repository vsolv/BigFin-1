from django.conf.urls import url
from django.urls import path
from Bigflow.Inventory import views

urlpatterns = [
    path('Inventory/', views.Inventory_Index, name='Inventory_Index'),
    path('Inventory_Approval/', views.Inventory_Approval, name='Inventory_Approval'),
    path('Inventory_Details/', views.Inventory_Details, name='Inventory_Details'),
    path('getstock_details/',views.getstock_details,name='getstock_details'),
    path('stockdetials_set/',views.stockdetials_set,name='stockdetials_set'),
    path('stock_sales_order_get/',views.stock_sales_order_get,name='stock_sales_order_get'),
    path('return_set/',views.return_set,name='return_set'),
    path('get_purrtnsmry/',views.get_purrtnsmry, name='get_purrtnsmry'),
    path('get_pur_rtnsmry/',views.get_pur_rtnsmry, name='get_pur_rtnsmry'),
    path('get_recepit/',views.get_recepit,name='get_recepit'),
    path('sales_favproduct/',views.sales_favproduct,name='sales_favproduct'),
    path('get_metadata/',views.get_metadata,name='get_metadata'),
    path('Stock_conversionSummary/',views.Stock_conversionSummary,name='Stock_conversionSummary'),
    path('stockconvert_set/',views.stockconvert_set,name='stockconvert_set'),
    path('get_conversionsummary/',views.get_conversionsummary,name='get_conversionsummary'),
]