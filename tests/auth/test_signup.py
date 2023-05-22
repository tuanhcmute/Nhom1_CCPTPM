
def test_login_get(client):
    response = client.get('/auth/signup')
    assert response.status_code == 200

def test_sign_up_success(client):
    # Gửi yêu cầu POST đến '/signup' với dữ liệu hợp lệ
    data = {
        'username': 'testuser1',
        'password': '123Qaz',
        'fullname': 'Test User',
        'address': 'Test Address',
        'age': '25',
        'email': 'test@example.com',
        'avatar': 'test.jpg'
    }
    response = client.post('/auth/signup', data=data)
    assert response.status_code == 200

def test_sign_up_fail(client):
    with client.session_transaction() as sess:
        # Tạo mock session
        sess['message_signup'] = None  # Khởi tạo giá trị None cho session['message']
    # Gửi yêu cầu POST đến '/signup' với dữ liệu hợp lệ
    data = {
        'username': 'testuser2',
        'password': '123',
        'fullname': 'Test User',
        'address': 'Test Address',
        'age': '25',
        'email': 'test1@example.com',
        'avatar': 'test.jpg'
    }
    response = client.post('/auth/signup', data=data)
    with client.session_transaction() as sess:
        # Kiểm tra giá trị của session['message'] sau khi xử lý yêu cầu
        assert sess['message_signup'] == "Mật khẩu phải từ 6 đến 20 ký tự"