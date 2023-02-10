from app.auth.auth import router as AuthRouter
from app.user.routers import router as UserRouter

ROUTE_LIST = [{
    'route': AuthRouter,
    'tags': ["Xác Thực"],
    'prefix': '/auth'
}, {
    'route': UserRouter,
    'tags': ['User'],
    'prefix': '/user'
}]
