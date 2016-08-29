angular.module('TermsScheduler').controller('RegisterController', [
  'UserService'
  'AuthenticationService'
  'FlashService'
  '$state'
  (UserService, AuthenticationService, FlashService, $state) ->
    vm = this

    vm.register = ->
      vm.dataLoading = true
      UserService.Create(vm.user).then(
        () ->
          FlashService.Success 'Registration successful'
          AuthenticationService.Login(vm.user.username, vm.user.password, ()->
            $state.go('home')
          )
        (error) ->
          FlashService.Error error
          vm.dataLoading = false
      )
      return
    return
])
