#!/usr/bin/env python3
"""Basic Flask app"""

from flask_babel import Babel, _
from flask import Flask, render_template, request, g


class Config:
    """Configuration class for Babel"""
    LANGUAGES = ['en', 'fr']
    BABEL_DEFAULT_LOCALE = "en"
    BABEL_DEFAULT_TIMEZONE = "UTC"


app = Flask(__name__)
app.url_map.strict_slashes = False
app.config.from_object(Config)


babel = Babel(app)


@babel.localeselector
def get_locale():
    """determine the best match with our supported languages"""
    req_locale = request.args.get('locale')
    if req_locale is not None:
        if req_locale in app.config['LANGUAGES']:
            return req_locale

    return request.accept_languages.best_match(app.config['LANGUAGES'])


users = {
    1: {"name": "Balou", "locale": "fr", "timezone": "Europe/Paris"},
    2: {"name": "Beyonce", "locale": "en", "timezone": "US/Central"},
    3: {"name": "Spock", "locale": "kg", "timezone": "Vulcan"},
    4: {"name": "Teletubby", "locale": None, "timezone": "Europe/London"},
}


def get_user(id: int):
    """returns a user dictionary or None if the ID cannot be found
    or if login_as was not passed.
    """
    return users.get(id)


@app.before_request
def before_request():
    """use get_user to find a user if any,
    and set it as a global on flask.g.user
    """
    user_id = request.args.get('login_as')
    try:
        g.user = get_user(int(user_id)) if user_id else None
    except ValueError as err:
        g.user = None


@app.route("/")
def index():
    """
    Outputs “Welcome to Holberton” as page title (<title>)
    and “Hello world” as header (<h1>)
    """
    return render_template('5-index.html', user=g.user)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
