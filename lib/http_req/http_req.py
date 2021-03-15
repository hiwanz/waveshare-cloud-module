#!/usr/bin/python
# -*- coding:utf-8 -*-

import requests
import re
import os


class get_http_data():
    def __init__(self, location=('福州', '台江')):
        self.headers = {
            'Content-Type': 'application/json',
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.150 Safari/537.36'
        }
        location_url = 'https://geoapi.qweather.com/v2/city/lookup?adm=%s&location=%s&key=f3488e987bce466d8ae6b523becf278f' % location
        json_data = requests.get(location_url, headers = self.headers)
        json_data = json_data.json()
        self.gps = '%s,%s' % (json_data['location'][0]['lon'], json_data['location'][0]['lat'])

    def get_5day_weather_info(self):
        self.url = 'https://api.caiyunapp.com/v2.5/ghbkeChNeRd8bvF4/%s/weather.json' % self.gps
        json_data = requests.get(self.url, headers = self.headers)
        json_data = json_data.json()
        daily_weather_info = []

        for weather in json_data['result']['daily']['skycon']:
            daily_weather_info.append({'date': weather['date'], 'weather': weather['value']})
        daily_weather_info[0]['temperature'] = json_data['result']['realtime']['temperature']

        return daily_weather_info

    def get_soul_info(self):
        self.url = 'https://v1.alapi.cn/api/soul'
        json_data = requests.get(self.url, headers = self.headers)
        json_data = json_data.json()
        
        return json_data['data']['title']
