class DispatchRequest(object):
    def __init__(self, request, args, kwargs):
        self.request = request
        self.args = args
        self.kwargs = kwargs

    def do(self):
        assert self.request.path == "/test_dispatch_request/1/test/"
        assert self.args == ()
        assert self.kwargs == {"id": 1, "word": "test"}
        return "<h1>OK</h1>"
