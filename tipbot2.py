import time
import vk_api
from time import sleep
from lxml import html
import requests as req

#vk = vk_api.VkApi(login = '79179170872', password = 'nlirem31')
vktoken='f9b8e9008e89f2d0418a4465a2770024b045a6d40daec647924559a06b0308b4ea2fd0cac4688d3f03ab6'
vk = vk_api.VkApi(token = vktoken)
vk._auth_token()
values = {'out': 0,'count': 100,'time_offset': 60}

def write_msg(user_id, s):
    vk.method('messages.send', {'user_id':user_id,'message':s})

def help(id):
   s1='Я умею здороваться и прощаться, могу рассказать как мои дела и чем я сейчас занимаюсь. А еще вот этот небольшой список полезных штук:\n\n'
   s2='Пиши "/погода" -- я довольно точно ее предсказываю.\n'
   s3='Пиши "/хех" и я несмешно пошучу.\n'
   s4='Пиши "/боль" и я сделаю больно.\n'
   s5='Пиши "/валюта" -- покажу курс доллара и евро.\n Кстати, вот эту палочку: "/" писать тоже нужно;)'
   return s1+s2+s3+s4+s5


def getweather(id):
    r = req.get('https://www.meteoservice.ru/weather/text/name/kazan.html')
    doc = html.document_fromstring(r.text)
    s1='\n'.join(doc.xpath('//*[@id="act_text"]/div[3]/div[2]/div[3]/div[1]/div[1]/div[2]/div[2]/div/div/h3[1]/text()'))+':\n'+'\n'.join(doc.xpath('//*[@id="act_text"]/div[3]/div[2]/div[3]/div[1]/div[1]/div[2]/div[2]/div/div/div[1]/p[2]/text()'))
    s2='\n'.join(doc.xpath('//*[@id="act_text"]/div[3]/div[2]/div[3]/div[1]/div[1]/div[2]/div[2]/div/div/h3[2]/text()'))+':\n'+'\n'.join(doc.xpath('//*[@id="act_text"]/div[3]/div[2]/div[3]/div[1]/div[1]/div[2]/div[2]/div/div/div[2]/p[2]/text()'))
    return s1+'\n'+s2



def bitoc(id):
    r = req.get('https://myfin.by/crypto-rates/bitcoin')
    doc = html.document_fromstring(r.text)
    bit = '\n'.join(doc.xpath('//*[@id="workarea"]/div[1]/div[2]/div[1]/div/div[3]/div[1]/div/text()'))
    return bit

def bash(id):
    r = req.get('http://bash.im/random')
    doc = html.document_fromstring(r.text)
    bash = '\n'.join(doc.xpath('//*[@id="body"]/div[3]/div[@class="text"]/text()'))
    return bash


def kurs(id):
    r = req.get('http://www.cbr.ru')
    doc = html.document_fromstring(r.text)
    kd = ' '.join(doc.xpath('//*[@id="widget_exchange"]/div/table/tbody/tr[2]/td[3]/div/text()'))
    ke = ' '.join(doc.xpath('//*[@id="widget_exchange"]/div/table/tbody/tr[3]/td[3]/div/text()'))
    return 'Курс доллара: '+kd+'\nКурс евро: '+ke



while True:
    response = vk.method('messages.get', values)
    if response['items']:
        values['last_message_id'] = response['items'][0]['id']
    result='Отлично!'
    for item in response['items']:
        print(response)
        if "ивет" in item['body']:
            result='Привет! Я бот, которого написал Вадим. Пока я мало чего умею и нечасто работаю, но скоро многому научусь. Если хочешь узнать подробнее, напиши: "Что ты умеешь?"'
        elif "дела?" in item['body'] or "дела " in item['body'] or item['body']=="как дела" or item['body']=="Как дела":
            result='Отлично!'
        elif "укусики" in item['body']:
            result='Кукусики'
        elif "делаешь" in item['body'] or "делаете" in item['body'] or "занимае" in item['body']:
            result='Пытаюсь правильно соотносить введенный текст с тем, что написал в коде Вадим, чтобы выдавать правильные ответы. Сложно😫'
        elif "пока" in item['body'] or "свидули" in item['body'] or "свидания" in item['body']:
            result='До встречи!'
        elif "Ясн" in item['body'] or "ясн" in item['body'] or "онятн" in item['body']:
            result='угу🙄'
        elif "лох" in item['body'] or "урак" in item['body'] or "урачок" in item['body'] or "ибил" in item['body']:
            result='Не ругайся:('
        elif "асибо" in item['body']:
            result = "Да не за что! ;-)"
        elif "хах" in item['body'] or "аха" in item['body'] or "Хах" in item['body']:
            result = "Да уж, смешно)"
        elif item['body']=="/хех":
            result = bash(item['user_id'])
        elif item['body']=="/боль":
            result = bitoc(item['user_id'])
            result = 'Курс bitcoin на сегодня:'+result+'. А ты так и не купил!'
        elif item['body']=="/погода" :
            result = getweather(item['user_id'])
        elif item['body']=="/валюта" :
            result = kurs(item['user_id'])
        elif 'то ты умеешь' in item['body'] or item['body']=="/help" or item['body']=="/помощь":
            result = help(item['user_id'])
        else:
            result='Пока не знаю, как отвечать на такое 3( Пиши /help и я расскажу что я умею'

        write_msg(item[u'user_id'],result)

    time.sleep(1)
