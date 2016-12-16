'use strict';

angular.module('FYPClient', [
    'ngMaterial',
    'ui.router',
    'ngMessages',
    'ngAnimate',
    'chart.js',
    'angular-websocket'
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
        });

    $urlRouterProvider.otherwise('/');
}).run(function () {
    // Chart.js configuration
    Chart.defaults.global.elements.point.radius = 0;
    Chart.defaults.global.elements.line.fill = false;
    Chart.defaults.global.elements.line.borderWidth = 0.6;
});