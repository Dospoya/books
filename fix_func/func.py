from collections import Counter
from typing import Callable, Iterable, TypeVar
from re import findall


T = TypeVar('T')

def get_first_matching_object(
    predicate: Callable[[T], bool],
    objects: Iterable[T]
) -> T | None:
    """Возвращает первый объект, удовлетворяющий условию.

    Args:
        predicate: Функция, возвращающая True для искомого объекта.
        objects: Последовательность объектов для поиска.

    Returns:
        Первый найденный объект или None, если совпадений нет.
    """
    return next((obj for obj in objects if predicate(obj)), None)


def word_statistics(lines: list[str]) -> dict[str, int]:
    """Считает статистику слов в списке строк.

    Args:
        lines: Список строк для анализа.

    Returns:
        Словарь {слово: количество}, отсортированный по убыванию частоты
        и по алфавиту при равенстве.
    """
    count = Counter()
    for line in lines:
        words: list[str] = findall(r'[a-zA-Zа-яА-Я]+', line.lower())
        count.update(words)
    sorted_items = sorted(count.items(), key=lambda x: (-x[1], x[0]))
    return dict(sorted_items)
