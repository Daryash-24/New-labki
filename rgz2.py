from flask import Blueprint, redirect, url_for, render_template, render_template_string, abort, request, make_response, session,  current_app
from functools import wraps
import psycopg2
from psycopg2.extras import RealDictCursor
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3
from os import path

rgz2 = Blueprint('rgz2', __name__, static_folder='static')

def db_connect():

    if current_app.config['DB_TYPE'] == 'postgres':
        conn = psycopg2.connect(dbname="webka", 
        user="postgres", 
        password="postgres", 
        host="127.0.0.1"
        )
        cur = conn.cursor(cursor_factory = RealDictCursor)

    else:
        dir_path = path.dirname(path.realpath(__file__))
        db_path = path.join(dir_path, "database.db")
        conn = sqlite3.connect(db_path)
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()

    return conn, cur

def db_close(conn, cur):
    conn.commit()
    cur.close()
    conn.close()

@rgz2.route('/rgz2/')
def rgz():
    return render_template('/rgz2/rgz2.html', user = session.get('login'))


@rgz2.route('/rgz2/login', methods = ['POST', 'GET'])
def login():
    if request.method == 'GET':
        return render_template ('rgz2/login.html')
    
    login = request.form.get('login')
    password = request.form.get('password')

    if not (login or password):
        return render_template ('rgz2/login.html', error = 'Заполните поля')
    
    conn, cur = db_connect()
    cur = conn.cursor(cursor_factory = RealDictCursor)

    if current_app.config['DB_TYPE'] == 'postgres':
        cur.execute("SELECT * FROM users WHERE login=%s;", (login,))
    else:
        cur.execute("SELECT * FROM users WHERE login=?;", (login,))

    user = cur.fetchone()

    if not user:
        db_close(conn, cur)
        return render_template ('rgz2/login.html', error = 'Логин и/или пароль неверны')
    
    if not check_password_hash(user['password'], password):
        db_close(conn, cur)
        return render_template ('rgz2/login.html', error = 'Логин и/или пароль неверны')

    session['login'] = login
    db_close(conn, cur)
    return render_template ('rgz2/success_login.html', login = login)

