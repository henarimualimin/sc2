from telethon.sync import TelegramClient

api_id = '24827540'
api_hash = '85437c48c6ced09a0465091982160a7d'
bot_token = '7161930638:AAEUuEM8CknZhTCkEcfJPaxvi9FnMXkJH-Q'

# Mulai sesi bot dengan API ID, API hash, dan token bot yang diberikan
with TelegramClient('session_name', api_id, api_hash) as client:
    # Kirim pesan menggunakan metode .send_message() dengan menyertakan username atau ID pengguna sebagai parameter
    client.send_message('username_or_entity', 'Hello, Bot!')
    print('Pesan terkirim!')
