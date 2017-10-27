from dreamrich import settings


class CorsMiddleware:

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        self.set_allow_hosts(response, request.META.get('HTTP_ORIGIN'))
        return response

    @staticmethod
    def set_allow_hosts(response, origin):
        if hasattr(settings,
                   'CORS_WHITELIST') and origin in settings.CORS_WHITELIST:
            response["Access-Control-Allow-Origin"] = origin
            response["Access-Control-Allow-Methods"] = "\
                         GET,\
                         OPTIONS,\
                         POST,\
                         PUT,\
                         DELETE"
            response["Access-Control-Max-Age"] = "1000"
            response["Access-Control-Allow-Headers"] = "\
                         Content-Type,\
                         Accept,\
                         X-CSRFToken"
            response["Access-Control-Allow-Credentials"] = 'true'
