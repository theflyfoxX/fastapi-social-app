import pytest
import logging
from sqlalchemy import text
from sqlalchemy.exc import OperationalError
from importlib import reload
from app.config import database as database_module
from app.config.database import engine, SessionLocal, get_db
from app.config.settings import settings

# ✅ Configure Logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

# ✅ Test that the database URL is built correctly
def test_database_url():
    logger.info("Testing database connection URL formation.")

    expected_url = (
        f"postgresql://{settings.database_username}:"
        f"{settings.database_password}@"
        f"{settings.database_hostname}:"
        f"{settings.database_port}/"
        f"{settings.database_name}"
    )

    assert database_module.SQLALCHEMY_DATABASE_URL == expected_url

    logger.info("✅ Database connection URL is correctly formatted.")

# ✅ Test database connection
def test_database_connection():
    logger.info("Testing database connection.")

    try:
        with engine.connect() as connection:
            result = connection.execute(text("SELECT 1"))
            assert result.fetchone()[0] == 1
            logger.info("✅ Successfully connected to the database.")
    except OperationalError as e:
        logger.error(f"❌ Database connection failed: {e}")
        pytest.fail("Database connection failed.")

# ✅ Test creating and closing a database session
def test_get_db_session():
    logger.info("Testing database session creation and closure.")

    db = None
    try:
        db = next(get_db())
        assert db is not None
        logger.info("✅ Successfully created a database session.")
    finally:
        if db:
            db.close()
            logger.info("✅ Database session closed successfully.")

# ✅ Test failure with invalid credentials
def test_invalid_database_credentials(monkeypatch):
    logger.info("Testing database connection with invalid credentials (should fail).")

    # Set incorrect credentials
    monkeypatch.setattr(settings, "database_password", "wrongpassword")

    with pytest.raises(OperationalError):
        reload(database_module)  # Reload the module to apply changes
        with database_module.engine.connect() as connection:
            connection.execute(text("SELECT 1"))

    logger.info("✅ Invalid database credentials caused expected OperationalError.")
