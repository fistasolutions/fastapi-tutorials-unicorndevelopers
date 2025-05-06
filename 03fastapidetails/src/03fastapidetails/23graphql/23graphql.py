from fastapi import FastAPI
from strawberry.fastapi import GraphQLRouter
import strawberry
from typing import List, Optional
from datetime import datetime
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Database simulation
fake_items_db = {
    1: {
        "id": 1,
        "name": "Item 1",
        "description": "Description 1",
        "price": 10.5,
        "created_at": datetime.now(),
        "tags": ["new", "featured"],
        "stock": 100
    },
    2: {
        "id": 2,
        "name": "Item 2",
        "description": "Description 2",
        "price": 20.0,
        "created_at": datetime.now(),
        "tags": ["sale"],
        "stock": 50
    }
}

# GraphQL Types
@strawberry.type
class Item:
    id: int
    name: str
    description: Optional[str]
    price: float
    created_at: datetime
    tags: List[str]
    stock: int

# GraphQL Query
@strawberry.type
class Query:
    @strawberry.field
    def items(self) -> List[Item]:
        logger.info("Fetching all items")
        return [Item(**item) for item in fake_items_db.values()]

    @strawberry.field
    def item(self, id: int) -> Optional[Item]:
        logger.info(f"Fetching item {id}")
        if id not in fake_items_db:
            return None
        return Item(**fake_items_db[id])

# GraphQL Mutation
@strawberry.type
class Mutation:
    @strawberry.mutation
    def create_item(
        self,
        name: str,
        description: Optional[str] = None,
        price: float = 0.0,
        tags: List[str] = [],
        stock: int = 0
    ) -> Item:
        logger.info(f"Creating new item: {name}")
        item_id = max(fake_items_db.keys()) + 1
        item = {
            "id": item_id,
            "name": name,
            "description": description,
            "price": price,
            "created_at": datetime.now(),
            "tags": tags,
            "stock": stock
        }
        fake_items_db[item_id] = item
        return Item(**item)

    @strawberry.mutation
    def update_item(
        self,
        id: int,
        name: Optional[str] = None,
        description: Optional[str] = None,
        price: Optional[float] = None,
        tags: Optional[List[str]] = None,
        stock: Optional[int] = None
    ) -> Optional[Item]:
        logger.info(f"Updating item {id}")
        if id not in fake_items_db:
            return None
        
        item = fake_items_db[id]
        if name is not None:
            item["name"] = name
        if description is not None:
            item["description"] = description
        if price is not None:
            item["price"] = price
        if tags is not None:
            item["tags"] = tags
        if stock is not None:
            item["stock"] = stock
        
        return Item(**item)

    @strawberry.mutation
    def delete_item(self, id: int) -> bool:
        logger.info(f"Deleting item {id}")
        if id not in fake_items_db:
            return False
        del fake_items_db[id]
        return True

# Create schema
schema = strawberry.Schema(query=Query, mutation=Mutation)

# Create GraphQL router
graphql_app = GraphQLRouter(schema)

# Create FastAPI app
app = FastAPI(
    title="FastAPI GraphQL Example",
    description="Example of GraphQL integration with FastAPI using Strawberry",
    version="1.0.0"
)

# Include GraphQL router
app.include_router(graphql_app, prefix="/graphql")

# Example GraphQL queries:
"""
# Query all items
query {
  items {
    id
    name
    price
    stock
  }
}

# Query single item
query {
  item(id: 1) {
    id
    name
    description
    price
    tags
    stock
  }
}

# Create item mutation
mutation {
  createItem(
    name: "New Item"
    description: "A new item"
    price: 15.99
    tags: ["new"]
    stock: 100
  ) {
    id
    name
    price
  }
}

# Update item mutation
mutation {
  updateItem(
    id: 1
    name: "Updated Item"
    price: 25.99
  ) {
    id
    name
    price
  }
}

# Delete item mutation
mutation {
  deleteItem(id: 1)
}
""" 