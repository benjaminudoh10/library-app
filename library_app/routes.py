from datetime import date, timedelta

from flask import render_template, flash, jsonify
from flask import request, jsonify, redirect, url_for
from flask_login import (
    current_user, login_user, logout_user, login_required)

from library_app import app, models, db, forms

@app.route('/')
@login_required
def index():
    return render_template('_blank.html')


@app.route('/auth', methods=['POST', 'GET'])
def login():
    context = {}

    login_form = forms.LoginForm()
    register_form = forms.RegisterForm()

    context['login_form'] = login_form
    context['register_form'] = register_form

    if login_form.login_submit.data and \
        login_form.validate_on_submit():
        email = login_form.login_email.data.strip()
        password = login_form.login_password.data.strip()
        remember = login_form.remember_me.data
        user = db.session.query(models.User).filter_by(email=email).first()
        print(f'\n\nUser: {user}')
        if user and user.verify_password(password):
            login_user(user, remember)
            flash('Login successful')
            return redirect(request.args.get('next') or url_for('index'))
        else:
            flash('Username or password incorrect')
    
    if register_form.register_submit.data and \
        register_form.validate_on_submit():
        fullname = register_form.fullname.data.strip()
        username = register_form.username.data.strip()
        email = register_form.email.data.strip()
        phone = register_form.phone.data.strip()
        password = register_form.password.data
        user = models.User(
            name=fullname,
            phone=phone,
            username=username,
            email=email,
            password=password
        )
        try:
            db.session.add(user)
            db.session.commit()
        except:
            db.session.rollback()

    return render_template('auth.html', **context)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.')
    return redirect(url_for('index'))


@app.route('/authors', methods=['POST', 'GET'])
@login_required
def author():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        author = models.Author(
            name=name,
            email=email
        )
        try:
            db.session.add(author)
            db.session.commit()
        except:
            db.session.rollback()
        return jsonify({'status': 'OK'})
    elif request.method == 'GET' and not request.is_xhr:
        return render_template('authors.html')
    elif request.method == 'GET' and request.is_xhr:
        authors = db.session.query(models.Author).all()
        authors_json = [author.to_json() for author in authors]
        return jsonify({
            'authors': authors_json
        })


@app.route('/authors/<author_id>', methods=['DELETE'])
@login_required
def delete_author(author_id):
    try:
        author = db.session.query(models.Author).get(int(author_id))
        db.session.delete(author)
        db.session.commit()
        return jsonify({
            'message': 'Author deleted successfully.'
        })
    except:
        db.session.rollback()
        return jsonify({
            'error': 'Error encountered while deleting author. Rolling back transaction.'
        })


@app.route('/books', methods=['POST', 'GET'])
@login_required
def book():
    if request.method == 'POST':
        title = request.form['title']
        edition = request.form['edition']
        isbn = request.form['isbn']
        pages = request.form['pages']
        year = request.form['year']
        copies = request.form['copies']
        description = request.form['description']
        author_id = request.form['author']
        author = db.session.query(models.Author).get(int(author_id))
        book = models.Book(
            title=title,
            edition=edition,
            isbn=isbn,
            pages=pages,
            year=year,
            copies=copies,
            description=description,
            author=author
        )
        try:
            db.session.add(book)
            db.session.commit()
        except:
            db.session.rollback()
        return jsonify({'status': 'OK'})
    elif request.method == 'GET' and not request.is_xhr:
        return render_template('books.html')
    elif request.method == 'GET' and request.is_xhr:
        books = db.session.query(models.Book).all()
        authors = db.session.query(models.Author).all()
        books_json = [book.to_json() for book in books]
        authors_json = [author.to_json() for author in authors]
        return jsonify({
            'books': books_json,
            'authors': authors_json
        })


@app.route('/books/<book_id>', methods=['DELETE'])
@login_required
def delete_book(book_id):
    try:
        book = db.session.query(models.Book).get(int(book_id))
        db.session.delete(book)
        db.session.commit()
        return jsonify({
            'message': 'Book deleted successfully.'
        })
    except:
        db.session.rollback()
        return jsonify({
            'error': 'Error encountered while deleting book. Rolling back transaction.'
        })


@app.route('/books/<book_id>/borrow', methods=['POST', 'GET'])
@login_required
def borrow_book(book_id):
    if request.method == 'POST':
        book = db.session.query(models.Book).get(int(book_id))
        from_date = date.today() # request.form['from_date']
        to_date = date.today() + timedelta(days=2) # request.form['to_date']
        book_borrowed = db.session.query(models.Borrowed).filter_by(
            book=book, user=current_user)
        if book_borrowed:
            return jsonify({
                'error': 'Book already in possession.'
            })
        if book.copies:
            try:
                borrowed = models.Borrowed(
                    book=book,
                    user=current_user,
                    _from=from_date,
                    to=to_date
                )
                book.copies -= 1
                db.session.add(borrowed)
                db.session.add(book)
                db.session.commit()
                return jsonify({
                    'message': 'Book borrowed successfully'
                })
            except:
                db.session.rollback()
                return jsonify({
                    'error': 'Encountered an error while borrowing this book. Try again later.'
                })
        else:
            return jsonify({
                'error': 'Books no longer in stock'
            })


@app.route('/hire', defaults={'id': 0}, methods=['GET', 'PUT', 'DELETE'])
@app.route('/hire/<int:id>', methods=['GET', 'PUT', 'DELETE'])
@login_required
def hire_requests(id):
    if request.method == 'GET':
        if request.is_xhr:
            hire_requests = db.session.query(models.Borrowed).all()
            hires = [hire.to_json() for hire in hire_requests]
            return jsonify({
                'hires': hires
            })
        else:
            return render_template('hire-requests.html')
    elif request.method == 'DELETE':
        # returning the borrowed book
        error = ''
        hired_request = db.session.query(models.Borrowed).get(int(id))
        if hired_request:
            book = hired_request.book
            if book:
                book.copies += 1
                try:
                    db.session.add(book)
                    db.session.commit()
                except:
                    db.session.rollback()
                    error = 'Book count increment failed'
            try:
                db.session.delete(hired_request)
                if not error:
                    db.session.commit()
                    return jsonify({
                        'message': 'Book has been returned successfully'
                    })
                else:
                    db.session.rollback()
                    return jsonify({
                        'error': error
                    })
            except:
                db.session.rollback()
                return jsonify({
                    'error': 'Failed to return book. Try again later.'
                })
    elif request.method == 'PUT':
        # extending the request
        hired_request = db.session.query(models.Borrowed).get(int(id))
        if hired_request:
            hired_request.to = hired_request.to + timedelta(days=2)
            try:
                db.session.add(hired_request)
                db.session.commit()
                return jsonify({
                    'message': 'Return date extended successfully'
                })
            except:
                db.session.rollback()
                return jsonify({
                    'error': 'Failed to extend return date.'
                })
