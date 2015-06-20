'use strict';


angular.module('myApp.Home', ['ngRoute'])
    .config(['$routeProvider', function($routeProvider) {
        $routeProvider.when('/home', {
            title : 'Home',
            templateUrl : 'modules/home/home.html',
            controller : 'HomeController'
        })
    }])

    .controller('HomeController', ['$scope', 'DomainService',
        function ($scope, DomainService) {
            $scope.domains = {};
            $scope.inputDomain = "";
            $scope.loading = false;

            $scope.getDomains = function() {
                $scope.loading = true;
                $scope.domains = {};
                DomainService.getPhishDomainsFor($scope.inputDomain).success(function(data) {
                    $scope.domains = data.domains;
                    $scope.loading = false;
                });
            }
        }
    ]);

