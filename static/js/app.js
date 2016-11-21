var app = angular.module("urlShortenApp", []);

app.config(['$interpolateProvider', function ($interpolateProvider) {
  $interpolateProvider.startSymbol('{$');
  $interpolateProvider.endSymbol('$}');
}]);

app.config(function ($httpProvider) {
  $httpProvider.defaults.xsrfCookieName = 'csrftoken';
  $httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken';
  $httpProvider.defaults.headers.post['Content-Type'] = 'application/x-www-form-urlencoded';
  $httpProvider.defaults.headers.common['X-Requested-With'] = 'XMLHttpRequest';
});

app.controller('DummyController', ['$scope', '$http', function ($scope, $http) {
}]);

app.controller('LinkController', ['$scope', '$http', function ($scope, $http) {

}]);
