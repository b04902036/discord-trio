class WrongParam(Exception):
    def __init__(self, msg):
        self.msg = msg
        print("wrong parameter")

class InvalidMove(Exception):
    def __init__(self, msg):
        self.msg = msg
        print("invalid movement")

class InternalError(Exception):
    def __init__(self, msg):
        self.msg = msg
        print("internal error")