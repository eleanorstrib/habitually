angular.module('habitually', ['ngRoute'])

	.config(function($routeProvider){
		$routeProvider

			.when('/', {
				templateUrl: '/templates/main.html'
			})

			.when('/about', {
				templateUrl: 'templates/about.html'
			})

			.when('/howitworks', {
				templateUrl: 'templates/howitworks.html'
			})

			.when('/getstarted', {
				templateUrl: 'templates/getstarted.html'
			})

	})