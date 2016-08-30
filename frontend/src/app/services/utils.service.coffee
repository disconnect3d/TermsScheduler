angular.module('TermsScheduler').factory('utils', [
  '$q'
  ($q)->
    return {
      handleError: (altMessage) ->
        return  (response) ->
          if response.data && response.data.message
            return $q.reject(response.data.message)
          return $q.reject(altMessage)

      capitalize: (string) -> string.charAt(0).toUpperCase() + string.slice(1)
    }
])
.filter('pretty', ['utils', (utils)->
  (input)-> utils.capitalize(input).replace(/_/g, ' ')
])
