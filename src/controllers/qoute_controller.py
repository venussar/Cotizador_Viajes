from flask import Blueprint, render_template
from flask_login import login_required

quote_bp = Blueprint('quote', __name__)


@quote_bp.route('/cotizaciones')
@login_required
def cotizaciones():
    return render_template('qoutes/cotizaciones.html')


@quote_bp.route('/historial')
@login_required
def historial():
    return render_template('qoutes/historial.html')
