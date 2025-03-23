from fastapi import FastAPI
from controllers.user_controller import router as user_router
from routes import auth

app = FastAPI()

# Include controllers
# app.include_router(user_router)

app.include_router(auth.router)

# Run server: uvicorn main:app --reload
