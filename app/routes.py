from . import app, db
from app.models import User
from flask import render_template, request, redirect, url_for

@app.route('/')
def home():
  return render_template('index.html')

@app.route('/login')
def login():
  return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
  if request.method =="POST":
    name = request.form.get('name')
    email = request.form.get('email')
    password = request.form.get('password')
    confirm_password = request.form.get('confirm_password')

    if confirm_password == password:
      u = User(name=name, email=email, password=password)
      u.generate_password(u.password)

      db.session.add(u)
      db.session.commit()
      return redirect(url_for('login'))

  return render_template('register.html')