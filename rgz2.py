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

def initialize_storage_cells():
    conn, cur = db_connect()
    try:
        # Вставка 100 ячеек, если они еще не существуют
        for _ in range(100):
            cur.execute("INSERT INTO storage_cells (is_occupied, username) VALUES (%s, %s);", (False, None))

        # Сохранение изменений
        conn.commit()
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        db_close(conn, cur)


@rgz2.route('/rgz2/')
def rgz():
    return render_template('/rgz2/rgz2.html', user = session.get('login'))



@rgz2.route('/rgz2/register', methods = ['POST', 'GET'])
def register():
    if request.method == 'GET':
        return render_template('rgz2/register.html')

    login = request.form.get('login')
    password = request.form.get('password')

    if not (login and password):
        return render_template('rgz2/register.html', error='Заполните все поля')

    conn, cur = db_connect()

  # Используйте параметризованный запрос для проверки наличия пользователя
    if current_app.config['DB_TYPE'] == 'postgres':
        cur.execute("SELECT login FROM users WHERE login=%s", (login,))
    else:
        cur.execute("SELECT login FROM users WHERE login=?", (login,))

    if cur.fetchone():
        db_close(conn, cur)
        return render_template('rgz2/register.html', error = 'Такой пользователь уже существует')

  # Используйте параметризованный запрос для вставки данных

    password_hash = generate_password_hash(password)

    if current_app.config['DB_TYPE'] == 'postgres':
        cur.execute("INSERT INTO users (login, password) VALUES (%s, %s)", (login, password_hash))
    else:
        cur.execute("INSERT INTO users (login, password) VALUES (?, ?)", (login, password_hash))

    db_close(conn, cur)
    return render_template('rgz2/success.html', login = login)


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

@rgz2.route('/rgz2/logout')
def logout():
    session.pop('login', None)
    return redirect('/rgz2/') 


@rgz2.route('/rgz2/storage', methods=['GET'])
def storage():
    conn, cur = db_connect()
    try:
        # Получаем все ячейки из базы данных
        if current_app.config['DB_TYPE'] == 'postgres':
            cur.execute("SELECT * FROM storage_cells;")
        else:
            cur.execute("SELECT * FROM storage_cells;")

        cells = cur.fetchall()

        # Подсчитываем количество свободных и занятых ячеек
        occupied_cells = [cell for cell in cells if cell['is_occupied']]
        free_cells = [cell for cell in cells if not cell['is_occupied']]
        
        total_occupied = len(occupied_cells)
        total_free = len(free_cells)

        # Передаем данные в шаблон
        return render_template('rgz2/storage.html', 
                               cells=cells, 
                               total_occupied=total_occupied, 
                               total_free=total_free)
    finally:
        db_close(conn, cur)



