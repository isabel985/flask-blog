from app import db, login_manager
from app.models import User, Post
from flask import render_template, request, redirect, url_for, flash, current_app as app
from flask_login import login_user, logout_user, current_user, login_required

@app.route('/', methods=['GET', 'POST'])
def home():
  if current_user.is_authenticated:
    posts = current_user.followed_posts()
  else:
    posts = Post.query.order_by(Post.created_on).all()

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

@app.route('/profile')
@login_required
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

