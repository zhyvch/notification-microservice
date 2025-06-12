import logging

from fastapi import FastAPI
from fastapi.responses import ORJSONResponse

logger = logging.getLogger(__name__)


def exception_registry(app: FastAPI) -> None:
    ...
