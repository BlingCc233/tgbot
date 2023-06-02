__author__ = 'BlingCc'

import glob
import json
import os
import shutil

import instaloader as instaloader
import requests
from flask import request
from instaloader import Post

TELEGRAM_API_TOKEN = 'your token'
bottoken = TELEGRAM_API_TOKEN
surl = r"https://api.telegram.org/bot" + bottoken + "/sendMessage"
purl = r"https://api.telegram.org/bot" + bottoken + "/sendPhoto"
vurl = r"https://api.telegram.org/bot" + bottoken + "/sendVideo"

def cmds(message, chat_id, update):
    if message == '/holidays':
        print(message)
        holidays(chat_id)
    if message == "/hello":
        print(message)
        index(chat_id)
    if message[0:6] == "/whats":
        print(message)
        send_message(chat_id, "🔐Clash订阅:\n")
    if message == "/mihoyo":
        print(message)
        send_message(chat_id, os.popen("python3 /home/tgbot/mihoyo.py"))
    if message == "/help":
        print(message)
        commands(chat_id)
    if message == "/college":
        print(message)
        webs(chat_id, message)
    if message == "/galgame":
        print(message)
        webs(chat_id, message)
    if message[0:8] == "/insdown":
        print(message)
        insd(chat_id, message)






def send_message(chat_id, message):
    decodedata={}
    decodedata["text"]=message
    decodedata["chat_id"]=chat_id
    response=requests.post(url=surl,data=decodedata)
    print(response.text)

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

def holidays(chat_id):
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


    decodedata={}
    decodedata["text"]=message
    decodedata["chat_id"]=chat_id
    response=requests.post(url=surl,data=decodedata)

def index(chat_id):
    # 定义自定义键盘
    inline_keyboard = [[{'text': '👨🏼‍💻Developer', 'url': 'https://github.com/blingcc233'},
                        {'text': '📖命令列表', 'callback_data': 'cmd'}],
                       [{'text': '🔗源码', 'url': 'https://github.com/blingcc233/tgbot'},
                        {'text': '⚙中文', 'url': 'https://t.me/setlanguage/zhcncc'}],
                       [{'text': '👴の主页', 'url': 'https://blingcc.eu.org/'},
                        {'text': '🧩反馈问题', 'url': 'https://t.me/BlingCc233'}]]

    # 将自定义键盘转换为JSON格式字符串
    reply_markup = {'inline_keyboard': inline_keyboard}
    data = {
        'chat_id': chat_id,
        'text': 'Cc的机器人',
        'reply_markup': json.dumps(reply_markup)
    }
    response = requests.post(surl, data=data)

# 定义回调函数
def button_callback(update, context):
    query = update["callback_query"]
    if query["data"] == 'cmd':
        commands(query["from"]["id"])
    elif query["data"] == 'world':
        payload = {
            'chat_id': query["from"]["id"],
            'text': '您点击了World按钮！'
        }
        response = requests.post(surl, json=payload)

def commands(chat_id):
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
    data = {
        'chat_id': chat_id,
        'text': theList
    }
    response = requests.post(surl, data=data)

def webs(chat_id, message):
    if message == "/galgame":
        inline_keyboard = [[{'text': '🎮Gal', 'url': 'https://pan.zhacg.com/od2'}],
                            [{'text': '(广告)MacApp', 'url': 'http://ahcos.com/list.php?fid=42'}]]
    if message == "/college":
        inline_keyboard = [[{'text': '📚网课资源', 'url': 'https://www.techfens.com/posts/buguake.html'}],
                             [{'text': '(广告)WinApp', 'url': 'https://www.uy5.net/'}]]
    reply_markup = {'inline_keyboard': inline_keyboard}
    print(reply_markup)
    data = {
        'chat_id': chat_id,
        'text': message[1:].upper(),
        'reply_markup': json.dumps(reply_markup)
    }
    requests.post(surl, data=data)

def insd(chat_id, message):
    try:
        if message == "/insdown":
            send_message(chat_id, "语法错误，请使用/insdown url下载图片")
            return
        url = message[9:]
        index = url.find('/?')
        if index != -1:
            url = url[:index]

        SHORTCODE = url.split('/')[-1]
        # 使用Instaloader下载给定的URL的图片
        L = instaloader.Instaloader()
        post = Post.from_shortcode(L.context, SHORTCODE)
        # 下载根据url截短出的shortcode的图片
        L.download_post(post, target='insdown')
        # 打开文件夹
        dir_path = 'insdown/'

        # 获取子目录下所有jpg文件的文件路径
        jpg_files = glob.glob(os.path.join(dir_path, '*.jpg'))
        send_message(chat_id, "正在发送图片……(*^▽^*)")
        # 打开所有jpg文件
        for file_path in jpg_files:
            with open(file_path, 'rb') as f:
                # 发送图片
                data = {
                    'chat_id': chat_id
                }
                files = {
                    'photo': f
                }

                requests.post(purl, data=data, files=files)
        # 获取子目录下所有mp4文件的文件路径
        mp4_files = glob.glob(os.path.join(dir_path, '*.mp4'))
        send_message(chat_id, "正在发送视频……(*^▽^*)")
        # 打开所有mp4文件
        for file_path in mp4_files:
            with open(file_path, 'rb') as f:
                # 发送视频
                data = {
                    'chat_id': chat_id
                }
                files = {
                    'video': f
                }
                requests.post(vurl, data=data, files=files)
        # 删除文件夹
        shutil.rmtree(dir_path)
    except Exception as e:
        send_message(chat_id, "" + str(e) + "好像出错了……(╥╯^╰╥)")



