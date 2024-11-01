from flask import Blueprint, url_for, redirect, render_template, request, session
lab4 = Blueprint('lab4', __name__)


@lab4.route('/lab4/')
def lab():
    return render_template('/lab4/lab4.html')

@lab4.route('/lab4/div-form')
def div_form():
    return render_template('lab4/div-form.html')

@lab4.route('/lab4/sum-form')
def sum_form():
    return render_template ('lab4/sum-form.html')

@lab4.route('/lab4/mult-form')
def mult_form():
    return render_template('lab4/mult-form.html')

@lab4.route('/lab4/sub-form')
def sub_form():
    return render_template('lab4/sub-form.html')

@lab4.route('/lab4/deg-form')
def deg_form():
    return render_template('/lab4/deg-form.html')

@lab4.route('/lab4/div', methods = ['POST'])
def div():
    x1 = request.form.get('x1')
    x2 = request.form.get('x2')
    if x1 == '' or x2 == '':
        return render_template ('lab4/div.html', error = 'Оба поля должны быть заполнены!')
    
    if x2 == '0':
        return render_template ('lab4/div.html', errors = 'На ноль делить нельзя!')

    x1 = int(x1)
    x2 = int(x2)
    result = x1 / x2
    return render_template('lab4/div.html', x1 = x1, x2 = x2, result = result)

@lab4.route('/lab4/sum', methods = ['POST'])
def sum():
    x1 = request.form.get('x1')
    x2 = request.form.get('x2')

    if x1 == '':
        x1 = 0 
    else:
        x1 = int(x1)

    if x2 == '':
        x2 = 0 
    else:
        x2 = int(x2) 

    result = x1 + x2

    return render_template('lab4/sum.html', x1 = x1, x2 = x2, result = result)

@lab4.route('/lab4/mult', methods = ['POST'])
def mult():
    x1 = request.form.get('x1')
    x2 = request.form.get('x2')

    if x1 == '':
        x1 = 0 
    else:
        x1 = int(x1)

    if x2 == '':
        x2 = 0 
    else:
        x2 = int(x2) 

    result = x1 * x2

    return render_template('lab4/mult.html', x1 = x1, x2 = x2, result = result)

@lab4.route('/lab4/sub', methods = ['POST'])
def sub():
    x1 = request.form.get('x1')
    x2 = request.form.get('x2')
    if x1 == '' or x2 == '':
        return render_template ('lab4/sub.html', error = 'Оба поля должны быть заполнены!')
    
    x1 = int(x1)
    x2 = int(x2)
    result = x1 - x2
    return render_template('lab4/sub.html', x1 = x1, x2 = x2, result = result)

@lab4.route('/lab4/deg', methods = ['POST'])
def deg():
    x1 = request.form.get('x1')
    x2 = request.form.get('x2')
    if x1 == '' or x2 == '':
        return render_template ('lab4/deg.html', error = 'Оба поля должны быть заполнены!')
    
    if x1 == '0' and x2 == '0':
        return render_template ('lab4/deg.html', errors = 'Оба числа не могут быть нулями!')

    x1 = int(x1)
    x2 = int(x2)
    result = x1 ** x2
    return render_template('lab4/deg.html', x1 = x1, x2 = x2, result = result)

tree_count = 0

@lab4.route('/lab4/tree', methods = ['GET', 'POST'])
def tree():
    global tree_count 
    if request.method == 'GET':
        return render_template('lab4/tree.html', tree_count = tree_count)
    
    operation = request.form.get('operation')

    if operation == 'cut':
        if tree_count > 0: 
            tree_count -= 1
    elif operation == 'plant':
        if tree_count < 10:  
            tree_count += 1
    return redirect ('/lab4/tree')

users = [
    {'login': 'darya', 'password': '246', 'name': 'Дарья Дыбалина', 'sex': 'female'},
    {'login': 'dima', 'password': 'grub', 'name': 'Дмитрий Фуфачев', 'sex': 'male'},
    {'login': 'dasha', 'password': '10032002', 'name': 'Дарья Вадрецкая', 'sex': 'female'},
    {'login': 'kate', 'password': '0108', 'name': 'Екатерина Кузьменко', 'sex': 'female'},
    {'login': 'alina_design', 'password': '24122003', 'name': 'Алина Бардина', 'sex': 'female'}
    
]

@lab4.route('/lab4/login', methods = ['GET', 'POST'])
def login():
    if request.method == 'GET':
        if 'login' in session:
            authorized = True
            login = session['login']
            user = next((user for user in users if user['login'] == login), None)
            if user:
                name = user['name']
            else:
                name = ''
        else:
            authorized = False
            login = ''
            name = ''
        return render_template('lab4/login.html', authorized = authorized, login = login, name=name)
    
    login = request.form.get('login')
    password = request.form.get('password')

    error = ''
    if not login:
        error = 'Не введён логин'
    elif not password:
        error = 'Не введён пароль'
    else:
        for user in users:
            if login == user['login'] and password == user['password']:
                session['login'] = login
                return redirect ('/lab4/login')
        error = 'Неверный логин и/или пароль'
    return render_template('/lab4/login.html', error = error, authorized = False, login=login)


@lab4.route('/lab4/logout', methods = ['POST'])
def logout():
    session.pop('login', None)
    return redirect('/lab4/login')
