'use strict';

angular.module('FYPClient').controller('ToolbarController', [
    '$mdSidenav',
    'ELEMENT_ID',
    function ($mdSidenav, ELEMENT_ID) {
        var vm = this;

        vm.openSideNav = function () {
            $mdSidenav(ELEMENT_ID.SIDENAV).toggle();
        };
    }
]);