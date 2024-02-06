from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String, Float
from main import app
from tmbd_api import *

MOVIE_DB_IMAGE_URL = "https://image.tmdb.org/t/p/w500"


# -----------------------------------------------------------------------
# ---------------------------- CREATE DB --------------------------------
# -----------------------------------------------------------------------
class Base(DeclarativeBase):
    pass


app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///top_movie.db"
db = SQLAlchemy(model_class=Base)
db.init_app(app)


# -----------------------------------------------------------------------
# --------------------------- CREATE TABLE ------------------------------
# -----------------------------------------------------------------------

class Movie(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String(250), unique=True, nullable=False)
    year: Mapped[int] = mapped_column(Integer, nullable=False)
    description: Mapped[str] = mapped_column(String(500), nullable=False)
    rating: Mapped[float] = mapped_column(Float, nullable=True, default=0)
    ranking: Mapped[int] = mapped_column(Integer, nullable=True)
    review: Mapped[str] = mapped_column(String(250), nullable=True)
    img_url: Mapped[str] = mapped_column(String(250), nullable=False)


with app.app_context():
    db.create_all()


# -----------------------------------------------------------------------
# ----------------------------- FUNCTIONS -------------------------------
# -----------------------------------------------------------------------
def get_movies():
    with app.app_context():
        result = db.session.execute(db.select(Movie).order_by(Movie.ranking))
        movies = list(result.scalars())
        return movies


def modify_movie(title, to_update, value):
    with app.app_context():
        movie_to_update = db.session.execute(db.select(Movie).where(Movie.title == title)).scalar()
        setattr(movie_to_update, to_update, value)
        db.session.commit()


def delete_movie(title):
    with app.app_context():
        movie_to_delete = db.session.execute(db.select(Movie).where(Movie.title == title)).scalar()
        db.session.delete(movie_to_delete)
        db.session.commit()


def new_movie(data):
    with app.app_context():
        data = find_selected_movie(data)
        movie_to_add = Movie(title=data["title"], year=data["release_date"].split("-")[0],
                             img_url=f"{MOVIE_DB_IMAGE_URL}{data['poster_path']}", description=data["overview"])
        db.session.add(movie_to_add)
        db.session.commit()
    return data["title"]


def asign_movie_ranking():
    with app.app_context():
        result = db.session.execute(db.select(Movie).order_by(Movie.rating))
        all_movies = result.scalars().all()
        for i in range(len(all_movies)):
            all_movies[i].ranking = len(all_movies) - i
        db.session.commit()
