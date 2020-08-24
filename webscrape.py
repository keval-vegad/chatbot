from requests import get
from requests.exceptions import RequestException
from contextlib import closing
from bs4 import BeautifulSoup
import json
from datetime import datetime, timedelta
import re

# TODO ensure price is in correct £.00 format

# This modules has the following functions:
#   - Provide information on the cheapest ticket from nationalrail.co.uk for chosen journey
#   - Provide a url to link the user to that ticket

with open('station_codes_all.json') as json_file:
    station_info = json.load(json_file)


########################################################################################################################
# These 3 methods are taken from https://realpython.com/python-web-scraping-practical-introduction/
def simple_get(url):
    """
    Attempts to get the content at `url` by making an HTTP GET request.
    If the content-type of response is some kind of HTML/XML, return the
    text content, otherwise return None.
    """
    try:
        with closing(get(url, stream=True)) as resp:
            if is_good_response(resp):
                return resp.content
            else:
                return None

    except RequestException as e:
        log_error('Error during requests to {0} : {1}'.format(url, str(e)))
        return None


def is_good_response(resp):
    """
    Returns True if the response seems to be HTML, False otherwise.
    """
    content_type = resp.headers['Content-Type'].lower()
    return (resp.status_code == 200
            and content_type is not None
            and content_type.find('html') > -1)


def log_error(e):
    """
    It is always a good idea to log errors.
    This function just prints them, but you can
    make it do anything.
    """
    print(e)


########################################################################################################################


# def scrape_ticket_info(url):
#     raw_html = simple_get(url)
#     html = BeautifulSoup(raw_html, 'html.parser')
#     x = html.find_all("script", attrs={"id": "jsonJourney-4-1"})
#     y = json.loads(x[0].text)
#     return 'For your journey from {0} to {1} we have selected the following as the best option:'.format(
#         y['jsonJourneyBreakdown']['departureStationName'], y['jsonJourneyBreakdown']['arrivalStationName']) + \
#            '<br/>Departing: {0}'.format(y['jsonJourneyBreakdown']['departureTime']) + \
#            '<br/>Arriving: {0}'.format(y['jsonJourneyBreakdown']['arrivalTime']) + \
#            '<br/>Duration: {0} hours {1} minutes'.format(y['jsonJourneyBreakdown']['durationHours'],
#                                                          y['jsonJourneyBreakdown']['durationMinutes']) + \
#            '<br/>Changes: {0}'.format(y['jsonJourneyBreakdown']['changes']) + \
#            '<br/>Price: £{0}'.format(y['singleJsonFareBreakdowns'][0]['ticketPrice'])

def scrape_ticket_info(url):
    raw_html = simple_get(url)
    html = BeautifulSoup(raw_html, 'html.parser')
    x = html.find_all("script", attrs={"id": "jsonJourney-4-1"})
    string = re.sub("<.*?>", "", str(x))
    y = json.loads(string)[0]
    # y = json.loads(x[0].text)
    return 'For your journey from {0} to {1} we have selected the following as the best option:'.format(
        y['jsonJourneyBreakdown']['departureStationName'], y['jsonJourneyBreakdown']['arrivalStationName']) + \
           '<br/>Departing: {0}'.format(y['jsonJourneyBreakdown']['departureTime']) + \
           '<br/>Arriving: {0}'.format(y['jsonJourneyBreakdown']['arrivalTime']) + \
           '<br/>Duration: {0} hours {1} minutes'.format(y['jsonJourneyBreakdown']['durationHours'],
                                                         y['jsonJourneyBreakdown']['durationMinutes']) + \
           '<br/>Changes: {0}'.format(y['jsonJourneyBreakdown']['changes']) + \
           '<br/>Price: £{0}'.format(y['singleJsonFareBreakdowns'][0]['ticketPrice'])


