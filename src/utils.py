import logging
import re
import uuid
from datetime import datetime
from enum import Enum
from json import load
from typing import Optional, Match, List, Dict

from fastapi.responses import JSONResponse

from src.constants import LOGGER_CONFIG

logger = logging.getLogger(__name__)


class ClaimStatus(Enum):
    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"


def get_logger_config():
    with open(LOGGER_CONFIG, "r") as f:
        config_dict = load(f)
    return config_dict


def get_error_object(message, error=None):
    error_dict = dict(message=message)
    if error:
        error_dict['error'] = str(error)
    return error_dict


def get_error_content(errors: List[Dict]):
    return {
        "errors": errors
    }


def create_response(content, code):
    return JSONResponse(content=content, status_code=code)


def get_current_time():
    return datetime.now().strftime('%Y-%m-%d %H:%M:%S')


def map_objs_to_dict(objs, key_field="id"):
    """
    Convert objects to json
    :param objs: List of orm objects
    :param key_field: Field to be used as key in json payload
    :return: JSON objects
    """
    json_payload = dict()
    for obj in objs:
        json_obj = map_obj_to_dict(obj)
        if key_field in json_obj:
            json_payload[json_obj[key_field]] = json_obj
    return json_payload


def map_obj_to_dict(obj):
    keys = obj.__dict__.keys()
    obj_dict = dict()
    for key in keys:
        if key.startswith(('_', '__')):
            continue
        value = getattr(obj, key)
        if isinstance(value, uuid.UUID):
            obj_dict[key] = str(value)
        elif isinstance(value, datetime):
            obj_dict[key] = str(value)
        else:
            obj_dict[key] = value
    return obj_dict


def parse_db_integrity_error_message(error_message):
    """
    Parses an error message to extract the type of error, key, and value.
    """
    error_dict = dict()

    error_type_match: Optional[Match[str]] = re.search(r"<class '([^']+)'>",
                                                       error_message)
    if error_type_match:
        error_dict['error_type'] = error_type_match.group(1).split('.')[-1]
    else:
        error_dict['error_type'] = "Unknown"

    key_value_match: Optional[Match[str]] = re.search(
        r'Key \((.*?)\)=\((.*?)\)', error_message)
    if key_value_match:
        error_dict['key'] = key_value_match.group(1)
        error_dict['value'] = key_value_match.group(2)

    return error_dict
