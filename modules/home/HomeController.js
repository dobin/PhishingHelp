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

            $scope.updateTable = function() {
                var n = 0;

                // Check if we have unresolved domain entries
                for(n=0; n < $scope.domains.length; n++) {
                    if ( $scope.domains[n].isFullyResolved == false) {
                        DomainService.getPhishingDomainInfo($scope.domains[n].domain).success(function(data) {
                            if (data.isFullyResolved == true) {
                                // TODO FIXME FUCKING N CHANGES
                                for(var i=0; i<$scope.domains.length; i++) {
                                    if ($scope.domains[i].domain == data.domain) {
                                        $scope.domains[i] = data;
                                        console.log("Resolve: " + i + " : " + data.domain);
                                    }

                                }
                            }
                        });
                    }
                }

                console.log("blerg");
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
        }
    ])
    /*
    .directive('myCurrentTime', ['$interval', 'dateFilter',
        function($interval, dateFilter) {
            // return the directive link function. (compile function not needed)
            return function(scope, element, attrs) {
                var format,  // date format
                    stopTime; // so that we can cancel the time updates

                // used to update the UI
                function updateTime() {
                    element.text(dateFilter(new Date(), format));
                }

                // watch the expression, and update the UI on change.
                scope.$watch(attrs.myCurrentTime, function(value) {
                    format = value;
                    updateTime();
                });

                stopTime = $interval(updateTime, 1000);

                // listen on DOM destroy (removal) event, and cancel the next UI update
                // to prevent updating time after the DOM element was removed.
                element.on('$destroy', function() {
                    $interval.cancel(stopTime);
                });
            }
        }])
*/
;


;

