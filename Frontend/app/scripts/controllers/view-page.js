'use strict';

/**
 * @ngdoc function
 * @name sampleProject3App.controller:ViewPageCtrl
 * @description
 * # ViewPageCtrl
 * Controller of the sampleProject3App
 */
 /*
angular.module('sampleProject3App')
  .controller('ViewPageCtrl', function ($scope,$routeParams) {
  	$scope.source = $routeParams.url;
  	//$scope.source = 'http://www.w3schools.com'

  });
*/
//http://www.ng-newsletter.com/posts/restangular.html
angular.module('sampleProject3App')
// takes the url from message service and passes it to view of this page 
  .controller('ViewPageCtrl', function ($scope,messageService,Movie,$http,$location) {
  	$scope.URLOfsource = messageService.getMessages()[0];
    $http({
      method: 'GET',
      host: "proxy",
      port: 8080,
      path: $scope.URLOfsource
    }).then(function successCallback(response) {
      $scope.response = response;  
    // this callback will be called asynchronously
    // when the response is available
    }, function errorCallback(response) {
         $scope.response = response;
  });
    //console.log(Movie);
    
/*
    $scope.getURLContent = function(){
      return Movie.post(messageService.getMessages()[0]).$object; 
    };


    $scope.getURLContent.then(function(modifiedData) {
      $scope.ListOfMovies = modifiedData;
    });
    
    $scope.getURLContent()

      .then(function(data) {
        return data;
      })
      .then(function(data) {
        //here a Promise is return which will resovle later (cause of the timeout)
        return new Promise(function(resolve) {
          setTimeout(function() {
            resolve(data+' !!!!!!');
          },200);
        });
      })
      .then(function(data) {
        //this will have 'some data !!!!!!'
        console.log(data);
      });
*/

    //$scope.ListOfMovies = Movie.post(messageService.getMessages()[0]).$object;
    
  });

 

 