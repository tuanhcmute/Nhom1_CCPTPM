from app.model.user import User

def test_login_get(client):
    response = client.get('/auth/login')
    assert response.status_code == 200

def test_login_post_success(client):
    with client.session_transaction() as sess:
        # Tạo mock session
        sess['message'] = None  # Khởi tạo giá trị None cho session['message']
    response = client.post('/auth/login', data={'username': 'admin', 'password': 'admin'})
    with client.session_transaction() as sess:
        # Kiểm tra giá trị của session['message'] sau khi xử lý yêu cầu
        assert sess['message'] == None

def test_login_post_deny(client):
    with client.session_transaction() as sess:
        # Tạo mock session
        sess['message'] = None  # Khởi tạo giá trị None cho session['message']
    response = client.post('/auth/login', data={'username': 'admin1', 'password': 'admin'})
    with client.session_transaction() as sess:
        # Kiểm tra giá trị của session['message'] sau khi xử lý yêu cầu
        assert sess['message'] == 'Access Denied'

def test_login_post_fail(client):
    with client:
        with client.session_transaction() as sess:
            # Tạo mock session
            sess['message'] = None  # Khởi tạo giá trị None cho session['message']
        response = client.post('/auth/login', data={'username': 'admin', 'password': 'admin1'})
        with client.session_transaction() as sess:
            # Kiểm tra giá trị của session['message'] sau khi xử lý yêu cầu
            assert sess['message'] == 'Invalid username or password'