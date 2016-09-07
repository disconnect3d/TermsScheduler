angular.module('TermsScheduler', [
  'ngCookies',
  'templates-app',
  'templates-common',
  'ui.router'
])
.config(($stateProvider, $urlRouterProvider) ->
  # Can't inject it here
  cap = (string) -> string.charAt(0).toUpperCase() + string.slice(1)
  state = ($sp, name, extraOptions = {})->
    config = {
      url: "/#{name}",
      templateUrl: "views/#{name}/#{name}.tpl.html",
      controller: "#{cap(name)}Controller"
    }
    $sp.state(name, $.extend(config, extraOptions))

  state($stateProvider, 'login', {controllerAs: 'vm'})
  state($stateProvider, 'register', {controllerAs: 'vm'})
  state($stateProvider, 'home', {controllerAs: 'vm'})
  state($stateProvider, 'subjects')
  state($stateProvider, 'user')
  state($stateProvider, 'terms')
  $urlRouterProvider.otherwise('/home')
)

.run(($rootScope, $location, $cookieStore, $http) ->
  $rootScope.globals = $cookieStore.get('globals') || {}
  if $rootScope.globals.currentUser
    $http.defaults.headers.common['Authorization'] = 'Basic ' + $rootScope.globals.currentUser.authdata


  $rootScope.$on('$locationChangeStart', (event, next, current) ->
    # redirect to login page if not logged in and trying to access a restricted page
    restrictedPage = ['/login', '/register'].indexOf($location.path()) == -1
    loggedIn = $rootScope.globals.currentUser
    if restrictedPage && !loggedIn
      $location.path('/login')
  )
)

.controller('AppCtrl', [
  '$scope'
  'utils'
  ($scope, utils) ->
    $scope.pageTitle = 'Terms Scheduler'
    $scope.$on('$stateChangeSuccess', (event, toState, toParams, fromState, fromParams) ->
      if angular.isDefined(toState.name)
        $scope.pageTitle = toState.name + ' | Terms Scheduler'
        $scope.name = utils.capitalize(toState.name)
    )
])
