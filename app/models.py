from . import db, login_manager
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from datetime import datetime
from hashlib import md5

followers = db.Table('followers', 
    db.Column('follower_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('followed_id', db.Integer, db.ForeignKey('user.id')),
  )

class User(UserMixin, db.Model):
  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String, nullable=False)
  email = db.Column(db.String, nullable=False, unique=True)
  password = db.Column(db.String, nullable=False)
  posts = db.relationship('Post', backref='author', lazy='dynamic')
  followed = db.relationship(
    'User', secondary=followers,
        primaryjoin=(followers.c.follower_id == id),
        secondaryjoin=(followers.c.followed_id == id),
        backref=db.backref('followers', lazy='dynamic'), lazy='dynamic'
  )

  def avatar(self, size):
    digest = md5(self.email.lower().encode('utf-8')).hexdigest()
    return f'https://www.gravatar.com/avatar/{digest}?s={size}&d=identicon'

  def followed_posts(self):
    followed = Post.query.join(followers, (followers.c.followed_id == Post.user_id)).filter(followers.c.follower_id == self.id)
    users_posts = Post.query.filter_by(user_id=self.id)
    return followed.union(users_posts).order_by(Post.created_on.desc())

  def generate_password(self, original_password):
    self.password = generate_password_hash(original_password)

  def check_password(self, original_password):
    return check_password_hash(self.password, original_password)

  def __repr__(self):
    return f'{self.name}'

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

@login_manager.user_loader
def load_user(user_id):
  return User.query.get (int(user_id))