from flask import Blueprint, url_for, redirect, render_template, request, session
import psycopg2
from psycopg2.extras import RealDictCursor
from werkzeug.security import check_password_hash, generate_password_hash

lab5 = Blueprint('lab5', __name__)

@lab5.route('/lab5/')
def lab():
    return render_template('/lab5/lab5.html', user = session.get('login'))

def db_connect():
    conn = psycopg2.connect(dbname="webka", user="postgres", password="postgres", host="127.0.0.1", options="-c client_encoding=UTF8")
    cur = conn.cursor(cursor_factory = RealDictCursor)

    return conn, cur

def db_close(conn, cur):
    conn.commit()
    cur.close()
    conn.close()

@lab5.route('/lab5/register', methods = ['POST', 'GET'])
def register():
    if request.method == 'GET':
        return render_template('lab5/register.html')

    login = request.form.get('login')
    password = request.form.get('password')

    if not (login and password):
        return render_template('lab5/register.html', error='Заполните все поля')

    conn, cur = db_connect()

  # Используйте параметризованный запрос для проверки наличия пользователя
    cur.execute("SELECT login FROM users WHERE login=%s", (login,))
    if cur.fetchone():
        db_close(conn, cur)
        return render_template('lab5/register.html', error = 'Такой пользователь уже существует')

  # Используйте параметризованный запрос для вставки данных

    password_hash = generate_password_hash(password)
    cur.execute("INSERT INTO users (login, password) VALUES (%s, %s)", (login, password_hash))

    db_close(conn, cur)
    return render_template('lab5/success.html', login = login)


@lab5.route('/lab5/success')
def success():
    return render_template('/lab5/success.html')


@lab5.route('/lab5/login', methods = ['POST', 'GET'])
def login():
    if request.method == 'GET':
        return render_template ('lab5/login.html')
    
    login = request.form.get('login')
    password = request.form.get('password')

    if not (login or password):
        return render_template ('lab5/login.html', error = 'Заполните поля')
    
    conn, cur = db_connect()
    cur = conn.cursor(cursor_factory = RealDictCursor)

    cur.execute(f"SELECT * FROM users WHERE login ='{login}';")
    user = cur.fetchone()

    if not user:
        db_close(conn, cur)
        return render_template ('lab5/login.html', error = 'Логин и/или пароль неверны')
    
    if not check_password_hash(user['password'], password):
        db_close(conn, cur)
        return render_template ('lab5/login.html', error = 'Логин и/или пароль неверны')

    session['login'] = login
    db_close(conn, cur)
    return render_template ('lab5/success_login.html', login = login)


@lab5.route('/lab5/create', methods = ['GET', 'POST'])
def create():
    login = session.get('login')
    if not login:
        return redirect('/lab5/login')
    
    if request.method == 'GET':
        return render_template('lab5/create_article.html')
    
    title = request.form.get('title')
    article_text = request.form.get('article_text')

    conn, cur = db_connect()

    cur.execute('SELECT * FROM users WHERE login=%s;',(login, ))
    user_id = cur.fetchone()['id']

    cur.execute("INSERT INTO articles (user_id, title, article_text) VALUES (%s, %s, %s)", (user_id, title, article_text))
    
    db_close(conn, cur)
    return redirect ('/lab5')

@lab5.route('/lab5/list')
def list():
  login = session.get('login')
  if not login:
    return redirect('/lab5/login')
  
  conn, cur = db_connect()

  # Используем стандартную строку и %s для параметризованного запроса
  cur.execute('SELECT id FROM users WHERE login=%s;', (login,))
  user_id = cur.fetchone()['id']

  cur.execute("SELECT * FROM articles WHERE user_id = %s;", (user_id,))
  articles = cur.fetchall()

  db_close(conn, cur)
  return render_template ('/lab5/articles.html', articles = articles)