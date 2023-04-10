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

RESTlike view
-------------

CLI
---

Signals
-------

Implementing your own backend or cache
--------------------------------------

Configuration
-------------

Flask-Admin integration
-----------------------