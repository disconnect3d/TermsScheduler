angular.module('TermsScheduler').controller 'TermsResultsController', [
  '$scope'
  'TermsService'
  'FlashService'
  ($scope, TermsService, FlashService) ->
    TermsService.Get().then(
      (terms)->
        $scope.terms = terms.map((subject) ->
          subject.classes = subject.terms_aggregated.map((type)->{
            name: type.term_type
            term: type.terms.find((term)-> term.is_assigned)
          })
          subject.terms_aggregated = undefined
          return subject
        )
      (error)-> FlashService.Error(error)
    )
    return
]
