from sqlalchemy import Column, String, Integer, Text
from sqlalchemy.orm import relationship
from dataclasses import dataclass

from app.configs.database import db

@dataclass
class CategoriesModel(db.Model):
	id: int
	name: str
	description: str
	
	keys = ["id", "name", "description"]
	__tablename__ = "categories"

	id = Column(Integer, primary_key=True)
	name = Column(String(100), nullable=False, unique=True)
	description = Column(Text)

	tasks = relationship("TaskModel", secondary="tasks_categories", backref="categories")