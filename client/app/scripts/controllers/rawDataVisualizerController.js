'use strict';

angular.module('FYPClient').controller('RawDataVisualizerController', [
    'DataFactory',
    'ChartFactory',
    '$mdToast',
    function (DataFactory, ChartFactory, $mdToast) {
        var vm = this;

        vm.NUMBER_OF_GRAPH_COLUMNS = 2;
        vm.LIST_OF_SUBJECTS = [];
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
        vm.dataSubject = 'edwin';

        vm.chartColors = ['#2196F3', '#FF4081', '#FF5722'];
        vm.isLoadingData = true;
        vm.initialLoad = false;
        vm.graphData = [];
        vm.graphDataKeys = [];

        vm.getNumberOfGraphRows = function (fileId) {
            return Math.ceil(vm.graphData.get(fileId).length / vm.NUMBER_OF_GRAPH_COLUMNS);
        };

        vm.getGraphCardWidth = function () {
            return 100 / vm.NUMBER_OF_GRAPH_COLUMNS;
        };

        vm.getListOfSubjects = function () {
            vm.isLoadingData = true;
            DataFactory.getListOfSubjects().then(function onSuccess (response) {
                vm.LIST_OF_SUBJECTS = response.data.data;
            }, function onError () {
                $mdToast.show($mdToast.simple().textContent('Cannot load list of subjects!').position('bottom').hideDelay(2000));
            });
        };

        vm.loadRawData = function () {
            var toastMessage;
            vm.isLoadingData = true;

            DataFactory.loadRawDataByActivityAndSource(
                vm.activityType,
                vm.dataSource,
                vm.dataSubject
            ).then(
                function onSuccess (response) {
                    vm.isLoadingData = false;
                    vm.initialLoad = true;
                    vm.graphData = convertRawDataObjectToSortedMap(response.data.data);
                    vm.graphDataKeys = Array.from(vm.graphData.keys());
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
        vm.getListOfSubjects();
        vm.loadRawData();

        vm.getRawDataByRowAndCol = function (fileId, row, col) {
            var index = vm.NUMBER_OF_GRAPH_COLUMNS * row + col;
            return vm.graphData.get(fileId)[index];
        };

        function convertRawDataObjectToSortedMap(rawData) {
            var result = {};
            var data = null;
            var processedData = null;
            var series = null;
            var points = null;

            for (var fileId in rawData) {
                result[fileId] = [];
                for (var k in rawData[fileId]) {
                    series = [];
                    points = [];
                    processedData = getGraphDatasetFormat(k, rawData[fileId][k]);

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

                    result[fileId].push(data);
                }
            }
            
            return convertGraphDataObjectToSortedMap(result);
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

        function convertGraphDataObjectToSortedMap(data) {
            var keys = [];
            var sortedMap = new Map();
            
            for (var k in data) {
                keys.push(k);
            }

            keys.sort();
            for (var i in keys) {
                sortedMap.set(keys[i], data[keys[i]]);
            }
            
            return sortedMap;
        }
    }
]);