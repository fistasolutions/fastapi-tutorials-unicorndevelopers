from fastapi import FastAPI, Query
from typing import List, Optional

app = FastAPI()

@app.get("/items/")
async def read_items(
    q: Optional[str] = Query(None, min_length=3, max_length=50),
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100)
):
    results = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
    if q:
        results.update({"q": q})
    return results

@app.get("/items/multiple/")
async def read_items_multiple(
    q: Optional[List[str]] = Query(None, title="Query string", description="Query string for the items to search")
):
    query_items = {"q": q}
    return query_items 