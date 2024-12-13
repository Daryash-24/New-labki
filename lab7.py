from flask import Blueprint, redirect, url_for, render_template, render_template_string, abort, request, make_response, jsonify,  current_app
import psycopg2
from psycopg2.extras import RealDictCursor
import sqlite3
from os import path

lab7 = Blueprint('lab7', __name__, static_folder='static')

def db_connect():
    if current_app.config['DB_TYPE'] == 'postgres':
        conn = psycopg2.connect(
            dbname="webka", 
            user="postgres", 
            password="postgres", 
            host="127.0.0.1"
        )
        cur = conn.cursor(cursor_factory=RealDictCursor)  # Используем RealDictCursor для PostgreSQL
    else:
        dir_path = path.dirname(path.realpath(__file__))
        db_path = path.join(dir_path, "database.db")
        conn = sqlite3.connect(db_path)
        conn.row_factory = sqlite3.Row  # Устанавливаем row_factory для SQLite
        cur = conn.cursor()  # Создаем курсор для SQLite

    return conn, cur

def db_close(conn, cur):
    conn.commit()
    cur.close()
    conn.close()


@lab7.route('/lab7/')
def main():
    return render_template('lab7/index.html')


@lab7.route('/lab7/rest-api/films', methods=['GET'])
def get_films():
    conn, cur = db_connect()
    cur.execute("SELECT * FROM films;")
    films = cur.fetchall()
    db_close(conn, cur)
    return jsonify(films)


@lab7.route('/lab7/rest-api/films/<int:id>', methods=['GET'])
def get_film(id):
    conn, cur = db_connect()
    cur.execute("SELECT * FROM films WHERE id = %s;", (id,))
    film = cur.fetchone()
    db_close(conn, cur)

    if film is None:
        abort(404)
    return jsonify(film)


@lab7.route('/lab7/rest-api/films/<int:id>', methods=['DELETE'])
def del_film(id):
    conn, cur = db_connect()
    cur.execute("DELETE FROM films WHERE id = %s;", (id,))
    db_close(conn, cur)
    return '', 204

@lab7.route('/lab7/rest-api/films', methods=['POST'])
def add_film():
    film = request.get_json()
    
    if not isinstance(film, dict):
        return {'error': 'Неверный формат данных.'}, 400

    # Проверка на оригинальное название
    if not film.get('title') and not film['title_ru']:
        return {'error': 'Название на оригинальном языке должно быть заполнено, если русское название пустое.'}, 400
    
    if not film.get('title_ru'):
        return {'error': 'Русское название не должно быть пустое.'}, 400

    if not (1895 <= film['year'] <= 2024):
        return {'error': 'Год должен быть от 1895 до 2024.'}, 400
    
    if len(film['description']) > 2000:
        return {'error': 'Описание не должно превышать 2000 символов.'}, 400
    
    if not (film['description']):
        return {'error': 'Описание не должно быть пустым.'}, 400
    
    conn, cur = db_connect()
    try:
        cur.execute("""
            INSERT INTO films (title, title_ru, year, description) 
            VALUES (%s, %s, %s, %s) RETURNING id;
        """, (film['title'], film['title_ru'], film['year'], film['description']))
        film_id = cur.fetchone()['id']
        return jsonify({'id': film_id}), 201
    except Exception as e:
        return {'error': str(e)}, 500
    finally:
        db_close(conn, cur)

@lab7.route('/lab7/rest-api/films/<int:id>', methods=['PUT'])
def put_film(id):
    film = request.get_json()
    if film is None:
        return {'error': 'Неверный формат данных.'}, 400
    
    if not film.get('title_ru'):
        return {'error': 'Русское название должно быть непустым.'}, 400
    
    if not film.get('title') and not film['title_ru']:
        return {'error': 'Название на оригинальном языке должно быть непустым, если русское название пустое.'}, 400
    
    
    if not (1895 <= film.get('year', 0) <= 2024):
        return {'error': f'Год должен быть от 1895 до 2024.'}, 400
    
    if not film.get('description') or len(film['description']) > 2000:
        return {'error': 'Описание должно быть непустым и не более 2000 символов.'}, 400
    
    conn, cur = db_connect()
    cur.execute("""
        UPDATE films 
        SET title = %s, title_ru = %s, year = %s, description = %s 
        WHERE id = %s;
    """, (film['title'], film['title_ru'], film['year'], film['description'], id))
    db_close(conn, cur)
    return jsonify(film)

