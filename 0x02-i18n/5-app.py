#!/usr/bin/env python3
"""flask simple app"""
from flask import Flask, render_template, request, g
from flask_babel import Babel, _


users = {
    1: {"name": "Balou", "locale": "fr", "timezone": "Europe/Paris"},
    2: {"name": "Beyonce", "locale": "en", "timezone": "US/Central"},
    3: {"name": "Spock", "locale": "kg", "timezone": "Vulcan"},
    4: {"name": "Teletubby", "locale": None, "timezone": "Europe/London"},
}

app = Flask(__name__)


class Config:
    """config class"""
    LANGUAGES = ['en', 'fr']
    BABEL_DEFAULT_LOCALE = 'en'
    BABEL_DEFAULT_TIMEZONE = 'UTC'


app.config.from_object(Config)
babel = Babel(app)


def get_user():
    """get user function"""
    user_id = request.args.get('login_as')
    if user_id is None:
        return None
    return users.get(int(user_id))


@app.before_request
def before_request():
    """before request"""
    current_user = get_user()
    if current_user is not None:
        g.user = current_user


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
    user = g.get('user')
    if user is None:
        message = _('not_logged_in')
    else:
        message = _("logged_in_as", username=user['name'])
    return render_template(
            '5-index.html', home_title=home_title,
            home_header=home_header, user=user,
            message=message)


if __name__ == "__main__":
    """ Main Function """
    app.run(host='0.0.0.0', port=5000)
