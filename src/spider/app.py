#!flask/bin/python
import datetime
from flask import Flask, jsonify, json
from flask import abort
from flask import make_response
from flask import request
# from flask import url_for
# from flask_httpauth import HTTPBasicAuth
import pymongo
from scrapy.conf import settings
from NameCrawlerSpider.processData import *


app = Flask(__name__)

# auth = HTTPBasicAuth()

client = pymongo.MongoClient(settings['MONGODB_URI'])
db = client[settings['MONGODB_DB']]
collection = db[settings['MONGODB_COLLECTION']]
MAX = collection.find().count()

name_process = ProcessData([])

#
# @auth.get_password
# def get_password(username):
#     if username == 'ok':
#         return 'python'
#     return None
#
#
# @auth.error_handler
# def unauthorized():
#     return make_response(jsonify({'error': 'Unauthorized access'}), 401)


@app.route('/count', methods=['GET'])
def count():
    return jsonify({'count': MAX})


@app.route('/api/v1.0/peoples/<int:start>/<int:stop>', methods=['GET'])
# @auth.login_required
def get_peoples(start, stop):
    if start < 0 or stop > MAX:
        abort(404)
    peoples = collection.find(projection={'_id': False})[start:stop]
    data = []
    for people in peoples:
        data.append(people)
    return json.dumps(data, ensure_ascii=False)


@app.route('/api/v1.0/people/<name>', methods=['GET'])
def get_people(name):
    people = collection.find_one_and_update({'name': name}, {'$inc': {'search_count': 1}}, projection={'_id': False})
    if not (people):
        abort(404)
    return jsonify(people)


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)


@app.route('/api/v1.0/people/query', methods=['POST'])
def query_name():
    if not request.json or not 'name' in request.json:
        abort(400)
    name = request.json['name'].strip()
    name_exit = collection.find_one({'name': name})
    # print name_exit
    if name_exit:
        add_count_fields(name)
        # collection.update_one({'name': name}, {'$inc': {'search_count': 1}})
        return jsonify({'name.exit': True})
    else:
        status = name_process.is_name(name)
        if not status:
            return jsonify({'status': False, 'reason': "recognize people's name false"})
        else:
            collection.insert_one({'name': name, 'records': {'from': 'search'}})
            return jsonify({'status': True, 'reason': "success write in db"})


def add_count_fields(name):
    try:
        collection.update_one({'name': name}, {'$inc': {'search_count': 1}})
    except Exception, e:
        print "fail to add counts", e





if __name__ == '__main__':
    app.run(debug=True)
