from django.urls import path

from Bigflow.eRMA import views

urlpatterns = [
    path('rmu2/', views.rmu2, name='rmu2'),
    path('excelgen1/', views.excelgen1, name='excel'),
    path('archival_summary/', views.archival_summary, name='archival_summary'),
    path('Archival_details/', views.Archival_details, name='Archival_details'),
    path('barcode_request/', views.barcode_request, name='barcode_request'),
    path('barcode_requestadd/', views.barcode_requestadd, name='barcode_requestadd'),
    path('barcodesumamry_get/', views.barcodesumamry_get, name='barcodesumamry_get'),
    path('barcode_set/', views.barcode_set, name='barcode_set'),
    path('barcode_assignsummary/', views.barcode_assignsummary, name='barcode_assignsummary'),
    path('barcode_assign/', views.barcode_assign, name='barcode_assign'),
]
