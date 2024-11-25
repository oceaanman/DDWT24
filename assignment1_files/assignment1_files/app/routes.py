from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from app.models import Movie, User
from app import db


# Blueprints for main and auth routes
main_bp = Blueprint('main', __name__)
auth_bp = Blueprint('auth', __name__)

# Movie Routes
@main_bp.route('/', methods=['GET'])
@login_required
def index():
    # Get all movies from the database
    movie_list = Movie.query.all()
    return render_template('index.html', movies=movie_list)

@main_bp.route('/add_movie', methods=['GET', 'POST'])
@login_required
def add_movie():
    if request.method == 'POST':
        movie_id = request.form.get('id')

        if movie_id:  # Edit movie
            movie = Movie.query.get(movie_id)
            if movie:
                movie.name = request.form.get('name')
                movie.year = request.form.get('year')
                movie.oscars = request.form.get('oscars')
            else:
                return "Movie not found.", 404
        else:  # Add new movie
            movie = Movie(
                name=request.form.get('name'),
                year=int(request.form.get('year')) if request.form.get('year') else None,
                oscars=int(request.form.get('oscars')) if request.form.get('oscars') else None
            )

        db.session.add(movie)
        db.session.commit()
        return redirect(url_for('main.index'))

    movie_id = request.args.get('id')
    movie = Movie.query.get(movie_id) if movie_id else None
    return render_template('add_movie.html', movie=movie)

@main_bp.route('/delete_movie/<int:id>', methods=['POST'])
@login_required
def delete_movie(id):
    movie = Movie.query.get(id)
    if movie:
        db.session.delete(movie)
        db.session.commit()
    return redirect(url_for('main.index'))

# Authentication Routes
@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()

        if user:
            flash('Username already exists.')
            return redirect(url_for('auth.register'))

        hashed_password = generate_password_hash(password)
        new_user = User(username=username, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()

        flash('Registration successful! Please log in.')
        return redirect(url_for('auth.login'))

    return render_template('register.html')

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()

        if user and check_password_hash(user.password, password):
            login_user(user)
            return redirect(url_for('main.index'))

        flash('Invalid username or password.')
    return render_template('login.html')

@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))
