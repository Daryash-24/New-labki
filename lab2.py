from flask import Blueprint, url_for, redirect, render_template, render_template_string, abort, request
lab2 = Blueprint('lab2', __name__)

@lab2.route('/lab2/')
def labs2():
    return render_template('lab2/lab2.html')

@lab2.route('/lab2/a')
def a():
    return 'без слэша'


@lab2.route('/lab2/a/')
def a2():
    return 'со слэшем'

flower_list = [
    {"name": "Гортензия", "price": 950},
    {"name": "Пион", "price": 500},
    {"name": "Хризантема", "price": 350},
    {"name": "Подсолнух", "price": 450}
]


@lab2.route('/lab2/all_flowers/')
def all_flowers():
    return render_template('lab2/all_flowers.html', flowers=flower_list)


@lab2.route('/lab2/add_flower', methods=['POST'])
def add_flower():
    name = request.form['flower_name']
    price = request.form['flower_price']
    flower_list.append({"name": name, "price": price}) 
    return redirect(url_for('lab2.all_flowers')) 


@lab2.route('/lab2/delete_flower/<int:flower_index>')
def delete_flower(flower_index):
    if 0 <= flower_index < len(flower_list):
        del flower_list[flower_index]
        return redirect(url_for('lab2.all_flowers'))
    else:
        abort(404)


@lab2.route('/lab2/clear_flowers/')
def clear_flowers():
    global flower_list
    flower_list = []
    return redirect(url_for('lab2.all_flowers'))


@lab2.route('/lab2/example')
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
    return render_template('lab2/example.html', 
                           name = name, number = number, group = group, 
                           cours = cours, fruits = fruits)


@lab2.route('/lab2/')
def labs():
    return render_template('lab2.html')


@lab2.route('/lab2/filters')
def filters():
    phrase = "О <b>сколько</b> нам <u>открытий</u> <i>чудных...</i>"
    return render_template('lab2/filter.html', phrase = phrase)


@lab2.route('/lab2/calc/')
def calc_default():
    return redirect(url_for('lab2.calc', a=1, b=1))


@lab2.route('/lab2/calc/<int:a>')
def calc_one_number(a):
    return redirect(url_for('lab2.calc', a=a, b=1))


@lab2.route('/lab2/calc/<int:a>/<int:b>')
def calc(a, b):
    return render_template('lab2/calc.html', a=a, b=b)

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


@lab2.route('/lab2/books')
def books_list():
    return render_template('lab2/books_list.html', books=books)

films = [
    {
        "name": "Интерстеллар",
        "image": "/static/lab2/inter.jpg",
        "description": "Фильм Интерстеллар (Interstellar) — это научно-фантастическая драма,"
        "которая оставляет зрителя задумчивым и проникает в самые глубины его сознания. "
        "Режиссер Кристофер Нолан создал шедевр, который заслуживает внимания и обязательно стоит посмотреть. "
    },
    {
        "name": "Начало",
        "image": "/static/lab2/incep.jpg",
        "description": "Несмотря на достаточно сложносочиненный сюжет, затрагивающий темы человеческого бессознательного "
        "и манипуляций над ним, «Начало» остается ярким примером тождественности гениальности и простоты, которая в свое "
        "время была воспета классиками философской науки в лице Евклида, Да Винчи. В «Начале» много визуальной и диалоговой "
        "экспозиции — именно она активно помогает зрителям разобраться в сложной природе сновидений, а также механике влияния на подсознание."
    },
    {
        "name": "Время",
        "image": "/static/lab2/time.jpg",
        "description": "Неординарный сюжет  заставляет задуматься о многих ценностях. Как мы зачастую тратим  время на пустые разговоры "
        "с людьми,которые нам совсем неинтересны. На жизнь в социальных сетях, залипая в экраны телефонов, не замечаем, как пролетают секунды, "
        "минуты, часы. Тратим бесценное время своей жизни на решение чужих вопросов, отодвигая свои дела на потом, не можем сказать людям: «Нет»."
    },
    {
        "name": "Хроники Нарнии: Принц Каспиан",
        "image": "/static/lab2/narnia.jpg",
        "description": "Хроники Нарнии» оставили след в моей памяти, как цикл фильмов о, продуманном до нЕльзя, вымышленном мире: "
        "со своими героями, порядками и укладом жизни. Сродни миру «Гарри Поттера» или, скажем, «Властелина колец». "
    },
    {
        "name": "Кто я?",
        "image": "/static/lab2/who.jpg",
        "description": "Кто я? — это фильм, который вдохновляет нас на то, чтобы стать лучше, чтобы быть честными с "
        "самими собой, чтобы не бояться идти против течения."
    }
]


@lab2.route('/lab2/films')
def film_list():
    return render_template("lab2/film_list.html", films=films)