from . import account
from flask import request, render_template, redirect, url_for, flash
from flask_login import login_required, login_user, logout_user, current_user
from app.models import User
from app import db
import sqlalchemy, werkzeug

@account.route('/login', methods=['GET', 'POST'])
def login():
  # write a try/except block for incorrect password (and email). if user tries to type in the incorrect password, need to try to break application

  if request.method == "POST":
    email = request.form.get('email')
    password = request.form.get('password')
    remember_me = request.form.get('remember_me')

    try:
      user = User.query.filter_by(email=email).first()
      if user is None or not user.check_password(password):
        flash('Either your email address or password is not correct. Try again', 'warning')
        return redirect(url_for('account.login'))

        login_user(user, remember=remember_me)
        flash('User logged in successfully.', 'info')
        return redirect(url_for('home'))
      
    except AttributeError as err:
      print(err)
      print('you have an incorrect password or maybe you are trying to login as a use that desnt exist.')
    
  return render_template('login.html')


@account.route('/register', methods=['GET', 'POST'])
def register():
  if request.method == "POST":
    name = request.form.get('name')
    email = request.form.get('email')
    password = request.form.get('password')
    confirm_password = request.form.get('confirm_password')

    user = User.query.filter_by(email=email).first()
    if user is not None:
      flash('Email already exists. Use another one.', 'danger')
      return redirect(url_for('account.register'))

    if confirm_password != password:
      flash("Your passwords don't match. Try again.")
      return redirect(url_for('account.register'))

    try:
      u = User(name=name, email=email, password=password)
      u.generate_password(u.password)

      db.session.add(u)
      db.session.commit()
      flash('User registered successfully', 'success')
      return redirect(url_for('account.login'))

    except sqlalchemy.exc.IntegrityError as err:
      print(err)
      return redirect(url_for('account.register'))

  return render_template('register.html')

@account.route('/logout', methods=['GET'])
@login_required
def logout():
  # write try/except that checks if the current user is logged in
  try:
    logout_user()
    flash('This user has been logged out successfully.', 'info')
    return redirect(url_for('account.login'))

  except:
    print("Something went wrong. Try again.")