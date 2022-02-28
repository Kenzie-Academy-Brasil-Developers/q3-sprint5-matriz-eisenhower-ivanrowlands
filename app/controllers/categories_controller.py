from app.models.categories_models import CategoriesModel
from sqlalchemy.orm.exc import UnmappedInstanceError
from sqlalchemy.exc import IntegrityError
from flask import jsonify, request
from app.configs.database import db

def create_categorie():
    data = request.get_json()
    keys = CategoriesModel.keys
    wrong_keys = list(data.keys() - keys)
    data["name"] = data["name"].title()
    try:
        category = CategoriesModel(**data)
        db.session.add(category)
        db.session.commit()
        return jsonify(category), 201
    
    except (KeyError, TypeError):
        return jsonify({"error": {"expected_keys": keys,"incoming_keys": wrong_keys}}), 400

    except IntegrityError:
        return ({"msg": "category already exists!"}), 409

def update_categorie(id):
    data = request.get_json()
    keys = CategoriesModel.keys
    wrong_keys = []
    
    for item in data.keys():
        if item not in keys:
            wrong_keys.append(item)

    if len(wrong_keys) > 0:
        return {"wrong_keys": wrong_keys}, 400

    try:
        category = CategoriesModel.query.get(id)

        for key, value in data.items():
            setattr(category, key, value)

        print(category)

        db.session.add(category)
        db.session.commit()
        
        return jsonify(category), 200

    except AttributeError:
        return  {"msg": "category not found!"}, 404
    
    except IntegrityError:
        return ({"msg": "category already exists!"}), 409

def delete_categorie(id):
    to_delete = CategoriesModel.query.get(id)

    try:
        db.session.delete(to_delete)
        db.session.commit()
    
    except UnmappedInstanceError:
        return {"msg": "category not found!"}, 404


    return "", 204