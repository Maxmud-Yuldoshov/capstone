# FSND-Capstone-Project
## WELCOME! To our Casting Agency!!!
This documentation is created for Casting Center!

https://makhmud-project-capstone.herokuapp.com/movies

Udacity Fullstack Nanodegree capstone project

Before installing requirements you need to configure Virtual Enviroment:
```
export FLASK_APP=app.py
export FLASK_ENV=development
flask run
```
- The Stack
- Python 3.8.2
- Flask - Web Framework
- SQLAlechmy ORM
- PostgresSQL
- Flask - Migrate
- RESTful - API
- Authentication - JSON Web Token (JWT) with Auth0
- User Roles/Permissions
- Python virtual environment - venv
- Python - unittest
- API testing with Postman
- Deployment on Heroku
## Getting Started

Install the necessary requirements by running:
    pip3 install -r requirements.txt
Running on local machine

Set up Authentication with Auth0.com. You need two roles with different permissions:

Endpoints

- GET '/movies'
- GET '/movies/id'
- POST '/movies/'
- PATCH '/movies/id'
- DELETE '/movies/id'
- GET '/actors'
GET '/actors/id'
POST '/actors/'
PATCH '/actors/id'
DELETE '/actors/id'

There are 8 types of Permissions and 3 types of Roles:
- `get:movies`
- `post:movies`
- `patch:movies`
- `delete:movies`
- `get:actors`
- `post:actors`
- `patch:actors`
- `delete:actors`
+  **and 3 Roles:**
    - Assistant
    - Director
    - Producer 
#### GET
- Returns
    ```
    {
        'success': True,
        'movies': [{
            "id": self.id,
            "title": self.title,
            "genre": self.genre,
            "release_date": self.release_date
            }, ...]
    }
    ```

## Movies
GET '/movies/<int:id>'
- Require permission `get:movies` or Role
- Can view to info
- Returns:
    ```
    {
        'success': True,
        'movies': [{
            "id": self.id,
            "title": self.title,
            "gender": self.gender,
            "release_date": self.release_date
            }]
        'len_movies': len_movies
    }
    ```
POST '/movies/'
- Required Authorization with 'Producer' role
- Requires Permission 
- Returns:
    {   
        'success': True,
        'message': 'The Movie successfully created!'
    }


PATCH '/movies/id'
- Required Authorization with 'Casting Producer' role
- Used tp update partially
- Required input (data type listed inside brackets):
    {
        "title": (string),
        "genre": (string)
        "release_date": (string)
    }
- Return
    {
        "success": True,
        "": "The Movie is Successfully Updated"
    }
DELETE '/movies/id'
- Required Authorization with 'Casting Producer' role
- Deletes the Movie with id replaced by id
- Returns Response if deletes successfully:
    {
        "success": True,
        "message": "The Movie is successfully Deleted"
    }
    
## Actors

GET '/movies/id'
- Require permission `get:actors` or Role
- Can view to info
- Returns:
    ```
    {
        'success': True,
        'actors': [{
            "id": self.id,
            "name": self.name,
            "age": self.age
            "role": self.role,
            "gender": self.gender
            }]
        'len_actors': len_actors
    }
    ```
POST '/actors/'
- Required Authorization with 'Producer' role
- Requires Permission 
- Returns:
    ```
    {   
        'success': True,
        'message': 'The Actors successfully created!'
    }
    ```

PATCH '/actors/id'
- Required Authorization with 'Casting Producer' role
- Used tp update partially
- Required input (data type listed inside brackets):
    ```
    {
        "name": (string),
        "age": (string),
        "gender": (string),
        "role": (string)
    }
    ```
- Return
    ```
    {   
        'success': True,
        'message': 'The Actors successfully updated!'
    }
    ```
DELETE '/actors/id'
- Required Authorization with 'Casting Producer' role
- Deletes the Actor with id replaced by id
- Returns Response if deletes successfully:
    ```
    {
        "success": True,
        "message": "The Actors is successfully Deleted"
    }
    ```  
    
__ERROR HANDLERS__

-   ```
    Error 422 (Unprocessable)
    Returns:
    {
      "success": False,
      "error": 422,
      "message": "Unprocessable Request"
    }
    ```

-   ```
    Error 404 (Bad Request)
    Returns:
    {
        "success": False,
        "error": 404,
        "message": "Not Found"
    }
    ```

-   ```
    Error 401 (Resource Not Found)
    Returns:
    {
        "success": False,
        "error": 401,
        "message": "Unauthorized"
    }
    ```
   

-   ```
     Error 400 (Unauthorized Error)
     Returns:
        {
            "success": False,
            "error": 400,
            "message": "Bad Request"
        }
     ```
        

