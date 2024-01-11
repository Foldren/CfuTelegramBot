from dataclasses import dataclass


@dataclass
class SignInRequest:
    __slots__ = {"email", "password"}
    email: str
    password: str
