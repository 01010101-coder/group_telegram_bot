from apscheduler.schedulers.asyncio import AsyncIOScheduler
from datetime import datetime
import pytz

from db.netnapare_db import SkipTable
from db.users_db import UsersTable

skip_db = SkipTable()
users_db = UsersTable()

pairs_time = {
    1: "08:15",
    2: "09:45",
    3: "11:15",
    4: "13:00",
    5: "14:30"
}


# Асинхронная функция для проверки отсутствующих студентов
async def check_absent_students_for_time(pair_time):
    try:
        current_date = datetime.now(pytz.timezone('Europe/Moscow')).strftime("%d.%m.%Y")

        absent_students = await skip_db.get_absent_students_by_date(current_date)

        current_absent_students = []

        for student in absent_students:
            absent_pairs = eval(student['pairs'])

            for pair in absent_pairs:
                if pairs_time[pair] == pair_time:
                    current_absent_students.append({
                        'tg_id': student['tg_id'],
                        'time': pairs_time[pair],
                        'reason': student['description']
                    })

        # Если есть отсутствующие студенты, отправляем им сообщение через бота
        # if current_absent_students:
        #     for student in current_absent_students:
        #         message = f"Напоминание: Вы отсутствуете на паре в {student['time']}.\nПричина: {student['reason']}"
        #         await bot.send_message(student['tg_id'], message)

    except Exception as e:
        print(f"Ошибка при проверке отсутствующих студентов: {e}")


# Функция для планирования задач на конкретное время начала пар
def schedule_pair_checks():
    scheduler = AsyncIOScheduler()

    for pair, time_str in pairs_time.items():
        hour, minute = map(int, time_str.split(":"))

        scheduler.add_job(check_absent_students_for_time, 'cron', hour=hour, minute=minute, args=[time_str],
                          timezone='Europe/Moscow')

    # Запуск планировщика
    scheduler.start()


schedule_pair_checks()
