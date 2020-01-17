# -*- coding: utf-8 -*-
"""Reading data from socrata datasets
"""
from .constants import *
import requests


def where_between(dataset, parameter, first_value, second_value):
    """Simplified function for responses shorter than one page.
    :param dataset: dataset four by four code
    :param parameter: str, the name of parameter for where ... between query
    :param first_value: minimum value for between
    :param second_value: maximum value for between
    :return: list of records
    """
    api_url = f'https://{CHICAGO_RESOURCE_URL}/resource/{dataset}.json'
    api_uri = api_url + f'?$where={parameter} between "{first_value}" and "{second_value}"'
    response = requests.request(method="GET", url=api_uri, headers=socrata_authorization_header)
    if response.status_code == 200:
        return response.json()
    elif response.status_code == 201:
        raise RuntimeError("Request Processing")
    elif response.status_code == 400:
        raise RuntimeError("Bad Request")
    elif response.status_code == 401:
        raise RuntimeError("Unauthorized")
    elif response.status_code == 403:
        raise RuntimeError("Forbidden")
    elif response.status_code == 404:
        raise RuntimeError("Not Found")
    elif response.status_code == 429:
        raise RuntimeError("Too many Requests")
    elif response.status_code == 500:
        raise RuntimeError("Server Error")
    else:
        return


def where_a_lot_between(dataset, parameter, first_value, second_value):
    """Complete function for multi-query reading of long paginated responses.
    :param dataset: datasets' four by four code
    :param parameter: str, the name of parameter for where ... between query
    :param first_value: minimum value for between
    :param second_value: maximum value for between
    :return: list of records
    """
    def data_chunk(uri):
        response = requests.get(uri, headers=socrata_authorization_header)
        if response.status_code == 200:
            return response.json()
        elif response.status_code == 201:
            raise RuntimeError("Request Processing")
        elif response.status_code == 400:
            raise RuntimeError("Bad Request")
        elif response.status_code == 401:
            raise RuntimeError("Unauthorized")
        elif response.status_code == 403:
            raise RuntimeError("Forbidden")
        elif response.status_code == 404:
            raise RuntimeError("Not Found")
        elif response.status_code == 429:
            raise RuntimeError("Too many Requests")
        elif response.status_code == 500:
            raise RuntimeError("Server Error")
        else:
            return None  # silently return nothing

    api_url = f'https://{CHICAGO_RESOURCE_URL}/resource/{dataset}.json'
    api_call = api_url + f'?$where={parameter} between "{first_value}" and "{second_value}"'

    limit = 1000    # limit of the frame within the time window
    offset = 0
    data = []       # the accumulation of chunks for final result
    data_to_read_left = True

    while data_to_read_left:
        api_frame = api_call + f'&$limit={limit}&$offset={offset}'
        new_chunk = data_chunk(api_frame)
        data.extend(new_chunk)      # Append the newly acquired records to the list
        # a way to detect 'has_more' (with probability of error 1/2000)
        if len(new_chunk) == limit:
            offset += limit
            print('offset: ', offset) # show the man that something's going on.
        else:
            data_to_read_left = False
    return data


def main():
    print("You've launched the datasets.py module of socradata package as __main__")
    return


if __name__ == '__main__':
    main()
    print('Done')