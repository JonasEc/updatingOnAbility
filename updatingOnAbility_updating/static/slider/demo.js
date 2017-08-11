var app = angular.module('rzSliderDemo', ['rzModule', 'ui.bootstrap', 'hljs', 'ngSanitize']);

// app.directive('showCode', function () {
//   return {
//     scope: {
//       jsFile: '@',
//       htmlFile: '@'
//     },
//     templateUrl: 'show-code.html'
//   };
// });
//
// app.directive('clickableLabel', function () {
//   return {
//     restrict: 'E',
//     scope: {label: '='},
//     replace: true,
//     template: "<button ng-click='onclick(label)' style='cursor: pointer;'>click me - {{label}}</button>",
//     link: function (scope, elem, attrs) {
//       scope.onclick = function (label) {
//         alert("I'm " + label);
//       };
//     }
//   };
// });

app.controller('MainCtrl', function ($scope, $rootScope, $timeout, $uibModal) {
  //Minimal slider config
      //Slider with ticks and values
    $scope.slider_ticks_values = {
        value: 0,
        options: {
            ceil: 4,
            floor: 0,
            translate: function(value, sliderId, label){
            switch (label) {
          case 'ceil':
          return 'emoji squad B';
          case 'floor':
          return 'emoji squad A + $2';
          case 'model':
          return value;
        //default:
          //return '$' + value
      }
            },
            // translate: function(value, , 'floor'){
            // return "emoji squad A + $2"
            // },
            step: 0.1,
            precision: 1,
            showTicks: 1,
            // ticksArray: [0, 0.5, 1, 1.5, 2, 2.5, 3, 3.5, 4],
            ticksTooltip: function(v) {
            return '$' + v;
            },
            showSelectionBar: true,
            getLegend: function(value){
            if (value < $scope.slider_ticks_values.value)
            return "";
            return value
            },
            // onEnd: function (value) {}
            // $scope.slider_ticks_values.options['ceil'] =  g($scope.slider_ticks_values.value);
            // $scope.slider_ticks_values.options['getLegend'] = f5;

        }
    };


});
