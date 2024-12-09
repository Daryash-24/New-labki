from flask import Blueprint, redirect, url_for, render_template, render_template_string, abort, request, jsonify, session,  current_app
from functools import wraps
import psycopg2
from psycopg2.extras import RealDictCursor
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3
from os import path
import re

rgz2 = Blueprint('rgz2', __name__, static_folder='static')

def db_connect():
    if current_app.config['DB_TYPE'] == 'postgres':
        conn = psycopg2.connect(
            dbname="webka", 
            user="postgres", 
            password="postgres", 
            host="127.0.0.1"
        )
        cur = conn.cursor()  # Создаем курсор для PostgreSQL
    else:
        dir_path = path.dirname(path.realpath(__file__))
        db_path = path.join(dir_path, "database.db")
        conn = sqlite3.connect(db_path)
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()  # Создаем курсор для SQLite

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
            if current_app.config['DB_TYPE'] == 'postgres':
                cur.execute("INSERT INTO storage_cells (is_occupied, username) VALUES (%s, %s);", (False, None))
            else:
                cur.execute("INSERT INTO storage_cells (is_occupied, username) VALUES (?, ?);", (False, None))

        # Сохранение изменений
        conn.commit()
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        db_close(conn, cur)


@rgz2.route('/rgz2/')
def rgz():
    return render_template('/rgz2/rgz2.html', user = session.get('login'))



@rgz2.route('/rgz2/register', methods=['POST', 'GET'])
def register():
    if request.method == 'GET':
        return render_template('rgz2/register.html')

    login = request.form.get('login')
    password = request.form.get('password')

    # Проверка на пустые поля
    if not (login and password):
        return render_template('rgz2/register.html', error='Заполните все поля')

    # Валидация логина и пароля
    if not re.match(r'^[a-zA-Z0-9!_]+$', login):
        return render_template('rgz2/register.html', error='Логин может содержать только латинские буквы, цифры и символы ! и _')

    if not re.match(r'^[a-zA-Z0-9!_]+$', password):
        return render_template('rgz2/register.html', error='Пароль может содержать только латинские буквы, цифры и символы ! и _')

    conn, cur = db_connect()

    # Проверка наличия пользователя
    if current_app.config['DB_TYPE'] == 'postgres':
        cur.execute("SELECT login FROM users WHERE login=%s", (login,))
    else:
        cur.execute("SELECT login FROM users WHERE login=?", (login,))

    if cur.fetchone():
        db_close(conn, cur)
        return render_template('rgz2/register.html', error='Такой пользователь уже существует')

    # Хеширование пароля
    password_hash = generate_password_hash(password)

    # Вставка данных в базу
    if current_app.config['DB_TYPE'] == 'postgres':
        cur.execute("INSERT INTO users (login, password) VALUES (%s, %s)", (login, password_hash))
    else:
        cur.execute("INSERT INTO users (login, password) VALUES (?, ?)", (login, password_hash))

    db_close(conn, cur)
    return render_template('rgz2/success.html', login=login)


@rgz2.route('/rgz2/login', methods = ['POST', 'GET'])
def login():
    if request.method == 'GET':
        return render_template ('rgz2/login.html')
    
    login = request.form.get('login')
    password = request.form.get('password')

    if not (login or password):
        return render_template ('rgz2/login.html', error = 'Заполните поля')
    
    conn, cur = db_connect()

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

@rgz2.route('/rgz2/delete_user', methods=['DELETE'])
def delete_user():
    login = session.get('login')
    if not login:
        return jsonify({"error": "Unauthorized"}), 403

    conn, cur = db_connect()
    try:
        # Получаем пользователя по логину
        if current_app.config['DB_TYPE'] == 'postgres':
            cur.execute("SELECT * FROM users WHERE login = %s;", (login,))
        else:
            cur.execute("SELECT * FROM users WHERE login = ?;", (login,))
        
        user = cur.fetchone()

        if user is None:
            return jsonify({"error": "User  not found"}), 404

        # Освобождение забронированных ячеек
        if current_app.config['DB_TYPE'] == 'postgres':
            cur.execute("SELECT id FROM storage_cells WHERE username = %s;", (login,))
        else:
           cur.execute("SELECT id FROM storage_cells WHERE username = ?;", (login,)) 
        
        bookings = cur.fetchall()
        
        if bookings:
            for booking in bookings:
                if current_app.config['DB_TYPE'] == 'postgres':
                    cur.execute("UPDATE storage_cells SET is_occupied = FALSE, username = NULL WHERE id = %s;", (booking['id'],))
                else:
                    cur.execute("UPDATE storage_cells SET is_occupied = FALSE, username = NULL WHERE id = ?;", (booking['id'],))


        # Удаление пользователя
        if current_app.config['DB_TYPE'] == 'postgres':
            cur.execute("DELETE FROM users WHERE login = %s;", (login,))
        else:
            cur.execute("DELETE FROM users WHERE login = ?;", (login,))
        
        conn.commit()

        # Очистка сессии
        session.pop('login', None)  # Удаляем логин из сессии
        return jsonify({"message": "Пользователь успешно удален и все ваши бронирования освобождены."}), 200

    except Exception as e:
        return jsonify({"error": "An error occurred"}), 500
    finally:
        db_close(conn, cur)


