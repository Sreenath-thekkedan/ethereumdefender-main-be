class BlockNotFoundException(Exception):
    def __init__(self, message="Block not found"):
        self.message = message
        super().__init__(self.message)