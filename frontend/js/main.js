const DATETIME_FMT = 'YYYY-MM-DD HH:mm:ss';
const API = 'http://192.168.0.24:3000';
const USER_ID = 10002;

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

    console.log('called');

    $('.datepicker').pickadate({
        closeOnSelect: true,
        format: 'yyyy-mm-dd'
    });

    show(location.hash.substring(1) || 'offers');
}

function bind() {
	$.urlParam = function(name){
	    var results = new RegExp('[\?&]' + name + '=([^]*)').exec(window.location.href);
	    if (results === null){
	       return null;
	    }
	    else{
	       return results[1] || 0;
	    }
	}

	$('#offer-form').submit(submitOffer);
}

function submitOffer(e) {

	const form = e.target;

	const depart_date = moment(form.depart_date.value + ' ' + form.depart_time.value + ':00', DATETIME_FMT)
		.utc()
		.format(DATETIME_FMT);

	const arrive_date = moment(form.arrive_date.value + ' ' + form.arrive_time.value + ':00', DATETIME_FMT)
		.utc()
		.format(DATETIME_FMT);

	const payload = {
		amount: form.amount.value,
		currency: form.currency.value,
		exchange_currency: form.exchange_currency.value,
		depart_date,
		arrive_date,
		depart_from: form.depart_from.value,
		arrive_to: form.arrive_to.value
	};

	$('#submit').attr('disabled', 'disabled');
	$('#submit-loader').toggleClass('active');

	function doneLoading() {
		$('#submit').removeAttr('disabled');
		$('#submit-loader').toggleClass('active');
	}

	$.ajax({
			method: 'POST',
			url: API + '/api/transaction',
			data: JSON.stringify(payload),
			contentType: 'application/json',
			headers: {
				'x-user-id': USER_ID
			}
		})
		.done(result => {
			doneLoading();
			show('listings');
		})
		.fail(e => {
			console.error(e);
			Materialize.toast('Ooops! Something went wrong. I\'m sorry', 4000)
			doneLoading();
		});

	return false;
}

function show(section) {
	location.hash = section;
	$('section').hide();
	$('#nav-mobile li').removeClass('active');
	$('#' + section + '-nav').addClass('active');
	$('.' + section + '-section').show();
}
$(document).ready(start);