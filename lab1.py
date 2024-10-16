from flask import Blueprint, url_for, redirect
lab1 = Blueprint('lab1', __name__)


@lab1.route("/lab1")
def lab():
    return '''
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
            <li><a href="/lab1/cats">Котики</a></li>
        </ol>
        
        <footer>
            &copy; Дарья Александровна Дыбалина, ФБИ-23, 3 курс, 2024
        </footer>

        <link rel='stylesheet' href = "''' + url_for('static', filename='important.css') + '''">
    </body>
</html>
'''


@lab1.route("/lab1/student")
def student():
    return '''
<!doctype html>
<html>
    <head>
        <title>НГТУ, ФБ, Лабораторная работа 1 - Студент</title>
    </head>
    <body>
        <header>
            НГТУ, ФБ, WEB-программирование, часть 2. Студент
        </header>
        <h1>Дыбалина Дарья Александровна</h1>
        <div class="student">
            <img src="''' + url_for('static', filename='nstu.png') + '''", width='700px'>
        </div>
        <link rel='stylesheet' href = "''' + url_for('static', filename='important.css') + '''">

        <footer>
            &copy; Дарья Александровна Дыбалина, ФБИ-23, 3 курс, 2024
        </footer>
    </body>
</html>
'''


@lab1.route("/lab1/python")
def python():
    return '''
<!doctype html>
<html>
    <head>
        <title>НГТУ, ФБ, Лабораторные работы - Python</title>
    </head>
    <body>
        <header>
            НГТУ, ФБ, WEB-программирование, часть 2.
        </header>

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

        <footer>
            &copy; Дарья Александровна Дыбалина, ФБИ-23, 3 курс, 2024
        </footer>

        <div class="python">
            <img src="''' + url_for('static', filename='python.jpg') + '''", width="500px">
        </div>
        <link rel='stylesheet' href = "''' + url_for('static', filename='important.css') + '''">
    </body>
</html>
'''


@lab1.route("/lab1/oak")
def oak():
    return '''
<!doctype html>
<html>
    <head>
        <title>НГТУ, ФБ, Лабораторные работы - Дуб</title>
    </head>
    <body>
        <header>
            НГТУ, ФБ, WEB-программирование, часть 2.
        </header>
        <h1>Дуб</h1>
        <div class="oak">
            <img src="''' + url_for('static', filename='oak.jpg') + '''">
        </div>
        <link rel='stylesheet' href = "''' + url_for('static', filename='important.css') + '''">
        <footer>
            &copy; Дарья Александровна Дыбалина, ФБИ-23, 3 курс, 2024
        </footer>
    </body>
</html>
'''


@lab1.route("/lab1/cats")
def cats():
    return '''
<!doctype html>
<html>
    <head>
        <title>НГТУ, ФБ, Лабораторные работы - Тыгыдык</title>
    </head>
    <body>
        <header>
            НГТУ, ФБ, WEB-программирование, часть 2.
        </header>
        <h1>Почему кот ночью одержим тыгыдыком.</h1>
        <p>Всем нам, окошаченным людям, известен кошачий ночной праздник под названием "Тыгыдык". 
        Именно ночью что-то находит на милого котика (или всё-таки вселяется?) и он... носится по дому, 
        как ненормальный. Сшибая всё и всех на своем пути.
        <p>А если серьезно. Что вызывает в коте желание сойти ночью с ума и носиться по квартире диким мустангом?

        <h2>Почему у кота или кошки ночью - тыгыдык?</h2>
        <p><b>Причина 1. Котик просто пытается разбудить хозяев.</b>
        <p>Это касается семей, где котик получает еду, как только хозяева просыпаются. Если режим для кошки непонятен, 
        и хозяева все время встают в разное время, киса начинает беспокоиться о своей еде.

        <p>Тогда, уж поверьте, "кошачий демон" устроит свой тыгыдык прямо на Вашем безмятежно спящем теле. Или упадет на Вас. Случайно. Со шкафа. Несколько раз. И еще разок>
        <div class="cat">
            <img src="''' + url_for('static', filename='cat.jpg') + '''", width='500px'>
        </div>

        <p><b>Причина 2. Не устал.</b>
        <p>Вашей кошке просто некуда выплескивать энергию! Возможно, еще и вашего внимания не хватает.
        Наши кисы большую часть дня просто бессовестно спят или лежат в причудливых позах.
        <div class="tired">
            <img src="''' + url_for('static', filename='tired.png') + '''", height='300px'>
        </div>

        <p><b>Причина 3. Гулянка!</b>
        <p>Если кошка или кот "гуляют", находятся "в охоте", у них "весеннее обострение" - 
        ночные тыгыдыки могут участиться и усилиться. Держись дом и его обитатели
        <div class="night">
            <img src="''' + url_for('static', filename='night.jpg') + '''", width='500px'>
        </div>
        <div class="mycat">
            <img src="''' + url_for('static', filename='mycat.jpg') + '''", height='450px'>
        </div>

        <link rel='stylesheet' href = "''' + url_for('static', filename='important.css') + '''">
        <footer>
            &copy; Дарья Александровна Дыбалина, ФБИ-23, 3 курс, 2024
        </footer>
    </body>
</html>
'''

