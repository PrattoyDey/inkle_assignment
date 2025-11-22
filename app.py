from flask import Flask, jsonify
from flask_jwt_extended import JWTManager
from flask_cors import CORS

from config import Config
from models import db


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Extensions
    db.init_app(app)
    JWTManager(app)
    CORS(app)

    # Blueprints
    from auth_routes import auth_bp
    from user_routes import user_bp
    from post_routes import post_bp
    from activity_routes import activity_bp

    app.register_blueprint(auth_bp, url_prefix="/auth")
    app.register_blueprint(user_bp, url_prefix="/users")
    app.register_blueprint(post_bp, url_prefix="/posts")
    app.register_blueprint(activity_bp, url_prefix="/activity")

    @app.route("/")
    def index():
        return jsonify({"message": "Inkle mini-twitter backend running ✅"})

    return app


app = create_app()

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)