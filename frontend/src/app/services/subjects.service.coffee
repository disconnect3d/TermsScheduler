angular.module('TermsScheduler').factory('SubjectsService', [
  '$http'
  '$q'
  'settings'
  'FlashService'
  ($http, $q, settings, FlashService) ->
    handleError = (altMessage, clb) ->
      (response) ->
        if response.data && response.data.message
          FlashService.Error(response.data.message)
        else
          FlashService.Error(altMessage)
        if clb
          clb()

    return {
      Get: ()->
        subjectsPromise = $http.get(settings.backendUrl + 'subjects')
        subjectsSignupPromise = $http.get(settings.backendUrl + 'subjects_signup')

        $q.all([subjectsPromise, subjectsSignupPromise]).then(
          ([subjectsResponse,signupResponse])->
            subjects = subjectsResponse.data.subjects
            for s in signupResponse.data.subjects_signup
              subjects.find((el)-> el.id == s.subject_id).signed = true
            # TODO: Needs polyfill
            return subjects
          handleError("Fetching subjects failed")
        )

      SignIn: (subject) ->
        $http.post(settings.backendUrl + 'subjects_signup', {'subject_id': subject.id}).then(
          ()-> FlashService.Success('You are signed on ' + subject.name)
          handleError("Signing on #{subject.name} failed", ()-> subject.signed = !subject.signed)
        )

      SignOut: (subject) ->
        $http.delete(settings.backendUrl + 'subjects_signup/' + subject.id).then(
          ()-> FlashService.Success('You are unsigned from ' + subject.name)
          handleError("Unsigning from #{subject.name} failed", ()-> subject.signed = !subject.signed)
        )
    }
])
