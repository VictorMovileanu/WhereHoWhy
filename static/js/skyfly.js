
let iataCodesArray = [];

$.getJSON('/skyfly/data/iata-codes', function (json) {
    iataCodesArray = json['data']
});

$('.js-addDestination').on("click", function () {
    const city = $("#city");
    const iata_code = city.val().toUpperCase();
    const price = $("#price");
    const color = $("#color");
    if (iataCodesArray.some(e => e === iata_code)) {
        const table_row =
            `<tr class='data-row' data-city='${iata_code}' data-price='${price.val()}' data-color='${color.val()}'>` +
                `<td>${iata_code}</td>` +
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

// js-deleteRow
$('table').on("click", ".js-deleteRow", function () {
    $(this).closest('.data-row').remove()
});

$('.js-readTable').on("click", function () {
    /*
    * Submission data format:
    * {
    *   'destination-table': [{'city': $, 'price': $, 'color': $}, ...],
    *   'date-table': [{'from': 'dd/mm/yyyy', 'until': 'dd/mm/yyyy'], ...]
    * }
    * */
    const tableData = {};
    tableData['city-from'] = $('#city-from').val().toUpperCase();
    $('.data-table').each(function () {
        let table_id = this.id;
        tableData[table_id] = [];
        $(`#${table_id} .data-row`).each(function () {
            tableData[table_id].push($(this).data());
        });
    });
    submitData(tableData);
});

function submitData(data) {
    $.ajax({
        url: '.',
        type: 'POST',
        data: {'data': JSON.stringify(data)},
        success: function (data) {
            window.location.href = data['redirect_url']
        },
        error: function (jqXHR, textStatus, errorThrown) {
            alert(jqXHR.responseJSON['message'])
        }
    })
}