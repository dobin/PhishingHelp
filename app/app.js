'use strict'

var app = angular.module('myApp', [
    'ngRoute',
    'ngTable',
    'ngTagsInput',
    'ngSanitize',
    'ui.select',
    'ui.bootstrap',
    'myApp.Domain',
    'myApp.Home',
    'ngCookies']);

app.config(['$routeProvider', function($routeProvider) {
    $routeProvider.otherwise({
        redirectTo : '/home'
    });
}]);


// Index
app.controller('indexCtrl', function($scope) {

});