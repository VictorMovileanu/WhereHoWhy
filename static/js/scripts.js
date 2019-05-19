let timerIdentifier;
const doneTypingInterval = 500;
const $input_quote = $('textarea#id_quote');
const $input_source = $('input#id_source');
const $preview_quote = $('.tweet.preview blockquote');
const $preview_source = $('.tweet.preview cite');

$input_quote.on("keydown", function () {
    clearTimeout(timerIdentifier);
});

$input_source.on("keydown", function () {
    clearTimeout(timerIdentifier);
});

$input_quote.on("keyup", function () {
   clearTimeout(timerIdentifier);
   timerIdentifier = setTimeout($preview_quote.html($input_quote.val()), doneTypingInterval);
});

$input_source.on("keyup", function () {
   clearTimeout(timerIdentifier);
   timerIdentifier = setTimeout($preview_source.html($input_source.val()), doneTypingInterval);
});

let iataCodesArray = [];

$.getJSON('/skyfly/data/iata-codes', function (json) {
    iataCodesArray = json['data']
});

$('.js-addDestination').on("click", function () {
    const city = $("#city");
    const price = $("#price");
    const color = $("#color");
    if (iataCodesArray.some(e => e === city)) {
        const table_row =
            `<tr class='data-row' data-city='${city.val()}' data-price='${price.val()}' data-color='${color.val()}'>` +
                `<td>${city.val()}</td>` +
                `<td>${price.val()}</td>` +
                `<td><span class='dot' style='background-color: ${color.val()}'></span></td>` +
                `<td><button class='js-deleteRow' type='button'>X</button></td>` +
            "</tr>";
        $(this).closest('table').find('tbody').append(table_row);
        city.val('');
        price.val('');
        color.val('#000000')
    } else {
        alert('Airport IATA code does not exist')
    }

});

$('.js-addTimeFrame').on("click", function () {
    const from = $("#time_from");
    const until = $("#time_until");
    const ary_from = from.val().split('/');
    const ary_until = until.val().split('/');
    const a = `${ary_from[1]}/${ary_from[0]}/${ary_from[2]}`;
    const b = `${ary_until[1]}/${ary_until[0]}/${ary_until[2]}`;
    if ( Date.parse(a) < Date.parse(b) ) {
        const table_row =
            `<tr class='data-row' data-from='${from.val()}' data-until='${until.val()}'>` +
                `<td>${from.val()}</td>` +
                `<td>${until.val()}</td>` +
                `<td><button class='js-deleteRow' type='button'>X</button></td>` +
            "</tr>";
        $(this).closest('table').find('tbody').append(table_row);
        from.val('');
        until.val('');
    } else {
        alert('Start date must be smaller than end date!')
    }
});

// js-deleteRow
$('table').on("click", ".js-deleteRow", function () {
    $(this).closest('.data-row').remove()
});

$(function () {
    $('[data-toggle="datepicker"]').datepicker({
        format: 'dd/mm/yyyy'
    })
});
