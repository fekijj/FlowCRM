from flask import Flask
from backend.routes import register_routes

def create_app():
    app = Flask(__name__, template_folder="../frontend/templates")
    app.config['COLIZEOM'] = 'flowcrm-super-secret'
    register_routes(app)
    return app
