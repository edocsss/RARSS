'use strict';

angular.module('FYPClient', [
    'ngMaterial',
    'ui.router',
    'ngMessages',
    'chart.js'
])
.config(function ($stateProvider, $urlRouterProvider, $mdThemingProvider) {
    $mdThemingProvider.theme('default').primaryPalette('blue').accentPalette('pink');

    $stateProvider
        // .state('home', {
        //     url: '/',
        //     templateUrl: 'views/home.html',
        //     controller: 'HomeController',
        //     controllerAs: 'homeController'
        // })
        .state('rawDataVisualizer', {
            url: '/rawDataVisualizer',
            templateUrl: 'views/raw-data-visualizer.html',
            controller: 'RawDataVisualizerController',
            controllerAs: 'rawDataVisualizerController'
        });

    $urlRouterProvider.otherwise('/rawDataVisualizer');
}).run(function () {
    // Chart.js configuration
    Chart.defaults.global.elements.point.radius = 0;
    Chart.defaults.global.elements.line.fill = false;
    Chart.defaults.global.elements.line.borderWidth = 0.6;
});