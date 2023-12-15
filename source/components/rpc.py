from dataclasses import dataclass, fields


class MessageRpc:
    @staticmethod
    def _init_message(cls: dataclass, message_text: str):
        list_data = message_text.split("\n")
        i = 0

        for field in fields(cls):
            if field.name != "message_text":
                setattr(cls, field.name, list_data[i])
                i += 1