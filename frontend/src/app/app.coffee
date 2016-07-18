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
  $stateProvider
  .state('login', {
    url: "/login",
    templateUrl: 'login/login.tpl.html',
    controller: 'LoginController',
    controllerAs: 'vm'
  })
  .state('register', {
    url: "/register",
    templateUrl: 'register/register.tpl.html',
    controller: 'RegisterController',
    controllerAs: 'vm'
  })
  .state('home', {
    url: "/",
    templateUrl: 'home/home.tpl.html',
    controller: 'HomeController',
    controllerAs: 'vm'
  })
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

.controller('AppCtrl', ($scope, $location) ->
  $scope.pageTitle = 'Terms Scheduler'
  $scope.$on('$stateChangeSuccess',(event, toState, toParams, fromState, fromParams) ->
    if angular.isDefined(toState.data.pageTitle)
      $scope.pageTitle = toState.data.pageTitle + ' | Terms Scheduler'
  )
)
