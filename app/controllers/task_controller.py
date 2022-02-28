from flask import request, jsonify
from sqlalchemy.exc import PendingRollbackError

from app.exception.InvalidDataError import InvalidDataError
from app.models.categories_models import CategoriesModel
from app.models.eisenhower_model import EisenhowerModel
from app.models.task_model import TaskModel
from app.configs.database import db

def create_task():
    data = request.get_json()
    importance = data["importance"]
    urgency = data["urgency"]
    EisenhowerModel.create_eisenhower()

    data_keys = data.keys()
    keys = TaskModel.keys
    wrong_keys = data_keys - keys
    
    if len(wrong_keys) > 0:
        return {"error": f"wrong key: {wrong_keys}"}, 400

    try:
        data["name"] = data["name"].title()
        type_eisenhower = TaskModel.eisenhower_type(importance, urgency)
            
        eisenhower = EisenhowerModel.query.filter_by(type=type_eisenhower).first()
        data["eisenhower_id"] = eisenhower.id

        add_categories = data.pop("categories")

        task = TaskModel(**data)

        for item in add_categories:
            try:
                category = CategoriesModel.query.filter_by(name=item.title()).one()
                task.categories.append(category)

            except:
                new_category = CategoriesModel(name=item.title())
                db.session.add(new_category)
                db.session.commit()
                

                category = CategoriesModel.query.filter_by(name=item.title()).first()
                task.categories.append(category)


        db.session.add(task)
        db.session.commit()

        return jsonify({
            "id": task.id,
            "name": task.name,
            "description": task.description,
            "duration": task.duration,
            "classification": eisenhower.type,
            "categories": [category.name for category in task.categories]
        }), 201

    except (InvalidDataError) as e:
        return {"msg": e.__dict__["description"]}, 400

    except PendingRollbackError as e:
        name = data["name"]
        return jsonify({"error": f"name: {name}; already registered"}), 409
    
    except KeyError as e:
        return jsonify({
            "msg":{
                "valid_options": {
                    "importance": [1, 2],
                    "urgency": [1, 2]
                },
                "recieved_options":{
                    "importance": importance,
                    "urgency": urgency
                }
            }
        }), 400
    
def update_task(id):
    data  = request.get_json()
    data_keys = data.keys()
    keys = TaskModel.keys
    wrong_keys = data_keys - keys
    
    if len(wrong_keys) > 0:
        return {"error": f"wrong key: {wrong_keys}"}, 400

    try:
        task = TaskModel.query.get(id)
        
        if task == None:
            return {"error": "task not found!"}, 404

        for key, value in data.items():
            setattr(task, key, value)

        type_eisenhower = TaskModel.eisenhower_type(task.importance, task.urgency)
        eisenhower = EisenhowerModel.query.filter_by(type=type_eisenhower).first()
        data["eisenhower_id"] = eisenhower.id
        
        db.session.add(task)
        db.session.commit()


        return jsonify({
            "id": task.id,
            "name": task.name,
            "description": task.description,
            "duration": task.duration,
            "classification": eisenhower.type,
            "categories": [category.name for category in task.categories]
        }), 200

    except TypeError as e:
        return jsonify({
            "msg":{
                "valid_options": {
                    "importance": [1, 2],
                    "urgency": [1, 2]
                },
                "recieved_options":{
                    "importance": data["importance"],
                    "urgency": data["urgency"]
                }
            }
        }), 400

    except InvalidDataError as e :
        return {"error": e.args[0]}, 400

def delete_task(id):
    task_to_delete = TaskModel.query.get(id)

    if task_to_delete == None:
            return {"error": "task not found!"}, 404

    db.session.delete(task_to_delete)
    db.session.commit()

    return "", 204