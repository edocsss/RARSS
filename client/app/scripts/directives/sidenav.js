'use strict';

angular.module('FYPClient').directive('sidenav', function () {
    return {
        restrict: 'E',
        controller: 'SidenavController',
        controllerAs: 'sidenavController',
        templateUrl: 'views/sidenav.html'
    };
});