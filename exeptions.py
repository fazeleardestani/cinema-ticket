class UsernameExistsError(Exception):
    """Raised when trying to register with a username that is already taken."""
    pass

class InvalidPasswordError(Exception):
    """Raised when a password does not meet the security criteria (e.g., length)."""
    pass

class PasswordsDoesNotMatchError(Exception):
    """Raised when password and confirmation password do not match."""
    pass

class InvalidCredentialsError(Exception):
    """Raised for login attempts with wrong username or password."""
    pass

class InvalidBirthDateError(Exception):
    """Raised when a birthdate is invalid."""
    pass

class InvalidCvv2Error(Exception):
    """Raised when CVV2 is invalid."""
    pass

class NegativeAmountError(Exception):
    """Raised when Amount is negative."""
    pass

class InvalidAccountNumberError(Exception):
    """Raised when account number is invalid."""
    pass

class NotEnoughAmountError(Exception):
    """Raised when Amount is not enough."""
    pass

