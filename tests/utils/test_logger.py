from utils.logger import Logger
import logging

def test_singleton_behavior():
    logger1 = Logger()
    logger2 = Logger()
    assert logger1 is logger2, "Logger should be a singleton (same instance)"


def test_logger_output(caplog):
    logger = Logger().get_logger()

    with caplog.at_level(logging.INFO):
        logger.info("Test log message")

    # Check if the log message was captured
    assert "Test log message" in caplog.text
    assert "INFO" in caplog.text

