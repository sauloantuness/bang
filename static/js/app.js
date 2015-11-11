var myApp = angular.module('myApp', []);

myApp.controller('mainCtrl', ['$scope', '$http', function($scope, $http){ 
	
	// == TABS ==
	$scope.tabs = [
		{'name' : 'Users', 	'tabName' : 'users', 'tabPage' : '/static/users.html'},
		{'name' : 'Problems', 'tabName' : 'problems', 'tabPage' : '/static/problems.html'},
		{'name' : 'Contest', 	'tabName' : 'contest', 'tabPage' : '/static/contest.html'}
	];

	$scope.isCurrentTab = function isCurrentTab(tab){
		return $scope.currentTab == tab;
	}

	$scope.setCurrentTab = function setCurrentTab(tab){
		$scope.currentTab = tab;
	}

	$scope.currentTab = 'users';

	// == USERS ==

	$scope.users = [];

	var loadUsers = function(){
		$http.get('/users').success(function(data, status){
			$scope.users = data;
		});
	};

	loadUsers();

	$scope.deleteUser = function deleteUser(user){
		var successCallback = function(response){
			console.log(response);
			$scope.users = $scope.users.filter(function(item){
				return item.userId != user.userId;
			});
		};

		var errorCallback = function(response){
			console.log(response);
		};

	    $http({
			method: 'DELETE',
			url: '/user',
			data: user
	    }).then(successCallback, errorCallback);
	};

	$scope.addUser = function addUser(user){
		$http.post('/user', user).success(function(response){
			$scope.users.push(angular.copy(response));
			delete $scope.user;
			$scope.setAdding(false);
		});
	};

	$scope.categories = [
		{code : 1, value : 0, name : "Beginner" },
		{code : 2, value : 0, name : "Ad-Hoc" },
		{code : 3, value : 0, name : "Strings" },
		{code : 4, value : 0, name : "Data Structures" },
		{code : 5, value : 0, name : "Mathematics" },
		{code : 6, value : 0, name : "Paradigms" },
		{code : 7, value : 0, name : "Graph" },
		{code : 8, value : 0, name : "Computational Geometry" }
	];

	$scope.problems = [
		{code : '1001', name : 'Extremely Basic'},
		{code : '1002', name : 'Area of a Circle'},
		{code : '1003', name : 'Simple Sum'}
	];

	$scope.setAdding = function setAdding(status){
		$scope.adding = status;
	}

	$scope.isAdding = function isAdding(){
		return $scope.adding;
	}


	$scope.setContestStatus = function setContestStatus(status){
		$scope.contestStatus = status;
	}

	$scope.isContestStatus = function isContestStatus(status){
		return $scope.contestStatus == status;
	}

	$scope.setCategory = function setCategory(category, value){
		category.value += value;
		if(category.value < 0)
			category.value = 0;
	}

	$scope.contestStatus = 'done'; //waiting, loading, done
	$scope.contestProgress = 35;
	$scope.adding = false;

}]);