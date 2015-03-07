
(function() { 

	var app = angular.module('habitually', ['ngRoute']);

	app.config(function($routeProvider){
		$routeProvider

			.when('/', {
				templateUrl: '../static/partials/main.html'
			})

			.when('/about', {
				templateUrl: '../static/partials/about.html'
			})

			.when('/howitworks', {
				templateUrl: '../static/partials/howitworks.html'
			})

			.when('/getstarted', {
				templateUrl: '../static/partials/getstarted.html'
			})
	})

	app.controller('mainPage', ['$scope', '$http', function($scope, $http){
		$http.get("/allhabits.json").success(function(data) {
			console.dir(data);
			$scope.habits = data;
		});
	}])

	app.controller('userForm', ['$scope', '$http', function($scope, $http) {
		$scope.master = {};

		$http.get("/allhabits.json").success(function(data) {
			console.dir(data);
			$scope.habits = data;
		});

		$scope.update = function(user) {
			$scope.master = angular.copy(user);
		};
		$scope.reset = function() {
			$scope.user = angular.copy($scope.master);
		};

		$scope.reset();

		$scope.userName = {
			text: '',
			word: /^\s*\w*\s*$/
		};

		$scope.currentlySelectedUserName = $scope.userName.text;

		$scope.ageRange = 1;
		$scope.ageRange = [
			{ description: 'Under 20 years old', decade: 'under twenty', value: 1 },
			{ description: '20 - 29 years old', decade: 'twenties', value: 2 },
			{ description: '30 - 39 years old', decade: 'thirties', value: 3 },
			{ description: '40 - 49 years old', decade: 'forties', value: 4 },
			{ description: '50 - 59 years old', decade: 'fifties', value: 5 },
			{ description: '60 - 69 years old', decade: 'sixties', value: 6 },
			{ description: 'Over 70 years old', decade: 'seventy +', value: 7 }
		];

		$scope.currentlySelectedAge = $scope.ageRange[0].value;


		$scope.gender = [
			{ description: 'Female', value: 2, img: 'blah' },
			{ description: 'Male', value: 1, img: './male.png' }
		];

		$scope.currentlySelectedGender = $scope.gender.value;


		$scope.region = [
			{ description: 'Northeast', value: 1 },
			{ description: 'Midwest', value: 2 },
			{ description: 'South', value: 3 },
			{ description: 'West', value: 4 }

		];

		$scope.currentlySelectedRegion = $scope.region.value;

		$scope.education = [
			{ description: 'Less than High School', value: 1 },
			{ description: 'High School graduate', value: 2 },
			{ description: 'Some college/Associates Degree', value: 3 },
			{ description: 'Four year college degree', value: 4 },
			{ description: 'Masters/Professional Degree/PhD', value: 5 }
		];

		$scope.currentlySelectedEducation = $scope.education.value;

		$scope.income = [
			{ description: 'Under $20,000', value: 1 },
			{ description: '$20,000 to $39,999', value: 2 },
			{ description: '$40,000 to 59,999', value: 3 },
			{ description: 'Over $60,000', value: 4}
		];

		$scope.currentlySelectedIncome = $scope.income.value;


	}]) //closes form controller

}) (); //closes whole function