def conv_to_url(origin, destination, date, time):
    url_origin = station_info[origin.upper()]['alpha3']
    url_dest = station_info[destination.upper()]['alpha3']
    if date == datetime.now().strftime('%d/%m/%y'):
        url_date = 'today'
    elif date == (datetime.now() + timedelta(days=1)).strftime('%d/%m/%y'):
        url_date = 'tomorrow'
    else:
        url_date = date.replace('/', '')
    url_time = time.replace(':', '')
    return 'http://ojp.nationalrail.co.uk/service/timesandfares/{0}/{1}/{2}/{3}/dep'.format(url_origin, url_dest,
                                                                                            url_date, url_time)


# Example of data taken from national rail website:
# {'jsonJourneyBreakdown': {'departureStationName': 'Norwich', 'departureStationCRS': 'NRW',
# 'arrivalStationName': 'London Liverpool Street', 'arrivalStationCRS': 'LST', 'statusMessage': 'on time',
# 'departureTime': '11:30', 'arrivalTime': '13:19', 'durationHours': 1, 'durationMinutes': 49, 'changes': 0,
# 'journeyId': 1, 'responseId': 4, 'statusIcon': 'GREEN_TICK', 'hoverInformation': None},
# 'singleJsonFareBreakdowns': [{'breakdownType': 'SingleFare', 'fareTicketType': 'Off-Peak Single',
# 'ticketRestriction': '1A', 'fareRouteDescription': 'Travel is allowed via any permitted route.',
# 'fareRouteName': 'ANY PERMITTED', 'passengerType': 'Adult', 'railcardName': '', 'ticketType': 'Off-Peak Single',
# 'ticketTypeCode': 'SVS', 'fareSetter': 'LER', 'fareProvider': 'Great Western Railway', 'tocName': 'Greater Anglia',
# 'tocProvider': 'Great Western Railway', 'fareId': 10, 'numberOfTickets': 1, 'fullFarePrice': 55.7, 'discount': 0,
# 'ticketPrice': 55.7, 'cheapestFirstClassFare': 23.1, 'nreFareCategory': 'FLEXIBLE', 'redRoute': False}],
# 'returnJsonFareBreakdowns': []}

if __name__ == '__main__':
    # raw_html = simple_get('http://ojp.nationalrail.co.uk/service/timesandfares/NRW/LST/tomorrow/1130/dep')
    # print(raw_html)
    # html = BeautifulSoup(raw_html, 'html.parser')
    # print("-----------print x-------------")
    # x = html.find_all("script",attrs={"id":"jsonJourney-4-1"})
    # print(type(str(x)))
    # print("-----------print string-------------")
    # string = re.sub("<.*?>", "", str(x))
    # print(string)
    # # # y = json.loads(x[0].text) already writtern code
    # y = json.loads(string)
    # print("-----------print y-------------")
    # print(type(y))
    # print(y[0])
    # print(x)
    # print("-----------new line-------------")
    # print(y)
    # print(y['singleJsonFareBreakdowns'][0]['fullFarePrice'])
    # print(y['jsonJourneyBreakdown']['departureTime'])
    # # # string = '17/12/19'
    # # # print(string.replace('/',''))
    # # # # print(string)
    # scrape_ticket_info(conv_to_url('Aberdeen','Liverpool lime street','19/12/19','17:30'))
    # print((datetime.now() + timedelta(days=1)).strftime('%d/%m/%y'))
    # print(scrape_ticket_info('http://ojp.nationalrail.co.uk/service/timesandfares/NRW/LST/tomorrow/1130/dep'))
    #
    # url_origin = station_info['Aberdeen'.upper()]['alpha3']
    # print(url_origin)
    # url_dest = station_info['Liverpool lime street'.upper()]['alpha3']
    # print(url_dest)
    # url_date = '19/12/19'.replace('/', '')
    # print(url_date)
    # url_time = '17:30'.replace(':', '')
    # print(url_time)

    print(conv_to_url('Aberdeen', 'Liverpool lime street', '10/10/20', '17:30'))
    scrape_ticket_info(conv_to_url('Aberdeen', 'Liverpool lime street', '10/10/20', '17:30'))
