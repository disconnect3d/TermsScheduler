angular
.module('TermsScheduler')
.factory('AuthenticationService', [
  '$http',
  'settings',
  'FlashService',
  ($http, settings, FlashService) ->
    Login = (username, password, callback) ->
      SetCredentials(username, password)
      $http.get(settings.backendUrl + 'login')
      .then(
        (response) -> callback(response),
        (response) -> FlashService.Error(response)
      )

    SetCredentials = (username, password) ->
      authdata = Base64.encode(username + ':' + password)
      $http.defaults.headers.common['Authorization'] = 'Basic ' + authdata

    ClearCredentials = () ->
      $http.defaults.headers.common.Authorization = 'Basic'

    return {
      Login: Login
      SetCredentials: SetCredentials
      ClearCredentials: ClearCredentials
    }
])
