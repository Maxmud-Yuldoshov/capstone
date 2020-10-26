import os
from sqlalchemy import Column, String, Boolean, Integer, DateTime, ForeignKey
from flask_sqlalchemy import SQLAlchemy

DB_HOST = os.getenv('DB_HOST', '127.0.0.1:5432')
DB_USER = os.getenv('DB_USER', 'postgres')
DB_PASSWORD = os.getenv('DB_PASSWORD', '123')
DB_NAME = os.getenv('DB_NAME', 'CastingAgency')
database_path = 'postgresql://{}:{}@{}/{}'.format(
    DB_USER, DB_PASSWORD, DB_HOST, DB_NAME
)
db = SQLAlchemy()


def setup_db(app, database_path=database_path):
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)


def db_create_all():
    db.create_all()


class Actors(db.Model):
    __tablename__ = 'Actors'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    age = Column(String)
    role = Column(String)
    gender = Column(String)

    def __init__(self, id, name, age, role, gender):
        self.id = id
        self.name = name
        self.age = age
        self.role = role
        self.gender = gender

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def format(self):
        return {
            'id': self.id,
            'name': self.name,
            'age': self.age,
            'role': self.role,
            'gender': self.gender
        }


class Movies(db.Model):
    __tablename__ = 'Movies'
    id = Column(Integer, primary_key=True)
    title = Column(String)
    genre = Column(String)
    release_date = Column(String)

    def __init__(self, title, genre, release_date):
        self.title = title
        self.genre = genre
        self.release_date = release_date

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def format(self):
        return {
            'id': self.id,
            'title': self.title,
            'genre': self.genre,
            'release_date': self.release_date
        }
