from flask import Flask, Response, request, jsonify, render_template, redirect, url_for, flash, session
from datetime import datetime
import json
from movie_resource import MovieResource
from flask_cors import CORS

# Create the Flask application object.
app = Flask(__name__,
            static_url_path='/',
            static_folder='static/class-ui/',
            template_folder='templates')

CORS(app)


@app.route("/api/health")
def get_health():
    t = str(datetime.now())
    msg = {
        "name": "Movie-Microservice",
        "health": "Good",
        "at time": t
    }

    # DFF TODO Explain status codes, content type, ... ...
    result = Response(json.dumps(msg), status=200, content_type="application/json")

    return result

#
# @app.route("api/")
# def index():
#     return render_template("index.html")


@app.route("/api/movie/addNewMovie")
def add_movie():
    return render_template('create_movie.html')

@app.route("/api/movie/create", methods=["GET", "POST"])
def create():
    if request.method == 'POST':
        name = request.form['movie_name']
        category = request.form['category']
        year = request.form['year']
        rating = request.form['rating']
        if name is None or category is None or year is None or rating is None:
            flash("check your input")
            return redirect(url_for('add_movie'))
        try:
            result = MovieResource.add_movie(name, category, year, rating)
            return '', 200
        except:
            return '', 400
    return




@app.route("/api/movies", methods=["GET"])
def get_all_movies():
    result = MovieResource.get_all()
    if result:
        rsp = Response(json.dumps(result), status=200, content_type="application.json")
    else:
        rsp = Response("NOT FOUND", status=404, content_type="text/plain")

    return rsp


@app.route("/api/movies/<guid>", methods=["GET"])
def get_movie_by_id(guid):
    print(guid)
    result = MovieResource.get_by_key(guid)
    print(result)
    if result:
        rsp = Response(json.dumps(result), status=200, content_type="application.json")
    else:
        rsp = Response("NOT FOUND", status=404, content_type="text/plain")

    return rsp

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001)

