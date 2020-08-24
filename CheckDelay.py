import station_methods as s
import time_and_date_methods as td
import webscrape as w
import re

# This is a basic module based upon BookTicket and would connect to a delay prediction model if we had one
# Likely to be unused or possibly superseded by a similar module like app.py


def welcome():
    print("Hello!")


class CheckDelay:
    def __init__(self, current_station=None, current_delay=None):
        self.current_station = current_station
        self.current_delay = current_delay

    def start_chat(self):
        welcome()
        if self.current_station is None:
            self.ask_station()
        if self.current_delay is None:
            self.ask_delay()
        # self.confirm()

    def ask_station(self):
        user_input = s.extract_station(input("Which station are you at currently?").lower())
        while s.check_station(user_input) is None:
            user_input = input("I did not get the station name, please try again")
        self.current_station = user_input.title()

    def ask_delay(self):
        user_input = input("For how many minutes have you been delayed?")
        # print(user_input.split())
        numbers = []
        for a in user_input.split():
            if a.isdigit():
                numbers.append(a)
        return numbers[0]

    def confirm(self):
        user_input = input(
            'I understand you are delayed for {0} minutes at {1} station, is this correct?'.format(self.current_delay,
                                                                                                   self.current_station))
        if user_input.lower() == 'yes':
            print('Our best estimate is that you will be delayed at London Liverpool Street by [Prediction model] '
                  'minutes')
        elif user_input.lower() == 'no':
            print('Okay, let\'s try again')
            self.clear_attributes()

    def clear_attributes(self):
        self.current_station = None
        self.current_delay = None


if __name__ == '__main__':
    id1 = CheckDelay()
    id1.start_chat()
    # res = [int(a) for a in user_input.split() is a.isdigit()]
