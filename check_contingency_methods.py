import pandas as pd
from nltk.corpus import stopwords

# This module reads the spreadsheet contingency_instructions.xlsx and enables the function get_signaller_action which is
# used in Contingency.py and probably a contingency version of app.py in the future
#   - get_signaller_action takes in 3 inputs and returns 'Instructions to Signallers / Controllers'
#   - if there are additional conditions which are satisfied then 'Instructions to Signallers / Controllers' is returned
#   - if the additional conditions are not satisfied then go_to_next_plan and get_signaller_action_with_code are used
#     to action the plan specified in the 'If false execute' column

data = pd.read_excel('contingency_instructions.xlsx')
df = pd.DataFrame(data)

stopWords = list(set(stopwords.words('english')))
stopWords.extend(['would', 'like', 'travel', 'want', 'go', 'take', 'get', 'ticket', 'please', 'train', 'thank'])


def get_signaller_action(station1, station2, severity):
    for index, row in df.iterrows():
        if (row['Station1'].lower() == station1.lower()) & (row['Station2'].lower() == station2.lower()) & (
                row['Severity'].lower() == severity.lower()) & (pd.isnull(row['Additional Condition'])):
            return row['Instructions to Signallers / Controllers']
        elif (row['Station1'].lower() == station1.lower()) & (row['Station2'].lower() == station2.lower()) & (
                row['Severity'].lower() == severity.lower()) & ((pd.isnull(row['Additional Condition'])) is False):
            user_input = input("Is the following condition true, yes or no: {0}".format(row['Additional Condition']))
            if user_input.lower() == 'yes':
                return row['Instructions to Signallers / Controllers']
            else:
                return go_to_next_plan(row['If false execute'])


def get_signaller_action_edit(station1, station2, severity):
    for index, row in df.iterrows():
        if (row['Station1'].lower() == station1.lower()) & (row['Station2'].lower() == station2.lower()) & (
                row['Severity'].lower() == severity.lower()) & (pd.isnull(row['Additional Condition'])):
            return [None, row['Instructions to Signallers / Controllers']]
        elif (row['Station1'].lower() == station1.lower()) & (row['Station2'].lower() == station2.lower()) & (
                row['Severity'].lower() == severity.lower()) & ((pd.isnull(row['Additional Condition'])) is False):
            return [row['If false execute'], row['Additional Condition']]


def go_to_next_plan(othercode):
    for index, row in df.iterrows():
        if row['Code'] == othercode:
            return get_signaller_action_with_code(othercode)


def get_signaller_action_with_code(code_to_action):
    for index, row in df.iterrows():
        if (row['Code'] == code_to_action) & (pd.isnull(row['Additional Condition'])):
            return [None, row['Instructions to Signallers / Controllers']]
        elif (row['Code'] == code_to_action) & ((pd.isnull(row['Additional Condition'])) is False):
            user_input = input("Is the following condition true, yes or no: {0}".format(row['Additional Condition']))
            if user_input.lower() == 'yes':
                return row['Instructions to  Signallers / Controllers']
            else:
                return go_to_next_plan(row['If false execute'])


def get_severity(user_text):
    if (user_text.lower() in ["full", "fully"]):
        return "Full"
    elif (user_text.lower() in ["partial", "partially"]):
        return "Partial"
    else:
        return None


def get_signaller_action1(station1, station2, severity):
    for index, row in df.iterrows():
        if (row['Station1'].lower() == station1.lower()) & (row['Station2'].lower() == station2.lower()) & (
                row['Severity'].lower() == severity.lower()) & (pd.isnull(row['Additional Condition'])):
            return row['Instructions to Signallers / Controllers']


def get_signaller_action2(station1, station2, severity):
    for index, row in df.iterrows():
        if (row['Station1'].lower() == station1.lower()) & (row['Station2'].lower() == station2.lower()) & (
                row['Severity'].lower() == severity.lower()) & ((pd.isnull(row['Additional Condition'])) is False):
            return row['Additional Condition']


def action2_yes(station1, station2, severity):
    for index, row in df.iterrows():
        if (row['Station1'].lower() == station1.lower()) & (row['Station2'].lower() == station2.lower()) & (
                row['Severity'].lower() == severity.lower()):
            return row['Instructions to Signallers / Controllers']


def action2_no(station1, station2, severity):
    for index, row in df.iterrows():
        if (row['Station1'].lower() == station1.lower()) & (row['Station2'].lower() == station2.lower()) & (
                row['Severity'].lower() == severity.lower()) & ((pd.isnull(row['Additional Condition'])) is False):
            return go_to_next_plan(row['If false execute'])


#
#
# def get_signaller_action2(station1, station2, severity):
#     for index, row in df.iterrows():
#         if (row['Station1'].lower() == station1.lower()) & (row['Station2'].lower() == station2.lower()) & (
#                 row['Severity'].lower() == severity.lower()) & ((pd.isnull(row['Additional Condition'])) is False):
#             user_input = input("Is the following condition true, yes or no: {0}".format(row['Additional Condition']))
#             if user_input.lower() == 'yes':
#                 return row['Instructions to Signallers / Controllers']
#             else:
#                 return go_to_next_plan(row['If false execute'])

def get_additional_condition(user_text):
    if (user_text.lower() in ["yes", "y"]):
        return "yes"
    elif (user_text.lower() in ["no", "n"]):
        return "no"
    else:
        return None


def additional_condition_answer(user_text):
    if (user_text.lower() in ["yes", "y"]):
        return "yes"
    elif (user_text.lower() in ["no", "n"]):
        return "no"
    else:
        return None


# # Create a list of stations
# contingency_stations1 = df["Station1"].tolist()
# contingency_stations2 = df["Station2"].tolist()
# unique_list = set(contingency_stations1 + list(set(contingency_stations2) - set(contingency_stations1)))
# Nltk has a list of 'stopwords' which are words that don't tend to add anything to a sentence and can
# be taken out. We have added some more that are relevant to our problem
if __name__ == '__main__':
    # pprint(df2)
    # print(get_action1('Colchester','Manningtree','Partial'))
    # print(get_signaller_action('Colchester', 'Manningtree', 'Partial'))
    # print(get_signaller_action('Halifax Junction', 'Ipswich', 'Partial'))
    # print(get_signaller_action1('Colchester', 'Manningtree', 'Partial'))
    # # print(get_signaller_action2('Halifax', 'Ipswich', 'Partial'))
    # print(action2_yes('Halifax', 'Ipswich', 'Partial'))
    # # print(action2_yes('Colchester', 'Manningtree', 'Partial'))
    # print(action2_no('Halifax', 'Ipswich', 'Partial'))
    # # print(df.head())
    # # print(get_additional_condition("y"))
    # print(additional_condition_answer("No"))
    print(get_signaller_action("Ipswich", "Stowmarket", "Full"))
    print(get_signaller_action1("Ipswich", "Stowmarket", "Full"))
