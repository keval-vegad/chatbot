import json
import lzma
from pprint import pprint


# This module extracts schedules involving any of the stations passing through Norwich - Colchester
# Want to be able to say:
#   - Input: There is a partial/full blockage at this location/between these locations
#   - Output: These are the trains that are affected

def unzip():
    with lzma.open('ga_schedules.json.xz') as f, open('schedules_all_unformatted.json', 'wb') as fout:
        file_content = f.read()
        fout.write(file_content)


###################################
# Manually changed schedules_all_unformatted.json to schedules_all_intermediate.txt and added [ to beginning and ] to
# end of file so we can create a json array
###################################

def convert_to_array():
    with open('schedules_all_intermediate.txt') as f:
        with open('schedules_all_formatted.json', 'w') as f1:
            for line in f:
                f1.write(line.replace("\n", ",").strip())


with open('schedules_all_formatted.json') as json_file:
    ga_schedules = json.load(json_file)

with open('station_codes_tiploc_to_name.json') as json_file:
    tiploc_to_name = json.load(json_file)

colc_to_nrch_tiploc = {"NRCH": "NORWICH", "DISS": "DISS", "HAGHLYJ": "HAUGHLEY JUNCTION", "STWMRKT": "STOWMARKET",
                       "NEEDHAM": "NEEDHAM MARKET", "IPSWESJ": "EAST SUFFOLK JUNCTION",
                       "IPSWICH": "IPSWICH", "IPSWHJN": "HALIFAX JUNCTION", "MANNGTR": "MANNINGTREE",
                       "CLCHSTR": "COLCHESTER"}


def get_colc_to_nrch_schedules():
    colc_to_nrch_schedules = []
    for i in ga_schedules:
        schedule = {}
        for location in i["JsonScheduleV1"]['schedule_segment']['schedule_location']:
            try:
                if location['departure'] is not None:
                    schedule[location['tiploc_code']] = location['departure'].replace("H", "")
                else:
                    schedule[location['tiploc_code']] = location['pass'].replace("H", "")
            except KeyError:
                if location['arrival'] is not None:
                    schedule[location['tiploc_code']] = location['arrival'].replace("H", "")
                else:
                    schedule[location['tiploc_code']] = location['pass'].replace("H", "")

        flag = False
        for l in schedule:
            if l in colc_to_nrch_tiploc:
                flag = True
                break
        if flag == True:
            colc_to_nrch_schedules.append(schedule)
    with open('schedules_colc_to_nrch.json', 'w') as outfile:
        json.dump(colc_to_nrch_schedules, outfile)


with open('schedules_colc_to_nrch.json') as json_file:
    schedules_colc_to_nrch = json.load(json_file)


def conv_to_mins_HHMM(time):
    return int(time[:2]) * 60 + int(time[-2:])


def get_affected_trains(station1, station2, time):
    affected_trains = {}
    affected_trains_sorted = []
    for dict in schedules_colc_to_nrch:
        if (station1 in dict) and (station2 in dict) and (
                (conv_to_mins_HHMM(dict[station1]) > conv_to_mins_HHMM(time)) or (
                conv_to_mins_HHMM(dict[station2]) > conv_to_mins_HHMM(time))):
            affected_trains[int(list(dict.values())[0])] = (list(dict.keys())[0], list(dict.keys())[-1], list(dict.values())[-1])
    # print(affected_trains)
    for key in sorted(affected_trains.keys()):
        train = "{0} service from {1} to {2} arriving at {3}".format(key, affected_trains[key][0],
                                                                     affected_trains[key][1], affected_trains[key][2])
        affected_trains_sorted.append(train)
    return affected_trains_sorted


# print(ga_schedules[1]["JsonScheduleV1"]['schedule_segment']['schedule_location'][0]['tiploc_code'])
if __name__ == '__main__':
    # get_colc_to_nrch_schedules()

    for i in get_affected_trains('HAGHLYJ', 'DISS', '20:50'):
        print(i)
    # get_affected_trains('HAGHLYJ', 'DISS', '20:50')
