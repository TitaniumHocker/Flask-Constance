Guide
=====

The following is a more advanced guide to using the extension.

Initializing methods
--------------------

As most extensions, Flask-Constance can be initialized
in two ways:

1. Pass application object to extension ``__init__`` method:

.. code:: python

    from flask import Flask
    from flask_constance import Constance

    app = Flask(__name__)
    constance = Constance(app)

2. Use ``init_app`` method:

.. code:: python

    from flask import Flask
    from flask_constance import Constance

    app = Flask(__name__)
    constance = Constance()
    constance.init_app(app)

These two methods are equal. Extension constructor just
calls `init_app` method if application object was provided.

Naming restrictions
-------------------

There are few restrictions on settings naming:

- Names can't contain ``-`` character.
- Names can't starts with underscore ``_`` character.
- Names can't starts with number.

Given that the settings will be accessed through the class attributes
of the global object :obj:`~flask_constance.settings`, it is desirable 
that the settings names be valid for  use as class attribute names.

Managing settings
-----------------

For accessing dynamic settings provided by Flask-Constance extension
there is global object :obj:`~flask_constance.settings`.
Actually this in werkzeug's LocalProxy object pointing to
:class:`~flask_constance.storage.Storage` instance.
``Storage`` object defines ``__getattr__``, ``__setattr__`` and
``__delattr__`` methods to access settings. So you can access your
settings like normal attributes of ``Storage`` object.

For example you defined some settings via ``CONSTANCE_PAYLOAD``
application config value:

.. code:: python

    app.config["CONSTANCE_PAYLOAD"] = {
        "foo": "bar",
        "hello": "world",
    }

Then they becomes accessable with global ``settings`` object:

.. code:: python

    from flask_constance import settings

    assert settings.foo == "bar"
    assert settings.hello == "world"

They can be updated like normal class attributes:

.. code:: python

    from flask_constance import settings

    settings.foo = "not bar"  # Will be updated in backend.
    assert settings.foo == "not bar"

Also they can be deleted to reset them to default value:

.. code:: python

    from flask_constance import settings

    assert settings.foo == "bar"     # default value.
    settings.foo = "not bar"         # updating.
    assert settings.foo == "not bar" # updated value.
    del settings.foo                 # resetting to default value.
    assert settings.foo == "bar"     # default value

Supported backends
------------------

`Backend` in Flask-Constance terminology is actual storage of 
settings values. When settin first accessed it will be stored
in connected backend.

Flask-SQLAlchemy
^^^^^^^^^^^^^^^^

Most common backend is `Flask-SQLAlchemy` backend provided via
:class:`~flask_constance.backends.fsqla.FlaskSQLAlchemyBackend`
class. This backend stores settings in database configured with
`SQLAlchemy`. To initialize this backend `SQLAlchemy` session
and corresponding model must be provided.

Database model must have some required fields:

- ``name`` field with required unique string type.
- ``value`` field with JSON type.

Here is an example of using `Flask-SQLAlchemy` backend:

.. code:: python
    
    from flask import Flask
    from flask_sqlalchemy import SQLAlchemy
    from flask_constance import Constance
    from flask_constance.backends import FlaskSQLAlchemyBackend
    import sqlalchemy as sa

    app = Flask(__name__)
    db = SQLAlchemy(app)

    class Setting(db.Model):
        id = sa.Column(sa.Integer, primary_key=True)
        name = sa.Column(sa.String, unique=True, nullable=False, index=True)
        value = sa.Column(sa.JSON, nullable=True)

    constance = Constance(app, FlaskSQLAlchemyBackend())

There is predefined model mixin with all required fields.
Here is same example with using this mixin:

.. code:: python

    from flask import Flask
    from flask_sqlalchemy import SQLAlchemy
    from flask_constance import Constance
    from flask_constance.backends import \
        FlaskSQLAlchemyBackend, SettingMixin
    import sqlalchemy as sa

    app = Flask(__name__)
    db = SQLAlchemy(app)

    class Setting(db.Model, SettingMixin):
        pass

    constance = Constance(app, FlaskSQLAlchemyBackend())

Caching
-------

By default Flask-Constance will cache settings that are accessed
in Flask's ``g`` object. This object recreates on every request,
so this caching mechanism is very limited. It can reduce number
of access operations to the backend during request, but nothing 
more.

In the future there are plans to implement some external backend
cache support. For now it can be implemented by hand with
:class:`~flask_constance.backends.base.BackendCache` base class
and passed to :class:`~flask_constance.Constance`.

