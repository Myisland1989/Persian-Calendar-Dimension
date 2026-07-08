"""
Persian Calendar Dimension
Jalali / Gregorian Converter
"""

import jdatetime


def gregorian_to_jalali(g_date):
    return jdatetime.date.fromgregorian(date=g_date)


def jalali_to_gregorian(j_date):
    return j_date.togregorian()


def days_in_jalali_month(year, month):

    if month <= 6:
        return 31

    elif month <= 11:
        return 30

    else:
        try:
            jdatetime.date(year, 12, 30)
            return 30
        except:
            return 29


def jalali_year_length(year):

    return sum(
        days_in_jalali_month(year, m)
        for m in range(1, 13)
    )
