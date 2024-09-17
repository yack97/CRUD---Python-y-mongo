# app/__init__.py

from flask import Flask

def create_app():
    app = Flask(__name__)

    # Registrar las rutas
    from .routes import main
    app.register_blueprint(main)

    return app