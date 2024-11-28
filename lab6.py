from flask import Blueprint, url_for, redirect, render_template, request, session, current_app
import psycopg2
from psycopg2.extras import RealDictCursor
from werkzeug.security import check_password_hash, generate_password_hash
import sqlite3
from os import path

lab6 = Blueprint('lab6', __name__)

offices = []
price_per_office = 1000  
for i in range(1, 11):
    offices.append({'number': i, 'tenant': '', 'price': price_per_office})


def db_connect():
    if current_app.config['DB_TYPE'] == 'postgres':
        conn = psycopg2.connect(dbname="webka", user="postgres", password="postgres", host="127.0.0.1", options="-c client_encoding=UTF8")
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

@lab6.route('/')
def home():
    return redirect(url_for('lab6.lab'))

@lab6.route('/lab6/')
def lab():
    username = session.get('login', '')
    return render_template('lab6/lab6.html', login=session.get('login'), username=username, offices=offices)

@lab6.route('/lab6/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('lab6/register.html')
    
    login = request.form.get('login')
    password = request.form.get('password')

    if not (login and password):
        return render_template('lab6/register.html', error='Заполните все поля')
    conn, cur = db_connect()

    if current_app.config['DB_TYPE'] == 'postgres':
        cur.execute("SELECT login FROM users WHERE login=%s;", (login,))
    else:
        cur.execute("SELECT login FROM users WHERE login=?;", (login,))
    if cur.fetchone():
        db_close(conn, cur)
        return render_template('lab6/register.html', error="Такой пользователь уже существует")
    password_hash = generate_password_hash(password)

    if current_app.config['DB_TYPE'] == 'postgres':
        cur.execute("INSERT INTO users (login, password) VALUES (%s, %s);", (login, password_hash))
    else:
        cur.execute("INSERT INTO users (login, password) VALUES (?, ?);", (login, password_hash))
    db_close(conn, cur)
    return render_template('lab6/success.html', login=login)


@lab6.route('/lab6/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('lab6/login.html')
    login = request.form.get('login')
    password = request.form.get('password')
    if not (login and password):
        return render_template('lab6/login.html', error="Заполните поля")
    conn, cur = db_connect()

    if current_app.config['DB_TYPE'] == 'postgres':
        cur.execute("SELECT * FROM users WHERE login=%s;", (login,))
    else:
        cur.execute("SELECT * FROM users WHERE login=?;", (login,))
    user = cur.fetchone()
    if not user or not check_password_hash(user['password'], password):
        db_close(conn, cur)
        return render_template('lab6/login.html', error='Логин и/или пароль неверны')
    session['login'] = login  
    db_close(conn, cur)
    return redirect(url_for('lab6.lab'))


@lab6.route('/lab6/logout')
def logout():
    session.pop('login', None) 
    return redirect(url_for('lab6.lab'))


@lab6.route('/lab6/json-rpc-api/', methods = ['POST'])
def api():
    try:
        data = request.json
        if data is None:
            return {'jsonrpc': '2.0', 'error': {'code': -32700, 'message': 'Parse error'}}, 400

        if data['method'] == 'info':
            conn, cur = db_connect()
            cur.execute("SELECT * FROM offices")
            offices_db = cur.fetchall()
            db_close(conn, cur)
            return {
                'jsonrpc': '2.0',
                'result': [{'number': office['number'], 'tenant': office['tenant'], 'price': office['price']} for office in offices_db],
                'id': data.get('id')
            }
        
        login = session.get('login')
        if not login:
            return {
                'jsonrpc': '2.0',
                'error': {
                    'code': 1, 
                    'message': 'Unauthorized'
                },
                'id': data.get('id')
            }

        if data['method'] == 'booking':
            office_number = data['params']
            conn, cur = db_connect()
            cur.execute("SELECT * FROM offices WHERE number = ?", (office_number,))
            office_db = cur.fetchone()
            if office_db and office_db['tenant'] != '':
                db_close(conn, cur)
                return {
                    'jsonrpc': '2.0',
                    'error': {
                        'code': 2,
                        'message': 'Already booked'
                    },
                    'id': data.get('id')
                }
            cur.execute("UPDATE offices SET tenant = ? WHERE number = ?", (login, office_number))
            db_close(conn, cur)
            return {
                'jsonrpc': '2.0',
                'result': 'success',
                'id': data.get('id')
            }
            
        if data['method'] == 'cancellation':
            office_number = data['params']
            conn, cur = db_connect()
            cur.execute("SELECT * FROM offices WHERE number = ?", (office_number,))
            office_db = cur.fetchone()
            if office_db and office_db['tenant'] == '':
                db_close(conn, cur)
                return {
                    'jsonrpc': '2.0',
                    'error': {
                        'code': 3,
                        'message': 'Офис не забронирован'
                    },
                    'id': data.get('id')
                }
            if office_db and office_db['tenant'] != login:
                db_close(conn, cur)
                return {
                    'jsonrpc': '2.0',
                    'error': {
                        'code': 4,
                        'message': 'Вы не можете отменить чужое бронирование.'
                    },
                    'id': data.get('id')
                }
            cur.execute("UPDATE offices SET tenant = NULL WHERE number = ?", (office_number,))
            db_close(conn, cur)
            return {
                'jsonrpc': '2.0',
                'result': 'success',
                'id': data.get('id')
            }

        return {
            'jsonrpc': '2.0',
            'error': {
                'code': -32601,
                'message': 'Method not found'
            },
            'id': data.get('id')
        }
    except Exception as e:
        return {'jsonrpc': '2.0', 'error': {'code': -32603, 'message': str(e)}}, 500
