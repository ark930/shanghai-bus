class InvalidParameterException(Exception):
    def __init__(self, error, error_msg, status_code=None, payload=None):
        Exception.__init__(self)
        self.error = error
        self.error_msg = error_msg

        if status_code is not None:
            self.status_code = status_code
        self.payload = payload

    def to_dict(self):
        rv = dict(self.payload or ())
        rv['error'] = self.error
        rv['error_msg'] = self.error_msg

        return rv
