$('.js-readTable').on("click", function () {
    /*
    * Submission data format:
    * {
    *   'destination-table': [{'city': $, 'price': $, 'color': $}, ...],
    *   'date-table': [{'from': 'dd/mm/yyyy', 'until': 'dd/mm/yyyy'], ...]
    * }
    * */
    const tableData = {};
    $('table').each(function () {
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
        error: function (response) {
            alert(response['error_msg'])
        }
    })
}