$(document).ready(function () {
    $.ajax({
        method: "GET",
        url: "/hire",
        success: function(response) {
            if (response &&response.hires && response.hires.length) {
                allData = response.hires;
                for (var i = 0; i < allData.length; i++) {
                    var tr = $('<tr></tr>').addClass('hire-row')
                        .append(
                            $('<td></td>').append(
                                allData[i].book.title
                            )
                        )
                        .append(
                            $('<td></td>').append(
                                allData[i].user.name
                            )
                        )
                        .append(
                            $('<td></td>').append(allData[i].from)
                        )
                        .append(
                            $('<td></td>').append(allData[i].to)
                        )
                        .append(
                            $('<td></td>').append(
                                $('<a></a>')
                                    .addClass('ui basic small blue button return-hire')
                                    .data('value', allData[i].id)
                                    .append('Return')
                            )
                        )
                        .append(
                            $('<td></td>').append(
                                $('<a></a>')
                                    .addClass('ui basic small blue button extend-hire')
                                    .data('value', allData[i].id)
                                    .append('Extend Rent')
                            )
                        );
                    $('#hire-list tbody').append(tr);
                }
            }
        },
        error: function(error) {
            console.log('error ', error);
        }
    })

    // return a book
    setTimeout(function () {
        $(".blue.button.return-hire").click(function(event) {
            event.preventDefault();
            event.stopImmediatePropagation();
            var value = $(this).data('value');
            var return_book =
                confirm('Are you sure you want to return this book?');
            if (!return_book) {
                return
            }
            $.ajax({
                method: "DELETE",
                url: "/hire/" + value,
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
    }, 1000);

    // extend a book rentage
    setTimeout(function () {
        $(".blue.button.extend-hire").click(function(event) {
            event.preventDefault();
            event.stopImmediatePropagation();
            var value = $(this).data('value');
            var extend_hire =
                confirm('Are you sure you want to extend the hire of this book?');
            if (!extend_hire) {
                return
            }
            $.ajax({
                method: "PUT",
                url: "/hire/" + value,
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
    }, 1000);
});
