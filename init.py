import os


def fetch_app_path():
    application_path = os.path.abspath(os.path.dirname(__file__))
    return application_path


def fetch_default_config_path():
    return fetch_app_path() + '/helper/config.ini'


def fetch_pyfolio_template_path():
    return fetch_app_path() + '/helper/report.html'
