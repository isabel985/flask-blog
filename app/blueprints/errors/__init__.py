from flask import Blueprint

errors = Blueprint('error', __name__)

from . import handlers