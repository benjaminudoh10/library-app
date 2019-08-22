import os
basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    # Database Configuration for the application
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_FILE') or \
        'sqlite:///' + os.path.join(basedir, 'library-app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = 'dfhgjkliuytdbn34jbvdut456kmnbdsxnmkgfdw@#$$jkt'

