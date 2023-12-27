from src.apps.api.routes import BLUEPRINTS, API_PREFIX
from flask import Blueprint
from flask_restful import Api


def init_app(app):
    """Initialize blueprints"""

    def register_resources(api, resources_list):
        for resource, route in resources_list:
            api.add_resource(resource, route)

    for blueprint_name, blueprint_url, resources_list in BLUEPRINTS:
        blueprint = Blueprint(
            blueprint_name,
            __name__,
            url_prefix=f"{API_PREFIX}{blueprint_url}"
        )
        api = Api(blueprint)
        register_resources(api, resources_list)
        app.register_blueprint(blueprint)
