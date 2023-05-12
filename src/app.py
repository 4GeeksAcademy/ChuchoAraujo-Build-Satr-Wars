"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User, People, Planet, Favorite
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False

db_url = os.getenv("DATABASE_URL")
if db_url is not None:
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url.replace("postgres://", "postgresql://")
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:////tmp/test.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

#########################################################  USERS #############################################################################################

#------------------------------- GET USERS -------------------------------
@app.route('/users', methods=['GET'])
def get_all_users():

    users = User.query.all()
    serialized_users = [user.serialize() for user in users]

    return jsonify(serialized_users), 200

#------------------------------- GET USER/ID -------------------------------
@app.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id):

    user = User.query.get(user_id)
    serialized_user = user.serialize()

    return jsonify(serialized_user), 200

#------------------------------- POST USERS -------------------------------
@app.route('/users', methods=['POST'])
def create_user():
    body = request.get_json()
    new_user = User(email = body['email'], password = body['password'])
    db.session.add(new_user)
    db.session.commit()

    response_body = {
        "msg": "User created successfully", 
        "user": user.serialize()
    }

    return jsonify(response_body), 200

#------------------------------- DELETE USERS -------------------------------

@app.route('/users/<int:user_id>', methods= ['DELETE'])
def delete_user(user_id):
    user = User.query.get(user_id)
    db.session.delete(user)
    db.session.commit()

    response_body = {
        "msg": "User deleted", 
        "user": user.serialize()
    }

    return jsonify(response_body)


#########################################################  PEOPLE #############################################################################################

#------------------------------- GET PEOPLE -------------------------------
@app.route('/people', methods=['GET'])
def get_all_people():

    people = People.query.all()
    serialized_people = [p.serialize() for p in people]

    return jsonify(serialized_people), 200


#------------------------------- GET USER/ID -------------------------------
@app.route('/people/<int:people_id>', methods=['GET'])
def get_people(people_id):

    people = People.query.get(people_id)
    serialized_people = people.serialize()

    return jsonify(serialized_people), 200

#------------------------------- POST PEOPLE -------------------------------
@app.route('/people', methods=['POST'])
def create_people():
    body = request.get_json()
    new_people = People(name = body['name'], description = body['description'])
    db.session.add(new_people)
    db.session.commit()

    response_body = {
        "msg": "People created successfully", 
        "people": new_people.serialize()
    }

    return jsonify(response_body), 200


#------------------------------- DELETE USERS -------------------------------

@app.route('/people/<int:people_id>', methods= ['DELETE'])
def delete_people(people_id):
    people = People.query.get(people_id)
    db.session.delete(people)
    db.session.commit()

    response_body = {
        "msg": "people deleted", 
        "people": people.serialize()
    }

    return jsonify(response_body)



















# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
