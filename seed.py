import os
from app import app, db
from models import Athlete, Bow
from datetime import date
from sqlalchemy import select

def seed_data():
    """Створює тестових спортсменів та луки"""
    print("--- Автозаповнення БД ---")
    
    with app.app_context():
        
        if db.session.scalar(select(Athlete).where(Athlete.email == 'admin@seed.com')):
            print("БД вже має тестові дані. Автозаповнення пропущено")
            return

        # ------------------- АДМІН -------------------
        admin = Athlete(
            email='admin@seed.com',
            fio='Головний адміністратор',
            start_date=date(2023, 1, 1),
            rank='Майстер Спорту',
            role='Admin'
        )
        admin.set_password('123456') 
        db.session.add(admin)
        print("Створено: Адміна")

        # ------------------- СПОРТСМЕН А -------------------
        athlete_a = Athlete(
            email='user_a@seed.com',
            fio='Оксана Лучникова',
            start_date=date(2024, 4, 10),
            rank='Кандидат в МС',
            role='Athlete'
        )
        athlete_a.set_password('123456')
        db.session.add(athlete_a)
        print("Створено: Спортсмена А")

        # ------------------- СПОРТСМЕН Б -------------------
        athlete_b = Athlete(
            email='user_b@seed.com',
            fio='Іван Стріла',
            start_date=date(2023, 11, 20),
            rank='Перший Розряд',
            role='Athlete'
        )
        athlete_b.set_password('123456')
        db.session.add(athlete_b)
        print("Створено: Спортсмена Б")
        
        db.session.commit()
        
        # ------------------- ТЕСТОВІ ЛУКИ -------------------
        
        bow_1 = Bow(name='Hunter Pro', athlete_id=athlete_a.id, shoulders='Limb B', draw_weight=38.5, draw_length=28.0, model='WNS')
        bow_2 = Bow(name='Тренувальний', athlete_id=athlete_b.id, shoulders='Limb C', draw_weight=30.0, draw_length=27.5, model='Hotr')
        bow_3 = Bow(name='Матчевий Лук', athlete_id=athlete_a.id, shoulders='Limb A', draw_weight=42.0, draw_length=28.5, model='WiaWis')
        bow_4 = Bow(name='Запасний WNS', athlete_id=athlete_a.id, shoulders='Limb D', draw_weight=36.0, draw_length=28.0, model='WNS')
        bow_5 = Bow(name='Зимовий Лук', athlete_id=athlete_b.id, shoulders='Limb B', draw_weight=32.5, draw_length=27.0, model='Hotr')
        
        db.session.add_all([bow_1, bow_2, bow_3, bow_4, bow_5])
        db.session.commit()
        print(f"Створено тестові луки")
        
        print("--- Автозаповнення завершено ---")

if __name__ == '__main__':
    seed_data()