# Flask | Flask-SQLAlchemy Model Relationships

A simple example demonstrating the progression of adding relationships to SQLAlchemy models in a Flask project.

[Documentation for SQLAlchemy relationships](http://flask-sqlalchemy.pocoo.org/2.3/models/).

Relationship Coordinality Samples:

* One-to-One
* One-to-Many
* Many-to-Many

## One-to-One

One-to-One relationships are defined with a `db.relationship()` function. This is not a `Column`, but a function that manages the relationship between models to return the Python objects when the property is accessed.

The related object must have a `Column` for the `ForeignKey()`.

The `backref` attribute is providing a name for an attribute to attach to the related model to allow access both directions.

```python
# Access
director.guild # returns <Guild> object
guild.director # returns <Director> object

# Update Related Objects
director.guild = Guild(...) # sets the related <Guild> object to the new one
guild.director = Director(...) # sets the related <Director> object to the new one
db.session.commit() # persists changed models to the database
```

The only difference between a One-to-One and One-to-Many relationship is the use of the keyword argument `uselist` set to `False`.

```python
class Director(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    # ...
    guild = db.relationship(
        "GuildMembership", backref="director", lazy="select", uselist=False
    )

class GuildMembership(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    # ...
    direcotr_id = db.Column(db.Integer, db.ForeignKey("director.id"))
```

## One-to-Many

One-to-Many relationships are defined with a `db.relationship()` function. This is not a `Column`, but a function that manages the relationship between models to return the Python objects when the property is accessed.

The related object must have a `Column` for the `ForeignKey()`.

```python
class Movie(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    # ...
    director_id = db.Column(db.Integer, db.ForeignKey("director.id"))
    # ...

class Director(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    # ...
    movies = db.relationship(
        "Movie", backref="director", lazy="joined"), lazy="select"
    )
    # ...
```

A One-to-Many relationship allows you to manipulate the related objects as native Python objects.

```python
# Access
director.movies # returns a list of <Movie> objects
for m in director.movies:
    print(m.title)

movie.director # returns <Director> object
movie.director.guild.name # traverses related objects to access nested data

# Update Related Objects
m = Movie(...)
d = Director(...)

db.session.add(m)
db.session.add(d)

director.movies.append(m) # adds related <Movie> object to the list of movies
movie.director = d # sets the related <Director> object to the new one
db.session.commit() # persists changed models to the database
```

## Many-to-Many

Many-to-Many relationships are defined with a `db.relationship()` function. This is not a `Column`, but a function that manages the relationship between models to return the Python objects when the property is accessed.

The related object does *not* have a `Column` for the `ForeignKey()`.

Instead, a join table is needed to maintain the relationship by defining a `Table`.

```python
actors = db.Table(
    "actors",
    db.Column("actor_id", db.Integer, db.ForeignKey("actor.id")),
    db.Column("movie_id", db.Integer, db.ForeignKey("movie.id")),
)

class Movie(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    # ...
    actors = db.relationship("Actor", secondary=actors, backref="movies", lazy="select")
    # ...

class Actor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    # ...
```

A Many-to-Many relationship allows you to manipulate the related objects as native Python objects.

```python
# Access
actor.movies # returns a list of <Movie> objects
for m in actor.movies:
    print(m.title)

movie.actors # returns a list of <Actor> objects
for a in movie.actors:
    print(a.first_name)

# Update Related Objects
m = Movie(...)
a = Actor(...)

db.session.add(m)
db.session.add(a)

actor.movies.append(m) # adds related <Movie> object to the list of movies
movie.actors.append(d) # adds related <Actor> object to the list of actors
db.session.commit() # persists changed models to the database
```
