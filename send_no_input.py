from inspect import getfullargspec as getargspec
from web3 import Web3
import json
import os
import time

# Kode warna ANSI
hijau = "\033[1;32m"
drk = '\x1b[1;30m'
res = "\033[1;0m"
abu = "\033[1;30m"
abu2 = "\033[0;37m"
putih = "\033[1;37m"
biru = "\033[1;34m"
bir = "\033[0;34m"
purp = "\033[0;35m"
purple = "\033[1;35m"
hijau2 = "\033[0;32m"
emas = "\033[0;33m"
kuning = "\033[1;33m"
merah1 = "\033[0;31m"
merah = "\033[1;31m"
cyan = "\033[1;36m"
fex1="»"
fex2="«"
kur1 = abu+"["+res
kur2 = abu+"]"+res
grs=bir+"▬"*69
grs1=hijau+fex1*37
grs2=hijau+fex2*37
kib=biru+fex1+res
kur3 = merah+"〘"+putih+"+"+merah+"〙"+res
plus = putih+"["+hijau+"+"+putih+"]"+res
tasi = putih+"["+merah+"x"+putih+"]"+res
taku = putih+"["+kuning+"-"+putih+"]"+res
tase = "\r"+putih+"["+merah+"!"+putih+"]"+res
tata = "\r"+putih+"["+merah+"?"+putih+"]"+res
oke = "\r"+putih+"["+hijau+"✓"+putih+"]"+res
nok = "\r"+putih+"["+merah+"x"+putih+"]"+res
wok = "\r"+putih+"["+hijau+"▪"+putih+"]"+res
bana = "\r"+putih+"["+hijau+"➲"+putih+"]"+res
banb = "\r"+putih+"["+hijau+"➾"+putih+"]"+res
mes = ["\033[0;31m" ,"\033[1;31m","\033[0;32m","\033[1;32m","\033[0;33m","\033[1;33m","\033[0;34m","\033[1;34m","\033[0;35m","\033[1;35m","\033[0;36m","\033[1;36m","\033[0;37m","\033[1;37m"]
pamerah = kur3+merah+">>>"
pahijau = kur3+hijau+">>>"
pakuning = kur3+purple+"➢"
krg1=abu+'⟨'+res
krg2=abu+'⟩'+res

# Infura Project ID
infura_project_id = '59ad23946a7b4d57977e0ebe476348db'

def print_banner():
    os.system("clear")  # Membersihkan layar sebelum menampilkan banner
    banner = f"""
\t {merah} ██╗  ██╗██╗███╗   ██╗ ██████╗     ███████╗ ██████╗
\t {merah} ██║ ██╔╝██║████╗  ██║██╔════╝     ██╔════╝██╔════╝
\t {merah} █████╔╝ ██║██╔██╗ ██║██║  ███╗    ███████╗██║     
\t {putih} ██╔═██╗ ██║██║╚██╗██║██║   ██║    ╚════██║██║     
\t {putih} ██║  ██╗██║██║ ╚████║╚██████╔╝    ███████║╚██████╗
\t {putih} ╚═╝  ╚═╝╚═╝╚═╝  ╚═══╝ ╚═════╝     ╚══════╝ ╚═════╝
"""
    print(banner)
    print(f"{kuning}  \t Script to Send Native Coins or Tokens{res}")
    print(grs)

