from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI(title="Simple FastAPI App", version="1.0.0")


class Item(BaseModel):
    name: str
    description: str | None = None
    price: float
    is_available: bool = True


@app.get("/")
async def root():
    """Root endpoint"""
    return {"message": "Welcome to FastAPI!"}


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy"}


@app.get("/items/{item_id}")
async def read_item(item_id: int, q: str | None = None):
    """Get item by ID with optional query parameter"""
    return {"item_id": item_id, "query": q}


@app.post("/items/")
async def create_item(item: Item):
    """Create a new item"""
    return {"item": item, "message": "Item created successfully"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)