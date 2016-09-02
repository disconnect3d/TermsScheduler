angular.module('TermsScheduler').controller 'TermsController', [
  '$scope'
  'TermsService'
  'FlashService'
  ($scope, TermsService, FlashService) ->
    $scope.label = (n)-> return if n == -1 then 'Impossible' else n

    TermsService.Get().then(
      (terms)->
        $scope.terms = terms
        $scope.termSubscriptions = []
      (error)-> FlashService.Error(error)
    )

    $scope.save = ()->
      $scope.termSubscriptions
      TermsService.SaveTermsSignup(
        $scope.termSubscriptions.map((term, id)-> term.term_id = id; return term)
      ).then(null, (error)-> FlashService.Error(error))
    return
]
