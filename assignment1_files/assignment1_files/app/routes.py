from assignment1_files.assignment1_files.flask_application_assignment2 import Blueprint, render_template, request, redirect, url_for
from app.models import Movie
from app import db

# Define the Blueprint
main_bp = Blueprint('main', __name__)

@main_bp.route('/', methods=['GET'])
def index():
    # Get all movies from the database
    movie_list = Movie.query.all()
    return render_template('index.html', movies=movie_list)

@main_bp.route('/add_movie', methods=['GET', 'POST'])
def add_movie():
    movie = None

    if request.method == 'POST':
        movie_id = request.form.get('id')

        # If id is given check if the movie exists and update it
        if movie_id:
            movie = Movie.query.get(movie_id)
            if movie:
                # Update movie fields with the form data
                movie.name = request.form.get('name')
                movie.year = request.form.get('year')
                movie.oscars = request.form.get('oscars')
            else:
                return "Movie not found.", 404
        else:
            # Add new movie if no ID is given
            movie_name = request.form.get('name')
            movie_year = request.form.get('year')
            movie_oscars = request.form.get('oscars')

            movie = Movie(
                name=movie_name,
                year=int(movie_year) if movie_year else None,
                oscars=int(movie_oscars) if movie_oscars else None
            )

        # Add and Commit changes to the database for both update and add
        db.session.add(movie)
        db.session.commit()
        return redirect(url_for('main.index'))

    # Check if editing an existing movie via query parameter
    movie_id = request.args.get('id')
    if movie_id:
        movie = Movie.query.get(movie_id)

    return render_template('add_movie.html', movie=movie)

@main_bp.route('/delete_movie/<int:id>', methods=['POST'])
def delete_movie(id):
    movie = Movie.query.get(id)  # Get the movie by ID

    if not movie:
        return render_template('index.html', movies=Movie.query.all(), error="Movie not found.")

    try:
        db.session.delete(movie)  # Delete the movie
        db.session.commit()  # Commit the changes
        return redirect(url_for('main.index'))  # Redirect back to the movies list
    except Exception as e:
        return f"There was a problem deleting that movie. Error: {str(e)}"
