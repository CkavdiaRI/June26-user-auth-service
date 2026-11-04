class AppErrror(Exception):
    status_code = 500

class EmailTakenError(AppErrror):
    status_code = 409
    detail = "Email already taken"

class InvalidCredentialsError(AppErrror):
    status_code = 401
    detail = "Invalid credentials"