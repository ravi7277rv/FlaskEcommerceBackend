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
        return (
            jsonify({"message": "User register successfully....", "data": newUser}),
            201,
        )

    except Exception as e:
        db.rollback()
        return (jsonify({"message": "Internal Server Error", "error": str(e)}), 500)
