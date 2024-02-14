from dataclasses import dataclass
from aiogram.utils.markdown import hitalic, hcode, hbold


@dataclass
class Text:
    params_from_new_str: str = hitalic("(каждый параметр вводите с новой строки, как в примере ниже)")

    @staticmethod
    def example(*args):
        arguments = '\n'.join([e for e in args])
        return hbold("Пример") + " (просто нажмите 👇):" + "\n" + hcode(arguments)

    @staticmethod
    def title(text: str, step: int = 1, with_step: bool = False):
        if with_step:
            result_text = hbold(f"{text}: ") + hitalic(f"(шаг {step})")
        else:
            result_text = hbold(text) + "\n"

        return result_text


