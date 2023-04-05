from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import inspect, create_engine

db = SQLAlchemy()

def database_is_empty(url):
  engine = create_engine(url)
  insp = inspect(engine)
  table_names = insp.get_table_names()
  is_empty = table_names == []
  return is_empty
