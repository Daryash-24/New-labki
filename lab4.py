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

users_list = [
    {'login': 'darya', 'password': '246', 'name': 'Дарья Дыбалина', 'sex': 'female'},
    {'login': 'dima', 'password': 'grub', 'name': 'Дмитрий Фуфачев', 'sex': 'male'},
    {'login': 'dasha', 'password': '10032002', 'name': 'Дарья Вадрецкая', 'sex': 'female'},
    {'login': 'kate', 'password': '0108', 'name': 'Екатерина Кузьменко', 'sex': 'female'},
    {'login': 'alina_design', 'password': '24122003', 'name': 'Алина Бардина', 'sex': 'female'}
    
]

@lab4.route('/lab4/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        if 'login' in session:
            authorized = True
            login = session['login']
            user = next((user for user in users_list if user['login'] == login), None)
            if user:
                name = user['name']
            else:
                name = ''
        else:
            authorized = False
            login = ''
            name = ''
        return render_template('lab4/login.html', authorized=authorized, login=login, name=name)
    
    login = request.form.get('login')
    password = request.form.get('password')

    error = ''
    if not login:
        error = 'Не введён логин'
    elif not password:
        error = 'Не введён пароль'
    else:
        for user in users_list:
            if login == user['login'] and password == user['password']:
                session['login'] = login
                return redirect('/lab4/users')  # Перенаправление на страницу пользователей
        error = 'Неверный логин и/или пароль'
    return render_template('lab4/login.html', error=error, authorized=False, login=login)


@lab4.route('/lab4/users', methods=['GET', 'POST'])
def users_list_view():
    if 'login' not in session:
        return redirect('/lab4/login')

    current_user_login = session['login']
    current_user = next((user for user in users_list if user['login'] == current_user_login), None)
    return render_template('lab4/users.html', users=users_list, current_user=current_user)

@lab4.route('/lab4/delete', methods=['POST'])
def delete_user():
    if 'login' not in session:
        return redirect('/lab4/login')

    current_user_login = session['login']
    global users_list
    users_list = [user for user in users_list if user['login'] != current_user_login]
    session.pop('login', None)  # Завершить сессию
    return redirect('/lab4/login')

@lab4.route('/lab4/edit', methods=['GET', 'POST'])
def edit_user():
    if 'login' not in session:
        return redirect('/lab4/login')

    current_user_login = session['login']
    current_user = next((user for user in users_list if user['login'] == current_user_login), None)

    if request.method == 'POST':
        new_name = request.form.get('name')
        new_password = request.form.get('password')

        if new_name:
            current_user['name'] = new_name
        if new_password:
            current_user['password'] = new_password
        
        return redirect('/lab4/users')

    return render_template('lab4/edit_user.html', user=current_user)

@lab4.route('/lab4/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        login = request.form.get('login')
        password = request.form.get('password')
        name = request.form.get('name')

        error = ''
        if not login or not password or not name:
            error = 'Все поля обязательны для заполнения.'
        else:
            if any(user['login'] == login for user in users_list):
                error = 'Пользователь с таким логином уже существует.'
            else:
                users_list.append({'login': login, 'password': password, 'name': name})
                return redirect('/lab4/login')

        return render_template('lab4/register.html', error=error)

    return render_template('lab4/register.html')

@lab4.route('/lab4/logout', methods = ['POST'])
def logout():
    session.pop('login', None)
    return redirect('/lab4/login')

@lab4.route('/lab4/fridge', methods=['GET', 'POST'])
def fridge():
    message = ""
    
    if request.method == 'POST':
        temperature = request.form.get('temperature')
        
        if temperature is None or temperature == '':
            message = "Ошибка: не задана температура"
        else:
            try:
                temperature = float(temperature)
                if temperature < -12:
                    message = "Не удалось установить температуру — слишком низкое значение"
                elif temperature > -1:
                    message = "Не удалось установить температуру — слишком высокое значение"
                elif -12 <= temperature <= -9:
                    message = f"Установлена температура: {temperature}°C ❄️❄️❄️"
                elif -8 <= temperature <= -5:
                    message = f"Установлена температура: {temperature}°C ❄️❄️"
                elif -4 <= temperature <= -1:
                    message = f"Установлена температура: {temperature}°C ❄️"
            except ValueError:
                message = "Ошибка: введено некорректное значение температуры"
    return render_template('lab4/fridge.html', message=message) 

prices = {
            'ячмень': 12345,
            'овёс': 8522,
            'пшеница': 8722,
            'рожь': 14111
        }

@lab4.route('/lab4/seed', methods=['GET', 'POST'])
def seed():
    if request.method == 'POST':
        grain_type = request.form.get('grain-type')
        weight = request.form.get('weight')

        if not weight:
            error_message = "Ошибка: Не указан вес."
            return render_template('lab4/seed.html', error_message=error_message)
    
        weight = float(weight)

        if weight <= 0:
            error_message = "Ошибка: Вес должен быть больше 0."
            return render_template('lab4/seed.html', error_message=error_message)


        price_per_ton = prices.get(grain_type)

        total_price = weight * price_per_ton
        discount = 0

        if weight > 500:
            error_message = "К сожалению, такого объёма сейчас нет в наличии."
            return render_template('lab4/seed.html', error_message=error_message)
        elif weight > 50:
            discount = 0.1 * total_price
            total_price -= discount

        return render_template(
            'lab4/seed.html',
            grain_type=grain_type,
            weight=weight,
            total_price=total_price,
            discount=discount,
            success_message = (
                f"Заказ успешно сформирован. Вы заказали {grain_type}.<br>"
                f"Вес: {weight} т.<br>"
                f"Сумма к оплате: {total_price:.2f} руб.<br>"
                f"Применена скидка за большой объём: {discount:.2f} руб."
            )
        )

    return render_template('lab4/seed.html')

