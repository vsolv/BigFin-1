from django.urls import path

from Bigflow.API import view_MEP as view_MEP

urlpatterns = [

    path('PARSET_API', view_MEP.PARSET_API.as_view()),
    path('PARGET_API', view_MEP.PARGET_API.as_view()),
    path('MEPSET_API', view_MEP.MEPSET_API.as_view()),
    path('MEPGET_API', view_MEP.MEPGET_API.as_view()),
]





