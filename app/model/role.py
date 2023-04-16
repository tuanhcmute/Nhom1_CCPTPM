from app.extensions import db

class Role(db.Model):
  __tablename__ = 'tblRole'

  id = db.Column(db.Integer, primary_key=True, autoincrement=True)
  roleName = db.Column(db.String, unique=True, nullable=False)
  users = db.relationship('User', backref='Role', lazy=True)

  def __init__(self, roleName):
    self.roleName = roleName

  def __repr__(self) -> str:
    return f'<Role "{self.roleName}">'
