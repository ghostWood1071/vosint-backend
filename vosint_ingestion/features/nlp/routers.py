from fastapi import APIRouter
from fastapi.responses import JSONResponse

from .nlpcontroller import NlpController

router = APIRouter()

nlp_controller = NlpController()

@router.get('/api/nlp_chude/')
def nlp_chude(user_id, title, order=None, page_number=None, page_size=None):
    return JSONResponse(nlp_controller.nlp_chude(user_id, title, order, page_number, page_size))