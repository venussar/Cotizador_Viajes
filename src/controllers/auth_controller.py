from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user

from models.modelUser import ModelUser

auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/')
def index():
    return redirect(url_for('auth.login'))


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    from app import db
    if request.method == 'POST':
        logged_user = ModelUser.login(db, request.form['namee'], request.form['password_hash'])
        if logged_user is not None:
            login_user(logged_user)
            return redirect(url_for('dashboard.home'))
        else:
            flash('Email o contraseña incorrectos')
        return render_template('auth/login.html')
    else:
        return render_template('auth/login.html')


@auth_bp.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('auth.login'))
