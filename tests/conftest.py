import pytest
import os
from app import app as flask_app, db as flask_db
from models import Athlete

@pytest.fixture
def app():
    """Створює екземпляр тестового додатку"""
    # тестова конфігурація
    flask_app.config['TESTING'] = True
    flask_app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    flask_app.config['SECRET_KEY'] = 'test-secret-key'
    
    with flask_app.app_context():
        
        flask_db.create_all()
        # тестові користувачі
        admin = Athlete(email='test_admin@app.com', fio='Тест Адмін', role='Admin')
        admin.set_password('testpass')
        
        athlete_a = Athlete(email='test_user@app.com', fio='Тест Спортсмен А', role='Athlete')
        athlete_a.set_password('testpass')
        
        flask_db.session.add_all([admin, athlete_a])
        flask_db.session.commit()

        yield flask_app
        
        flask_db.session.remove()
        flask_db.drop_all()

@pytest.fixture
def client(app):
    """Створення тестового клієнта для відправки запитів"""
    return app.test_client()

@pytest.fixture
def auth_client(client):
    """Створення клієнта, який авторизується як Тест Спортсмен А"""
    client.post('/login', data={'email': 'test_user@app.com', 'password': 'testpass'}, follow_redirects=True)
    return client

@pytest.fixture
def admin_client(client):
    """Створюення клієнта, який авторизується як Тест Адмін"""
    client.post('/login', data={'email': 'test_admin@app.com', 'password': 'testpass'}, follow_redirects=True)
    return client