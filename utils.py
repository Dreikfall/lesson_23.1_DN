from exceptions import FilterMapColErrors


def iterator(file) -> iter:
    """Итератор всего лога"""

    with open(file, 'r', encoding='utf-8') as f:
        return (i for i in f.readlines())


def filter_query(iter_obj, value: str) -> iter:
    """Фильтрация по вхождению слова"""

    iter_obj = filter(lambda x: value in x, iter_obj)
    return iter_obj


def filter_map(iter_obj, col: str) -> iter:
    """Фильтрация по столбцам"""

    if col == '1':
        iter_obj = map(lambda x: f'{x.split()[0]}\n', iter_obj)
        return iter_obj
    elif col == '2':
        iter_obj = map(lambda x: f"{x[x.find('['):x.find(']')+1]}\n", iter_obj)
        return iter_obj
    elif col == '3':
        iter_obj = map(lambda x: f'''{x[x.find('"'):]}\n''', iter_obj)
        return iter_obj
    raise FilterMapColErrors('Необходимо ввести value в диапазоне 1-3')


def filter_unique(iter_obj) -> iter:
    """Только уникальные значения"""

    uniq_set = set(iter_obj)
    for i in uniq_set:
        yield i


def filter_sort(iter_obj, asc_desc) -> iter:
    """Фильтрация по алфавиту в обе стороны"""

    iter_obj = sorted(iter_obj, reverse=asc_desc)
    return iter_obj


def filter_limit(iter_obj, limit: int) -> iter:
    """Лимит записей"""

    buff = (next(iter_obj) for i in range(limit))
    return buff

