from django.urls import path
from Bigflow.DemoFet import views

urlpatterns = [
    path('demofet/', views.demo_fet, name="Demo_Fet"),
    path('demofetset/', views.demo_fet_set, name="Demo_Fet_Set"),]