from sqlmodel import SQLModel, create_engine, Session

database_url = "sqlite:///dabbe_wala.db"

engine = create_engine(database_url, echo=True)


def create_tables():
    SQLModel.metadata.create_all(engine)


def get_session():
    """provides a new database session"""
    with Session(engine) as session:
        yield session
