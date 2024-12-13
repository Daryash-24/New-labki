from flask import Blueprint, redirect, url_for, render_template, render_template_string, abort, request, make_response, jsonify,  current_app
import psycopg2
from psycopg2.extras import RealDictCursor
import sqlite3
from os import path

lab7 = Blueprint('lab7', __name__, static_folder='static')

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
        "year": 2017,
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
    {
        "title": "Harry Potter and the Prisoner of Azkaban",
        "title_ru": "Гарри Поттер и узник Азкабана",
        "year": 2004,
        "description": "Гарри, Рон и Гермиона возвращаются на третий курс школы чародейства и волшебства Хогвартс.\
            На этот раз они должны раскрыть тайну узника, сбежавшего из тюрьмы Азкабан, чье пребывание \
            на воле создает для Гарри смертельную опасность."
    },
    {
        "title": "Upgrade",
        "title_ru": "Апгрейд",
        "year": 2018,
        "description": "2046 год. Разнообразные технологии участвуют во всех аспектах человеческой жизни. \
            Но в этом технологичном мире Грей — один из немногих людей, кто любит работать руками. \
            Он восстанавливает и чинит старые автомобили. Однажды, возвращаясь от клиента, \
            Грей с женой попадают в аварию, а после — в руки банды отморозков, в результате \
            чего женщина погибает, а Грей оказывается парализованным ниже шеи. Тот самый \
            богатый клиент предлагает несчастному поставить экспериментальный имплант Stem, \
            который может полностью восстановить подвижность."
    }
]

@lab7.route('/lab7/rest-api/films', methods=['GET'])
def get_films():
    return jsonify (films)


@lab7.route('/lab7/rest-api/films/<int:id>', methods=['GET'])
def get_film(id):
    if id < 0 or id >= len(films):
        abort(404)
    return films[id]


@lab7.route('/lab7/rest-api/films/<int:id>', methods=['DELETE'])
def del_film(id):
    if id < 0 or id >= len(films):
        abort(404)  
    del films[id]
    return '', 204

@lab7.route('/lab7/rest-api/films', methods=['POST'])
def add_film():
    film = request.get_json()
    if not film.get('description'):
        return {'description': 'Заполните описание'}, 400
    films.append(film)
    return {'id': len(films) - 1}, 201


@lab7.route('/lab7/rest-api/films/<int:id>', methods=['PUT'])
def put_film(id):
    if id < 0 or id >= len(films):
        abort(404)
    film = request.get_json()
    if not film.get('description'):
        return {'description': 'Заполните описание'}, 400
    films[id] = film
    return films[id]


