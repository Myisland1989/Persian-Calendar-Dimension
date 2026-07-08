from datetime import date, timedelta
import pandas as pd

from converter import (
    gregorian_to_jalali,
    days_in_jalali_month,
    jalali_year_length
)


# ==========================================
# Settings
# ==========================================

START_DATE = date(2001, 3, 21)   # 1380/01/01
END_DATE   = date(2042, 3, 20)   # 1420/12/29


# ==========================================
# Labels
# ==========================================

MONTH_NAMES = {
    1: "فروردین",
    2: "اردیبهشت",
    3: "خرداد",
    4: "تیر",
    5: "مرداد",
    6: "شهریور",
    7: "مهر",
    8: "آبان",
    9: "آذر",
    10:"دی",
    11:"بهمن",
    12:"اسفند"
}


DAY_NAMES = {
    1:"شنبه",
    2:"یکشنبه",
    3:"دوشنبه",
    4:"سه شنبه",
    5:"چهارشنبه",
    6:"پنجشنبه",
    7:"جمعه"
}


SEASON_NAMES = {
    1:"بهار",
    2:"تابستان",
    3:"پاییز",
    4:"زمستان"
}


# ==========================================
# Helper functions
# ==========================================


def persian_day_number(g_date):

    # Python:
    # Monday=0 Tuesday=1 ... Sunday=6

    mapping = {
        5:1,   # Saturday
        6:2,   # Sunday
        0:3,   # Monday
        1:4,   # Tuesday
        2:5,   # Wednesday
        3:6,   # Thursday
        4:7    # Friday
    }

    return mapping[g_date.weekday()]



def season_number(month):

    if month <= 3:
        return 1

    elif month <= 6:
        return 2

    elif month <= 9:
        return 3

    else:
        return 4



def is_friday(g_date):

    return g_date.weekday() == 4



def next_day_jalali(g_date):

    return gregorian_to_jalali(
        g_date + timedelta(days=1)
    )



# ==========================================
# Build Calendar
# ==========================================


rows = []


day_index = 0
week_index = 0
month_index = 0
quarter_index = 0
season_index = 0


year_index = 0


last_year = None
last_week = None
last_month = None
last_quarter = None
last_season = None


current = START_DATE



