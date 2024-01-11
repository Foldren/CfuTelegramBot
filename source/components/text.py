from dataclasses import dataclass
from aiogram.utils.markdown import hitalic, hcode, hbold


@dataclass
class Text:
    params_from_new_str: str = hitalic("(каждый параметр вводите с новой строки, как в примере ниже)")

    @staticmethod
    def example(*args):
        arguments = '\n'.join([e for e in args])
        return "\n" + hbold("Пример") + " (просто нажмите 👇):" + "\n" + hcode(arguments)

    @staticmethod
    def title(text: str):
        return hbold(text) + "\n"
