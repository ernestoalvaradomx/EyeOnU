from flask import Blueprint, request,  jsonify

import src.services.testORMService as testORMService

testORMRoute = Blueprint('testORMRoute', __name__)

@testORMRoute.route("/", methods=['GET'])
def home():
    return jsonify({'message': 'Home'}), 200

@testORMRoute.route('/users', methods=['GET'])
def listUser():
    return testORMService.listUser()
    
@testORMRoute.route('/users/<int:idUser>', methods=['GET'])
def getUser(idUser):
    return testORMService.getUser(idUser)

@testORMRoute.route("/users", methods=['POST'])
def createUser():
    return testORMService.createUser(request)
     
@testORMRoute.route('/users/<int:idUser>', methods=['PUT'])
def updateUser(idUser):
    return testORMService.updateUser(idUser, request)
    
@testORMRoute.route('/users/<int:idUser>', methods=['DELETE'])
def deleteUser(idUser):
    return testORMService.deleteUser(idUser)