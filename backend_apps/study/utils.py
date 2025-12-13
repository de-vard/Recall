import uuid
from bson import Binary, ObjectId
from datetime import datetime


def mongo_to_json(doc: dict) -> dict:
    """
        Приводит Mongo-документ к JSON-совместимому виду
    """
    result = {}

    for key, value in doc.items():
        if isinstance(value, Binary):
            result[key] = str(uuid.UUID(bytes=value))
        elif isinstance(value, ObjectId):
            result[key] = str(value)
        elif isinstance(value, datetime):
            result[key] = value.isoformat()
        else:
            result[key] = value

    return result
