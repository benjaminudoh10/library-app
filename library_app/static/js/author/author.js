$(document).ready(function () {
    window.allAuthors = [];
    $.ajax({
        method: "GET",
        url: "/authors",
        success: function(response) {
            if (response && response.authors.length) {
                allAuthors = response.authors;
                for (var i = 0; i < allAuthors.length; i++) {
                    var tr = $('<tr></tr>').addClass('author-row')
                        .append(
                            $('<td></td>').append(allAuthors[i].name)
                        )
                        .append(
                            $('<td></td>').append(allAuthors[i].email)
                        )
                        .append(
                            $('<td></td>').append(
                                $('<a></a>')
                                    .addClass('ui green icon button edit author')
                                    .data('value', allAuthors[i].id)
                                    .append($('<i></i>').addClass('edit icon'))
                            )
                            .append(
                                $('<a></a>')
                                    .addClass('ui red icon button delete author')
                                    .attr('data-value', allAuthors[i].id)
                                    .append($('<i></i>').addClass('trash icon'))
                            )
                        );
                    $('#author-list tbody').append(tr);
                }
            }
        },
        error: function(error) {
            console.log('error ', error);
        }
    })

    $("#author-form").submit(function(event) {
        event.preventDefault();
        event.stopImmediatePropagation();
        $.ajax({
            method: "POST",
            url: "/authors",
            data: $("#author-form").serialize(),
            success: function(response) {
                if (response && response.status === 'OK') {
                    window.location.reload();
                }
            },
            error: function(error) {
                console.log('error ', error);
            }
        })
    });

    setTimeout(function () {
        $(".red.icon.button.delete.author").click(function(event) {
            event.preventDefault();
            event.stopImmediatePropagation();
            var value = $(this).data('value');
            var delete_author =
                confirm('Are you sure you want to delete this book?');
            if (!delete_author) {
                return
            }
            $.ajax({
                method: "DELETE",
                url: "/authors/" + value,
                success: function(response) {
                    if (response) {
                        if (response.error) {
                            console.log('error ', response)
                        } else if (response.message) {
                            window.location.reload();
                        }
                    }
                },
                error: function(error) {
                    console.log('error ', error);
                }
            })
        });
    }, 1000)
})