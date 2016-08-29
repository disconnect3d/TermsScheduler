angular.module('TermsScheduler').controller 'SubjectsController', [
  '$scope'
  'SubjectsService'
  'FlashService'
  ($scope, SubjectsService, FlashService) ->
    SubjectsService.Get().then(
      (subjects)-> $scope.subjects = subjects
      (error)-> FlashService.Error(error)
    )
    $scope.signUpToogle = (subject)->
      if !subject.signed
        SubjectsService.SignOut(subject).then(
          ()-> FlashService.Success('You are unsigned from ' + subject.name)
          (error)-> FlashService.Error(error); subject.signed = !subject.signed
        )
      else
        SubjectsService.SignIn(subject).then(
          ()-> FlashService.Success('You are signed on ' + subject.name)
          (error)-> FlashService.Error(error); subject.signed = !subject.signed
        )
    return
]
