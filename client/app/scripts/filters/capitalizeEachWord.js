'use strict';

angular.module('FYPClient').filter('capitalizeEachWord', function () {
    return function (input) {
        if (!input) return '';

        var splitted = input.split(' ');
        for (var i in splitted) {
            var word = splitted[i];
            splitted[i] = word[0].toUpperCase() + word.slice(1);
        }

        return splitted.join(' ');
    };
});