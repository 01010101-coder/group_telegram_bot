min_lessons = 1
max_lessons = 5

def parse_lessons(text):
    text = text.lower().strip()
    lessons = []

    # Формат "весь день"
    if "весь день" in text:
        return list(range(min_lessons, max_lessons + 1))

    # Формат одного числа, например "3"
    try:
        single_lesson = int(text)
        if min_lessons <= single_lesson <= max_lessons:
            return [single_lesson]
        else:
            return f"Ошибка: Пара {single_lesson} выходит за пределы допустимого диапазона {min_lessons}-{max_lessons}."
    except ValueError:
        pass

    # Формат "и"
    if "и" in text:
        parts = text.split(" и ")
        for part in parts:
            try:
                lesson = int(part)
                if min_lessons <= lesson <= max_lessons:
                    lessons.append(lesson)
                else:
                    return f"Ошибка: Пара {lesson} выходит за пределы допустимого диапазона {min_lessons}-{max_lessons}."
            except ValueError:
                return "Ошибка: Некорректный ввод для формата 'и'."
        return sorted(lessons)

    # Формат через запятую
    if "," in text:
        parts = text.split(", ")
        for part in parts:
            try:
                lesson = int(part)
                if min_lessons <= lesson <= max_lessons:
                    lessons.append(lesson)
                else:
                    return f"Ошибка: Пара {lesson} выходит за пределы допустимого диапазона {min_lessons}-{max_lessons}."
            except ValueError:
                return "Ошибка: Некорректный ввод для формата через запятую."
        return sorted(lessons)

    # Формат диапазона
    if "-" in text:
        try:
            start, end = text.split("-")
            start = int(start)
            end = int(end)
            if min_lessons <= start <= max_lessons and min_lessons <= end <= max_lessons:
                return list(range(start, end + 1))
            else:
                return f"Ошибка: Диапазон выходит за пределы {min_lessons}-{max_lessons}."
        except ValueError:
            return "Ошибка: Некорректный ввод для формата диапазона."

    return "Ошибка: Некорректный ввод."

# Примеры использования:
print(parse_lessons("1"))          # [1]
print(parse_lessons("3"))          # [3]
print(parse_lessons("1, 3"))       # [1, 3]
print(parse_lessons("2-4"))        # [2, 3, 4]
print(parse_lessons("3 и 5"))      # [3, 5]
print(parse_lessons("весь день"))  # [1, 2, 3, 4, 5]
print(parse_lessons("6"))          # Ошибка
