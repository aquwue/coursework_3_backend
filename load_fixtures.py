from sqlalchemy.exc import IntegrityError

from project.config import DevelopmentConfig
from project.dao.models import Genre, Director, Movie, User
from project.server import create_app
from project.setup_db import db
from project.utils import read_json

app = create_app(DevelopmentConfig)

data = read_json("fixtures.json")

with app.app_context():
    for genre in data["genres"]:
        db.session.add(Genre(id=genre["pk"], name=genre["name"]))

    for director in data["directors"]:
        db.session.add(Director(id=director["pk"], name=director["name"]))

    for movie in data["movies"]:
        db.session.add(Movie(id=movie["pk"], title=movie["title"], description=movie["description"], trailer=movie["trailer"], year=movie["year"], rating=movie["rating"], genre_id=movie["genre_id"], director_id=movie["director_id"],))

    # for user in data["users"]:
    #     db.session.add(User(id=user["pk"], email=user["email"], password=user["password"], name=user["name"], surname=user["surname"], favorite_genre=user["favorite_genre"]))

    try:
        db.session.commit()
    except IntegrityError:
        print("Fixtures already loaded")
