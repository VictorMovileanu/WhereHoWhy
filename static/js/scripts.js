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
    const table_row = "<tr><td>" + city.val() + "</td><td>" + price.val() + "</td><td><span class='dot' style='background-color: " + color.val() + "'></span></td></tr>";
    $(table_row).insertAfter(".table-header");
    city.empty();
    price.empty();
    color.empty()
});