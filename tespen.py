import os, sys
import re
import random
import sqlite3
from time import sleep
from colorama import Fore, Back, Style
from telethon import TelegramClient, sync, events
from telethon.sync import TelegramClient
from telethon import functions, types
from telethon.errors import *
from telethon.tl.functions.auth import ResetAuthorizationsRequest
from telethon.tl.functions.account import UpdateUsernameRequest
from telethon.tl.functions.messages import GetFullChatRequest
from telethon.tl.functions.channels import JoinChannelRequest
from telethon.tl.functions.messages import ImportChatInviteRequest
from telethon.tl.functions.photos import UploadProfilePhotoRequest
api_id = 2182338
api_hash = 'fa411eff2ec7dcf61bdfadd2478e07bb'
R = Fore.RED 
B = Fore.BLUE
G = Fore.GREEN
Y = Fore.YELLOW
M = Fore.MAGENTA
W = Fore.WHITE
C = Fore.CYAN
BA = Fore.BLACK
SN = Style.NORMAL 
SB = Style.BRIGHT
SD = Style.DIM
BR = Back.RED 
BB = Back.BLUE
BG = Back.GREEN
BY = Back.YELLOW
BM = Back.MAGENTA
BW = Back.WHITE
BC = Back.CYAN
BBA = Back.BLACK
class RefPremium():
    def new_data(self):
        with open("bot.txt","w") as ff:
            bot = input(C+SN+SB+"\nMasukan Link Reff: ")
            ff.write(bot.split("?start=")[0].lstrip("https://t.me/")+"\n")
            ff.write(bot.split("?start=")[1]+"\n")
            while(True):
                cd = input(M+f"Bot options:\n{Y}1: Tombol\n2: Tombol Sebaris\n{M}PILIH: ")
                if cd == "1":
                    ff.write("Tombol")
                    break
                elif cd == "2":
                    ff.write("Tombol Sebaris")
                    break
                else:
                    print("Silahkan Ulangi")
        with open("list_channel.txt","w") as f:
            print(C+SN+SB+"Silahkan Masukkan Link")
            while(True):
                channels = input(C+SN+SB+"Channels/group join: ")
                if channels == "":
                    break
                else:
                    f.write(channels+"\n")
        with open("ex_message.txt","w") as f:
            m = 1
            while(True):
                ex_msg = input(f"Message {m}: ")
                f.write(ex_msg+"\n")
                if ex_msg == "":
                    break
                m=m+1
    def read_data(self):
        lst_bot = []
        lst_pub = []
        lst_prv = []
        lst_msg = []
        with open("bot.txt","r") as bots:
            for bot in bots:
                bot = bot.strip()
                if bot != "":
                    lst_bot.append(bot)
        with open("list_channel.txt","r") as channels:
            for channel in channels:
                channel = channel.strip()
                if channel.find("joinchat") != -1:
                    channel = channel.replace('https://t.me/joinchat/',"")
                    lst_prv.append(channel)
                else:
                    if channel.find("@") != -1:
                        channel.replace("@","")
                    lst_pub.append(channel)
        with open("ex_message.txt",'r') as ex_msg:
            for msg in ex_msg:
                msg = msg.strip()
                if msg != "":
                    lst_msg.append(msg)
        #print(lst_bot,lst_pub,lst_prv)
        return lst_bot,lst_pub,lst_prv,lst_msg
    def connect(self,phone):
        api_id = 19237578
        api_hash = '0d6ea918503661108b1a8ba8c9ba3c9d'
        client = TelegramClient("session/"+phone,api_id,api_hash)
        client.connect()
        #if not client.is_user_authorized():
        #    print(x,"- ",Fore.RED+phone+" Session lỗi!")
        #    client.disconnect()
        return client
    
    def join(self,client,lst_pub,lst_prv):
        self.resp = ""
        for channel in lst_pub:
            #print("Public channel: ",channel)
            ent = client.get_entity(channel)
            try:
                client(JoinChannelRequest(ent))
                print(G+f"{channel}...       ",end = "\r")
            except UserAlreadyParticipantError:
                print ("da join pub")
            except FloodWaitError as e:
                self.resp = "e"
                #print(C+SN+"-"*30)
                print(B+f"{channel}                 ")
                print(SN+SB+R+f"FloodWaitError ", e.seconds)
            except ChannelPrivateError:
                print("Prv err")
            except UsernameInvalidError:
                self.resp = B+channel+"             "
                self.error = "UsernameInvalidError"
        for channel in lst_prv:
            #channel = channel.strip()
            #print("Private channels: "+channel)
            #print(len("https://t.me/joinchat/"))
            #check_bot_pv = bot_pv1.find("t",22,23)
            #if str(check_bot_pv) == "22":
            #bot_pv = "t"+bot_pv2
            #else:
            #bot_pv = bot_pv2
            try:
                client(ImportChatInviteRequest(channel))
                print(G+f"https://t.me/joinchat/{channel}....         ",end = "\r")
            except UserAlreadyParticipantError:
                print(Y+f"https://t.me/joinchat/{channel}             ",end = "\r")
            except InviteHashExpiredError:
                self.resp = B+"https://t.me/joinchat/"+channel
                self.error = f"Liên kết hết hạn, kiểm tra lại!                     \n{SN+SD+BBA}(InviteHashExpiredError)\n"
            except FloodWaitError as e:
                self.resp = "e"
                #print(C+SN+"-"*30)
                print(B+f"https://t.me/joinchat/{channel}           ")
                print(SN+SB+R+f"FloodWaitError ", e.seconds)
        
    def check_data(self):
        if os.stat("bot.txt").st_size == 0:
            self.new_data()
            #lst_bot,lst_pub,lst_prv = read_data()
        else:
            with open("bot.txt","r") as bot:
                print(W+"\nBot saat ini:", G+bot.readline().strip())
                print(W+"Code ref: ",G+bot.readline().strip())
            while(True):
                sl = input(Y+SN+f"Ganti Bot Pilih? :{G+SN+SB}\n1: Yes    2: No\n{Y+SN}Pilih Cok: ")
                if sl == "1":
                    self.new_data()
                    #lst_bot,lst_pub,lst_prv = read_data()
                    break
                elif sl == "2":
                    #lst_bot,lst_pub,lst_prv = read_data()
                    break
                else:
                    print(R+"Silahkan Ulangi")
                    
    def ex_send_msg(self,client,lst_bot,lst_msg):
        for msg in lst_msg:
            client.send_message(lst_bot[0],msg)
            sleep(3)
    def run(self,client,lst_bot,lst_pub,lst_prv,lst_msg):
        code =  f'/start '+ lst_bot[1]
        client.send_message(lst_bot[0],code)
        sleep(2)
        self.join(client,lst_pub,lst_prv)
        sleep(1)
        if lst_bot[2] == "Tombol":
            while(True):
                try:
                    msg = client.get_messages(lst_bot[0],limit=2)
                    #print(msg)
                    for msg in msg:
                        try:
                            msg_done = msg.reply_markup.rows[0].buttons[0].text
                        except AttributeError:
                            pass
                            #print(msg.message)
                    client.send_message(lst_bot[0],msg_done)
                    break
                except UnboundLocalError:
                    sleep(1)
        elif lst_bot[2] == "Tombol Sebaris":
            
            msg = client.get_messages(lst_bot[0],limit=3)
            #print(msg)
            for msg in msg:
                #print(B,msg)
                try:
                    client (functions.messages.GetBotCallbackAnswerRequest ( peer = lst_bot[0] , msg_id = msg.id, data = msg.reply_markup.rows[0].buttons[0].data)) 
                except Exception as e:
                    pass
                    #print(Y,e)
                    #    print ("mode bot salah button")
                    #except AttributeError:
                     #   print("mode bot salah button")
                     #                               except BotResponseTimeoutError:
                    #                                    print(x,"- "+Fore.MAGENTA+phone+R+" BotResponseTimeoutError!")
                     #                                   #client.send_message(bot, message)
                     #                                   #client (functions.messages.GetBotCallbackAnswerRequest ( peer = bot_link2 , msg_id = idz, data = dataz)) 
                     #                                   break
                      #      msg_done = msg.reply_markup.rows[0].buttons[0].text
            #except Exception as e:
           #     print(e)
           # self.error = R+"The current version is not supported Inlinebutton"
           # self.resp = Y+"\nComming soon!"
        self.ex_send_msg(client,lst_bot,lst_msg)
    def main(self):
        self.check_data()
        lst_bot,lst_pub,lst_prv,lst_msg = self.read_data()
        print(lst_msg)
        while(True):
            try:
                i = int(input(B+SN+SB+"Waktu Delay: "))
                break
            except ValueError:
                print(R+"Silahkan Ulangi!")
        with open("list.txt","r") as phones:
            a = 1
            for phone in phones:
                phone = phone.strip()
                #phone = "+6283849304116"
                print(M+SN+"="*50+Y+SN+SB+f"\n[{C}{a}{Y}] {phone}")
                client = self.connect(phone)
                if not client.is_user_authorized():
                    print(R+SN+SB+"                  Session Error!")
                    client.disconnect()
                else:
                    self.run(client,lst_bot,lst_pub,lst_prv,lst_msg)
                    if self.resp == "":
                        #print(M+SN+"-"*50)
                        print(SN+SB+G+"            ℝ𝕖𝕗𝕗𝕖𝕣𝕒𝕝 𝔹𝕖𝕣𝕙𝕒𝕤𝕚𝕝 𝔻𝕚 𝕌𝕟𝕕𝕒𝕟𝕘 ☑️☑️      ")
                    elif self.resp == "e":
                        pass
                    else:
                        print(R+SN+SB+f"{self.error}{self.resp}")
                        break
                    client.disconnect()
                    for j in range(i,0,-1):
                        print(C+SN+f"                  tunggu beberapa {j} detik! ",end="\r")
                        sleep(1)                     
                a = a+1
