angular
.module('TermsScheduler')
.factory('UserService', [
  '$http'
  '$q'
  'settings'
  ($http, $q, settings) ->
    GetById = (id) ->
      return $http.get(settings.backendUrl + 'users/' + id).then(handleSuccess, handleError('Error getting user by id'))

    Create = (user) ->
      return $http.post(settings.backendUrl + 'users', user).then(handleSuccess, handleError('Error creating user'))

    Update = (user) ->
      return $http.put('/api/users/' + user.id, user).then(handleSuccess, handleError('Error updating user'))

    handleSuccess = (res) ->
      return res.data


    handleError = (altMessage) ->
      return  (response) ->
        if response.data && response.data.message
          return $q.reject(response.data.message)
        return $q.reject(altMessage)

    return {
      GetById: GetById
      Create: Create
      Update: Update
    }
])
