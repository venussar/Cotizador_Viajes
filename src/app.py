
from flask import Flask
from config import config
from flask_mysqldb import MySQL
from flask_login import LoginManager

from models.modelUser import ModelUser


app = Flask(__name__)
db = MySQL(app)
login_manager_app = LoginManager(app)
login_manager_app.login_view = 'auth.login'


@login_manager_app.user_loader
def load_user(id):
    return ModelUser.get_by_id(db, id)


from controllers.auth_controller import auth_bp
from controllers.dashboard_controller import dashboard_bp
from controllers.qoute_controller import quote_bp
from controllers.vehicle_controller import vehicle_bp
from controllers.user_controller import user_bp

app.register_blueprint(auth_bp)
app.register_blueprint(dashboard_bp)
app.register_blueprint(quote_bp)
app.register_blueprint(vehicle_bp)
app.register_blueprint(user_bp)


if __name__ == "__main__":
    app.config.from_object(config['development'])
    app.run()