from aiogram_dialog import Dialog, LaunchMode
from windows.admin.categories.create import select_name
from windows.admin.categories.get import main_categories, child_categories
from windows.admin.counterparties.get import counterparties
from windows.admin.menu import main
from windows.not_authorized.authorization import start, authorization


# authorization
authorization = Dialog(start, authorization, launch_mode=LaunchMode.ROOT)


# menu
change_menu = Dialog(main, launch_mode=LaunchMode.ROOT)


# category
get_categories = Dialog(main_categories, child_categories, launch_mode=LaunchMode.SINGLE_TOP)

create_category = Dialog(select_name, launch_mode=LaunchMode.SINGLE_TOP)


# counterparty
get_counterparties = Dialog(counterparties, launch_mode=LaunchMode.SINGLE_TOP)
