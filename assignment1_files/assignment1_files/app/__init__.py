from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)

    # Configure SQLite database
    basedir = os.path.abspath(os.path.dirname(__file__))
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, '../movies.db')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)

    from app.routes import main_bp
    app.register_blueprint(main_bp)

    return app
