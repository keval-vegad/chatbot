# import sqlite3
import station_methods as s
import time_and_date_methods as td
import webscrape as w
import AllThreeFlow as A
from datetime import datetime

# import station_pairings_sql as sql

# This module is used for controlling a conversation to book a ticket
# It has been superseded by app.py

def welcome():
    print("Hello!")

# conn = sqlite3.connect('common_station_pairings.sqlite')

class BookTicket:
    def __init__(self, origin=None, destination=None, date=None, time=None):
        self.origin = origin
        self.destination = destination
        self.date = date
        self.time = time


    # process_input(input)
    def start_chat(self):
        welcome()
        if self.origin is None:
            self.ask_origin()
        if self.destination is None:
            self.ask_destination()
        if self.date is None:
            self.ask_date()
        if self.time is None:
            self.ask_time()
        self.confirm()

    def ask_origin(self):
        text = input("Where are you travelling from?").lower()
        user_input = s.extract_station(text)
        while user_input is None:
            if s.get_matches(s.extract_station2(text), s.get_station_name_for_spell_check()) is None:
                user_input = s.extract_station(input("I did not get the station name, please try again"))
                break
            else:
                best_match_stations = s.get_matches(s.extract_station2(text), s.get_station_name_for_spell_check())
                print("Do you mean these?")
                print ('\n '.join(best_match_stations))
                user_input = s.extract_station(input("select station name from above list:"))
                break
        self.origin = user_input.title()

    def ask_destination(self):
        text = input("Where are you travelling to?").lower()
        user_input = s.extract_station(text)
        while user_input is None:
            if s.get_matches(s.extract_station2(text), s.get_station_name_for_spell_check()) is None:
                user_input = s.extract_station(input("I did not get the station name, please try again"))
                break
            else:
                best_match_stations = s.get_matches(s.extract_station2(text), s.get_station_name_for_spell_check())
                print("Do you mean these?")
                print('\n '.join(best_match_stations))
                user_input = s.extract_station(input("select station name from above list:"))
                break
        self.destination = user_input.title()

    def ask_date(self):
        user_input = td.extract_date(input("When would you like to travel?"))
        while user_input is None:
            user_input = td.extract_date(input("I did not get the date, please try again"))
        self.date = user_input

    def ask_time(self):
        user_input = td.extract_time(input("What time would you like to travel?"))
        while user_input is None:
            user_input = td.extract_time(input("I did not get the time, please try again in the format HH:MM"))
        self.time = user_input

    def confirm(self):
        user_input = input(
            'I understand you would like to travel from {0} to {1} on {2} at {3}, is this correct?'.format(self.origin,
                                                                                                           self.destination,
                                                                                                           self.date,
                                                                                                           self.time))
        if user_input.lower() == 'yes':
            url = w.conv_to_url(self.origin, self.destination, self.date, self.time)
            w.scrape_ticket_info(url)
            user_confirm = input('Would you like to purchase?')
            if user_confirm.lower() != 'no':
                print(w.conv_to_url(self.origin, self.destination, self.date, self.time))
                A.start_main_chat()
                # sqlite3.connect('common_station_pairings.sqlite')
                # sql.increment_or_insert(self.origin,self.destination)
                # sql.conn.close()
            else:
                print('Okay, let\'s try again')
                self.clear_attributes()
        elif user_input.lower() == 'no':
            print('Okay, let\'s try again')
            self.clear_attributes()

    def clear_attributes(self):
        self.origin = None
        self.destination = None
        self.date = None
        self.time = None


if __name__ == '__main__':
    test1 = BookTicket()
    test1.start_chat()
    # print(ed.get_date_from_user("5th of march"))
