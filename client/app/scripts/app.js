'use strict';

angular.module('FYPClient', [
    'ngMaterial',
    'ui.router',
    'ngMessages',
    'ngAnimate',
    'chart.js',
    'angular-websocket',
    'md.data.table'
])
.config(function ($stateProvider, $urlRouterProvider, $mdThemingProvider) {
    // Main Theme
    $mdThemingProvider.theme('default').primaryPalette('blue').accentPalette('pink');

    $stateProvider
        .state('rawDataVisualizer', {
            url: '/rawDataVisualizer',
            templateUrl: 'views/raw-data-visualizer.html',
            controller: 'RawDataVisualizerController',
            controllerAs: 'rawDataVisualizerController'
        })
        .state('realTimeMonitoring', {
            url: '/',
            templateUrl: 'views/real-time-monitoring.html',
            controller: 'RealTimeMonitoringController',
            controllerAs: 'realTimeMonitoringController'
        })
        .state('activityHistoryList', {
            url: '/history',
            templateUrl: 'views/activity-history-list.html',
            controller: 'ActivityHistoryListController',
            controllerAs: 'activityHistoryListController'
        });

    $urlRouterProvider.otherwise('/');
}).run(function ($rootScope, WebsocketFactory) {
    // Chart.js configuration
    Chart.defaults.global.elements.point.radius = 0;
    Chart.defaults.global.elements.line.fill = false;
    Chart.defaults.global.elements.line.borderWidth = 0.6;

    // Init Websocket
    WebsocketFactory.init();
    $rootScope.$on('$destroy', WebsocketFactory.tearDown);
});