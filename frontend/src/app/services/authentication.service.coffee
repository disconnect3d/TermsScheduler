angular
.module('TermsScheduler')
.factory('AuthenticationService', [
  '$http'
  'settings'
  'FlashService'
  '$rootScope'
  '$cookieStore'
  ($http, settings, FlashService, $rootScope, $cookieStore) ->
    Login = (username, password, callback, errCallback) ->
      SetCredentials(username, password)
      $http.get(settings.backendUrl + 'login')
      .then(
        (response) -> setUserData(response); callback(response); $rootScope.$broadcast('LoggedIn'),
        (response) -> FlashService.Error(response); errCallback(response)
      )
    setUserData = (response) ->
      $rootScope.globals.currentUser['id'] = response.data.id
      $rootScope.globals.currentUser['token'] = response.data.token
      $cookieStore.put('globals', $rootScope.globals)

    SetCredentials = (username, password) ->
      authdata = Base64.encode(username + ':' + password)
      $http.defaults.headers.common['Authorization'] = 'Basic ' + authdata
      $rootScope.globals.currentUser = {
        username: username
        authdata: authdata
      }
      $cookieStore.put('globals', $rootScope.globals)

    ClearCredentials = () ->
      $http.defaults.headers.common.Authorization = 'Basic'
      $rootScope.globals = {}
      $cookieStore.remove('globals')

    return {
      Login: Login
      SetCredentials: SetCredentials
      ClearCredentials: ClearCredentials
    }
])
