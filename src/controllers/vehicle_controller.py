from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required

from models.modelvehicle import ModelVehicle

# Crear Blueprint para vehículos
vehicle_bp = Blueprint('vehicle', __name__)


@vehicle_bp.route('/vehicles')
@login_required
def vehicles():
    from app import db
    vehicle_list = ModelVehicle.get_all(db)
    return render_template('vehicles/vehicles.html', vehicles=vehicle_list)


@vehicle_bp.route('/vehicles/create', methods=['POST'])
@login_required
def create_vehicle():
    from app import db
    try:
        data = {
            "type_vehicles": request.form['tipo_vehiculo'],
            "fuel_consumption_km": request.form['consumo_combustible'],
            "driver_cost": request.form['costo_chofer'],
            "labor_cost": request.form['costo_mano_obra']
        }
        ModelVehicle.create(db, data)
        flash('Vehículo creado exitosamente', 'success')
    except Exception as ex:
        flash(f'Error al crear vehículo: {ex}', 'danger')
    return redirect(url_for('vehicle.vehicles'))


@vehicle_bp.route('/vehicles/edit/<int:id>', methods=['POST'])
@login_required
def edit_vehicle(id):
    from app import db
    try:
        data = {
            "type_vehicles": request.form['tipo_vehiculo'],
            "fuel_consumption_km": request.form['consumo_combustible'],
            "driver_cost": request.form['costo_chofer'],
            "labor_cost": request.form['costo_mano_obra']
        }
        ModelVehicle.update(db, id, data)
        flash('Vehículo actualizado exitosamente', 'success')
    except Exception as ex:
        flash(f'Error al actualizar vehículo: {ex}', 'danger')
    return redirect(url_for('vehicle.vehicles'))


@vehicle_bp.route('/vehicles/delete/<int:id>', methods=['POST'])
@login_required
def delete_vehicle(id):
    from app import db
    try:
        ModelVehicle.delete(db, id)
        flash('Vehículo eliminado exitosamente', 'success')
    except Exception as ex:
        flash(f'Error al eliminar vehículo: {ex}', 'danger')
    return redirect(url_for('vehicle.vehicles'))
