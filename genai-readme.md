# Cursor Agent Spec: Random Quotes Flask App (VD08)

**Цель:** создать простое Flask‑приложение, которое получает случайные цитаты с публичных API и показывает их на странице.  
**Контекст:** домашка к уроку **VD08 (Работа с API)**. Повторяем паттерн урока: **Flask + requests + Jinja2 + Bootstrap**.

> Важно: спецификация “жёсткая”. Делай ровно как написано. Не добавляй лишнего.

---

## 0) Жёсткие требования (НЕ обсуждаются)

1. **Весь Python код в одном файле** `main.py` (как на уроке)
2. **Только Flask + requests** (никаких других веб‑фреймворков)
3. **Bootstrap 5.x только через CDN**
4. **Шаблон Jinja2** только в `templates/index.html`
5. **Минимум 2 источника работают без API ключей**
6. **Приложение не падает** при ошибках сети/API/JSON — показываем понятное сообщение
7. **Тесты не ходят в интернет** (обязательно мокать `requests.get`)

---

## 1) Структура проекта (ОБЯЗАТЕЛЬНО)

```
flask-random-quotes/
├── main.py              # ВЕСЬ backend здесь
├── requirements.txt     # зависимости
├── .env.example         # шаблон env-переменных (без секретов)
├── .gitignore           # игнор .env и venv
├── LICENSE              # MIT
├── README.md            # документация
├── templates/
│   └── index.html       # единственный шаблон
└── tests/
    └── test_quotes.py   # pytest тесты (моки)
```

---

## 2) Источники цитат (API)

### 2.1 QuoteSlate (БЕСПЛАТНО, без ключа) — ДЕФОЛТ
- URL: `https://quoteslate.vercel.app/api/quotes/random`
- Метод: GET
- Особенности: публичный endpoint имеет rate limit (примерно **100 req / 15 min per IP**)
- Также автор API просит делать attribution (“Quotes powered by QuoteSlate API”) — добавь в footer (не обязательно юридически, но корректно).

**Пример ответа (объект):**
```json
{
  "id": 498,
  "quote": "Every strike brings me closer to the next home run.",
  "author": "Babe Ruth",
  "length": 51,
  "tags": ["wisdom"]
}
```

Парсим:
- text = `data["quote"]`
- author = `data["author"]`
- meta.tags = `data.get("tags", [])`

---

### 2.2 ZenQuotes (БЕСПЛАТНО, без ключа, НУЖНА АТРИБУЦИЯ)
- URL: `https://zenquotes.io/api/random`
- Метод: GET
- Ответ всегда **массив** (list)
- Ограничение free‑режима: **5 запросов / 30 секунд / IP**
- Требование: показывать attribution с ссылкой на ZenQuotes в free‑режиме  
  (добавь в footer и показывай всегда — так проще и безопаснее).

**Пример ответа (массив):**
```json
[
  {
    "q": "Quality means doing it right when no one is looking.",
    "a": "Henry Ford",
    "h": "<blockquote>...</blockquote>"
  }
]
```

Парсим:
- item = `data[0]`
- text = `item["q"]`
- author = `item["a"]`

---

### 2.3 API Ninjas (ОПЦИОНАЛЬНО, НУЖЕН КЛЮЧ)
- Документация из задания: https://api-ninjas.com/api/quotes
- Endpoint для случайных цитат:
  - URL: `https://api.api-ninjas.com/v2/randomquotes`
- Метод: GET
- Заголовок: `X-Api-Key: <KEY>`
- Переменная окружения: `API_NINJAS_KEY`

**Пример ответа (массив):**
```json
[
  {
    "quote": "Always remember, success leaves clues.",
    "author": "John Patrick Hickey",
    "work": "On The Journey To Achievement",
    "categories": ["success", "wisdom", "inspirational"]
  }
]
```

Парсим:
- item = `data[0]`
- text = `item["quote"]`
- author = `item["author"]`
- meta.work = `item.get("work", "")`
- meta.categories = `item.get("categories", [])`

---

## 3) Архитектура `main.py` (строго)

### 3.1 Импорты и инициализация

```python
from flask import Flask, render_template, request
import requests
import os
from dotenv import load_dotenv
```

- `load_dotenv()` вызывается сразу
- `app = Flask(__name__)`
- константа: `API_TIMEOUT = 8`

---

### 3.2 Нормализованный формат цитаты (единый для всех API)

Каждая `fetch_*` функция возвращает:

```python
{
  "text": str,
  "author": str,
  "source": str,   # quoteslate | zenquotes | apininjas
  "meta": dict     # tags/categories/work и т.п.
}
```

