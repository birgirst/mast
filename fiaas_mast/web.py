import requests
from flask import current_app as app
from flask import url_for, jsonify, request, abort, Blueprint
from werkzeug.exceptions import UnprocessableEntity

from .deployer import Deployer
from .models import Release
from .status import status

web = Blueprint("web", __name__)


@web.route("/health", methods=["GET"])
def health_check():
    return jsonify("ok"), 200


@web.route("/deploy/", methods=["PUT", "POST"])
def deploy_handler():
    data = request.get_json(force=True)
    required_fields = ("application_name", "config_url", "image")
    errors = ["Missing key {!r} in input".format(key) for key in required_fields if key not in data]
    if errors:
        abort(UnprocessableEntity.code, errors)
    deployer = Deployer(get_http_client())
    namespace = app.config['NAMESPACE']
    application, deployment_id = deployer.deploy(namespace,
                                                 Release(data["image"], data["config_url"], data["application_name"]))
    response = status(namespace, application, deployment_id)
    return jsonify(response._asdict()), 201, {
        "Location": url_for("web.status_handler", _external=True, _scheme="https", namespace=namespace,
                            application=application,
                            deployment_id=deployment_id)}


@web.route("/status/<namespace>/<application>/<deployment_id>/", methods=["GET"])
def status_handler(namespace, application, deployment_id):
    response = status(namespace, application, deployment_id)
    return jsonify(response._asdict())


def get_http_client():
    http_client = requests.Session()
    http_client.auth = (app.config['ARTIFACTORY_USER'], app.config['ARTIFACTORY_PWD'])

    return http_client
