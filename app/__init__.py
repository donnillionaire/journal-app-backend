from fastapi import FastAPI

app = FastAPI()

# You can import your routes here
from app.routes import auth  # Ensure this uses absolute import

app.include_router(auth.router)
