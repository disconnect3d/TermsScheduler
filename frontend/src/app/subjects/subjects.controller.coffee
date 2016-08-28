angular.module('TermsScheduler').controller 'SubjectsController', [
  '$scope'
  'AuthenticationService'
  'FlashService',
  'settings',
  '$http',
  '$q'
  ($scope, AuthenticationService, FlashService, settings, $http, $q) ->
    subjectsPromise = $http.get(settings.backendUrl + 'subjects').then((response)->
      $scope.subjects = response.data.subjects
    )
    subjectsSignupPromise = $http.get(settings.backendUrl + 'subjects_signup')
    $q.all([subjectsPromise, subjectsSignupPromise]).then(([_,signupResponse])->
      for s in signupResponse.data.subjects_signup
        $scope.subjects.find((el)-> el.id == s.subject_id).signed = true
        # TODO: Needs polyfill
      return
    )
    $scope.signUp = (id)->
      $http.post(settings.backendUrl + 'subjects_signup', {'subject_id': id}).then((response)->
        FlashService.Success('ok')
      )
    return
]
