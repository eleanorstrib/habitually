
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
				templateUrl: '../static/partials/getstarted.html',
				controller: 'userForm'
			})

			.when('/predictions', {
				templateUrl: '../static/partials/predictions.html'
			})

			.when('/thankyou', {
				templateUrl: '../static/partials/thankyou.html'
			})
	})

	// app.controller('facebooklogin', ['$scope', function($scope) {

	// }]);


	app.controller('mainPage', ['$scope', '$http', function($scope, $http){
		$http.get("/allhabits.json")
		.success(function(data) {
			console.dir(data);
			$scope.habits = data;
		});
	}])
	
	app.controller('predictPage', ['$scope', '$http', function($scope, $http){
		$http.get("/predictions.json")
		.success(function(data) {
			console.dir(data);
			$scope.predictions = data;
		});
	}])

	app.controller('userForm', [ '$scope', '$http', '$location', function($scope, $http, $location) {
		$scope.load = function() {
			facebooklogin();
			console.log("called facebooklogin");
		};
		$scope.load()
		console.log($scope.userData);
		$scope.wasSubmitted = false;
		console.log("false was submitted");
		$scope.submit = function() {
			console.log($scope.formData);
			var userData = {};
			userData.firstName = $scope.formData.firstName;
			userData.queryAge = $scope.formData.ageRange.value;
			if ($scope.formData.gender == "You are a woman") {
				userData.queryGender = 2;
			} else {
				userData.queryGender = 1;
			}
			userData.queryRegion = $scope.formData.region.value;
			userData.queryEducation = $scope.formData.education.value;
			userData.queryIncome = $scope.formData.income.value;
			console.log(userData);
			userData = JSON.stringify(userData);
			console.log(userData);
			$http.post("/userData.json", JSON.stringify(userData))
				.success(function(data, status, headers, config){
					console.log("Success!");
					console.log(userData);
					$location.path('predictions');
				})
				.error(function(data, status, headers, config) {
					console.log("Fail!!");
					console.log(userData);
				})
			


		};//end submit function

		

		$scope.firstName = {
			text: '',
			word: /^\s*\w*\s*$/
		};

		$scope.ageRange = [
			{ description: 'Under 20 years old', decade: 'You are under twenty', value: 1 },
			{ description: '20 - 29 years old', decade: 'You are in your twenties', value: 2 },
			{ description: '30 - 39 years old', decade: 'You are in your thirties', value: 3 },
			{ description: '40 - 49 years old', decade: 'You are in your forties', value: 4 },
			{ description: '50 - 59 years old', decade: 'You are in your fifties', value: 5 },
			{ description: '60 - 69 years old', decade: 'You are in your sixties', value: 6 },
			{ description: 'Over 70 years old', decade: 'You are over seventy years old', value: 7 }
		];

		$scope.gender = [
			{ description: 'Female', value: 2, text: 'woman' },
			{ description: 'Male', value: 1, text: 'man' }
		];


		$scope.region = [
			{ description: 'Northeast', value: 1, text: 'Live in Northeastern US' },
			{ description: 'Midwest', value: 2, text: 'Live in Midwestern US' },
			{ description: 'South', value: 3, text: 'Live in Southern US' },
			{ description: 'West', value: 4,  text: 'Live in Western US' }

		];

		
		$scope.education = [
			{ description: 'Less than High School', value: 1, text: 'Didn\'t finish high school' },
			{ description: 'High School graduate', value: 2, text: 'Graduated High School/GED' },
			{ description: 'Some college/Associates Degree', value: 3, text: 'Completed some college or Associates' },
			{ description: 'Four year college degree', value: 4, text: 'Completed a four year college degree' },
			{ description: 'Masters/Professional Degree/PhD', value: 5, text: 'Finished graduate or professional school' }
		];

		$scope.income = [
			{ description: 'Under $20,000', value: 1, text: 'Annual household income of under $20K' },
			{ description: '$20,000 to $39,999', value: 2, text: 'Annual household income between $20-30K' },
			{ description: '$40,000 to 59,999', value: 3, text: 'Annual household income between $40-60K' },
			{ description: 'Over $60,000', value: 4, text: 'Annual household income over $60K'}
		];


	}]) //closes form controller

	app.controller('predictPage', ['$scope', '$http', function($scope, $http) {
		$http.get("/predictions.json")
		.success(function(data) {
			// console.dir(data);
			$scope.predictions = data;
		});//concludes getting predictions
	}]) //closes predict controller

	app.controller('actualData', ['$scope', '$http', '$location', function($scope, $http, $location){
		$scope.aWork = 0;
		$scope.aSleep = 0;
		$scope.aEx = 0;
		$scope.aClothes = 0;
		$scope.aEatOut = 0;
		$scope.wasSubmitted = false;
		console.log("false was submitted");

		$scope.submitActual = function() {
			console.log("in submit function");
			var actualData = {};
			console.log('trying aWork');
			console.log($scope.formData.aWork);
			actualData.work = $scope.formData.aWork;
			actualData.sleep = $scope.formData.aSleep;
			actualData.exercise = $scope.formData.aEx;
			actualData.clothes = $scope.formData.aClothes;
			actualData.eatout = $scope.formData.aEatOut;

			console.log(actualData);
			$http.post("/actualData.json", JSON.stringify(actualData))
				.success(function(data, status, headers, config){
					console.log("Success!");
					console.log("this is in the post function" + actualData);
					$location.path('thankyou');
				})
				.error(function(data, status, headers, config) {
					console.log("Fail!!");
					console.log(actualData);
					alert("There was an error - please try again.");
				})
		};
	}]) //closes actual data controller


}) (); //closes whole function




