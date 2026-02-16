class EmailAlreadyRegisteredError(Exception):
    """Raised when attempting to sign up with an existing email."""


class InvalidCredentialsError(Exception):
    """Raised when login credentials are invalid."""

