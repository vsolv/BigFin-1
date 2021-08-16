var done_msg = "SUCCESS";
var not_enter_reason = "Please Enter the Reason";
var not_enter_date = "Please Enter the Date";
var not_enter_branch = "Please Enter the Branch";
var not_enter_location = "Please Enter the Location";
var not_enter_category = "Please Enter the Category";
var not_enter_customer = "Please Enter the Customer Data";
var not_enter_customer = "Please Enter the Customer Data";
var not_enter_name = "Please Enter the Name";
var not_enter_gstno = "Please Enter the Gst No";
var not_enter_cellno = "Please Enter the Cell No";
var not_enter_address = "Please Enter the Address";
var not_matched = "Data Not Matched";
var no_data = "Please Enter Data"
var not_enter_date_reason = "Please Enter the reason & Date";
var same_data = "Already in Same Data";
var date_clubed = "Date is Irrelavent";
var Advancedate_error = "Advance Date End";
var expensedate_erroe = "Tour Date Not Start";
var img_attached = "Image Successfully Attached..";
var img_fr_mismatch = "Your Image Format is Miss Match";
var not_enter_state = "Please Choose the State";
var not_enter_rate = "Please Enter the Sale Rate";
var not_enter_cc = "Please Enter the CC Data";
var not_enter_product = "Please Choose The Product";
var not_enter_parent = "Please Choose the Parent Asset";
var not_enter_cwipgrp = "Please Choose the CWIP Group";
var not_enter_bs = "Please Enter the BS Data";
var not_matched_hsn = "Data Not Matched HSN Code";
var not_matched_sgst = "Data Not Matched SGST";
var not_matched_cgst = "Data Not Matched CGST";
var not_matched_igst = "Data Not Matched IGST";
var not_matched_branch = "Data Not Matched Branch";
var no_cwip_name = "Please Enter the Cwip Name";
var no_cwip_gl = "Please Enter the Cwip Gl";
var check_mep_amount ="Check MEP Amount";
var reach_mep_amount ="Reach MEP Amount";
var update_mep ="Update MEP Values";
var add_mep ="Add MEP Values";

var from_date ="Please Enter From Date";
var from_time ="Please Enter From Time";
var to_date ="Please Enter To Date";
var totime ="Please Enter To Time";
var city ="Please Choose City";
var system_hours ="System Calc Hour Missing";
var noofhours ="Please Enter No of Hours";
var claimamount ="Please Enter Claimamount";
var eligibleamount ="Eliible Amount is Missing";
var noleavedays ="Please Enter No of Leave Days";

var code ="Please choose Mode of Travel";
var samedayreturn ="Please choose same Day Return";
var travelhours ="Please Enter Travel Hours";
var singlefare ="Please Enter Single Fare";
var expenses ="Expense Amount Missing";

var subcatogory ="Please choose Subcatogory";
var center ="Please choose Center";
var fromplace ="Please Enter From Place";
var toplace ="Please Enter To Place";
var onwardreturn ="Please choose OnWardReturn";
var remarks ="Please Enter Remarks";

var centreclassification ="Please choose Center Classification";
var placeofactualstay ="Please Enter Place of Actual Stay";
var checkindate ="Please Enter Checkindate";
var fr_time ="Please Enter CheckinTime";
var checkoutdate ="Please Enter Checkoutdate";
var to_time ="Please Enter CheckoutTime";
var lodgcheckoutdate ="Please Enter LodgCheckoutdate";
var lodgto_time ="Please Enter LodgCheckoutTime";
var noofdays ="Please Enter No of Days";
var accbybank = "Please choose Accomantation By Bank";
var billavailable ="Please choose Bill Available";
var totalbillamount ="Please Enter Total Bill Amount";
var taxonly ="Please Enter Taxonly";
var expreason ="Please choose Expense reason";
var description ="Please Enter Description";


var twowheelertrans ="Please choose Two wheeler transport";
var hhgoodstrans ="Please choose House Hold Goods Transport";
var transtwowheelerby ="Please choose Transport of Two wheeler";
var ibaappvendor ="Please Enter IBA Approved Vendor Name";
var vendorcode ="Please Enter Vendor Code";
var totaldisttrans ="Please Enter Total Distance(KM) For Transport ";
var distinhilly ="Please Enter Distance in Hilly Terrain";
var tonnagehhgood ="Please Enter Tonnage of Household Goods	";
var maxtonnage ="Max Eligible Tonnage Missing";
var billedamthhgoodstrans = "Please Enter Billed Amount for Household Goods Transport";
var eligtransamt ="Please Enter Eligible Transportation Amount";
var transchargesvehicle ="Please Enter Transport Charges for Vehicle";
var vehicletransbydriver ="Please Choose Vehicle Transported By Driver";
var traveltimeinhours ="Please Enter Travel Time In Hours(HH)";
var daysdrivereng ="No of Days Driver Engaged Missing";
var driverbatta ="Driver Battas Missing";
var octroivehicle ="Please Enter Octroi Charges for Transport of vehicle";
var breakagecharges ="Please Enter Breakage Charges";
var receiptlosses ="Please Choose Receipt for Losses Due To Damage Produced";
var eligbreakagecharge ="Eligible Breakage Charge Missing";

var depaturedate ="Please Enter Depaturedate";
var depaturetime ="Please Enter Depaturetime";
var depatureplace ="Please Enter Depatureplace";
var arrivaldate ="Please Enter Arrivaldate";
var arrivaltime ="Please Enter Arrivaltime";
var placeofvisit ="Please Enter Placeofvisit";
var totaltkttamt ="Please Enter Total Ticket Amount";
var tktbybank ="Please Choose Ticket By Bank";
var actualtravel ="Please Choose Actual Mode";
var class_travel ="Please Choose Class";
var highermodereasons ="Please Choose Higher Mode Reason";
var priorpermission ="Please Choose Priorpermission";
var highermodeopted ="Please Enter Who Has Opted Higher Mode ";
var noofdependents ="Please Enter No of Dependents";
var not_found_asstcat ="Asset Category Not Found";
var tour_not_end ="Tour expense claim can be submitted after the tour ended";
var CR_NO_Same ="Same CR NO also Get Rejected";



var time_toast =4000;

var warning_toast = function(data,type){
$.toast({
    heading: 'Warning',
    text: data,
    position: {
        right: 120,
        top: 120
    },
    showHideTransition: 'slide',
    hideAfter: type,
    icon: 'warning'
})
}
var success_toast = function(){
$.toast({
    heading: 'Success',
    text: done_msg,
    position: {
        right: 120,
        top: 120
    },
    allowToastClose: true,
    showHideTransition: 'slide',
    hideAfter: 3000,
    icon: 'success'
})
}
var error_toast = function(data,type){
$.toast({
    heading: 'Error',
    text: data,
    position: {
        right: 120,
        top: 120
    },
    showHideTransition: 'slide',
    hideAfter: type,
    icon: 'error'
})
}
var info_toast = function(data,type){
$.toast({
    heading: 'Information',
    text: data,
    position: {
        right: 120,
        top: 120
    },
    showHideTransition: 'slide',
    hideAfter: type,
    icon: 'info'
})
}