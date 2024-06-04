import os
if not os.path.exists("session"):
    os.makedirs("session")

def banner():
    print("BUNG DROID")

try:
    from telethon import TelegramClient
    from telethon.errors import SessionPasswordNeededError, PhoneNumberBannedError
    import sqlite3
    from time import sleep
except ImportError:
    os.system("pip install telethon")

def create_session():
    phone = input("Masukkan Nomor Telegram Anda (dalam format internasional, contoh: +628xxxxxxxxxx): ")
    try:
        api_id = 2182338
        api_hash = 'fa411eff2ec7dcf61bdfadd2478e07bb'
        
        client = TelegramClient("session/"+phone, api_id, api_hash)
        client.connect()

        if not client.is_user_authorized():
            try:
                client.send_code_request(phone)
                client.sign_in(phone, input("Masukkan kode verifikasi Anda: "))
                print("Sesi berhasil dibuat untuk", phone)
                with open("list.txt", "a") as file:
                    file.write(phone + "\n")
                client.disconnect()
            except SessionPasswordNeededError:
                password = input("Masukkan kata sandi 2FA Anda: ")
                client.start(phone, password)
                print("Sesi berhasil dibuat untuk", phone)
                with open("list.txt", "a") as file:
                    file.write(phone + "\n")
                client.disconnect()
            except PhoneNumberBannedError:
                print("Nomor telepon Anda telah diblokir. Harap coba dengan nomor telepon lain.")
                client.disconnect()
        else:
            print("Sesi sudah ada")
            client.disconnect()
    except (sqlite3.DatabaseError, sqlite3.OperationalError):
        print("Kesalahan sesi, hapus file sesi lama dan buat yang baru")
    except Exception as e:
        print(e)

print("Tekan CTRL+C untuk menghentikan alat")
while True:
    create_session()