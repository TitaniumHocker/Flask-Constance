from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

from flask_constance import Constance
from flask_constance.backends.fsqla import FlaskSQLAlchemyBackend, SettingMixin

app = Flask(__name__)
app.config["SERCET_KEY"] = "super-secret"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["CONSTANCE_PAYLOAD"] = {"foo": "bar"}
app.config["CONSTANCE_VIEW_BASE_URL"] = "/api/constance"

db = SQLAlchemy(app)


class ConstanceSettings(db.Model, SettingMixin):  # type: ignore
    pass


constance = Constance(app, FlaskSQLAlchemyBackend(ConstanceSettings, db.session))

def main():
    db.create_all()
    app.run("0.0.0.0", 5000, True)


if __name__ == "__main__":
    main()
