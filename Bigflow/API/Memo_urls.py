from django.urls import path

from Bigflow.API import view_Memo as view_Memo

urlpatterns = [

    path('Memo_Request_API', view_Memo.Memo_Request_API.as_view()),
    path('Memo_Request_GetAPI', view_Memo.Memo_Request_GetAPI.as_view()),
    path('Memo_Approvel_SetAPI', view_Memo.Memo_Approvel_SetAPI.as_view()),
    path('Memo_Master_SetAPI', view_Memo.Memo_Master_SetAPI.as_view()),
    path('Memo_Master_GetAPI', view_Memo.Memo_Master_GetAPI.as_view()),

]





