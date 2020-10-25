import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy
from app import create_app
from models import setup_db, Actors, Movies

DB_HOST = os.getenv('DB_HOST', '127.0.0.1:5432')
DB_USER = os.getenv('DB_USER', 'postgres')
DB_PASSWORD = os.getenv('DB_PASSWORD', '123')
DB_NAME = os.getenv('DB_NAME', 'Agency')
database_path = 'postgresql://{}:{}@{}/{}'.format(DB_USER, DB_PASSWORD, DB_HOST, DB_NAME)

new_movie = {
    'title': 'Kingsman The Gold Ring',
    'genre': 'Action',
    'release_date': '2013.07.25'
}

new_actor = {
    'name': 'John Doe',
    'age': '26',
    'role': 'Misterious',
    'gender': 'Male'
}


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_path = database_path
        setup_db(self.app, self.database_path)
        self.assistance_token = 'Bearer' + str(os.getenv('assistant'))
        self.director_token = 'Bearer' + str(os.getenv('director'))
        self.producer_token = 'Bearer' + str(os.getenv('producer'))

        self.assistant = {'Authorization': self.assistance_token}
        self.director = {'Authorization': self.director_token}
        self.producer = {'Authorization': self.producer_token}
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            self.db.create_all()


    def tearDown(self):
        pass

    def test_get_movies(self):
        res = self.client().get('/movies', headers=self.assistant)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['movies'])
        self.assertTrue(data['len_movies'])

    def test_get_movies_id(self):
        res = self.client().get('/movies/2', headers=self.producer)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['movies'])

    def test_post(self):
        res = self.client().get('/movies', json=new_movie, headers=self.producer)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['message'], 'The Movie is successfully created')

    def test_post_m_invalid(self):
        new_error = {
            'title': 'Gentlemen',
            'genre': 'Fantasy'
        }
        res = self.client().post('/movies', json=new_error, headers=self.producer)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "Unprocessable Request")

    def test_delete_m_by_id(self):
        res = self.client().delete('/movies/5', headers=self.producer)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['message'])

    def test_invalid_delete_movies(self):
        res = self.client().delete('/movies/makhmud', headers=self.producer)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Not Found')

    def test_search_movie(self):
        search_item = {'searchTerm': 'h'}
        res = self.client().post('/movies/search', json=search_item, headers=self.producer)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['movies'])
        self.assertTrue(data['len_movies'])

    def test_search_movie_invalid(self):
        new_search = {'searchTerm': ''}
        res = self.client().post('/movies/search', json=new_search, headers=self.producer)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "Not Found")

    def test_patch_movie(self):
        patch_t = {'title': 'John Wick'}
        res = self.client().patch('/movies/4', json=patch_t, headers=self.producer)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['message'], 'The Movie Successfully updated!')

    def test_patch_movie_invalid(self):
        patch_t = {'err_title': 'Hello'}
        res = self.client().patch('/movies/4', json=patch_t, headers=self.producer)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "Unprocessable Request")

    def test_get_actors(self):
        res = self.client().get('/actors', headers=self.producer)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['actors'])
        self.assertTrue(data['len_actors'])

    def test_actors_by_using_id(self):
        res = self.client().get('/actors/2', headers=self.producer)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['actors'])

    def test_post_actors(self):
        res = self.client().get('/actors', json=new_actor, headers=self.director)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['message'], 'The Actor is successfully created')

    def test_post_actors_invalid(self):
        new_a_error = {
            'name': 'Jhonme',
            'age': '57'
        }
        res = self.client().post('/actors', json=new_a_error, headers=self.producer)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "Unprocessable Request")

    def test_delete_actor_by_id(self):
        res = self.client().delete('/actors/3', headers=self.producer)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['message'], 'The Actors is successfully deleted')

    def test_invalid_delete_actors(self):
        res = self.client().delete('/actors/me', headers=self.producer)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Not Found')

    def test_search_actor(self):
        search_item = {'searchTerm': 'a'}
        res = self.client().post('/actors/search', json=search_item, headers=self.producer)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['actors'])
        self.assertTrue(data['len_actors'])

    def test_search_actor_invalid(self):
        new_search = {'searchTerm': ''}
        res = self.client().post('/actors/search', json=new_search, headers=self.producer)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "Not Found")

    def test_patch_actor(self):
        patch_title = {'name': 'mac book pro'}
        res = self.client().patch('/actors/1', json=patch_title, headers=self.producer)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['message'], 'The Actor Successfully updated!')

    def test_patch_actor_invalid(self):
        patch_t = {'error_a_name': 'Hello'}
        res = self.client().patch('/actors/1', json=patch_t, headers=self.producer)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "Unprocessable Request")

if __name__ == "__main__":
    unittest.main()
