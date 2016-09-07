angular
.module('TermsScheduler')
.factory('settings', [
  '$http'
  'utils'
  'FlashService'
  ($http, utils, FlashService) ->
    settings = {
      backendUrl: "http://localhost:5000/api/"
    }
    settings.settingsPromise = $http.get(settings.backendUrl + 'settings').then(
      (response) ->
        for setting in response.data.settings
          settings[setting.name] = setting.value
        return settings
      utils.handleError('Fetching settings failed')
    ).catch((error)-> FlashService.Error(error))
    # TODO: $http(settings.backendUrl + url) ->  FlashService.Error is the most common case, extract it into utils
    return settings
])
