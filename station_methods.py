
import pandas as pd
from nltk import word_tokenize, pos_tag
from nltk.stem import WordNetLemmatizer
from nltk.stem.porter import *
from nltk.tokenize import sent_tokenize
from nltk.corpus import stopwords
from itertools import permutations
import json
import nltk

# This module has two uses:
#   - To collate station information (alpha3, tiploc codes and name) from stations.csv (provided on UEA portal)
#   - To extract a station from a sentence


lem = WordNetLemmatizer()
stem = PorterStemmer()


def collate_station_info():
    # Read in the csv of station names
    data = pd.read_csv('stations.csv')
    df = pd.DataFrame(data)
    # Converts data frame to a list of stations
    station_list = df["name"].tolist()
    lower_slist = []
    for x in station_list:
        lower_slist.append(x.lower())
    # Create station_codes_all.json which is a dictionary of station linking to tiploc and alpha3 codes
    station_dict = {}
    for index, row in df.iterrows():
        station_dict[row['name']] = {'alpha3': row['alpha3'], 'tiploc': row['tiploc']}
    with open('station_codes_all.json', 'w') as outfile:
        json.dump(station_dict, outfile)
    # Create a new dictionary with tiploc as key and name as value
    tiploc_to_name_dict = {}
    for index, row in df.iterrows():
        tiploc_to_name_dict[row['tiploc']] = row['name']
    with open('station_codes_tiploc_to_name.json', 'w') as outfile:
        json.dump(tiploc_to_name_dict, outfile)


with open('station_codes_all.json') as json_file:
    station_info = json.load(json_file)

with open('station_codes_tiploc_to_name.json') as json_file:
    tiploc_to_name = json.load(json_file)

# Nltk has a list of 'stopwords' which are words that don't tend to add anything to a sentence and can
# be taken out. We have added some more that are relevant to our problem
stopWords = list(set(stopwords.words('english')))
stopWords.extend(['would', 'like', 'travel', 'want', 'go', 'take', 'get', 'ticket', 'please', 'train', 'thank'])


# Tokenises words and removes those in stopWords
def tokenize_words(words):
    tokenized_words = (word_tokenize(words.lower()))
    # Adding non stop words to a new list
    words_filtered = []
    for w in tokenized_words:
        if w not in stopWords:
            words_filtered.append(w)
    return words_filtered


# It is not unlikely that the station name could be more than one word, so all the possible combinations of
# words_filtered are searched using find_station.
# ['london','liverpool','street'] will search for each word individually, then 'london liverpool', 'london street',
# 'liverpool street' etc. 'liverpool street' is the only station name so that is what's returned
def extract_station(user_input):
    words_filtered = tokenize_words(user_input)
    unique_stations = []
    for i in range(len(words_filtered) + 1):
        perm = permutations(words_filtered, i)
        for perms in list(perm):
            # print(perms)
            concatenation = ''
            for element in perms:
                concatenation += str(element) + ' '
            # print(concatenation.rstrip())
            if check_station(concatenation.rstrip()) is not None and \
                    check_station(concatenation.rstrip()) not in unique_stations:
                unique_stations.append(check_station(concatenation.rstrip()))
    if len(unique_stations) == 0:
        return None
    # elif len(unique_stations) == 1:
    #     return unique_stations[0]
    else:
        return unique_stations[0]


# Function looks to find input 'x' in the list of lower case station names, and returns it if true
def check_station(x):
    if x.upper() in station_info:
        return x
    else:
        return None

def get_station_name_for_spell_check():
    with open('station_codes_tiploc_to_name.json') as json_file:
        station_details = json.load(json_file)
        # station_info = json.dumps(json_file)
        list_station_name = []
        for key in station_details.values():
            # print(station_info[key])
            list_station_name.append(station_details.values())
        return list(list_station_name[0])

def extract_station2(user_input):
    words_filtered = tokenize_words(user_input)
    perm_station = []
    final_list = []
    for i in range(len(words_filtered) + 1):
        perm = permutations(words_filtered, i)
        for perms in list(perm):
            # print(perms)
            concatenation = ''
            for element in perms:
                concatenation += str(element) + ' '
                perm_station.append(concatenation.rstrip().upper())
                for num in perm_station: #remove duplicate list items
                    if num not in final_list:
                        final_list.append(num)
    return final_list


def get_matches(query, choices):
    best_match = []
    for i in query:
        for word in choices:
            sd = nltk.edit_distance(i, word)
            if sd<3:
                print(word,sd)
                best_match.append(word)
                # print(best_match)
    return best_match


if __name__ == '__main__':
    text1 = "I would like to go to Norwich"
    # text2 = "Get me a train to Attleborough"
    # text3 = "wymondham high school"
    # t4 = "i would like to travel to norwich"
    print(extract_station(text1))

    print(get_matches(extract_station2(text1), get_station_name_for_spell_check()))


    # extract_station(text2)
    # print(extract_station(text3))
    # print(data)
    # print(df)
    # print(station_list)
    # print(extract_station(t4))
    # print(check_station(extract_station(t4)))
    # print(station_info['ABERDARE']['alpha3'])
    # print(check_station('norwich'))
    # x = word_tokenize("i would like to travel to London Liverpool St, that's all thank you")
    #
    # print(x)
    # print(lem.lemmatize("geese"))
    # print(stem.stem("am"))


