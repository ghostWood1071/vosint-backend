from fastapi import APIRouter
from fastapi.responses import JSONResponse

from .pipelinecontroller import PipelineController

router = APIRouter()
pipeline_controller = PipelineController()


@router.get('/api/get_action_infos')
def get_action_infos():
    return JSONResponse(pipeline_controller.get_action_infos())


@router.get('/api/get_pipeline_by_id/{id}')
def get_pipeline_by_id(id: str):
    return JSONResponse(pipeline_controller.get_pipeline_by_id(id))


@router.get('/api/get_pipelines')
def get_pipelines():
    return JSONResponse(pipeline_controller.get_pipelines())


@router.post('/api/put_pipeline')
def put_pipeline(pipeline_obj):
    return JSONResponse(pipeline_controller.put_pipeline(pipeline_obj))


@router.post('/api/clone_pipeline/{from_id}')
def clone_pipeline(from_id: str):
    return JSONResponse(pipeline_controller.clone_pipeline(from_id))


@router.delete('/api/delete_pipeline/{id}')
def delete_pipeline_by_id(id: str):
    return JSONResponse(pipeline_controller.delete_pipeline_by_id(id))
