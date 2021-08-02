from flask.signals import Namespace


signals = Namespace()

constance_setup = signals.signal("constance-setup")
constance_get = signals.signal("constance-get")
constance_set = signals.signal("constance-set")
