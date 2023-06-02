import requests
import json
import api
import os
import Config
bottoken = Config.TELEGRAM_API_TOKEN
purl = r"https://api.telegram.org/bot" + bottoken + "/sendPhoto"
def setu(chat_id, from_id, message):
    try:
        if chat_id > 0:
            res = requests.get(r'https://api.lolicon.app/setu/v2?r18=1&' + str(message[6:]))
        else:
            #@blingcc_bot /setu
            res = requests.get(r'https://api.lolicon.app/setu/v2?r18=1&' + str(message[19:]))
        data = res.json()
        datas = data["data"]
        for dat in datas:
            url = dat['urls']['original']
            n_res = requests.get(url)
            f = n_res.content
            data = {
                'chat_id': chat_id,
                'reply_to_message_id': from_id
            }
            files = {
                'photo': f
            }

            requests.post(api.purl, data=data, files=files)

    except:
        pass

