from django.conf.urls import url
from django.urls import path
from Bigflow.inward import views

urlpatterns = [
    path('inward_summary/', views.inward_summary, name='inward_summary'),
    path('setinwardentry/',views.inward_create,name='setinwardentry'),
    path('get_inwardsummary/',views.get_inwardsummary,name='get_inwardsummary'),
    path('get_inwardsummary_details/',views.get_inwardsummary_details,name='get_inwardsummary'),
    path('setinwarddetails/', views.setinwarddetails, name='setinwarddetails'),
    path('invoice/',views.invoice_crt, name='createinvoice'),
    path('employee_mst_data/',views.employee_mst_data, name='employee_mst_data'),
    path('Courier_dtll/', views.Courier_dtl, name='Courier_dtll'),

];
