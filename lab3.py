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