while current <= END_DATE:


    day_index += 1


    j_date = gregorian_to_jalali(current)

    jy = j_date.year
    jm = j_date.month
    jd = j_date.day


    shamsi_number = (
        jy * 10000 +
        jm * 100 +
        jd
    )


    # -----------------------------
    # Year
    # -----------------------------

    if jy != last_year:

        year_index += 1
        last_year = jy


    # -----------------------------
    # Week
    # Saturday start
    # -----------------------------

    day_no = persian_day_number(current)


    if jy != last_week:

        week_of_year = 1
        week_index += 1
        last_week = jy


    elif day_no == 1:

        week_of_year += 1
        week_index += 1


    else:

        week_of_year = week_of_year



    # -----------------------------
    # Month
    # -----------------------------

    if (jy, jm) != last_month:

        month_index += 1
        last_month = (jy, jm)



    # -----------------------------
    # Quarter
    # -----------------------------

    quarter = ((jm-1)//3)+1


    if (jy, quarter) != last_quarter:

        quarter_index += 1
        last_quarter = (jy, quarter)



    # -----------------------------
    # Season
    # -----------------------------

    season = season_number(jm)


    if (jy, season) != last_season:

        season_index += 1
        last_season = (jy, season)



    # -----------------------------
    # Day of year
    # -----------------------------

    day_of_year = sum(
        days_in_jalali_month(jy,m)
        for m in range(1,jm)
    ) + jd


    days_in_month = days_in_jalali_month(
        jy,jm
    )


    days_in_year = jalali_year_length(
        jy
    )
        # ======================================
    # Start / End Dates
    # ======================================

    start_of_week = current - timedelta(
        days=(current.weekday()-5) % 7
    )

    end_of_week = start_of_week + timedelta(days=6)


    start_of_month = current

    while True:

        previous = start_of_month - timedelta(days=1)

        p_j = gregorian_to_jalali(previous)

        if p_j.month != jm:

            start_of_month = current
            break

        start_of_month = previous



    end_of_month = current

    while True:

        nxt = end_of_month + timedelta(days=1)

        n_j = gregorian_to_jalali(nxt)

        if n_j.month != jm:

            break

        end_of_month = nxt



    start_of_quarter = current

    while True:

        previous = start_of_quarter - timedelta(days=1)

        p_j = gregorian_to_jalali(previous)

        if ((p_j.month-1)//3+1) != quarter:

            break

        start_of_quarter = previous



    end_of_quarter = current

    while True:

        nxt = end_of_quarter + timedelta(days=1)

        n_j = gregorian_to_jalali(nxt)

        if ((n_j.month-1)//3+1) != quarter:

            break

        end_of_quarter = nxt



    start_of_year = current

    while True:

        previous = start_of_year - timedelta(days=1)

        p_j = gregorian_to_jalali(previous)

        if p_j.year != jy:

            break

        start_of_year = previous



    end_of_year = current

    while True:

        nxt = end_of_year + timedelta(days=1)

        n_j = gregorian_to_jalali(nxt)

        if n_j.year != jy:

            break

        end_of_year = nxt



    # ======================================
    # Flags
    # ======================================

    is_weekend = is_friday(current)

    is_start_week = day_no == 1

    is_end_week = day_no == 7

    is_start_month = jd == 1

    is_end_month = current == end_of_month

    is_start_quarter = (
        jm in [1,4,7,10]
        and jd == 1
    )

    is_end_quarter = (
        current == end_of_quarter
    )

    is_start_year = (
        jm == 1 and jd == 1
    )

    is_end_year = (
        current == end_of_year
    )


    # ======================================
    # Add Row
    # ======================================

    rows.append({

        "MiladyDate": current,

        "ShamsiDate": shamsi_number,

        "ShamsiYear": jy,
        "ShamsiMonth": jm,
        "ShamsiDay": jd,


        "YearIndex": year_index,
        "MonthIndex": month_index,
        "QuarterIndex": quarter_index,
        "SeasonIndex": season_index,

        "DayIndex": day_index,

        "DayOfYear": day_of_year,
        "DaysInMonth": days_in_month,
        "DaysInYear": days_in_year,


        "MonthName": MONTH_NAMES[jm],

        "Season": SEASON_NAMES[season],

        "Quarter": quarter,


        "DayOfWeekNo": day_no,

        "DayOfWeekName": DAY_NAMES[day_no],


        "WeekOfYear": week_of_year,

        "WeekIndex": week_index,


        "WeekStartDate": start_of_week,

        "WeekEndDate": end_of_week,


        "MonthStartDate": start_of_month,

        "MonthEndDate": end_of_month,


        "QuarterStartDate": start_of_quarter,

        "QuarterEndDate": end_of_quarter,


        "YearStartDate": start_of_year,

        "YearEndDate": end_of_year,


        "StartOfWeek": is_start_week,

        "EndOfWeek": is_end_week,


        "StartOfMonth": is_start_month,

        "EndOfMonth": is_end_month,


        "StartOfQuarter": is_start_quarter,

        "EndOfQuarter": is_end_quarter,


        "StartOfYear": is_start_year,

        "EndOfYear": is_end_year,


        "IsWeekend": is_weekend,


        # فعلاً تعطیلات رسمی بعداً اضافه می‌شود
        "Holiday": False,

        "HolidayName": "",


        # فعلاً جمعه غیرکاری است
        "IsWorkingDay": not is_weekend,


        "YearMonth":
            f"{jy}-{jm:02d}",


        "YearQuarter":
            f"{jy}-Q{quarter}"


    })


    current += timedelta(days=1)



# ======================================
# Export
# ======================================


df = pd.DataFrame(rows)


df.sort_values(
    "MiladyDate",
    inplace=True
)


df.to_excel(
    "Calendar.xlsx",
    index=False
)


df.to_csv(
    "Calendar.csv",
    index=False,
    encoding="utf-8-sig"
)


print(
    "Calendar.xlsx and Calendar.csv created successfully"
)
