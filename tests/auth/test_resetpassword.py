def test_get_reset_password_form(client):
    response = client.get('/auth/reset-password')
    assert response.status_code == 200
    assert b'Reset Password' in response.data