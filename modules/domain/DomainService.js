'use strict'

angular.module('myApp.Domain', ['ngRoute'])

.factory("DomainService", ['$http', function($http) {
    var serviceBase = '/service/myphish/api/v1.0/';
    var obj = {};

    obj.getPhishDomainsFor = function(domain) {
        return $http.jsonp("" + serviceBase + "domain/" + domain + "?jsonp=JSON_CALLBACK");
    }

    return obj;
}])
;
