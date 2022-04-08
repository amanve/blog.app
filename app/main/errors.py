from flask import render_template
from . import main


@main.error_handler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@main.error_handler(500)
def page_not_found(e):
    return render_template('500.html'), 500
