import json
import requests

from django.conf import settings


def get_uber_data(start_lat, start_long, end_lat, end_long):
    """

    :param start_lat:
    :param start_long:
    :param end_lat:
    :param end_long:
    :return:
    """
    uber_data = []
    response = requests.get(u'{}/estimates/price'.format(settings.UBER_BASE_URL), params={
        u'start_latitude': start_lat,
        u'start_longitude': start_long,
        u'end_latitude': end_lat,
        u'end_longitude': end_long
    }, headers={
        u'Authorization': u'Token {}'.format(settings.UBER_SERVER_TOKEN)
    })
    if response.status_code == 200:
        for item in json.loads(response.content).get(u'prices', []):
            uber_data.append(item)
    return uber_data


def get_ola_data(start_lat, start_long, end_lat, end_long):
    """

    :param start_lat:
    :param start_long:
    :param end_lat:
    :param end_long:
    :return:
    """
    ola_data = []
    response = requests.get(u'{}/products'.format(settings.OLA_BASE_URL), params={
        u'pickup_lat': start_lat,
        u'pickup_long': start_long,
        u'drop_lat': end_lat,
        u'drop_long': end_long
    }, headers={
        u'X-APP-TOKEN': settings.OLA_XAPP_TOKEN
    })
    if response.status_code == 200:
        for item in json.loads(response.content).get(u'ride_estimate', []):
            ola_data.append(item)
    return ola_data


def combine_rides_data(uber_data=None, ola_data=None):
    """

    :param uber_data:
    :param ola_data:
    :return:
    """
    uber_data = uber_data or []
    ola_data = ola_data or []
    combined_data = []
    for item in uber_data:
        combined_data.append({
            u'source': u'uber',
            u'data': item
        })
    for item in ola_data:
        combined_data.append({
            u'source': u'ola',
            u'data': item
        })
    return combined_data
