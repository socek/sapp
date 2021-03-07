"""
This hack allows to encode uuid4 and datetime in json
"""
from inspect import isabstract
from logging import getLogger

from qq.plugins.jsonhack import encoders
from qq.plugins.jsonhack.errors import UnknownObjectError

logger = getLogger(__name__)

ENCODERS_CACHE = set()


def get_encoders():
    return ENCODERS_CACHE


def is_encoder(obj: object) -> bool:
    return issubclass(obj, encoders.Encoder) and not isabstract(obj)


def init_encoders(finder):
    """
    Get all encoders from qq.plugins.jsonhack.encoders and from all dataclasses
    from the provided finder.
    """
    for name in dir(encoders):
        if name.startswith("_"):
            continue
        element = getattr(encoders, name)
        try:
            if is_encoder(element):
                add_encoder(element())
        except TypeError:
            continue

    if finder:
        # search for all dataclasses and generate encoder
        for encoder in encoders.encoder_for(finder.find()):
            add_encoder(encoder)


def object_hook(obj):
    if "_type" not in obj:
        return obj

    for encoder in get_encoders():
        if encoder.is_decodable(obj):
            return encoder.decode(obj)
    raise UnknownObjectError(obj)


def add_encoder(encoder):
    ENCODERS_CACHE.add(encoder)