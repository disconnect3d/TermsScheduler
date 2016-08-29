angular.module('TermsScheduler', [
  'ngCookies',
  'templates-app',
  'templates-common',
  'ui.router'
])
.constant("settings", {
  backendUrl: "http://localhost:5000/api/"
})
.config(($stateProvider, $urlRouterProvider) ->
  # Can't inject it here
  cap = (string) -> string.charAt(0).toUpperCase() + string.slice(1)
  state = ($sp, name) ->
    $sp.state(name, {
      url: "/#{name}",
      templateUrl: "views/#{name}/#{name}.tpl.html",
      controller: "#{cap(name)}Controller"
    })

  $stateProvider
  .state('login', {
    url: "/login",
    templateUrl: 'views/login/login.tpl.html',
    controller: 'LoginController',
    controllerAs: 'vm'
  })
  .state('register', {
    url: "/register",
    templateUrl: 'views/register/register.tpl.html',
    controller: 'RegisterController',
    controllerAs: 'vm'
  })
  .state('home', {
    url: "/",
    templateUrl: 'views/home/home.tpl.html',
    controller: 'HomeController',
    controllerAs: 'vm'
  })
  state($stateProvider, 'subjects')
  state($stateProvider, 'user')
  $urlRouterProvider.otherwise('/')
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
