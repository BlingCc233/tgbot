import glob
import os
import shutil

import requests
from instaloader import Post, instaloader
import instaloader
from Config import *
import api

def insd(chat_id, from_id, message):
    try:
        if not message.startswith("/insdown http") and chat_id > 0:
            api.send_message(chat_id, from_id, "语法错误，请使用/insdown url下载图片")
            return
        if chat_id < 0 and not message.startswith("@blingcc_bot /insdown"):
            api.send_message(chat_id, from_id, "语法错误，请使用 @blingcc_bot /insdown url 下载图片")
            return
        if chat_id > 0:
            url = message[9:]
        else:
            url = message[22:]
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
        api.send_message(chat_id, from_id, "正在发送图片/视频……(*^▽^*)")
        # 打开所有jpg文件
        for file_path in jpg_files:
            with open(file_path, 'rb') as f:
                # 发送图片
                data = {
                    'chat_id': chat_id,
                    'reply_to_message_id': from_id
                }
                files = {
                    'photo': f
                }

                requests.post(api.purl, data=data, files=files)
        # 获取子目录下所有mp4文件的文件路径
        mp4_files = glob.glob(os.path.join(dir_path, '*.mp4'))
        # 打开所有mp4文件
        for file_path in mp4_files:
            with open(file_path, 'rb') as f:
                # 发送视频
                data = {
                    'chat_id': chat_id,
                    'reply_to_message_id': from_id
                }
                files = {
                    'video': f
                }
                requests.post(api.vurl, data=data, files=files)
        # 删除文件夹
        shutil.rmtree(dir_path)
    except Exception as e:
        api.send_message(chat_id, from_id, "" + str(e) + "好像出错了……(╥╯^╰╥)")
