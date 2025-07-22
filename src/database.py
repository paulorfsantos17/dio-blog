import databases
import sqlalchemy

from src.settings import settings

database = databases.Database(settings.database_url)
metadata = sqlalchemy.MetaData()


if settings.environment == "production":
    engine = sqlalchemy.create_engine(
        settings.database_url
    )
else:
    engine = sqlalchemy.create_engine(
        settings.database_url, connect_args={"check_same_thread": False}
    )
