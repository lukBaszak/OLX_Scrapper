from flask import Blueprint, request, Response
import redis

from flaskr.scrapper_utils.scrapper import ScrapperService

db = redis.Redis(host='redis', port=6379)

bp = Blueprint('scrapper', __name__, url_prefix='/scrapper')

@bp.route('/latest_url', methods=['GET'])
def get_latest_url():
    if request.method == 'GET':
        return str(len(db.lrange('links', 0, -1)))

@bp.route('/update_list', methods=['GET'])
def update_url_list():
    service = ScrapperService()
    service.fill_urls_list()

    return Response("{'a':'OK'}", status=200, mimetype='application/json')