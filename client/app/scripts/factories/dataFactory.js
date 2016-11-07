'use strict';

angular.module('FYPClient').factory('DataFactory', [
    '$http',
    'URL',
    function ($http, URL) {
        return {
            loadRawDataByActivityAndSource: loadRawDataByActivityAndSource,
            getListOfSubjects: getListOfSubjects
        };

        function loadRawDataByActivityAndSource(activityType, dataSource, dataSubject) {
            var httpOptions = {
                method: 'POST',
                url: URL.GET_RAW_DATA_URL,
                data: {
                    activityType: activityType,
                    dataSource: dataSource,
                    dataSubject: dataSubject
                }
            };

            return $http(httpOptions);
        }

        function getListOfSubjects() {
            var httpOptions = {
                method: 'GET',
                url: URL.GET_LIST_OF_SUBJECTS_URL
            };

            return $http(httpOptions);
        }
    }
]);