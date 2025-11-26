import uvicorn
from fastapi import FastAPI

from src.auth.dependencies import login_required
from src.auth.router import router as auth_router
from src.cart.router import router as cart_router
from src.products.api.categories import router as category_router
from src.products.api.products import router as product_router

app = FastAPI()
app.include_router(auth_router, prefix="/auth", tags=["auth"])
app.include_router(product_router, prefix="/products", tags=["products"])
app.include_router(category_router, prefix="/categories", tags=["categories"])
app.include_router(cart_router, prefix="/carts", tags=["carts"])


@app.get("/")
@login_required
async def home(current_user):
    return f"Hello {current_user.first_name}"


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8003)
