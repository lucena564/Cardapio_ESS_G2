from typing import Optional
from pydantic import BaseModel
import sys
if sys.version_info.minor >= (10):
    from typing import Optional, Union

from typing import Optional, Union

class HttpResponseModel(BaseModel):
    message: str
    status_code: int

    if sys.version_info.minor >= (10):
        # Essa forma de declaração só funciona pro python 3.10+
        data: Optional[dict] | Optional[list] = None
    else:
        data: Optional[Union[dict, list]] = None

class HTTPResponses:

    """
    This class contains the basic HTTP responses for the API
    """

    @staticmethod
    def ITEM_NOT_FOUND() -> HttpResponseModel:
        return HttpResponseModel(
            message="Item not found",
            status_code=404,
        )

    @staticmethod
    def ITEM_FOUND() -> HttpResponseModel:
        return HttpResponseModel(
            message="Item found",
            status_code=200,
        )

    @staticmethod
    def ITEM_CREATED() -> HttpResponseModel:
        return HttpResponseModel(
            message="Item created",
            status_code=201,
        )

    @staticmethod
    def SERVER_ERROR() -> HttpResponseModel:
        return HttpResponseModel(
            message="Server error",
            status_code=500,
        )


    # TODO: implement other responses (item created, updated, deleted, etc)