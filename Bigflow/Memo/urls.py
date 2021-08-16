from django.urls import path
from Bigflow.Memo import views
urlpatterns = [
path('Memo_Summary/', views.Memo_Summary, name='Memo_Summary'),
path('Memo_ApprovalSummary/', views.Memo_ApprovalSummary, name='Memo_ApprovalSummary'),
path('Memo_request_Get/', views.Memo_request_Get, name='Memo_request_Get'),
path('Memo_Approve/', views.Memo_Approve, name='Memo_Approve'),
path('Memo_Approve_Set/', views.Memo_Approve_Set, name='Memo_Approve_Set'),
path('Memo_addrequest/', views.Memo_addrequest, name='Memo_addrequest'),
path('Memo_Masters/', views.Memo_Masters, name='Memo_Masters'),
path('Memo_downloadfile/', views.Memo_downloadfile, name='Memo_downloadfile'),
path('Memo_Categoryadd/', views.Memo_Categoryadd, name='Memo_Categoryadd'),
path('Memo_SubCategory/', views.Memo_SubCategory, name='Memo_SubCategory'),
path('Memo_Create/', views.Memo_Create, name='Memo_Create'),
]