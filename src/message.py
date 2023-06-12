class Message:
    def __init__(self, origin, destiny=None, move_info=None, receive_confirm=0):
        self.init_marker = "01110"
        self.origin = origin
        self.destiny = destiny
        self.move_info = move_info
        self.receive_confirm = receive_confirm
        self.end_marker = "10001"

    def __str__(self):
        return str(self.__dict__)