from fastapi import FastAPI
from products import products
from pydantic import BaseModel
from fastapi import HTTPException

app = FastAPI()


@app.get("/")
def get_home():
    return {"message": "Welcome to our E-commerce API"}


# list of sample products
@app.get("/products")
def get_products():
    return {"products": products}


@app.get("/products/{product_id}")
def get_product_by_id(product_id: int):
    for product in products:
        if product["id"] == product_id:
            return {"product": product}


# gets one product by id
@app.get("/products/{product_id}")
# Tells the function to get the product id and specifies that it should be an integer
def get_product_id(product_id: int):
    for product in products:
        if product["id"] == product_id:
            return product
        return {"error": "Product not found"}


# users list
users = []
# A dictionary to store carts.Use user id as key
carts = {}


class CartItem(BaseModel):
    user_id: int
    Product_id: int
    quantity: int


class User(BaseModel):
    id: int
    username: str
    email: str
    password: str


# Creating a new user with a POST
@app.post("/register")
def register_user(user: User):
    users.append(user.model_dump())
    return {"message": "User registered successfully"}


# Check user credentials with a POST
@app.post("/login")
def login_user(user: User):
    for existing_user in users:
        if (
            existing_user["username"] == user.username
            and existing_user["password"] == user.password
        ):
            return {"message": "Successfully Logged in"}
        raise HTTPException(status_code=409, detail="Invalid credentials")


# Add a product to a user's cart
@app.post("/cart")
def add_to_cart(item: CartItem):
    #check item availability
    product_is_available = False
    for product in products:
       if product ["id"]== item.Product_id :
          product_is_available=True
          break
    if not product_is_available :
      raise HTTPException(status_code = 404, detail="Product not found")
    if carts.get(item.user_id) is None:
        carts[item.user_id] = []
    carts[item.user_id].append(item.model_dump())
    return {"message": "Item added successfully"}
# calculate the total price of a user's cart
@app.post("/checkout/{user_id}")
def checkout(user_id: int):
    total_price = 0
    summary = []
    # Check if the user has a cart
    if user_id not in carts:
        return {"items": [], "total": 0}
    user_cart_items = carts[user_id]
    for cart_item in user_cart_items:
        for product in products:
            if product["id"] == cart_item["product_id"]:
                subtotal = product["price"] * cart_item["quantity"]
                total_price = total_price+ subtotal
                summary.append({
                    "product_id": product["id"],
                    "name": product["name"],
                    "price": product["price"],
                    "quantity": cart_item["quantity"],
                    "subtotal": subtotal
                })
                break
    return {"items": summary, "total": total_price}