При ошибке возвращаем:

```python
{
  "error": "Понятное сообщение для пользователя",
  "source": str
}
```

> Не возвращай traceback пользователю. Ошибка должна быть короткой и понятной.

---

### 3.3 Helper для запросов (рекомендуется)

Сделай в `main.py` функцию:

- `safe_get_json(url, headers=None, params=None)`

Правила:
- `requests.get(..., timeout=API_TIMEOUT)`
- `response.raise_for_status()`
- `return response.json()`
- ловим:
  - `requests.exceptions.RequestException`
  - `ValueError` (битый JSON)
- в ошибке пишем: “Источник временно недоступен” + детали 1 строкой

---

### 3.4 Функции источников (ОБЯЗАТЕЛЬНО)

- `fetch_quoteslate()`
- `fetch_zenquotes()`
- `fetch_apininjas(api_key: str)`

Каждая делает запрос, парсит JSON, возвращает **нормализованный словарь**.

---

### 3.5 Доступные источники (динамика)

Логика:
- QuoteSlate и ZenQuotes доступны всегда
- API Ninjas добавляется **только если** `API_NINJAS_KEY` не пустой

Сделай функцию:
- `get_available_sources(api_ninjas_key: str | None) -> list[tuple[str,str]]`

Возвращает список для селекта, например:
```python
[
  ("quoteslate", "QuoteSlate (free)"),
  ("zenquotes", "ZenQuotes (free)"),
  ("apinjas", "API Ninjas (API key)")
]
```

---

## 4) Flask роут и поведение страницы

### Роут
`@app.route("/", methods=["GET", "POST"])`

Поведение:
1. **GET** → показываем страницу и сразу получаем цитату из **QuoteSlate** (дефолт)
2. **POST** → читаем `source` из формы, запрашиваем цитату из выбранного источника
3. Если ошибка — показываем bootstrap‑alert, приложение не падает

В конце файла обязательно:

```python
if __name__ == "__main__":
    app.run(debug=True)
```

Переменные для шаблона:
- `quote` (dict или None)
- `error` (str или None)
- `available_sources` (list[tuple[value,label]])
- `selected_source` (str)

---

## 5) Шаблон `templates/index.html` (Bootstrap 5)

Обязательные элементы:
1. Bootstrap 5 CDN в `<head>`
2. Заголовок
3. Форма POST:
   - select источника
   - кнопка “Получить цитату”
4. Если `error` → `<div class="alert alert-danger">...`
5. Если `quote` → карточка `<div class="card">...`
6. Footer с атрибуцией:
   - ZenQuotes attribution (обязательно)
   - QuoteSlate credit (рекомендуется)

---

## 6) requirements.txt

Содержимое (минимум):

```
Flask>=3.0.0
requests>=2.31.0
python-dotenv>=1.0.0
pytest>=8.0.0
```

---

## 7) .env.example

```
# Optional: API Ninjas key (https://api-ninjas.com)
API_NINJAS_KEY=
```

---

## 8) .gitignore (минимум)

```
.env
__pycache__/
*.pyc
.pytest_cache/
.venv/
venv/
```

---

## 9) LICENSE

Создай `LICENSE` с текстом **MIT License** (стандартный шаблон).

---

## 10) Тесты (tests/test_quotes.py)

Требования:
- pytest
- использовать `unittest.mock.patch` для моков `requests.get`
- тесты не должны делать реальные HTTP запросы

Минимальный набор:
1. `test_quoteslate_parse` — мокнуть JSON QuoteSlate и проверить нормализацию
2. `test_zenquotes_parse` — мокнуть JSON ZenQuotes (массив) и проверить нормализацию
3. `test_apininjas_parse` — мокнуть JSON API Ninjas (массив) и проверить нормализацию
4. `test_available_sources_without_key` — API Ninjas не в списке, если ключа нет

---

## 11) Проверка перед завершением (агент обязан сделать)

1) Установка:
```bash
pip install -r requirements.txt
```

2) Тесты:
```bash
pytest -v
```

3) Запуск:
```bash
python main.py
```

4) Ручная проверка в браузере:
- страница открывается
- цитата показывается
- источники переключаются
- при ошибке API показывается alert (без падения)

5) В конце — показать структуру:
```bash
tree
```

---

## 12) НЕ ДЕЛАТЬ

- ❌ не создавать много python файлов (всё в main.py)
- ❌ не подключать базы данных / ORM
- ❌ не подключать Flask‑WTF
- ❌ не добавлять кеширование/фоновые задачи
- ❌ не добавлять отдельные CSS/JS файлы
- ❌ не хардкодить ключи в коде

