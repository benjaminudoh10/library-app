$(document).ready(function () {
    $('a[data-toggle="popup"]').each(function () {
        $(this).popup({
            popup: $(this).attr('data-content'),
            position: $(this).attr('data-position'),
            on: 'click'
        })
    });

    $('.ui.accordion').accordion();
    $('.ui.dropdown').dropdown();
    $('.ui.checkbox').checkbox();
    $('.ui.progress').progress();

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

    $("#author-form").submit(function(event) {
        event.preventDefault();
        event.stopImmediatePropagation();
        $.ajax({
            method: "POST",
            url: "/authors",
            data: $("#author-form").serialize(),
            success: function(response) {
                console.log('resp ', response.status);
                if (response && JSON.parse(response).status === 'OK') {
                    window.location.reload();
                }
            },
            error: function(error) {
                console.log('error ', error);
            }
        })
    });

    $(".red.icon.button.delete").click(function(event) {
        event.preventDefault();
        event.stopImmediatePropagation();
        var value = $(this).data('value');
        $.ajax({
            method: "DELETE",
            url: "/authors/" + value,
            success: function(response) {
                var json = JSON.parse(response);
                if (response) {
                    if (json.error) {
                        console.log('error ', response)
                    } else if (json.message) {
                        window.location.reload();
                    }
                }
            },
            error: function(error) {
                console.log('error ', error);
            }
        })
    });
});
