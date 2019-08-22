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

    $("#author-form").submit(function(event) {
        event.preventDefault();
        event.stopImmediatePropagation();
        $.ajax({
            method: "POST",
            url: "/authors",
            data: $("#author-form").serialize(),
            success: function(response) {
                var json = JSON.parse(response);
                if (response && json.status === 'OK') {
                    window.location.reload();
                }
            },
            error: function(error) {
                console.log('error ', error);
            }
        })
    });

    $(".red.icon.button.delete.author").click(function(event) {
        event.preventDefault();
        event.stopImmediatePropagation();
        var value = $(this).data('value');
        var delete_author =
            confirm('Are you sure you want to delete this author?');
        if (!delete_author) {
            return
        }
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

    $("#book-form").submit(function(event) {
        event.preventDefault();
        event.stopImmediatePropagation();
        $.ajax({
            method: "POST",
            url: "/books",
            data: $("#book-form").serialize(),
            success: function(response) {
                var json = JSON.parse(response);
                if (response && json.status === 'OK') {
                    window.location.reload();
                }
            },
            error: function(error) {
                console.log('error ', error);
            }
        })
    });

    $(".red.icon.button.delete.book").click(function(event) {
        event.preventDefault();
        event.stopImmediatePropagation();
        var value = $(this).data('value');
        var delete_book =
            confirm('Are you sure you want to delete this book?');
        if (!delete_book) {
            return
        }
        $.ajax({
            method: "DELETE",
            url: "/books/" + value,
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
    
    $('.book-detail').click(function (event) {
        event.preventDefault();
        event.stopImmediatePropagation();
        // $(this).attr('href').substr(1);
        $('#bookDetailsModal').modal('show');
    });
});
