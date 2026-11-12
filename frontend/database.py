
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

db_url = "postgresql+psycopg2://jeet@localhost:5432/DemoM"

engine = create_engine(db_url, echo=True)

sessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)
