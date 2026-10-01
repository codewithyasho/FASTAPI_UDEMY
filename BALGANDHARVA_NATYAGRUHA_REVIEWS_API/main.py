from contextlib import asynccontextmanager
from fastapi import FastAPI
import uvicorn
from database import create_tables
from routes.reviews import router as reviews_router
from fastapi.exceptions import RequestValidationError

from exceptions import validation_exception_handler


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Step A: Runs at startup
    create_tables()
    print("\nDatabase tables created✅.")
    # Step B: Hands control back to FastAPI
    yield
    # Step C: Runs at shutdown
    print("\nshutting down the app")


app = FastAPI(
    title="Balgandharva natyagruh reviews API",
    description="Theatre review API for Balgandharva natyagruh Pune",
    #  Enforces the lifespan logic
    lifespan=lifespan
)


# anything that starts from '/review' will auto handle by this routing config.
app.include_router(reviews_router)

app.add_exception_handler(
    RequestValidationError,
    validation_exception_handler
)


@app.get("/")
def root():
    return {
        "message": "welcome to the Theatre review API",
        "status": "healthy"
    }


if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
