from flask import Flask, jsonify, abort, make_response, request
from flask_sqlalchemy import SQLAlchemy

from app import TAGS_MODEL

app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)


@app.errorhandler(400)
def bad_request(error):
    return make_response(jsonify({'error': 'Bad Request'}), 400)


@app.route('/api/v1.0/search_tags', methods=['POST'])
def get_files():
    print(request.json)
    tags = TAGS_MODEL.search_tags_in_text(request.json["text"])
    return jsonify({"tags": tags})


if __name__ == '__main__':
    app.run(debug=True)
