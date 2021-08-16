from django.urls import path
from Bigflow.API import view_eClaim as view_eClaim

urlpatterns = [
    path('ECLAIM_MASTER', view_eClaim.eClaim_Master.as_view()),
    path('ECLAIM_SUMMARY', view_eClaim.eClaim_Summary.as_view()),
    path('ECLAIM_TRAN', view_eClaim.eClaim_Tran.as_view()),
    # path('FILE_DATA', view_eClaim.file_up.as_view()),


    path('TOUR_MAKER_SUMMARY', view_eClaim.Tour_Request.as_view()),
    path('TOUR_MAKER_SET', view_eClaim.Tour_Maker.as_view()),
    path('TOUR_DETAILS_GET', view_eClaim.Tour_Details.as_view()),
    path('TOUR_REASON_LIST', view_eClaim.Tour_Reason.as_view()),
    path('BRANCH_LIST', view_eClaim.Branch.as_view()),
    path('EMPLOYEE_LIST', view_eClaim.Emp_Branch.as_view()),
    path('ELIGIBLE_TRAVEL_TYPE', view_eClaim.Eligible.as_view()),
    path('APPROVAL_FLOW', view_eClaim.Approval_Flow.as_view()),
    path('APPROVAL_FLOW_PDF', view_eClaim.Approval_Flow_Pdf.as_view()),

    path('ECLAIM_APPROVAL_SUMMARY', view_eClaim.Approval.as_view()),
    path('ECLAIM_APPROVE_SET', view_eClaim.eClaim_Approve.as_view()),
    path('ECLAIM_REJECT_SET', view_eClaim.eClaim_Reject.as_view()),
    path('ECLAIM_RETURN_SET', view_eClaim.eClaim_Return.as_view()),
    path('TOUR_FORWARD_SET', view_eClaim.Tour_Forward.as_view()),
    path('APPROVER_LIST_GET', view_eClaim.Approver_List.as_view()),

    path('EMPLOYEE_DATA_GET', view_eClaim.Employee_Data.as_view()),
    path('FORWARD_DATA_GET', view_eClaim.Forward_Get.as_view()),

    path('INVOICE_PAYMENT_STATUS', view_eClaim.Invoice_PaymentStatus.as_view()),
    path('ONBEHALF_GET', view_eClaim.Onbehalfof_get.as_view()),
    path('ONBEHALF_SET', view_eClaim.Onbehalfof_set.as_view()),
    path('APPROVER_SET', view_eClaim.Approver_set.as_view()),
    path('ONBEHALF_DROPDOWN_GET', view_eClaim.Onbehalfof_dropdown_get.as_view()),
    path('EMPLOYEE_ONBEHALF', view_eClaim.Onbehalfof_Employee_get.as_view()),
    path('TOUR_APPROVER_GET', view_eClaim.TourApprover_get.as_view()),

    path('ADVANCE_MAKER_SUMMARY', view_eClaim.Advance_Summary.as_view()),
    path('CANCEL_MAKER_SUMMARY', view_eClaim.Cancel_Maker_Summary.as_view()),
    path('ADVANCE_MAKER_LIST', view_eClaim.Advance_Maker_Summary.as_view()),
    path('TOUR_CANCEL_LIST', view_eClaim.Tour_Cancel_List.as_view()),
    path('ADVANCE_CANCEL_LIST', view_eClaim.Advance_Cancel_List.as_view()),
    path('TOUR_ADVANCE_GET', view_eClaim.Tour_Advance_Get.as_view()),
    path('TOUR_ADVANCE_SET', view_eClaim.Tour_Advance_Set.as_view()),
    path('TOUR_CANCEL_SET', view_eClaim.Tour_Cancel_Set.as_view()),
    path('ADVANCE_APPROVEAMOUNT_SET', view_eClaim.Advance_Approveamount_Set.as_view()),

    path('EXPENSE_SUMMARY_GET', view_eClaim.Claimed_expense.as_view()),
    path('EXPENSE_LIST', view_eClaim.Expense_Get.as_view()),
    path('CLAIM_MAKER_SUMMARY', view_eClaim.Claim_Summary.as_view()),
    path('CLAIM_MAKER_SET', view_eClaim.Expense_Maker.as_view()),

    path('DAILYDIEM_EXP_DETAIL_GET', view_eClaim.Dailydiem_Get.as_view()),
    path('DAILYDIEM_EXP_ELIGIBLITY_CALC', view_eClaim.Dailydiem_Logic.as_view()),
    path('DAILYDIEM_EXP_DETAIL_SET', view_eClaim.Dailydiem.as_view()),

    path('EXPENSE_CITY_LIST', view_eClaim.Expense_City.as_view()),
    path('GST_LIST_GET', view_eClaim.Gst_Get.as_view()),
    path('HSN_LIST_GET', view_eClaim.Hsn_Get.as_view()),
    path('APPROVE_AMOUNT_CHANGE_SET', view_eClaim.Approve_amount.as_view()),


    path('PKG_ELIGIBLE_GET', view_eClaim.pkg_eligible_Get.as_view()),
    path('EMP_DEPENDENT_LIST', view_eClaim.Employee_Dependent.as_view()),
    path('TRAVEL_ELIGIBLE_GET', view_eClaim.Travel_Eligible.as_view()),

    path('BS_DATA_GET', view_eClaim.BS_Data_Get.as_view()),
    path('CC_DATA_GET', view_eClaim.CC_Data_Get.as_view()),
    path('CCBS_GET', view_eClaim.CCBS_Data_Get.as_view()),

    path('TRAVEL_EXP_DETAIL_GET', view_eClaim.Travel_Get.as_view()),
    path('TRAVEL_EXP_ELIGIBLITY_CALC', view_eClaim.Travel_Logic.as_view()),
    path('TRAVEL_EXP_DETAIL_SET', view_eClaim.Travel.as_view()),

    path('INCIDENTAL_EXP_DETAIL_GET', view_eClaim.Incidental_Get.as_view()),
    path('INCIDENTAL_EXP_ELIGIBLITY_CALC', view_eClaim.Incidental_Logic.as_view()),
    path('INCIDENTAL_EXP_DETAIL_SET', view_eClaim.Incidental.as_view()),

    path('PKGMVG_EXP_DETAIL_GET', view_eClaim.Pkgmvg_Get.as_view()),
    path('PKGMVG_EXP_ELIGIBLITY_CALC', view_eClaim.Pkgmvg_Logic.as_view()),
    path('PKGMVG_EXP_DETAIL_SET', view_eClaim.Pkgmvg.as_view()),

    path('LODGING_EXP_DETAIL_GET', view_eClaim.Lodging_Get.as_view()),
    path('LODGING_EXP_ELIGIBLITY_CALC', view_eClaim.Lodging_Logic.as_view()),
    path('LODGING_EXP_DETAIL_SET', view_eClaim.Lodging.as_view()),

    path('LOCCONV_EXP_DETAIL_GET', view_eClaim.Locconv_Get.as_view()),
    path('LOCCONV_EXP_ELIGIBLITY_CALC', view_eClaim.Locconv_Logic.as_view()),
    path('LOCCONV_EXP_DETAIL_SET', view_eClaim.Locconv.as_view()),

    path('MISC_EXP_DETAIL_GET', view_eClaim.Misc_Get.as_view()),
    path('MISC_EXP_DETAIL_SET', view_eClaim.Misc.as_view()),
    path('MISC_EXP_ELIGIBLITY_CALC', view_eClaim.Misc_Logic.as_view()),

    path('LOCAL_DEP_EXP_DETAIL_GET', view_eClaim.LocalDeputation_Get.as_view()),
    path('LOCAL_DEP_EXP_DETAIL_SET', view_eClaim.LocalDeputation.as_view()),
    path('LOCAL_DEP_EXP_ELIGIBLITY_CALC', view_eClaim.LocalDeputation_Logic.as_view()),

    path('HRD_EMPLOYEE_DATA', view_eClaim.HRD_Employee_Data.as_view()),
    path('EXPENSE_DELETE', view_eClaim.Expense_delete.as_view()),
    path('RECOVERY_GET', view_eClaim.Recovery_Get.as_view()),
    path('AP_ADVANCE_GET', view_eClaim.AP_Advance_Get.as_view()),
    path('ADVANCE_ADJUST', view_eClaim.Advance_Adjust.as_view()),
    path('ADVANCE_RECOVERY', view_eClaim.Advance_Recovery.as_view()),

    path('TOUR_REPORT_SUMMARY', view_eClaim.Tour_Report_Summary.as_view()),
    path('TOUR_REPORT_DOWNLOAD', view_eClaim.Tour_Report_Download.as_view()),
    path('TOUR_DETAIL_REPORT_DOWNLOAD', view_eClaim.TourDetail_Report_Download.as_view()),
    path('TOUR_EXPENSE_REPORT_DOWNLOAD', view_eClaim.TourExpense_Report_Download.as_view()),
    path('TOURNO_EXPENSE_REPORT', view_eClaim.TournoExpense_Report.as_view()),
    path('BRANCH_PENDING_COUNT', view_eClaim.Branch_Wise_Count.as_view()),

    path('ALLOWANCE', view_eClaim.Allowance.as_view()),

    path('GLMAPPING', view_eClaim.Glmapping.as_view()),
    path('GRADE_ELIGIBLITY', view_eClaim.Gradeeligibility.as_view()),
    path('CCBS_SET', view_eClaim.Ccbs_Set.as_view()),

    path('TOURDATE_RELAXATION', view_eClaim.Tour_Relaxation.as_view()),

    path('DEPENDENT_DETAILS', view_eClaim.Dependent_Details.as_view()),

    #mobile Api
    path('TOUR_DAILYDIEM_GET', view_eClaim.Tour_Dailydiem_Get.as_view()),
    path('TOUR_LOCCONV_GET', view_eClaim.Tour_Loccon_Get.as_view()),
    path('TOUR_LODGING_GET', view_eClaim.Tour_Lodging_Get.as_view()),
    path('TOUR_PKGMVG_GET', view_eClaim.Tour_Pkmvg_Get.as_view()),
    path('TOUR_TRAVEL_GET', view_eClaim.Tour_Travel_Get.as_view()),
    path('TOUR_INCIDENTAL_GET', view_eClaim.Tour_Incidental_Get.as_view()),
    path('TOUR_MISC_GET', view_eClaim.Tour_Misc_Get.as_view()),
    path('ONGOING_TOUR', view_eClaim.Ongoing_Tour.as_view()),
    path('EXPENSE_AMOUNT', view_eClaim.Expense_amount.as_view()),

    ]