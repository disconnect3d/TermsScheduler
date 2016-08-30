(function () {
    'use strict';

    angular
        .module('TermsScheduler')
        .controller('LoginController', LoginController);

    LoginController.$inject = ['$state', 'AuthenticationService', 'FlashService'];
    function LoginController($state, AuthenticationService, FlashService) {
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
                    $state.go('home');
                },
                function () {
                    vm.dataLoading = false;
                });
        }
    }
})();
