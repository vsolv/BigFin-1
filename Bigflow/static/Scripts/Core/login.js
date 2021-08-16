var loginapp = angular.module('loginapp', ['ngMaterial']).config(function($httpProvider) {
    $httpProvider.defaults.xsrfCookieName = 'csrftoken';
    $httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken';
});

loginapp.controller("Logincnt", ['$scope', '$window', 'loginService', '$http','$mdDialog', function($scope, $window, loginService, $http,$mdDialog) {

// Credit: Mateusz Rybczonec
$scope.otp_validate = false;
const FULL_DASH_ARRAY = 283;
const WARNING_THRESHOLD = 10;
const ALERT_THRESHOLD = 5;

const COLOR_CODES = {
  info: {
    color: "green"
  },
  warning: {
    color: "orange",
    threshold: WARNING_THRESHOLD
  },
  alert: {
    color: "red",
    threshold: ALERT_THRESHOLD
  }
};

const TIME_LIMIT = 10;
//var timePassed = 0;
let timeLeft = TIME_LIMIT;
let timerInterval = null;
let remainingPathColor = COLOR_CODES.info.color;


function demoDisplay(){
document.getElementById("app").innerHTML = `
<div class="base-timer">
  <svg class="base-timer__svg" viewBox="0 0 100 100" xmlns="http://www.w3.org/2000/svg">
    <g class="base-timer__circle">
      <circle class="base-timer__path-elapsed" cx="50" cy="50" r="45"></circle>
      <path
        id="base-timer-path-remaining"
        stroke-dasharray="283"
        class="base-timer__path-remaining ${remainingPathColor}"
        d="
          M 50, 50
          m -45, 0
          a 45,45 0 1,0 90,0
          a 45,45 0 1,0 -90,0
        "
      ></path>
    </g>
  </svg>
  <span id="base-timer-label" class="base-timer__label">${formatTime(
    timeLeft
  )}</span>
</div>
`;
}
function onTimesUp() {
  clearInterval(timerInterval);
}

function startTimer(timePassed) {
  timerInterval = setInterval(() => {
    timePassed = timePassed += 1;
    timeLeft = TIME_LIMIT - timePassed;
    document.getElementById("base-timer-label").innerHTML = formatTime(
      timeLeft
    );
    setCircleDasharray();
    setRemainingPathColor(timeLeft);

    if (timeLeft === 0) {
      onTimesUp();
    }
  }, 1000);
}

function formatTime(time) {
  const minutes = Math.floor(time / 60);
  let seconds = time % 60;

  if (seconds < 10) {
    seconds = `0${seconds}`;
  }

  return `${minutes}:${seconds}`;
}

function setRemainingPathColor(timeLeft) {
  const { alert, warning, info } = COLOR_CODES;
  if (timeLeft <= alert.threshold) {
    document
      .getElementById("base-timer-path-remaining")
      .classList.remove(warning.color);
    document
      .getElementById("base-timer-path-remaining")
      .classList.add(alert.color);
  } else if (timeLeft <= warning.threshold) {
    document
      .getElementById("base-timer-path-remaining")
      .classList.remove(info.color);
    document
      .getElementById("base-timer-path-remaining")
      .classList.add(warning.color);
  }
}

function calculateTimeFraction() {
  const rawTimeFraction = timeLeft / TIME_LIMIT;
  return rawTimeFraction - (1 / TIME_LIMIT) * (1 - rawTimeFraction);
}

function setCircleDasharray() {
  const circleDasharray = `${(
    calculateTimeFraction() * FULL_DASH_ARRAY
  ).toFixed(0)} 283`;
  document
    .getElementById("base-timer-path-remaining")
    .setAttribute("stroke-dasharray", circleDasharray);
}

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
            };
        var schedule_check = loginService.ipset('insert', jsonData)
        schedule_check.then(function(result) {
            if (result.data > 0) {
                sessionStorage.setItem('today',  $scope.maindata);
                $window.location.href = "../bigfin/welcome";
            }
            else if (result.data == "User Already Logged-In.") {
                alert(result.data);
                sessionStorage.removeItem('today');
            }
             else {
                alert('User Code or Password Not Matched.');
            }
        }, function(err) {
            alert('User Code or Password Not Matched.');
        });
    };

$scope.clear = function(){

    $scope.Username = '';
    $scope.Password = '';
    if($scope.passwordCheckbox){
    $scope.passwordCheckbox = false;
    }
      $scope.inputType = 'password';
}

$scope.inputType ="password";
  $scope.hideShowPassword = function(){
    if ($scope.inputType == 'password')
      $scope.inputType = 'text';
    else
      $scope.inputType = 'password';
  };

    $scope.Login_chk_otp = function(){
    $scope.loading();
    var jsonData = {
                "mobileNumber": $scope.employee_mobileno,
                "otp": $scope.otp_number
            };
        var pswd = loginService.validate_api('VERIFY_OTP',jsonData);
        pswd.then(function(result) {
                if (result.data.ERRORCODE == "00") {
                load()
                }
                if(result.data.ERRORCODE == "16"){
                alert(result.data.Description);
                }
                if(result.data.ERRORCODE == "12"){
                alert(result.data.Description);
                }
                if(result.data.ERRORCODE == "13"){
                alert(result.data.Description);
                }
                if(result.data.ERRORCODE == "14"){
                alert(result.data.Description);
                }
            }).finally($scope.endloading)
    }

    function generate_otp() {
            var jsonData = {
                "mobileNumber": $scope.employee_mobileno,
            };
        var schedule_check = loginService.validate_api('GENERATE_OTP', jsonData)
        schedule_check.then(function(result) {
        startTimer(0);
        demoDisplay()
            if (result.data.ERRORCODE == "00") {
            return false;
            }
             if (result.data.ERRORCODE == "14") {
            alert(result.data.Description);
            return false;
            }
        }, function(err) {
            alert('Click to Resend OTP.');
        });
    };

    $scope.clk_resend_otp = function() {
    $scope.loading();
            var jsonData = {
                "mobileNumber": $scope.employee_mobileno,
            };
        var schedule_check = loginService.validate_api('GENERATE_OTP', jsonData)
        schedule_check.then(function(result) {

          if (result.data.ERRORCODE == "00") {
startTimer(0);
        demoDisplay();
            }
            if (result.data.ERRORCODE == "14") {
            alert(result.data.Description);
            return false;
            }
        }, function(err) {
            alert('Click to Resend OTP');
        }).finally($scope.endloading);
    };



    $scope.Loginchk = function() {
     $scope.loading();
        var username = $scope.Username;
        var password = $scope.Password;
        var pswd = loginService.getlogin(username, password);
        pswd.then(function(result) {
                if (JSON.parse(result.data) == "No Branch") {
                alert(JSON.parse(result.data));
                return false;
                } if(JSON.parse(result.data) == "FAIL") {
                    alert('User Code or Password Not Matched.');
                    return false;
                }
                else{
                  $scope.maindata = result.data;
                    $scope.maintable = JSON.parse(result.data);
                    $scope.maintable.employee_gid = $scope.maintable.employee_gid;
                    $scope.employee_mobileno = $scope.maintable.employee_mobileno;
                    if($scope.maintable.OTP_Validate =='0'){
                     load()
                     return false;
                    }
                    if($scope.employee_mobileno == null){
                    sessionStorage.removeItem('today');
                    alert('You are trying to login from outside KVB environment. Kindly access the WISEFIN via KVB environment and update your mobile number in the UPDATE MOBILE NUMBER for getting the OTP.')
                    return false;
                    }
                    else{
                    $scope.employee_mob_display = $scope.employee_mobileno.slice(6, 10);
                    $scope.otp_validate = true;
                      generate_otp();
                    }
                }
            }).finally($scope.endloading)
    };



}]);

loginapp.service("loginService", function($http) {
    this.getlogin = function(e, e1) {
        var response = $http.post("/bigfin/loginpswd/", {
            parms: {
                "TYPE":"LOGIN_LOCAL",
                "username": e,
                "password": e1,
                "source":"AD"
            }
        });
        return response;
    }

    this.ipset = function(action, jsonData) {
        var response = $http.post("/bigfin/setip_sys/", {
            parms: {
                "action": action,
                "jsonData": jsonData
            }
        });
        return response;
    }
     this.validate_api = function(action, jsonData) {
        var response = $http.post("/otp_genrte_validte/", {
            parms: {
                "action": action,
                "jsonData": jsonData
            }
        });
        return response;
    }
});
