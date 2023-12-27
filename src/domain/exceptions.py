class RepositoryErrorException(Exception):
    """Custom exception for repository layer errors."""
    def __init__(self, message, status_code=500):
        self.message = message
        self.status_code = status_code
        super().__init__(message)
