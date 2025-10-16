from fastapi import FastAPI
import uvicorn

from src.auth.router import router as auth_router
from src.auth.dependencies import login_required

app = FastAPI()
app.include_router(auth_router, prefix="/auth", tags=["auth"])


@app.get("/")
@login_required
async def home(current_user):
    return f"Hello {current_user.first_name}"


if __name__ == '__main__':
    uvicorn.run("main:app", host="0.0.0.0", port=8003)