angular.module('TermsScheduler').controller 'UserController', [
  '$scope'
  '$rootScope'
  '$q'
  'UserService'
  'FlashService'
  ($scope, $rootScope, $q, UserService, FlashService) ->
    userPromise = UserService.GetById($rootScope.globals.currentUser['id'])
    groupPromise = UserService.GetGroups()

    $q.all([userPromise, groupPromise]).then(
      ([user, groups])->
        user.groups = groups.groups
        $scope.user = user
        $scope.keys = Object.keys(user)
        $scope.keys.splice($scope.keys.indexOf('id'), 1)
      (error)-> FlashService.Error(error)
    )
    return
]
