key_words = ['сегодня', 'завтра', 'послезавтра']
months = ['январь', 'февраль', 'март', 'апрель', 'май', 'июнь', 'июль', 'август', 'сентябрь', 'октябрь', 'ноябрь', 'декабрь',
          'января', 'февраля', 'марта', 'апреля', 'мая', 'июня', 'июля', 'августа', 'сентября', 'октября', 'ноября', 'декабря']


def check_for_invalid_date(number):
    pass


def check_for_key_words(text):
    if text.lower() in key_words:
        print(text.lower() + " - ключевое слово")
        return True


def check_for_number_date(text):
    try:
        date = int(text)
        print(f"{date} + текущий месяц")
        return True
    except ValueError:
        return False


def check_for_date_text(text):
    words = text.split()
    if len(words) == 2:
        try:
            words[0] = int(words[0])
        except ValueError:
            return False

        if words[1] in months:
            print(f"{words[0]} + {words[1]} - число + месяц")
        else:
            return False
        return True
    else:
        return False


def check_for_date_format(text):
    words = text.split(".")
    if len(words) == 2 or len(words) == 3:
        try:
            for i in range(len(words)):
                words[i] = int(words[i])
        except ValueError:
            return False
        print(f"{words} - полный формат")
        return True
    else:
        return False


print(check_for_key_words('сегодня'))
print(check_for_date_format('14.01.2024'))
print(check_for_date_format('05.05.2025'))
print(check_for_number_date('20'))
print(check_for_date_text('20 сентября'))
print(check_for_date_text('13 декабря'))
