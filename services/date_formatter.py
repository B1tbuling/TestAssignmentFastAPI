from datetime import datetime, date


def convert_string_to_date(date_str: str) -> date:
    """
        Принимает и конвертирует строку с датой
        (в формате dd.mm.YYYY) в объект даты (date(year, month, day))
    """
    d = datetime.strptime(date_str, '%d.%m.%Y')
    return date(d.year, d.month, d.day)


def convert_date_to_string(date_: date) -> str:
    """
        Принимает и конвертирует объект даты (date(year, month, day))
        в строку с датой (в формате dd.mm.YYYY)
    """

    return f'{date_.day:02}.{date_.month:02}.{date_.year}'
