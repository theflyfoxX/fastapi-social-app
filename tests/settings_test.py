import os
import logging
import pytest
from importlib import reload
from pydantic import ValidationError

# Import the settings
import app.config.settings as settings_module
from app.config.settings import Settings

# ✅ Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

# ✅ Test valid settings
def test_valid_settings():
    logger.info("Testing valid settings from .env")
    
    assert isinstance(settings_module.settings.database_hostname, str)
    assert isinstance(settings_module.settings.database_port, str)
    assert isinstance(settings_module.settings.database_password, str)
    assert isinstance(settings_module.settings.database_name, str)
    assert isinstance(settings_module.settings.database_username, str)
    assert isinstance(settings_module.settings.secret_key, str)
    assert isinstance(settings_module.settings.algorithm, str)
    assert isinstance(settings_module.settings.access_token_expire_minutes, int)

    logger.info("✅ All settings variables are of correct type.")

# ✅ Test missing environment variables (failing test)
def test_missing_env_variables(monkeypatch):
    logger.info("Testing missing environment variables (should fail)")

    # Unset the database name environment variable
    monkeypatch.delenv("DATABASE_NAME", raising=False)

    with pytest.raises(ValidationError):
        reload(settings_module)
        Settings()

    logger.info("✅ Missing environment variable caused expected ValidationError.")

# ✅ Test invalid data type (failing test)
def test_invalid_data_type(monkeypatch):
    logger.info("Testing invalid data type for an environment variable (should fail)")

    # Set `access_token_expire_minutes` as a string instead of an integer
    monkeypatch.setenv("ACCESS_TOKEN_EXPIRE_MINUTES", "invalid_string")

    with pytest.raises(ValidationError):
        reload(settings_module)
        Settings()

    logger.info("✅ Invalid data type caused expected ValidationError.")

# import os
# import logging
# import pytest
# from app.config.settings import settings
# from pydantic import ValidationError

# # ✅ Configure logging
# logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
# logger = logging.getLogger(__name__)

# # ✅ Test valid settings
# def test_valid_settings():
#     logger.info("Testing valid settings from .env")
    
#     assert isinstance(settings.database_hostname, str)
#     assert isinstance(settings.database_port, str)
#     assert isinstance(settings.database_password, str)
#     assert isinstance(settings.database_name, str)
#     assert isinstance(settings.database_username, str)
#     assert isinstance(settings.secret_key, str)
#     assert isinstance(settings.algorithm, str)
#     assert isinstance(settings.access_token_expire_minutes, int)

#     logger.info("✅ All settings variables are of correct type.")

# # ✅ Test missing environment variables (failing test)
# def test_missing_env_variables(monkeypatch):
#     logger.info("Testing missing environment variables (should fail)")
    
#     # Remove database name temporarily
#     monkeypatch.delenv("DATABASE_NAME", raising=False)

#     with pytest.raises(ValidationError):
#         from app.config.settings import Settings
#         Settings()

#     logger.info("✅ Missing environment variable caused expected ValidationError.")

# # ✅ Test invalid data type (failing test)
# def test_invalid_data_type(monkeypatch):
#     logger.info("Testing invalid data type for an environment variable (should fail)")
    
#     # Set `access_token_expire_minutes` as a string instead of an integer
#     monkeypatch.setenv("ACCESS_TOKEN_EXPIRE_MINUTES", "invalid_string")

#     with pytest.raises(ValidationError):
#         from app.config.settings import Settings
#         Settings()

#     logger.info("✅ Invalid data type caused expected ValidationError.")
