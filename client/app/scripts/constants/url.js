'use strict';

angular.module('FYPClient').constant('URL', (function () {
    const BASE_URL = 'http://localhost:5000';
    const BASE_WEBSOCKET_URL = 'ws://localhost:5000';

    return {
        BASE_URL: BASE_URL,
        GET_RAW_DATA_URL: BASE_URL + '/client/raw',
        GET_LIST_OF_SUBJECTS_URL: BASE_URL + '/client/raw',
        WEBSOCKET_REAL_TIME_MONITORING_URL: BASE_WEBSOCKET_URL + '/client/ws' 
    };
})());