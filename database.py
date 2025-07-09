from databases import Database
from sqlalchemy import Table, Column, Integer, String, MetaData, create_engine

DATABASE_URL = "postgresql+asyncpg://user_fastapi:qwerty12345@localhost:5432/fastapi_database"

database = Database(DATABASE_URL)
metadata = MetaData()

engine = create_engine(DATABASE_URL.replace("+asyncpg", ""))
metadata.create_all(engine)
