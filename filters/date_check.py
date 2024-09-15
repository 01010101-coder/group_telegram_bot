from datetime import datetime, timedelta

# Ключевые слова и их смещения
key_words = {
    'сегодня': 0,
    'завтра': 1,
    'послезавтра': 2
}

# Месяцы с поддержкой различных падежей
months = {
    'январь': 1, 'февраль': 2, 'март': 3, 'апрель': 4, 'май': 5, 'июнь': 6,
    'июль': 7, 'август': 8, 'сентябрь': 9, 'октябрь': 10, 'ноябрь': 11, 'декабрь': 12,
    'января': 1, 'февраля': 2, 'марта': 3, 'апреля': 4, 'мая': 5, 'июня': 6,
    'июля': 7, 'августа': 8, 'сентября': 9, 'октября': 10, 'ноября': 11, 'декабря': 12
}


def parse_date(text):
    text = text.lower().strip()

    # Проверка ключевых слов
    if text in key_words:
        date = datetime.now() + timedelta(days=key_words[text])
        return date.strftime("%d.%m.%Y")

    # Проверка форматов dd.mm или dd.mm.yyyy
    try:
        if "." in text:
            if len(text.split(".")) == 2:
                date = datetime.strptime(text + f".{datetime.now().year}", "%d.%m.%Y")
                # Проверка, если дата уже прошла в текущем году
                if date < datetime.now():
                    date = date.replace(year=datetime.now().year + 1)
            else:
                date = datetime.strptime(text, "%d.%m.%Y")
            return date.strftime("%d.%m.%Y")
    except ValueError:
        pass

    # Проверка формата 'день месяц'
    words = text.split()
    if len(words) == 2:
        try:
            day = int(words[0])
            if words[1] in months and 1 <= day <= 31:
                month = months[words[1]]
                date = datetime(datetime.now().year, month, day)
                # Проверка, если дата уже прошла в текущем году
                if date < datetime.now():
                    date = date.replace(year=datetime.now().year + 1)
                return date.strftime("%d.%m.%Y")
        except ValueError:
            pass

    # Если дата не распознана
    return "Неправильный формат даты"

print(parse_date('абоба'))
