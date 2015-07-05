'use strict';


angular.module('myApp.Home', ['ngRoute'])
    .config(['$routeProvider', function($routeProvider) {
        $routeProvider.when('/home', {
            title : 'Home',
            templateUrl : 'modules/home/home.html',
            controller : 'HomeController'
        })
    }])

    .controller('HomeController', ['$scope', '$interval', 'DomainService',
        function ($scope, $interval, DomainService) {
            $scope.domains = {};
            $scope.inputDomain = "";
            $scope.loading = false;
            $scope.showUnregistered = true;

            $scope.updateTable = function() {
                var n = 0;

                // Check if we have unresolved domain entries
                for(n=0; n < $scope.domains.length; n++) {
                    if ( $scope.domains[n].isFullyResolved == false) {
                        DomainService.getPhishingDomainInfo($scope.domains[n].domain).success(function(data) {
                            // TODO FIXME FUCKING N CHANGES
                            for(var i=0; i<$scope.domains.length; i++) {
                                if ($scope.domains[i].domain == data.domain) {
                                    if (! angular.equals($scope.domains[i], data)) {
                                        $scope.domains[i] = data;
                                    }
                                }
                            }
                        });
                    }
                }
            }

            $interval( function() { $scope.updateTable(); }, 10000 );

            $scope.whois = function(domain) {
                DomainService.getWhoisFor(domain.domain).success(function(data) {
                    domain.whois = data.name;
                });

            }

            $scope.getDomains = function() {
                $scope.loading = true;
                $scope.domains = {};
                DomainService.getPhishDomainsFor($scope.inputDomain).success(function(data) {
                    $scope.domains = data.domains;
                    $scope.loading = false;
                });
            }

            $scope.toggleShowUnregistered = function() {
                $scope.showUnregistered = ! $scope.showUnregistered;

            }
        }
    ])
;

