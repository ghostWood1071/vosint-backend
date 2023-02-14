from app.auth.auth import router as AuthRouter
from app.user.routers import router as UserRouter
from app.newsletter.routers import router as NewsLetterRouter

ROUTE_LIST = [{
    'route': AuthRouter,
    'tags': ["Xác Thực"],
    'prefix': '/auth'
}, {
    'route': UserRouter,
    'tags': ['User'],
    'prefix': '/user'
}, {
    'route': NewsLetterRouter,
    'tags': ['NewsLetters'],
    'prefix': '/newsletters'
}]
