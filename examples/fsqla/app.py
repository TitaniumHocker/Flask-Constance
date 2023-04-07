from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy

from flask_constance import Constance, settings
from flask_constance.backends.fsqla import FlaskSQLAlchemyBackend, SettingMixin

app = Flask(__name__)
db = SQLAlchemy(app)


class ConstanceSettings(db.Model, SettingMixin):  # type: ignore
    pass


constance = Constance(app, FlaskSQLAlchemyBackend(ConstanceSettings, db.session))

app.config["SERCET_KEY"] = "super-secret"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["CONSTANCE_PAYLOAD"] = {"foo": "bar"}


@app.route("/")
def index():
    return {key: getattr(settings, key) for key in dir(settings)}


@app.route("/<name>", methods=["POST"])
def update(name: str):
    if request.json is None:
        return {}, 400
    setattr(settings, name, request.json)
    return {key: getattr(settings, key) for key in dir(settings)}


def main():
    db.create_all()
    app.run("0.0.0.0", 5000, True)


if __name__ == "__main__":
    main()
