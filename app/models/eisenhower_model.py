from flask import session
from sqlalchemy import Column, String, Integer
from sqlalchemy.orm import relationship, backref
from app.configs.database import db
from dataclasses import dataclass

@dataclass
class EisenhowerModel(db.Model):
	id: int
	type: str
	
	__tablename__ = "eisenhower"

	id = Column(Integer, primary_key=True)
	type = Column(String(100))

	tasks = relationship("TaskModel", backref=backref("classification", uselist=False))

	@classmethod
	def create_eisenhower(cls):
		classification = ["Do It First", "Delegate It", "Schedule It", "Delete It"]
		eisenhower_value = EisenhowerModel.query.all()
		if not eisenhower_value:
			create_classification = []
			for item in classification:
				add_eisenhower = EisenhowerModel(**{"type": item})
				create_classification.append(add_eisenhower)
			db.session.add_all(create_classification)
			db.session.commit()