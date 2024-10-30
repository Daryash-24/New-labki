from flask import Blueprint, url_for, redirect, render_template, request
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