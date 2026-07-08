"""
Persian Calendar Dimension
Jalali / Gregorian Converter
"""

import jdatetime


def gregorian_to_jalali(g_date):
    """
    Convert Gregorian date to Jalali date

    Input:
        datetime.date

    Output:
        datetime.date (Jalali)
    """

    return jdatetime.date.fromgregorian(date=g_date)


def jalali_to_gregorian(j_date):
    """
    Convert Jalali date to Gregorian date

    Input:
        jdatetime.date

    Output:
        datetime.date
    """

    return j_date.togregorian()


def jalali_year_length(year):
    """
    Return number of days in Jalali year
    """

    if jdatetime.date(year, 12, 30):
        try:
            jdatetime.date(year, 12, 30)
            return 366
        except:
            return 365


def days_in_jalali_month(year, month):

    if month <= 6:
        return 31

    if month <= 11:
        return 30

    try:
        jdatetime.date(year,12,30)
        return 30
    except:
        return 29
