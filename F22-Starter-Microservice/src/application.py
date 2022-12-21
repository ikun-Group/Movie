from flask import Flask, Response, request, jsonify, render_template, redirect, url_for, flash, session
from datetime import datetime
import json
from movie_resource import MovieResource
from flask_cors import CORS
import copy

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


# @app.route("api/")
# def index():
#     return render_template("index.html")


# @app.route("/api/movie/addNewMovie")
# def add_movie():
#     return render_template('create_movie.html')


@app.route("/api/movies", methods=["GET", "POST"])
def movies():
    if request.method == "GET":
        result = MovieResource.get_all()
        if result:
            rsp = Response(json.dumps(result), status=200, content_type="application.json")
        else:
            rsp = Response("NOT FOUND", status=404, content_type="text/plain")
        return rsp
    else:
        name = request.form['movie_name']
        category = request.form['category']
        year = request.form['year']
        rating = request.form['rating']
        if name is None or category is None or year is None or rating is None:
            res = 'check your input'
            status_code = 400
        else:
            try:
                ret = MovieResource.create_movie(name, category, year, rating)
                if ret:
                    res = 'Movie created!'
                    status_code = 201
                else:
                    res = 'Failed to create movie'
                    status_code = 422
            except Exception as e:
                res = 'Error: {}'.format(str(e))
                status_code = 422
        return Response(f"{status_code} - {res}", status=status_code, mimetype="application/json")


@app.route("/api/movies/<guid>", methods=["GET", "PUT", "DELETE"])
def movie_by_id(guid):
    if request.method == "GET":
        tmp = copy.copy(request.args)
        limit = tmp.get("limit")
        offset = tmp.get("offset")
        if limit and offset:
            del tmp['limit']
            del tmp['offset']
        result = MovieResource.get_by_template('*', {'guid': guid}, limit, offset)
        if result:
            rsp = Response(json.dumps(result), status=200, content_type="application.json")
        else:
            rsp = Response("NOT FOUND", status=404, content_type="text/plain")
    elif request.method == "PUT":
        name = request.form['movie_name']
        category = request.form['category']
        year = request.form['year']
        rating = request.form['rating']
        if name is None or category is None or year is None or rating is None:
            flash("check your input")
            return redirect(url_for('movie_by_id'))
        try:
            result = MovieResource.update_movie(guid, name, category, year, rating)
            if result:
                rsp = Response(json.dumps(result), status=200, content_type="application.json")
            else:
                rsp = Response("NOT FOUND", status=404, content_type="text/plain")
        except:
            rsp = Response("NOT FOUND", status=404, content_type="text/plain")
    elif request.method == "DELETE":
        result = MovieResource.delete_movie(guid)
        if result:
            rsp = Response(json.dumps(result), status=200, content_type="application.json")
        else:
            rsp = Response("NOT FOUND", status=404, content_type="text/plain")
    else:
        rsp = Response("NOT IMPLEMENTED", status=501, content_type="text/plain")
    return rsp


@app.route("/api/movies/<guid>/<value>", methods=["GET"])
def get_value_by_id(guid, value):
    result = MovieResource.get_by_template([value], {'guid': guid})
    if result:
        rsp = Response(json.dumps(result), status=200, content_type="application.json")
    else:
        rsp = Response("NOT FOUND", status=404, content_type="text/plain")
    return rsp


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001)
