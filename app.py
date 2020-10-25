from flask import Flask, jsonify, request, abort
from flask_cors import CORS

from models import setup_db, db_create_all, Movies, Actors
from auth import requires_auth

list = 10


def create_app(test_config=None):
    app = Flask(__name__)
    setup_db(app)
    CORS(app)


    def movie_listing(request, selection):
        request = request.args.get('page', 1, type=int)
        start = (request - 1) * list
        end = start + list

        movies = [movie.format() for movie in selection]
        current_movies = movies[start:end]

        return current_movies


    def actor_listing(request, selection):
        request = request.args.get('page', 1, type=int)
        start = (request - 1) * list
        end = start + list

        actors = [actor.format() for actor in selection]
        current_actors = actors[start:end]

        return current_actors

    @app.after_request
    def after_request(response):
        response.headers.add(
            'Access-Control-Allow-Headers',
            'Content-type, Authorization'
        )
        response.headers.add(
            'Access-Control-Allow-Methods',
            'GET, POST, PATCH, DELETE, OPTIONS'
        )

        return response

    @app.route('/movies/<int:id>', methods=['GET'])
    @requires_auth('get:movies')
    def movie_by_id(id, token):
        try:
            movies = Movies.query.filter_by(id=id).all()
            all_movie = movie_listing(request, movies)

            return jsonify({
                'success': True,
                'movies': all_movie,
            })
        except Exception:
            abort(404)

    @app.route('/movies/search', methods=['POST'])
    def search_movie():
        data = request.get_json()
        answer = data.get('searchTerm', '')
        if answer == '':
            abort(404)
        try:
            movies = Movies.query.filter(
                Movies.title.ilike(f'%{answer}%')
            ).all()

            if len(movies) == 0:
                abort(404)
            all_movie = movie_listing(request, movies)

            return jsonify({
                'success': True,
                'movies': all_movie,
                'len_movies': len(movies)
            })
        except Exception:
            abort(404)

    @app.route('/movies')
    @requires_auth('get:movies')
    def get_movies(token):
        try:
            movies = Movies.query.order_by('id').all()
            all_movie = movie_listing(request, movies)

            return jsonify({
                'success': True,
                'movies': all_movie,
                'len_movies': len(movies)
            })
        except Exception:
            abort(404)

    @app.route('/movies', methods=['POST'])
    @requires_auth('post:movies')
    def add_movie(token):
        try:
            new_movie = request.get_json()

            title = new_movie.get('title')
            genre = new_movie.get('genre')
            release_date = new_movie.get('release_date')

            movie_add = Movies(
                title=title, genre=genre, release_date=release_date
            )
            movie_add.insert()

            return jsonify({
                'success': True,
                'message': 'The Movie is successfully created'
            })
        except Exception:
            abort(422)

    @app.route('/movies/<int:id>', methods=['DELETE'])
    @requires_auth('delete:movies')
    def delete_movie(token, id):
        try:
            movie = Movies.query.get(id)
            movies = Movies.query.all()
            all_movie = movie_listing(request, movies)

            movie.delete()

            return jsonify({
                'success': True,
                'message': 'The Movie is successfully deleted'
            })
        except Exception:
            abort(422)

    @app.route('/movies/<int:id>', methods=['PATCH'])
    @requires_auth('patch:movies')
    def patch_movies(token, id):
        try:
            patch_movie = request.get_json()

            movies = Movies.query.filter(Movies.id == id).one_or_none()
            if movies is None:
                abort(404)

            if 'title' in patch_movie:
                movies.title = str(patch_movie.get('title'))
            elif 'genre' in patch_movie:
                movies.genre = str(patch_movie.get('genre'))
            elif 'release_date' in patch_movie:
                movies.release_date = str(patch_movie.get('release_date'))

            movies.update()

            return jsonify({
                'success': True,
                'message': 'The Movie Successfully updated!'
            })
        except Exception:
            abort(422)

    @app.route('/actor/search', methods=['POST'])
    def search_actor():
        data = request.get_json()
        answer = data.get('searchTerm', '')
        if answer == '':
            abort(404)
        try:
            actors = Actors.query.filter(
                Actors.name.ilike(f'%{answer}%')
            ).all()

            if len(actors) == 0:
                abort(404)
            all_actor = actor_listing(request, actors)

            return jsonify({
                'success': True,
                'actors': all_actor,
                'len_actors': len(actors)
            })
        except Exception:
            abort(404)

    @app.route('/actors')
    @requires_auth('get:actors')
    def get_actors(token):
        try:
            actors = Actors.query.order_by('id').all()
            all_actor = actor_listing(request, actors)

            return jsonify({
                'success': True,
                'actors': all_actor,
                'len_actors': len(actors)
            })
        except Exception:
            abort(404)

    @app.route('/actors', methods=['POST'])
    @requires_auth('post:actors')
    def add_actor(token):
        try:
            new_actor = request.get_json()

            id = new_actor.get('id')
            name = new_actor.get('name')
            age = new_actor.get('age')
            role = new_actor.get('role')
            gender = new_actor.get('gender')

            actor_add = Actors(
                id=id, name=name, age=age, role=role, gender=gender
            )
            actor_add.insert()
            return jsonify({
                'success': True,
                'message': 'The Artist is successfully created'
            })
        except Exception:
            abort(422)

    @app.route('/actors/<int:id>', methods=['DELETE'])
    @requires_auth('delete:actors')
    def delete_actor(token, id):
        try:
            actor = Actors.query.get(id)
            actor.delete()

            return jsonify({
                'success': True,
                'message': 'The Actor is successfully deleted'
            })
        except Exception:
            abort(422)

    @app.route('/actors/<int:id>', methods=['PATCH'])
    @requires_auth('patch:actors')
    def patch_actors(token, id):
        try:
            patch_actor = request.get_json()

            actors = Actors.query.filter(Actors.id == id).one_or_none()
            if actors is None:
                abort(404)

            if 'name' in patch_actor:
                actors.name = str(patch_actor.get('name'))
            elif 'age' in patch_actor:
                actors.age = str(patch_actor.get('age'))
            elif 'role' in patch_actor:
                actors.role = str(patch_actor.get('role'))
            elif 'gender' in patch_actor:
                actors.gender = str(patch_actor.get('gender'))

            actors.update()

            return jsonify({
                'success': True,
                'message': 'The Actor Successfully updated!'
            })
        except Exception:
            abort(422)

    # error handlers
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            'success': False,
            'error': 404,
            'message': 'Not Found'
        }), 404

    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            'success': False,
            'error': 400,
            'message': 'Bad Request'
        }), 400

    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
            'success': False,
            'error': 422,
            'message': 'Unprocessable Request'
        }), 422

    @app.errorhandler(500)
    def method_not_allowed(error):
        return jsonify({
            'success': False,
            'error': 500,
            'message': 'Method Not Allowed'
        }), 500

    @app.errorhandler(401)
    def method_not_allowed(error):
        return jsonify({
            'success': False,
            'error': 401,
            'message': 'Unauthorized'
        }), 401

    return app


app = create_app()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
