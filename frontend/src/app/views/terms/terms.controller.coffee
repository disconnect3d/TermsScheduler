angular.module('TermsScheduler').controller 'TermsController', [
  '$scope'
  'TermsService'
  'FlashService'
  'settings'
  ($scope, TermsService, FlashService, settings) ->
    $scope.label = (n)-> return if n == -1 then 'Impossible' else n
    settings.settingsPromise.then(()->
      $scope.options = [ -1 ... settings.MAX_PTS_PER_TERM + 1 ]
    )

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
