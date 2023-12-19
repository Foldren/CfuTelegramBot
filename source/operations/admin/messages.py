from dataclasses import dataclass
from components.rpc import MessageRpc


@dataclass
class AuthorizationMessage(MessageRpc):
    email: str = None
    password: str = None

    def __init__(self, message_text: str):
        super()._init_message(self, message_text)
