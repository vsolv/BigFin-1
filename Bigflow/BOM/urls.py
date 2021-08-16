from django.urls import path
from Bigflow.BOM import views

urlpatterns = [

    path('cmpnt_summary/', views.componentIndex, name='Component Summary'),
    path('cmpnt_rate/', views.componentRateIndex, name='Component Rate'),
    path('cmpnt_suprate/', views.componentSupplierRateIndex, name='Component Supplier Rate'),
    path('compnt_get/', views.compnt_get, name='compnt_get'),
    path('mapped_get/', views.mapped_get, name='mapped_get'),
    path('setcomp/', views.setcomp, name='setcomp'),
]
