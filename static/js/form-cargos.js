$(document).ready(function () {
    const $cargoSelect = $('select[name="cargo"]');

    $cargoSelect.select2({
        theme: 'bootstrap-5',
        width: '100%',
        placeholder: 'Selecione um cargo',
    });

    // Ajustes visuais para alinhar com form-control-lg do Bootstrap 5
    const $selectStyled = $('.select2-container--bootstrap-5 .select2-selection--single');

    $selectStyled.css({
        'height': 'calc(2.875rem + 2px)',   // form-control-lg
        'padding': '0.375rem 0.75rem',
        'font-size': '1.25rem',
        'line-height': '1.5',
        'border': '1px solid #ced4da',
        'border-radius': '0.375rem',
        'background-color': '#fff',
        'display': 'flex',
        'align-items': 'center',
        'box-shadow': 'none'
    });
    
    $('<style>')
    .prop('type', 'text/css')
    .html(`
        .select2-container--bootstrap-5 .select2-results__option--highlighted {
            background-color: #0d6efd !important;
            color: white !important;
        }
    `)
    .appendTo('head');

    $('.select2-selection__rendered').css({
        'line-height': '1.5'
    });
});
