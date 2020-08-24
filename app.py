from flask import Flask, render_template, request
# import sqlite3
import station_methods as s
# import station_pairings_sql as sql
import time_and_date_methods as td
import webscrape as w
import Contingency as c
import check_contingency_methods as ccm

app = Flask(__name__)

initial_choice = None
origin = None
destination = None
date = None
time = None
details_correct = None
#### for task 3
location1 = None
location2 = None
severity = None
check_additional_condition = None
additional_question_is_true = None
details_correct_task3 = None
additional_condition = None


# Used to control flow of conversation
def calculate_stage():
    if initial_choice is None:
        return -1
    if origin is None and initial_choice == "Book ticket":
        return 1.0
    elif destination is None and initial_choice == "Book ticket":
        return 1.1
    elif date is None and initial_choice == "Book ticket":
        return 1.2
    elif time is None and initial_choice == "Book ticket":
        return 1.3
    elif details_correct is None and initial_choice == "Book ticket":
        return 1.4
    elif initial_choice == "Book ticket":
        return 1.5
    elif location1 is None and initial_choice == "Check contingency":
        return 3.0
    elif location2 is None and initial_choice == "Check contingency":
        return 3.1
    elif severity is None and initial_choice == "Check contingency":
        return 3.2
    elif additional_condition is not None and initial_choice == "Check contingency":
        return 3.4
    elif details_correct is None and initial_choice == "Check contingency":
        return 3.5
    elif initial_choice == "Check contingency":
        return 3.6


# Used to dynamically ask whichever question is needed to get the information we need
def ask_next_question(stage):
    if stage == 1.1:
        return 'Where are you travelling to from {0}?'.format(origin)
    if stage == 1.2:
        return 'When would you like to travel from {0} to {1}?'.format(origin, destination)
    if stage == 1.3:
        return 'What time would you like to travel on {0}?'.format(date)
    if stage == 1.4:
        return 'I understand you would like to travel from {0} to {1} on {2} at {3}, is this correct?'.format(
            origin,
            destination,
            date,
            time)
    if stage == 3.0:
        return 'Which station have you most recently passed?'
    if stage == 3.1:
        return 'Which station would you have arrived at next?'
    if stage == 3.2:
        return 'Is it partially or fully blocked?'
    if stage == 3.3:
        return 'Any additional condition?, say Yes or No'
    if stage == 3.4:
        return 'Is {0} working?'.format(ccm.get_signaller_action2(location1, location2, severity))
    if stage == 3.5:
        return 'I understand your {0} blockage is between {1} and {2}, is this correct?'.format(severity,
                                                                                                location1,
                                                                                                location2)


# Global variables are reset if someone decides at the end not to change their booking or not to purchase offered ticket
def reset_stage():
    global origin, destination, date, time, details_correct, initial_choice, location1, location2, severity, details_correct_task3, check_additional_condition, additional_question_is_true, additional_question, additional_condition
    origin = destination = date = time = details_correct = initial_choice = location1 = location2 = severity = details_correct_task3 = check_additional_condition = additional_question_is_true = additional_question = additional_condition = None


@app.route("/")
def home():
    reset_stage()
    return render_template("home2020.html")


