from models.modelUser import ModelUser
from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required

user_bp = Blueprint('user', __name__)

@user_bp.route('/users')
@login_required
def list_users():
    from app import db
    users = ModelUser.get_all(db)
    return render_template('users/list_users.html', users=users)

@user_bp.route('/users/create', methods=['GET', 'POST'])
@login_required
def create_user():
    if request.method == 'POST':
        from app import db
        name = request.form['namee']
        email = request.form['email']
        password = request.form['password']
        confirm_password = request.form['confirm_password']
        role = request.form.get('role', 'cotizador')

        if password != confirm_password:
            flash('Las contraseñas no coinciden.', 'danger')
            return redirect(url_for('user.create_user'))

        try:
            ModelUser.create_user(db, name, email, password, role)
            flash('Usuario creado exitosamente', 'success')
        except Exception as ex:
            flash(f'Error al crear usuario: {ex}', 'danger')
            return redirect(url_for('user.create_user'))
        return redirect(url_for('user.list_users'))

    return render_template('users/create_user.html')

@user_bp.route('/users/edit/<int:user_id>', methods=['GET', 'POST'])
@login_required
def edit_user(user_id):
    from app import db
    if request.method == 'POST':
        name = request.form['namee']
        email = request.form['email']
        role = request.form.get('role', 'cotizador')
        password = request.form.get('password', '').strip()
        confirm_password = request.form.get('confirm_password', '').strip()

        if password and password != confirm_password:
            flash('Las contraseñas no coinciden.', 'danger')
            return redirect(url_for('user.edit_user', user_id=user_id))

        if password and len(password) < 6:
            flash('La contraseña debe tener al menos 6 caracteres.', 'danger')
            return redirect(url_for('user.edit_user', user_id=user_id))

        try:
            ModelUser.update_user(db, user_id, name, email, role, password if password else None)
            flash('Usuario actualizado exitosamente', 'success')
        except Exception as ex:
            flash(f'Error al actualizar usuario: {ex}', 'danger')
        return redirect(url_for('user.list_users'))

    user = ModelUser.get_by_id(db, user_id)
    if not user:
        flash('Usuario no encontrado.', 'danger')
        return redirect(url_for('user.list_users'))
    return render_template('users/edit_user.html', user=user)

@user_bp.route('/users/delete/<int:user_id>', methods=['POST'])
@login_required
def delete_user(user_id):
    from app import db
    try:
        ModelUser.delete_user(db, user_id)
        flash('Usuario eliminado exitosamente', 'success')
    except Exception as ex:
        flash(f'Error al eliminar usuario: {ex}', 'danger')
    return redirect(url_for('user.list_users'))