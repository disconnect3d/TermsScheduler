angular.module('TermsScheduler').directive("formElement", ()->
  return {
    restrict: "E"
    scope: {
      name: '@'
      type: '@'
      label: '@'
      model: '='
      form: '='
    }
    templateUrl: 'formElement/formElement.tpl.html'
  }
)
