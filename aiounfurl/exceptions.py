class BaseAiounfurlException(Exception):
    pass


class InvalidURLException(BaseAiounfurlException):
    pass


class InvalidOEmbedEndpoint(BaseAiounfurlException):
    pass


class FetchPageException(BaseAiounfurlException):
    pass
