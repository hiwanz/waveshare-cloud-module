#!/usr/bin/python
# -*- coding:utf-8 -*-

import os
import signal
import socketserver
import logging
import time
import textwrap
from PIL import ImageDraw
from PIL import ImageFont
from PIL import Image
from lib.waveshare_epd import waveshare_epd
from lib.tcp_server import tcp_sver
from lib.http_req import http_req

logging.basicConfig(level=logging.INFO)

need_refresh = True

WEATHER_TEXT = {
    'CLEAR_DAY': 'B',
    'CLEAR_NIGHT': 'C',
    'PARTLY_CLOUDY_DAY': 'H',
    'PARTLY_CLOUDY_NIGHT': 'I',
    'CLOUDY': 'Y',
    'LIGHT_HAZE': 'L',
    'MODERATE_HAZE': 'M',
    'HEAVY_HAZE': 'M',
    'WIND': 'F',
    'LIGHT_RAIN': 'Q',
    'MODERATE_RAIN': 'R',
    'HEAVY_RAIN': 'R',
    'STORM_RAIN': 'T',
    'FOG': 'M',
    'LIGHT_SNOW': 'U',
    'MODERATE_SNOW': 'V',
    'HEAVY_SNOW': 'W',
    'STORM_SNOW': 'X'
}

WEEK_DAY = ['星期日','星期一','星期二','星期三','星期四','星期五','星期六']

def get_assets(filename):
    return os.path.join('assets', filename)

def custom_icon_font(size):
    return ImageFont.truetype(get_assets('fonts/iconfont.ttf'), size)

def english_text_font(size):
    return ImageFont.truetype(get_assets('fonts/QingKeHuangYou.ttf'), size)

def chinese_text_font(size):
    return ImageFont.truetype(get_assets('fonts/WenQuanYi.ttc'), size)

def custom_weather_icon_font(size):
    return ImageFont.truetype(get_assets('fonts/meteocons.ttf'), size)

def draw_center_text(draw, text_y_coordinate, text, size):
    w, h = draw.textsize(text, font=english_text_font(size))
    draw.text(((400 - w)/2, text_y_coordinate), text, font = english_text_font(size), fill = 0)

def draw_center_multiline_text(draw, text_y_coordinate, text, size):
    lines = textwrap.wrap(text, width=20)
    for line in lines:
        w, h = draw.textsize(line, font=chinese_text_font(size))
        draw.text(((400 - w)/2, text_y_coordinate), line, font = chinese_text_font(size), fill = 0)
        text_y_coordinate += h

def draw_weather_forecast(draw, weather_info):
    info_size = len(weather_info)
    padding_w = 10
    text_w, text_h = draw.textsize('01234', font=english_text_font(20))
    icon_w, icon_h = draw.textsize('0', font=custom_weather_icon_font(24))
    text_margin = (400 - padding_w * 2 - info_size * text_w) / info_size / 2
    icon_margin = (400 - padding_w * 2 - info_size * icon_w) / info_size / 2
    for index in range(info_size):
        icon_l = padding_w + index * icon_w + (icon_margin if index == 0 else icon_margin * (1 + index * 2))
        text_l = padding_w + index * text_w + (text_margin if index == 0 else text_margin * (1 + index * 2))
        draw.text((icon_l, 250), WEATHER_TEXT[weather_info[index]['weather']], font = custom_weather_icon_font(24), fill = 0)
        draw.text((text_l, 280), time.strftime('%m-%d',time.strptime(weather_info[index]['date'],'%Y-%m-%dT%H:%M+08:00')), font = english_text_font(20), fill = 0)

class EDPServer(tcp_sver.tcp_sver):
    # Handle client request
    def handle(self):
        global need_refresh
        # Keep connection and refresh in 5min
        current_minute = int(time.strftime("%M", time.localtime()))
        if current_minute%5 != 0:
            need_refresh = True
            self.client = self.request
            self.get_id()
            return
        elif not need_refresh:
            self.client = self.request
            self.get_id()
            return
        try:
            need_refresh = False
            self.client = self.request
            self.get_id()
            self.unlock('123456')
            epd = waveshare_epd.EPD(4.2)
            self.set_size(epd.width,epd.height)

            # Load an image file and display
            # landingImage = Image.open(get_assets('avatar.bmp'))
            # self.flush_buffer(epd.get_buffer(landingImage))
            http_data = http_req.get_http_data()
            soul = http_data.get_soul_info()
            weather_info = http_data.get_5day_weather_info()
            # creat new 1-bit image and draw the image
            screen_image = Image.new('1', (epd.width, epd.height), 255)  # 255: clear the frame
            draw = ImageDraw.Draw(screen_image)
            # draw top status bar
            draw.text((0, 0), time.strftime("%Y-%m-%d %a", time.localtime()), font = english_text_font(20), fill = 0)
            draw.text((135, 0), WEATHER_TEXT[weather_info[0]['weather']], font = custom_weather_icon_font(24), fill = 0)
            draw.text((170, 0), '%s°C' % weather_info[0]['temperature'], font = english_text_font(20), fill = 0)
            draw.text((370, 0), u'\ue51b', font = custom_icon_font(24), fill = 0)
            # draw middle content
            draw_center_text(draw, 50, time.strftime("%d", time.localtime()), 72)
            draw_center_text(draw, 140, WEEK_DAY[int(time.strftime("%w", time.localtime()))], 24)
            draw_center_multiline_text(draw, 180, soul, 20)
            # draw bottom weather
            draw.line([(10, 240), (390, 240)], fill=0)
            draw_weather_forecast(draw, weather_info)
            self.flush_buffer(epd.get_buffer(screen_image))

        except ConnectionResetError :
            self.write_log("lose connect.")
        except KeyboardInterrupt :
            self.close()

if __name__ == "__main__":
    ip = tcp_sver.get_host_ip()
    port = 6868

    logging.info('{0}'.format(ip))

    server = socketserver.ThreadingTCPServer((ip, port), EDPServer)
    server.allow_reuse_address = True

    try:
        server.serve_forever()
    except KeyboardInterrupt:
        server.shutdown()
        os.kill(os.getpid(), signal.SIGTERM)
