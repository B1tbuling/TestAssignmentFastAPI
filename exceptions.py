class ValidationException(Exception):
    def __init__(self, error, *args, **kwargs):
        self.error = error
        super().__init__(*args, **kwargs)