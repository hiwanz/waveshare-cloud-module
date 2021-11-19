#!/usr/bin/python
# -*- coding:utf-8 -*-

import requests


class get_http_data():
    def __init__(self, location=('福州', '台江')):
        self.headers = {
            'Content-Type': 'application/json',
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.150 Safari/537.36'
        }
        location_url = 'http://restapi.amap.com/v3/geocode/geo?key=73832f0792532300af11b193225c10bb&city=%s&address=%s' % location
        json_data = requests.get(location_url, headers = self.headers)
        json_data = json_data.json()
        self.gps = json_data['geocodes'][0]['location']

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
        self.url = 'https://api.muxiaoguo.cn/api/dujitang'
        json_data = requests.get(self.url, headers = self.headers)
        json_data = json_data.json()
        
        return json_data['data']['comment']
