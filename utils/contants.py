class Method:
  POST = 'POST'
  GET = 'GET'
  PUT = 'PUT'
  DELETE = 'DELETE'
  PATCH = 'PATCH'

class StatusCode:
  _200 = 200
  _404 = 404
  _500 = 500


class URI:
  HOME = '/'
  LOGIN = '/login'
  REGISTER = '/register'
  LOGOUT = '/logout'