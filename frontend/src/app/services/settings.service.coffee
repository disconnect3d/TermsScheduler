angular
.module('TermsScheduler')
.factory('settings', [
  '$http'
  'utils'
  'FlashService'
  '$rootScope'
  '$q'
  ($http, utils, FlashService, $rootScope, $q) ->
    settings = {
      backendUrl: "http://localhost:5000/api/"
    }
    makeRequest = ()->
      $http.get(settings.backendUrl + 'settings').then(
        (response) ->
          for setting in response.data.settings
            settings[setting.name] = parseInt(setting.value)
          return settings
        utils.handleError('Fetching settings failed')
      ).catch((error)-> FlashService.Error(error))


    if $rootScope.globals.currentUser
      settings.settingsPromise = makeRequest()
    else
      settingsPromise = $q.defer()
      $rootScope.$on('LoggedIn', ()-> settingsPromise.resolve(makeRequest()))
      settings.settingsPromise = settingsPromise.promise
    # TODO: $http(settings.backendUrl + url) ->  FlashService.Error is the most common case, extract it into utils
    return settings
])
