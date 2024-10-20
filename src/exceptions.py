"""File to handle exceptions"""

class ResumerGeneratorApiError(Exception):
    """Base exception class"""
    def __init__(self, message: str = "Service is unavailable", name: str = "ResumerGenerator"):
        self.message = message
        self.name = name
        super().__init__(self.message, self.name)

class ServiceError(ResumerGeneratorApiError):
    """Failures in external services or APIs like databases of third-party service"""

class EntityDoesNotExistError(ResumerGeneratorApiError):
    """When the database of any third-party service does not return anything"""

class UnprocessedRequestError(ResumerGeneratorApiError):
    """When the third-party service request returns an unprecedented result"""
    