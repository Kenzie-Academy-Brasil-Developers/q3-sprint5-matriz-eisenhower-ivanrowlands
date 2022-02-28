from flask import Blueprint
from app.controllers.get_controller import get

bp_get = Blueprint("bp_get", __name__, url_prefix="/")
bp_get.get("")(get)