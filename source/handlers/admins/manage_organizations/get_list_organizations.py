from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from components.filters import IsAdminFilter
from components.keyboards_components.configurations.inline import cf_keyb_get_empty_list_organizations
from components.keyboards_components.generators import get_inline_keyb_markup
from components.keyboards_components.strings.inline import keyb_str_get_full_list_organizations
from components.texts.admins.manage_organizations import text_get_list_organizations
from services.sql_models_extends.organization import OrganizationExtend
from states.admin.steps_manage_organizations import StepsGetOrganizationsList

rt = Router()

# Фильтр на проверку категории доступа пользователя
rt.message.filter(IsAdminFilter(), F.chat.type == "private")
rt.callback_query.filter(IsAdminFilter(), F.message.chat.type == "private")


@rt.message(F.text == "ЮР Лица")
async def get_organizations_list(message: Message, state: FSMContext):
    await state.clear()
    await state.set_state(StepsGetOrganizationsList.get_list_organizations)

    organizations = await OrganizationExtend.get_admin_organizations(message.from_user.id)

    if organizations:
        keyboard = await get_inline_keyb_markup(
            list_names=[(e["name"] + ("  💤" if e["status"] == 0 else "")) for e in organizations],
            list_data=[e["id"] for e in organizations],
            callback_str="empty",  # change_organization
            number_cols=2,
            add_keyb_to_start=keyb_str_get_full_list_organizations
        )
    else:
        keyboard = cf_keyb_get_empty_list_organizations

    await message.answer(text=text_get_list_organizations, reply_markup=keyboard, parse_mode="html")
