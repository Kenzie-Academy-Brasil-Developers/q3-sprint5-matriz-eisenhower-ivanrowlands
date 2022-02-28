from flask import jsonify

from app.models.categories_models import CategoriesModel
from app.models.task_model import TaskModel

def get():
	categories = CategoriesModel.query.all()
	result = []

	for item_category in categories:
		categories_data = {
			"id": item_category.id,
			"name": item_category.name,
			"description": item_category.description,
			"tasks": []
		}

		for item_task in item_category.tasks:
			importance = item_task.importance
			urgency = item_task.urgency	
			
			task_data  = {
				"id": item_task.id,
				"name": item_task.name,
				"description": item_task.description,
				"duration": item_task.duration,
				"classification": TaskModel.eisenhower_type(importance, urgency)
			}
			
			categories_data["tasks"].append(task_data)
		
		result.append(categories_data)
	
	return jsonify(result), 200