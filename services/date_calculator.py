from datetime import date


def calculate_date_list(date_: date, periods: int) -> list[date]:
    """
        Принимает дату заявку и период действия вклада. Собирает список
        всех дат начисления процентов по вкладу и возвращает его
    """
    date_list = []
    month = date_.month
    year = date_.year

    for i in range(periods):
        next_period_day = get_next_period_day(year, month, date_.day)
        date_list.append(date(year, month, next_period_day))
        month, year = get_next_iteration_month_and_year(month, year)

    return date_list


def get_next_period_day(year: int, month: int, day: int) -> int:
    """
        Принимает параметры года, месяца и дня. Определяет корректность значения дня
        в зависимости от месяца (в месяце 30 дней, високосный год или нет). Возвращает
        корректное значение дня
    """
    if day == 31 and month in [4, 6, 9, 11]:
        return 30

    if day in [29, 30, 31] and month == 2:
        return 29 if is_leap_year(year) else 28

    return day


def is_leap_year(year: int) -> bool:
    """
        Принимает значение года и определяет, является ли он високосным
    """
    return year % 4 == 0 and year % 100 != 0 or year % 400 == 0


def get_next_iteration_month_and_year(month: int, year: int) -> tuple[int, int]:
    """
        Принимает параметры месяца и года. Возвращает следующий месяц и год
        относительно заданной даты. Если значение месяца равно 12 (декабрь),
        то присваивает 1 (январь), а год увеличивает на 1. Иначе присваивает следующий месяц
    """
    return (1, year + 1) if month == 12 else (month + 1, year)
