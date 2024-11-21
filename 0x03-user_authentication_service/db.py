#!/usr/bin/env python3
"""
DB module
"""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session
from sqlalchemy.exc import InvalidRequestError
from sqlalchemy.orm.exc import NoResultFound
from user import Base, User


class DB:
    """DB class for database interactions."""

    def __init__(self) -> None:
        """Initialize a new DB instance."""
        self._engine = create_engine("sqlite:///a.db", echo=False)
        Base.metadata.drop_all(self._engine)
        Base.metadata.create_all(self._engine)
        self.__session = None

    @property
    def _session(self) -> Session:
        """Memoized session object."""
        if self.__session is None:
            DBSession = sessionmaker(bind=self._engine)
            self.__session = DBSession()
        return self.__session

    def add_user(self, email: str, hashed_password: str) -> User:
        """
        Add a new user to the database.

        Args:
            email (str): The user's email.
            hashed_password (str): The hashed password.

        Returns:
            User: The newly created user object.
        """
        new_user = User(email=email, hashed_password=hashed_password)
        self._session.add(new_user)
        self._session.commit()  # Save the new user in the database.
        return new_user

    def find_user_by(self, **kwargs) -> User:
        """
        Find a user in the database using the provided keyword arguments.

        Args:
            **kwargs: Arbitrary keyword arguments for user attributes
            (e.g., email="test@test.com").

        Returns:
            User: The first user matching the criteria.

        Raises:
            NoResultFound: If no user matches the criteria.
            InvalidRequestError: If invalid arguments are passed
            (e.g., non-existent columns).
        """
        try:
            # Query the User model using the provided keyword arguments
            user = self._session.query(User).filter_by(**kwargs).one()
            return user
        except NoResultFound:
            # Raise NoResultFound if no user is found
            raise NoResultFound("No user found matching the criteria.")
        except InvalidRequestError:
            # Raise InvalidRequestError if the query is invalid
            raise InvalidRequestError("Invalid query arguments.")

    def update_user(self, user_id: int, **kwargs) -> None:
        """
        Update an existing user's attributes in the database.

        Args:
            user_id (int): The user's ID.
            **kwargs: Arbitrary keyword arguments for user attributes
            (e.g., hashed_password="newPwd").

        Raises:
            ValueError: If an invalid user attribute is passed.
        """
        user = self.find_user_by(id=user_id)

        # List of valid user attributes
        valid_attributes = ['email', 'hashed_password',
                            'session_id', 'reset_token']

        for key, value in kwargs.items():
            # Check if the key is a valid user attribute
            if key not in valid_attributes:
                raise ValueError(f"Invalid attribute: {key}")
            # Update the user attribute
            setattr(user, key, value)

        # Commit changes to the database
        self._session.commit()
