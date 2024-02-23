from backend.src.crosscutting import DummyLogger


def logger_factory():
    return DummyLogger()
