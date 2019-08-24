$(document).ready(function () {
    $('a[data-toggle="popup"]').each(function () {
        $(this).popup({
            popup: $(this).attr('data-content'),
            position: $(this).attr('data-position'),
            on: 'click'
        })
    });

    $('.ui.dropdown').dropdown();
    $('.ui.checkbox').checkbox();
    $('.ui.progress').progress();
    $('.ui.modal').modal();

    $('#showToggle').hide();
    $('#hideToggle').show();
    $('#hideToggle').click(function () {
        $('#hideToggle').hide();
        $('#showToggle').show();
        $('#sideMenu').addClass('hide');
    });
    $('#showToggle').click(function () {
        $('#showToggle').hide();
        $('#hideToggle').show();
        $('#sideMenu').removeClass('hide');
    });

    $('.message .close').on('click', function() {
        $(this).closest('.message').hide();
    });
});
