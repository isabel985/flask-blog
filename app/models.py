from . import db, login
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from datetime import datetime

followers = db.Table('followers', 
    db.Column('follower_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('followed_id', db.Integer, db.ForeignKey('user.id')),
  )

class User(UserMixin, db.Model):
  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String, nullable=False)
  email = db.Column(db.String, nullable=False, unique=True)
  password = db.Column(db.String, nullable=False)
  posts = db.relationship('Post', backref='posts', lazy='dynamic')
  followed = db.relationship(
    'User', secondary=followers,
        primaryjoin=(followers.c.follower_id == id),
        secondaryjoin=(followers.c.followed_id == id),
        backref=db.backref('followers', lazy='dynamic'), lazy='dynamic'
  )

  def generate_password(self, original_password):
    self.password = generate_password_hash(original_password)

  def check_password(self, original_password):
    return check_password_hash(self.password, original_password)

  def __repr__(self):
    return "<User {}>".format(self.name)

  def follow(self, user):
    if not self.is_following(user):
      self.followed.append(user)

  def unfollow(self, user):
    if self.is_following(user):
      self.followed.remove(user)

  def is_following(self, user):
    return self.followed.filter(followers.c.followed_id == user.id).count() > 0

class Post(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  title = db.Column(db.String())
  body = db.Column(db.Text)
  created_on = db.Column(db.DateTime, index=True, default=datetime.utcnow())
  user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

  def __repr__(self):
    return f'<Post: {self.body}>'

@login.user_loader
def load_user(user_id):
  return User.query.get (int(user_id))