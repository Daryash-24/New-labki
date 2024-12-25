from flask import Blueprint, redirect, url_for, render_template, render_template_string, abort, request, session, make_response, jsonify,  current_app
import psycopg2
from psycopg2.extras import RealDictCursor
import sqlite3
from os import path
from db import db  
from db.models import users, article
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, current_user

lab8 = Blueprint('lab8', __name__, static_folder='static')


@lab8.route('/lab8/')
def main():
    return render_template('/lab8/lab8.html', user=current_user.login if current_user.is_authenticated else None)

@lab8.route('/lab8/register/', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('lab8/register.html')
    
    login_form = request.form.get('login')
    password_form = request.form.get('password')

    # Проверка на пустое имя пользователя
    if not login_form:
        return render_template('lab8/register.html', error='Имя пользователя не должно быть пустым')

    # Проверка на пустой пароль
    if not password_form:
        return render_template('lab8/register.html', error='Пароль не должен быть пустым')

    # Проверка на существование пользователя
    login_exists = users.query.filter_by(login=login_form).first()
    if login_exists:
        return render_template('lab8/register.html', error='Такой пользователь уже существует')
    
    # Хеширование пароля и создание нового пользователя
    password_hash = generate_password_hash(password_form)
    new_user = users(login=login_form, password=password_hash)
    db.session.add(new_user)
    db.session.commit()
    
    return redirect('/lab8/')

@lab8.route('/lab8/login', methods = ['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('/lab8/login.html')
    
    login_form = request.form.get('login')
    password_form = request.form.get('password')

    user = users.query.filter_by(login = login_form).first()

    if user:
        if check_password_hash(user.password, password_form):
            login_user(user, remember=False)
            return redirect('/lab8/')
        
    return render_template ('/lab8/login.html',
                            error = 'Ошибка входа: логин и/или пароль неверны ')

@lab8.route('/lab8/articles/')
@login_required
def article_list():
    return "Список статей"