from datetime import date, datetime

def get_today_date():
    return date.today()

def get_weekday_name():
    day_of_the_week = datetime.today().weekday()
    weekdays = ['Poniedziałek', 'Wtorek', 'Środa', 'Czwartek', 'Piątek', 'Sobota', 'Niedziela']
    return weekdays[day_of_the_week]