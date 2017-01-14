class BaseAiounfurlException(Exception):
    pass


class ResourceErrorResponse(BaseAiounfurlException):
    pass


class FetchPageException(BaseAiounfurlException):
    pass
