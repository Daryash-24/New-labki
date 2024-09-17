from flask import Flask, redirect, url_for
app = Flask(__name__)

@app.route("/")
@app.route("/index")

def start():
    return redirect ("/menu", code=302)

@app.route("/menu")
def menu():
    return """
<!doctype html>
<html>
    <head>
        <title>НГТУ, ФБ, Лабораторные работы</title>
    </head>
    <body>
        <header>
            НГТУ, ФБ, WEB-программирование, часть 2. Список лабораторных
        </header>

        <h1>Меню</h1>
        <ol>
            <li><a href="/lab1">Первая лабораторная</a></li>
        </ol>

        <footer>
            &copy; Дарья Александровна Дыбалина, ФБИ-23, 3 курс, 2024
        </footer>
    </body>
</html>
"""

@app.route("/lab1")
def lab1():
    return """
<!doctype html>
<html>
    <head>
        <title>НГТУ, ФБ, Лабораторные работы</title>
    </head>
    <body>

        <header>
            НГТУ, ФБ, WEB-программирование, часть 2. Список лабораторных
        </header>

        <h1>web-сервер на flask</h1>
        <p>Flask — фреймворк для создания веб-приложений на языке
        программирования Python, использующий набор инструментов
        Werkzeug, а также шаблонизатор Jinja2. Относится к категории так
        называемых микрофреймворков — минималистичных каркасов
        веб-приложений, сознательно предоставляющих лишь самые базовые возможности.
        <p><a href="/menu">Меню</a>

        <h2>Реализованные роуты</h2>
        <ol>
            <li><a href="/lab1/oak">Дуб</a></li>
            <li><a href="/lab1/student">Студент</a></li>
            <li><a href="/lab1/python">Python</a></li>
        </ol>
        
        <footer>
            &copy; Дарья Александровна Дыбалина, ФБИ-23, 3 курс, 2024
        </footer>

        <link rel='stylesheet' href = "''' + url_for('static', filename='important.css') + '''">
    </body>
</html>
"""

@app.route("/lab1/student")
def student():
    return '''
<!doctype html>
<html>
    <body>
        <h1>Дыбалина Дарья Александровна</h1>
        <div class="student">
            <img src="''' + url_for('static', filename='nstu.png') + '''">
        </div>
        <link rel='stylesheet' href = "''' + url_for('static', filename='important.css') + '''">
    </body>
</html>
'''
@app.route("/lab1/python")
def python():
    return '''
<!doctype html>
<html>
    <body>
        <h1>Язык программирования Python</h1>

        <h2>Насколько Python популярен</h2>

        <p>По данным GitHub за 2023 год, Python входит в топ-3 самых популярных языков,
        уступая лишь JavaScript. В чём секрет такой популярности в использовании языка? 
        Python подходит для решения широкого круга задач и применяется на всех популярных платформах. 
        Росту популярности Python способствовала и его эффективность в стремительно развивающихся сферах 
        Machine Learning и Data Science.

        <p>Специалисты выделяют массу преимуществ Python — остановимся на ключевых из них.
        Простота синтаксиса, а значит — низкий порог вхождения. Код языка чистый и понятный, 
        без лишних символов и выражений.

        <h2>Преимущества: чем хорош Python</h2>

        <p><b>Расширяемость и гибкость.</b> 
        Не зря один из слоганов языка — это «Just Import!» 
        Python можно легко расширить для взаимодействия с другими программными системами или встроить 
        в программы в качестве компонента. Он очень и очень гибкий. Это даёт больше возможностей 
        для использования языка в разных сферах.

        <p><b>Интерпретируемость и кроссплатформенность.</b> 
        Интерпретатор Python есть для всех популярных платформ и по умолчанию входит в большинство 
        дистрибутивов Linux.

        <p><b>Стандартизированность.</b> 
        У Python есть единый стандарт для написания кода — 
        Python Enhancement Proposal или PEP, благодаря чему язык остаётся читабельным даже при переходе 
        от одного программиста к другому.

        <p><b>Open Source.</b> 
        У интерпретатора Python открытый код, то есть любой, кто заинтересован 
        в развитии языка, может поучаствовать в его разработке и улучшении.

        <p><b>Сильное комьюнити и конференции.</b> 
        Вокруг Python образовалось дружественное комьюнити, 
        которое готово прийти на помощь новичку или уже опытному разработчику и разобраться в его проблеме. 
        Во всём мире проходит много мероприятий, где можно познакомиться с коллегами и узнать много нового 
        о применении Пайтона.

        <p><b>Широта применения.</b> 
        Наиболее широко Python используется в web-разработке, работе с данными, 
        автоматизации бизнес-процессов и геймдеве.

        <p><b>Востребованность на рынке труда и поддержка гигантами IT-сферы.</b> 
        Python-разработчики востребованы во многих проектах и им несложно найти работу. 
        Разработку на Python ведут в Google, Facebook, Dropbox, Spotify, Quora, Netflix, 
        Microsoft Intel, а в России — «Яндекс», «ВКонтакте» и «Сбербанк». Это серьёзно влияет на статус языка.

        <div class="python">
            <img src="''' + url_for('static', filename='python.jpg') + '''", width="500px">
        </div>
        <link rel='stylesheet' href = "''' + url_for('static', filename='important.css') + '''">
    </body>
</html>
'''

@app.route("/lab1/oak")
def oak():
    return '''
<!doctype html>
<html>
    <body>
        <h1>Дуб</h1>
        <img src="''' + url_for('static', filename='oak.jpg') + '''">
        <link rel='stylesheet' href = "''' + url_for('static', filename='lab1.css') + '''">
    </body>
</html>
'''