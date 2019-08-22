from datetime import datetime
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

from library_app import db
from . import login_manager


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(UserMixin, db.Model):
    '''
    This model describes a user.
    '''
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    phone = db.Column(
        db.String, nullable=False, index=True, unique=True)
    username = db.Column(
        db.String, nullable=False, unique=True, index=True)
    email = db.Column(
        db.String, nullable=False, index=True, unique=True)
    password_hash = db.Column(db.String(128))
    # role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))
    role = db.Column(db.String, nullable=False, default='member')
    books = db.relationship('Book', backref='user')

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return '<User {}, {}>'.format(self.name, self.email)


# class Role(db.Model):
#     '''
#     This model describes the role of a user (currently admin and regular)
#     '''
#     __tablename__ = 'roles'
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(64), unique=True)
#     users = db.relationship('User', backref='role')

#     def __repr__(self):
#         return '<Role {}>'.format(self.name)


class Book(db.Model):
    '''
    This model describes a book.
    '''
    __tablename__ = 'books'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    edition = db.Column(db.String, nullable=False, index=True)
    year = db.Column(db.String, nullable=False, index=True)
    price = db.Column(db.String)
    isbn = db.Column(db.String, nullable=False)
    pages = db.Column(db.Integer)
    copies = db.Column(db.Integer, nullable=False)
    description = db.Column(db.String)
    author_id = db.Column(db.Integer, db.ForeignKey('authors.id'))
    # Current user with the book
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    def __repr__(self):
        return '<Book {} {}>'.format(self.title, self.isbn)


class Author(db.Model):
    '''
    This model describes an author
    '''
    __tablename__ = 'authors'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    email = db.Column(db.String, nullable=False, index=True)
    books = db.relationship('Book', backref='author')

    def __repr__(self):
        return '<Author {} {}>'.format(self.name, self.email)


# class Borrowed(db.Model):
#     '''
#     This model describes the relationship between a book
#     and the user who borrowed it
#     '''
