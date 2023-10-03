from server.src.crosscutting import DummyLogger


def logger_factory():
    return DummyLogger()
