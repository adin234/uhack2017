const MATCHES = 0;
const LISTINGS = 1;

const templates = [
	'#tpl-matches',
	'#tpl-listings'
];

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


	//open('details.html?id='+target.data('id'));
	// mock details request
	show('details');
}

function matches(holder, _matchesData) {
	//mockUrlRequest
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
			.replace(/\{\{ID\}\}/gi, data[i].user_transaction_id)
			.replace(/\{\{FROM\}\}/gi, data[i].depart_from)
			.replace(/\{\{TO\}\}/gi, data[i].arrive_to)
			.replace(/\{\{DATE\}\}/gi, moment(data[i].arrive_date).format('MMM DD, YYYY'))
			.replace(/\{\{ALIAS\}\}/gi, data[i].currency)
			.replace(/\{\{TIME\}\}/gi, moment(data[i].arrive_date).format('HH:mm'))
			.replace(/\{\{AMOUNT\}\}/gi, data[i].amount + " " + data[i].exchange_currency)
			.replace(/\{\{CHEV\}\}/gi, data[i].done ? "" : chevBadge)
			.replace(/\{\{MESSAGE_BADGE\}\}/gi, data[i].done ? "DONE" : messageBadge)
			.replace(/\{\{BADGE\}\}/gi, data[i].newMessages || (data[i].done ? "DONE" : data[i].matches))
			.replace(/\{\{TYPE\}\}/gi, data[i].type);

		rowItemHtmlArr.push(tpl);
	}

	return rowItemHtmlArr.join('');

}