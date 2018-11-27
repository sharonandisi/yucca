from flask import render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required
from . import auth
from ..models import Admin, Comments, Posts
from .forms import RegistrationForm, LoginForm
from .. import db
from ..email import mail_message

@auth.route('/login', methods=['GET', 'POST'])
def login():
  login_form = LoginForm()
  if login_form.validate_on_submit():
    admin = Admin.query.filter_by(username=login_form.username.data).first()
    if admin is not None and admin.verify_password(login_form.password.data):
      login_user(admin, login_form.remember.data)
      return redirect(request.args.get('next') or url_for('main.index'))

    flash('Invalid Username or Password')

  title = 'Yucca Admin Login'
  return render_template('auth/login.html', login_form = login_form, title = title)

@auth.route('/register', methods=['GET', 'POST'])
def register():
  form = RegistrationForm()
  if form.validate_on_submit():
    admin = Admin(email=form.email.data, username=form.username.data, password=form.password.data, first_name=form.fname.data, surname=form.lname.data)

    db.session.add(admin)
    db.session.commit()

    title='New Account'
    mail_message('Welcome to Yucca', 'email/welcome_user', admin.email, admin=admin)
    return redirect(url_for('auth.login'))

  return render_template('auth/register.html', registration_form=form)


@auth.route('/logout')
@login_required
def logout():
  logout_user()
  return redirect(url_for("main.index"))