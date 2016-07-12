angular.module('TermsScheduler', [
        'ngCookies',
        'templates-app',
        'templates-common',
        'ui.router'
    ])

    //http://plnkr.co/edit/tg25kr?p=preview
    .constant("settings", {
        backendUrl: "http://localhost:5000/api/"
    })
    .config(function myAppConfig($stateProvider, $urlRouterProvider) {
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
            });
        $urlRouterProvider.otherwise('/');
    })

    .run(function run($rootScope, $location, $cookieStore, $http) {
        $rootScope.globals = $cookieStore.get('globals') || {};
        if ($rootScope.globals.currentUser) {
            $http.defaults.headers.common['Authorization'] = 'Basic ' + $rootScope.globals.currentUser.authdata; // jshint ignore:line
        }

        $rootScope.$on('$locationChangeStart', function (event, next, current) {
            // redirect to login page if not logged in and trying to access a restricted page
            var restrictedPage = ['/login', '/register'].indexOf($location.path()) === -1;
            var loggedIn = $rootScope.globals.currentUser;
            if (restrictedPage && !loggedIn) {
                $location.path('/login');
            }
        });
    })

    .controller('AppCtrl', function AppCtrl($scope, $location) {
        $scope.pageTitle = 'a';
        //$scope.$on('$stateChangeSuccess', function (event, toState, toParams, fromState, fromParams) {
        //    if (angular.isDefined(toState.data.pageTitle)) {
        //        $scope.pageTitle = toState.data.pageTitle + ' | ngBoilerplate';
        //    }
        //});
    });

