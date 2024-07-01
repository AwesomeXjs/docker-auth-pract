from fastapi import APIRouter

from .task.view import router as task_router
from .user.view import router as user_router
from .jwt_auth.views import router as jwt_router
from .basic_auth.views import router as basic_auth_router
from .header_auth.views import router as header_auth_router
from .cookie_auth.views import router as cookie_auth_router

router = APIRouter(prefix="/v1")
router.include_router(task_router)
# router.include_router(basic_auth_router)
# router.include_router(header_auth_router)
# router.include_router(cookie_auth_router)
# router.include_router(jwt_router)
router.include_router(user_router)
