from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
import os
from flask_login import LoginManager

db = SQLAlchemy()

def create_app():
    app = Flask(__name__, template_folder='../templates')

    # Configure SQLite database
    basedir = os.path.abspath(os.path.dirname(__file__))
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, '../movies.db')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = 'your-secret-key'  # Required for Flask-Login

    db.init_app(app)

    from app.routes import main_bp, auth_bp
    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp)

    # Initialize Flask-Login
    login = LoginManager(app)
    login.login_view = 'auth.login'  # terug naar login, indien niet geregistreerd

    @login.user_loader
    def load_user(user_id):
        from app.models import User  # kreeg circular imports, vgm fixt dit het
        return User.query.get(int(user_id))  # users by id get

    # Custom 404 error handler
    @app.errorhandler(404)
    def page_not_found(e):
        return render_template('404.html'), 404

    with app.app_context():
        db.create_all()  # Ensure the tables are created

    return app
