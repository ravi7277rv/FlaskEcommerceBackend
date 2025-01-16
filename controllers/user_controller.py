from flask import jsonify, request
from flask_bcrypt import bcrypt

from databases.allTables import User
from databases.db import db


def user_register():
    try:
        if not request.is_json:
            return jsonify({"message": "Data is not a valid json"}), 400

        data = request.get_json()
        print(f"user data : {data}")
        if "username" not in data or "email" not in data or "password" not in data:
            return jsonify({"message": "Please provide the required data of user"}), 400

        existing_user = db.query(User).filter(User.email == data["email"]).first()
        if existing_user:
            return jsonify({"message": "User already exist with this email_Id"})
        encoded_password = data["password"].encode("utf-8")
        salt = bcrypt.gensalt()
        hashedPassword = bcrypt.hashpw(encoded_password, salt)
        newUser = User(
            username=data["username"], email=data["email"], password_hash=hashedPassword
        )
        print(f"hashed password : {hashedPassword}")
        db.add(newUser)
        db.commit()
        db.refresh(newUser)
        new_user_data = {
            "id": newUser.id,
            "username": newUser.username,
            "email": newUser.email,
            "first_name": newUser.first_name,
            "last_name": newUser.last_name,
            "date_of_birth": newUser.date_of_birth,
            "role": newUser.role,
            "is_active": newUser.is_active,
            "created_at": newUser.created_at,
            "updated_at": newUser.updated_at,
        }
        return (
            jsonify(
                {"message": "User register successfully....", "data": new_user_data}
            ),
            201,
        )
    except Exception as e:
        db.rollback()
        return (jsonify({"message": "Internal Server Error", "error": str(e)}), 500)


def user_login():
    try:
        if not request.is_json:
            return (jsonify({"message": "Not a valid json data"}), 400)
        data = request.get_json()
        if "email" not in data and "password" not in data:
            return (jsonify({"message": "Please enter your credentials"}), 400)
        existing_user = db.query(User).filter(User.email == data["email"]).first()
        if not existing_user:
            return (jsonify({"message": "User does not exist with this email_Id"}), 400)
        user_entered_password = data["password"].encode("utf-8")
        password_matched = bcrypt.checkpw(
            user_entered_password, existing_user.password_hash
        )
        if not password_matched:
            return (jsonify({"message": "Invalid credentials"}), 400)
        existing_user_data = {
            "id": existing_user.id,
            "username": existing_user.username,
            "email": existing_user.email,
            "first_name": existing_user.first_name,
            "last_name": existing_user.last_name,
            "date_of_birth": existing_user.date_of_birth,
            "role": existing_user.role,
            "is_active": existing_user.is_active,
            "created_at": existing_user.created_at,
            "updated_at": existing_user.updated_at,
        }
        return jsonify(
            {"message": "User loggedin successfully....", "data": existing_user_data}
        )
    except Exception as e:
        return (jsonify({"message": "Internal Server Error", "error": str(e)}), 500)
