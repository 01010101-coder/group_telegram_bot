import requests
import json
from datetime import datetime


class YandexPrompt:
    def __init__(self, TOKEN, url_path):
        self.TOKEN = TOKEN
        self.url_path = url_path

    def request(self, text):
        today = datetime.today().strftime('%d.%m.%Y')
        print(text + today)
        prompt = {
            "messages": [
                {
                    "text": "Вы обрабатываете текст, чтобы найти информацию об отсутствии студента. В фигурных скобках всегда указывается текущая дата. На основе этого текста извлеките следующие данные:\nДата отсутствия – если указано \"завтра\", добавьте 1 день к сегодняшней дате, если \"послезавтра\" – 2 дня, и так далее. Если дата не указана, считается, что это сегодня.\nПары – диапазон от 1 до 5. Если указаны фразы \"весь день\" или \"все пары\", считаем, что пропущены все пары (1-5).\nПричина отсутствия – объяснение причины пропуска.\nПоле ошибок (error) – если в тексте:\nДата не существует или написана неверно (например, 90 марта),\nУказана пара вне диапазона (например, 7 пара),\nНе хватает ключевых элементов (дата, пары, причина), то поле error должно быть Yes.\nПримеры ответов:\nПример 1\nТекст: Меня не будет завтра на 2-4 парах, потому что завал на работе, сори.{09.10.2024}\n'date': 10.10.2024,\n'when': [2, 3, 4],\n'description': \"завал на работе\",\n'error': None\nПример 2\nТекст: Меня не будет на 2 последних парах, так как я очень хочу спать.{06.09.2024}\n'date': 06.09.2024,\n'when': [4, 5],\n'description': \"я очень хочу спать\",\n'error': None\nПример 3\nТекст: Меня не будет послезавтра весь день, иду по врачам для справки. {29.09.2024}\n'date': 01.10.2024,\n'when': [1, 2, 3, 4, 5],\n'description': \"иду по врачам для справки\",\n'error': None\nПример 4\nТекст: Не будет на 7 паре 90 марта{11.09.2024}\n'date': None,\n'when': None,\n'description': None,\n'error': Yes\nОтвет должен быть строго в указанном формате, без дополнительного текста.",
                    "role": "system"
                },
                {
                    "text": f"{text}{{today}}",
                    "role": "user"
                }
            ],
            "completionOptions": {
                "stream": True,
                "maxTokens": "500",
                "temperature": 0.1
            },
            "modelUri": f"{self.url_path}"
        }

        url = "https://llm.api.cloud.yandex.net/foundationModels/v1/completion"
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Api-Key {self.TOKEN}"
        }

        try:
            response = requests.post(url, headers=headers, json=prompt)
        except:
            return "error"

        raw_response = response.text

        json_objects = raw_response.splitlines()

        if len(json_objects) > 1:
            second_json_object = json_objects[1]
        else:
            second_json_object = json_objects[0]

        try:
            result = json.loads(second_json_object)
            result = result['result']['alternatives'][0]['message']['text']
        except json.JSONDecodeError as e:
            return 'error'

        return self.result_parse(result)

    def result_parse(self, raw_data):
        lines = raw_data.split(',')

        result = {}

        for line in lines:
            line = line.strip()

            if line.startswith("'date'"):
                key, value = line.split(':')
                result['date'] = value.strip().replace("'", "").replace("“", "").replace("”", "").strip()

            elif line.startswith("'when'"):
                key, value = line.split(':')
                when_values = value.strip().replace('[', '').replace(']', '').split()
                result['when'] = [int(i) for i in when_values if i.isdigit()]

            elif line.startswith("'description'"):
                key, value = line.split(':', 1)
                result['description'] = value.strip().replace('"', '').strip()

            elif line.startswith("'error'"):
                key, value = line.split(':')
                result['error'] = value.strip()
                if result['error'] == 'None':
                    result['error'] = None

        return result
