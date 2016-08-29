angular
.module('TermsScheduler')
.factory('FlashService', [
  '$rootScope',
  ($rootScope) ->
    $rootScope.$on('$locationChangeStart', () ->
      clearFlashMessage()
    )

    clearFlashMessage = () ->
      flash = $rootScope.flash
      if flash
        if !flash.keepAfterLocationChange
          delete $rootScope.flash
        else
          # only keep for a single location change
          flash.keepAfterLocationChange = false

    Success = (message, keepAfterLocationChange) ->
      $rootScope.flash = {
        message: message,
        type: 'success',
        keepAfterLocationChange: keepAfterLocationChange
      }

    Error = (message, keepAfterLocationChange) ->
      $rootScope.flash = {
        message: message,
        type: 'error',
        keepAfterLocationChange: keepAfterLocationChange
      }

    return {
      Success: Success
      Error: Error
    }
])
