from django.urls import path
from Bigflow.Gst import views

urlpatterns = [
    path('Gstrecon/', views.Gstrecon, name='Gstrecon'),
    path('GstSummary/', views.Gst_MatchesSummary, name='Gst_MatchesSummary'),
    path('gstexcel_set/', views.gstexcel_set, name='gstexcel_set'),
    path('gstsummary_get/', views.gstsummary_get, name='gstsummary_get'),
    path('Gstvalidate_set/', views.Gstvalidate_set, name='Gstvalidate_set'),
]