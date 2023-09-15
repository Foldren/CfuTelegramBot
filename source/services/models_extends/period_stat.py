from models import PeriodStat, User


class PeriodStatApi:
    @staticmethod
    async def get_period_stat_users_with_flag_observer(name_stat, admin_id):
        period_stat = await PeriodStat.get(name=name_stat)
        users = await User.filter(admin_id=admin_id).all().values("chat_id", "fullname", "profession")
        observers = await period_stat.observers

        if observers:
            for i in range(0, len(users)):
                for obs in observers:
                    if users[i]['chat_id'] == obs.chat_id:
                        users[i]['observer'] = True
                        break

        # Меняем статус для пользователей у которых нет пункта observer
        for i in range(0, len(users)):
            if "observer" not in users[i].keys():
                users[i]['observer'] = False

        return users

    @staticmethod
    async def update_observers_by_name(ps_name: int, observers_id_list: list):
        period_stat = await PeriodStat.get(name=ps_name)
        users = await User.filter(chat_id__in=observers_id_list)
        await period_stat.observers.clear()  # Удаляем текущих наблюдателей
        await period_stat.observers.add(*users)  # Добавляем новых наблюдателей
        await period_stat.save()
