from flask import Flask

from routes.public_routes import public_bp
from routes.auth_routes import auth_bp
from routes.manufacturer_routes import manufacturer_bp
from routes.service_routes import service_bp


app = Flask(__name__)

app.secret_key = "trace360-development-key"


app.register_blueprint(public_bp)
app.register_blueprint(auth_bp)
app.register_blueprint(manufacturer_bp)
app.register_blueprint(service_bp)


if __name__ == "__main__":
    app.run(debug=True)