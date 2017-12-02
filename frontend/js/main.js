function onSignIn(googleUser) {
	var profile = googleUser.getBasicProfile();
	console.log('ID: ' + profile.getId()); // Do not send to your backend! Use an ID token instead.
	console.log('Name: ' + profile.getName());
	console.log('Image URL: ' + profile.getImageUrl());
	console.log('Email: ' + profile.getEmail()); // This is null if the 'email' scope is not present.

	location.href = "offer.html";
}

function start () {
	bind();

	typeof pageStart != "undefined" && pageStart();


    $('select').material_select();

    $('.timepicker').pickatime({
        twelvehour: false,
        autoclose: true
    });

    $('.datepicker').pickadate({
        closeOnSelect: true
    });
}

function bind() {
	$.urlParam = function(name){
	    var results = new RegExp('[\?&]' + name + '=([^]*)').exec(window.location.href);
	    if (results==null){
	       return null;
	    }
	    else{
	       return results[1] || 0;
	    }
	}

	$('.header-nav').click(headerClick);

	$('#btn-buy').click(buy);
	$('#btn-sell').click(sell);

	$('#submit').click(showListings);
}

function showListings(e) {
	//call saving here
	e.preventDefault();
	nextPage();
}

function nextPage(id) {
	let goTo = 'list.html?listings=true&id=' + id;
	open(goTo)
}

function buy() {
	open('details.html?buy=true');
}

function sell() {
	open('details.html')
}

function open(path) {
	location.href = path;
}

function headerClick(e) {
	const open = $(this).data('open');

	$('.tab').hide();
	$('.tab.' + open).show();
}

$(document).ready(start);