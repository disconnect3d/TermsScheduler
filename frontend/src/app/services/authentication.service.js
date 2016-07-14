(function () {
    'use strict';

    angular
        .module('TermsScheduler')
        .factory('AuthenticationService', AuthenticationService);

    AuthenticationService.$inject = ['$http', 'settings', 'FlashService'];
    function AuthenticationService($http, settings, FlashService) {
        var service = {};

        service.Login = Login;
        service.SetCredentials = SetCredentials;
        service.ClearCredentials = ClearCredentials;

        return service;

        function Login(username, password, callback) {
            SetCredentials(username, password);
            $http.get(settings.backendUrl + 'login')
                .then(function (response) {
                        callback(response);
                    },
                    function (response) {
                        FlashService.Error(response)
                    }
                );
        }

        function SetCredentials(username, password) {
            var authdata = Base64.encode(username + ':' + password);
            $http.defaults.headers.common['Authorization'] = 'Basic ' + authdata; // jshint ignore:line
        }

        function ClearCredentials() {
            $http.defaults.headers.common.Authorization = 'Basic';
        }
    }
})();
