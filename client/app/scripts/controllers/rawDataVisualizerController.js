'use strict';

angular.module('FYPClient').controller('RawDataVisualizerController', [
    'RawDataFactory',
    'ChartFactory',
    '$mdToast',
    function (RawDataFactory, ChartFactory, $mdToast) {
        var vm = this;

        vm.NUMBER_OF_GRAPH_COLUMNS = 1;
        vm.DATA_SOURCES = ['Smartphone', 'Smartwatch'];
        vm.ACTIVITY_TYPES = [
            'Walking',
            'Running',
            'Lying',
            'Sitting',
            'Standing',
            'Going Upstairs',
            'Going Downstairs',
            'Brushing',
            'Typing',
            'Writing',
            'Reading',
            'Eating',
            'Food Preparation',
            'Folding',
            'Sweeping the Floor'
        ];

        vm.activityType = 'standing';
        vm.dataSource = 'smartphone';

        vm.chartColors = ['#2196F3', '#FF4081', '#FF5722'];
        vm.isLoadingData = true;
        vm.initialLoad = false;
        vm.rawData = [];

        vm.getNumberOfGraphRows = function () {
            return Math.ceil(vm.rawData.length / vm.NUMBER_OF_GRAPH_COLUMNS);
        };

        vm.getGraphCardWidth = function () {
            return 100 / vm.NUMBER_OF_GRAPH_COLUMNS;
        };

        vm.loadRawData = function () {
            var toastMessage;
            vm.isLoadingData = true;

            RawDataFactory.loadRawDataByActivityAndSource(
                vm.activityType,
                vm.dataSource
            ).then(
                function onSuccess (response) {
                    vm.isLoadingData = false;
                    vm.initialLoad = true;
                    vm.rawData = convertRawDataObjectToArray(response.data.data);
                    toastMessage = 'Raw data is successfully retrieved!';
                },
                function onError () {
                    vm.isLoadingData = false;
                    toastMessage = 'Raw data for activity ' + vm.activityType + ' from ' + vm.dataSource + ' cannot be retrieved!';
                }
            ).finally(function onFinally () {
                $mdToast.show($mdToast.simple().textContent(toastMessage).position('bottom').hideDelay(2000));
            });
        };

        // Init
        vm.loadRawData();

        vm.getRawDataByRowAndCol = function (row, col) {
            var index = vm.NUMBER_OF_GRAPH_COLUMNS * row + col;
            return vm.rawData[index];
        };

        function convertRawDataObjectToArray (rawData) {
            var result = [];
            var data = null;
            var processedData = null;
            var series = null;
            var points = null;

            for (var k in rawData) {
                series = [];
                points = [];
                processedData = getGraphDatasetFormat(k, rawData[k]);

                for (var i in processedData.datasets) {
                    points.push(processedData.datasets[i].data);
                    series.push(processedData.datasets[i].label);
                }

                data = {
                    graphName: k,
                    labels: processedData.labels,
                    series: series,
                    data: points
                };

                result.push(data);
            }

            return result;
        }

        function getGraphDatasetFormat (graphName, graphData) {
            var dataType = graphName.split('_')[1];
            var fullData = graphData;

            if (dataType.indexOf('accelerometer') >= 0 || dataType.indexOf('linear') >= 0) {
                return ChartFactory.buildAccelerometerDatasetFormat(fullData);
            } else if (dataType.indexOf('gyroscope') >= 0) {
                return ChartFactory.buildGyroscopeDatasetFormat(fullData);
            } else if (dataType.indexOf('barometer') >= 0 || dataType.indexOf('pressure') >= 0) {
                return ChartFactory.buildBarometerDatasetFormat(fullData);
            } else if (dataType.indexOf('gravity') >= 0) {
                return ChartFactory.buildGravityDatasetFormat(fullData);
            } else if (dataType.indexOf('magnetic') >= 0) {
                return ChartFactory.buildMagneticDatasetFormat(fullData);
            } else if (dataType.indexOf('ultraviolet') >= 0) {
                return ChartFactory.buildUltravioletDatasetFormat(fullData);
            } else if (dataType.indexOf('light') >= 0) {
                return ChartFactory.buildLightDatasetFormat(fullData);
            }
        }
    }
]);