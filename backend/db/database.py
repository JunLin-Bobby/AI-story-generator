from sqlalchemy import create_engine
from sqlachemy.orm import sessionmaker
from sqlachemy.ext.declarative import declarative_base
from core.config import settings

engine = create_engine(settings.DATABASE_URL, echo=True)

sessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
	db =sessionLocal()
	try:
		yield db
	finally:
		db.close()

def create_tables():
	Base.metadata.create_all(bind=engine)