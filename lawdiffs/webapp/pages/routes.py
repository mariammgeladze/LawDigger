import logging
from flask import (render_template, request, flash, redirect, url_for, session,
    Blueprint)

logger = logging.getLogger(__name__)

blueprint = Blueprint('pages', __name__, template_folder='templates')


@blueprint.route('/view', defaults={'path': ''})
@blueprint.route('/view/<path:path>')
def view_route(path):
    return render_template('index.html')


@blueprint.route('/')
def index_route():
    return render_template('index.html')

