from models.modelUser import ModelUser
from flask import Blueprint, render_template, request, redirect, url_for, flash

user_bp = Blueprint('user', __name__)

@user_bp.route('/users/create', methods=['GET', 'POST'])
def create_user():
    if request.method == 'POST':
        from app import db
        name = request.form['namee']
        email = request.form['email']
        password = request.form['password']

        try:
            ModelUser.create_user(db, name, email, password)
            flash('Usuario creado exitosamente', 'success')
        except Exception as ex:
            flash(f'Error al crear usuario: {ex}', 'danger')
        return redirect(url_for('user.create_user'))

    return render_template('users/create_user.html')