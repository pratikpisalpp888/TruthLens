"""
TruthLens — Exception Hierarchy.

Custom exceptions for the application.
"""

from fastapi import status

class TruthLensException(Exception):
    """Base exception for all custom errors."""
    def __init__(self, detail: str, error_code: str = "INTERNAL_ERROR", status_code: int = status.HTTP_500_INTERNAL_SERVER_ERROR):
        self.detail = detail
        self.error_code = error_code
        self.status_code = status_code
        super().__init__(self.detail)

class DatabaseException(TruthLensException):
    def __init__(self, detail: str, error_code: str = "DB_ERROR"):
        super().__init__(detail, error_code, status.HTTP_503_SERVICE_UNAVAILABLE)

class AuthenticationException(TruthLensException):
    def __init__(self, detail: str, error_code: str = "AUTH_ERROR"):
        super().__init__(detail, error_code, status.HTTP_401_UNAUTHORIZED)

class AuthorizationException(TruthLensException):
    def __init__(self, detail: str, error_code: str = "FORBIDDEN"):
        super().__init__(detail, error_code, status.HTTP_403_FORBIDDEN)

class DocumentException(TruthLensException):
    def __init__(self, detail: str, error_code: str = "DOCUMENT_ERROR"):
        super().__init__(detail, error_code, status.HTTP_400_BAD_REQUEST)

class AnalysisException(TruthLensException):
    def __init__(self, detail: str, error_code: str = "ANALYSIS_ERROR"):
        super().__init__(detail, error_code, status.HTTP_500_INTERNAL_SERVER_ERROR)

class LLMException(TruthLensException):
    def __init__(self, detail: str, error_code: str = "LLM_ERROR"):
        super().__init__(detail, error_code, status.HTTP_503_SERVICE_UNAVAILABLE)

class LLMError(TruthLensException):
    def __init__(self, message: str = "LLM Error", detail: str = None):
        super().__init__(detail=message, error_code="LLM_ERROR", status_code=status.HTTP_503_SERVICE_UNAVAILABLE)
        self.extended_detail = detail

class LLMTimeoutError(LLMError):
    def __init__(self, message: str = "LLM Timeout", detail: str = None):
        super().__init__(message=message, detail=detail)
        self.error_code = "LLM_TIMEOUT"

class StorageException(TruthLensException):
    def __init__(self, detail: str, error_code: str = "STORAGE_ERROR"):
        super().__init__(detail, error_code, status.HTTP_503_SERVICE_UNAVAILABLE)

class ValidationException(TruthLensException):
    def __init__(self, detail: str, error_code: str = "VALIDATION_ERROR"):
        super().__init__(detail, error_code, status.HTTP_422_UNPROCESSABLE_ENTITY)

class ResourceNotFoundError(TruthLensException):
    def __init__(self, detail: str = "Resource not found", error_code: str = "NOT_FOUND"):
        super().__init__(detail, error_code, status.HTTP_404_NOT_FOUND)

class NotFoundError(ResourceNotFoundError):
    pass

class FileNotFoundInStorageError(ResourceNotFoundError):
    def __init__(self, detail: str = "File not found in storage", error_code: str = "FILE_NOT_FOUND"):
        super().__init__(detail, error_code)

