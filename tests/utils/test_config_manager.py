from utils.config_manager import ConfigManager

def test_singleton_behavior():
    config1 = ConfigManager()
    config2 = ConfigManager()

    assert config1 is config2, "ConfigManager is not maintaining singleton behavior"


def test_get_existing_setting():
    config = ConfigManager()
    assert config.get_settings("DEFAULT_PAGE_SIZE") == 10
    assert config.get_settings("ENABLE_ANALYTICS") is True


def test_set_and_get_setting():
    config = ConfigManager()
    config.set_settings("RATE_LIMIT", 200)
    assert config.get_settings("RATE_LIMIT") == 200


def test_get_non_existent_setting():
    config = ConfigManager()
    assert config.get_settings("NON_EXISTENT_KEY") is None