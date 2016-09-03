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
        $scope.termSubscriptions.map((term, id)->
          if term.points > -1
            term.reason = ''
          term.term_id = id
          return term)
      ).then(
        ()->
          $scope.success = true
          $scope.message = "Your terms are saved"
          $('#resultModal').modal('show', {keyboard: true})
        (error)->
          $scope.success = false
          $scope.message = error
          $('#resultModal').modal('show', {keyboard: true})
      )
    return
]
