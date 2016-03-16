'use strict';

/**
 * @ngdoc overview
 * @name sampleProject3App
 * @description
 * # sampleProject3App
 *
 * Main module of the application.
 */
angular
  .module('sampleProject3App', [
    'ngAnimate',
    'ngCookies',
    'ngMessages',
    'ngResource',
    'ngRoute',
    'ngSanitize',
    'restangular'
  ])
  // routes required for the app
  .config(function ($routeProvider,RestangularProvider) {
    RestangularProvider.setBaseUrl('http://localhost:8080/api');
    $routeProvider
      .when('/', {
        templateUrl: 'views/main.html',
        controller: 'MainCtrl'
      })
      .when('/about', {
        templateUrl: 'views/about.html',
        controller: 'AboutCtrl'
      })
      .when('/view-page', {
        templateUrl: 'views/view-page.html',
        controller: 'ViewPageCtrl'
      })
      .when('/view-page/:url', {
        templateUrl: 'views/view-page.html',
        controller: 'ViewPageCtrl'
      })
      .when('/errorPage', {
        templateUrl: 'views/errorpage.html',
        controller: 'ErrorpageCtrl',
      })
      .otherwise({
        redirectTo: '/'
      });
  })
  // to make a page trusted otherwise the page is not loaded in browser by angular server
  .filter('trusted', function ($sce) {
    return function(url) {
      return $sce.trustAsResourceUrl(url);
    };
  })

  // implementation of message service to send/ receive messages
  .factory('messages', function(){
  var messages = {};

  messages.list = [];

  messages.add = function(message){
    messages.list.push({id: messages.list.length, text: message});
  };

  return messages;
})
  
  .factory('MovieRestangular', function(Restangular) {
    return Restangular.withConfig(function(RestangularConfigurer) {
      RestangularConfigurer.setRestangularFields({
        id: '_id'
      });
    });
  })
  .factory('Movie', function(MovieRestangular) {
    return MovieRestangular.service('/');
  })

.service('messageService', function() {
  var messageList = [];

  var addMessage = function(newMsg) {
      messageList.push(newMsg);
  };

  var getMessages = function(){
      return messageList;
  };
  return {
    addMessage: addMessage,
    getMessages: getMessages
  };
});
