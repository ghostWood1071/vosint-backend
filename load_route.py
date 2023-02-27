from app.auth.routers import router as AuthRouter
from app.information.route import router as InformationRouter
from app.list_country.route import router as CountryRouter
from app.list_object.route import router as ObjectRouter
from app.list_organize.route import router as OrganizeRouter
from app.news.routers import router as NewsRouter
from app.newsletter.routers import router as NewsLetterRouter
from app.proxy.route import router as ProxyRouter
from app.upload.upload_file import router as UploadFileRouter
from app.user.routers import router as UserRouter
from vosint_ingestion.features.job.routers import router as Job
from vosint_ingestion.features.nlp.routers import router as Nlp
from vosint_ingestion.features.pipeline.routers import router as PipeLine

ROUTE_LIST = [
    {"route": AuthRouter, "tags": ["Xác Thực"], "prefix": ""},
    {"route": UserRouter, "tags": ["User"], "prefix": "/user"},
    {"route": NewsLetterRouter, "tags": ["NewsLetters"], "prefix": "/newsletters"},
    {"route": NewsRouter, "tags": ["News"], "prefix": "/news"},
    {"route": OrganizeRouter, "tags": ["Organize"], "prefix": "/organize"},
    {"route": CountryRouter, "tags": ["Country"], "prefix": "/country"},
    {"route": UploadFileRouter, "tags": ["Upload"], "prefix": "/upload"},
    {"route": ObjectRouter, "tags": ["Object"], "prefix": "/object"},
    {"route": Job, "tags": ["Job"], "prefix": "/Job"},
    {"route": PipeLine, "tags": ["Pipeline"], "prefix": "/Pipeline"},
    {"route": Nlp, "tags": ["Nlp"], "prefix": "/Nlp"},
    {"route": ProxyRouter, "tags": ["Proxy"], "prefix": "/Proxy"},
    {"route": InformationRouter, "tags": ["Infor"], "prefix": "/Infor"},
]
