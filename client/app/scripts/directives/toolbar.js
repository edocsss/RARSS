'use strict';

angular.module('FYPClient').directive('toolbar', function () {
    return {
        restrict: 'E',
        controller: 'ToolbarController',
        controllerAs: 'toolbarController',
        templateUrl: 'views/toolbar.html'
    };
});