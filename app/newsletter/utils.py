from bson.objectid import ObjectId


def newsletter_to_json(newsletter) -> dict:
    newsletter['_id'] = str(newsletter['_id'])

    if "user_id" in newsletter:
        newsletter["user_id"] = str(newsletter["user_id"])

    if "parent_id" in newsletter:
        newsletter["parent_id"] = str(newsletter["parent_id"])

    return newsletter


def newsletter_to_ojbectId(newsletter):
    if "user_id" in newsletter:
        newsletter["user_id"] = ObjectId(newsletter["user_id"])

    if "parent_id" in newsletter:
        newsletter["parent_id"] = ObjectId(newsletter["parent_id"])

    return newsletter
