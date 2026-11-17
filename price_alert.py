"""CryptoWatch: цінові сповіщення (user story CWT-1 / CW-11 з Product Backlog ЛР2).

Як користувач, я хочу створити цінове сповіщення (поріг вище або нижче),
щоб не стежити за курсом постійно.
"""
from dataclasses import dataclass

DIRECTIONS = ("above", "below")


@dataclass(frozen=True)
class PriceAlert:
    ticker: str
    threshold: float
    direction: str


def _is_number(value) -> bool:
    return isinstance(value, (int, float)) and not isinstance(value, bool)


def create_alert(ticker: str, threshold: float, direction: str) -> PriceAlert:
    """Створює сповіщення з перевіркою вхідних даних."""
    if not isinstance(ticker, str) or not ticker.strip():
        raise ValueError("Тикер монети не може бути порожнім")
    if not _is_number(threshold) or threshold <= 0:
        raise ValueError("Поріг має бути додатним числом")
    if direction not in DIRECTIONS:
        raise ValueError("Напрямок має бути 'above' або 'below'")
    return PriceAlert(ticker.strip().upper(), float(threshold), direction)


def should_trigger(alert: PriceAlert, current_price: float) -> bool:
    """Повертає True, якщо поточна ціна досягла порогу сповіщення."""
    if not _is_number(current_price) or current_price < 0:
        raise ValueError("Ціна має бути невід'ємним числом")
    if alert.direction == "above":
        return current_price > alert.threshold
    return current_price <= alert.threshold
