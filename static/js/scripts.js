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

$('.js-addDestination').on("click", function () {
    let city = $("#city");
    let price = $("#price");
    let color = $("#color");
    const table_row = "<tr class='data-row'>" +
        `<td data-destination='${city.val()}'>${city.val()}</td>` +
        `<td data-destination='${price.val()}'>${price.val()}</td>` +
        `<td data-destination='${color.val()}'><span class='dot' style='background-color: ${color.val()}'></span></td>` +
        "</tr>";
    $(table_row).insertAfter(".table-header");
    city.val('');
    price.val('');
    color.val('#000000')
});

$('.js-readTable').on("click", function () {
    let tableData = {};
    let i = 0;
    $('.data-row').each(function () {
        let rowData = [];
        $('td', this).each(function () {
            rowData.push($(this).attr('data-destination'))
        });
        tableData[i] = rowData;
        i += 1;
    });
    console.log(tableData);
});