'use strict'

angular.module('myApp.Domain', ['ngRoute'])

.factory("DomainService", ['$http', function($http) {
        var serviceBase = '/service/myphish/api/v1.0/';
        var obj = {};

        obj.getPhishDomainsFor = function(domain) {
            return $http.jsonp("" + serviceBase + "domain/" + domain + "?jsonp=JSON_CALLBACK");
        }

        obj.getPhishingDomainInfo = function(domain) {
            return $http.jsonp("" + serviceBase + "domainInfo/" + domain + "?jsonp=JSON_CALLBACK");
        }

        obj.getWhoisFor = function(domain) {
            return $http.get("" + serviceBase + "whois/" + domain);
        }

        return obj;
}])
;
