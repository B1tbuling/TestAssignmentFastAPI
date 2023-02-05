from schemas import ContributionInfo
from .contribution_calculator import calculate_contribution_list
from .date_calculator import calculate_date_list
from .date_formatter import convert_string_to_date, convert_date_to_string


def get_contribution(data: ContributionInfo) -> dict[str, float]:
    """
        Функция принимает данные от клиента (дату заявки, период действия вклада, сумму и процентную ставку)
        вместе с классом валидатором, который проверяет корректность этих данных. Возвращает соединенный из
        двух списков (список сумм за период действия вклада с начисленными ежемесячными процентами и список
        дат с начисленными ежемесячными процентами) словарь с ключем "дата" и значением "суммы с начисленными
        процентами"
    """
    contribution_list = calculate_contribution_list(periods=data.periods, amount=data.amount, rate=data.rate)
    date_list = calculate_date_list(date_=convert_string_to_date(data.date), periods=data.periods)
    return dict(zip(map(convert_date_to_string, date_list), contribution_list))


