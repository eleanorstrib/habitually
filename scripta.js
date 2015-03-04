
(function() {
	var app = angular.module('habitually', []);



	app.controller('UserForm', function($scope) {
		$scope.master = {};
		$scope.update = function(user) {
			console.log($scope);
			console.log(user.target);
			$scope.master = angular.copy(user);
		};
		// $scope.reset = function() {
		// 	$scope.user = angular.copy($scope.master);
		// };

		$scope.userName = {
			text: '',
			word: /^\s*\w*\s*$/
		};

		$scope.currentlySelectedUserName = $scope.userName.text;

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
			{ description: 'Female', value: 2 },
			{ description: 'Male', value: 1 }
		];

		$scope.currentlySelectedGender = $scope.gender[0].value;


		$scope.region = [
			{ description: 'Northeast', value: 1 },
			{ description: 'Midwest', value: 2 },
			{ description: 'South', value: 3 },
			{ description: 'West', value: 4 }

		];

		$scope.currentlySelectedRegion = $scope.region[0].value;

		$scope.education = [
			{ description: 'Less than High School', value: 1 },
			{ description: 'High School graduate', value: 2},
			{ description: 'Some college/Associates Degree', value: 3 },
			{ description: 'Four year college degree', value: 4 },
			{ description: 'Masters/Professional Degree/PhD', value: 5 }
		];

		$scope.currentlySelectedEducation = $scope.education[0].value;

		$scope.income = [
			{ description: 'Under $20,000', value: 1 },
			{ description: '$20,000 to $39,999', value: 2 },
			{ description: '$40,000 to 59,999', value: 3 },
			{ description: 'Over $60,000', value: 4}
		];

		$scope.currentlySelectedIncome = $scope.income[0].value;

		$scope.submit = function($event) {
			// if($scope.ageRange && $scope.gender && $scope.region && $scope.education && $scope.income) {
				angular.element($event.target.form).triggerHandler('submit');
			// }
		};

		// $scope.reset();
	
	});




	
})();