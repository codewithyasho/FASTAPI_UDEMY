from fastapi import FastAPI, Query, HTTPException
import uvicorn
from models import SingleMenuItem, MultiMenuItems
from data import menu_items

app = FastAPI(
    title="The Seventh Sip Menu API",
    description="Read only menu API for kiosk displays and mobile apps"

)


@app.get("/")
def root():
    return {
        "message": "Welcome to the seventh sip menu api",
        "status": "healthy"
    }


@app.get("/menu", response_model=MultiMenuItems, tags=["menu"])
def get_menu():
    return MultiMenuItems(count=len(menu_items), items=menu_items)


@app.get("/menu/filter", response_model=MultiMenuItems, tags=["menu"])
def filter_by_category(category: str | None = Query(None, description="filter by shake, cold_coffee, sandwich")):
    if category:
        filtered_items = [
            item for item in menu_items if item["category"] == category.lower()]

        if not filtered_items:
            raise HTTPException(
                status_code=404, detail=f"Category doesn't exist: {category}")

        return MultiMenuItems(count=len(filtered_items), items=filtered_items)

    raise HTTPException(
        status_code=400, detail=f"Please provide category parameter...")


@app.get("/menu/sort", response_model=MultiMenuItems, tags=["menu"])
def sort_by_price():
    sorted_items = sorted(menu_items, key=lambda x: x["price"])
    return MultiMenuItems(count=len(sorted_items), items=sorted_items)


@app.get("/menu/{item_id}", response_model=SingleMenuItem, tags=["menu"])
def get_item(item_id: int):
    for item in menu_items:
        if item["id"] == item_id:
            return item

    raise HTTPException(
        status_code=404, detail=f"Menu item not found with the item id: {item_id}")


if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8100, reload=True)
