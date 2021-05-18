from flask import Blueprint, render_template
from flask_login import login_required

home_bp = Blueprint('home_bp', __name__, template_folder='templates/home')


@home_bp.route('/')
def index():
    return render_template('index.html')


@home_bp.route('/intro')
def intro():
    return render_template('intro.html')


@home_bp.route('/outro')
def outro():
    return render_template('outro.html')
