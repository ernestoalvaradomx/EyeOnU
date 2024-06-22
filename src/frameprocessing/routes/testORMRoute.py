from flask import Blueprint, request,  jsonify

import src.frameprocessing.services.testORMService as frameprocessingService

testORMRoute = Blueprint('testORMRoute', __name__)

@testORMRoute.route("/", methods=['GET'])
def home():
    return jsonify({'message': 'Home'}), 200

@testORMRoute.route('/users', methods=['GET'])
def listUser():
    return frameprocessingService.listUser()
    
@testORMRoute.route('/users/<int:idUser>', methods=['GET'])
def getUser(idUser):
    return frameprocessingService.getUser(idUser)

@testORMRoute.route("/users", methods=['POST'])
def createUser():
    return frameprocessingService.createUser(request)
     
@testORMRoute.route('/users/<int:idUser>', methods=['PUT'])
def updateUser(idUser):
    return frameprocessingService.updateUser(idUser, request)
    
@testORMRoute.route('/users/<int:idUser>', methods=['DELETE'])
def deleteUser(idUser):
    return frameprocessingService.deleteUser(idUser)