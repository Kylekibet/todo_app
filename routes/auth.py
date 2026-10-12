from forms import LoginForm, RegisterUser
from flask import Blueprint, render_template, redirect, url_for, flash
from werkzeug.security import generate_password_hash, check_password_hash
from models import db, User
from flask_login import login_user, logout_user

auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/login', methods=["GET", "POST"])
def log_in():
    login_form = LoginForm()
    if login_form.validate_on_submit():
        email = login_form.email.data
        password = login_form.password.data
        user = db.session.execute(db.select(User).where(User.email == email)).scalar()
        if user and check_password_hash(user.password_hash, password):
            login_user(user)
            return redirect(url_for('pages.view_categories'))
        flash("Invalid email or password.", "danger")
        return redirect(url_for('auth.log_in'))
    return render_template('login.html', form=login_form)


@auth_bp.route('/sign_up', methods=['GET', 'POST'])
def sign_up():
    form = RegisterUser()
    if form.validate_on_submit():
        existing = db.session.execute(db.select(User).where(User.email == form.email.data)).scalar()
        if existing:
            flash("That email is already registered.", "danger")
            return redirect(url_for('auth.sign_up'))
        user = User(
            email=form.email.data,
            username=form.username.data,
            name=form.name.data,
            password_hash=generate_password_hash(form.password.data, method='scrypt', salt_length=16),
        )
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('auth.log_in'))
    return render_template('sign_up.html', form=form)


@auth_bp.route('/logout')
def log_out():
    logout_user()
    return redirect(url_for('pages.home'))