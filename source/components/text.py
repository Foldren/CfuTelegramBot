from dataclasses import dataclass


@dataclass
class Text:
    params_from_new_str: str = "<i>(каждый параметр вводите с новой строки, как в примере ниже)</i>"

    @staticmethod
    def example(*args):
        arguments = '\n'.join([e for e in args])
        return f"\n<b>Пример</b> (просто нажмите 👇):\n<code>{arguments}</code>"

    @staticmethod
    def title(name: str):
        return f"<b>{name}</b>\n"
