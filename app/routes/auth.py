from fastapi import APIRouter
from app.controllers.auth import router as auth_controller

router = APIRouter()
router.include_router(auth_controller)
