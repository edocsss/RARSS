'use strict';

angular.module('FYPClient').factory('ActivityFactory',[
    '$rootScope',
    function ($rootScope) {
        let activityHistoryList = [{
            activity: 'DOING NOTHING',
            datetime: 'N/A N/A'
        }];

        $rootScope.$on('new_activity_data', function (e, data) {
            let activityType = data.activity.split('_').join(' ');
            let datetime = data.datetime;
            let activity = activityType.toUpperCase();
            
            activityHistoryList.unshift({
                activity: activity,
                datetime: datetime
            });
        });

        return {
            getActivityHistoryList: getActivityHistoryList
        };

        function getActivityHistoryList() {
            return activityHistoryList;
        }
    }
]);