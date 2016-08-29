angular.module('TermsScheduler').factory('SubjectsService', [
  '$http'
  '$q'
  'settings'
  'utils'
  ($http, $q, settings, u) ->
    return {
      Get: ()->
        subjectsPromise = $http.get(settings.backendUrl + 'subjects')
        subjectsSignupPromise = $http.get(settings.backendUrl + 'subjects_signup')

        $q.all([subjectsPromise, subjectsSignupPromise]).then(
          ([subjectsResponse, signupResponse])->
            subjects = subjectsResponse.data.subjects
            for s in signupResponse.data.subjects_signup
              subjects.find((el)-> el.id == s.subject_id).signed = true
            # TODO: Needs polyfill
            return subjects
          u.handleError("Fetching subjects failed")
        )

      SignIn: (subject) ->
        $http.post(settings.backendUrl + 'subjects_signup', {'subject_id': subject.id}).then(
          null
          u.handleError("Signing on #{subject.name} failed")
        )

      SignOut: (subject) ->
        $http.delete(settings.backendUrl + 'subjects_signup/' + subject.id).then(
          null
          u.handleError("Unsigning from #{subject.name} failed")
        )
    }
])
