from aiogram_dialog import Dialog, LaunchMode
from operations.admin.change_menu.windows import main
from operations.not_authorized.authorization.windows import start, authorization
from operations.admin.manage.categories.get.windows import get_categories


# menu
change_menu = Dialog(main, launch_mode=LaunchMode.ROOT)

# category
get_categories = Dialog(get_categories, launch_mode=LaunchMode.SINGLE_TOP)


