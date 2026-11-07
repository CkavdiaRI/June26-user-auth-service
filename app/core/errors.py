class AppError(Exception):
    status_code = 500

class EmailTakenError(AppError):
    status_code = 409
    detail = "Email already taken"

class InvalidCredentialsError(AppError):
    status_code = 401