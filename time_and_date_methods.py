import dateparser.search
from timefhuman import timefhuman
from datetime import datetime
import BookTicket as bt

# This module has two methods:
#   - to extract date from a sentence
#   - to extract time from a sentence


def extract_date(user_input):
    try:
        date_x = (dateparser.search.search_dates(user_input, languages=['en'], settings={'DATE_ORDER': 'DMY'})[0][1])
        present_date = datetime.now()
        if date_x < present_date:
            print("The date has already passed, please enter valid date")
            bt.BookTicket.ask_date()

        return date_x.strftime('%d/%m/%y')
    except:
        return None


def extract_time(user_input):
    try:
        return timefhuman(user_input).strftime('%H:%M')
    except:
        return None


if __name__ == '__main__':
    texta = 'can i please go on the 10-09-2020'
    textb = 'can i please go on the 15/12/20'
    textc = 'i want to travel on july 17 at 3pm'
    textd = 'jul 04 19 '
    texte = '20th of december'
    textf = 'december 14th, 2019'
    textl = 'take me to my destination tomorrow'
    textm = 'in three days time'
    textn = 'in two weeks time'
    textg = 'take me next wednesday'  # doesn't recognise next, wednesday of current week even if in the past
    texth = 'I would like to go on the 1st of next month'  # doesn't recognise next, 1st of current month
    texti = 'on the 1st'  # does the first of the current month
    texto = 'on christmas day'  # picks up nothing (doesn't like christmas)
    textj = 'at the start of next week'  # picks up nothing
    textk = 'a week on monday'  # picks up nothing

    t1 = 'at 17:30'
    t1a = 'at 5:30' # 05:30
    t2 = 'at 4:30pm'
    t3 = '5pm'
    t4 = 'afternoon' # 15:00
    t5 = 'I want to go at 5pm'
    t6 = 'four thirty' # nothing

    training_data = [texta, textb, textc, textd, texte, textf, textg, texth, texti, textj, textk, textl, textm, textn,
                     texto]
    time_training = [t1,t1a,t2,t3,t4,t5,t6]

    # for i in training_data:
    #     print(i + ": ")
    #     print(extract_date(i))
    #
    # print(extract_date("5th of march"))
    for i in time_training:
        print(i + ": ")
        print(extract_time(i))
        # print(timefhuman(i))
    a = timefhuman(t1)
    # print(a.strftime('%H:%M'))
    # print(type(dateparser.search.search_dates(t1, languages=['en'], settings={'DATE_ORDER': 'DMY'})[0][1]))