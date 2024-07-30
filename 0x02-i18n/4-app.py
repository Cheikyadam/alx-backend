#!/usr/bin/env python3
"""flask simple app"""
from flask import Flask, render_template, request
from flask_babel import Babel, _
app = Flask(__name__)


class Config:
    """config class"""
    LANGUAGES = ['en', 'fr']
    BABEL_DEFAULT_LOCALE = 'en'
    BABEL_DEFAULT_TIMEZONE = 'UTC'


app.config.from_object(Config)
babel = Babel(app)


@babel.localeselector
def get_locale():
    """best language"""
    locale = request.args.get('locale')

    if locale in app.config['LANGUAGES']:
        return locale
    return request.accept_languages.best_match(app.config['LANGUAGES'])


@app.route('/')
def index():
    """main route"""
    home_title = _('home_title')
    home_header = _('home_header')
    return render_template(
            '4-index.html', home_title=home_title,
            home_header=home_header)


if __name__ == "__main__":
    """ Main Function """
    app.run(host='0.0.0.0', port=5000)
