angular.module('TermsScheduler').factory('TermsService', [
  '$http'
  'settings'
  'utils'
  ($http, settings, u) ->
    url = settings.backendUrl + 'terms/signup'
    return {
      Get: ()->
        $http.get(url).then(
          (response)-> response.data.subjects_terms
          u.handleError("Fetching terms failed")
        )

      SaveTermsSignup: (terms) ->
        $http.post(url, {'terms_signup': terms}).then(
          null
          u.handleError("Saving terms failed")
        )
    }
])
