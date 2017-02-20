'use strict';

angular.module('FYPClient').factory('ActivityFactory',[
    '$rootScope',
    function ($rootScope) {
        const SMOOTHING_WINDOW_SIZE = 5;
        const HALF_SMOOTHING_WINDOW_SIZE = Math.floor(SMOOTHING_WINDOW_SIZE / 2);
        const STARTING_INDEX = Math.ceil(SMOOTHING_WINDOW_SIZE / 2);
        let currentSmoothingIndex = STARTING_INDEX;

        let activityHistoryList = [{
            activity: 'DOING NOTHING',
            datetime: 'N/A N/A'
        }];

        $rootScope.$on('new_activity_data', function (e, data) {
            let activityType = data.activity.split('_').join(' ');
            let datetime = data.datetime;
            let activity = activityType.toUpperCase();

            if (activityHistoryList.length >= SMOOTHING_WINDOW_SIZE) {
                smoothActivityHistoryList();
            }

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

        function smoothActivityHistoryList() {
            let counter = {};
            let startIndex = currentSmoothingIndex - HALF_SMOOTHING_WINDOW_SIZE;
            let endIndex = currentSmoothingIndex + HALF_SMOOTHING_WINDOW_SIZE;
            let activity;
            let maxActivity;
            let maxActivityCounter = -1;

            // Count activity occurence
            for (let i = startIndex; i <= endIndex; i++) {
                activity = activityHistoryList[i].activity;
                if (!counter.hasOwnProperty(activity)) {
                    counter[activity] = 0;
                }

                counter[activity]++;
            }

            // Find most common activity
            for (let a in counter) {
                if (counter[a] > maxActivityCounter) {
                    maxActivityCounter = counter[a];
                    maxActivity = a;
                }
            }

            // Smooth activity history
            activityHistoryList[currentSmoothingIndex].activity = maxActivity;
            currentSmoothingIndex++;
        }
    }
]);
