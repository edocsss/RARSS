'use strict';

angular.module('FYPClient').controller('RealTimeMonitoringController', [
    'WebsocketFactory',
    '$scope',
    '$interval',
    '$mdColors',
    function (WebsocketFactory, $scope, $interval, $mdColors) {
        const THEME_CHANGE_INTERVAL = 5000;
        const PALETTES = ['blue', 'pink', 'teal', 'light-blue', 'amber', 'indigo', 'orange', 'deepOrange'];
        const HUES = [400, 500, 600, 700];
        const INITIAL_BACKGROUND_COLOR = 'blue-500';

        let vm = this;
        let toolbarElement = document.querySelector('md-toolbar');
        let bodyElement = document.querySelector('body');

        vm.activityType = 'DOING NOTHING';
        vm.lastActivityDatetime = 'N/A';

        function init() { 
            toolbarElement.style.backgroundColor = 'transparent';
            bodyElement.style.transition = 'all ease 0.75s';
            bodyElement.style.backgroundColor = $mdColors.getThemeColor(INITIAL_BACKGROUND_COLOR);
            WebsocketFactory.init();
        }

        function tearDown() {
            toolbarElement.style.backgroundColor = $mdColors.getThemeColor('blue-500');
            bodyElement.style.transition = 'none';
            bodyElement.style.backgroundColor = $mdColors.getThemeColor('grey-50');
            WebsocketFactory.tearDown();
        }

        init();
        $scope.$on('$destroy', tearDown);

        $interval(function () {
            let nextPaletteIndex = Math.floor(Math.random() * PALETTES.length);
            let nextHueIndex = Math.floor(Math.random() * HUES.length);

            let nextBackgroundColor = PALETTES[nextPaletteIndex] + '-' + HUES[nextHueIndex];
            bodyElement.style.backgroundColor = $mdColors.getThemeColor(nextBackgroundColor);
        }, THEME_CHANGE_INTERVAL);

        $scope.$on('new_activity_data', function (e, data) {
            let activityType = data.activity.split('_').join(' ');
            let datetime = data.datetime;

            vm.activityType = activityType.toUpperCase();
            vm.lastActivityDatetime = datetime;
        });
    }
]);