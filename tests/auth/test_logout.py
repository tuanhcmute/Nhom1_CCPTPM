def test_logout(client):
    client.post('/auth/login', data={'username': 'admin', 'password': 'admin'})
    response = client.get('/auth/logout', follow_redirects=True)
    # Kiểm tra phản hồi và trạng thái chuyển hướng
    assert response.status_code == 200