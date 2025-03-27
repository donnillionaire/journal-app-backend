from fastapi import FastAPI
# from controllers.journal_controller import router as user_router
from app.routes import journal
from fastapi.middleware.cors import CORSMiddleware

from app.routes import auth
from app.routes import admin

app = FastAPI()


# oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")



# Configure CORS
app.add_middleware(
    CORSMiddleware,
    # allow_origins=["*"],  # Allow all origins (change this to specific origins in production)
    allow_origins=["http://localhost:5173"],  # React frontend URL
    allow_credentials=True,
    allow_methods=["*"],  # Allow all methods (GET, POST, etc.)
    allow_headers=["*"],  # Allow all headers
)

# Include controllers
# app.include_router(user_router)

app.include_router(auth.router)
app.include_router(journal.router)
app.include_router(admin.router)



# Run server: uvicorn main:app --reload
