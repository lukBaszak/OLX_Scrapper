import json
import datetime
from flask import Blueprint, request, Response
import redis

from flaskr.scrapper_utils.scrapper import ScrapperService

db = redis.Redis(host='redis', port=6379)

bp = Blueprint('scrapper', __name__, url_prefix='/scrapper')

@bp.route('/latest_url', methods=['GET'])
def get_latest_url():

    return db.lpop('links')

@bp.route('/add_data', methods=['POST'])
def add_scrapper_data():

    data = json.loads(request.data)
    url = data.pop("url")
    db.hmset(f"{datetime.datetime.today().strftime('%Y-%m-%d')}:{url}", data)


    return Response(data, status=200)


@bp.route('/update_list', methods=['GET'])
def update_url_list():
    service = ScrapperService()
    service.fill_urls_list()

    return Response(status=200)