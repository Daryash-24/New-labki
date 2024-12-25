from flask import Blueprint, redirect, url_for, render_template, render_template_string, abort, request, session, make_response, jsonify,  current_app
import psycopg2
from psycopg2.extras import RealDictCursor
import sqlite3
from os import path
from db import db  
from db.models import users, article
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, current_user, logout_user
from flask_login import LoginManager

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
    
    # Автоматический логин после регистрации
    login_user(new_user)  # Вход пользователя

    return redirect('/lab8/')

@lab8.route('/lab8/login/', methods=['GET', 'POST'])
def login():
   if request.method == 'GET':
       return render_template('lab8/login.html')
   
   login_form = request.form.get('login')
   password_form = request.form.get('password')

   # Логика аутентификации (замените на вашу)
   user = users.query.filter_by(login=login_form).first()
   if user and check_password_hash(user.password, password_form):
        session['_user_id'] = str(user.id).encode('utf-8').decode('utf-8') # Преобразование к строке и кодирование/декодирование в UTF-8
        remember_me = request.form.get('remember-me') # Получение значения чекбокса
        login_user(user, remember=remember_me)
        return redirect(url_for('lab8.main'))
   else:
      return render_template('lab8/login.html', error='Неверный логин или пароль')

@lab8.route('/lab8/articles/')
@login_required
def article_list():
    return "Список статей"

@lab8.route('/lab8/logout')
@login_required
def logout():
    logout_user()
    return redirect('/lab8/')