# Fungsi untuk memilih jaringan
def select_network():
    print(f"{pakuning} {kuning}Pilih jaringan:{res}")
    print(f"{pakuning} {cyan}[1] BSC{res}")
    print(f"{pakuning} {cyan}[2] ETH{res}")
    print(f"{pakuning} {cyan}[3] MATIC{res}")
    print(f"{pakuning} {cyan}[4] ETH BASE{res}")
    print(f"{pakuning} {cyan}[5] Fitur Kirim Token{res}")
    print(grs)
    choice = input(f"{pakuning} {kuning}Masukkan pilihan Anda : {res}")
    
    if choice == '1':
        return 'https://bsc-dataseed.binance.org/', 56, False
    elif choice == '2':
        return f'https://mainnet.infura.io/v3/{infura_project_id}', 1, False
    elif choice == '3':
        return f'https://polygon-mainnet.infura.io/v3/{infura_project_id}', 137, False
    elif choice == '4':
        return f'https://base-mainnet.infura.io/v3/{infura_project_id}', 8453, False
    elif choice == '5':
        print(f"{pakuning}{tase}{kuning} Pilih jaringan untuk mengirim token:{res}")
        print(f"{pakuning} {hijau}[1] BSC{res}")
        print(f"{pakuning} {hijau}[2] ETH{res}")
        print(f"{pakuning} {hijau}[3] MATIC{res}")
        print(f"{pakuning} {hijau}[4] ETH BASE{res}")
        token_choice = input(f"{tata}{kuning}Masukkan pilihan Anda (1-4): {res}")
        
        if token_choice == '1':
            return 'https://bsc-dataseed.binance.org/', 56, True
        elif token_choice == '2':
            return f'https://mainnet.infura.io/v3/{infura_project_id}', 1, True
        elif token_choice == '3':
            return f'https://polygon-mainnet.infura.io/v3/{infura_project_id}', 137, True
        elif token_choice == '4':
            return f'https://base-mainnet.infura.io/v3/{infura_project_id}', 8453, True
        else:
            print(f"{merah}Pilihan tidak valid. Menggunakan jaringan ETH sebagai default.{res}")
            return f'https://mainnet.infura.io/v3/{infura_project_id}', 1, True
    else:
        print(f"{merah}Pilihan tidak valid. Menggunakan jaringan ETH sebagai default.{res}")
        return f'https://mainnet.infura.io/v3/{infura_project_id}', 1, False

# Banner
print_banner()

# Memilih jaringan
network_url, chain_id, send_token = select_network()

# Koneksi ke node yang dipilih
w3 = Web3(Web3.HTTPProvider(network_url))

# Cek koneksi
if not w3.isConnected():
    print(f"{merah}Koneksi ke jaringan gagal{res}")
    exit()

# Private key Anda
private_key = '0x588889cf3521d159e9a5568e26aeaca03df0f1dc1010b93ff905db29062c34df'

# Alamat pengirim
account = w3.eth.account.from_key(private_key)
sender_address = account.address

# Membaca file dengan alamat
def read_recipients(file_path):
    recipients = []
    with open(file_path, 'r') as file:
        for line in file:
            line = line.strip()
            if line:  # Cek apakah baris tidak kosong
                recipients.append(line)
    return recipients

recipients = read_recipients('recipients.txt')

# Meminta jumlah yang akan dikirim
amount_input = input(f"{tase}{kuning}Masukkan jumlah yang akan dikirim : {res}")

# Jika mengirim token, minta contract address dan setup transaksi token
if send_token:
    token_contract_address = input(f"{tase}{kuning}Masukkan contract address token: {res}")
    token_abi = '[{"constant":false,"inputs":[{"name":"_to","type":"address"},{"name":"_value","type":"uint256"}],"name":"transfer","outputs":[{"name":"","type":"bool"}],"type":"function"},{"constant":true,"inputs":[],"name":"decimals","outputs":[{"name":"","type":"uint8"}],"type":"function"}]'
    token_contract = w3.eth.contract(address=token_contract_address, abi=token_abi)
    decimals = token_contract.functions.decimals().call()
    amount_wei = int(float(amount_input) * (10 ** decimals))  # Mengonversi jumlah sesuai dengan decimals token
else:
    amount_wei = w3.toWei(amount_input, 'ether')

# Mengirim transaksi
def send_transactions():
    nonce = w3.eth.getTransactionCount(sender_address)
    gas_price = w3.eth.gasPrice

    for address in recipients:
        if send_token:
            # Token transfer
            transaction = token_contract.functions.transfer(
                address, amount_wei
            ).buildTransaction({
                'chainId': chain_id,
                'gas': 70000,
                'gasPrice': gas_price,
                'nonce': nonce,
            })
        else:
            # Native coin transfer
            transaction = {
                'to': address,
                'value': amount_wei,
                'gas': 21000,
                'gasPrice': gas_price,
                'nonce': nonce,
                'chainId': chain_id
            }

        signed_tx = w3.eth.account.signTransaction(transaction, private_key)
        tx_hash = w3.eth.sendRawTransaction(signed_tx.rawTransaction)
        print(f"{oke}{hijau}Sukses Kirim: {res}{hijau} ke {res}{address} {hijau}for {res}{amount_input} {hijau}{'tokens' if send_token else 'ETH/MATIC/etc'}{res}")
        print(grs)
        time.sleep(2)

        nonce += 1

send_transactions()
