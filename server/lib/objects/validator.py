class ResponseObject(object):
    pass


class RequestValidator:

    expected_status_code = None
    target_source = None
    params = {}

    endpoint = None
    message = None
    error = None
    data = None

    def __init__(self,
                 ):

        pass

    def bad_request(self):
        bad_request_object = ResponseObject()
        bad_request_object.expected_status_code = 400
        bad_request_object.response = {
            "status": "error",
            "code": 400,
            "message": self.message,
            "error": self.error
        }
        return bad_request_object

    def internal_server_error(self):
        internal_server_error_object = ResponseObject()
        internal_server_error_object.expected_status_code = 500
        internal_server_error_object.response = {
            "status": "error",
            "code": 500,
            "message": self.message,
            "error": self.error
        }
        return internal_server_error_object

    def valid_request(self):
        self.expected_status_code = 200
        self.message = "Valid request"
        return self

