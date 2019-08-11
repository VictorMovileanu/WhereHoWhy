
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

let inputCount = 3;

$('body').on('click', '.btn__add', function () {
    const inputGroup = $(this).closest(".input-group");
    let clone = inputGroup.clone();
    let name = clone.find('input').attr('name');
    let new_name = name.split('_')[0] + "_" + inputCount;
    inputCount += 1;
    clone.find('input').attr('name', new_name);
    clone.appendTo(inputGroup.parent());
    initDatePicker()
});

$('body').on('click', '.btn__remove', function () {
    const inputGroup = $(this).closest(".input-group");
    if (inputGroup.parent().children('.input-group').length > 1) {
        inputGroup.remove()
    }
});

$('body').on('click', '.js-datepickerButton', function () {
   $(this).parents().prev('.js-datepickerInput').click()
});

function initDatePicker () {
    $('.js-datepickerInput').daterangepicker({
        locale: {
          format: 'DD/MM/YYYY'
        }
    }).on('apply.daterangepicker', function(ev, picker) {
        const date_from = picker.startDate.format('DD/MM/YYYY');
        const date_until = picker.endDate.format('DD/MM/YYYY');
        $(this).attr('data-from', date_from);
        $(this).attr('data-until', date_until);
    });
}

initDatePicker();
