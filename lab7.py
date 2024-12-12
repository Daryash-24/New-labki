from flask import Blueprint, redirect, url_for, render_template, render_template_string, abort, request, make_response, session,  current_app
from functools import wraps
import psycopg2
from psycopg2.extras import RealDictCursor
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3
from os import path

lab7 = Blueprint('lab7', __name__, static_folder='static')

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

@lab7.route('/lab7/')
def main():
    return render_template('lab7/index.html')

films = [
    {
        'title': "Interstellar",
        'title_ru': "Интерстеллар",
        "year": 2014,
        'description': 'Когда засуха, пыльные бури и вымирание \
            растений приводят человечество к продовольственному кризису,\
            коллектив исследователей и учёных отправляется сквозь червоточину\
            (которая предположительно соединяет области пространства-времени \
            через большое расстояние) в путешествие, чтобы превзойти прежние \
            ограничения для космических путешествий человека и найти планету \
            с подходящими для человечества условиями.'
    },
    {
        'title': "Dark",
        'title_ru': "Тьма",
        "year": 2017-2020,
        'description': 'История четырёх семей, живущих спокойной и размеренной \
            жизнью в маленьком немецком городке. Видимая идиллия рушится, \
            когда бесследно исчезают двое детей и воскресают тёмные тайны прошлого.'
    },
    {
        'title': "Hitman: Agent 47",
        'title_ru': "Хитмэн: Агент 47 ",
        "year": 2015,
        'description': 'История об элитном убийце, созданном при помощи \
            генной инженерии, который объединяется с женщиной, чтобы помочь \
            ей найти отца и раскрыть тайну своего происхождения.'
    },
]

@lab7.route('/lab7/rest-api/films', methods=['GET'])
def get_films():
    return films