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


# ----------------- МАРШРУТИ ДЛЯ ЛУКІВ ---------------

# перегляд своїх луків
@app.route('/my_bows')
@login_required
def my_bows():
    bows = db.session.scalars(
        db.select(Bow).filter_by(athlete_id=current_user.id)
    ).all()
    return render_template('forBows/list.html', title='Мої луки', bows=bows, owner_view=True)

# створення одного луку
@app.route('/bow/create', methods=['GET', 'POST'])
@login_required
def create_bow():
    if request.method == 'POST':
        try:
            new_bow = Bow(
                name=request.form.get('name'),
                athlete_id=current_user.id,
                shoulders=request.form.get('shoulders'),
                draw_weight=float(request.form.get('draw_weight')),
                draw_length=float(request.form.get('draw_length')),
                model=request.form.get('model')
            )
            db.session.add(new_bow)
            db.session.commit()
            flash(f'Лук "{new_bow.name}" успішно створений!', 'success')
            return redirect(url_for('my_bows'))
        except Exception as e:
            flash(f'Помилка створення луку: {e}', 'danger')
            db.session.rollback()
            
    MODELS = ['Hotr', 'WiaWis', 'WNS']
    return render_template('forBows/form.html', title='Створити лук', models=MODELS, bow=None)

# редагування луку
@app.route('/bow/edit/<int:bow_id>', methods=['GET', 'POST'])
@login_required
def edit_bow(bow_id):
    bow = db.session.get(Bow, bow_id)
    
    if bow is None or bow.athlete_id != current_user.id:
        flash('Доступ заборонено або лук не знайдено.', 'danger')
        return redirect(url_for('my_bows'))

    if request.method == 'POST':
        try:
            bow.name = request.form.get('name')
            # athlete_id не змінюється
            bow.shoulders = request.form.get('shoulders')
            bow.draw_weight = float(request.form.get('draw_weight'))
            bow.draw_length = float(request.form.get('draw_length'))
            bow.model = request.form.get('model')
            
            db.session.commit()
            flash(f'Лук "{bow.name}" успішно оновлено!', 'success')
            return redirect(url_for('my_bows'))
        except Exception as e:
            flash(f'Помилка оновлення луку: {e}', 'danger')
            db.session.rollback()
            
    MODELS = ['Hotr', 'WiaWis', 'WNS']
    return render_template('forBows/form.html', title='Редагувати Лук', models=MODELS, bow=bow)

# видалення луку
@app.route('/bow/delete/<int:bow_id>', methods=['POST'])
@login_required
def delete_bow(bow_id):
    bow = db.session.get(Bow, bow_id)
    
    if bow is None or bow.athlete_id != current_user.id:
        flash('Доступ заборонено або лук не знайдено.', 'danger')
        return redirect(url_for('my_bows'))
        
    db.session.delete(bow)
    db.session.commit()
    flash('Лук успішно видалено.', 'success')
    return redirect(url_for('my_bows'))


# --------------- СТОРІНКА КОРИСТУВАЧА ---------------

@app.route('/profile')
@login_required
def profile():
    return render_template('profile.html', title='Мій профіль')

                
# ----------------- ГОЛОВНА СТОРІНКА -----------------

@app.route('/')
@login_required 
def index():
    return render_template('index.html', title='Головна сторінка')