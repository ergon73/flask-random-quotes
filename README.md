# Random Quotes — Flask + Public APIs

Небольшое Flask‑приложение, которое получает **случайные цитаты** из публичных API и показывает их на странице.

Сделано как домашнее задание к уроку **VD08 (Работа с API)**: Flask + requests + Jinja2 + Bootstrap.

**Автор:** Георгий Белянин (Georgy Belyanin)  
**Email:** <georgy.belyanin@gmail.com>

---

## Возможности

- Случайные цитаты из нескольких источников
- Переключение источника через dropdown
- Bootstrap UI (адаптивная верстка)
- Аккуратная обработка ошибок: приложение не падает при проблемах API
- Два источника работают без ключа из коробки (QuoteSlate + ZenQuotes)
- Опциональная интеграция API Ninjas через `.env`
- Базовые тесты (pytest) без реальных HTTP запросов

---

## Источники цитат

| Source | API Key | Notes |
| --- | ---: | --- |
| **QuoteSlate** | ❌ | Дефолтный источник, просит credit; публичный endpoint имеет rate limit (~100 req / 15 min per IP). Используется браузерный User-Agent для снижения ограничений |
| **ZenQuotes** | ❌ | Есть лимит запросов в free‑режиме (5 req / 30 sec / IP) и требуется attribution |
| **API Ninjas** | ✅ | Опционально: подключается только если задан `API_NINJAS_KEY` |

---

## Быстрый старт

### 1) Установка

```bash
git clone <repository-url>
cd flask-random-quotes

python -m venv .venv

# Windows:
.venv\Scripts\activate
# macOS/Linux:
source .venv/bin/activate

pip install -r requirements.txt
```

### 2) (Опционально) API Ninjas

Создай `.env` рядом с `main.py`:

```env
API_NINJAS_KEY=your_key_here
```

Без этого ключа приложение всё равно работает (QuoteSlate + ZenQuotes).

### 3) Запуск

```bash
python main.py
```

Открой в браузере: `http://127.0.0.1:5000`

---

## Тесты

```bash
pytest -v
```

---

## Структура проекта

```text
flask-random-quotes/
├── main.py
├── requirements.txt
├── .env.example
├── .gitignore
├── LICENSE
├── README.md
├── templates/
│   └── index.html
└── tests/
    └── test_quotes.py
```

---

## Как это работает

1. На **GET /** приложение показывает страницу и пытается получить цитату из дефолтного источника.
1. На **POST /** приложение читает выбранный источник из формы (`request.form`) и запрашивает новую цитату.
1. Ответы разных API имеют разный JSON‑формат → приложение нормализует данные в общий вид:

```python
{
  "text": str,
  "author": str,
  "source": str,
  "meta": dict
}
```

1. Для снижения rate limits все запросы используют браузерный User-Agent, что позволяет обходить более строгие ограничения для программных клиентов.
1. Если источник недоступен / лимит / ошибка сети — пользователю показывается понятное сообщение в Bootstrap‑alert.

---

## Переменные окружения

Смотри `.env.example`.

- `API_NINJAS_KEY` — опционально, ключ для API Ninjas

---

## Attribution

- Для ZenQuotes в free‑режиме требуется attribution с ссылкой (поэтому он всегда отображается в footer).
- Для QuoteSlate корректно указывать credit (рекомендуется и добавлено в footer).

---

## Лицензия

MIT (см. `LICENSE`).

---

**Автор:** Георгий Белянин (Georgy Belyanin)  
**Email:** <georgy.belyanin@gmail.com>
