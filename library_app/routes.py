from flask import render_template, flash
from flask import request, jsonify, redirect, url_for, json
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
        return json.dumps({'status': 'OK'})
    elif request.method == 'GET':
        authors = db.session.query(models.Author).all()
        return render_template('authors.html', authors=authors)


@app.route('/authors/<author_id>', methods=['DELETE'])
@login_required
def delete_author(author_id):
    try:
        author = db.session.query(models.Author).get(int(author_id))
        db.session.delete(author)
        db.session.commit()
        return json.dumps({'message': 'Author deleted successfully.'})
    except:
        db.session.rollback()
        return json.dumps({'error': 'Error encountered while deleting author. Rolling back transaction.'})