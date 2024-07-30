#!/usr/bin/env python3
"""flask simple app"""
from flask import Flask, render_template, request, g
from flask_babel import Babel, _
import pytz
from pytz.exceptions import UnknownTimeZoneError
from datetime import datetime

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
    locale_url = request.args.get('locale')

    if locale_url in app.config['LANGUAGES']:
        return locale_url
    if g.get('user') is not None:
        locale_set = g.get('user').get('locale')
        if locale_set in app.config['LANGUAGES']:
            return locale_set

    return request.accept_languages.best_match(app.config['LANGUAGES'])


@babel.timezoneselector
def get_timezone() -> str:
    """time funcy=tion"""
    timezone = request.args.get('timezone')
    if timezone:
        try:
            pytz.timezone(timezone)
            return timezone
        except UnknownTimeZoneError:
            pass

    if g.get('user') is not None:
        user_timezone = g.get('user').get('timezone')
        if user_timezone:
            try:
                pytz.timezone(user_timezone)
                return user_timezone
            except UnknownTimeZoneError:
                pass

    return app.config['BABEL_DEFAULT_TIMEZONE']


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

    timezone = get_timezone()
    tz = pytz.timezone(timezone)
    current = datetime.now(tz).strftime('%b %d, %Y, %I:%M:%S %p')
    time_mesg = _("current_time_is", current_time=current)
    return render_template(
            'index.html', home_title=home_title,
            home_header=home_header, user=user,
            message=message, current_time=time_mesg)


if __name__ == "__main__":
    """ Main Function """
    app.run(host='0.0.0.0', port=5000)
