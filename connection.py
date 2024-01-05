# connection.py
from flask_mysqldb import MySQL
from flask import Flask

def create_app():
    app = Flask(__name__)
    app.config['MYSQL_HOST'] = 'localhost'
    app.config['MYSQL_USER'] = 'root'
    app.config['MYSQL_PASSWORD'] = ''
    app.config['MYSQL_DB'] = ''
    app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

    mysql = MySQL(app)

    return app, mysql
