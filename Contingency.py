import station_methods as s
import time_and_date_methods as td
import webscrape as w
import check_contingency_methods as c

# This is a module used to control a conversation to check for a contingency action, uses methods
# from check_contingency_methods.py
# Likely to superseded by a similar module like app.py so it can be used on a front end


# TODO
#   - account for misspellings, can store common misspellings eg Ipswitch and offer "Did you mean..."
#   - store all input and output stations in order to offer common stations as an option,
#     eg if they are travelling from Norwich offer them "London Liverpool Street"
#   - be able to take in more than one bit of information at a time (can just run the station and the data functions
#     on the same input
#   - could offer multiple options to the user, currently just provides the ticket info of the time closest to input
#     even if there is a cheaper ticket an hour later
def welcome():
    print("Hello!")


class Contingency:
    def __init__(self, location1=None, location2=None, severity=None):
        self.location1 = location1
        self.location2 = location2
        self.severity = severity

    def start_chat(self):
        welcome()
        if self.location1 is None:
            self.ask_location1()
        if self.location2 is None:
            self.ask_location2()
        if self.severity is None:
            self.ask_severity()
        self.confirm()

    def ask_location1(self):
        user_input = s.extract_station(input("Which station have you most recently passed?").lower())
        print(user_input)
        while user_input is None:
            user_input = s.extract_station(input("I did not get the station name, please try again"))
        self.location1 = user_input.title()

    def ask_location2(self):
        user_input = s.extract_station(input("Which station would you have arrived at next?").lower())
        while user_input is None:
            user_input = s.extract_station(input("I did not get the station name, please try again"))
        self.location2 = user_input.title()

    def ask_severity(self):
        user_input = input("Is it partially or fully blocked")
        self.severity = user_input

    def confirm(self):
        user_input = input(
            'I understand your {0} blockage is between {1} and {2}, is this correct?'.format(self.severity,
                                                                                             self.location1,
                                                                                             self.location2))
        if user_input.lower() == 'yes':
            print(c.get_signaller_action(self.location1,self.location2,self.severity))

        elif user_input.lower() == 'no':
            print('Okay, let\'s try again')
            self.clear_attributes()

    def clear_attributes(self):
        self.location1 = None
        self.location2 = None
        self.severity = None


if __name__ == '__main__':
    test1 = Contingency()
    test1.start_chat()
    # print(ed.get_date_from_user("5th of march"))
