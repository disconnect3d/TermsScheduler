angular
.module('TermsScheduler')
.factory('AuthenticationService', [
  '$http',
  'settings',
  'FlashService',
  '$rootScope',
  ($http, settings, FlashService, $rootScope) ->
    Login = (username, password, callback, errCallback) ->
      SetCredentials(username, password)
      $http.get(settings.backendUrl + 'login')
      .then(
        (response) -> callback(response),
        (response) -> FlashService.Error(response); errCallback(response)
      )

    SetCredentials = (username, password) ->
      authdata = Base64.encode(username + ':' + password)
      $http.defaults.headers.common['Authorization'] = 'Basic ' + authdata
      $rootScope.globals.currentUser = {username: username}

    ClearCredentials = () ->
      $http.defaults.headers.common.Authorization = 'Basic'

    return {
      Login: Login
      SetCredentials: SetCredentials
      ClearCredentials: ClearCredentials
    }
])
