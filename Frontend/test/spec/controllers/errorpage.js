'use strict';

describe('Controller: ErrorpageCtrl', function () {

  // load the controller's module
  beforeEach(module('sampleProject3App'));

  var ErrorpageCtrl,
    scope;

  // Initialize the controller and a mock scope
  beforeEach(inject(function ($controller, $rootScope) {
    scope = $rootScope.$new();
    ErrorpageCtrl = $controller('ErrorpageCtrl', {
      $scope: scope
      // place here mocked dependencies
    });
  }));

  it('should attach a list of awesomeThings to the scope', function () {
    expect(ErrorpageCtrl.awesomeThings.length).toBe(3);
  });
});
