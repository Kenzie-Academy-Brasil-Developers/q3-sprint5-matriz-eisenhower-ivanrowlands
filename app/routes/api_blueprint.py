from flask import Blueprint

from app.routes.categorie_blueprint import bp_categorie
from app.routes.task_blueprint import bp_task
from app.routes.get_blueprint import bp_get

bp_api = Blueprint("bp_api", __name__)

bp_api.register_blueprint(bp_categorie)
bp_api.register_blueprint(bp_task)
bp_api.register_blueprint(bp_get)