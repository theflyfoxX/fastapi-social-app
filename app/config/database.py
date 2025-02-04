from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from app.config.settings import settings

# ✅ PostgreSQL Connection URL
SQLALCHEMY_DATABASE_URL = (
    f"postgresql://{settings.database_username}:"
    f"{settings.database_password}@"
    f"{settings.database_hostname}:"
    f"{settings.database_port}/"
    f"{settings.database_name}"
)

# ✅ Create SQLAlchemy Engine
engine = create_engine(SQLALCHEMY_DATABASE_URL)

# ✅ Create Session Factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# ✅ Base Class for Models
Base = declarative_base()

# ✅ Dependency for Getting DB Session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
