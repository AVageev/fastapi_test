from database import engine, metadata
import models  # чтобы импортировать таблицы

metadata.create_all(engine)
