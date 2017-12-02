const listingData = [{
	"id": 1,
	"amount": "10,523.00 PHP",
	"from": "japan",
	"to": "manila",
	"date": "December 26, 2017",
	"matches": 3,
	"type": "money",
	"alias": "nin" 
}, {
	"id": 2,
	"amount": "10,523.00 PHP",
	"from": "manila",
	"to": "cebu",
	"date": "December 29, 2017",
	"matches": 10,
	"type": "baggage",
	"alias": "nin"
}, {
	"id": 2,
	"amount": "10,523.00 PHP",
	"from": "manila",
	"to": "cebu",
	"date": "December 29, 2017",
	"matches": 10,
	"type": "baggage",
	"alias": "nin"
}];

const matchesData = [{
	"id": 1,
	"amount": "10,523.00 YEN",
	"from": "japan",
	"to": "manila",
	"date": "December 26, 2017",
	"newMessages": 4,
	"time": "7:00PM",
	"type": "money",
	"alias": "nin"
}, {
	"id": 2,
	"amount": "10,523.00 YEN",
	"from": "manila",
	"to": "cebu",
	"date": "December 29, 2017",
	"newMessages": 2,
	"time": "7:00PM",
	"type": "baggage",
	"alias": "nin"
}, {
	"id": 2,
	"amount": "10,523.00 YEN",
	"from": "manila",
	"to": "cebu",
	"date": "December 29, 2017",
	"newMessages": 2,
	"time": "7:00PM",
	"type": "baggage",
	"alias": "nin"
}];

const MATCHES = 0;
const LISTINGS = 1;

const templates = [
	'#tpl-matches',
	'#tpl-listings'
];

function pageStart() {
	pageBind();
	listings();
}

function pageBind() {
	$('#listings').on('click', '.listing', showListing);
}

function showListing(e) {
	const target = $(e.currentTarget);

	$('.listing-data').css('background-color', 'white');
	$('.material-icons.chevron').html('keyboard_arrow_down');

	if ($(target).data('type') === 'listing') {
		//mock request

		$('.matches').html("");
		matches(target, matchesData)
		return;
	}


	open('/details.html?id='+target.data('id'));
}

function matches(holder, _matchesData) {
	//mockUrlRequest
	const tpl = template(_matchesData, MATCHES);

	if ($('.matches', holder).html().trim() != "") {
		$('.matches', holder).html("");
		
		$('.listing-data', holder).css('background-color', 'white');

		return;
	}

	$('.listing-data', holder).css('background-color', '#FEE0D2');
	$('.matches', holder).html(tpl);
	$('.material-icons.chevron', holder).html('keyboard_arrow_up');

}

function listings() {
	const tpl = template(listingData, LISTINGS);

	$('#listings').html(tpl);
}

function template(data, type) {
	let rowItemHtmlArr = [];

	for (let i=0; i< data.length; i++) {
		const tpl = $(templates[type]).html()
			.replace(/\{\{ID\}\}/gi, data[i].id)
			.replace(/\{\{FROM\}\}/gi, data[i].from)
			.replace(/\{\{TO\}\}/gi, data[i].to)
			.replace(/\{\{DATE\}\}/gi, data[i].date)
			.replace(/\{\{BADGE\}\}/gi, data[i].newMessages || data[i].matches)
			.replace(/\{\{TYPE\}\}/gi, data[i].type)
			.replace(/\{\{AMOUNT\}\}/gi, data[i].amount)
			.replace(/\{\{ALIAS\}\}/gi, data[i].alias)
			.replace(/\{\{TIME\}\}/gi, data[i].time);

		rowItemHtmlArr.push(tpl);
	}

	return rowItemHtmlArr.join('');

}