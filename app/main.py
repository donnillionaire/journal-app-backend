from fastapi import FastAPI
from controllers.user_controller import router as user_router

app = FastAPI()

# Include controllers
app.include_router(user_router)

# Run server: uvicorn main:app --reload
