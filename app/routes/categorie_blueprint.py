from flask import Blueprint
from app.controllers.categories_controller import create_categorie, delete_categorie, update_categorie

bp_categorie = Blueprint("bp_categorie", __name__, url_prefix="/categories")
bp_categorie.post("")(create_categorie)
bp_categorie.patch("/<id>")(update_categorie)
bp_categorie.delete("<id>")(delete_categorie)