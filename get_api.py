import pandas as pd
import requests
from requests_oauthlib import OAuth2Session

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
    
    

def stations_parser_prepare_data(data):
    list_of_data = []

    for page in data:
        for stations in page["content"]:
            
            temp_dict = {}
            temp_dict['countries_nm'] = stations.get('countries')
            temp_dict['settlements_nm'] = stations.get('settlements')
            temp_dict['stations_nm'] = stations.get('stations')
            temp_dict['direction'] = stations.get('direction')
            temp_dict['yandex_code_cd'] = get_json_string_or_none(stations.get('yandex_code', []))
            temp_dict['station_type'] = stations.get('station_type')
            temp_dict['transport_type'] = stations.get('transport_type')
            temp_dict['long'] = stations.get('longitude')
            temp_dict['lat'] = stations.get('latitude')
            list_of_data.append(temp_dict)
    return list_of_data

if __name__ == "__main__":
    data = get_data_from_api(api_url, access_token) 
    df = pd.DataFrame(stations_parser_prepare_data(data))
    df.to_csv(r"/home/usrerp/ProjectDB/task_metrostations/stations.csv", index=False, sep=";")