os.system("clear")
ver ="2.0"
banner =   "𝔸𝕌𝕋𝕆 ℝ𝔼𝔽𝔽𝔼ℝ𝔸𝕃 𝔹𝕆𝕋"
title = C+SN+SB+"Telegram: @yeniitaf"
title1 = C+SN+SB+"Group: @airdropindocrt "
trx = "TR4KtFxkQXMZMsSzb4sskkPakopejgyR5o"
print(M+SB+"                ╔═╗╔═╗  ╔═╗╦╦═╗╔╦╗╦═╗╔═╗╔═╗") 
print(M+SB+"                ╚═╗║    ╠═╣║╠╦╝ ║║╠╦╝║ ║╠═╝") 
print(M+SB+"                ╚═╝╚═╝  ╩ ╩╩╩╚══╩╝╩╚═╚═╝╩") 
print("\n                  "+SD+BBA+B+title+BBA)
print("                 "+SD+BBA+B+title1+BBA)
print(G+"Donasi TRX Seiklasnya : "+SN+SB+Y+trx+BBA)
print("\n                    "+SN+SB+BW+R+banner+BBA)
print("                       "+BR+W+SD+"Verison:"+ver+BBA)
print(W+'▬'+R+'▬'+W+'▬'+R+'▬'+W+'▬'+R+'▬'+W+'▬'+R+'▬'+W+'▬'+R+'▬'+W+'▬'+R+'▬'+W+'▬'+R+'▬'+W+'▬'+R+'▬'+W+'▬'+R+'▬'+W+'▬'+R+'▬'+W+'▬'+R+'▬'+W+'▬'+R+'▬'+W+'▬'+R+'▬'+W+'▬'+R+'▬'+W+'▬'+R+'▬'+W+'▬'+R+'▬'+W+'▬'+R+'▬'+W+'▬'+R+'▬'+W+'▬'+R+'▬'+W+'▬'+R+'▬'+W+'▬'+R+'▬'+W+'▬'+R+'▬'+W+'▬'+R+'▬'+W+'▬'+R+'▬')
RefPremium().main()

