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

function renderDetails(details, parent, target) {
	parent = JSON.parse(decodeURIComponent(parent));
	target = JSON.parse(decodeURIComponent(target));

	console.log(parent);
	console.log(target);
	console.log(details);

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

	$('#details .listing-data').html(tpl);

	if (details.base_transaction_id == parent.user_transaction_id && parent.user_id == USER_ID) {
		
	} else {

	}

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
			.replace(/\{\{DONE\}\}/gi, data[i].done ? "done" : "")
			.replace(/\{\{SERIALIZED\}\}/gi, encodeURIComponent(JSON.stringify(data[i])))
			.replace(/\{\{ID\}\}/gi, data[i].user_transaction_id)
			.replace(/\{\{FROM\}\}/gi, data[i].depart_from)
			.replace(/\{\{TO\}\}/gi, data[i].arrive_to)
			.replace(/\{\{DATE\}\}/gi, moment(data[i].arrive_date).format('MMM DD, YYYY'))
			.replace(/\{\{ALIAS\}\}/gi, data[i].exchange_currency)
			.replace(/\{\{TIME\}\}/gi, moment(data[i].arrive_date).format('HH:mm'))
			.replace(/\{\{AMOUNT\}\}/gi, data[i].amount + " " + data[i].currency)
			.replace(/\{\{CHEV\}\}/gi, data[i].done ? "" : chevBadge)
			.replace(/\{\{MESSAGE_BADGE\}\}/gi, data[i].done ? "DONE" : messageBadge)
			.replace(/\{\{BADGE\}\}/gi, data[i].newMessages || (data[i].done ? "DONE" : data[i].matches))
			.replace(/\{\{TYPE\}\}/gi, data[i].type);

		rowItemHtmlArr.push(tpl);
	}

	return rowItemHtmlArr.join('');

}