'use strict';

angular.module('FYPClient').factory('WebsocketFactory',[
    '$rootScope',
    '$websocket',
    '$log',
    'URL',
    function ($rootScope, $websocket, $log, URL) {
        let socket;
        return {
            init: init,
            tearDown: tearDown
        };

        function init() {
            socket = $websocket(URL.WEBSOCKET_REAL_TIME_MONITORING_URL);
            
            socket.onMessage(function (message) {
                let data = JSON.parse(message.data);
                $rootScope.$broadcast('new_activity_data', data);   
            });

            socket.onClose(function () {
                $log.log('Socket closed!');
            });

            socket.onOpen(function () {
                $log.log('Socket opened!');
            });

            socket.onError(function () {
                $log.error('Socket error!');
            });
        }

        function tearDown() {
            socket.close(true);
            socket = null;
        }
    }
]);