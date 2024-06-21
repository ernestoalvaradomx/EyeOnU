from flask import Blueprint, request, jsonify
from src.frameprocessing.models.userTestModel import User
from src.util.database.db import db

testORM = Blueprint('testORM', __name__)

@testORM.route("/", methods=['GET'])
def home():
    return "Home"

@testORM.route('/users', methods=['GET'])
def listUser():
    users = User.query.all()
    usersList = [user.toJson() for user in users]
    return jsonify(usersList), 200

@testORM.route('/users/<int:idUser>', methods=['GET'])
def getUser(idUser):
    user = User.query.get(idUser)
    if user:
        return jsonify(user.toJson()), 200
    else:
        return jsonify({"error": "User not found"}), 404

@testORM.route("/users", methods=['POST'])
def createUser():
    if request.is_json:
        data = request.get_json()
        newUser = User(name=data['name'], 
                       lastName=data['lastName'],
                       age=data['age'])

        db.session.add(newUser)
        db.session.commit()

        return jsonify({"message": f"User {newUser.name} has been created successfully."}), 200
    else:
        return jsonify({"error": "The request body is not in JSON format"}), 400
    
@testORM.route('/users/<int:idUser>', methods=['PUT'])
def updateUser(idUser):
    user = User.query.get(idUser)
    if user:
        if request.is_json:
            data = request.get_json()
            if 'name' in data:
                user.name = data['name']
            if 'lastName' in data:
                user.lastName = data['lastName']
            if 'age' in data:
                user.age = data['age']
            db.session.commit()
            return jsonify({"message": f"User {user.name} has been updated successfully."}), 200
        else:
            return jsonify({"error": "The request payload is not in JSON format"}), 400
    else:
        return jsonify({"error": "User not found"}), 404
    
@testORM.route('/users/<int:idUser>', methods=['DELETE'])
def deleteUser(idUser):
    user = User.query.get(idUser)
    if user:
        db.session.delete(user)
        db.session.commit()
        return jsonify({"message": "User has been deleted successfully."}), 200
    else:
        return jsonify({"error": "User not found"}), 404
