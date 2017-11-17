# -*- coding: utf-8 -*-

from flask import Flask, render_template, jsonify
import redis
import sys


app = Flask(__name__)
r = redis.Redis(decode_responses=True)

channel = sys.argv[1]

def parse_messages():
    stats = r.zrevrange(channel, 0, 21, withscores=True)
    return [{ 'term': w, 'ocurrencies': o } for w, o in stats]

@app.context_processor
def inject_user():
    return dict(channel=channel)

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/stream', methods=['GET'])
def stream():
    return jsonify(parse_messages())

if __name__ == '__main__':
    app.run(debug=True)