from sqlalchemy import Column, ForeignKey, String, Integer, Text
from sqlalchemy.orm import validates
from dataclasses import dataclass

from app.configs.database import db
from app.exception.InvalidDataError import InvalidDataError

@dataclass
class TaskModel(db.Model):
    
    keys = ["name", "description", "duration", "importance", "urgency", "categories"]

    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False, unique=True)
    description = Column(Text)
    duration = Column(Integer)
    importance = Column(Integer)
    urgency = Column(Integer)
    
    eisenhower_id = Column(
        Integer, 
        ForeignKey("eisenhower.id")
    )

    @classmethod
    def eisenhower_type(cls, importance, urgency):

        eisenhower_dict = {
            (1, 1): "Do It First",
            (1, 2): "Delegate It",
            (2, 1): "Schedule It",
            (2, 2): "Delete It"
        }

        return eisenhower_dict[importance, urgency]

    @validates("importance", "urgency")
    def validade_importance_urgency(self, key, value):

        if type(value) != int:
            raise InvalidDataError(
                "Keys 'urgency' and 'importance' should be 'int'"
            )

        if value < 1 or value > 2:
            raise KeyError(
                description={
                    "valid_options": {
                        "importance": [1, 2],
                        "urgency": [1, 2]
                    },
                    "recieved_options":{
                        key: value
                    }
                }
                
            )
        return value