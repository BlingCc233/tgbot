__author__ = 'BlingCc'

import glob
import json
import os
import shutil

import instaloader as instaloader
import requests
from flask import request
from instaloader import Post

import plugins.Instagram
import plugins.Spotify
import plugins.Setu
from Config import *
from plugins.mihoyo import main_handler

bottoken = TELEGRAM_API_TOKEN
surl = r"https://api.telegram.org/bot" + bottoken + "/sendMessage"
purl = r"https://api.telegram.org/bot" + bottoken + "/sendPhoto"
vurl = r"https://api.telegram.org/bot" + bottoken + "/sendVideo"



def cmds(message, chat_id, from_id, update):
    if "/hello" in message:
        print(message)
        index(chat_id, from_id)
    if "/help" in message:
        print(message)
        commands(chat_id, from_id)
    if "/college" in message:
        print(message)
        webs(chat_id, from_id, message)
    if "/galgame" in message:
        print(message)
        webs(chat_id, from_id, message)
    if "/insdown" in message:
        print(message)
        plugins.Instagram.insd(chat_id, from_id, message)
    if "/setu" in message:
        print(message)
        plugins.Setu.setu(chat_id, from_id, message)
    if "/whats" in message:
        print(message)
        if chat_id == 1945870291:
            send_message(chat_id, from_id, "🔐Clash订阅:\nhttps://pqjc.site/api/v1/client/subscribe?token=59af7f013010af9d62f12a365bc7966c")
        else:
            send_message(chat_id, from_id, "🔐Clash订阅\t？\t自己买咯:\nhttps://xn--mes358aby2apfg.com/#/register?code=97JHU2xB")
    if "/holidays" in message:
        print(message)
        holidays(chat_id, from_id)
    if "/mihoyo" in message:
        print(message)
        if chat_id == 1945870291 or update["message"]["from"]["id"] == 1945870291:
            main_handler(None, None)
            send_message(chat_id, from_id, "米游社签到成功！")
        else:
            send_message(chat_id,from_id,"您尚未绑定米游社账号，无法使用此功能！\n请联系管理员绑定账号！")

# 定义回调函数
def button_callback(update, context):
    query = update["callback_query"]
    if query["data"] == 'cmd':
        commands(query["from"]["id"], None)
    elif query["data"] == 'world':
        payload = {
            'chat_id': query["from"]["id"],
            'text': '您点击了World按钮！'
        }
        response = requests.post(surl, json=payload)



def send_message(chat_id,from_id, message):
    decodedata={}
    decodedata["text"]=message
    decodedata["chat_id"]=chat_id
    decodedata["reply_to_message_id"]=from_id
    response=requests.post(url=surl,data=decodedata)
    print(response.text)




def send_sticker(chat_id, sticker):
    # 构造请求的URL
    url = r"https://api.telegram.org/bot" + bottoken + r"/sendSticker"
    # 构造请求的参数
    params = {
        "chat_id": chat_id,
        "sticker": sticker
    }
    response = requests.post(url, data=params)
    pass

def get_holidays():
    #today = datetime.now().strftime('%Y-%m-%d')
    url = f'https://date.nager.at/api/v3/NextPublicHolidaysWorldwide/'
    try:
        response = requests.get(url)
        response.raise_for_status() # 如果响应状态码不为 200，则抛出异常
        holidays = response.json()
    except (requests.exceptions.RequestException, ValueError) as e:
        raise Exception(f'Error occurred while fetching holidays: {str(e)}')

    chinese_holidays = [holiday for holiday in holidays if holiday['countryCode'] == 'CN']
    international_holidays = [holiday for holiday in holidays if holiday['global']]

    return chinese_holidays, international_holidays

def holidays(chat_id, from_id):
    try:
        chinese_holidays, international_holidays = get_holidays()
        # 在这里编写处理假期数据的代码
    except Exception as e:
        print(f'Error occurred: {str(e)}')

    message = 'Today\'s holidays:\n\n'

    if chinese_holidays:
        message += 'Chinese holidays:\n'
        for holiday in chinese_holidays:
            message += f"- {holiday['localName']} ({holiday['name']})\n"
        message += '\n'

    if international_holidays:
        message += 'International holidays:\n'
        for holiday in international_holidays:
            message += f"- {holiday['name']} ({holiday['countryCode']})\n"

    if not chinese_holidays and not international_holidays:
        message += 'No holidays today.'

    send_message(chat_id,from_id, message)


def index(chat_id, from_id):
    # 定义自定义键盘
    if chat_id > 0:
        inline_keyboard = [[{'text': '👨🏼‍💻Developer', 'url': 'https://github.com/blingcc233'},
                            {'text': '📖命令列表', 'callback_data': 'cmd'}],
                           [{'text': '🔗源码', 'url': 'https://github.com/blingcc233/tgbot'},
                            {'text': '⚙中文', 'url': 'https://t.me/setlanguage/zhcncc'}],
                           [{'text': '👴の主页', 'url': 'https://blingcc.eu.org/'},
                            {'text': '🧩反馈问题', 'url': 'https://t.me/BlingCc233'}]]
    else:
        inline_keyboard = [[{'text': '👨🏼‍💻Developer', 'url': 'https://github.com/blingcc233'}],
                           [{'text': '🔗源码', 'url': 'https://github.com/blingcc233/tgbot'},
                            {'text': '⚙中文', 'url': 'https://t.me/setlanguage/zhcncc'}],
                           [{'text': '👴の主页', 'url': 'https://blingcc.eu.org/'},
                            {'text': '🧩反馈问题', 'url': 'https://t.me/BlingCc233'}]]

    # 将自定义键盘转换为JSON格式字符串
    reply_markup = {'inline_keyboard': inline_keyboard}
    data = {
        'chat_id': chat_id,
        'text': 'Cc的机器人',
        'reply_markup': json.dumps(reply_markup),
        'reply_to_message_id': from_id
    }
    response = requests.post(surl, data=data)



def commands(chat_id, from_id):
    theList = """
        点击对应命令即可：
        /hello -打个招呼
        /holidays -holiday
        /help -命令列表
        /whats_the_subscribe -clash
        /mihoyo -sign
        /college -大学无忧
        /galgame -gal资源
        /insdown -ins下载
    """

    send_message(chat_id,from_id, theList)


def webs(chat_id, from_id, message):
    if "/galgame" in message:
        inline_keyboard = [[{'text': '🎮Gal', 'url': 'https://pan.zhacg.com/od2'}],
                            [{'text': '(广告)MacApp', 'url': 'http://ahcos.com/list.php?fid=42'}]]
    if "/college" in message:
        inline_keyboard = [[{'text': '📚网课资源', 'url': 'https://www.techfens.com/posts/buguake.html'}],
                             [{'text': '(广告)WinApp', 'url': 'https://www.uy5.net/'}]]
    reply_markup = {'inline_keyboard': inline_keyboard}

    data = {
        'chat_id': chat_id,
        'text': message[1:].upper(),
        'reply_markup': json.dumps(reply_markup),
        'reply_to_message_id': from_id
    }
    requests.post(surl, data=data)

