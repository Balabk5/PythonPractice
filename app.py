
from flask import Flask, Blueprint, jsonify
from flask_cors import CORS
# from flask_pymongo import pymongo

from digiverz_portal_API.FlaskRestAPI import project_api_routes
from digiverz_portal_API.model_builder import model_builder_endpoint
from digiverz_portal_API.EDA import eda_endpoint

def create_app():
    web_app = Flask(__name__)  # Initialize Flask App
    CORS(web_app)

    api_blueprint = Blueprint('api_blueprint', __name__)
    api_blueprint = project_api_routes(api_blueprint)
    api_blueprint = model_builder_endpoint(api_blueprint)
    api_blueprint = eda_endpoint(api_blueprint)
    web_app.register_blueprint(api_blueprint, url_prefix='/api')    
    

    return web_app


app = create_app()

if __name__ == "__main__":
    app.run(host="0.0.0.0",debug=True)
