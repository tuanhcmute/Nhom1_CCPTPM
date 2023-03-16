from app.model.user import User

# def test_login_get(client):
#     response = client.get('/auth/login')
#     print(response.data)
#     assert b'<title>404 Not Found</title>' in response.data

# def test_login_post(client, app):
#     response = client.post('/auth/login', data={'username': 'admin', 'password': 'admin'})
    
#     with app.app_context():
#         assert User.query.count() == 1
#         assert User.query.first().username == "admin"
