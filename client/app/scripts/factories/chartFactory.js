'use strict';

angular.module('FYPClient').factory('ChartFactory', [
    function () {
        return {
            buildAccelerometerDatasetFormat: buildAccelerometerDatasetFormat,
            buildGyroscopeDatasetFormat: buildGyroscopeDatasetFormat,
            buildBarometerDatasetFormat: buildBarometerDatasetFormat,
            buildGravityDatasetFormat: buildGravityDatasetFormat,
            buildMagneticDatasetFormat: buildMagneticDatasetFormat,
            buildUltravioletDatasetFormat: buildUltravioletDatasetFormat,
            buildLightDatasetFormat: buildLightDatasetFormat
        };

        function buildAccelerometerDatasetFormat(fullData) {
            var labels = [];
            var datasets = [];

            var ax = [];
            var ay = [];
            var az = [];

            for (var i in fullData) {
                labels.push(fullData[i][0]);
                ax.push(fullData[i][1]);
                ay.push(fullData[i][2]);
                az.push(fullData[i][3]);
            }

            datasets.push({
                label: 'ax',
                fill: false,
                data: ax
            });

            datasets.push({
                label: 'ay',
                fill: false,
                data: ay
            });

            datasets.push({
                label: 'az',
                fill: false,
                data: az
            });

            return {
                labels: labels,
                datasets: datasets
            };
        }

        function buildGyroscopeDatasetFormat(fullData) {
            var labels = [];
            var datasets = [];

            var gx = [];
            var gy = [];
            var gz = [];

            for (var i in fullData) {
                labels.push(fullData[i][0]);
                gx.push(fullData[i][1]);
                gy.push(fullData[i][2]);
                gz.push(fullData[i][3]);
            }

            datasets.push({
                label: 'gx',
                fill: false,
                data: gx
            });

            datasets.push({
                label: 'gy',
                fill: false,
                data: gy
            });

            datasets.push({
                label: 'gz',
                fill: false,
                data: gz
            });

            return {
                labels: labels,
                datasets: datasets
            };
        }

        function buildBarometerDatasetFormat(fullData) {
            var labels = [];
            var datasets = [];
            var pressure = [];

            for (var i in fullData) {
                labels.push(fullData[i][0]);
                pressure.push(fullData[i][1]);
            }

            datasets.push({
                label: 'pressure',
                fill: false,
                data: pressure
            });

            return {
                labels: labels,
                datasets: datasets
            };
        }

        function buildGravityDatasetFormat(fullData) {
            var labels = [];
            var datasets = [];

            var gx = [];
            var gy = [];
            var gz = [];

            for (var i in fullData) {
                labels.push(fullData[i][0]);
                gx.push(fullData[i][1]);
                gy.push(fullData[i][2]);
                gz.push(fullData[i][3]);
            }

            datasets.push({
                label: 'gx',
                fill: false,
                data: gx
            });

            datasets.push({
                label: 'gy',
                fill: false,
                data: gy
            });

            datasets.push({
                label: 'gz',
                fill: false,
                data: gz
            });

            return {
                labels: labels,
                datasets: datasets
            };
        }

        function buildMagneticDatasetFormat(fullData) {
            var labels = [];
            var datasets = [];

            var mx = [];
            var my = [];
            var mz = [];

            for (var i in fullData) {
                labels.push(fullData[i][0]);
                mx.push(fullData[i][1]);
                my.push(fullData[i][2]);
                mz.push(fullData[i][3]);
            }

            datasets.push({
                label: 'mx',
                fill: false,
                data: mx
            });

            datasets.push({
                label: 'my',
                fill: false,
                data: my
            });

            datasets.push({
                label: 'mz',
                fill: false,
                data: mz
            });

            return {
                labels: labels,
                datasets: datasets
            };
        }

        function buildUltravioletDatasetFormat(fullData) {
            var labels = [];
            var datasets = [];
            var uv = [];

            for (var i in fullData) {
                labels.push(fullData[i][0]);
                uv.push(fullData[i][1]);
            }

            datasets.push({
                label: 'uv',
                fill: false,
                data: uv
            });

            return {
                labels: labels,
                datasets: datasets
            };
        }

        function buildLightDatasetFormat(fullData) {
            var labels = [];
            var datasets = [];
            var light = [];

            for (var i in fullData) {
                labels.push(fullData[i][0]);
                light.push(fullData[i][1]);
            }

            datasets.push({
                label: 'light',
                fill: false,
                data: light
            });

            return {
                labels: labels,
                datasets: datasets
            };
        }
    }
]);