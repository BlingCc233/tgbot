

<div align="center">
  
# Telegram-Bot
> 🤖一个使用了<a href="https://github.com/instaloader/instaloader">instaloader</a>和Python的开箱即用的tg机器人

  <p align="center">
  <a href="https://github.com/BlingCc233/tgbot/releases">
    <img src="https://img.shields.io/github/v/release/BlingCc233/tgbot?color=blueviolet&include_prereleases&style=for-the-badge" alt="release">
  </a>
</p>

## 声明
一切开发旨在学习，请勿用于非法用途
  <br/>
_tgbot的动漫形象尚未建立_
</div>

## 启动
- 使用时仅需修改`Config.py`中的机器人token`TELEGRAM_API_TOKEN`，以及`/mihoyo.py`中的抓包信息(请自行参考注释)
- 不需要的功能请直接用`'''`多行注释掉
- 需要的功能请自行参照源码补充
## 功能
- 参考`/api.py`的注释

| 功能        | 说明                       |
| ---------- | ------------------------- |
| hello      | 发送 /hello                 |
| 命令列表     | /help                     |
| 翻墙链接   | /whats_the_subscribe       |
| 米哈游签到     | 发送/mihoyo                  |
| ins解析下载        | 图片视频均可以/insdown url |
| 各种资源     | 参考/help      |
| 涩图！！！   | 参考readme涩图用法/setu  |

## 施工中的功能
- [ ] QRcode二维码生成
- [X] 群聊（群聊暂不支持callback请求）
- [ ] 今日人品
- [X] 涩图
- [ ] 原神小助手
- [ ] 社工库
- [ ] Spotify歌曲下载
- [ ] GPT

## 涩图
- 使用`/setu `自定义涩图类型，for instance:`/setu tag=萝莉|少女&tag=白丝|黑丝&num=3`
- <a href="https://api.lolicon.app/#/">参考涩图API调用方法</a>
