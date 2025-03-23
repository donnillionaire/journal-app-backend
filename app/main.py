from fastapi import FastAPI
# from controllers.journal_controller import router as user_router
from routes import journal
from routes import auth


app = FastAPI()

# Include controllers
# app.include_router(user_router)

app.include_router(auth.router)
app.include_router(journal.router)


# Run server: uvicorn main:app --reload
