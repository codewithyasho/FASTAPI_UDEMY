from sqlmodel import SQLModel, Session, create_engine

DATABSE_URL = "sqlite:///rangmanch.db"

# echo=True: This is a logging flag.
# Python will print every raw SQL query it runs under the hood to your console.
engine = create_engine(DATABSE_URL, echo=True)


def create_tables():
    """Create all tables defined by SQLModel class"""
    SQLModel.metadata.create_all(engine)


# yield session: Instead of returning the session and destroying the function,
# yield passes the open session over to whatever route or function requested it.
def get_session():
    """Dependency that provides a database session per request"""
    with Session(engine) as session:
        yield session
