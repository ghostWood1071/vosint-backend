from bson.objectid import ObjectId


def newsletter_to_json(newsletter) -> dict:
    newsletter["_id"] = str(newsletter["_id"])

    if "user_id" in newsletter:
        newsletter["user_id"] = str(newsletter["user_id"])

    if "parent_id" in newsletter:
        newsletter["parent_id"] = str(newsletter["parent_id"])

    return newsletter


def newsletter_to_object_id(newsletter):
    if "user_id" in newsletter:
        if newsletter["user_id"] is None:
            newsletter.pop("user_id")
        else:
            newsletter["user_id"] = ObjectId(newsletter["user_id"])

    if "parent_id" in newsletter:
        if newsletter["parent_id"] is None:
            newsletter.pop("parent_id")
        else:
            newsletter["parent_id"] = ObjectId(newsletter["parent_id"])

    return newsletter
