from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), unique=False, nullable=False)

    favorites = db.relationship('Favorite', backref='user', lazy=True)

    def __repr__(self):
        return '<User %r>' % self.email

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            "favorites": [fav.serialize() for fav in self.favorites]
        }


class Planet(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    climate = db.Column(db.String(80))
    terrain = db.Column(db.String(80))

    def __repr__(self):
        return f'<Planet {self.name}>'

    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'climate': self.climate,
            'terrain': self.terrain
        }

class People(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    description = db.Column(db.String(280))

    def __repr__(self):
        return f'<People {self.name}>'

    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
        }

class Favorite(db.Model):
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    planet_id = db.Column(db.Integer, db.ForeignKey('planet.id'), nullable=True)
    people_id = db.Column(db.Integer, db.ForeignKey('people.id'), nullable=True)
    
    planet = db.relationship('Planet')
    people = db.relationship('People')

    def __repr__(self):
        return f'<Favorite {self.user_id}>'

    def serialize(self):
        return {
            'user_id': self.user_id,
            'planet': self.planet.serialize() if self.planet else None,
            'people': self.people.serialize() if self.people else None
        }


