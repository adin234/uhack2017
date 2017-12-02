const listingData = [{
	"id": 1,
	"from": "japan",
	"to": "manila",
	"date": "December 26, 2017",
	"matches": 3,
	"type": "money"
}, {
	"id": 2,
	"from": "manila",
	"to": "cebu",
	"date": "December 29, 2017",
	"matches": 10,
	"type": "baggage"
}];

const matchesData = [{
	"id": 1,
	"from": "japan",
	"to": "manila",
	"date": "December 26, 2017",
	"newMessages": 4,
	"type": "money"
}, {
	"id": 2,
	"from": "manila",
	"to": "cebu",
	"date": "December 29, 2017",
	"newMessages": 2,
	"type": "baggage"
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

	for (let i=0; i< data.length; i++) {
		const tpl = $(templates[type]).html()
			.replace(/\{\{ID\}\}/gi, data[i].id)
			.replace(/\{\{FROM\}\}/gi, data[i].from)
			.replace(/\{\{TO\}\}/gi, data[i].to)
			.replace(/\{\{DATE\}\}/gi, data[i].date)
			.replace(/\{\{BADGE\}\}/gi, data[i].newMessages || data[i].matches)
			.replace(/\{\{TYPE\}\}/gi, data[i].type);

		rowItemHtmlArr.push(tpl);
	}

	return rowItemHtmlArr.join('');

}