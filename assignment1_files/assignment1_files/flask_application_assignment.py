from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import os

#Create App context
app = Flask(__name__)

basedir = os.path.abspath(os.path.dirname(__file__))

# Configure SQLite database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///'+os.path.join(basedir, 'movies.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize the database
db = SQLAlchemy(app)

# Movie model representing the movies table
class Movie(db.Model):
    __table_args__ = {'extend_existing': True}
    __tablename__ = 'movies'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    year = db.Column(db.Integer, nullable=True)
    oscars = db.Column(db.Integer, nullable=True)

# Create the database and the tables
with app.app_context():
    db.create_all()

@app.route('/', methods=['GET'])
def index():
    # Get all movies from the database
    movie_list = Movie.query.all()
    return render_template('index.html', movies=movie_list)

@app.route('/add_movie', methods=['GET', 'POST'])
def add_movie():
    movie = None

    if request.method ==  'POST':
        movie_id = request.form.get('id')
        
        # If an id is provided, check if the movie exists and update it
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
            # Add new movie if no ID is provided
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
        return redirect(url_for('index'))

    # Check if editing an existing movie via query parameter - pass to add values in add_movie page (optional)
    movie_id = request.args.get('id')
    if movie_id:
        movie = Movie.query.get(movie_id)

    return render_template('add_movie.html', movie=movie)

@app.route('/delete_movie/<int:id>', methods=['POST'])
def delete_movie(id):
    # Get the movie by ID
    [...]    
    
    try:
        # Delete the movie from the database
        [...]

        return redirect(url_for('index'))
    except:
        return "There was a problem deleting that movie."

if __name__ == '__main__':
    app.run(debug=False)