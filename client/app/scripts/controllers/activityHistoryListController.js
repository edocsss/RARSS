'use strict';

angular.module('FYPClient').controller('ActivityHistoryListController', [
    'ActivityFactory',
    function (ActivityFactory) {
        let vm = this;
        vm.activityHistoryList = ActivityFactory.getActivityHistoryList();
        vm.query = {
            order: '',
            limit: 10,
            page: 1
        };
    }
]);