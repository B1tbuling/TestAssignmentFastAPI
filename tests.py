import unittest
from datetime import date

from fastapi import HTTPException

from schemas import ContributionInfo
from services.contribution_calculator import calculate_contribution_for_next_month, \
    calculate_contribution_list
from services.contribution_service import get_contribution
from services.date_calculator import calculate_date_list, get_next_period_day, is_leap_year, \
    get_next_iteration_month_and_year
from services.date_formatter import convert_string_to_date, convert_date_to_string


class ContributionCalculatorTest(unittest.TestCase):
    def test_calculate_contribution_for_next_month(self):
        self.assertEqual(calculate_contribution_for_next_month(10000, 6.0), 10050.0)
        self.assertEqual(calculate_contribution_for_next_month(10050, 6.0), 10100.25)
        self.assertEqual(calculate_contribution_for_next_month(10100.25, 6.0), 10150.75)

    def test_calculate_contribution_list(self):
        self.assertEqual(calculate_contribution_list(4, 10000, 6), [10050.0, 10100.25, 10150.75, 10201.5])


class DateCalculatorTest(unittest.TestCase):
    def test_is_leap_year(self):
        self.assertTrue(is_leap_year(2008))
        self.assertFalse(is_leap_year(2007))
        self.assertTrue(is_leap_year(2000))
        self.assertFalse(is_leap_year(1000))

    def test_get_next_iteration_month_and_year(self):
        self.assertEqual(get_next_iteration_month_and_year(12, 2000), (1, 2001))
        self.assertEqual(get_next_iteration_month_and_year(1, 2000), (2, 2000))

    def test_get_next_period_day(self):
        self.assertEqual(get_next_period_day(2022, 4, 31), 30)
        self.assertEqual(get_next_period_day(2022, 5, 31), 31)

        self.assertEqual(get_next_period_day(2022, 2, 31), 28)
        self.assertEqual(get_next_period_day(2000, 2, 30), 29)

        self.assertEqual(get_next_period_day(2022, 2, 18), 18)

    def test_calculate_date_list(self):
        self.assertEqual(
            calculate_date_list(date(2007, 12, 31), 5),
            [
                date(2007, 12, 31),
                date(2008, 1, 31),
                date(2008, 2, 29),
                date(2008, 3, 31),
                date(2008, 4, 30)
            ]
        )


class DateFormatterTest(unittest.TestCase):
    def test_convert_string_to_date(self):
        self.assertEqual(convert_string_to_date('01.01.2001'), date(2001, 1, 1))

    def test_convert_date_to_string(self):
        self.assertEqual(convert_date_to_string(date(2002, 2, 2)), '02.02.2002')


class GetContributionTest(unittest.TestCase):
    def test_get_contribution(self):
        data = ContributionInfo(date='01.02.2012', periods=4, amount=10000, rate=6)
        json = {'01.02.2012': 10050.0, '01.03.2012': 10100.25, '01.04.2012': 10150.75, '01.05.2012': 10201.5}
        self.assertEqual(get_contribution(data), json)

    def test_contribution_and_date_lists_len(self):
        data = ContributionInfo(date='01.02.2012', periods=4, amount=10000, rate=6)
        contribution_list = calculate_contribution_list(periods=data.periods, amount=data.amount, rate=data.rate)
        date_list = calculate_date_list(date_=convert_string_to_date(data.date), periods=data.periods)
        self.assertEqual(len(contribution_list), len(date_list))


class ValidationTest(unittest.TestCase):
    def test_date_validation(self):
        with self.assertRaises(HTTPException) as e:
            ContributionInfo(date='abc', periods=4, amount=10000, rate=6)
            self.assertEqual(e.exception.status_code, 400)
            self.assertEqual(e.exception.detail, 'Date is not valid')

    def test_periods_validation(self):
        with self.assertRaises(HTTPException) as e:
            ContributionInfo(date='01.02.2012', periods=90, amount=10000, rate=6)
            self.assertEqual(e.exception.status_code, 400)
            self.assertEqual(e.exception.detail, 'Periods is not valid')

            ContributionInfo(date='01.02.2012', periods=-1, amount=10000, rate=6)
            self.assertEqual(e.exception.status_code, 400)
            self.assertEqual(e.exception.detail, 'Periods is not valid')

    def test_amount_validation(self):
        with self.assertRaises(HTTPException) as e:
            ContributionInfo(date='01.02.2012', periods=4, amount=20, rate=6)
            self.assertEqual(e.exception.status_code, 400)
            self.assertEqual(e.exception.detail, 'Amount is not valid')

            ContributionInfo(date='01.02.2012', periods=4, amount=10000000000, rate=6)
            self.assertEqual(e.exception.status_code, 400)
            self.assertEqual(e.exception.detail, 'Amount is not valid')

    def test_rate_validation(self):
        with self.assertRaises(HTTPException) as e:
            ContributionInfo(date='01.02.2012', periods=4, amount=10000, rate=0)
            self.assertEqual(e.exception.status_code, 400)
            self.assertEqual(e.exception.detail, 'Rate is not valid')

            ContributionInfo(date='01.02.2012', periods=4, amount=10000, rate=10)
            self.assertEqual(e.exception.status_code, 400)
            self.assertEqual(e.exception.detail, 'Rate is not valid')
