from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + os.path.join(
    app.root_path, "movies.db"
)
# Suppress deprecation warning
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)


actors = db.Table('actors',
    db.Column('actor_id', db.Integer, db.ForeignKey('actor.id')),
    db.Column('movie_id', db.Integer, db.ForeignKey('movie.id'))
)


class Movie(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255))
    director_id = db.Column(db.Integer, db.ForeignKey('director.id'))
    release_date = db.Column(db.DateTime)
    actors = db.relationship(
        'Actor', secondary=actors, backref='movies', lazy="select"
    )

    def release_year(self):
        return self.release_date.strftime("%Y")

    # def actor_list(self):
    #     return self.actors.split(',')


class Director(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(255))
    last_name = db.Column(db.String(255))
    movies = db.relationship(
        "Movie", backref=db.backref("director", lazy="joined"), lazy="select")

# m = Movie(...)
# m.director.first_name

class Actor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(255))
    last_name = db.Column(db.String(255))


class GuildMembership(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    guild = db.Column(db.String(255))


@app.route("/")
def hello():
    return "Hello World!"


@app.cli.command("initdb")
def reset_db():
    """Drops and Creates fresh database"""
    db.drop_all()
    db.create_all()

    print("Initialized default DB")


@app.cli.command("bootstrap")
def bootstrap_data():
    """Populates database with data"""
    db.drop_all()
    db.create_all()

    m = Movie(
            title="Evil Dead",
            release_date=datetime.strptime("Oct 15 1981", "%b %d %Y")
        )

    db.session.add(m)
    d = Director(first_name="Sam", last_name="Raimi")
    m.director = d

    db.session.add(d)

    bruce = Actor(first_name="Bruce", last_name="Campbell")
    ellen = Actor(first_name="Ellen", last_name="Sandweiss")
    hal = Actor(first_name="Hal", last_name="Delrich")
    betsy = Actor(first_name="Betsy", last_name="Baker")
    sarah = Actor(first_name="Sarah", last_name="York")

    db.session.add(bruce)
    db.session.add(ellen)
    db.session.add(hal)
    db.session.add(betsy)
    db.session.add(sarah)

    m.actors.extend((bruce, ellen, hal, betsy, sarah))

    db.session.commit()

    print("Added development dataset")


if __name__ == "__main__":
    app.run()
