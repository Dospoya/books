from decimal import Decimal

def validate_rating(value: Decimal | None, allow_none: bool = False) -> Decimal | None:
    """Валидатор рейтинга книги.

    Args:
        value: Значение рейтинга.
        allow_none: Если True — допускает None.

    Returns:
        Валидированное значение рейтинга или None.

    Raises:
        ValueError: Если значение пустое (allow_none=False) или не в диапазоне 0.0–10.0.
    """
    if value is None:
        if allow_none:
            return None
        raise ValueError('Значение не должно быть пустым')
    if not 0.0 <= value <= 10.0:
        raise ValueError('Допустимый диапазон рейтинга от 0.0 до 10.0')
    return value