@rgz2.route('/rgz2/storage', methods=['GET'])
def storage():
    conn, cur = db_connect()  # Получаем соединение и курсор
    try:
        # Получаем все ячейки из базы данных, сортируя по id
        cur.execute("SELECT * FROM storage_cells ORDER BY id;")
        cells = cur.fetchall()

        # Подсчитываем количество свободных и занятых ячеек
        occupied_cells = [cell for cell in cells if cell[1]]  # Используем индекс 1 для is_occupied
        free_cells = [cell for cell in cells if not cell[1]]  # Используем индекс 1 для is_occupied
        
        total_occupied = len(occupied_cells)
        total_free = len(free_cells)

        # Получаем текущего пользователя
        user = session.get('login')

        # Передаем данные в шаблон
        return render_template('rgz2/storage.html', 
                               user=user,
                               cells=cells, 
                               total_occupied=total_occupied, 
                               total_free=total_free)
    finally:
        db_close(conn, cur)

@rgz2.route('/rgz2/booking', methods=['POST'])
def booking():
    login = session.get('login')
    if not login:
        return "Вы не можете забронировать ячейку, пожалуйста, авторизуйтесь", 403

    cell_id = request.form.get('cell_id')  # Получаем id ячейки из формы

    conn, cur = db_connect()
    try:
        # Проверяем, существует ли ячейка
        if current_app.config['DB_TYPE'] == 'postgres':
            cur.execute("SELECT * FROM storage_cells WHERE id = %s;", (cell_id,))
        else:
            cur.execute("SELECT * FROM storage_cells WHERE id = ?;", (cell_id,))

        cell = cur.fetchone()

        if cell is None:
            return "Cell not found", 404

        # Проверяем, занята ли ячейка
        if cell['is_occupied']:
            return "Cell is already booked", 400

        # Проверяем, сколько ячеек уже забронировано пользователем
        if current_app.config['DB_TYPE'] == 'postgres':
            cur.execute("SELECT COUNT(*) FROM storage_cells WHERE username = %s AND is_occupied = TRUE;", (login,))
        else:
            cur.execute("SELECT COUNT(*) FROM storage_cells WHERE username = ? AND is_occupied = TRUE;", (login,))
        
        booked_count = cur.fetchone()['count']

        if booked_count >= 5:
            return "Вы не можете забронировать более 5 ячеек.", 400

        # Бронирование ячейки
        if current_app.config['DB_TYPE'] == 'postgres':
            cur.execute("UPDATE storage_cells SET is_occupied = TRUE, username = %s WHERE id = %s;", (login, cell_id))
        else:
            cur.execute("UPDATE storage_cells SET is_occupied = TRUE, username = ? WHERE id = ?;", (login, cell_id))
        
        conn.commit()
        return "Ячейка забронирована!", 200

    except Exception as e:
        print(f"An error occurred: {e}")
        return "An error occurred", 500
    finally:
        db_close(conn, cur)


@rgz2.route('/rgz2/cancellation', methods=['POST'])
def cancellation():
    login = session.get('login')
    if not login:
        return "Unauthorized", 403

    cell_id = request.form.get('cell_id')  # Получаем id ячейки из формы

    conn, cur = db_connect()
    try:
        # Проверяем, существует ли ячейка
        if current_app.config['DB_TYPE'] == 'postgres':
            cur.execute("SELECT * FROM storage_cells WHERE id = %s;", (cell_id,))
        else:
            cur.execute("SELECT * FROM storage_cells WHERE id = ?;", (cell_id,))
        cell = cur.fetchone()

        if cell is None:
            return "Cell not found", 404

        # Проверяем, занята ли ячейка
        if not cell['is_occupied']:
            return "Cell is not booked", 400

        # Проверяем, является ли текущий пользователь владельцем брони
        if cell['username'] != login:
            return "Вы не можете снять чужую бронь", 403

        # Отмена бронирования
        if current_app.config['DB_TYPE'] == 'postgres':
            cur.execute("UPDATE storage_cells SET is_occupied = FALSE, username = NULL WHERE id = %s;", (cell_id,))
        else:
            cur.execute("UPDATE storage_cells SET is_occupied = FALSE, username = NULL WHERE id = ?;", (cell_id,))
        conn.commit()
        return "Бронь снята!", 200

    except Exception as e:
        print(f"An error occurred: {e}")
        return "An error occurred", 500
    finally:
        db_close(conn, cur)

@rgz2.route('/rgz2/cells', methods=['GET'])
def view_cells():
    conn, cur = db_connect()
    try:
        cur.execute("SELECT * FROM storage_cells;")
        cells = cur.fetchall()
        return render_template('cells.html', cells=cells)
    finally:
        db_close(conn, cur)

@rgz2.route('/rgz2/cell/<int:cell_id>/details', methods=['GET'])
def get_cell_details(cell_id):
    conn, cur = db_connect()
    try:
        if current_app.config['DB_TYPE'] == 'postgres':
            cur.execute("SELECT * FROM storage_cells WHERE id = %s;", (cell_id,))
        else:
            cur.execute("SELECT * FROM storage_cells WHERE id = ?;", (cell_id,))
        cell = cur.fetchone()

        if cell is None:
            return jsonify({"error": "Cell not found"}), 404

        # Возвращаем информацию о ячейке, включая имя пользователя, если ячейка занята
        return jsonify({
            "id": cell['id'],
            "is_occupied": cell['is_occupied'],
            "username": cell['username'] if cell['is_occupied'] else None
        })

    except Exception as e:
        print(f"An error occurred: {e}")
        return jsonify({"error": "An error occurred"}), 500
    finally:
        db_close(conn, cur)