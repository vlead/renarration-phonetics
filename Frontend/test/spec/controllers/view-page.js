'use strict';

describe('Controller: ViewPageCtrl', function () {

  // load the controller's module
  beforeEach(module('sampleProject3App'));

  var ViewPageCtrl,
    scope;

  // Initialize the controller and a mock scope
  beforeEach(inject(function ($controller, $rootScope) {
    scope = $rootScope.$new();
    ViewPageCtrl = $controller('ViewPageCtrl', {
      $scope: scope
      // place here mocked dependencies
    });
  }));

  it('should attach a list of awesomeThings to the scope', function () {
    expect(ViewPageCtrl.awesomeThings.length).toBe(3);
  });
});
