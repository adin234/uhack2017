const MATCHES = 0;
const LISTINGS = 1;
const DETAIL = 2;

const templates = [
	'#tpl-matches',
	'#tpl-listings',
	'#tpl-listing-data'
];

function pageStart() {
	pageBind();
	request(
		'/api/transaction/user_transaction',
		function (e) {
			listings(e.data);
		},
		function (e) {}
	);
}

function pageBind() {
	$('#listings').on('click', '.listing', showListing);
}

function showListing(e) {
	const target = $(e.currentTarget);

	if ($(target).hasClass('done')) {
		return;
	}

	if ($(target).data('type') === 'listing') {
		$('.chevron', target).hide();
		$('.preloader-wrapper', target).css('width', '36px').toggleClass('active');
		//mock request
		request(
			'/api/transaction/search_match?transaction_id=' + $(target).data('id'),
			function (e) {
				if (!e.length) {
					$('.chevron', target).hide();
				}

				matches(target, e.data);
			},
			function (e) {},
			function (e) {
				$('.preloader-wrapper', target).toggleClass('active').css('width', '0');
			}
		);
		return;
	}

	// mock details request
	const payload = {
		current_user_transaction: $(target).data('id'),
		target_transaction: $(target.parent().parent()).data('id')
	}

	const parentPayload = $(target.parent().parent()).data('serialized');

	$.ajax({
			method: 'POST',
			url: API + '/api/transaction/check_match',
			data: JSON.stringify(payload),
			contentType: 'application/json',
			headers: {
				'x-user-id': USER_ID
			}
		})
		.done(result => {
			console.log($(target));
			renderDetails(result.data, parentPayload, $(target).data('serialized'));
		})
		.fail(e => {
		})
		.always(e => {
			show('details');
		});

}

let toasted = false;

function renderDetails(details, parent, target) {
	parent = JSON.parse(decodeURIComponent(parent));
	target = JSON.parse(decodeURIComponent(target));

	$("#accept").text("ACCEPT");
	
	const tplData = {}

	let src = parent
	if (target.user_id == USER_ID) {
		src = target;
	}

	tplData.exchange_currency = src.exchange_currency;
	tplData.amount = src.amount;
	tplData.currency = src.currency;
	tplData.arrive_to = src.arrive_to;
	tplData.arrive_at = src.arrive_at;

	const tpl = template([tplData], DETAIL);
	let transaction_id = 0;

	$('#details .listing-data').html(tpl);

	if (details.base_confirmation) {
		if (parent.user_id == USER_ID && details.base_transaction_id == parent.user_transaction_id && parent.exchange_currency != "PHP") {
			$("#accept").text("COMPLETE");
			transaction_id = parent.user_transaction_id;
		} else if (target.user_id == USER_ID && details.base_transaction_id == target.user_transaction_id && target.exchange_currency != "PHP") {
			$("#accept").text("COMPLETE");
			transaction_id = target.user_transaction_id;
		} else {
			$("#accept").hide();
		}
	} else if (details.secondary_confirmation) {
		if (parent.user_id == USER_ID && details.secondary_transaction_id == parent.user_transaction_id && parent.currency != "PHP") {
			$("#accept").text("COMPLETE");
			transaction_id = parent.user_transaction_id;
		} else if (target.user_id == USER_ID && details.secondary_transaction_id == target.user_transaction_id && target.currency != "PHP") {
			$("#accept").text("COMPLETE");
			transaction_id = target.user_transaction_id;
		} else {
			$("#accept").hide();
		}
	}

	$('#accept').click(function(e) {
		let endpoint = '/api/transaction/accept';
		const payload = {
			transaction_confirmation_id: details.transaction_confirmation_id,
			transaction_id: transaction_id
		};

		if ($(this).text().toLowerCase() == "complete") {
			endpoint = '/api/transaction/complete';
		}

		if (!toasted) {
			toasted = true;
			$.ajax({
				method: 'POST',
				url: API + endpoint,
				data: JSON.stringify(payload),
				contentType: 'application/json',
				headers: {
					'x-user-id': USER_ID
				}
			})
			.done(result => {
				Materialize.toast("CONGRATS!", 4000);
			})
			.fail(e => {
			})
			.always(e => {
				show('listings');
				toasted = false;
			});
		}

	});
}

function matches(holder, _matchesData) {
	const tpl = template(_matchesData, MATCHES);

	$('.matches', holder).html(tpl);

}

function listings(e) {
	const tpl = template(e, LISTINGS);

	$('#listings').html(tpl);
}

function template(data, type) {
	let rowItemHtmlArr = [];
	const chevBadge = '<i class="chevron material-icons">keyboard_arrow_down</i>';
	const messageBadge = '<i class="material-icons">message</i>';

	for (let i=0; i< data.length; i++) {
		const tpl = $(templates[type]).html()
			.replace(/\{\{DONE\}\}/gi, data[i].closed ? "done" : "")
			.replace(/\{\{SERIALIZED\}\}/gi, encodeURIComponent(JSON.stringify(data[i])))
			.replace(/\{\{ID\}\}/gi, data[i].user_transaction_id)
			.replace(/\{\{FROM\}\}/gi, data[i].depart_from)
			.replace(/\{\{TO\}\}/gi, data[i].arrive_to)
			.replace(/\{\{DATE\}\}/gi, moment(data[i].arrive_date).format('MMM DD, YYYY'))
			.replace(/\{\{ALIAS\}\}/gi, data[i].exchange_currency)
			.replace(/\{\{TIME\}\}/gi, moment(data[i].arrive_date).format('HH:mm'))
			.replace(/\{\{AMOUNT\}\}/gi, data[i].amount + " " + data[i].currency)
			.replace(/\{\{CHEV\}\}/gi, data[i].closed ? "" : chevBadge)
			.replace(/\{\{MESSAGE_BADGE\}\}/gi, data[i].closed ? "DONE" : messageBadge)
			.replace(/\{\{BADGE\}\}/gi, data[i].newMessages || (data[i].closed ? "DONE" : data[i].matches))
			.replace(/\{\{TYPE\}\}/gi, data[i].type);

		rowItemHtmlArr.push(tpl);
	}

	return rowItemHtmlArr.join('');

}