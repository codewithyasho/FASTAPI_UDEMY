from fastapi import FastAPI
from fastapi import Request
import uvicorn

app = FastAPI(
    title="Swiggy Order Service",
    description=(
        "internal API for managing orders "
        "Handle creation, tracking of delivery systems"
    ),
    version="1.2.1",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json"
)


@app.get("/")
def read_root():
    """Root endpoint - health check"""

    # FASTAPI auto converts this dict into JSON
    return {
        "message": "Welcome to Swiggy ORder Service API",
        "status": "healthy"
    }


@app.get("/about", deprecated=True)
def about():
    """Returns API metadata"""

    return {
        "service": "order-service",
        "team": "backend-platform",
        "region": "ap-south-1",
        "version": "1.2.2"
    }


@app.get("/orders")
def list_orders():
    """List recent orders"""

    return {
        "orders": [
            {"id": 1, "item": "Butter Chicken", "status": "delivered"},
            {"id": 2, "item": "Masala Dosa", "status": "prepairing"},
            {"id": 3, "item": "Pav Bhaji", "status": "delivered"},
        ]
    }


@app.get("orders/status")
def order_status():
    """Get order status"""

    return {
        "total_order_today": 1_23_045,
        "top_city": "Pune"
    }


@app.get("/debug/request-info", tags=["debug"],)
async def request_info(request: Request):
    """Inspect the raw request object"""

    return {
        "method": request.method,
        "url": str(request.url),
        "headers": dict(request.headers),
        "path_params": request.path_params,
        "query_params": dict(request.query_params),
    }


@app.get(
    "/orders/active",
    summary="Get Active Orders",
    description=(
        """Returns all the orders that are currently being prepared or out of delivery"""
    ),
    tags=["orders"],
    response_description="List of active order objects",
    deprecated=False
)
def get_active_order():
    return {
        "active_orders": [
            {"id": 1, "item": "wada pav", "status": "out_of_delivery"}
        ]
    }


if __name__ == "__main__":
    uvicorn.run("main:app",
                host="127.0.0.1", port=8000, reload=True)
