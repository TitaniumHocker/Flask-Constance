from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_admin import Admin

from flask_constance import Constance, settings
from flask_constance.backends.fsqla import FlaskSQLAlchemyBackend, SettingMixin
from flask_constance.admin import ConstanceAdminView

app = Flask(__name__)
app.config["SECRET_KEY"] = "super-secret"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["CONSTANCE_PAYLOAD"] = {"foo": "bar", "hello": "world"}

db = SQLAlchemy(app)


class ConstanceSettings(db.Model, SettingMixin):  # type: ignore
    pass


constance = Constance(app, FlaskSQLAlchemyBackend(ConstanceSettings, db.session))

admin = Admin(app, template_mode="bootstrap4")
admin.add_view(ConstanceAdminView(name="Settings", endpoint="settings"))


@app.route("/")
def index():
    """This view will return current settings as a JSON."""
    if settings.foo == "bar":
        settings.foo = "not bar"
    elif settings.foo == "not bar":
        settings.foo = "bar"
    return jsonify({key: getattr(settings, key) for key in dir(settings)})


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
