from flask_sqlalchemy import SQLAlchemy
from flask import Flask
from os import getenv

db = SQLAlchemy()

def init_app(app: Flask):
    
    app.config["SQLALCHEMY_DATABASE_URI"] = getenv("SQLALCHEMY_DATABASE_URI")
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["JSON_SORT_KEYS"] = False

    db.init_app(app)
    app.db = db

    from app.models.categories_models import CategoriesModel
    from app.models.task_model import TaskModel
    from app.models.eisenhower_model import EisenhowerModel
    from app.models.tasks_categories import TasksCategories

    