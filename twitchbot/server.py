# -*- coding: utf-8 -*-
import dotenv
import flask
import os
import redis


dotenv.load_dotenv(dotenv.find_dotenv())


def create_app():
    app = flask.Flask(__name__)
    r = redis.Redis(decode_responses=True)

    channel = os.environ.get('TWITCH_CHANNEL')

    def parse_messages():
        stats = r.zrevrange(channel, 0, 21, withscores=True)
        return [{'term': w, 'ocurrencies': o} for w, o in stats]

    @app.context_processor
    def inject_vars():
        return {'channel': channel}

    @app.route('/', methods=['GET'])
    def index():
        return flask.render_template('index.html')

    @app.route('/stream', methods=['GET'])
    def stream():
        return flask.jsonify(parse_messages())

    return app


if __name__ == '__main__':
    app = create_app()
    app.run()
