import os

import redis
from flask import Flask
from flask.ext.cors import CORS

import api.views
from extract import URLExtractor


def create_app(redis_client=None):
    app = Flask(__name__)
    CORS(app)

    embedly_url = 'https://api.embedly.com/1/extract'
    embedly_key = os.environ.get('EMBEDLY_KEY', None)

    redis_timeout = 24 * 60 * 60  # 24 hour timeout
    redis_url = os.environ.get('REDIS_URL', None)
    app.redis_client = redis_client or redis.StrictRedis(
        host=redis_url, port=6379, db=0)

    app.extractor = URLExtractor(
        embedly_url,
        embedly_key,
        app.redis_client,
        redis_timeout,
    )

    app.config['VERSION_INFO'] = ''
    if os.path.exists('./version.json'):  # pragma: no cover
        with open('./version.json') as version_file:
            app.config['VERSION_INFO'] = version_file.read()

    app.register_blueprint(api.views.blueprint)

    return app