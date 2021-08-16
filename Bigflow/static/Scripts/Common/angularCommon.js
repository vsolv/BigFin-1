var commonApp = angular.module('AppCommon', []);
commonApp.controller('CtrlCommon', ['$scope', function($scope) {}]);
commonApp.controller('DialogController', ['$scope', '$mdDialog', 'SerCommon', '$filter','dialogData', function($scope, $mdDialog,
  SerCommon,$filter, dialogData) {
  if (dialogData.action == 'employee') {
    employeeDetails(dialogData.emp_gid)
  }
   else if(dialogData.action == 'custmercont'){
    custmercont(dialogData);
  }
  else if(dialogData.action == 'productdetails'){
    prodview(dialogData);
  }
  else if(dialogData.action == 'select_supplier'){
    select_suppliers(dialogData);
  }
  else if(dialogData.action == 'select_product'){
    select_products(dialogData);
  }
  else if(dialogData.action == 'select_employee'){
    select_employee(dialogData);
  }
  else if(dialogData.action == 'FET_REPORT'){
    select_FETROUTE('FET_DAY_ROUTE',dialogData.emp_gid,dialogData.date,dialogData.todate);
  }
  else if(dialogData.action == 'FET_LOGIN'){
    select_FETLOGIN('EMPLOYEE',dialogData.type,dialogData.json);
  }
  else if(dialogData.action == 'select_clas'){
    select_clasification('BRANCH_SALES','BILLING','SALES',dialogData.Params);
  }

//for sale index page
    $scope.getbranch = gotobranch;
    $scope.branchchange = function(item){
    $scope.branchlist = item.lj_godown_data;
    $scope.selectedItm = "";
    }

    $scope.getbranches = gotobranches;
    function gotobranch(query) {
            var result = $filter('filter')($scope.getclasification, {
                'Godown_Name': query
            });
            return result;
        }

     function gotobranches(query) {
                var result = $filter('filter')($scope.getclasification, {
                    'branch_name': query
                });
                return result;
            }
//end here

    $scope.senddata=function(){
    var data =[$scope.selectedone,$scope.selectedItm]
        hideDialog(data);
    };

  function employeeDetails(emp_gid) {
    var get_employ = SerCommon.getemployee(dialogData.emp_gid, '', 0,'ALL')
    get_employ.then(function(result) {
      var empsmry = result.data;
      if (empsmry.length != 0) {
      $scope.shwemp = true;
        $scope.emp_name = empsmry[0].employee_name;
        $scope.emp_doj = empsmry[0].employee_doj;
        $scope.emp_gendr = empsmry[0].employee_gender;
        $scope.emp_mobnum = empsmry[0].employee_mobileno;
        $scope.emp_mailid = empsmry[0].employee_emailid;
      }
    }, function(err) {
      alert('No data!.');
    });
  }


    function custmercont(e){
        $scope.shwcust = true;
        $scope.cus_name = e.cus_name;
        $scope.lanlinenum = e.landline;
        $scope.mob_num = e.mobilenum;
      }

    function prodview (e){
        $scope.shwproduct = true;
        $scope.prod_name = e.prod_name;
        $scope.prod_displayname=e.prod_displayname;
        $scope.prod_unitprice=e.prod_unitprice;
        $scope.prod_weight=e.prod_weight;
        $scope.prodtype_name=e.prodtype_name;
    }



  $scope.cancelDialog = function() {
      $mdDialog.cancel();
  };

  $scope.cancelDial = function() {
      $mdDialog.cancel();
  };

  $scope.cancelDialogproduct = function() {

      $mdDialog.cancel();
  }

  function select_FETROUTE(action,emp_gid,date,todate){
     var data = SerCommon.getlocation(action,emp_gid,date,todate);
         data.then(function(res) {
             $scope.getroutedetails = res.data;
         }, function(err) {
             alert(err);
         });
  }

  function select_FETLOGIN(action,type,json){
    $scope.logindetemp=[];
  var data = SerCommon.getlogindetails(action, '', json);
            data.then(function(res) {
            $scope.logindetails=[];
            $scope.logindetemp=[];
                    $scope.logindetails=res.data.DATA;
                    angular.forEach($scope.logindetails,function(user,key){
                        if(user.login_devicedetails){
                         $scope.logindetemp.push(JSON.parse(user.login_devicedetails));
                         $scope.logindetemp[$scope.logindetemp.length-1].date=user.date;
                         $scope.logindetemp[$scope.logindetemp.length-1].emp_name=user.employee_name;
                         }else{
                         $scope.logindetemp.push({'data':user.date,'emp_name':user.employee_name});
                         }
                    });
            }, function(err) {
                alert(err);
            })
   }

   function select_clasification(Group,Type,SubType,data){
     var dta = {
                Group: Group,
                Type:Type,
                SubType: SubType,
                data: data
            }
   $scope.getclasification = [];
        var getcompaig = SerCommon.getclasification(dta)
            getcompaig.then(function(result) {
                $scope.getclasification = result.data.DATA;
                for(i=0;i<$scope.getclasification.length;i++){
                var empname = $scope.getclasification[i].employee_name;
                $scope.getclasification[i].lj_godown_data = JSON.parse($scope.getclasification[i].lj_godown_data)
                if(empname != ""){
                 $scope.selectedone = $scope.getclasification[i];
                var d = $scope.getclasification[i]
                $scope.branchchange(d);
//             $scope.selectedItm = $scope.getclasification[i].lj_godown_data[0].Godown_Name;
                }
                }
            }, function(err) {
                alert('No data!.');
            }).finally();
        }

function select_employee(data){
    $scope.is_multiple=data.isMultiple;
     var get_supplier = SerCommon.getdropdown('employee', 0,'')
     get_supplier.then(function(response){
        $scope.bindingList=[];
        $scope.bindingList=JSON.parse(response.data);
        if(data.selectedData){
            reselectList(data);
        }
     },function(err){
        alert('No data!.');
     })
};

function reselectList(data){
    if(data.isMultiple){
        for( i=0;i<data.selectedData.length;i++){
            var temp=$filter('filter')($scope.bindingList,{employee_gid:data.selectedData[i].employee_gid},true)
            var index=$scope.bindingList.indexOf(temp[0]);
            $scope.bindingList[index].is_checked=true;
        }
    }
    else{
        var temp=$filter('filter')($scope.bindingList,{employee_gid:data.selectedData.employee_gid},true)
        var index=$scope.bindingList.indexOf(temp[0]);
        $scope.bindingList[index].is_checked=true;
    }
};
function displayLocation(user,type,latitude, longitude) {
            var request = new XMLHttpRequest();
            var location='';
            var method = 'GET';
            var url = 'https://maps.googleapis.com/maps/api/geocode/json?latlng='
                    + latitude + ',' + longitude + '&sensor=true';
            var async = true;

            request.open(method, url, async);
            request.onreadystatechange = function() {
                if (request.readyState == 4 && request.status == 200) {
                    var data = JSON.parse(request.responseText);
                    var address = data.results[0];
                    var value = address.formatted_address.split(",");

                    count = value.length;
                    country=value[count-1];
                    state = value[count - 2];
                    city = value[count - 3];
                    location = value[count - 4];

                }
            };

            request.send();
            return location;
        };

    $scope.row_click=function(clicked_data){
        if (!$scope.is_multiple){
             hideDialog(clicked_data);
        }
    };

    $scope.submitData=function(){
        var data=[];
        data=$filter('filter')($scope.bindingList,{is_checked:true},true)
        hideDialog(data);
    };

$scope.submitproddata=function(){
    var data=[];
    data=$filter('filter')($scope.bindingList,{is_checked:true},true)
    hideDialog(data);
};

  function select_suppliers(data){
  $scope.is_multiple=data.isMultiple;
     var get_supplier = SerCommon.getdropdown('supplier',  0,'')
     get_supplier.then(function(response){
        $scope.bindingList=[];
        $scope.bindingList=JSON.parse(response.data);
        if(data.selectedData){
            sup_reselectList(data);
        }
     },function(err){
        alert('No data!.');
     })
  };

  function select_products(data){
  $scope.is_multiple=data.isMultiple;
     var get_product = SerCommon.getdropdown('product',  0,'')
     get_product.then(function(response){
        $scope.bindingList=[];
        $scope.bindingList=JSON.parse(response.data);
        if(data.selectedData){
        pro_reselectList(data);
        }
     },function(err){
        alert('No data!.');
     })
  };
  function sup_reselectList(data){
    if(data.isMultiple){
        for( i=0;i<data.selectedData.length;i++){
            var temp=$filter('filter')($scope.bindingList,{supplier_gid:data.selectedData[i].supplier_gid},true)
            var index=$scope.bindingList.indexOf(temp[0]);
            $scope.bindingList[index].is_checked=true;
        }
    }
    else{
        var temp=$filter('filter')($scope.bindingList,{supplier_gid:data.selectedData.supplier_gid},true)
        var index=$scope.bindingList.indexOf(temp[0]);
        $scope.bindingList[index].is_checked=true;
    }
  };
  function pro_reselectList(data){
    if(data.isMultiple){
        for( i=0;i<data.selectedData.length;i++){
            var temp=$filter('filter')($scope.bindingList,{product_gid:data.selectedData[i].product_gid},true)
            var index=$scope.bindingList.indexOf(temp[0]);
            $scope.bindingList[index].is_checked=true;
        }
    }
    else{
        var temp=$filter('filter')($scope.bindingList,{product_gid:data.selectedData.product_gid},true)
        var index=$scope.bindingList.indexOf(temp[0]);
        $scope.bindingList[index].is_checked=true;
    }
  };
function hideDialog(data){
    $mdDialog.hide(data);
}

  $scope.checkSupplier=function(sup){
    $mdDialog.hide(sup);
  };

}]);
commonApp.service("SerCommon", function($http) {
  this.getemployee = function(gid, name, clusgid,cluster) {
    var response = $http.get(Appname + "/employee_get/", {
      params: {
        "emp_gid": gid,
        "emp_name": name,
        "li_cluster_gid": clusgid,
         "cluster": cluster
      }
    });
    return response;
  }


  this.getposition = function(action, emp_gid, date,todate) {
    var response = $http.get(Appname + "/getposition/", {
        params: {
            "action": action,
            "emp_gid": emp_gid,
            "date": date,
            "todate":todate,
        }
    });
    return response;
   }

   this.getlocation = function(action, emp_gid, date,todate) {
    var response = $http.get(Appname + "/getdayroute/", {
        params: {
            "action": action,
            "emp_gid": emp_gid,
            "date": date,
            "todate":todate,
        }
    });
    return response;
   }

   this.getdropdown = function(table_name, gid, name) {
    var response = $http.get(Appname + "/dropdowndata/", {
        params: {
            "table_name": table_name,
            "search_gid": gid,
            "search_name": name,
        }
    });
    return response;
   }
    this.getclasification = function(custid) {
        var respons = $http.post(Appname + "/getclasification/",
            custid
        );
        return respons;
    }
 this.getcustomer = function(jsonData) {
    var response = $http.get(Appname +"/customer_ddl/", {
      params: {
            "jsonData": jsonData
      }
    });
    return response;
  }

   this.getemp_customer = function(action,gid) {
    var response = $http.get(Appname +"/emp_mapped_customer/", {
      params: {
        "action":action,
        "emp_gid": gid
      }
    });
    return response;
  }
  this.getoutstanding = function (action,cust_gid,f_date,t_date,emp_gid,row_limit) {
       var response = $http.get(Appname+"/outstanding_fet_get/",{
       params:{
       "action":action,
       "cust_gid":cust_gid,
       "f_date":f_date,
       "t_date":t_date,
       "emp_gid":emp_gid,
       "row_limit":row_limit
       }});
       return response;
  }

   this.getday = function(action,emp_gid,date,todate) {
            var response = $http.get(Appname + "/getdayroute/", {
                params: {
                    "action": action,
                     "emp_gid": emp_gid,
                     "date": date,
                     "todate":todate,
                }
            });
            return response;
        };

    this.getlogindetails=function(action,type,jsondata){
            var response=$http.get(Appname+"/getLogindetails/",{
                params:{
                    "Action":action,
                    "Type":type,
                    "Json":jsondata

                }
            });
             return response;
        };


  this.new_toast=function(type,msg){
    var value ={
        template: '<md-toast class="md-toast-'+ type +'">' + msg + '</md-toast>',
        parent:document.querySelectorAll('#div_toast'),
        hideDelay: 5000,
        position: 'top right'
    };
    return value;
  }
});
commonApp.config(function() {});