See :ref:`guide:Implementing your own backend or cache` section for
additional information.

RESTlike view
-------------

If you need to manage settings via HTTP API - there is simple
implementation of RESTlike view :class:`~flask_constance.view.ConstanceView`.
To enable it just set ``CONSTANCE_VIEW_BASE_URL`` config value.

For example if config value set to ``/api/constance`` then this
operations can be done with HTTP API:

- ``GET`` on ``/api/constance`` to get all settings values.
- ``GET`` on ``/api/constance/<name>`` to get specific config value by it's name.
- ``PUT`` on ``/api/constance/<name>`` to update specific config value by it's name.
- ``DELETE`` on ``/api/constance/<name>`` to reset specific config value by it's name.

``PUT`` request accepts JSON as a payload. ``GET`` requests returns JSON 
as response payload. If setting not found by it's name - 404 status will
be returned.

Here is an example how you can connect this API:

.. code:: python

    from flask import Flask
    from flask_constance import Constance

    app = Flask(__name__)
    app.config["CONSTANCE_PAYLOAD"] = {"foo": "bar"}
    app.config["CONSTANCE_VIEW_BASE_URL"] = "/api/constance"

    if __name__ == "__main__":
        app.run(debug=True)

And then use it:

.. code:: bash

    $ curl -X GET http://localhost:5000/api/constance
    {
    "foo": "bar"
    }
    $ curl -X PUT http://localhost:5000/api/constance/foo \
        -H "Content-Type: application/json" \
        -d '"new-data"'
    {}
    $ curl -X GET http://localhost:5000/api/constance
    {
    "foo": "new-data"
    }
    $ curl -X DELETE http://localhost:5000/api/constance/foo
    {}
    $ curl -X GET http://localhost:5000/api/constance
    {
    "foo": "bar"
    }

CLI
---

Settings can be accessed from simple CLI interface.

- ``flask constance get`` command for reading values.
- ``flask constance set`` for updating.
- and ``flask constance del`` for deleting(resetting) values.

Signals
-------

Flask-Constance supports Flask's signalling feature via `blinker`
package. Extension sends signalls in these cases:

- When extension was initialized: :obj:`~flask_constance.signals.constance_setup`.
- When setting value was accessed: :obj:`~flask_constance.signals.constance_get`.
- When setting value was updated: :obj:`~flask_constance.signals.constance_set`.

Implementing your own backend or cache
--------------------------------------

If you want to implement your own backend or backend cache there is
two base classes - :class:`~flask_constance.backends.base.Backend`
and :class:`~flask_constance.backends.base.BackendCache`.

In general backend must implement to methods:

 - ``set`` to set setting value, that takes name and value as arguments.
 - ``get`` to get setting value by it's name.

For backend cache signature is the same, except that in addition
``invalidate`` method must be implemented. This method deletes value
from the cache by it's name.

Here is an example of a backend cache that uses memcached(pymemcache):

.. code:: python

    import typing as t
    import os
    import json
    from pymemcache.client.base import Client
    from flask_constance.backends.base import BackendCache

    class MemcachedBackendCache(BackendCache):
        def __init__(self, addr: str):
            self.client = Client(addr)
        
        def get(self, name: str) -> t.Any:
            return json.loads(self.client.get(name))
        
        def set(self, name: str, value: t.Any):
            self.client.set(name, json.dumps(value))
        
        def invalidate(name: str):
            self.client.delete(name)

Configuration
-------------

As usual for Flask extensions, Flask-Constance configuration
variables stored in Flask.config object with ``CONSTANCE_`` prefix.
Here is configuration variables of Flask-Constance extension:

+-------------------------+----------------------------+-------------+------------+
| Name                    | Description                | Type        | Default    |
+=========================+============================+=============+============+
| CONSTANCE_PAYLOAD       | Dictionay with settings.   | Dict        | Empty dict |
+-------------------------+----------------------------+-------------+------------+
| CONSTANCE_VIEW_BASE_URL | Base url for RESTlike view | str or None | None       |
+-------------------------+----------------------------+-------------+------------+

Flask-Admin integration
-----------------------

If you use ``Flask-Admin``, then there is an integration for this extension.

.. code:: python

    from flask import Flask
    from flask_admin import Admin
    from flask_constance import Constance, settings
    from flask_constance.admin import ConstanceAdminView
    from flask_constance.backends.fsqla import FlaskSQLAlchemyBackend, SettingMixin

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