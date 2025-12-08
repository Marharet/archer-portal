from app import app, db
from flask import render_template, redirect, url_for, flash, request
from models import Athlete, Bow
from flask_login import current_user, login_user, logout_user, login_required
from werkzeug.security import generate_password_hash

# ----------------- ТИМЧАСОВИЙ МАРШРУТ ДЛЯ АДМІНА -----------------

@app.route('/create_admin')
def create_admin():
    if db.session.get(Athlete, 1) is None: 
        admin = Athlete(
            email='admin@portal.com',
            fio='Адміністратор cистеми',
            rank='Майстер',
            role='Admin'
        )
        admin.set_password('adminpassword') 
        db.session.add(admin)
        db.session.commit()
        flash('Адміністратор створений: admin@portal.com / adminpassword', 'success')
        return redirect(url_for('login'))
    
    flash('Адміністратор вже існує.', 'info')
    return redirect(url_for('index'))



# ----------------- ЛОГІН ТА ЛОГАУТ -----------------

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index')) 
    
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        athlete = db.session.scalar(db.select(Athlete).filter_by(email=email))
        
        if athlete is None or not athlete.check_password(password):
            flash('Неправильна пошта або пароль', 'danger')
            return redirect(url_for('login'))
        
        login_user(athlete)
        next_page = request.args.get('next')
        return redirect(next_page) if next_page else redirect(url_for('index'))
    
    return render_template('login.html', title='Вхід')

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))


# ----------------- ГОЛОВНА СТОРІНКА -----------------

@app.route('/')
@login_required 
def index():
    return render_template('index.html', title='Головна сторінка')