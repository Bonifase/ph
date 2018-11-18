import os
import json
import requests
from flask import Flask, render_template
from pusher_push_notifications import PushNotifications

pn_client = PushNotifications(
    instance_id=os.getenv('INSTANCE_ID'),
    secret_key=os.getenv('SECRET_KEY'),
)


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # a simple page that says hello

    @app.route('/', methods=['GET'])
    def hello():
        request = requests.get('http://poetrydb.org/author')
        authors = json.loads(request.text)['authors']
        return render_template('authors.html', authors=authors)

    @app.route('/author/<name>', methods=['GET'])
    def works(name):
        request = requests.get('http://poetrydb.org/author/{}'.format(name))
        works = json.loads(request.text)

        return render_template('authors_work.html', works=works)

    return app
