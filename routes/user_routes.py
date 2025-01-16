from flask import Blueprint

from controllers.user_controller import user_login, user_register

user_bp = Blueprint("user_routes", __name__)


@user_bp.route("/usersregister", methods=["POST"])
def register():
    return user_register()


@user_bp.route("/userlogin", methods=["POST"])
def login():
    return user_login()
