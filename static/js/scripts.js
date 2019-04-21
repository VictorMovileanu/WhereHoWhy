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
    const table_row =
        `<tr class='data-row' data-city='${city.val()}' data-price='${price.val()}' data-color='${color.val()}'>` +
            `<td>${city.val()}</td>` +
            `<td>${price.val()}</td>` +
            `<td><span class='dot' style='background-color: ${color.val()}'></span></td>` +
            `<td><button class='js-deleteRow' type='button'>X</button></td>` +
        "</tr>";
    $('tbody').append(table_row);
    city.val('');
    price.val('');
    color.val('#000000')
});

$('.js-readTable').on("click", function () {
    let tableData = [];
    $('.data-row').each(function () {
        tableData.push($(this).data());
    });
    console.log(tableData);
});

$('table').on("click", ".js-deleteRow", function () {
    $(this).closest('.data-row').remove()
});