from fastapi import APIRouter
from controllers.auth import router as auth_controller

router = APIRouter()
router.include_router(auth_controller)
