def test_get_sample_data_authenticated(client):
    # Đăng nhập trước khi lấy dữ liệu
    client.post('/auth/login', data={'username': 'admin', 'password': 'admin'})

    # Gửi yêu cầu lấy dữ liệu
    response = client.get('/data', query_string={'month': 5, 'year': 2022})

    # Kiểm tra phản hồi và trạng thái yêu cầu
    assert response.status_code == 200

