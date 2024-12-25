from flask import Flask, redirect, url_for
import os
from os import path
from db import db  # Импортируйте db из db/__init__.py
from db.models import users, article
from lab1 import lab1
from lab2 import lab2
from lab3 import lab3
from lab4 import lab4
from lab5 import lab5
from lab6 import lab6
from lab7 import lab7
from lab8 import lab8
from rgz2 import rgz2

app = Flask(__name__)
app.register_blueprint(lab1)
app.register_blueprint(lab2)
app.register_blueprint(lab3)
app.register_blueprint(lab4)
app.register_blueprint(lab5)
app.register_blueprint(lab6)
app.register_blueprint(lab7)
app.register_blueprint(lab8)
app.register_blueprint(rgz2)

app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'сила в любви')
app.config['DB_TYPE'] = os.getenv('DB_TYPE', 'postgres')

if app.config['DB_TYPE'] == 'postgresql':
    db_name = 'darya_dybalina_orm'
    db_user = 'darya_dybalina_orm'
    db_password = '123'
    host_ip = '127.0.0.1'
    host_port = 5432

    app.config['SQLALCHEMY_DATABASE_URI'] = \
        f'postgresql://{db_user}:{db_password}@{host_ip}:{host_port}/{db_name}'
else:
    dir_path = path.dirname(path.realpath(__file__))
    db_path = path.join(dir_path, 'darya_dybalina_orm.db')
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_path}'

db.init_app(app)  # Инициализация db с приложением

with app.app_context():
    db.create_all()

@app.route("/")
@app.route("/index")
def start():
    return redirect("/menu", code=302)

@app.route("/menu")
def menu():
    return '''
<!doctype html>
<html>
    <head>
        <title>НГТУ, ФБ, Лабораторные работы</title>
    </head>
    <body>
        <link rel='stylesheet' href = "''' + url_for('static', filename='lab1/important.css') + '''">
        <header>
            НГТУ, ФБ, WEB-программирование, часть 2. Список лабораторных
        </header>

        <h1>Меню</h1>
        <ol>
            <li><a href="/lab1">Первая лабораторная</a></li>
            <li><a href="/lab2">Вторая лабораторная</a></li>
            <li><a href="/lab3">Третья лабораторная</a></li>
            <li><a href="/lab4">Четвертая лабораторная</a></li>
            <li><a href="/lab5">Пятая лабораторная</a></li>
            <li><a href="/lab6">Шестая лабораторная</a></li>
            <li><a href="/lab7">Седьмая лабораторная</a></li>
            <li><a href="/lab8">Восьмая лабораторная</a></li>
            <li><a href="/rgz2">StorageHub.Камера Хранения</a></li>
        </ol>

        <footer>
            &copy; Дарья Александровна Дыбалина, ФБИ-23, 3 курс, 2024
        </footer </body>
</html>
'''