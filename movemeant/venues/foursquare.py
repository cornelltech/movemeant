import os
import requests

GEO_PROVIDER = 'https://api.foursquare.com/v2/venues/search'

# reference: https://developer.foursquare.com/categorytree
GEO_PROVIDER_CATEGORY_EXCLUSION = [
    "Neighborhood",
    "City",
    "County",
    "Country",
    "State",
    "Town",
    "Village",
    "States & Municipalities"
]


def process_response(response):
    """
    for now return only the first response in the search array
    as long as it is not a generic neighborhood or something
    """
    for result in response['response']['venues']:
        categories = result['categories']
        if categories:
            primary_category = [category for category in categories if category['primary']][0]
            if primary_category['name'] not in GEO_PROVIDER_CATEGORY_EXCLUSION:
                return {
                    'name': result['name'],
                    'category': primary_category['pluralName'],
                    'foursquare_id': result['id'],
                    'lat': result['location']['lat'],
                    'lng': result['location']['lng'],
                }

    return None


def search(lat, lng, radius=100):
    """
    perform a query against a geo provider
    """
    params = {
        'll': str(lat) + ',' + str(lng),
        'client_id': os.environ.get("FOURSQUARE_CLIENT_ID"),
        'client_secret': os.environ.get("FOURSQUARE_CLIENT_SECRET"),
        'v': os.environ.get("FOURSQUARE_V")
    }
    response = requests.get(GEO_PROVIDER, params=params)
    if response.status_code == 200:
        return process_response(response.json())
    else:
        return None
