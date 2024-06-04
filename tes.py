from telethon.sync import TelegramClient
from telethon.tl.functions.messages import ImportChatInviteRequest

# Masukkan informasi API Telegram Anda
api_id = '24827540'
api_hash = '85437c48c6ced09a0465091982160a7d'

# Inisialisasi klien Telegram
client = TelegramClient('session_name', api_id, api_hash)

async def main():
    # Mulai sesi klien
    await client.start()
    
    # URL undangan untuk grup Telegram yang ingin Anda bergabung
    invite_link = input(f'https://t.me/joinchat/your_invite_link: ')
    
    try:
        # Kirim permintaan untuk bergabung ke grup menggunakan URL undangan
        result = await client(ImportChatInviteRequest(invite_link))
        print(f'Joined the group successfully!')
    
    except Exception as e:
        print('Failed to join the group:', e)

# Jalankan program utama
with client:
    client.loop.run_until_complete(main())
