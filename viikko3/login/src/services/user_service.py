from entities.user import User
from repositories.user_repository import (
    user_repository as default_user_repository
)


class UserInputError(Exception):
    pass


class AuthenticationError(Exception):
    pass


class UserService:
    def __init__(self, user_repository=default_user_repository):
        self._user_repository = user_repository

    def check_credentials(self, username, password):
        if not username or not password:
            raise UserInputError("Username and password are required")

        user = self._user_repository.find_by_username(username)

        if not user or user.password != password:
            raise AuthenticationError("Invalid username or password")

        return user

    def create_user(self, username, password, password_confirmation):
        self.validate(username, password, password_confirmation)

        user = self._user_repository.create(
            User(username, password)
        )

        return user

    def validate(self, username, password, password_confirmation):
        if not username or not password:
            raise UserInputError("Username and password are required")

        if len(username) < 4:
            raise UserInputError("Username must be at least 4 characters long")
        
        if len(password) < 4:
            raise UserInputError("Password must be at least 4 characters long")
        
        allowed = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!@#$%&*"
        if all(a in allowed for a in password) is False:
            raise UserInputError("Password contains invalid characters")
    
        if password != password_confirmation:
            raise UserInputError("Password and password confirmation do not match")
        
        existing = self._user_repository.find_by_username(username)
        if existing:
            raise UserInputError("Username is already taken")


user_service = UserService()
