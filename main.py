from telethon import TelegramClient
from personal_data import my_api_hash, my_api_id
import asyncio

api_id = my_api_id
api_hash = my_api_hash
link = 'https://t.me/NRlcjA4mJcowM2Uy'
my_adresses = {'ул.Лазо'} # В этом сете нужно перечислить все адреса, которые нужно отслеживать
limit_of_posts = 2


# Поиск адреса в тексте сообщения
def is_my_adress_in_text(text: str, my_adresses: set):
    search_space = text.split()

    for word in search_space:
        if word.rstrip(',') in my_adresses:
            return True
    return False

# Парсинг limit_of_posts сообщений из группы по ссылке link
async def parser(api_id, api_hash, num_posts, my_adresses, link):
    client = TelegramClient('session name', api_id, api_hash)

    await client.start()

    messages = await client.get_messages(link, limit = num_posts)
    result = ''
    for message in messages:
        if is_my_adress_in_text(message.text, my_adresses):
            result = 'мой адрес был указан'

    if result:
        print(result)
    else:
        print(f'мой адрес не был указан в последних {num_posts} постах')

    await client.disconnect()


if __name__ == '__main__':
    asyncio.run(parser(api_id, api_hash, limit_of_posts, my_adresses, link))