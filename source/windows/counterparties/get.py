from aiogram_dialog import Window
from aiogram_dialog.widgets.kbd import Start, Cancel, Row, ScrollingGroup, Select
from aiogram_dialog.widgets.text import Const, Multi, Format
from getters.counterparties import get_counterparties
from states.counterparties import GetCounterpartiesStates, DeleteCounterpartiesStates, CreateCounterpartyStates, \
    UpdateCounterpartyStates


counterparties = Window(
    Multi(
        Const("<b>Контрагенты</b>"),
        Const("💼 Здесь вы можете настроить контрагентов вашего бота Управляйки."),
        Const(f"<u>Кнопки управления:</u>\n"
              f"➕ - добавить контрагента.\n"
              f"✏️ - редактировать контрагентов.\n"
              f"🗑 - удалить контрагентов.\n"
              f"⛔️ - отменить операцию."),
        sep="\n\n"
    ),
    Row(
        Start(id="create_counterparty", text=Const("➕"), state=CreateCounterpartyStates.write_params),
        Start(id="update_counterparty", text=Const("✏️"), state=UpdateCounterpartyStates.select_counterparty),
        Start(id="delete_counterparties", text=Const("🗑"), state=DeleteCounterpartiesStates.select_counterparties),
        Cancel(text=Const("⛔️"))
    ),
    ScrollingGroup(
        Select(
            text=Format("{item[inn]} - {item[name]}"),
            items='counterparties',
            item_id_getter=lambda item: item['id'],
            id="counterparty"
        ),
        id="counterparties_sc",
        width=1,
        height=4,
        hide_on_single_page=True,
    ),
    state=GetCounterpartiesStates.render,
    getter=get_counterparties
)
