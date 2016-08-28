angular.module('TermsScheduler').factory('utils', [
  '$q'
  ($q)->
    return {
      handleError: (altMessage) ->
        return  (response) ->
          if response.data && response.data.message
            return $q.reject(response.data.message)
          return $q.reject(altMessage)
    }
])
