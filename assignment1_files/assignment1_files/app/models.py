from app import db

# Movie model representing the movies table
class Movie(db.Model):
    __table_args__ = {'extend_existing': True}
    __tablename__ = 'movies'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    year = db.Column(db.Integer, nullable=True)
    oscars = db.Column(db.Integer, nullable=True)
