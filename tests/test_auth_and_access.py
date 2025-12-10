from app import db
from models import Athlete, Bow

# Тест 1: Перевірка успішного логіну
def test_login_success(client):
    response = client.post('/login', data={'email': 'test_user@app.com', 'password': 'testpass'}, follow_redirects=True)
    assert response.status_code == 200
    assert "Тест Спортсмен А".encode('utf-8') in response.data

# Тест 2: Перевірка невдалого логіну
def test_login_failure(client):
    response = client.post('/login', data={'email': 'test_user@app.com', 'password': 'wrongpassword'}, follow_redirects=True)    
    assert response.status_code == 200
    assert 'Неправильна пошта або пароль'.encode('utf-8') in response.data

# Тест 3: Перевірка захисту адмін-маршруту від Спортсмена
def test_admin_route_protection(auth_client):
    # Спортсмен намагається отримати доступ до списку всіх луків
    response = auth_client.get('/admin/all_bows', follow_redirects=True)
    assert response.status_code == 200
    assert 'Доступ заборонено: потрібні права Адміна.'.encode('utf-8') in response.data
    
# Тест 4: Адмін може отримати доступ до адмін-маршруту
def test_admin_access_allowed(admin_client):
    response = admin_client.get('/admin/all_bows', follow_redirects=True)
    assert response.status_code == 200
    assert 'Всі луки'.encode('utf-8') in response.data 
