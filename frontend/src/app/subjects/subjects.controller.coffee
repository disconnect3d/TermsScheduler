angular.module('TermsScheduler').controller 'SubjectsController', [
  '$scope'
  'SubjectsService'
  ($scope, SubjectsService) ->
    SubjectsService.Get().then((subjects)-> $scope.subjects = subjects)

    $scope.signUpToogle = (subject)->
      if !subject.signed
        SubjectsService.SignOut(subject)
      else
        SubjectsService.SignIn(subject)
    return
]
