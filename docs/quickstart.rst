Quickstart
==========

Here some simple tutorial how to get started with
Flask-Constance after the installation.

Import and initialize
---------------------

First of all you need import and initialize extension
with your application and selected backend. In this
example Flask-SQLAlchemy will be used as backend.

.. code:: python

    from flask import Flask
    from flask_sqlalchemy import SQLAlchemy
    from flask_constance import Constance
    from flask_constance.backends import \
        FlaskSQLAlchemyBackend, SettingMixin

    # Initialize application and Flask-SQLAlchemy.
    app = Flask(__name__)
    app.config["SERCET_KEY"] = "super-secret"
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db = SQLAlchemy(app)

    # Define model for the backend.
    class Setting(db.Model, SettingMixin):
        pass

    # Finally, initialize Flask-Constance.
    constance = Constance(app, FlaskSQLAlchemyBackend(Setting, db.session))

    # Also you can use init_app method if you want.
    # constance = Constance(backend=FlaskSQLAlchemyBackend(Setting, db.session))
    # constance.init_app(app)

Describe settings
-----------------

To set up some settings and their default values they need
do be defined via config value `CONSTANCE_PAYLOAD`.
This must be a dictionary where key is a setting name
and value - default value for this setting.

.. code:: python

    app.config["CONSTANCE_PAYLOAD"] = {
        "foo": "bar",
        "hello": "world",
    }

Use it
------

After connecting Flask-Constance with your application you
finally can use global `settings` object to read or modify them.

.. note::
    Please note that the `settings` object is only available
    in the application context. In views for example.

.. code:: python

    from flask import jsonify, request
    from flask_constance import settings

    @app.route("/")
    def index():
        """This view will return current settings as a JSON."""
        if settings.foo == "bar":
            settings.foo == "not bar"
        elif settings.foo == "not bar":
            settings.foo == "bar"
        return jsonify({key: getattr(settings, key) for key in dir(settings)})

Full example
------------

Here is a full example from `examples` directory of the project repo.

.. include:: ../examples/fsqla/app.py
    :code: python