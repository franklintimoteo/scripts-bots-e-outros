#!/home/dietpi/newsjeff/env/bin/python
import requests
import xml.etree.ElementTree as ET


#videoId title published
url = "https://www.youtube.com/feeds/videos.xml?channel_id=UClz3DneoYlccluy4hBlx86Q"
r = requests.get(url)
root_tree = ET.fromstring(r.text)

videoid = root_tree[7].find("{http://www.youtube.com/xml/schemas/2015}videoId").text #RkweMmYHvVw
published = root_tree[7].find("{http://www.w3.org/2005/Atom}published").text #2022-10-13T12:15:35+00:00'

from datetime import datetime, timezone
published = datetime.fromisoformat(published)
time_now = datetime.now(timezone.utc)

# crontab vai executar a cada 10 minutos
# se for um video recente vai enviar para grupo telegram
if (time_now - published).seconds < 60*100: #10 minutos
    # evita carregamento desnecessário caso não precise enviar
    from os import getenv
    import telebot
    from dotenv import load_dotenv

    load_dotenv()
    
    #envia mensagem telegram
    url_video = "https://www.youtube.com/watch?v=%s" %videoid
    TOKEN = getenv("TOKEN")
    CHATID = getenv("CHATID")
    #tb = telebot.TeleBot(TOKEN, parse_mode="markdown")
    tb = telebot.TeleBot(TOKEN)
    msg = tb.send_message(CHATID, url_video)
    tb.pin_chat_message(CHATID, msg.message_id)
