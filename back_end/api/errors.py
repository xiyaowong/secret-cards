from flask import jsonify
from werkzeug.http import HTTP_STATUS_CODES

from back_end.api import api_bp
from back_end.models import db


def error_response(status_code, message=None):
    payload = {'error': HTTP_STATUS_CODES.get(status_code, 'Unknown error')}
    if message:
        payload['message'] = message
    response = jsonify(payload)
    response.status_code = status_code
    return response


def bad_request(message):
    return error_response(400, message)


@api_bp.app_errorhandler(404)
def not_found_error(error):
    return error_response(404)


@api_bp.app_errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return error_response(500)