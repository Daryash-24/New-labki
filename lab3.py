from flask import Blueprint, template_rendered, render_template, request, make_response, redirect, session, url_for
lab3 = Blueprint('lab3', __name__)

@lab3.route('/lab3/')
def lab():
    name = request.cookies.get('name') or 'Аноним'
    age = request.cookies.get('age') or 'неизвестный'
    name_color = request.cookies.get('name_color')
    return render_template('lab3/lab3.html', name=name, age = age, name_color=name_color)

@lab3.route('/lab3/cookie')
def cookie():
    resp = make_response(redirect('/lab3/'))
    resp.set_cookie('name', 'Alex', max_age=5)
    resp.set_cookie('age', '20')
    resp.set_cookie('name_color', 'teal')
    return resp


@lab3.route('/lab3/del_cookie')
def del_cookie():
    resp = make_response(redirect('/lab3'))
    resp.delete_cookie('name')
    resp.delete_cookie('age')
    resp.delete_cookie('name_color')
    resp.set_cookie('name_color', 'black')
    return resp


@lab3.route('/lab3/form1')
def form1():
    errors = {}
    user = request.args.get('user')
    if user == '':
        errors['user'] = 'Поле не заполнено!'

    age = request.args.get('age')
    if age == '':
        errors['age'] = 'Поле не заполнено!'

    sex = request.args.get('sex')
    return render_template('lab3/form1.html', user=user, age=age, sex=sex, errors=errors)


@lab3.route('/lab3/order')
def order():
    return render_template ('lab3/order.html')


@lab3.route('/lab3/pay')
def pay():
    price = 0
    drink = request.args.get('drink')
    if drink == 'coffe':
        price = 120
    elif drink == 'black-tea':
        price = 80
    else:
        price = 70

    if request.args.get('milk') == 'on':
        price += 30
    if request.args.get('sugar') == 'on':
        price += 10

    return render_template ('lab3/pay.html', price=price)

@lab3.route('/lab3/success')
def success():
    price = request.args.get('price', 0)
    return render_template ('lab3/success.html', price=price)


@lab3.route('/lab3/settings', methods=['GET', 'POST'])
def settings():
    if request.method == 'POST':
        color = request.form.get('color')
        background = request.form.get('background')
        size = request.form.get('size')
        font_style = request.form.get('font-style')

        resp = make_response(redirect('/lab3/settings'))

        if color:
            resp.set_cookie('color', color)
        if background:
            resp.set_cookie('background', background)
        if size:
            resp.set_cookie('size', size)
        if font_style: 
            resp.set_cookie('font-style', font_style)

        return resp

    background = request.cookies.get('background')
    color = request.cookies.get('color')
    size = request.cookies.get('size')
    font_style = request.cookies.get('font-style')

    return make_response(render_template('lab3/settings.html', color=color, 
                                         background=background, size=size, font_style=font_style))


@lab3.route('/lab3/clear_cookies')
def clear_cookies():
    resp = make_response(redirect(url_for('lab3.settings')))
    resp.set_cookie('color', '', expires=0)
    resp.set_cookie('background', '', expires=0)
    resp.set_cookie('size', '', expires=0)
    resp.set_cookie('font-style', '', expires=0)
    return resp


@lab3.route('/lab3/ticket_registration')
def ticket_registration():
    return render_template('lab3/ticket_registration.html')


@lab3.route('/lab3/ticket')
def ticket():
    age = int(request.args.get('age'))
    ticket_price = 0
    if age < 18:
        ticket_type = 'Детский билет'
        ticket_price = 700  
    else:
        ticket_type = 'Взрослый билет'
        ticket_price = 1000  

    shelf = request.args.get('shelf')
    if shelf in ['bottom-shelf', 'lower-side']:
        ticket_price += 100  

    if request.args.get('linen') == 'on':
        ticket_price += 75  

    if request.args.get('baggage') == 'on':
        ticket_price += 250 

    if request.args.get('insurance') == 'on':
        ticket_price += 150 

    return render_template ('lab3/ticket.html', ticket_price=ticket_price, ticket_type=ticket_type)


