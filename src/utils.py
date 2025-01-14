import logging
import uuid
from datetime import datetime

from fastapi.responses import JSONResponse

logger = logging.getLogger(__name__)


def create_response(content, code):
    return JSONResponse(content=content, status_code=code)


def get_current_time():
    return datetime.now().strftime('%Y-%m-%d %H:%M:%S')


def objects_to_json(objs):
    """
    Convert objects to json
    :param objs: List of orm objects
    :return: JSON objects
    """
    json_objs = []
    for obj in objs:
        json_obj = dict()
        for key in obj.__dict__.keys():
            if key.startswith(('_', '__')):
                continue
            value = getattr(obj, key)
            if isinstance(value, uuid.UUID):
                json_obj[key] = str(value)
            elif isinstance(value, datetime):
                json_obj[key] = str(value)
            else:
                json_obj[key] = value

        json_objs.append(json_obj)
    return json_objs
