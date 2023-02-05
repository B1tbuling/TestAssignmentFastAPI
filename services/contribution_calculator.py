def calculate_contribution_for_next_month(amount: float | int, rate: float) -> float:
    """
        Принимает параметры суммы вклада и процентной годовой ставки.
        Возвращает сумму с начисленными месячными процентами по вкладу
    """
    amount_with_percent = amount * (1 + rate / 12 / 100)
    return round(amount_with_percent, 2)


def calculate_contribution_list(periods: int, amount: int, rate: float) -> list[float]:
    """
        Принимает параметры периода действия вклада, сумму вклада, а также процент годовой ставки.
        Возвращает список сумм за период действия вклада с начисленными ежемесячными процентами
    """
    contribution_list = []
    for i in range(periods):
        amount = calculate_contribution_for_next_month(amount, rate)
        contribution_list.append(amount)
    return contribution_list
