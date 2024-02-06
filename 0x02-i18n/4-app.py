#!/usr/bin/env python3
"""Basic Flask app"""

from flask_babel import Babel
from flask import Flask, render_template, request


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


@app.route("/")
def index():
    """
    Outputs “Welcome to Holberton” as page title (<title>)
    and “Hello world” as header (<h1>)
    """
    return render_template('4-index.html')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
