try:
    from blinker import Namespace  # type: ignore

    signals = Namespace()

    constance_setup = signals.signal("constance-setup")
    constance_get = signals.signal("constance-get")
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
