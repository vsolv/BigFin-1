$scope.add_ccbs = function(i,e){
        if(e.claimedamount != 0){
            $scope.arr_index = i;
            $scope.claimamount = e.claimedamount;
                $scope.choices = [{
                exp_amt:"",
                exp_percentage:""}];
                modalshow('viewmodals');
            }
    }
    bsdata();
    function bsdata(){
        var data = {
            params: {
                "Type": "BS"
            }
        };
        var get_bs_data = eclaimService.drop_data(data)
            get_bs_data.then(function(result) {
                $scope.main = result.data.DATA;
                $scope.get_bs = $scope.main;
            })
    }
    $scope.querySearchcc = gotocc;
    function gotocc(query) {
        var result = $filter('filter')($scope.get_cc, {
            'cc_name': query
        });
        return result;
    }

    $scope.bschange = function(bs){
        var data = {
            params: {
                "Type": "CC",
                "Bs_gid": bs.bs_gid
            }
        };
        var get_cc_data = eclaimService.drop_data(data)
        get_cc_data.then(function(result) {
            $scope.main = result.data.DATA;
            $scope.get_cc = $scope.main;
        })
    }

    $scope.querySearchbs = gotobs;
    function gotobs(query) {
        var result = $filter('filter')($scope.get_bs, {
            'bs_name': query
        });
        return result;
    }

    $scope.percen_calc = function(i,v){
        var value = (v / $scope.claimamount)*100;
        $scope.choices[i].exp_percentage = value;
    }

    $scope.amount_calc = function(i,v){
        var value = (v /100)* $scope.claimamount;
        $scope.choices[i].exp_amt = value;
    }
    $scope.removeChoice = function() {
        var lastItem = $scope.choices.length-1;
        $scope.choices.splice(lastItem);
        $scope.add_asset = false;
    };
    $scope.addNewChoice = function() {
        var sum = 0;
        for (i = 0; i < $scope.choices.length; i++) {
            sum = parseFloat(sum) + parseFloat($scope.choices[i].exp_amt);
        }
            if (sum > $scope.claimamount){
                $scope.add_asset = true;
                var len = $scope.choices.length - 1;
                $scope.choices[len].exp_amt ="";
                $scope.choices[len].exp_percentage ="";
                warning_toast(not_matched,time_toast);
            }
            else if(sum < $scope.claimamount){
                var newItemNo = $scope.choices.length+1;
                $scope.len_asset = $scope.len_asset + 1;
                $scope.choices.push({
                exp_amt:"",
                exp_percentage:""});
            }
            else if(sum == $scope.claimamount){
                $scope.enable_update = false;
                $scope.reason = true;
            }
            else {
               error_toast(no_data,time_toast);
            }
    };

    $scope.ccbs_save = function(){
        var sum = 0;
        for (i = 0; i < $scope.choices.length; i++) {
            sum = parseFloat(sum) + parseFloat($scope.choices[i].exp_amt);
        }
            if (sum == $scope.claimamount){
                angular.forEach($scope.choices, function(item1) {
                    var data = {
                        "gid":"0",
                        "ccgid":item1.selectedcc.cc_gid,
                        "bsgid":item1.selectedbs.bs_gid,
                        "percentage":item1.exp_percentage,
                        "amount":item1.exp_amt
                    }
                     $scope.eClaim_dailys[$scope.arr_index].CCBS.push(data);
                });
                success_toast();
                modalhide('viewmodals');
            }
            else{
                error_toast(no_data,time_toast);
            }
    }