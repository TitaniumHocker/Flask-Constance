===
API
===

.. module:: flask_constance

Here you can find part of documentation that covers all
public interfaces of Flask-Constance.

Extension object
----------------

.. autoclass:: Constance
   :members:
   :undoc-members:
   :show-inheritance:

Global settings object
----------------------

.. attribute:: settings

   With this global you can access settings from any point
   of your application. This object actually is werkzeug's 
   LocalProxy pointing to :class:`~flask_constance.storage.Storage` object.

.. module:: flask_constance.storage

Storage aka settings object
---------------------------

.. autoclass:: Storage
   :members:
   :undoc-members:
   :show-inheritance:

.. module:: flask_constance.backends.base

Backends
--------

Flask-Constance supports various types of backends.
All of them implements :class:`~flask_constance.backends.base.Backend`
or :class:`flask_constance.backends.base.BackendCache` protocols.

Backend Protocol
^^^^^^^^^^^^^^^^

.. autoclass:: Backend
   :members:
   :undoc-members:
   :show-inheritance:

Backend Cache Protocol
^^^^^^^^^^^^^^^^^^^^^^

.. autoclass:: BackendCache
   :members:
   :undoc-members:
   :show-inheritance:

.. module:: flask_constance.backends.memory

Memory Backend object
^^^^^^^^^^^^^^^^^^^^^

Memory backend was implemented for testing purposes.
It can be used only in single-process mode, so
it really doesn't fit production environment requirenments.

.. autoclass:: MemoryBackend
   :members:
   :undoc-members:
   :show-inheritance:

.. module:: flask_constance.backends.fsqla

Flask-SQLAlchemy backend object
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

This backend implements intergration with Flask-SQLAlchemy
extension as main settings storage.

.. autoclass:: FlaskSQLAlchemyBackend
   :members:
   :undoc-members:
   :show-inheritance:


Flask-SQLAlchemy model mixin
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Mixin that will define all needed sqlalchemy
fiels for your model.

.. autoclass:: SettingMixin
   :members:
   :undoc-members:
   :show-inheritance:

.. module:: flask_constance.signals

Signals
-------

.. attribute:: constance_setup

Signal that called after extension was initialized.
Called with 2 agruments:

- Instance of :class:`~flask_constance.Constance`.
- Instance of Flask application.

.. attribute:: constance_get

Signal that called after setting value was accessed.
Called with 2 arguments:

- Instance of :class:`~flask_constance.Constance`.
- Name of the setting that was accessed.

.. attribute:: constance_set

Signal that called after setting value was updated.
Called with 3 arguments:

- Instance of :class:`~flask_constance.Constance`.
- Name of the setting that was updated.
- New value of the setting.

.. module:: flask_constance.view

RESTlike view
-------------

View implementing RESTlike interface for managing
Flask-Constance dynamic settings.

.. autoclass:: ConstanceView
   :members:
   :undoc-members:
   :show-inheritance: