from flask import Blueprint, request, jsonify

from src.services.raw_frame_service import RawFrameService

rawFrameRoute = Blueprint('raw_frame_route', __name__)

@rawFrameRoute.route("/", methods=['GET'])
def get_frame():
    id_cam = request.args.get('id_cam')
    try:
        frame = RawFrameService.capture_frame(id_cam=id_cam)
        return jsonify(frame.toJson()), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
