from flask import Flask
from app.configs import migration, database
from app import routes

def create_app():
	app = Flask(__name__)

	database.init_app(app)
	migration.init_app(app)
	routes.init_app(app)	

	return app