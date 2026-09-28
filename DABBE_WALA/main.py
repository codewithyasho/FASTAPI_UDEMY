from contextlib import asynccontextmanager
from fastapi import FastAPI
from database import create_tables
from routes.orders import router as orders_router
from routes.stats import router as stats_router
import uvicorn


@asynccontextmanager
async def lifespan(app: FastAPI):
    create_tables()
    print("Tables created successfully✅.")
    yield
    print("Application shutdown. Goodbye!👋")


app = FastAPI(
    title="DABBE WALA",
    description="A simple API for managing dabbawala deleivery services and tracking orders.",
    version="1.0.0",
    lifespan=lifespan
)

app.include_router(orders_router)
app.include_router(stats_router)


@app.get("/")
def root():
    return {"message": "Welcome to DABBE WALA API!🚀"}


if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
