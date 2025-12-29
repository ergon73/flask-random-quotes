from flask import Flask, render_template, request
import requests
import os
from dotenv import load_dotenv

load_dotenv()
app = Flask(__name__)
API_TIMEOUT = 8


def safe_get_json(url, headers=None, params=None):
    """Безопасный запрос с обработкой ошибок."""
    # Добавляем браузерный User-Agent, чтобы избежать более строгих rate limits
    default_headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }
    if headers:
        default_headers.update(headers)
    try:
        response = requests.get(url, headers=default_headers, params=params, timeout=API_TIMEOUT)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        raise ValueError(f"Источник временно недоступен: {str(e)}")
    except ValueError as e:
        raise ValueError(f"Ошибка при обработке ответа: {str(e)}")


def fetch_quoteslate():
    """Получает случайную цитату из QuoteSlate API."""
    url = "https://quoteslate.vercel.app/api/quotes/random"
    try:
        data = safe_get_json(url)
        return {
            "text": data.get("quote", ""),
            "author": data.get("author", ""),
            "source": "quoteslate",
            "meta": {
                "tags": data.get("tags", []),
                "id": data.get("id")
            }
        }
    except Exception as e:
        return {
            "error": str(e),
            "source": "quoteslate"
        }


def fetch_zenquotes():
    """Получает случайную цитату из ZenQuotes API."""
    url = "https://zenquotes.io/api/random"
    try:
        data = safe_get_json(url)
        if not isinstance(data, list) or len(data) == 0:
            raise ValueError("Пустой ответ от API")
        item = data[0]
        return {
            "text": item.get("q", ""),
            "author": item.get("a", ""),
            "source": "zenquotes",
            "meta": {}
        }
    except Exception as e:
        return {
            "error": str(e),
            "source": "zenquotes"
        }


def fetch_apininjas(api_key):
    """Получает случайную цитату из API Ninjas."""
    url = "https://api.api-ninjas.com/v2/randomquotes"
    headers = {"X-Api-Key": api_key}
    try:
        data = safe_get_json(url, headers=headers)
        if not isinstance(data, list) or len(data) == 0:
            raise ValueError("Пустой ответ от API")
        item = data[0]
        return {
            "text": item.get("quote", ""),
            "author": item.get("author", ""),
            "source": "apininjas",
            "meta": {
                "work": item.get("work", ""),
                "categories": item.get("categories", [])
            }
        }
    except Exception as e:
        return {
            "error": str(e),
            "source": "apininjas"
        }


def get_available_sources(api_ninjas_key):
    """Возвращает список доступных источников для селекта."""
    sources = [
        ("quoteslate", "QuoteSlate (free)"),
        ("zenquotes", "ZenQuotes (free)"),
    ]
    if api_ninjas_key:
        sources.append(("apininjas", "API Ninjas (API key)"))
    return sources


@app.route("/", methods=["GET", "POST"])
def index():
    """Главная страница приложения."""
    api_ninjas_key = os.getenv("API_NINJAS_KEY")
    available_sources = get_available_sources(api_ninjas_key)
    
    quote = None
    error = None
    selected_source = "quoteslate"
    
    if request.method == "POST":
        selected_source = request.form.get("source", "quoteslate")
    else:
        # GET запрос - показываем дефолтную цитату
        selected_source = "quoteslate"
    
    # Получаем цитату из выбранного источника
    if selected_source == "quoteslate":
        quote = fetch_quoteslate()
    elif selected_source == "zenquotes":
        quote = fetch_zenquotes()
    elif selected_source == "apininjas" and api_ninjas_key:
        quote = fetch_apininjas(api_ninjas_key)
    else:
        error = "Выбранный источник недоступен"
    
    # Проверяем, есть ли ошибка в ответе
    if quote and "error" in quote:
        error = quote["error"]
        quote = None
    
    return render_template(
        "index.html",
        quote=quote,
        error=error,
        available_sources=available_sources,
        selected_source=selected_source
    )


if __name__ == "__main__":
    app.run(debug=True)

