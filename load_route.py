from app.auth.routers import router as AuthRouter
from app.news.routers import router as NewsRouter
from app.newsletter.routers import router as NewsLetterRouter
from app.user.routers import router as UserRouter

ROUTE_LIST = [{
    'route': AuthRouter,
    'tags': ["Xác Thực"],
    'prefix': ''
}, {
    'route': UserRouter,
    'tags': ['User'],
    'prefix': '/user'
}, {
    'route': NewsLetterRouter,
    'tags': ['NewsLetters'],
    'prefix': '/newsletters'
}, {
    'route': NewsRouter,
    'tags': ['News'],
    'prefix': '/news'
}]
