var myApp = angular.module('myApp', []);

myApp.controller('mainCtrl', ['$scope', function($scope){ 
	
	// == TABS ==
	$scope.tabs = [
		{'name' : 'Users', 	'tabName' : 'users'},
		{'name' : 'Problems', 'tabName' : 'problems'},
		{'name' : 'Contest', 	'tabName' : 'contest'}
	];

	$scope.isCurrentTab = function isCurrentTab(tab){
		return $scope.currentTab == tab;
	}

	$scope.setCurrentTab = function setCurrentTab(tab){
		$scope.currentTab = tab;
	}

	$scope.currentTab = 'users';

	// == USERS ==

	$scope.users = [
		{'name' : "Joao", 'uriLogin' : "12345"},
		{'name' : "Felipe", 'uriLogin' : "78945"}
	];

	$scope.categories = [
		{'name' : "AdHoc", 		'value' : 0},
		{'name' : "Begginer", 	'value' : 0},
		{'name' : "String", 	'value' : 0},
		{'name' : "Graph", 		'value' : 0}
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

	$scope.addUser = function addUser(user){
		$scope.users.push(angular.copy(user));
		delete $scope.user;
		$scope.setAdding(false);
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