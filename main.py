import asyncio
import smtplib as smtp
from telethon import TelegramClient
from email.mime.text import MIMEText
from email.header import Header

from personal_data import my_api_hash, my_api_id, my_email, my_email_password


API_ID = my_api_id
API_HASH = my_api_hash

login = my_email
password = my_email_password

link = 'https://t.me/NRlcjA4mJcowM2Uy'
my_adresses = {'ул.Лазо'} # В этом сете нужно перечислить все адреса, которые нужно отслеживать
limit_of_posts = 2

server = smtp.SMTP('smtp.gmail.com', 587)
server.starttls()
server.login(login, password)
subject = 'Сообщение о подачи воды по адресу'


# Поиск адреса в тексте сообщения
def is_my_adress_in_text(text: str, my_adresses: set):
    search_space = text.split()

    for word in search_space:
        if word.rstrip(',') in my_adresses:
            return word.rstrip(',')
    return


# Парсинг limit_of_posts сообщений из группы по ссылке link
async def parser(API_ID, API_HASH, num_posts, my_adresses, link):
    client = TelegramClient('session name', API_ID, API_HASH)

    await client.start()

    messages = await client.get_messages(link, limit = num_posts)
    result = ''
    for message in messages:
        result = is_my_adress_in_text(message.text, my_adresses)

        if result:
            text = f'адрес {result} был указан в одном из постов'
        else:
            text = (f'мой адрес (мои адреса) не был(и)) 
                    указан(ы) в последних {num_posts} постах')
        
        mime = MIMEText(text, 'plain', 'utf-8')
        mime['Subject'] = Header(subject, 'utf-8')

        server.sendmail(login, 'адрес получателя', mime.as_string())

    await client.disconnect()
    

if __name__ == '__main__':
    asyncio.run(parser(API_ID, API_HASH, limit_of_posts, my_adresses, link))