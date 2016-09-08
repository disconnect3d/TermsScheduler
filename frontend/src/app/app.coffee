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
  state($stateProvider, 'termsResults')
  $urlRouterProvider.otherwise('/home')
)

.run(($rootScope, $state, $cookieStore, $http) ->
  $rootScope.globals = $cookieStore.get('globals') || {}
  if $rootScope.globals.currentUser
    $http.defaults.headers.common['Authorization'] = 'Basic ' + $rootScope.globals.currentUser.authdata

  $rootScope.$on('$stateChangeStart', (event, toState, toParams, fromState, fromParams)->
    # redirect to login page if not logged in and trying to access a restricted page
    restrictedPage = toState.name not in ['login', 'register']
    loggedIn = $rootScope.globals.currentUser
    if restrictedPage && !loggedIn
      event.preventDefault()
      $state.go('login')

    if $rootScope.statesEnabled? && $rootScope.statesEnabled[toState.name]? && !$rootScope.statesEnabled[toState.name]
      event.preventDefault()
  )
)
.controller('AppCtrl', [
  '$rootScope'
  '$scope'
  'utils'
  'settings'
  ($rootScope, $scope, utils, settings) ->
    settings.settingsPromise.then(()->
      $rootScope.statesEnabled = {
        'subjects': settings.SUBJECTS_SIGNUP == 1
        'terms': settings.TERMS_SIGNUP == 1
        'termsResults': settings.SHOW_TERM_RESULTS == 1
      }
    )
    $scope.navigationStates = [
      {name: 'subjects', title: 'Subjects'}
      {name: 'terms', title: 'Terms'}
      {name: 'termsResults', title: 'Results'}
    ]
    $scope.pageTitle = 'Terms Scheduler'
    $scope.$on('$stateChangeSuccess', (event, toState, toParams, fromState, fromParams) ->
      if angular.isDefined(toState.name)
        $scope.pageTitle = toState.name + ' | Terms Scheduler'
        $scope.name = utils.capitalize(toState.name)
    )
])
