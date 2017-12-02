const listingData = [{
	"id": 1,
	"from": "japan",
	"to": "manila",
	"date": "December 26, 2017",
	"matches": 3,
	"type": "money",
	"alias": "nin",
	"time": "7:00PM",
	"amount": "10,254.34 PHP"
}, {
	"id": 2,
	"from": "manila",
	"to": "cebu",
	"date": "December 29, 2017",
	"matches": 10,
	"type": "baggage",
	"alias": "nin",
	"time": "7:00PM",
	"amount": "10,254.34 PHP",
	"done": true
}];

const matchesData = [{
	"id": 1,
	"from": "japan",
	"to": "manila",
	"date": "December 26, 2017",
	"newMessages": 4,
	"type": "money",
	"alias": "nin",
	"time": "7:00PM",
	"amount": "10,254.34 PHP",
	"done" : true
}, {
	"id": 2,
	"from": "manila",
	"to": "cebu",
	"date": "December 29, 2017",
	"newMessages": 2,
	"type": "baggage",
	"alias": "nin",
	"time": "7:00PM",
	"amount": "10,254.34 PHP"
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


	if ($(target).hasClass('done')) {
		return;
	}

	if ($(target).data('type') === 'listing') {
		//mock request
		matches(target, matchesData)
		return;
	}


	open('/details.html?id='+target.data('id'));
}

function matches(holder, _matchesData) {
	//mockUrlRequest
	const tpl = template(_matchesData, MATCHES);

	$('.matches', holder).html(tpl);

}

function listings() {
	const tpl = template(listingData, LISTINGS);

	$('#listings').html(tpl);
}

function template(data, type) {
	let rowItemHtmlArr = [];
	const chevBadge = '<i class="chevron material-icons">keyboard_arrow_down</i>';
	const messageBadge = '<i class="material-icons">message</i>';

	for (let i=0; i< data.length; i++) {
		const tpl = $(templates[type]).html()
			.replace(/\{\{DONE\}\}/gi, data[i].done ? "done" : "")
			.replace(/\{\{ID\}\}/gi, data[i].id)
			.replace(/\{\{FROM\}\}/gi, data[i].from)
			.replace(/\{\{TO\}\}/gi, data[i].to)
			.replace(/\{\{DATE\}\}/gi, data[i].date)
			.replace(/\{\{ALIAS\}\}/gi, data[i].alias)
			.replace(/\{\{TIME\}\}/gi, data[i].time)
			.replace(/\{\{AMOUNT\}\}/gi, data[i].amount)
			.replace(/\{\{CHEV\}\}/gi, data[i].done ? "" : chevBadge)
			.replace(/\{\{MESSAGE_BADGE\}\}/gi, data[i].done ? "DONE" : messageBadge)
			.replace(/\{\{BADGE\}\}/gi, data[i].newMessages || (data[i].done ? "DONE" : data[i].matches))
			.replace(/\{\{TYPE\}\}/gi, data[i].type);

		rowItemHtmlArr.push(tpl);
	}

	return rowItemHtmlArr.join('');

}