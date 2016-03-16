'use strict';

/**
 * @ngdoc function
 * @name sampleProject3App.controller:MainCtrl
 * @description
 * # MainCtrl
 * Controller of the sampleProject3App
 */


angular.module('sampleProject3App')
  // takes the url from user and passes it to the message service
  .controller('MainCtrl', function ($scope,messageService,$location) {
    $scope.url = '';
     $scope.Convert=function() {
        messageService.addMessage($scope.url);
       	$location.path('/view-page');  
    };
    //$scope.received = Movie.post().$object;
    //console.log($scope.received);
  });