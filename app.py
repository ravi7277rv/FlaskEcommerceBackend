from flask import Flask, jsonify

from routes.user_routes import user_bp

app = Flask("__name__")


@app.route("/", methods=["GET"])
def api_running():
    return jsonify({"message": "API is running successfully.....!"})


app.register_blueprint(user_bp)

if __name__ == "__main__":
    app.run(debug=True, port=6900, host="0.0.0.0")
