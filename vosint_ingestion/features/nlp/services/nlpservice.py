from bson.objectid import ObjectId
from models import HBaseRepository, MongoRepository


class NlpService:
    def __init__(self):
        self.__mongo_repo = MongoRepository()

    def get_id_chude(self, user_id: str, title_chu_de: str):
        a = self.__mongo_repo.get_one(
            collection_name="newsletter",
            filter_spec={"title": title_chu_de, "user_id": user_id},
            filter_other={"_id": 1},
        )
        return str(a["_id"])

    def nlp_chude(self, user_id: str, title_chu_de: str, order_spec, pagination_spec):
        id_chude = self.get_id_chude(ObjectId(user_id), title_chu_de)

        query = {"data:class_chude": {"$regex": ".*" + id_chude + ".*"}}
        results = self.__mongo_repo.get_many_d(
            "News",
            filter_spec=query,
            order_spec=order_spec,
            pagination_spec=pagination_spec,
            filter_other={"_id": 0},
        )

        return results
