from flask import Blueprint, request, jsonify
from src.models.userTestModel import User
from src.util.database.db import db

import src.services.frameProcessingService as frameProcessingService

frameProcessingRoute = Blueprint('frameProcessingRoute', __name__)

@frameProcessingRoute.route("/", methods=['GET'])
def home():
    return jsonify({'message': 'Home'}), 200