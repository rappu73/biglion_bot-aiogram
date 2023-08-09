import requests
import json


def biglion_api_city():
    url = 'http://127.0.0.1:8000/city'
    response = requests.get(url)
    data = json.loads(response.text)
    return data


def biglion_api_category():
    url = 'http://127.0.0.1:8000/category'
    response = requests.get(url)
    data = json.loads(response.text)
    return data


def biglion_api_link(city, cat):
    url = 'http://127.0.0.1:8000/link'
    params = {'city': city, 'cat': cat}
    response = requests.post(url, params=params)
    data = json.loads(response.text)
    return data

