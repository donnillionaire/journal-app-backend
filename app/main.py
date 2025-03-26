from fastapi import FastAPI
# from controllers.journal_controller import router as user_router
from routes import journal
from fastapi.middleware.cors import CORSMiddleware

from routes import auth


app = FastAPI()


# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins (change this to specific origins in production)
    allow_credentials=True,
    allow_methods=["*"],  # Allow all methods (GET, POST, etc.)
    allow_headers=["*"],  # Allow all headers
)

# Include controllers
# app.include_router(user_router)

app.include_router(auth.router)
app.include_router(journal.router)


# Run server: uvicorn main:app --reload
