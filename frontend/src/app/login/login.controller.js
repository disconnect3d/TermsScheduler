(function () {
    'use strict';

    angular
        .module('TermsScheduler')
        .controller('LoginController', LoginController);

    LoginController.$inject = ['$location', 'AuthenticationService', 'FlashService'];
    function LoginController($location, AuthenticationService, FlashService) {
        var vm = this;

        vm.login = login;

        (function initController() {
            // reset login status
            AuthenticationService.ClearCredentials();
        })();

        function login() {
            vm.dataLoading = true;
            AuthenticationService.Login(vm.username, vm.password,
                function () {
                    vm.dataLoading = false;
                    $location.path('/');
                },
                function () {
                    vm.dataLoading = false;
                });
        }
    }
})();
