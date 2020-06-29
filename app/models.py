from . import db
from werkzeug.security import generate_password_hash, check_password_hash


class User(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String, nullable=False)
  email = db.Column(db.String, nullable=False)
  password = db.Column(db.String, nullable=False)

  def generate_password(self, original_password):
    self.password = generate_password_hash(original_password)
