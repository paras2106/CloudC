from flask import Flask
from flask_cors import CORS

from app.config import config as cfg
from src.views.auth import auth_app

app = Flask(__name__, template_folder="../templates")

app.config["SECRET_KEY"] = cfg.get("common", "SECRET_KEY")

if cfg.get("flask", "DEBUG", fallback=False):
    print("CORS enabled for the app !!")
    CORS(app)

# register blueprints
app.register_blueprint(auth_app)


@app.route("/health_check", methods=["GET"])
def verify():
    return "Hurray!! Happy that I am alive. Have a good day :)"


app.run(
    host="0.0.0.0",
    debug=cfg.get("common", "DEBUG", fallback=False),
    port=cfg.get("common", "PORT", fallback=5000),
)