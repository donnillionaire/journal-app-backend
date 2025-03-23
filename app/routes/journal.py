from fastapi import APIRouter
# from controller.journal import router as journal_controller
from controllers.journal import router as journal_controller

router = APIRouter()
router.include_router(journal_controller)
