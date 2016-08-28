angular
.module('TermsScheduler')
.factory('UserService', [
  '$http'
  '$q'
  'settings'
  'utils'
  ($http, $q, settings, u) ->
    GetById = (id) ->
      return $http.get(settings.backendUrl + 'users/' + id).then(handleSuccess,
        u.handleError('Error getting user by id'))

    Create = (user) ->
      return $http.post(settings.backendUrl + 'users', user).then(handleSuccess, u.handleError('Error creating user'))

    Update = (user) ->
      return $http.put('/api/users/' + user.id, user).then(handleSuccess, u.handleError('Error updating user'))

    handleSuccess = (res) ->
      return res.data

    return {
      GetById: GetById
      Create: Create
      Update: Update
    }
])
