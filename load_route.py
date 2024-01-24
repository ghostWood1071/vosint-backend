from app.auth.routers import router as AuthRouter
from app.dashboard.router import router as DashboardRouter
from app.information.route import router as InformationRouter
from app.manage_news.route import router as ManageNewsRouter
from app.news.routers import router as NewsRouter
from app.newsletter.routers import router as NewsLetterRouter
from app.proxy.route import router as ProxyRouter
from app.report.router import router as ReportRouter
from app.social.routers import router as SocialRouter
from app.social_media.routers import router as SocialMediaRouter
from app.upload.upload_file import router as UploadFileRouter
from app.user.routers import router as UserRouter
from vosint_ingestion.features.job.routers import router as Job
from app.resource_monitor.routers import router as ResourceMonitorRouter
from app.slave_activity.routers import router as SlaveActivityRouter
from app.subject.router import router as SubjectRouter
from vosint_ingestion.features.pipeline.routers import router as PipeLine
from app.nlp.routers import router as NLPRouter

ROUTE_LIST = [
    {"route": AuthRouter, "tags": ["Xác Thực"], "prefix": ""},
    {"route": UserRouter, "tags": ["User"], "prefix": "/user"},
    {"route": NewsLetterRouter, "tags": ["NewsLetters"], "prefix": "/newsletters"},
    {"route": NewsRouter, "tags": ["News"], "prefix": "/news"},
    {"route": UploadFileRouter, "tags": ["Upload"], "prefix": "/upload"},
    {"route": Job, "tags": ["Job"], "prefix": "/Job"},
    {"route": PipeLine, "tags": ["Pipeline"], "prefix": "/Pipeline"},
    {"route": NLPRouter, "tags": ["NLP"], "prefix": "/nlp"},
    {"route": ProxyRouter, "tags": ["Proxy"], "prefix": "/Proxy"},
    {"route": InformationRouter, "tags": ["Source"], "prefix": "/Source"},
    {
        "route": ManageNewsRouter,
        "tags": ["Source-group"],
        "prefix": "/Source-group",
    },
    {
        "route": SocialMediaRouter,
        "tags": ["Social-media"],
        "prefix": "/Social-media",
    },
    {"route": SocialRouter, "tags": ["Social"], "prefix": "/account-monitor"},
    {"route": ReportRouter, "tags": ["Report"], "prefix": "/report"},
    {
        "route": ResourceMonitorRouter,
        "tags": ["ResourceMonitor"],
        "prefix": "/resource-monitor",
    },
    {
        "route": SlaveActivityRouter,
        "tags": ["SlaveActivity"],
        "prefix": "/slave-activity",
    },
    {"route": DashboardRouter, "tags": ["Dashboard"], "prefix": "/dashboard"},
    {"route": SubjectRouter, "tags": ["Subject (chủ đề)"], "prefix":"/subject" }
]
