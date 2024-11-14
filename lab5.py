from flask import Blueprint, url_for, redirect, render_template, request, session
import psycopg2

lab5 = Blueprint('lab5', __name__)

@lab5.route('/lab5/')
def lab():
    return render_template('/lab5/lab5.html')

@lab5.route('/lab5/register', methods = ['POST', 'GET'])
def register():
    if request.method == 'GET':
        return render_template('lab5/register.html')

    login = request.form.get('login')
    password = request.form.get('password')

    if not (login and password):
        return render_template('lab5/register.html', error='Заполните все поля')

    conn = None
    cur = None

    try:
        conn = psycopg2.connect(dbname="webka", user="postgres", password="postgres", host="127.0.0.1", options="-c client_encoding=UTF8")
        cur = conn.cursor()

        # Используйте параметризацию запросов для предотвращения SQL-инъекций
        cur.execute("SELECT login FROM users WHERE login=%s;", (login,))
        if cur.fetchone():
            return render_template('lab5/register.html', error='Такой пользователь уже существует')

        # Хешируйте пароль перед сохранением
        cur.execute("INSERT INTO users (login, password) VALUES (%s, %s);", (login))
        conn.commit()

    except Exception as e:
        # Логирование ошибки
        print(f"Error: {e}")
        return render_template('lab5/register.html', error='Произошла ошибка при регистрации. Попробуйте позже.')

    finally:
        # Закрываем соединение с базой данных, если оно было открыто
        if cur:
            cur.close()
        if conn:
            conn.close()

    return render_template('lab5/success.html', login=login)

@lab5.route('/lab5/success')
def success():
    return render_template('/lab5/success.html')
