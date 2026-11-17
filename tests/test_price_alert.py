import pytest

from price_alert import create_alert, should_trigger


# AC1: сповіщення "вище" спрацьовує, коли ціна досягла або перевищила поріг
def test_above_triggers_when_price_exceeds_threshold():
    alert = create_alert("BTC", 70000, "above")
    assert should_trigger(alert, 71500) is True


def test_above_does_not_trigger_below_threshold():
    alert = create_alert("BTC", 70000, "above")
    assert should_trigger(alert, 69999.99) is False


# AC2: сповіщення "нижче" спрацьовує, коли ціна опустилася до порогу або нижче
def test_below_triggers_when_price_drops():
    alert = create_alert("ETH", 3000, "below")
    assert should_trigger(alert, 2950) is True


# Граничний випадок: ціна дорівнює порогу
@pytest.mark.parametrize("direction", ["above", "below"])
def test_price_equal_to_threshold_triggers(direction):
    alert = create_alert("SOL", 150, direction)
    assert should_trigger(alert, 150) is True


# AC3: тикер нормалізується (верхній регістр, без пробілів)
def test_ticker_is_normalized():
    alert = create_alert("  btc ", 1, "above")
    assert alert.ticker == "BTC"


# AC4: некоректні вхідні дані відхиляються
@pytest.mark.parametrize("threshold", [0, -10, "100", None, True])
def test_invalid_threshold_raises(threshold):
    with pytest.raises(ValueError):
        create_alert("BTC", threshold, "above")


def test_invalid_direction_raises():
    with pytest.raises(ValueError):
        create_alert("BTC", 100, "sideways")


def test_empty_ticker_raises():
    with pytest.raises(ValueError):
        create_alert("   ", 100, "above")


def test_negative_current_price_raises():
    alert = create_alert("BTC", 100, "below")
    with pytest.raises(ValueError):
        should_trigger(alert, -1)
