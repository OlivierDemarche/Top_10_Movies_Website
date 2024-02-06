from flask import Flask, render_template, redirect, url_for, request
from flask_bootstrap import Bootstrap5
from sqlalchemy_database import *
from forms import *
from tmbd_api import *

# -----------------------------------------------------------------------
# ----------------------------- FLASK APP -------------------------------
# -----------------------------------------------------------------------

app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
Bootstrap5(app)


@app.route("/")
def home():
    asign_movie_ranking()
    movies = get_movies()
    return render_template("index.html", movies=movies)


@app.route("/edit", methods=["GET", "POST"])
def edit():
    edit_form = MyEditForm()
    if request.method == "GET":
        movie = request.args.get("movie")
        return render_template("edit.html", form=edit_form, movie=movie)
    elif request.method == "POST":
        movie = request.args.get("title")
        new_rating = edit_form.rating.data
        new_review = edit_form.review.data
        modify_movie(title=movie, to_update="rating", value=new_rating)
        modify_movie(title=movie, to_update="review", value=new_review)
        return redirect(url_for("home"))


@app.route("/delete")
def delete():
    movie_to_delete = request.args.get("movie")
    delete_movie(movie_to_delete)
    return redirect(url_for('home'))


@app.route("/add", methods=["GET", "POST"])
def add():
    adding_form = MyAddingForm()
    if adding_form.validate_on_submit():
        movie_title = adding_form.title.data
        data = get_movies_from_api(movie_title)
        return render_template("select.html", options=data)

    return render_template("add.html", form=adding_form)


@app.route("/select")
def select():
    movie_api_id = request.args.get("id")
    if movie_api_id:
        movie_title = new_movie(movie_api_id)
        return redirect(url_for("edit", movie=movie_title, _method="GET"))


if __name__ == '__main__':
    app.run(debug=True)
