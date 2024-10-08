from flask import Flask, redirect, url_for, render_template, render_template_string, abort, request
app = Flask(__name__)

@app.route("/")
def start():
    return redirect ("/menu", code=302)

@app.route("/menu")
def menu(): 
    return '''
<!doctype html>
<html>
    <head>
        <title>НГТУ, ФБ, Лабораторные работы</title>
    </head>
    <body>
        <link rel='stylesheet' href = "''' + url_for('static', filename='important.css') + '''">
        <header>
            НГТУ, ФБ, WEB-программирование, часть 2. Список лабораторных
        </header>

        <h1>Меню</h1>
        <ol>
            <li><a href="/lab1">Первая лабораторная</a></li>
            <li><a href = "/lab2">Вторая лабораторная работа</li>
        </ol>

        <footer>
            &copy; Дарья Александровна Дыбалина, ФБИ-23, 3 курс, 2024
        </footer>
    </body>
</html>
'''

@app.route("/lab1")
def lab1():
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

@app.route("/lab1/student")
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
@app.route("/lab1/python")
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

@app.route("/lab1/oak")
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

@app.route("/lab1/cats")
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

@app.route('/lab2/a')
def a():
    return 'без слэша'

@app.route('/lab2/a/')
def a2():
    return 'со слэшем'

flower_list = [
    {"name": "Гортензия", "price": 950},
    {"name": "Пион", "price": 500},
    {"name": "Хризантема", "price": 350},
    {"name": "Подсолнух", "price": 450}
]


@app.route('/lab2/all_flowers/')
def all_flowers():
    return render_template('all_flowers.html', flowers=flower_list)

@app.route('/lab2/add_flower/<string:flower_name>/<int:flower_price>')
def add_flower(flower_name, flower_price):
    flower_list.append({'name': flower_name, 'price': flower_price})
    return redirect(url_for('all_flowers'))

@app.route('/lab2/delete_flower/<int:flower_index>')
def delete_flower(flower_index):
    if 0 <= flower_index < len(flower_list):
        del flower_list[flower_index]
        return redirect(url_for('all_flowers'))
    else:
        abort(404)

@app.route('/lab2/clear_flowers/')
def clear_flowers():
    global flower_list
    flower_list = []
    return redirect(url_for('all_flowers'))


    

@app.route('/lab2/example')
def example():
    name = 'Дарья Дыбалинa'
    number = '2'
    group = 'ФБИ-23'
    cours = '3'
    fruits = [
        {'name': 'манго', 'price': '249'},
        {'name': 'апельсины', 'price': '150'},
        {'name': 'бананы', 'price': '179'},
        {'name': 'персики', 'price': '220'},
        {'name': 'дыня', 'price': '200'}
    ]
    return render_template('example.html', 
                           name = name, number = number, group = group, 
                           cours = cours, fruits = fruits)

@app.route('/lab2/')
def lab2():
    return render_template('lab2.html')

@app.route('/lab2/filters')
def filters():
    phrase = "О <b>сколько</b> нам <u>открытий</u> <i>чудных...</i>"
    return render_template('filter.html', phrase = phrase)

@app.route('/lab2/calc/')
def calc_default():
    return redirect(url_for('calc', a=1, b=1))

@app.route('/lab2/calc/<int:a>')
def calc_one_number(a):
    return redirect(url_for('calc', a=a, b=1))

@app.route('/lab2/calc/<int:a>/<int:b>')
def calc(a, b):
    return render_template('calc.html', a=a, b=b)

books = [
    {'author': 'Джон Р. Р. Толкин', 'title': 'Властилин колец(сборник)', 'genre': 'Фэнтези', 'pages': 1120},
    {'author': 'Маргарет Митчел', 'title': 'Кнесенные ветром', 'genre': 'Исторический роман', 'pages': 992},
    {'author': 'Стивен Кинг', 'title': '11/22/63', 'genre': 'Фантастика', 'pages': 800},
    {'author': 'Джоан Роулинг', 'title': 'Гарри Поттер и узник Азкабана', 'genre': 'Фэнтези', 'pages': 492},
    {'author': 'Стивен Кинг', 'title': 'Зеленая миля', 'genre': 'Мистика', 'pages': 384},
    {'author': 'Джордж Мартин', 'title': 'Буря мечей', 'genre': 'Фэнтези', 'pages': 1168},
    {'author': 'Агата Кристи', 'title': 'Десять негретят', 'genre': 'Детектив', 'pages': 288},
    {'author': 'Сара Дж. Маас', 'title': 'Королева Теней', 'genre': 'Фэнтези', 'pages': 736},
    {'author': 'Сара Дж. Маас', 'title': 'Королевство Гнева и Тумана', 'genre': 'Фэнтези', 'pages': 704},
    {'author': 'Оскар Уайльд', 'title': 'Портрет Дориана Грея', 'genre': 'Роман', 'pages': 320},
]

@app.route('/lab2/books')
def books_list():
    return render_template('books_list.html', books=books)

films = [
    {
        "name": "Интерстеллар",
        "image": "/static/inter.jpg",
        "description": "Фильм Интерстеллар (Interstellar) — это научно-фантастическая драма,"
        "которая оставляет зрителя задумчивым и проникает в самые глубины его сознания. "
        "Режиссер Кристофер Нолан создал шедевр, который заслуживает внимания и обязательно стоит посмотреть. "
    },
    {
        "name": "Начало",
        "image": "/static/incep.jpg",
        "description": "Несмотря на достаточно сложносочиненный сюжет, затрагивающий темы человеческого бессознательного "
        "и манипуляций над ним, «Начало» остается ярким примером тождественности гениальности и простоты, которая в свое "
        "время была воспета классиками философской науки в лице Евклида, Да Винчи. В «Начале» много визуальной и диалоговой "
        "экспозиции — именно она активно помогает зрителям разобраться в сложной природе сновидений, а также механике влияния на подсознание."
    },
    {
        "name": "Время",
        "image": "/static/time.jpg",
        "description": "Неординарный сюжет  заставляет задуматься о многих ценностях. Как мы зачастую тратим  время на пустые разговоры "
        "с людьми,которые нам совсем неинтересны. На жизнь в социальных сетях, залипая в экраны телефонов, не замечаем, как пролетают секунды, "
        "минуты, часы. Тратим бесценное время своей жизни на решение чужих вопросов, отодвигая свои дела на потом, не можем сказать людям: «Нет»."
    },
    {
        "name": "Хроники Нарнии: Принц Каспиан",
        "image": "/static/narnia.jpg",
        "description": "Хроники Нарнии» оставили след в моей памяти, как цикл фильмов о, продуманном до нЕльзя, вымышленном мире: "
        "со своими героями, порядками и укладом жизни. Сродни миру «Гарри Поттера» или, скажем, «Властелина колец». "
    },
    {
        "name": "Кто я?",
        "image": "/static/who.jpg",
        "description": "Кто я? — это фильм, который вдохновляет нас на то, чтобы стать лучше, чтобы быть честными с "
        "самими собой, чтобы не бояться идти против течения."
    }
]


@app.route('/lab2/films')
def film_list():
    return render_template("film_list.html", films=films)