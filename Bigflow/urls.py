"""Bigflow URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from Bigflow.Core import views as core
from Bigflow.Master import views as master
from Bigflow.Transaction import views as transaction
from Bigflow.UserMgmt import views as userMgmnt
from Bigflow.AP import views as ap
from Bigflow.Purchase import views as purchase
from django.conf.urls import url, include
from django.contrib import admin
from Bigflow.Collection import urls as CollectionUrl
from Bigflow.Collection import views as CollectionViews
from Bigflow.Purchase import urls as PurchaseUrl
from Bigflow.Report import urls as Reporturl
from Bigflow.Service import urls as ServiceUrl
from Bigflow.inward import urls as InwardUrl
from Bigflow.AP import urls as APUrl
# from Bigflow.BranchExp import urls as BRUrl
from Bigflow.BOM import urls as BOMUrl
from Bigflow.Master import urls as MasterUrl
from Bigflow.API import urls as API_url
from django.conf import settings
from django.conf.urls.static import static
from Bigflow.Sales import views as apview
from Bigflow.BranchExp import views as brview
from Bigflow.Inventory import urls as InventoryUrl
from Bigflow.ATMA import urls as ATMAUrl
from Bigflow.BranchExp import urls as brUrl
from Bigflow.FA import urls as FAUrl
from Bigflow.MEP import urls as MEPUrl
from Bigflow.API import MEP_urls as MEP_urls
from Bigflow.eRMA import urls as eRMAUrl
from Bigflow.API import urls_erma as api_eRMAUrl
from Bigflow.API import urls_branchexp as Branch_url
from Bigflow.ServiceManagement import urls as ServiceManagement_url
from Bigflow.API import urls_servicemanagement as API_url_ServiceManagemnt
from Bigflow.StandardInstructions import urls as StandardInstructions_App_URL
from Bigflow.API import urls_standardinstructions as StandardInstuctions_API_URL
from Bigflow.eClaim import urls as eClaimUrls
from Bigflow.API import urls_eClaim as eClaimUrls_API
from Bigflow.Memo import urls as MemoUrl
from Bigflow.API import Memo_urls as Memo_urls
from Bigflow.API import Purchase_urls as Purchase_API_URL
from Bigflow.API import urls_ap as AP_API_URL
from Bigflow.JV import urls as JV_App_URL
from Bigflow.JVWiseFin import urls as JVWiseFin_App_URL
from Bigflow.API import urls_jv as JV_API_URL
from Bigflow.EBexpense import urls as ElectricityUrl
from Bigflow.DemoFet import urls as DemoFetUrl




urlpatterns = [
                  path('', core.loginIndex, name='login'),
                  path('welcome/', core.welcomeIndex, name='welcome'),
                  path('loaderSpinner/', core.loaderspinnerIndex, name='loaderSpinner'),
                  path('sidenavfilter/', master.sideNavFilterIndex, name='sidenavfilter'),
                  path('select_product/', core.selectproductIndex, name='select_product'),
                  path('select_supplier/', core.selectSupplierIndex, name='select_supplier'),
                  path('select_employee/', core.selectEmployeeIndex, name='select_employee'),
                  path('setposition/', core.setPosition, name='setPosition'),
                  path('getposition/', core.getposition, name='getposition'),
                  path('setday/', core.setDayroute, name='setDayroute'),
                  path('getdayroute/', core.getdayroute, name='getdayroute'),
                  path('state_add/', core.StateAdd, name="State_Add"),

                  # path('setday/', master.setDayroute, name='setDayroute'),

                  path('loginpswd/', core.loginpswd, name='loginpswd'),
                  path('setip_sys/', core.setip_sys, name='setip_sys'),
                  path('update_personal_info/', core.update_personal_index, name='update_personal_info'),
                  path('otp_genrte_validte/', core.validate_otp, name='loginpswd'),
                  path('setip_out/', core.setip_out, name='setip_out'),
                  path('menulist/', core.menuList, name='menu'),
                  path('version_get/', core.version_get, name='version_get'),

                  # report
                  path('col_performance/', core.collectionperformanceIndex, name='collection Performance'),
                  path('getcol_performance/', core.getcollectionperformance, name='collection Performance'),
                  path('report/', transaction.fetreportgenarate, name='report'),
                  path('update_personal_num/', transaction.update_personal_info, name='update_personal_info'),
                  path('excelreport/', transaction.excelreport, name='reportexcel'),
                  path('query_summary_salesproductget/', transaction.query_summary_salesproductget, name='query_summary_salesproductget'),
                  path('query_summary_collectionget/', transaction.query_summary_collectionget, name='query_summary_collectionget'),
                  path('query_summary_outstandingget/', transaction.query_summary_outstandingget, name='query_summary_outstandingget'),
                  path('query_summary_getcollectionstatus/', transaction.query_summary_getcollectionstatus, name='query_summary_getcollectionstatus'),

                  # Sales
                  path('genpopup/',apview.Generate_label_popup,name='generate_label'),
                  path('monthlyexcel/',apview.excelmonth,name='monthlyexcel'),
                  path('excel1/', apview.excel, name='excel12'),
                  path('viewpopup/', apview.Invoice_view_popup, name='viewpopup'),
                  path('saleindex/', apview.saleindex, name='SO_Summary'),
                  path('saleinvoice/', apview.SalesRegisterInvoice, name='SalesRegisterInvoice'),
                  path('saleget/', apview.salesget, name='salesget'),
                  path('compgn/', apview.compaiget, name='compaiget'),
                  path('prcesmry/', apview.prcsmry, name='prcsmry'),
                  path('stateget/', apview.get_state, name='get_state'),
                  path('prodget/', apview.get_prod, name='get_prod'),
                  path('pmapsmry/', apview.prodmapgsmry, name='prodmapgsmry'),
                  path('branchdetail/', apview.branchdetails, name="branchdetails"),
                  path('manuallabel/', apview.ManualLabelGenerate, name="ManualLabelGenerate"),
                  path('setinvc/', apview.set_inv, name='set_inv'),
                  path('setsal/', apview.set_sal, name='set_sal'),
                  path('getinv/', apview.getinvsmry, name='set_inv'),
                  path('invoicepopup/', apview.InvoicePopup, name='InvoicePopup'),
                  path('prodgett/', apview.prod_get, name='prod_get'),
                  path('dealerpricemaker/', apview.DealerPriceMakerSummary, name='DealerPriceMakerSummary'),
                  path('popup1/', apview.Dealer_Add_Popup, name="Dealer_Add_Popup"),
                  path('dealerpriceapprover/', apview.DealerPriceApproverSummary, name="DealerPriceApproverSummary"),
                  path('custpdctratecardmaker/', apview.CustomerMappingSummary, name="CustomerMappingSummary"),
                  path('custpopup/', apview.Customer_popup, name="Customer_popup"),
                  path('custpdctratecardapprover/', apview.CustomerApproverSummary, name="CustomerApproverSummary"),
                  path('dispatchsale/', apview.invcsmry, name="Dispatch_Sale_Invoice"),
                  path('weightpopup/', apview.weightupdatepop, name="weightupdate"),
                  path('setdispatch/', apview.SetDispatchValue, name="setdispatch"),
                  path('Excepted_Courier/',apview.Excepted_Courier_Bill,name="Excepted_Courier"),
                  path('courierexplorer/', apview.Courier_Explorer, name="Courier_Explorer"),
                  path('Bulkpopup/', apview.Bulkpopup, name="Bulkpopup"),
                  path('invoicancel/', apview.Invoice_Cancel_Summary, name="invoice_cancel"),
                  path('dispatchPOD/', apview.Dispatch_POD_Updation, name="dispatch_pod"),
                  path('dispatchpopup/', apview.Dispatch_Popup, name="dispatch_popup"),
                  path('printsummary/', apview.Invoice_print_Summary, name="print_summary"),
                  path('labelgenerate/', apview.Dispatchlabelgenerate, name="Dispatchlabelgenerate"),
                  path('getlablprod/', apview.get_prodlabl, name="get_prodlabl"),
                  path('setlablprod/', apview.set_prodlabl, name="set_prodlabl"),
                  path('getmstr/', apview.masterdrpdwn, name="masterdrpdwn"),
                  path('getclasification/', apview.branchdrpdown, name="branchdrpdown"),
                  # Employee
                  path('employee/', master.employeeIndex, name='Employee'),
                  path('empadrs/', master.employeeadrsIndex, name='Employee address'),
                  path('empcntct/', master.employeecntctIndex, name='Employee contact'),
                  path('empview/', master.employeeviewIndex, name='Employee view'),
                  path('empattendance/', master.empattendanceIndex, name='emp attendance'),
                  path('emp_summary/', master.employeesummaryIndex, name='emp_summary'),
                  path('department/', master.departmentIndex, name='Department'),
                  path('ccbs_maker/', master.Ccbs_Maker_fun, name='Ccbs_Maker'),
                  path('ccbs_approver/', master.Ccbs_Approver_fun, name='Ccbs_Approver'),
                  path('ccbs_maker_popup/', master.Ccbs_Maker_Popup_fun, name='Ccbs_Maker_popup'),
                  path('Cat_Subcat/', master.Cat_Subcat_fun, name='Cat_Subcat'),
                  path('Cat_Subcat_Approver/', master.Cat_Subcat_Approver, name='Cat_Subcat_Approver'),
                  path('Cc_Bb_Sum/', master.Cc_Bb_Summary, name='Cc_Bb_Sum'),
                  path('Cc_Bb_Pop/', master.Cc_Bb_Popup, name='Cc_Bb_Popup'),
                  path('Cat_Subcat_popup/', master.Cat_Subcat_Popup, name='Cat_Subcat_popup'),
                  path('deptjson/', master.dept_get),
                  path('desgjson/', master.desg_get),
                  path('departjson/', master.departjson),
                  path('depteditjson/', master.depteditjson),
                  path('deptdeletejson/', master.deptdeletejson),
                  path('deptactivejson/', master.deptactivejson),
                  path('deptinactivejson/', master.deptinactivejson),
                  # path('department/', master.department, name='department'),
                  path('employee_get/', master.employee_get, name='employee_get'),
                  path('employee_getexcel/', master.employee_getexcel, name='employee_getexcel'),
                  path('cluster_get/', master.cluster_get, name='cluster_get'),
                  path('get_custgroup/', master.get_custgroup, name='get_custgroup'),
                  path('get_contctgroup/', master.get_contctgroup, name='get_contctgroup'),
                  path('getMappedLocation/', master.getMappedLocation, name='sales_order_set'),
                  path('getRouteDtl/', master.getRouteDtl, name='getRouteDtl'),
                  path('gettown/', master.gettownn, name='gettown'),
                  path('getrout/', master.getrout, name='getrout'),
                  path('setRouteDtl/', master.setRouteDtl, name='setRouteDtl'),
                  path('employeeset/', master.employeeset, name='employeeset'),
                  path('employeeupset/', master.employeeupset, name='employeeupset'),
                  path('employedit_get/', master.employedit_get, name='employedit_get'),
                  path('hierarchy/', master.hierarchy, name='hierarchy'),
                  path('getroute/', master.getroute, name='getroute'),
                  path('customersales/', core.customerSales, name='customerSales'),
                  path('get_employeeddl/', master.get_employeeddl, name='get_employeeddl'),
                  path('employeeupload/', master.emp_upload, name='emp_upload'),

                  #branch
                  # path('BranchCreate/',brview.Branch_Create,name='Branch_Create'),


                  # FET
                  path('gettadetails/', transaction.gettadetails, name='gettadetails'),
                  path('taview/', transaction.taviewget, name='taviewget'),
                  #path('TASummary_API', transaction.TASummary_API.as_view()),
                  path('direct/', transaction.directIndex, name='direct'),
                  path('drctentry/', transaction.directentryIndex, name='direct'),
                  path('query_summary_salesget/', transaction.query_summary_salesget, name='query_summary_salesget'),
                  path('collectioncreate/', transaction.collectioncreateIndex, name='collectioncreate'),
                  path('stocktkncreate/', transaction.stockcreateIndex, name='stocktkncreate'),
                  path('salecreate/', transaction.salecreateIndex, name='salecreate'),
                  path('approval/', transaction.fetapprovalIndex, name='fetapproval'),
                  path('prospect/', transaction.fetprospctIndex, name='fetprospct'),
                  path('emproute/', master.emprouteIndex, name='emp emproute'),
                  path('empdaymap/', master.emproutedaymapping, name='emp routedaymapping'),
                  path('Schedule_report/', transaction.Schedule_reportIndex, name='Schedule_report'),
                  path('sales_order/', transaction.sales_orderIndex, name='sales_order'),
                  path('service/', transaction.serviceIndex, name='service'),
                  path('saledetail/', transaction.allsaledetIndex, name='saledetail'),


                  path('schedule_task/', transaction.reportupdateIndex, name='schedule_task'),
                  path('pschedule/', transaction.preschdleIndex, name='preschedule'),
                  path('pcollection/', transaction.pcollectionIndex, name='pcollection'),
                  path('schedule_collection/', transaction.schedule_collectionIndex, name='schedule_collection'),
                  path('TA_details/', transaction.TA_detailsIndex, name='TA_details'),
                  path('emptracking/', transaction.emptrackingIndex, name='employeetracking'),
                  path('emptrackingrep/', transaction.emptrackingrepIndex, name='employeetrackingrep'),
                  path('rep_review/', transaction.schedulereviewIndex, name='schedulereview'),
                  path('snap_shot_get/', transaction.snap_shot_get, name='snap_shot_get'),
                  path('fetprocess/', transaction.fetprocess, name='fetprocess'),
                  path('fetcollection/', transaction.fetcollection, name='fetprocess'),
                  path('get_collectionapi/', transaction.get_collectionapi, name='fetprocess'),
                  path('searchview/', transaction.searchview, name='searchview'),

                  path('clustermastr/', transaction.getclustermaster, name='getclustermaster'),
                  path('employeeddl/', transaction.employeeddl, name='employeeddl'),
                  path('tasummary/', transaction.tasummary, name='tasummary'),


                  path('fetsnapshot/', transaction.fetsnapshot,name='fetsnapshot'),
                  path('fetprocess/', transaction.fetprocess,name='fetprocess'),
                  path('fetcollection/', transaction.fetcollection, name='fetprocess'),
                  path('get_collectionapi/', transaction.get_collectionapi, name='fetprocess'),

                  path('schedule_type/', transaction.schedule_type, name='schedule_type'),
                  path('followup_reason/', transaction.followup_reason, name='followup_reason'),
                  path('mapped_customer/', transaction.mapped_customer, name='mapped_customer'),
                  path('emp_mapped_customer/', transaction.emp_mapped_customer, name='pass emp get mapped_customer'),
                  path('customer_ddl/', transaction.customer_ddl, name='customer_ddl'),
                  path('productcategory_ddl/', transaction.productcategory_ddl, name='productcategory_ddl'),
                  path('producttype_ddl/', transaction.producttype_ddl, name='producttype_ddl'),
                  path('getEditSchedule/', transaction.getEditSchedule, name='getEditSchedule'),
                  path('getEditdrct/', transaction.getEditdrct, name='getEditdrct'),
                  path('leadapprove/', transaction.leadrequest_approve, name='leadapprove'),
                  path('saleapprove/', transaction.sale_approval, name='sale_approval'),
                  path('emp_schedule_get/', transaction.empvsschedule_get, name='emp_schedule_get'),
                  path('pre_schedule_get/', transaction.pre_schedule_get, name='pre_schedule_get'),
                  path('pre_schedule_status/', transaction.pre_schedule_status, name='pre_schedule_status'),
                  path('set_sch_review/', transaction.setschedule_review, name='set_sch_review'),
                  path('sales_order_set/', transaction.sales_order_set, name='sales_order_set'),
                  # path('sales_order_setup/', transaction.sales_order_setup, name='sales_order_setup'),
                  path('sales_fav_product/', transaction.sales_fav_product, name='sales_fav_product'),
                  # path('service_get/', transaction.service_get, name='service_get'),
                  path('Productjson/', transaction.Productjson, name='Productjson'),
                  path('outstanding_fet_get/', transaction.outstanding_fet_get, name='outstanding_fet_get'),
                  path('outstanding_get/', transaction.getOutstanding, name='get Outstanding Details using API'),
                  path('sales_history_fet_get/', transaction.sales_history_fet_get, name='sales_history_fet_get'),
                  path('sales_order_get/', transaction.sales_order_get, name='sales_order_get'),
                  path('getapi/', transaction.apiget, name='apiget'),
                  path('custgroup/', transaction.custgroupget, name='custgroupget'),
                  path('reciptget/', transaction.getreceipt, name='getreceipt'),
                  path('banknmeget/', transaction.getbankname, name='getbankname'),
                  path('getcustemp/', transaction.getcustemp, name='getcustemp'),
                  path('getotsng/', transaction.outstndng, name='outstndng'),
                  path('custmer_get/', transaction.custmer_get, name='custmer_get'),
                  path('setexcel/', transaction.exclread, name='exclread'),
                  path('setcoll/', transaction.colset, name='colset'),
                  path('collection_history_fet/', transaction.collection_history_fet, name='collection_history_fet'),
                  path('schedule_view_fet/', transaction.schedule_view_fet_get, name='schedule_view_fet'),
                  path('status_get/', transaction.status_get, name='status_get'),
                  path('status_qty/', transaction.status_qty, name='status_qty'),
                  path('serviceFET_set/', transaction.serviceFET_set, name='serviceFET_set'),
                  path('service_set/', transaction.serviceFET_set, name='service_set'),
                  path('collection_set/', transaction.collection_set, name='collection_set'),
                  path('add_schedule/', transaction.add_schdle, name='add_schdle'),  # ## Page included

                  path('leadrequest_set/', transaction.leadrequest_set, name='leadrequest_set'),
                  path('leadrequest_get/', transaction.leadrequest_get, name='leadrequest_get'),
                  path('sale_order_get/', transaction.sale_order_get, name='sale_order_get'),
                  path('Schedule_reportget/', transaction.Schedule_reportget, name='Schedule_reportget'),
                  path('collection_get/', transaction.report_collection, name='report_collection'),
                  path('get_addScheduleDtl/', transaction.get_addScheduleDtl, name='get_addScheduleDtl'),
                  path('bank_detail/', transaction.bank_detail, name='bank_detail'),
                  # nav menu
                  path('getclustertree/', transaction.getClusterTree, name='getclustertree'),
                  path('getCustFilter/', transaction.getCustomerFilterlist, name='getCustFilter'),
                  path('stocktaken/', transaction.stocktakenIndex, name='stocktakenIndex'),
                  path('stockget/', transaction.stockget, name='stockget'),
                  path('stockset/', transaction.stockset, name='stockset'),
                  path('stockeditget/', transaction.stockeditget, name='stockeditget'),
                  path('getlaglongfet/', transaction.getlaglongfet, name='getlaglongfet'),
                  path('getLogindetails/', transaction.getLogindetails, name='getLogindetails'),
                  # ponraj
                  # User Mangement
                  path('rolesummary/', userMgmnt.rolesummaryIndex, name='rollsummary'),
                  path('userRoles/', userMgmnt.userroleIndex, name='menuList'),
                  path('changePassword/', userMgmnt.changepwdIndex, name='changePassword'),
                  path('resetPassword/', userMgmnt.resetpwdIndex, name='resetPassword'),
                  path('roleList/', userMgmnt.get_roleList, name='rollList'),
                  path('roleGroup/', userMgmnt.get_rollgroup, name='rollGroup'),
                  path('userList/', userMgmnt.get_userList, name='userList'),
                  path('menuList/', userMgmnt.get_menuList, name='menuList'),
                  path('setRollDetails/', userMgmnt.setRoleDetails, name='setRollDetails'),
                  path('employeeList/', userMgmnt.getEmployeeDtl, name='employeeList'),
                  path('clustgroupList/', userMgmnt.getClustGroup, name='clustgroupList'),
                  path('setempRoles/', userMgmnt.setEmployeeRole, name='setempRoles'),
                  path('Employee_detail/', userMgmnt.Employee_detail, name='Employee_detail'),
                  path('Password_verifiy/', userMgmnt.Password_verifiy, name='Password_verifiy'),
                  path('All_Employeedetail/', userMgmnt.All_Employeedetail, name='All_Employeedetail'),
                  path('Set_Password/', userMgmnt.Set_Password, name='Set_Password'),


                  # customer
                  path('Custmer/', master.Customer_Index, name='Custmer'),
                  path('territory/', master.CustomerTerritoryIndex, name='Customer_TerritoryIndex'),
                  path('customergrp_get/', master.customergrp_get, name='customergrp_get'),
                  path('customer_get/', master.customer_get, name='customer_get'),
                  path('customer_getexcel/', master.customer_getexcel, name='customer_getexcel'),
                  path('custpin_excel/', master.custpin_excel, name='custpin_excel'),
                  path('customeredt_get/', master.customeredt_get, name='customeredt_get'),
                  path('emailverify/', master.get_emailverify, name='get_emailverify'),
                  path('Supplier_Master/', master.Supplier_Master, name='supplierIndex'),

                  path('customercreate/', master.customercreateIndex, name='customercreate'),
                  path('locationddl/', master.locationddl, name='locationddl'),
                  path('stateddl/', master.stateddl, name='stateddl'),
                  path('districtddl/', master.districtddl, name='districtddl'),
                  path('allpinget/', master.allpinget, name='allpinget'),
                  path('cityddl/', master.cityddl, name='cityddl'),
                  path('pincode/', master.pincode, name='pincode'),
                  path('customerset/', master.customerset, name='customerset'),
                  path('locationget/', master.locationget, name='locationget'),
                  path('addressget/', master.addressget, name='addressget'),
                  path('customerdel/', master.customerdel, name='customerdel'),
                  path('getclusterdtl/', master.getClusterDtl, name='getclusterdtl'),
                  path('set_cluster/', master.setCluster, name='set_cluster'),
                  path('get_custcate/', master.get_custcate, name='get_custcate'),
                  path('get_cluster/', master.get_cluster, name='get_cluster'),
                  path('get_custdata/', master.get_custdata, name='get_custdata'),
                  path('customergroupset/', master.customergroupset, name='customergroupset'),
                  path('executivemapping_index/', master.executivemapping_index, name='executivemapping_index'),
                  path('exemapping/', master.exemapping, name='exemapping'),
                  path('empddl/', master.empddl, name='empddl'),
                  path('get_exemapping/', master.get_exemapping, name='get_exemapping'),
                  path('cbsmaster/',master.ccbs_master,name='cbs_master'),
                  path('catsubcat/',master.cat_subcat_master,name='cbs_master'),
                  path('cbsmain/',master.main_category_master,name='cbs_master'),

                  #barcode and scanning
                  path('pdfviewer/', core.pdfviewer, name='pdfviewer'),
                  path('Health_Check/', core.Health_Check, name='Health_Check'),
                  path('barcode/', transaction.barcode, name='barcode'),
                  path('scanning_barcode/', transaction.scanning_barcode, name='scanning'),

                  # purchase
                  path('', include(PurchaseUrl)),
                  path('', include(Purchase_API_URL)),

                  # Report
                  path('', include(Reporturl)),

                  # Collection
                  path('', include(CollectionUrl)),
                  path('receiptcancel/', CollectionViews.CollectionReceiptSummary, name='receipt_Cancel'),

                  # service
                  path('', include(ServiceUrl)),

                  # BOM
                  path('', include(BOMUrl)),

                  # inward
                  path('', include(InwardUrl)),

                  # Master
                  path('', include(MasterUrl)),

                  # AP
                  path('', include(APUrl)),
                  path('',include(AP_API_URL)),

                  # path('', include(BRUrl)),

                  # AP
                  path('billentry/', ap.billentryIndex, name='billentry'),

                  # # API
                  path('', include(API_url)),


                  # side panel
                  path('cus_cuecard/', core.customercuecardIndex, name='customerCueCard'),
                  path('cus_cuecardview/', core.customercuecardviewIndex, name='customerCueCardview'),
                  path('cus_snapshtview/', core.customersnapstviewIndex, name='customersnapshotview'),
                  path('cus_entityview/', core.customerentityviewIndex, name='customerentityview'),
                  path('cus_activityview/', core.customeractivitytrendviewIndex, name='customeractivityview'),
                  path('cus_creditapprvview/', core.customercreditapproveviewIndex, name='creditapproveview'),
                  path('cus_snapshot/', core.customersnapshotIndex, name='customersnapshot'),
                  path('cus_entity/', core.customerentityoutcomeIndex, name='customerentity'),
                  path('cus_credit/', core.customercreditapproveIndex, name='creditapprove'),
                  path('cus_activity/', core.customeractivitytrendIndex, name='activitytrendsale'),
                  # path('customersales/', core.customerSales, name='customerSales'),
                  path('dp_get/', core.dp_get, name='dp_get'),
                  path('snapsales/', core.snapsales, name='snapsales'),
                  path('credit_approve/', core.getapprove, name='credit_approve'),
                  path('credit_proposed/', core.getproposed, name='credit_proposed'),
                  path('credit_pdc/', core.pendingsmry, name='credit_pdc'),
                  path('trend_sale/', core.getactivity, name='activitytrendsale'),
                  path('trend_coll/', core.getactivitycol, name='activitytrendsale'),
                  path('daymapping/', core.routedaymap, name='routedaymapping'),
                  path('setdaymapping/', core.employedaymap, name='setdaymapping'),
                  path('outstnd_get/', core.outstnd_get, name='outstnd_get'),
                  path('payred_get/', core.payred_get, name='payred_get'),
                  path('getentityget/', core.getentityget, name='getentityget'),
                  path('get_categorygroup/', core.get_categorygroup, name='get_categorygroup'),
                  path('dropdowndata/', master.commondropdown, name='dropdownData'),
                  path('getuniquecode/', master.getuniquecode, name='getuniquecode'),
                  path('gettaxdetails/', master.gettaxdetails, name='gettaxdetails'),
                  path('comment/', core.commentviewindex, name='comment'),
                  path('viewDetails/', core.viewDetailsIndex, name='View Details'),
                  path('cmndispatch/', core.commondispatch, name='commondispatch'),
                  path('trackingview/', transaction.fetemptracking, name='trackingview'),
                  path('fetemplogin/', transaction.fetemplogin, name='fetemplogin'),
                  path('City/', master.city, name='City'),
                  path('city_get/', master.city_get, name='city_get'),
                  path('city_set/', master.city_set, name='city_set'),
                  path('fetreview_getexcel/', transaction.fetreview_getexcel, name='fetreview_getexcel'),
                  path('fetemployee_getexcel/', transaction.fetemployee_getexcel, name='fetemployee_getexcel'),
                  path('fetreport/', transaction.fetreport, name='fetreport'),
                  path('Supplierproduct/', master.Supplierproduct_index, name='Supplierproduct'),
                  path('suppplierproductmap_set/', master.suppplierproductmap_set, name='suppplierproductmap_set'),
                  path('suppplierproductmap_get/', master.suppplierproductmap_get, name='suppplierproductmap_get', ),
                  #Supplier
                  path('All_product_get/', master.All_product_get, name='All_product_get'),
                  # Client
                  path('Client/', master.client, name='client'),
                  path('Clientcreate/', master.clientcreate, name='clientcreate'),
                  path('client_get/', master.client_get, name='client_get'),
                  path('client_set/', master.client_set, name='client_set'),

                  path('', include(InventoryUrl)),
                  #ATMA
                  path('', include(ATMAUrl)),
                  path('',include(FAUrl)),

                  # BranchExp
                  path('', include(brUrl)),
                  path('', include(Branch_url)),

                  # Electricity Expenses
                  path('', include(ElectricityUrl)),

                  #MEP
                  path('',include(MEP_urls)),
                  path('', include(MEPUrl)),

                  #eRMA
                  path('', include(eRMAUrl)),
                  path('', include(api_eRMAUrl)),

                  #ServiceManagement
                  path('', include(API_url_ServiceManagemnt)),
                  path('', include(ServiceManagement_url)),

                  #StandardInstuctions
                  path('',include(StandardInstructions_App_URL)),
                  path('',include(StandardInstuctions_API_URL)),

                  #eClaim
                  path('',include(eClaimUrls)),
                  path('',include(eClaimUrls_API)),

                  # Memo
                  path('', include(MemoUrl)),
                  path('', include(Memo_urls)),

                  # JV
                  path('', include(JV_API_URL)),
                  path('', include(JV_App_URL)),
                  path('', include(JVWiseFin_App_URL)),
                path('',include(DemoFetUrl))

              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)