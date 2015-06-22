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

            $scope.whois = function(domain) {
                DomainService.getWhoisFor(domain.domain).success(function(data) {
                    domain.whois = data.name;
                });

            }
/*
            $.ajax({
                 url: 'http://www.whoisxmlapi.com/whoisserver/WhoisService',
                 dataType: 'jsonp',
                 data: {
                 domainName: 'stackoverflow.com',
                 outputFormat: 'json'
                 },
                 success: function(data) {
                     console.log(data.WhoisRecord);
                 }
                 });

*/
            $scope.getDomains = function() {
                $scope.loading = true;
                $scope.domains = {};
                DomainService.getPhishDomainsFor($scope.inputDomain).success(function(data) {
                    $scope.domains = data.domains;
                    $scope.loading = false;

                    for(var i=0; i<$scope.domains.length; i++) {
                    }
                });



            }
        }
    ]);

