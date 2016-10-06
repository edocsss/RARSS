'use strict';

angular.module('FYPClient').factory('RawDataFactory', [
    '$http',
    'URL',
    function ($http, URL) {
        return {
            loadRawDataByActivityAndSource: loadRawDataByActivityAndSource
        };

        function loadRawDataByActivityAndSource(activityType, dataSource) {
            var httpOptions = {
                method: 'POST',
                url: URL.RAW_DATA_URL,
                data: {
                    activityType: activityType,
                    dataSource: dataSource
                }
            };

            return $http(httpOptions);
        }
    }
]);