# 4.2inch e-Paper Cloud Module墨水屏开发Demo

## 运行环境

- 硬件环境：[4.2inch e-Paper Cloud Module](https://www.waveshare.net/wiki/4.2inch_e-Paper_Cloud_Module)
- 软件环境：Python3+Pip3
- 系统环境：macOS Bigsur v11+

## 数据API

代码中用到了：[彩云天气api](https://open.caiyunapp.com/%E5%BD%A9%E4%BA%91%E5%A4%A9%E6%B0%94_API_%E4%B8%80%E8%A7%88%E8%A1%A8)，[和风天气api](https://dev.qweather.com/docs/api/)和Alone88提供的[毒鸡汤api](https://v1.alapi.cn/api/soul)

项目中用到的API Key均从网上搜索得来，仅做学习用途，请勿商用，谢谢配合。

## 运行效果

使用本项目代码的前提是假设你已经了解如何配置微雪的4.2inch e-Paper Cloud Module，配置好硬件后，在上位机运行如下代码：

```python
python3 epdserv.py
```

唤醒模块后运行效果如下：

![demo](https://user-images.githubusercontent.com/338102/111144097-90d51c80-85c1-11eb-955e-6d58c6f0a148.jpg)
