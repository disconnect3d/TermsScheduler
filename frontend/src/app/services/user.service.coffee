angular
.module('TermsScheduler')
.factory('UserService', [
  '$http',
  'settings',
  ($http, settings) ->
    GetAll = () ->
      return $http.get(settings.backendUrl + 'allusers').then(handleSuccess, handleError('Error getting all users'))


    GetById = (id) ->
      return $http.get(settings.backendUrl + 'users/' + id).then(handleSuccess, handleError('Error getting user by id'))


    GetByUsername = (username) ->
      return $http.get('/api/users/' + username).then(handleSuccess, handleError('Error getting user by username'))


    Create = (user) ->
      return $http.post(settings.backendUrl + 'users', user).then(handleSuccess, handleError('Error creating user'))


    Update = (user) ->
      return $http.put('/api/users/' + user.id, user).then(handleSuccess, handleError('Error updating user'))

    handleSuccess = (res) ->
      return res.data


    handleError = (error) ->
      return  () ->
        return {success: false, message: error}

    return {
      GetAll: GetAll
      GetById: GetById
      GetByUsername: GetByUsername
      Create: Create
      Update: Update
    }
])
