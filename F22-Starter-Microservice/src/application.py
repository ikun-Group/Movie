from flask import Flask, Response, request, jsonify, render_template, redirect, url_for, flash, session
from datetime import datetime
import json
from movie_resource import MovieResource
from flask_cors import CORS
import copy
from rest_utils import RESTContext

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
    request_inputs = RESTContext(request, movies)
    if request_inputs.method == "GET":
        result = MovieResource.get_all(limit=request_inputs.limit, offset=request_inputs.offset)
        result = request_inputs.add_pagination(result)
        if result:
            rsp = Response(json.dumps(result), status=200, content_type="application.json")
        else:
            rsp = Response("NOT FOUND", status=404, content_type="text/plain")
        return rsp
    elif request.method == "POST":
        movie_profile = request.get_json()
        try:
            ret = MovieResource.create_movie(**movie_profile)
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
    else:
        return Response("Not implemented", status=501, content_type="text/plain")


@app.route("/api/movies/<guid>", methods=["GET", "PUT", "DELETE"])
def movie_by_id(guid):
    if request.method == "GET":
        result = MovieResource.get_by_template('*', {'guid': guid}, limit=None, offset=None)
        if result:
            rsp = Response(json.dumps(result), status=200, content_type="application.json")
        else:
            rsp = Response("NOT FOUND", status=404, content_type="text/plain")
    elif request.method == "PUT":
        movie_profile = request.get_json()
        if len(movie_profile) != 4:
            rsp = Response("input length not right", status=400, content_type="text/plain")
        else:
            try:
                result = MovieResource.update_movie(guid, **movie_profile)
                if result:
                    rsp = Response('Update successful', status=200, content_type="application.json")
                else:
                    rsp = Response("Update failed", status=404, content_type="text/plain")
            except Exception as e:
                rsp = Response('Error: {}'.format(str(e)), status=404, content_type="text/plain")
    elif request.method == "DELETE":
        try:
            result = MovieResource.delete_movie(guid)
            if result:
                rsp = Response('Delete successful', status=200, content_type="application.json")
            else:
                rsp = Response("Delete failed", status=404, content_type="text/plain")
        except Exception as e:
            rsp = Response('Error: {}'.format(str(e)), status=404, content_type="text/plain")
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
