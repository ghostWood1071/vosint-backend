from models.dtos import BaseDto


class PipelineForListDto(BaseDto):
    def __init__(self, record: dict):
        super().__init__(record)
        self.name = record["name"]
        self.enabled = record["enabled"]
        self.actived = record["actived"]
        self.schema = record["schema"]
        # self.working = record["working"]
        # self.last_success = record["last_success"]

    def to_dict(self) -> dict:
        return {
            **super().to_dict(),
            "name": self.name,
            "enabled": self.enabled,
            "actived": self.actived,
            "schema": self.schema,
            # "working": self.working,
            # "last_success": self.last_success,
        }
