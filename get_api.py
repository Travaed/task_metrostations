import pandas as pd
import requests
"""from requests_oauthlib import OAuth2Session"""
import json

api_url = "https://api.rasp.yandex.net/v3.0/stations_list/?"
access_token = ""

def get_data_from_api(url,token):
    headers = {
            "Authorization": f"OAuth {token}",
            "format": "json",
            "lang": "ru_RU"
            }
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status() 
        return response.json()
    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")
    except Exception as err:
        print(f"An error occurred: {err}")
    
def load_json():
    with open('/home/userp/Project_DB/task_metrostations/data.json', 'r', encoding='utf-8') as file:
        data = json.load(file)    
    return data

def stations_parser_prepare_data(data):
    list_of_data = []

    for country in data['countries']:
        country_name = country['title']
    
    for region in country['regions']:
        for settlement in region['settlements']:
            settlement_name = settlement['title']
            
            for station in settlement['stations']:
                list_of_data.append({
                    'countries_nm': country_name,
                    'settlements_nm': settlement_name,
                    'stations_nm': station['title'],
                    'direction': station['direction'],
                    'yandex_code_cd': station['codes'].get('yandex_code', ''),
                    'station_type': station['station_type'],
                    'transport_type': station['transport_type'],
                    'longitude': station['longitude'],
                    'latitude': station['latitude']
                })
            
    return list_of_data

if __name__ == "__main__":
    """data = get_data_from_api(api_url, access_token)"""
    data = load_json()
    df = pd.DataFrame(stations_parser_prepare_data(data))
    df.to_csv(r"/home/userp/Project_DB/task_metrostations/stations.csv", index=False, sep=";")
