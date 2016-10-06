'use strict';

angular.module('FYPClient').controller('SidenavController', [
    '$state',
    '$mdSidenav',
    'ELEMENT_ID',
    function ($state, $mdSidenav, ELEMENT_ID) {
        var vm = this;

        vm.getActiveState = function () {
            return $state.current.name;
        };

        vm.openPage = function (stateName) {
            $state.go(stateName);
            $mdSidenav(ELEMENT_ID.SIDENAV).toggle();
        };
    }
]);