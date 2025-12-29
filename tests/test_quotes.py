import pytest
from unittest.mock import patch, Mock
import sys
import os

# Добавляем корневую директорию в путь
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from main import fetch_quoteslate, fetch_zenquotes, fetch_apininjas, get_available_sources


def test_quoteslate_parse():
    """Тест парсинга ответа QuoteSlate."""
    mock_response = Mock()
    mock_response.json.return_value = {
        "id": 498,
        "quote": "Every strike brings me closer to the next home run.",
        "author": "Babe Ruth",
        "length": 51,
        "tags": ["wisdom"]
    }
    mock_response.raise_for_status = Mock()
    
    with patch('main.requests.get', return_value=mock_response):
        result = fetch_quoteslate()
        assert result["text"] == "Every strike brings me closer to the next home run."
        assert result["author"] == "Babe Ruth"
        assert result["source"] == "quoteslate"
        assert "tags" in result["meta"]
        assert result["meta"]["tags"] == ["wisdom"]


def test_zenquotes_parse():
    """Тест парсинга ответа ZenQuotes (массив)."""
    mock_response = Mock()
    mock_response.json.return_value = [
        {
            "q": "Quality means doing it right when no one is looking.",
            "a": "Henry Ford",
            "h": "<blockquote>...</blockquote>"
        }
    ]
    mock_response.raise_for_status = Mock()
    
    with patch('main.requests.get', return_value=mock_response):
        result = fetch_zenquotes()
        assert result["text"] == "Quality means doing it right when no one is looking."
        assert result["author"] == "Henry Ford"
        assert result["source"] == "zenquotes"


def test_apininjas_parse():
    """Тест парсинга ответа API Ninjas (массив)."""
    mock_response = Mock()
    mock_response.json.return_value = [
        {
            "quote": "Always remember, success leaves clues.",
            "author": "John Patrick Hickey",
            "work": "On The Journey To Achievement",
            "categories": ["success", "wisdom", "inspirational"]
        }
    ]
    mock_response.raise_for_status = Mock()
    
    with patch('main.requests.get', return_value=mock_response):
        result = fetch_apininjas("test_key")
        assert result["text"] == "Always remember, success leaves clues."
        assert result["author"] == "John Patrick Hickey"
        assert result["source"] == "apininjas"
        assert result["meta"]["work"] == "On The Journey To Achievement"
        assert "categories" in result["meta"]


def test_available_sources_without_key():
    """Тест: API Ninjas не в списке, если ключа нет."""
    sources = get_available_sources(None)
    source_values = [s[0] for s in sources]
    assert "apininjas" not in source_values
    assert "quoteslate" in source_values
    assert "zenquotes" in source_values


def test_available_sources_with_key():
    """Тест: API Ninjas в списке, если ключ есть."""
    sources = get_available_sources("test_key")
    source_values = [s[0] for s in sources]
    assert "apininjas" in source_values
    assert "quoteslate" in source_values
    assert "zenquotes" in source_values

