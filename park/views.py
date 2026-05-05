
from flask import Blueprint, render_template

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    return render_template('index.html')

@main_bp.route('/attractions')
def attractions():
    return render_template('attractions.html')

@main_bp.route('/buy_ticket')
def buy_ticket():
    return render_template('buy_ticket.html')