commonApp.directive('onlyLettersInput', onlyLettersInput);//Only letters only
commonApp.directive('numbersOnly', numbersOnly);
commonApp.directive('validNumber', validNumber);
commonApp.directive('noSpecialChar', noSpecialChar);
commonApp.directive('capitalize', capitalize);
commonApp.directive('excelExport', excelExport);
function numbersOnly() {
  return {
    require: 'ngModel',
    link: function(scope, element, attr, ngModelCtrl) {
      function fromUser(text) {
        if (text) {
          var transformedInput = text.replace(/[^0-9]/g, '');
          if (transformedInput !== text) {
            ngModelCtrl.$setViewValue(transformedInput);
            ngModelCtrl.$render();
          }
          return transformedInput;
        }
        return undefined;
      }
      ngModelCtrl.$parsers.push(fromUser);
    }
  };
};
function onlyLettersInput() {
  return {
    require: 'ngModel',
    link: function(scope, element, attr, ngModelCtrl) {
      function fromUser(text) {
        var transformedInput = text.replace(/[^a-zA-Z]/g, '');
        //console.log(transformedInput);
        if (transformedInput !== text) {
          ngModelCtrl.$setViewValue(transformedInput);
          ngModelCtrl.$render();
        }
        return transformedInput;
      }
      ngModelCtrl.$parsers.push(fromUser);
    }
  };
};

 function validNumber() {
  return {
    require: '?ngModel',
    link: function(scope, element, attrs, ngModelCtrl) {
      if (!ngModelCtrl) {
        return;
      }
      ngModelCtrl.$parsers.push(function(val) {
        if (angular.isUndefined(val)) {
          var val = '';
        }
        var clean = val.replace(/[^-0-9\.]/g, '');
        var negativeCheck = clean.split('-');
        var decimalCheck = clean.split('.');
        if (!angular.isUndefined(negativeCheck[1])) {
          negativeCheck[1] = negativeCheck[1].slice(0, negativeCheck[1].length);
          clean = negativeCheck[0] + '-' + negativeCheck[1];
          if (negativeCheck[0].length > 0) {
            clean = negativeCheck[0];
          }
        }
        if (!angular.isUndefined(decimalCheck[1])) {
          decimalCheck[1] = decimalCheck[1].slice(0, 2);
          clean = decimalCheck[0] + '.' + decimalCheck[1];
        }
        if (val !== clean) {
          ngModelCtrl.$setViewValue(clean);
          ngModelCtrl.$render();
        }
        return clean;
      });
      element.bind('keypress', function(event) {
        if (event.keyCode === 32) {
          event.preventDefault();
        }
      });
    }
  };
};


 function capitalize() {
    return {
      require: 'ngModel',
      link: function(scope, element, attrs, modelCtrl) {
        var capitalize = function(inputValue) {
          if (inputValue == undefined) inputValue = '';
          var capitalized = inputValue.toUpperCase();
          if (capitalized !== inputValue) {
            // see where the cursor is before the update so that we can set it back
            var selection = element[0].selectionStart;
            modelCtrl.$setViewValue(capitalized);
            modelCtrl.$render();
            // set back the cursor after rendering
            element[0].selectionStart = selection;
            element[0].selectionEnd = selection;
          }
          return capitalized;
        }
        modelCtrl.$parsers.push(capitalize);
        capitalize(scope[attrs.ngModel]); // capitalize initial value
      }
    };
  };

 function noSpecialChar() {
    return {
      require: 'ngModel',
      restrict: 'A',
      link: function(scope, element, attrs, modelCtrl) {
        modelCtrl.$parsers.push(function(inputValue) {
          if (inputValue == null)
            return ''
          cleanInputValue = inputValue.replace(/[^\w\s]/gi, '');
          if (cleanInputValue != inputValue) {
            modelCtrl.$setViewValue(cleanInputValue);
            modelCtrl.$render();
          }
          return cleanInputValue;
        });
      }
    }
  };

