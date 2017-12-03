let forEx = [];
let airports = [];

function request(url, done, fail, always) {
	$.ajax({
			url: API + url,
			headers: {
				'x-user-id': USER_ID
			}
		})
		.done(done)
		.fail(fail)
		.always(always);
}

function start () {
	bind();

    $('.timepicker').pickatime({
        twelvehour: false,
        autoclose: true
    });

	$('.modal').modal();
	$('select').material_select();

    $('.datepicker').pickadate({
        closeOnSelect: true,
        format: 'yyyy-mm-dd'
    });

    getForex();
    getAirports();

    if (localStorage.user) {
    	const user = JSON.parse(localStorage.user);
    	USER_ID = user.user_id;
    	NAME = user.name;
    	email = user.email;
    }


	typeof pageStart != "undefined" && pageStart();
    show(location.hash.substring(1) || 'offers');
}

function getAirports() {
	request(
		'/api/transaction/airports',
		function (e) {
			airports = e.data;

			let options = [];
			
			for(let i=0; i < airports.length; i++) {
				options.push('<option value="'+airports[i].code+'">'+airports[i].name+'</option>')
			}

			$('select.airports').html(options.join(''));
		},
		function (e) {},
		function (e) {
			$('select').material_select();
		}
	);
}

function getForex() {
	request(
		'/api/transaction/forex',
		function (e) {
			forEx = e.data;
			let options = ['<option value="PHP">Philippine Peso</option>'];

			for(let i=0; i < forEx.length; i++) {
				options.push('<option value="'+forEx[i].symbol+'">'+forEx[i].name+'</option>')
			}

			$('select.currency').html(options.join(''));

		},
		function (e) {},
		function (e) {
			$('select').material_select();
		}
	);
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
	$('#details-form').submit(submitDetails);

	$('select[name=exchange_currency]').change(function (e) {
		if (e.target.value != "PHP") {
			$('select[name=currency]').val('PHP');

			$('select').material_select();

			compute($('select[name=currency]').val(), $('select[name=exchange_currency]').val(), $('input[name=amount]').val());
		}
	});

	$('select[name=currency]').change(function (e) {
		if (e.target.value != "PHP") {
			$('select[name=exchange_currency]').val('PHP');

			$('select').material_select();

			compute($('select[name=currency]').val(), $('select[name=exchange_currency]').val(), $('input[name=amount]').val());
		}
	});
}

function compute(from, to, amount) {
	if (from == 'PHP') {
		multiplier = 1/convert('selling', to)
	}

	if (to == 'PHP') {
		multiplier = convert('buying', from)
	}

	$('input[name=converted]').val(multiplier * amount);

	$('#exchange-rate').html("1 " + from + " = " + multiplier + " " + to);
}

function convert(type, key) {
	for (let i=0; i < forEx.length; i++) {
		if (forEx[i].symbol == key) {
			return forEx[i][type];
		}
	}
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

function submitDetails(e) {

	const form = e.target;

	const payload = {
		card_number: form.card_number.value,
		expiry: form.expiry.value,
		cvv: form.cvv.value,
		zip_code: form.zip_code.value
	};

	$('#submit-details').attr('disabled', 'disabled');
	$('#submit-details-loader').toggleClass('active');

	function doneLoading() {
		$('#submit-details').removeAttr('disabled');
		$('#submit-details-loader').toggleClass('active');
	}

	$.ajax({
			method: 'POST',
			url: API + '/api/details',
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
	$('section').hide();
	$('.hidden').hide();
	$('#nav-mobile li').removeClass('active');
	$('#' + section + '-nav').addClass('active');
	$('.' + section + '-section').show();

	typeof pageStart != 'undefined' && pageStart();
}

function removeRow(row) {
	const $row = $(row);

	$row.closest('tr').hide();

	b = $row.closest('tbody');

	if ($row.closest('tbody').children(':visible').length === 0) {
		$('#no-offer-tr').show();
	} else {
		$('#no-offer-tr').hide();
	}
}

function sendMessage() {
	const msg = $('#message-area').val();

	if (!msg) {
		return;
	}

	$('#message-thread').append('<span>' + NAME + ': </span><span>' + msg + '</span><br/>')

	$('#message-area').val('');
}

$(document).ready(start);