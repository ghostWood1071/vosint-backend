from flask import Blueprint

from .pipelinecontroller import PipelineController

feature = Blueprint("Pipeline", __name__)
pipeline_controller = PipelineController()


@feature.route("/api/get_action_infos", methods=["GET"])
def get_action_infos():
    return pipeline_controller.get_action_infos()


@feature.route("/api/get_pipeline_by_id/<id>", methods=["GET"])
def get_pipeline_by_id(id: str):
    return pipeline_controller.get_pipeline_by_id(id)


@feature.route("/api/get_pipelines", methods=["GET"])
def get_pipelines():
    return pipeline_controller.get_pipelines()


@feature.route("/api/put_pipeline", methods=["POST"])
def put_pipeline():
    return pipeline_controller.put_pipeline()


@feature.route("/api/clone_pipeline/<from_id>", methods=["POST"])
def clone_pipeline(from_id: str):
    return pipeline_controller.clone_pipeline(from_id)


@feature.route("/api/delete_pipeline/<id>", methods=["DELETE"])
def delete_pipeline_by_id(id: str):
    return pipeline_controller.delete_pipeline_by_id(id)
