import json
def error_handler(err):
    return json.dumps({ 'message': err.message }), err.status_code

class BaseException(Exception):
    def __init__(self, message, status_code=None, payload=None):
        Exception.__init__(self)
        self.message = message
        if status_code is not None:
            self.status_code = status_code
        self.payload = payload

    def to_dict(self):
        rv = dict(self.payload or ())
        rv['message'] = self.message
        return rv

class NotFoundException(BaseException):
    status_code = 404
    
class DuplicateItemException(BaseException):
    status_code = 409