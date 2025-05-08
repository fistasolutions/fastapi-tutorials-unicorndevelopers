# 🎯 FastAPI GraphQL Adventure

## What This Code Does (Big Picture)
Imagine you have a magical toy store where customers can ask for EXACTLY what they want! Instead of having fixed menus like "show all toys" or "show one toy", GraphQL is like having a magical wish list where visitors can say things like "I want to see the name and price of all red toys" or "Show me just the name and stock of the newest toys". It's like having a super-smart toy store assistant who knows exactly what to show! 

## Step 1: Getting Our Magic Tools 🛠️
```python
from fastapi import FastAPI
from strawberry.fastapi import GraphQLRouter
import strawberry
```
This brings in our special tools:
- FastAPI for our magical store
- Strawberry for making our wish list system
- Special types to organize our toy information

## Step 2: Creating Our Toy Catalog 📚
```python
@strawberry.type
class Item:
    id: int
    name: str
    description: Optional[str]
    price: float
    created_at: datetime
    tags: List[str]
    stock: int
```
This creates our magical toy catalog that can show:
- The toy's special number (id)
- The toy's name
- A description of the toy
- How much it costs
- When we got the toy
- Special tags for the toy
- How many toys we have

## Step 3: Making Our Wish List System 🎁
```python
@strawberry.type
class Query:
    @strawberry.field
    def items(self) -> List[Item]:
        return [Item(**item) for item in fake_items_db.values()]
```
This creates our wish list system that lets visitors:
- Ask for all toys
- Ask for just one toy
- Choose what information they want to see
- Get exactly what they asked for!

## Step 4: Adding Magical Powers ✨
```python
@strawberry.type
class Mutation:
    @strawberry.mutation
    def create_item(self, name: str, price: float) -> Item:
        # Creates a new toy
```
This adds special powers that let us:
- Add new toys to the store
- Update toy information
- Remove toys we don't have anymore
- Keep everything organized

## Final Summary 📌
✅ We created a magical wish list system
✅ We made a flexible toy catalog
✅ We added special toy powers
✅ We can show exactly what visitors want

## Try It Yourself! 🚀
1. Make sure you have Python installed
2. Install FastAPI and Strawberry using uv:
   ```
   uv add "fastapi[standard]" strawberry-graphql
   ```
3. Save the code in a file named `23graphql.py`
4. Run the website using uv:
   ```
   uv run fastapi dev 23graphql.py
   ```
5. Visit the magical playground:
   - Go to `http://127.0.0.1:8000/graphql`
   - Try these magic spells:

### Show All Toys 🧸
```graphql
query {
  items {
    name
    price
    stock
  }
}
```

### Find One Special Toy 🎨
```graphql
query {
  item(id: 1) {
    name
    description
    price
  }
}
```

### Add a New Toy 🎁
```graphql
mutation {
  createItem(
    name: "New Toy"
    price: 15.99
    tags: ["new"]
    stock: 100
  ) {
    id
    name
  }
}
```

## What You'll Learn 🧠
- How to make a flexible toy catalog
- How to let visitors ask for exactly what they want
- How to add and update toys easily
- How to organize toy information

## Fun Things to Try! 🎮
1. Ask for different toy information
2. Create new toys with special tags
3. Update toy information
4. Make your own special queries

## Cool Features! ✨
- Custom wish lists (queries)
- Magical toy powers (mutations)
- Smart toy organization
- Flexible information display

## Special Powers You Get 🌟
### Queries (Looking at Toys):
- See all toys
- Find one special toy
- Choose what toy details to see

### Mutations (Changing Toys):
- Add new toys
- Update toy information
- Remove old toys

Happy coding! 🎉 Remember, GraphQL is like having a magical wish list system where you can ask for exactly what you want, and our toy store assistant (GraphQL) will get it for you perfectly! 