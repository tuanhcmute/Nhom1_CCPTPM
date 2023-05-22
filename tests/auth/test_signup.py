from flask import session

def test_login_get(client):
    response = client.get('/auth/signup')
    assert response.status_code == 200

def test_sign_up_success(client, app):
    # Gửi yêu cầu GET đến '/signup'
    response = client.get('/auth/signup')
    assert response.status_code == 200

    # Gửi yêu cầu POST đến '/signup' với dữ liệu hợp lệ
    data = {
        'username': 'testuser',
        'password': 'testpassword',
        'fullname': 'Test User',
        'address': 'Test Address',
        'age': '25',
        'email': 'test@example.com',
        'avatar': 'test.jpg'
    }
    response = client.post('/signup', data=data)
    assert response.status_code == 200

    # Kiểm tra session
    with app.app_context():
        with app.test_request_context():
            assert 'message_signup' not in session