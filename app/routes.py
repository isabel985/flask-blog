from . import app, db, login
from app.models import User, Post
from flask import render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, current_user

@app.route('/', methods=['GET', 'POST'])
def home():
  print(current_user.id, current_user.name)
  if request.method == 'POST':
    post_body = request.form.get('post_body')
    p = Post(body=post_body, user_id=current_user.id)
    db.session.add(p)
    db.session.commit()
    flash('Post was successfully created', 'success')
    return redirect(url_for('home'))

  context = {
    'posts': Post.query.order_by(Post.created_on.desc()).all()
  }
  return render_template('index.html', **context)

@app.route('/post/<int:id>')
def home_single(id):
  post = Post.query.get(id)
  context = {
    'post': post
  }
  return render_template('index-single.html', **context)

@app.route('/login', methods=['GET', 'POST'])
def login():
  if request.method == "POST":
    email = request.form.get('email')
    password = request.form.get('password')
    remember_me = request.form.get('remember_me')

    user = User.query.filter_by(email=email).first()
    if user is None or not user.check_password(password):
      flash('Either your email address or password is not correct. Try again', 'warning')
      return redirect(url_for('login'))
    login_user(user, remember=remember_me)
    flash('User logged in successfully.', 'info')
    return redirect(url_for('home'))
  return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
  if request.method == "POST":
    name = request.form.get('name')
    email = request.form.get('email')
    password = request.form.get('password')
    confirm_password = request.form.get('confirm_password')

    user = User.query.filter_by(email=email).first()
    if user is not None:
      flash('Email already exists. Use another one.', 'danger')
      return redirect(url_for('register'))
    if confirm_password != password:
      flash("Your passwrds don't match. Try again.")
      return redirect(url_for('register'))
    else:
      u = User(name=name, email=email, password=password)
      u.generate_password(u.password)

      db.session.add(u)
      db.session.commit()
      flash('User registered successfully', 'success')
      return redirect(url_for('login'))

  return render_template('register.html')

@app.route('/logout')
def logout():
  logout_user()
  flash('This user has been logged out successfully.', 'info')
  return redirect(url_for('login'))

@app.route('/profile')
def profile():
  context = {
    'posts': User.query.get(current_user.id).posts.all()
  }
  return render_template('profile.html', **context)

@app.route('/profile/post/<int:id>')
def profile_single(id):
  post = Post.query.get(id)
  context = {
    'post': post
  }
  return render_template('post-single.html', **context)

@app.route('/users')
def users():
  context = {
    'users': [user for user in User.query.all() if user.id != current_user.id]
  }
  return render_template('users.html', **context)

@app.route('/users/follow/<int:id>')
def user_follow(id):
  user = User.query.get(id)
  current_user.follow(user)
  db.session.commit()
  flash(f"You have followed {user.name}", "success")
  return redirect(url_for('users'))

@app.route('/users/unfollow/<int:id>')
def user_unfollow(id):
  user = User.query.get(id)
  current_user.unfollow(user)
  db.session.commit()
  flash(f"You have unfollowed {user.name}", "warning")
  return redirect(url_for('users'))