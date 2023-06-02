__author__ = 'BlingCc'

from flask import Flask, request
import api
import requests
import time
from Config import *

app = Flask(__name__)


bottoken = TELEGRAM_API_TOKEN
rurl = r"https://api.telegram.org/bot" + bottoken + "/getUpdates"
surl = r"https://api.telegram.org/bot" + bottoken + "/sendMessage"
curl = r"https://api.telegram.org/bot" + bottoken + "/ansewrCallbackQuery"


res = None
def get_updates(offset=None):

    try:
        params = {"offset": offset}
        response = requests.get(rurl, params=params)
        global res
        res = response
        print(response.text)
        if response.status_code != 200:
            raise Exception("Failed to get updates")
        data = response.json()
        if data["ok"] and data["result"]:
            for update in data["result"]:
                # 如果是消息更新
                if "message" in update:
                    message = update["message"]
                    chat_type = message["chat"]["type"]
                    api.cmds(message["text"], message["chat"]["id"], message["message_id"], update)

                # 如果是回调查询更新
                elif "callback_query" in update:
                    # if update["callback_query"]["message"]["chat"]["id"] > 0:
                    # 处理回调查询
                    api.button_callback(update, None)

                # 更新offset，以便获取下一批更新
                offset = update["update_id"] + 1
    except (requests.exceptions.RequestException, ValueError, KeyError) as e:
        print(f'Error occurred while fetching updates: {str(e)}')
        data = res.json()
        if data["ok"] and data["result"]:
            for update in data["result"]:
                offset = update["update_id"] + 1
        get_updates(offset)

    time.sleep(1)
    # 继续获取更新
    get_updates(offset)

'''监听端口获取tg信息'''
@app.route('/', methods=["POST"])
def indexx():
    return 'Hello, world!'




if __name__ == '__main__':
    get_updates(None)
    app.run(debug=True)