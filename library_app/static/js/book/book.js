$(document).ready(function () {
    window.allData = {};
    $.ajax({
        method: "GET",
        url: "/books",
        success: function(response) {
            if (response && response.books && response.books.length) {
                allData['books'] = response.books;
                for (var i = 0; i < allData.books.length; i++) {
                    var tr = $('<tr></tr>').addClass('book-row')
                        .append(
                            $('<td></td>').append(
                                allData.books[i].title + ' - '
                            )
                            .append(
                                $('<a></a>').addClass('book-detail')
                                .attr('href', '#' + allData.books[i].id)
                                .append('Details')
                            )
                        )
                        .append(
                            $('<td></td>').append(
                                allData.books[i].author
                                ? allData.books[i].author.name
                                : null
                            )
                        )
                        .append(
                            $('<td></td>').append(allData.books[i].copies)
                        )
                        .append(
                            $('<td></td>').append(allData.books[i].edition)
                        )
                        .append(
                            $('<td></td>').append(allData.books[i].isbn)
                        )
                        .append(
                            $('<td></td>').append(allData.books[i].year)
                        )
                        .append(
                            $('<td></td>').append(
                                $('<a></a>')
                                    .addClass('ui blue icon button hire book')
                                    .data('value', allData.books[i].id)
                                    .append($('<i></i>').addClass('cog icon'))
                            )
                            .append(
                                $('<a></a>')
                                    .addClass('ui green icon button edit book')
                                    .data('value', allData.books[i].id)
                                    .append($('<i></i>').addClass('edit icon'))
                            )
                            .append(
                                $('<a></a>')
                                    .addClass('ui red icon button delete book')
                                    .attr('data-value', allData.books[i].id)
                                    .append($('<i></i>').addClass('trash icon'))
                            )
                        );
                    $('#book-list tbody').append(tr);
                }
            }

            if (response && response.authors && response.authors.length) {
                allData['authors'] = response.authors;
                for (var j = 0; j < allData.authors.length; j++) {
                    var div = $('<div></div>')
                        .addClass('item')
                        .attr('data-value', allData.authors[j].id)
                        .append(
                            allData.authors[j] ?
                            allData.authors[j].name
                            : null
                        );
                    $('#authors-list').append(div);
                }
            }
        },
        error: function(error) {
            console.log('error ', error);
        }
    })

    $("#book-form").submit(function(event) {
        event.preventDefault();
        event.stopImmediatePropagation();
        $.ajax({
            method: "POST",
            url: "/books",
            data: $("#book-form").serialize(),
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

    // delete a book
    setTimeout(function () {
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

    // edit a book
    setTimeout(function () {
        $(".green.icon.button.edit.book").click(function(event) {
            event.preventDefault();
            event.stopImmediatePropagation();
            var value = $(this).data('value');
            var editForm = $('#book-form').clone();
            var currentBook = allData.books.map(function (book) {
                if (book.id == value) {
                    return book
                }
            });
            currentBook = currentBook[0];
            $('#bookDetailsModal').modal({
                onShow: function () {
                    $('#bookDetailsModal .header').val('Edit Book Details');
                    $('#display-book-details').hide();
                    $('#edit-book-details').show();
                    $('#edit-book-details').empty();
                    $('#edit-book-details').append(editForm);
                    $('#edit-book-details')
                        .find('input[name="title"]')
                        .val(currentBook.title);
                    $('#edit-book-details')
                        .find('input[name="edition"]')
                        .val(currentBook.edition);
                    $('#edit-book-details')
                        .find('input[name="isbn"]')
                        .val(currentBook.isbn);
                    $('#edit-book-details')
                        .find('input[name="year"]')
                        .val(currentBook.year);
                    $('#edit-book-details')
                        .find('input[name="pages"]')
                        .val(currentBook.pages);
                    $('#edit-book-details')
                        .find('input[name="copies"]')
                        .val(currentBook.copies);
                    $('#edit-book-details')
                        .find('textarea[name="description"]')
                        .val(currentBook.description);
                    $('#edit-book-details')
                        .find('input[name="author"]')
                        .val(currentBook.author ? currentBook.author.id : null);
                    $('.ui.dropdown').dropdown();
                }
            }).modal('show');
        });
    }, 1000);

    // hire a book
    setTimeout(function () {
        $('.blue.icon.button.hire.book').click(function(event) {
            event.preventDefault();
            event.stopImmediatePropagation();
            var value = $(this).data('value');
            var borrow_book =
                confirm('Are you sure you want to borrow this book?');
            if (!borrow_book) {
                return
            }
            $.ajax({
                method: 'POST',
                url: '/books/' + value + '/borrow',
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

    // display book info
    setTimeout(function () {
        $('.book-detail').click(function (event) {
            event.preventDefault();
            event.stopImmediatePropagation();
            var bookId = $(this).attr('href').substr(1);
            $('#bookDetailsModal').modal({
                onShow: function () {
                    $('#edit-book-details').hide();
                    $('#display-book-details').show();
                    var currentBook = allData.books.map(function (book) {
                        if (book.id == bookId) {
                            return book
                        }
                    });
                    currentBook = currentBook[0];
                    var titleRow = $('<tr></tr>').append(
                        $('<td></td>').addClass('warning').append('Title')
                    ).append(
                        $('<td></td>').addClass('positive').append(currentBook.title)
                    );
                    var editionRow = $('<tr></tr>').append(
                        $('<td></td>').addClass('warning').append('Edition')
                    ).append(
                        $('<td></td>').addClass('positive').append(currentBook.edition)
                    );
                    var yearRow = $('<tr></tr>').append(
                        $('<td></td>').addClass('warning').append('Year')
                    ).append(
                        $('<td></td>').addClass('positive').append(currentBook.year)
                    );
                    var priceRow = $('<tr></tr>').append(
                        $('<td></td>').addClass('warning').append('Price')
                    ).append(
                        $('<td></td>').addClass('positive').append(
                            currentBook.price || '---'
                        )
                    );
                    var isbnRow = $('<tr></tr>').append(
                        $('<td></td>').addClass('warning').append('ISBN')
                    ).append(
                        $('<td></td>').addClass('positive').append(currentBook.isbn)
                    );
                    var pagesRow = $('<tr></tr>').append(
                        $('<td></td>').addClass('warning').append('Pages')
                    ).append(
                        $('<td></td>').addClass('positive').append(currentBook.pages)
                    );
                    var copiesRow = $('<tr></tr>').append(
                        $('<td></td>').addClass('warning').append('Copies')
                    ).append(
                        $('<td></td>').addClass('positive').append(currentBook.copies)
                    );
                    var descriptionRow = $('<tr></tr>').append(
                        $('<td></td>').addClass('warning').append('Description')
                    ).append(
                        $('<td></td>').addClass('positive').append(currentBook.description)
                    );
                    var authorRow = $('<tr></tr>').append(
                        $('<td></td>').addClass('warning').append('Author')
                    ).append(
                        $('<td></td>').addClass('positive').append(
                            currentBook.author
                            ? currentBook.author.name
                            : '---'
                        )
                    );

                    $('#bookDetailsModal #details').empty();

                    $('#bookDetailsModal #details')
                        .append(titleRow)
                        .append(editionRow)
                        .append(yearRow)
                        .append(priceRow)
                        .append(isbnRow)
                        .append(pagesRow)
                        .append(copiesRow)
                        .append(descriptionRow)
                        .append(authorRow)
                }
            }).modal('show');
        });
    }, 1000);
});
