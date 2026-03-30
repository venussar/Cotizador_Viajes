from flask import Blueprint,  render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user
from models.modelvehicle import ModelVehicle
from models.modelquote import ModelQuote

quote_bp = Blueprint('quote', __name__)


@quote_bp.route('/cotizaciones')
@login_required
def cotizaciones():
    from app import db
    vehiculos = ModelVehicle.get_all(db)  # Obtener la lista de vehículos
    return render_template('qoutes/cotizaciones.html', vehiculos=vehiculos)


@quote_bp.route('/historial')
@login_required
def historial():
    from app import db
    cotizaciones = ModelQuote.get_all_by_user(db, current_user.id)
    return render_template('qoutes/historial.html', cotizaciones=cotizaciones)


@quote_bp.route('/cotizaciones/crear', methods=['POST'])
@login_required
def crear_cotizacion():
    from app import db
    try:
        distancia = request.form.get('distancia', None)
        precio_combustible = request.form.get('precio_combustible', None)
        peajes = request.form.get('peajes', None)
        incentivos = request.form.get('incentivos', None)
        hotel = request.form.get('hotel', None)
        tipo_vehiculo = request.form.get('tipo_vehiculo', None)

        # Verificar que todos los datos requeridos están presentes
        if not all([distancia, precio_combustible, peajes, incentivos, hotel, tipo_vehiculo]):
            flash('Por favor, complete todos los campos del formulario.', 'danger')
            return redirect(url_for('quote.cotizaciones'))

        # Preparar datos para la base de datos
        data = {
            "round_trip_distance_km": float(distancia),
            "tolls_value": float(peajes),
            "incentive_value": float(incentivos),
            "hotel_cost": float(hotel),
            "commission_percentage": int(request.form.get('comision', 0)),
            "vehicle_id": int(tipo_vehiculo),
            "user_id": current_user.id,
            "fuel_price": float(precio_combustible),
            "subtotal": float(request.form.get('subtotal_hidden', 0)),
            "commission_value": float(request.form.get('commission_value_hidden', 0)),
            "total": float(request.form.get('total_hidden', 0)),
        }


        try:
            ModelQuote.create(db, data)
            print("Cotización guardada exitosamente en la base de datos.")
        except Exception as ex:
            print("Error al guardar en la base de datos:", ex)  # Mostrar error si ocurre
            flash(f"Error al guardar la cotización: {ex}", "danger")

        flash('Cotización creada exitosamente', 'success')
    except Exception as ex:
        print("Error al procesar la solicitud:", ex)  # Mostrar error si ocurre
        flash(f'Error al crear la cotización: {ex}', 'danger')
    return redirect(url_for('quote.cotizaciones'))
