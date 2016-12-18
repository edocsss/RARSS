'use strict';

angular.module('FYPClient').controller('RealTimeMonitoringController', [
    '$scope',
    '$interval',
    '$mdColors',
    'ActivityFactory',
    function ($scope, $interval, $mdColors, ActivityFactory) {
        const THEME_CHANGE_INTERVAL = 10000;
        const PALETTES = ['blue', 'pink', 'teal', 'light-blue', 'amber', 'indigo', 'orange', 'deepOrange'];
        const HUES = [400, 500, 600, 700];
        const INITIAL_BACKGROUND_COLOR = 'blue-500';

        let vm = this;
        let interval;
        let toolbarElement = document.querySelector('md-toolbar');
        let bodyElement = document.querySelector('body');
        
        function init() { 
            vm.activityHistoryList = ActivityFactory.getActivityHistoryList();
            toolbarElement.style.backgroundColor = 'transparent';
            bodyElement.style.transition = 'all ease 0.75s';
            bodyElement.style.backgroundColor = $mdColors.getThemeColor(INITIAL_BACKGROUND_COLOR);
        }

        function tearDown() {
            toolbarElement.style.backgroundColor = $mdColors.getThemeColor('blue-500');
            bodyElement.style.transition = 'none';
            bodyElement.style.backgroundColor = $mdColors.getThemeColor('grey-50');
            $interval.cancel(interval);
        }

        init();
        $scope.$on('$destroy', tearDown);

        interval = $interval(function () {
            let nextPaletteIndex = Math.floor(Math.random() * PALETTES.length);
            let nextHueIndex = Math.floor(Math.random() * HUES.length);

            let nextBackgroundColor = PALETTES[nextPaletteIndex] + '-' + HUES[nextHueIndex];
            bodyElement.style.backgroundColor = $mdColors.getThemeColor(nextBackgroundColor);
        }, THEME_CHANGE_INTERVAL);
    }
]);