angular.module('TermsScheduler').controller 'TermsController', [
  '$scope'
  '$state'
  '$stateParams'
  'FlashService'
  ($scope, $state, $stateParams, FlashService) ->
    if !$stateParams.subject
      $state.go('subjects')
    $scope.subject = $stateParams.subject
    return
]
