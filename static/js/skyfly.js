
let iataCodesArray = [];

$.getJSON('/skyfly/data/iata-codes', function (json) {
    iataCodesArray = json['data']
});

function submitData(data) {
    event.preventDefault();
    let form = $(event.target);
    form.find('.is-invalid').each( function () {
        $(this).removeClass('is-invalid')
    });
    form.find('.message').remove();
    form.find('.invalid-feedback').remove();
    $.ajax({
        url: '.',
        type: 'POST',
        data: form.serialize(),
        success: function (data) {
            $('.progress').css('display', 'flex');
            updateProgress(data['status-url'])
        },
        error: function (jqXHR, textStatus, errorThrown) {
            const input_errors = jqXHR.responseJSON['input-errors'];
            const non_field_errors = jqXHR.responseJSON['non-field-errors'];
            for (i = 0; i < input_errors.length; i++) {
                let name = input_errors[i]['input_name'];
                let message = input_errors[i]['message'];
                const input_field = $('input[name="' + name + '"]');
                input_field.addClass('is-invalid');
                input_field.parent().append('<div class="invalid-feedback">' + message + '</div>')
            }
            for (i = 0; i < non_field_errors.length; i++) {
                $(form).prepend('<div class="message alert alert-danger" role="alert">' + non_field_errors [i] + '</div>')
            }
        },
    })
}

function updateProgress(url) {
  $.ajax({
    url: url,
    success: function(data) {
        if (data['progress'] === 100) {
            window.location = data['redirect_url']
        } else {
            $('.progress-bar').css('width', String(data['progress']) + "%")
        }
    },
    complete: function() {
      // Schedule the next request when the current one's complete
      setTimeout(function(){updateProgress(url)}, 1000);
    }
  });
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
