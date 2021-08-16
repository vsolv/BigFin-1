from django.urls import path

from Bigflow.API import view_purchase as view_purchase

urlpatterns = [

    path('Delmat_set', view_purchase.Delmat.as_view()),
    path('Alltable_ccbs', view_purchase.Alltable_ccbs.as_view()),
    path('PR_Header_DDl', view_purchase.PR_Header_DDl.as_view()),
    path('PO_HeaderDDl',view_purchase.PO_HeaderDDl.as_view()),
    path('Mep_In_PR',view_purchase.Mep_In_PR.as_view()),
    path('Tran_History_Get',view_purchase.Tran_History_Get.as_view()),
    path('Set_Poterms', view_purchase.Set_Poterms.as_view()),
    path('Get_Poamend', view_purchase.Get_Poamend.as_view()),
    path('ms_po_FA_assetmake', view_purchase.MS_PO_FA_Asset_Make.as_view()),
    path('ms_po_FA_PO_Get', view_purchase.MS_PO_FA_PO_GET.as_view()),
]