function excelExport() {
  return {
    restrict: 'A',
    scope: {
        fileName: "@",
        data: "&exportData"
    },
    replace: true,
    template: '<button class="btn btn-primary btn-ef btn-ef-3 btn-ef-3c mb-10" ng-click="download()"> Excel <i class="fa fa-download"></i></button>',
    link: function (scope, element) {

        scope.download = function() {

            function datenum(v, date1904) {
                if(date1904) v+=1462;
                var epoch = Date.parse(v);
                return (epoch - new Date(Date.UTC(1899, 11, 30))) / (24 * 60 * 60 * 1000);
            };

            function getSheet(data, opts) {
                var ws = {};
                var range = {s: {c:10000000, r:10000000}, e: {c:0, r:0 }};
                for(var R = 0; R != data.length; ++R) {
                    for(var C = 0; C != data[R].length; ++C) {
                        if(range.s.r > R) range.s.r = R;
                        if(range.s.c > C) range.s.c = C;
                        if(range.e.r < R) range.e.r = R;
                        if(range.e.c < C) range.e.c = C;
                        var cell = {v: data[R][C] };
                        if(cell.v == null) continue;
                        var cell_ref = XLSX.utils.encode_cell({c:C,r:R});

                        if(typeof cell.v === 'number') cell.t = 'n';
                        else if(typeof cell.v === 'boolean') cell.t = 'b';
                        else if(cell.v instanceof Date) {
                            cell.t = 'n'; cell.z = XLSX.SSF._table[14];
                            cell.v = datenum(cell.v);
                        }
                        else cell.t = 's';

                        ws[cell_ref] = cell;
                    }
                }
                if(range.s.c < 10000000) ws['!ref'] = XLSX.utils.encode_range(range);
                return ws;
            };

            function Workbook() {
                if(!(this instanceof Workbook)) return new Workbook();
                this.SheetNames = [];
                this.Sheets = {};
            }

            var wb = new Workbook(), ws = getSheet(scope.data());
            /* add worksheet to workbook */
            wb.SheetNames.push(scope.fileName);
            wb.Sheets[scope.fileName] = ws;
            var wbout = XLSX.write(wb, {bookType:'xlsx', bookSST:true, type: 'binary'});

            function s2ab(s) {
                var buf = new ArrayBuffer(s.length);
                var view = new Uint8Array(buf);
                for (var i=0; i!=s.length; ++i) view[i] = s.charCodeAt(i) & 0xFF;
                return buf;
            }

            saveAs(new Blob([s2ab(wbout)],{type:"application/octet-stream"}), scope.fileName+'.xlsx');

        };

    }
  };
}