@app.route("/get")
def get_bot_response():
    global origin, destination, date, time, details_correct, initial_choice, location1, location2, severity, details_correct_task3, additional_question_is_true, check_additional_condition, additional_condition
    userText = request.args.get('msg')
    print('received my event: ' + userText)
    stage = calculate_stage()
    print("Stage:{0}".format(stage))
    response = ''

    if stage == -1:
        if userText == '1':
            initial_choice = "Book ticket"
            response = 'Where do you want to travel from?'
            print("im in if loop1")
        elif userText == '2':
            initial_choice = "Check delay"
            response = 'What is your current location?'
        elif userText == '3':
            initial_choice = 'Check contingency'
            response = 'What is your current location'
        else:
            response = 'Please select from above options'

    if stage == 1.0:  # Extract origin
        extracted_origin = s.extract_station(userText)
        if extracted_origin is not None:
            # extracted_date = td.extract_date(userText)
            # if extracted_date is not None:
            #     date = extracted_date
            # extracted_time = td.extract_time(userText)
            # if (extracted_time is not None) & (extracted_time != '00:00'):
            #     time = extracted_time
            origin = extracted_origin.title()
            response = ask_next_question(calculate_stage())
            print(response)
        else:
            if s.get_matches(s.extract_station2(userText), s.get_station_name_for_spell_check()) is None:
                response = 'I did not get the station name, please try again'
                # response = ask_next_question(calculate_stage())
                # response = s.extract_station(input("I did not get the station name, please try again"))
            else:
                best_matches = s.get_matches(s.extract_station2(userText), s.get_station_name_for_spell_check())
                # response = "Do you mean these?"
                a = str(best_matches)[1:-1]
                # response = "str(best_matches)[1:-1]"
                response = 'Enter station names from this suggested station names {0}\n '.format(a)
    if stage == 1.1:  # Extract destination
        extracted_destination = s.extract_station(userText)
        if extracted_destination is not None:
            # extracted_date = td.extract_date(userText)
            # if extracted_date is not None:
            #     date = extracted_date
            # extracted_time = td.extract_time(userText)
            # if (extracted_time is not None) & (extracted_time != '00:00'):
            #     time = extracted_time
            destination = extracted_destination.title()
            response = ask_next_question(calculate_stage())
            print(response)
        else:
            if s.get_matches(s.extract_station2(userText), s.get_station_name_for_spell_check()) is None:
                response = 'I did not get the station name, please try again'
                # response = ask_next_question(calculate_stage())
                # response = s.extract_station(input("I did not get the station name, please try again"))
            else:
                best_matches = s.get_matches(s.extract_station2(userText), s.get_station_name_for_spell_check())
                # response = "Do you mean these?"
                a = str(best_matches)[1:-1]
                # response = "str(best_matches)[1:-1]"
                response = 'Enter station names from this suggested station names {0}\n '.format(a)
    if stage == 1.2:  # Extract date
        extracted_date = td.extract_date(userText)
        if extracted_date is None:
            response = 'No date received, please try again'
        else:
            extracted_time = td.extract_time(userText)
            if (extracted_time is not None) and (extracted_time != '00:00') and (time is None):
                time = extracted_time
            date = extracted_date
            response = ask_next_question(calculate_stage())
    if stage == 1.3:  # Extract time
        extracted_time = td.extract_time(userText)
        if extracted_time is None:
            response = 'No time received, please try again'
        else:
            time = extracted_time
            response = ask_next_question(calculate_stage())
    if stage == 1.4:  # Confirm
        if userText.lower() != 'no':
            url = w.conv_to_url(origin, destination, date, time)
            journey_options_response = w.scrape_ticket_info(url)
            details_correct = True
            response = '{0} \n Would you like to purchase?'.format(journey_options_response)
        else:
            response = 'Okay, let\'s try again'
            reset_stage()
    if stage == 1.5:  # Provide link
        if userText.lower() != 'no':
            response = '<a href="{0}">{0}</a>'.format(w.conv_to_url(origin, destination, date, time))
            # conn = sqlite3.connect('common_station_pairings.sqlite')
            # sql.increment_or_insert(origin, destination, conn)
            # conn.close()
        else:
            response = 'Okay, let\'s try again'
            reset_stage()

    if stage == 3.0:  # Extract origin
        extracted_location1 = s.extract_station(userText)
        if extracted_location1 is not None:
            # extracted_date = td.extract_date(userText)
            # if extracted_date is not None:
            #     date = extracted_date
            # extracted_time = td.extract_time(userText)
            # if (extracted_time is not None) & (extracted_time != '00:00'):
            #     time = extracted_time
            location1 = extracted_location1.title()
            response = ask_next_question(calculate_stage())
            print(response)
        else:
            if s.get_matches(s.extract_station2(userText), s.get_station_name_for_spell_check()) is None:
                response = 'I did not get the station name, please try again'
                # response = ask_next_question(calculate_stage())
                # response = s.extract_station(input("I did not get the station name, please try again"))
            else:
                best_matches = s.get_matches(s.extract_station2(userText), s.get_station_name_for_spell_check())
                # response = "Do you mean these?"
                a = str(best_matches)[1:-1]
                # response = "str(best_matches)[1:-1]"
                response = 'Enter station names from this suggested station names {0}\n '.format(a)
                # response = ask_next_question(calculate_stage())

        # # If origin is not new, then most travelled to stations will be offered from database
        # conn = sqlite3.connect('common_station_pairings.sqlite')
        # top_destinations = sql.offer_top_destinations(origin, conn)
        # offer_stations_response = 'The most travelled to stations from your selection are: <br/>{0}'.format(
        #     top_destinations)
        # conn.close()
        # if (top_destinations != []) & (destination is None):
        #     response = '{0} \n {1}'.format(offer_stations_response,ask_next_question(calculate_stage()))
        # else:
        #     response = ask_next_question(calculate_stage())
        # print('response: ' + response)
    if stage == 3.1:  # Extract destination
        extracted_location2 = s.extract_station(userText)
        if extracted_location2 is not None:
            location2 = extracted_location2.title()
            response = ask_next_question(calculate_stage())
        else:
            if s.get_matches(s.extract_station2(userText), s.get_station_name_for_spell_check()) is None:
                response = 'I did not get the station name, please try again'
                # response = ask_next_question(calculate_stage())
                # response = s.extract_station(input("I did not get the station name, please try again"))
            else:
                best_matches = s.get_matches(s.extract_station2(userText), s.get_station_name_for_spell_check())
                # response = "Do you mean these?"
                response = 'Enter station names from this suggested station names {0}\n '.format(best_matches)

    if stage == 3.2:  # Extract severity
        extracted_severity = ccm.get_severity(userText)
        print("extracted severity {0}".format(extracted_severity))
        if extracted_severity is None:
            response = 'No severity received, please try again'
        else:
            severity = extracted_severity
            signaller_action = ccm.get_signaller_action_edit(location1, location2, severity)
            # If there is no additional condition then the signaller action is returned
            if signaller_action[0] is None:
                response = "Instructions to Signallers / Controllers: {0}".format(signaller_action[1])
            # If there is an additional condition then the "if false then execute" row = additional_condition
            if signaller_action[0]:
                response = "Is the following additional condition true: {0}".format(signaller_action[1])
                additional_condition = signaller_action[0]


    if stage == 3.4:
        if_true_or_not = ccm.additional_condition_answer(userText)
        print("ans->", if_true_or_not)
        if if_true_or_not.lower() not in ["no"]:
            print("a")
            response = ccm.action2_yes(location1, location2, severity)
        else:
            print("b")
            ccm.go_to_next_plan(additional_condition)
            additional_question_is_true = if_true_or_not
            print(ccm.action2_no(location1, location2, severity))
            response = ccm.action2_no(location1, location2, severity)

    if stage == 3.5:  # Confirm
        if userText.lower() != 'no':
            response = ccm.get_signaller_action(location1, location2, severity)
        else:
            response = 'Okay, let\'s try again'
            reset_stage()

    print("Response: {0}".format(response))
    # print(initial_choice)
    print("location1:{0} location2:{1} severity:{2}".format(location1, location2, severity))
    return response


if __name__ == "__main__":
    app.run()