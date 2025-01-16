from flask import Blueprint

from controllers.user_controller import user_register

user_bp = Blueprint("user_routes", __name__)


@user_bp.route("/users", methods=["POST"])
def users():
    return user_register()
