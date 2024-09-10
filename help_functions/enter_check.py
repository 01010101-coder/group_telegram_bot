key_words = ['сегодня', 'завтра', 'послезавтра']
months = ['январь', 'февраль', 'март', 'апрель', 'май', 'июнь', 'июль', 'август', 'сентябрь', 'октябрь', 'ноябрь', 'декабрь',
          'января', 'февраля', 'марта', 'апреля', 'мая', 'июня', 'июля', 'августа', 'сентября', 'октября', 'ноября', 'декабря']


def check_for_invalid_date(number):
    if 0 < number < 32:
        return True
    return False


def check_for_key_words(text):
    if text.lower() in key_words:
        print(text.lower() + " - ключевое слово")
        return True


def check_for_number_date(text):
    try:
        date = int(text)
    except ValueError:
        return False

    is_data_valid = check_for_invalid_date(date)
    if is_data_valid:
        print(f"{date} + текущий месяц")
        return True

    return False


def check_for_date_text(text):
    words = text.split()
    if len(words) == 2:
        try:
            words[0] = int(words[0])
        except ValueError:
            return False

        if words[1] in months and check_for_invalid_date(words[0]):
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

        for i in range(len(words) - 1):
            if not check_for_invalid_date(words[i]):
                return False
        print(f"{words} - полный формат")
        return True
    else:
        return False


