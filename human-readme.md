# Домашка VD08: Flask + Random Quotes (API)

Пошаговое руководство, как выполнить домашнее задание из урока **VD08 (Работа с API)** с помощью **Cursor**.

**Задание:** сделать простое веб‑приложение, которое запрашивает случайные цитаты с публичного API и показывает их на странице.

---

## Что понадобится

- Python **3.10+**
- Git
- Cursor (режим **Agent / Auto**)
- Интернет (для запросов к публичным API)

---

## Шаг 1. Создай репозиторий

### На GitHub

1. **New repository**
2. Name (пример): `flask-random-quotes`
3. Description (пример): `Flask app that fetches random quotes from public APIs`
4. ✅ Public
5. ✅ Add README
6. ✅ Add .gitignore: Python  
7. Create repository

### Локально

```bash
git clone https://github.com/YOUR_USERNAME/flask-random-quotes.git
cd flask-random-quotes
```

---

## Шаг 2. Положи “управляющие” файлы в корень проекта

Скопируй в корень репозитория эти файлы:

- `.cursorrules`
- `genai-readme.md`
- `human-readme.md` (этот файл)

---

## Шаг 3. Запусти Cursor Agent

1. Открой проект в Cursor
2. Открой **Agent** (обычно `Ctrl+L`)
3. Вставь **короткий промпт** ниже:

```
Прочитай genai-readme.md и создай проект строго по спецификации.
Следуй правилам из .cursorrules.
После генерации: установи зависимости, запусти pytest, затем запусти приложение.
Исправь все ошибки так, чтобы тесты были зелёные и приложение открывалось в браузере.
В конце покажи структуру проекта командой tree.
```

> Логика как на уроке: Flask + requests + Jinja2 + Bootstrap, один main.py, роут `/` с GET/POST и форма на странице.

---

## Шаг 4. Проверка локально (обязательно)

### 4.1 Создай виртуальное окружение и установи зависимости

```bash
python -m venv .venv

# Windows:
.venv\Scripts\activate
# macOS/Linux:
source .venv/bin/activate

pip install -r requirements.txt
```

### 4.2 (Опционально) Добавь ключ API Ninjas

Приложение **работает без ключей** с QuoteSlate и ZenQuotes.
API Ninjas подключается **только если** ты добавишь ключ в `.env`.

1. Зарегистрируйся на сайте API Ninjas
2. Скопируй API key
3. Создай файл `.env` (НЕ коммить его в git):

```
API_NINJAS_KEY=your_key_here
```

### 4.3 Запусти тесты

```bash
pytest -v
```

Должно быть **зелёным**.

### 4.4 Запусти приложение

```bash
python main.py
```

Открой в браузере: `http://127.0.0.1:5000`

---

## Шаг 5. Что проверить руками в браузере (чеклист)

- [ ] Страница открывается без ошибок
- [ ] На загрузке показывается цитата (дефолтный источник)
- [ ] Кнопка **“Получить цитату”** обновляет цитату
- [ ] Можно переключать источник в dropdown (минимум 2 источника без ключей)
- [ ] Если API недоступно / лимит — показывается понятная ошибка, приложение **не падает**
- [ ] Внизу страницы есть атрибуция для ZenQuotes (как требует их free‑режим)

---

## Шаг 6. Финальный коммит и пуш

Пример коммита:

```bash
git add .
git commit -m "feat: random quotes Flask app with public APIs"
git push origin main
```

---

## Типичные проблемы и быстрые решения

### `ModuleNotFoundError: No module named 'flask'`
✅ Ты не активировал venv или не поставил зависимости:
```bash
source .venv/bin/activate  # macOS/Linux
# или
.venv\Scripts\activate    # Windows
pip install -r requirements.txt
```

### `KeyError` / “list index out of range” при парсинге
✅ Некоторые API возвращают **массив** (ZenQuotes и API Ninjas), нужно брать `data[0]`.

### Ошибка `429 Too Many Requests`
✅ Это лимит API. Подожди и попробуй другой источник.  
Поэтому в проекте дефолтный источник — QuoteSlate (он мягче по лимитам).

### API Ninjas не появляется в списке
✅ Нет переменной окружения `API_NINJAS_KEY` в `.env` или она пустая.

---

## Что ты закрепишь после домашки

- REST API и JSON в реальном проекте
- requests + таймауты + обработка ошибок
- Flask: роуты, GET/POST, `request.form`
- Jinja2: условия и циклы
- Bootstrap: быстрое оформление интерфейса
- Переменные окружения через `.env`
- Базовое тестирование (pytest + mock)

