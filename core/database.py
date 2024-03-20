from sqlalchemy import create_engine, engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DATABASE_URL = "sqlite:///./tooling.db"  # path to the database

# # To use MySQL Database, uncomment this lines
# SQLALCHEMY_DATABASE_URL = (
#     "mysql+mysqlconnector://root@127.0.0.1:3306/tooling"  # path to the database
# )

# SQLALCHEMY default code
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},

    # # To use MySQL Database, uncomment this lines
    # SQLALCHEMY_DATABASE_URL
)

SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)
Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
