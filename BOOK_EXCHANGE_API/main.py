from fastapi import FastAPI
from database import create_tables
from routes import books, users
from contextlib import asynccontextmanager
import uvicorn


@asynccontextmanager
async def lifespan(app: FastAPI):
    create_tables()
    print("\nDatabase tables created✅.")
    yield
    print("\nshutting down the app")

app = FastAPI(
    title="Book Exchange API",
    description="An API for exchanging books between users.",
    version="1.0.0",
    lifespan=lifespan
)


app.include_router(books.router)
app.include_router(users.router)


@app.get("/")
def home():
    return {
        "message": "Welcome to the Book Exchange API",
        "status": "healthy"
    }


if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
