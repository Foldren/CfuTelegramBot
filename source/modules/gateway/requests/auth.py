from dataclasses import dataclass


@dataclass
class SignInRequest:
    email: str
    password: str
