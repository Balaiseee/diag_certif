from flask import Blueprint, render_template, flash, redirect, url_for
from flask_login import current_user, login_user, logout_user
from models import User
from auth.forms import LoginForm, RegistrationForm
from app import db

auth_bp = Blueprint('auth_bp', __name__, template_folder='templates/auth')


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home_bp.index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('auth_bp.login'))
        login_user(user, remember=form.remember_me.data)
        return redirect(url_for('home_bp.intro'))
    return render_template('login.html', title='Sign In', form=form)


@auth_bp.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home_bp.index'))


@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home_bp.index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('auth_bp.login'))
    return render_template('register.html', title='Register', form=form)