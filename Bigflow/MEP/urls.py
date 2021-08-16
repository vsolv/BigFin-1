from django.urls import path
from Bigflow.MEP import views
urlpatterns = [
path('PAR_Summary/', views.PAR_Summary, name='PAR_Summary'),
path('PAR_Add/', views.PAR_Add, name='PAR_Add'),
path('PAR_Add_Set/', views.PAR_Add_Set, name='PAR_Add_Set'),
path('Par_Get/', views.Par_Get, name='Par_Get'),
path('Par_Checker/', views.Par_Checker, name='Par_Checker'),
#path('Par_Update/', views.Par_Update, name='Par_Update'),
path('Mep_Summary/', views.Mep_Summary, name='Mep_Summary'),
path('Mep_Add/', views.Mep_Add, name='Mep_Add'),
path('Mep_Checker/', views.Mep_Checker, name='Mep_Checker'),
path('imageconvert_par/', views.imageconvert_par, name='imageconvert_par'),

]