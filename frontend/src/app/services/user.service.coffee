angular.module('TermsScheduler').factory('UserService', [
  '$http'
  'settings'
  'utils'
  ($http, settings, u) ->
    handleSuccess = (res) ->
      return res.data
    return {
      GetById: (id) ->
        $http.get(settings.backendUrl + 'users/' + id).then(handleSuccess, u.handleError('Error getting user by id'))

      GetGroups: () ->
        $http.get(settings.backendUrl + 'groups').then(handleSuccess, u.handleError('Error getting groups'))

      Create: (user) ->
        $http.post(settings.backendUrl + 'users', user).then(handleSuccess, u.handleError('Error creating user'))

      Update: (user) ->
        $http.put('/api/users/' + user.id, user).then(handleSuccess, u.handleError('Error updating user'))
    }
])
