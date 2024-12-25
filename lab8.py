from flask import Blueprint, redirect, url_for, render_template, request, flash
from db import db  
from db.models import users, Article  # Измените на Article
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, current_user, logout_user

lab8 = Blueprint('lab8', __name__, static_folder='static')

@lab8.route('/lab8/')
def main():
    return render_template('/lab8/lab8.html', user=current_user.login if current_user.is_authenticated else None)

@lab8.route('/lab8/register/', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('lab8/register.html')
    
    login_form = request.form.get('login')
    password_form = request.form.get('password')

    if not login_form:
        return render_template('lab8/register.html', error='Имя пользователя не должно быть пустым')

    if not password_form:
        return render_template('lab8/register.html', error='Пароль не должен быть пустым')

    login_exists = users.query.filter_by(login=login_form).first()
    if login_exists:
        return render_template('lab8/register.html', error='Такой пользователь уже существует')
    
    password_hash = generate_password_hash(password_form)
    new_user = users(login=login_form, password=password_hash)
    db.session.add(new_user)
    db.session.commit()
    
    login_user(new_user)
    return redirect('/lab8/')

@lab8.route('/lab8/login/', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('lab8/login.html')
   
    login_form = request.form.get('login')
    password_form = request.form.get('password')

    user = users.query.filter_by(login=login_form).first()
    if user and check_password_hash(user.password, password_form):
        login_user(user)
        return redirect(url_for('lab8.main'))
    else:
        return render_template('lab8/login.html', error='Неверный логин или пароль')

@lab8.route('/lab8/logout')
@login_required
def logout():
    logout_user()
    return redirect('/lab8/')

@lab8.route('/lab8/create', methods=['GET', 'POST'])
@login_required
def create_article():
    if request.method == 'POST':
        title = request.form.get('title')
        article_text = request.form.get('article_text')  
        
        new_article = Article(title=title , article_text=article_text, login_id=current_user.id)
        
        db.session.add(new_article)
        db.session.commit()
        flash('Статья успешно создана!', 'success')  
        return redirect(url_for('lab8.article_list'))  
    
    return render_template('lab8/create_article.html')

@lab8.route('/lab8/articles/')
def article_list():
    articles = Article.query.all()  
    for article in articles:
        article.user_login = users.query.get(article.login_id).login  
    return render_template('lab8/article_list.html', articles=articles)

@lab8.route('/lab8/edit/<int:article_id>', methods=['GET', 'POST'])
@login_required
def edit_article(article_id):
    article_instance = Article.query.get_or_404(article_id)  
    if request.method == 'POST':
        title = request.form.get('title')
        article_text = request.form.get('content') 
        
        article_instance.title = title
        article_instance.article_text = article_text
        db.session.commit()  
        return redirect('/lab8/articles/')  
    return render_template('lab8/edit_article.html', article=article_instance)

@lab8.route('/lab8/delete/<int:article_id>', methods=['POST'])
@login_required
def delete_article(article_id):
    article_instance = Article.query.get_or_404(article_id)  
    db.session.delete(article_instance)  
    db.session.commit()  
    return redirect('/lab8/articles/') 