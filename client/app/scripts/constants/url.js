'use strict';

angular.module('FYPClient').constant('URL', (function () {
    var BASE_URL = 'http://localhost:5000';
    return {
        BASE_URL: BASE_URL,
        GET_RAW_DATA_URL: BASE_URL + '/client/raw',
        GET_LIST_OF_SUBJECTS_URL: BASE_URL + '/client/raw'
    };
})());