from flask import Flask, render_template
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


actors = db.Table(
    "actors",
    db.Column("actor_id", db.Integer, db.ForeignKey("actor.id")),
    db.Column("movie_id", db.Integer, db.ForeignKey("movie.id")),
)


class Movie(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255))
    director_id = db.Column(db.Integer, db.ForeignKey("director.id"))
    release_date = db.Column(db.DateTime)
    actors = db.relationship("Actor", secondary=actors, backref="movies", lazy="select")

    def release_year(self):
        return self.release_date.strftime("%Y")

    # def actor_list(self):
    #     return self.actors.split(',')


class Director(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(255))
    last_name = db.Column(db.String(255))
    movies = db.relationship(
        "Movie", backref=db.backref("director", lazy="joined"), lazy="select"
    )
    guild = db.relationship(
        "GuildMembership", backref="director", lazy="select", uselist=False
    )


# m = Movie(...)
# m.director.first_name


class Actor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(255))
    last_name = db.Column(db.String(255))
    guild = db.relationship(
        "GuildMembership", backref="actor", lazy="select", uselist=False
    )


class GuildMembership(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    guild = db.Column(db.String(255))
    direcotr_id = db.Column(db.Integer, db.ForeignKey("director.id"))
    actor_id = db.Column(db.Integer, db.ForeignKey("actor.id"))


@app.route("/")
def hello():
    movie = db.session.query(Movie).first()
    return render_template('movie.html', movie=movie)


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
        title="Evil Dead", release_date=datetime.strptime("Oct 15 1981", "%b %d %Y")
    )

    db.session.add(m)
    d = Director(
        first_name="Sam", last_name="Raimi", guild=GuildMembership(guild="Raimi DGA")
    )
    m.director = d

    db.session.add(d)

    bruce = Actor(
        first_name="Bruce",
        last_name="Campbell",
        guild=GuildMembership(guild="Campbell SAG"),
    )
    ellen = Actor(
        first_name="Ellen",
        last_name="Sandweiss",
        guild=GuildMembership(guild="Sandweiss SAG"),
    )
    hal = Actor(
        first_name="Hal",
        last_name="Delrich",
        guild=GuildMembership(guild="Delrich SAG"),
    )
    betsy = Actor(
        first_name="Betsy", last_name="Baker", guild=GuildMembership(guild="Baker SAG")
    )
    sarah = Actor(
        first_name="Sarah", last_name="York", guild=GuildMembership(guild="York SAG")
    )

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
