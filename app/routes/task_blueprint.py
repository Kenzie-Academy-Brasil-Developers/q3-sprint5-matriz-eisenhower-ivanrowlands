from flask import Blueprint
from app.controllers.task_controller import create_task, delete_task, update_task

bp_task = Blueprint("bp_task", __name__, url_prefix="/tasks")
bp_task.post("")(create_task)
bp_task.patch("<id>")(update_task)
bp_task.delete("<id>")(delete_task)