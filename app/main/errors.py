from flask import render_template
from app import db
from . import main


@main.app_errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@main.app_errorhandler(500)
def page_not_found(e):
    db.session.rollback()
    return render_template('500.html'), 500
