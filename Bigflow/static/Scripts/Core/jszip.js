var loginapp = angular.module('loginapp', ['ngMaterial']).config(function($httpProvider) {
    $httpProvider.defaults.xsrfCookieName = 'csrftoken';
    $httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken';
});

loginapp.controller("Logincnt", ['$scope', '$window', 'loginService', '$http','$mdDialog', function($scope, $window, loginService, $http,$mdDialog) {

    $scope.maintable = [];
    document.getElementById('Username').focus();

       $scope.loading = function() {
        $mdDialog.show({
            templateUrl: 'loaderSpinner',
            parent: angular.element(document.body),
            clickOutsideToClose: false
        });
    };

    $scope.endloading = function() {
        $mdDialog.hide();
    };

    function loadcheck() {
        var jsonData = {
            "employee_gid": $scope.maintable.employee_gid
        };
        var schedule_check = loginService.ipset('check', jsonData)
        schedule_check.then(function(result) {
            if (result.data > 0) {
               alert("'Kindly Logout' Session Before You Logged In!");
                if (r == true) {
                    $scope.chckid = result.data;
                } else {
                    return false;
                }
            } else if (result.data == 0) {
                load()
            } else {
                alert("Not Login Successfully!.");
            }
        }, function(err) {
            alert("Not Login Successfully!");
        });
    };

    function load() {
            var jsonData = {
                "employee_gid": $scope.maintable.employee_gid,
                "logingid": ''
            }
        var schedule_check = loginService.ipset('insert', jsonData)
        schedule_check.then(function(result) {
            if (result.data > 0) {
                sessionStorage.setItem('today', result.data);
                $window.location.href = "../welcome";
            } else {
                alert('User Name or Password Not Matched.');
            }
        }, function(err) {
            alert('User Name or Password Not Matched.');
        });
    };

     $scope.clear = function(){
        $scope.Username = '';
        $scope.Password = '';
    }

    $scope.Loginchk = function() {
     $scope.loading();
        var username = $scope.Username;
        var password = $scope.Password;
        var pswd = loginService.getlogin(username, password);
        pswd.then(function(result) {
                if (JSON.parse(result.data) != "FAIL") {
                    $scope.maintable = JSON.parse(result.data);
                    $scope.maintable.employee_gid = $scope.maintable.employee_gid;
                    load()
                } else {
                    alert('User Name or Password Not Matched.');
                }
            }).finally($scope.endloading)
    };

}]);

loginapp.service("loginService", function($http) {
    this.getlogin = function(e, e1) {
        var response = $http.post("/loginpswd/", {
            parms: {
                "TYPE":"LOGIN_AD",
                "username": e,
                "password": e1,
                "source":"AD"
            }
        });
        return response;
    }
    this.ipset = function(action, jsonData) {
        var response = $http.post("/setip_sys/", {
            parms: {
                "action": action,
                "jsonData": jsonData
            }
        });
        return response;
    }
});