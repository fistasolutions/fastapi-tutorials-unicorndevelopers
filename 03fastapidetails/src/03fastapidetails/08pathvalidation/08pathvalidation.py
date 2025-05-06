from fastapi import FastAPI, Path
from typing import Optional

app = FastAPI()

@app.get("/items/{item_id}")
async def read_items(
    item_id: int = Path(..., title="The ID of the item to get", ge=1, le=1000),
    q: Optional[str] = None
):
    results = {"item_id": item_id}
    if q:
        results.update({"q": q})
    return results

@app.get("/items/{item_id}/details")
async def read_item_details(
    item_id: int = Path(..., title="The ID of the item to get", ge=1, le=1000),
    q: Optional[str] = None,
    short: bool = False
):
    item = {"item_id": item_id}
    if q:
        item.update({"q": q})
    if not short:
        item.update(
            {"description": "This is an amazing item that has a long description"}
        )
    return item 