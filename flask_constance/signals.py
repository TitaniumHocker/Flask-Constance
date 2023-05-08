try:
    from blinker import Namespace  # type: ignore[import]

    signals = Namespace()

    #: Signal called after extension was initialized.
    constance_setup = signals.signal("constance-setup")
    #: Signal called after setting value was accessed.
    constance_get = signals.signal("constance-get")
    #: Signal called after setting value was updated.
    constance_set = signals.signal("constance-set")
except ImportError:

    class MockedSignal:
        def __init__(self, name: str):
            self.name = name

        def __repr__(self) -> str:
            return f"<MockedSignal {self.name}>"

        def send(self, *args, **kwargs):
            pass

    constance_setup = MockedSignal("constance-setup")
    constance_get = MockedSignal("constance-get")
    constance_set = MockedSignal("constance-set")
