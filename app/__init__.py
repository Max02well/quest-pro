import os
from flask import Flask
from app.routes.job_routes import job_bp
from app.routes.main_routes import main_bp
from dotenv import load_dotenv
from app.database import db  # Import db directly instead of init_db

load_dotenv()

def create_app():
    app = Flask(__name__, template_folder="templates", static_folder="static")
    app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY")


    app.register_blueprint(job_bp)
    app.register_blueprint(main_bp)

    return app