phones = [
    {'name': 'iPhone 16 Pro Max', 'price': 1800, 'brand': 'Apple', 'color': 'Space Black'},
    {'name': 'Samsung Galaxy S23 Ultra', 'price': 1100, 'brand': 'Samsung', 'color': 'Phantom Black'},
    {'name': 'Google Pixel 7 Pro', 'price': 900, 'brand': 'Google', 'color': 'Obsidian'},
    {'name': 'iPhone 15 Pro', 'price': 1100, 'brand': 'Apple', 'color': 'Graphite'},
    {'name': 'Samsung Galaxy S22 Ultra', 'price': 800, 'brand': 'Samsung', 'color': 'Phantom Black'},
    {'name': 'Google Pixel 6 Pro', 'price': 700, 'brand': 'Google', 'color': 'Sorta Sunny'},
    {'name': 'iPhone 14 Pro Max', 'price': 900, 'brand': 'Apple', 'color': 'Pacific Blue'},
    {'name': 'Samsung Galaxy S21 Ultra', 'price': 700, 'brand': 'Samsung', 'color': 'Phantom Black'},
    {'name': 'Google Pixel 5', 'price': 500, 'brand': 'Google', 'color': 'Sorta Sage'},
    {'name': 'iPhone 13 Pro Max', 'price': 800, 'brand': 'Apple', 'color': 'Midnight Green'},
    {'name': 'Samsung Galaxy S20 Ultra', 'price': 600, 'brand': 'Samsung', 'color': 'Cosmic Gray'},
    {'name': 'Google Pixel 4 XL', 'price': 400, 'brand': 'Google', 'color': 'Oh So Orange'},
    {'name': 'iPhone XR', 'price': 400, 'brand': 'Apple', 'color': 'Yellow'},
    {'name': 'Samsung Galaxy A53 5G', 'price': 400, 'brand': 'Samsung', 'color': 'Awesome Black'},
    {'name': 'Google Pixel 6a', 'price': 350, 'brand': 'Google', 'color': 'Sage'},
    {'name': 'iPhone SE (3rd generation)', 'price': 450, 'brand': 'Apple', 'color': 'Midnight'},
    {'name': 'Samsung Galaxy A33 5G', 'price': 350, 'brand': 'Samsung', 'color': 'Awesome Black'},
    {'name': 'Google Pixel 6', 'price': 500, 'brand': 'Google', 'color': 'Sorta Seafoam'},
    {'name': 'iPhone 11', 'price': 400, 'brand': 'Apple', 'color': 'Purple'},
    {'name': 'Samsung Galaxy A73 5G', 'price': 450, 'brand': 'Samsung', 'color': 'Awesome Gray'},
    {'name': 'Google Pixel 5a', 'price': 350, 'brand': 'Google', 'color': 'Mostly Black'},
    {'name': 'iPhone 8 Plus', 'price': 300, 'brand': 'Apple', 'color': 'Gold'},
    {'name': 'Samsung Galaxy A52 5G', 'price': 300, 'brand': 'Samsung', 'color': 'Awesome Black'},
    {'name': 'Google Pixel 4a', 'price': 250, 'brand': 'Google', 'color': 'Just Black'}
]

@lab3.route('/lab3/phones', methods=['GET', 'POST'])
def phones_page():
    if request.method == 'POST':
        min_price = int(request.form.get('min_price', 0))
        max_price = int(request.form.get('max_price', 100000))
        filtered_phones = [phone for phone in phones if min_price <= phone['price'] <= max_price]
        return render_template('lab3/phones.html', phones=filtered_phones, min_price=min_price, max_price=max_price)
    else:
        return render_template('lab3/phones.html', phones=phones)

@lab3.route('/lab3/')
def index():
    return redirect(url_for('lab3.phones_page'))

